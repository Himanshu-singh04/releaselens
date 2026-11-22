"""Research only. Execute ONLY after exact-revision coordinator release; no CI hook."""
from decimal import Decimal, InvalidOperation
import contextlib
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys

import rfc8785

ROOT = Path(__file__).resolve().parents[2]
ORACLE = json.loads((ROOT / 'fixtures/b1d/oracle.json').read_text())
RETAINED = json.loads((ROOT / 'fixtures/b0b/vectors.json').read_text())
MIB = 1048576
SAFE = 9007199254740991
LIMITS = {'suite': 5 * MIB, 'bundle': 25 * MIB, 'artifact': MIB}


class Rejected(Exception):
    pass


def reject(code='E_SCHEMA'):
    raise Rejected(code)


def diagnostic(code, location):
    return {'code': code, 'location': location, 'message': ORACLE['diagnostics'][code]}


def number(token):
    exact = Decimal(token)
    if exact == exact.to_integral_value() and exact.copy_abs() > SAFE:
        reject()
    value = float(token)
    if not math.isfinite(value) or (value == 0 and exact != 0):
        reject()
    if value.is_integer():
        if abs(value) > SAFE:
            reject()
        return int(value)
    return value


def pairs(items):
    result = {}
    for key, value in items:
        key.encode('utf-8', errors='strict')
        if key in result:
            reject()
        result[key] = value
    return result


def valid_strings(value):
    if type(value) is str:
        value.encode('utf-8', errors='strict')
    elif type(value) is list:
        for child in value:
            valid_strings(child)
    elif type(value) is dict:
        for child in value.values():
            valid_strings(child)


def parse(raw, limit=25 * MIB):
    if type(raw) is not bytes or len(raw) > ORACLE['limits']['raw_bytes']:
        reject('E_LIMIT')
    if len(raw) > limit:
        reject('E_LIMIT')
    if raw.startswith(b'\xef\xbb\xbf'):
        reject()
    text = raw.decode('utf-8', errors='strict')
    quoted = escaped = False
    depth = 0
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in '[{':
            depth += 1
            if depth > 32:
                reject('E_LIMIT')
        elif char in ']}':
            depth -= 1
    value = json.loads(text, parse_int=number, parse_float=number,
                       parse_constant=lambda _: reject(), object_pairs_hook=pairs)
    valid_strings(value)
    return value


def token_span(raw, start):
    """Original byte offsets, before decoding. Caller supplies a known content offset."""
    while start < len(raw) and raw[start] in b' \t\r\n':
        start += 1
    quoted = escaped = False
    depth = 0
    for i in range(start, len(raw)):
        char = raw[i]
        if quoted:
            if escaped:
                escaped = False
            elif char == 92:
                escaped = True
            elif char == 34:
                quoted = False
                if depth == 0:
                    return start, i + 1
        elif char == 34:
            quoted = True
        elif char in b'[{':
            depth += 1
        elif char in b']}':
            if depth == 0:
                return start, i
            depth -= 1
            if depth == 0:
                return start, i + 1
        elif depth == 0 and char in b', \t\r\n':
            return start, i
    return start, len(raw)


def scalar(value):
    return type(value) in (str, bool, type(None), int)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bytes_record(data):
    record = {'length': len(data), 'sha256': sha(data)}
    if len(data) <= 512:
        record['hex'] = data.hex()
    return record


def types(value):
    if type(value) is list:
        return ['list', [types(v) for v in value]]
    if type(value) is dict:
        return ['dict', {k: types(v) for k, v in value.items()}]
    return type(value).__name__


def attempt(raw, limit=25 * MIB, dumps=rfc8785.dumps, location=None):
    if location is None:
        location = {'kind': 'input', 'input': 'suite', 'pointer': ''}
    try:
        value = parse(raw, limit)
        canonical = dumps(value)
        reparsed = parse(canonical)
        return {'value': value, 'canonical': canonical, 'reparsed': reparsed}
    except Rejected as error:
        return {'diagnostic': diagnostic(error.args[0], location)}
    except (ValueError, UnicodeError, InvalidOperation, OverflowError):
        return {'diagnostic': diagnostic('E_SCHEMA', location)}
    except Exception:
        return {'diagnostic': diagnostic('E_INTERNAL', None)}


def check_bytes(raw, expected=None, error=None, expected_type=None, limit=25 * MIB):
    calls = []

    def spy(value):
        calls.append(type(value).__name__)
        return rfc8785.dumps(value)

    result = attempt(raw, limit, spy)
    details = {'raw': bytes_record(raw), 'candidate_calls': len(calls)}
    if error:
        wanted = {'diagnostic': diagnostic(error, {'kind': 'input', 'input': 'suite', 'pointer': ''})}
        actual = result if 'diagnostic' in result else {
            'unexpected_accept': True, 'type': types(result['value']),
            'canonical': bytes_record(result['canonical'])}
        return result == wanted and not calls, {**details, 'expected': wanted, 'actual': actual}
    canonical = result.get('canonical')
    ok = canonical == expected
    details['expected'] = {'bytes': bytes_record(expected), 'type': expected_type}
    if canonical is None:
        return False, {**details, 'actual': result}
    before, after = types(result['value']), types(result['reparsed'])
    ok = ok and before == after and result['value'] == result['reparsed']
    if expected_type:
        ok = ok and before == expected_type
    return ok, {**details, 'actual': {'bytes': bytes_record(canonical), 'before': before, 'after': after}}


def roles(case):
    # Structural data, not Suite/Bundle schemas or evaluator implementation.
    raw_token = case['text'].encode()
    canonical_token = case['canon'].encode()
    template = b'{"actual":%s,"content":{"nested":[%s],"null":null},"expected":%s,"integer":%s,"subject":%s,"text":"%s"}'
    raw = template % ((raw_token,) * 6)
    expected = template % (((canonical_token,) * 5) + (raw_token,))
    ok, details = check_bytes(raw, expected)
    root_ok, root_details = check_bytes(raw_token, canonical_token, expected_type=case['type'])
    result = attempt(raw)
    if 'diagnostic' in result:
        return False, details
    states = []
    for value in [result['value'], result['reparsed']]:
        ok = ok and type(value['text']) is str and value['text'] == case['text'] and value['content']['null'] is None
        values = [value['actual'], value['content']['nested'][0], value['expected'],
                  value['integer'], value['subject']]
        state = [{'type': type(v).__name__, 'scalar': scalar(v), 'integer': type(v) is int,
                  'same_as_one': type(v) is int and v == 1} for v in values]
        wanted = {k: case[k] for k in ('type', 'scalar', 'integer', 'same_as_one')}
        ok = ok and state == [wanted] * 5
        states.append(state)
    # Required-field gates are narrow type gates, not schema validation.
    rejected = []
    for field in ('expected', 'subject', 'integer'):
        v = result['value'][field]
        allowed = type(v) is int if field == 'integer' else scalar(v)
        actual = None if allowed else diagnostic('E_SCHEMA', {'kind': 'input', 'input': 'suite', 'pointer': '/' + field})
        should_allow = case['integer'] if field == 'integer' else case['scalar']
        wanted = None if should_allow else diagnostic('E_SCHEMA', {'kind': 'input', 'input': 'suite', 'pointer': '/' + field})
        ok = ok and actual == wanted
        rejected.append({'field': field, 'expected': wanted, 'actual': actual})
    details.update(root=root_details, states=states, gates=rejected,
                   actual_type_compatible_with_integer_one=type(result['value']['actual']) is int)
    root_result = attempt(raw_token)
    semantic_one = 'canonical' in root_result and sha(root_result['canonical']) == sha(b'1')
    raw_one = sha(raw_token) == sha(b'1')
    ok = ok and semantic_one == case['same_as_one'] and raw_one == (case['text'] == '1')
    details['hash_relations'] = {'semantic_equals_integer_one': semantic_one,
                                'raw_equals_integer_one': raw_one,
                                'expected_semantic_equals_integer_one': case['same_as_one'],
                                'expected_raw_equals_integer_one': case['text'] == '1'}
    return ok and root_ok, details


def content_tokens(total, media):
    # At most one <=25MiB+1 raw input per check; each token <=1MiB.
    remaining = total
    tokens = []
    while remaining:
        count = min(remaining, MIB - 2 if media == 'text' else MIB)
        if media == 'json' and count < 2:
            # JSON numeric zero has one canonical byte, avoiding a negative string size.
            token = b'0'
        else:
            token = b'"' + b'a' * (count if media == 'text' else count - 2) + b'"'
        tokens.append(token)
        remaining -= count
    return tokens


def account(tokens, media):
    total = 0
    for token in tokens:
        start, end = token_span(token, 0)
        if end - start > MIB:
            reject('E_LIMIT')
        value = parse(token)
        if media == 'text' and type(value) is not str:
            reject()
        total += len(value.encode('utf-8')) if media == 'text' else len(rfc8785.dumps(value))
    return total, 'E_LIMIT' if total > 20 * MIB else 'ACCEPT'


def aggregate(case, total=None):
    total = 20 * MIB + case['delta'] if total is None else total
    tokens = content_tokens(total, case['media'])
    actual_total, component = account(tokens, case['media'])
    # Same IDs are intentionally reused when called for each owner/array.
    raw = b'{"artifacts":[' + b','.join(
        b'{"artifact_id":"a' + str(i).encode() + b'","content":' + token + b'}'
        for i, token in enumerate(tokens)) + b']}'
    assert len(raw) <= ORACLE['limits']['raw_bytes']
    suite_limit_applies = case['array'] == 'suite.artifacts' or '.suite_snapshot.' in case['array']
    bound = 5 * MIB if suite_limit_applies else 25 * MIB
    outer = attempt(raw, bound)
    envelope = outer.get('diagnostic', {}).get('code', component)
    bundle = None
    if '.suite_snapshot.' in case['array']:
        containing = b'{"suite_snapshot":' + raw + b'}'
        assert len(containing) <= ORACLE['limits']['raw_bytes']
        containing_result = attempt(containing, 25 * MIB)
        bundle = {'raw': bytes_record(containing),
                  'raw_parse_result': containing_result.get('diagnostic', {}).get('code', 'ACCEPT')}
    ok = actual_total == total and component == case['component'] and envelope == case['envelope']
    ok = ok and (bundle is None or bundle['raw_parse_result'] == 'ACCEPT')
    return ok, {
        'expected': {'decoded_bytes': total, 'component': case['component'], 'envelope': case['envelope']},
        'actual': {'decoded_bytes': actual_total, 'component': component, 'envelope': envelope},
        'array': case['array'], 'media': case['media'], 'raw': bytes_record(raw),
        'max_token': max(map(len, tokens)), 'containing_bundle_raw_fits': len(raw) <= 25 * MIB,
        'embedded_containing_bundle': bundle,
        'schema_or_full_envelope_qualification': False}


def run_case(case):
    kind = case['kind']
    if kind == 'binary64':
        value = struct.unpack('>d', bytes.fromhex(case['bits']))[0]
        try:
            actual = rfc8785.dumps(value)
        except rfc8785.CanonicalizationError:
            return case['canon'] is None, {'expected': case['canon'], 'actual': 'CanonicalizationError'}
        expected = case['canon'].encode() if case['canon'] is not None else None
        return actual == expected, {'expected': case['canon'], 'actual': bytes_record(actual), 'type': type(value).__name__}
    if kind == 'sample':
        sample = RETAINED['rfc_sample']
        if case['policy']:
            return check_bytes(sample['text'].encode(), error=case['error'])
        actual = rfc8785.dumps(json.loads(sample['text']))
        expected = bytes.fromhex(sample['canonical_hex'])
        return actual == expected, {'expected': bytes_record(expected), 'actual': bytes_record(actual)}
    if kind == 'retained':
        old = next(c for c in RETAINED['bytes'] if c['id'] == case['ref'])
        case = {**old, **case}
        kind = 'parse'
    if kind == 'parse':
        raw = bytes.fromhex(case['hex']) if 'hex' in case else case['text'].encode()
        return check_bytes(raw, case.get('canon', '').encode(), case.get('error'), case.get('type'))
    if kind == 'roles':
        return roles(case)
    if kind == 'raw-bound':
        label = case['envelope']
        size = LIMITS[label] + case['delta']
        if label == 'artifact':
            if case.get('spelling') == 'internal-whitespace':
                raw = b'[' + b' ' * (size - 3) + b'0]'
                expected = b'[0]'
            else:
                count, rest = divmod(size - 4, 6)
                raw = b'"' + b'\\u00e9' * count + b'a' * rest + b'\\"' + b'"'
                expected = b'"' + 'é'.encode() * count + b'a' * rest + b'\\"' + b'"'
            # Check original span; do not re-encode before the bound is applied.
            start, end = token_span(raw, 0)
            assert start == 0 and end == len(raw)
        else:
            expected = '"é"'.encode()
            raw = b' ' + expected + b' ' * (size - len(expected) - 1)
        assert len(raw) == size
        return check_bytes(raw, expected, case.get('error'), limit=LIMITS[label])
    if kind == 'aggregate':
        return aggregate(case)
    if kind == 'independent':
        records = []
        ok = True
        for array in case['arrays']:
            envelope = case['suite_envelope'] if array == 'suite.artifacts' or '.suite_snapshot.' in array else case['bundle_envelope']
            good, record = aggregate({'array': array, 'media': 'text', 'component': case['component'], 'envelope': envelope}, case['per_array'])
            ok = ok and good
            records.append(record)
        return ok, {'separate_arrays_reused_ids': records, 'combined_budget_not_applied': True}
    if kind == 'depth':
        opening, closing = (b'[', b']') if case['shape'] == 'array' else (b'{"a":', b'}')
        raw = opening * case['depth'] + b'"[{}]\\""' + closing * case['depth']
        return check_bytes(raw, raw, case.get('error'))
    if kind == 'span':
        raw = case['text'].encode()
        start, end = token_span(raw, raw.index(b':') + 1)
        value = parse(raw[start:end])
        actual = {'start': start, 'raw': end - start, 'json_bytes': len(rfc8785.dumps(value))}
        if 'text_bytes' in case:
            actual['text_bytes'] = len(value.encode())
        expected = {k: case[k] for k in actual}
        return actual == expected, {'expected': expected, 'actual': actual, 'envelope': bytes_record(raw)}
    if kind == 'diagnostic':
        def faulty(_):
            raise (ValueError if case['fault'] == 'ValueError' else RuntimeError)('SYNTHETIC_CANARY /private/path hostile-key')
        result = attempt(b'null', dumps=faulty, location={'kind': 'input', 'input': 'candidate', 'pointer': ''})
        expected = {'diagnostic': diagnostic(case['error'], case['location'])}
        return result == expected, {'expected': expected, 'actual': result}
    raise RuntimeError('Unknown reviewed recipe')


def legacy():
    """Observe original main's record return; never replace its lexical adapter/oracle."""
    path = ROOT / ORACLE['legacy']['adapter']
    spec = importlib.util.spec_from_file_location('b1d_unchanged_legacy', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    count = 0

    def observe(frame, event, arg):
        nonlocal count
        if event == 'return' and frame.f_code.co_name == 'record' and frame.f_code.co_filename == str(path):
            local = frame.f_locals
            row = {'id': local['identifier'], 'pass': bool(local['ok']),
                   'observed': local['observed'], **local['details']}
            count += 1
            sys.__stdout__.write(json.dumps({'legacy': row}, ensure_ascii=True) + '\n')
            sys.__stdout__.flush()
            if not row['pass']:
                raise SystemExit(1)
    sys.setprofile(observe)
    try:
        with contextlib.redirect_stdout(sys.stderr):
            code = module.main()
    finally:
        sys.setprofile(None)
    assert count == 105
    return code


def main():
    if sys.argv[1:] == ['legacy']:
        return legacy()
    identifier = sys.argv[1]
    cases = [{'id': 'RFC-' + name, 'kind': 'binary64', 'source': 'RFC', 'bits': bits, 'canon': canon}
             for name, bits, canon in RETAINED['binary64']] + ORACLE['checks']
    case = next(c for c in cases if c['id'] == identifier)
    ok, details = run_case(case)
    print(json.dumps({'id': identifier, 'pass': bool(ok), 'source': case['source'], **details}, ensure_ascii=True))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())

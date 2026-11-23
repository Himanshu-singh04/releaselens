"""In-memory Suite/Bundle validation; no I/O, evaluation, or evidence execution.

The wire contract is docs/evidence-contract.md. Numeric decoding adapts the
reviewed B1d N1/N2/N3 rules; historical research code is neither imported nor run.
"""
from datetime import datetime
from decimal import Decimal
import hashlib
import json
import math
import re

import rfc8785

MIB = 1048576
SAFE = 2**53 - 1
ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z')
HASH = re.compile(r'sha256:[0-9a-f]{64}\Z')
TIME = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z\Z')
STRING = re.compile(rb'"(?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))*"')
ATOM = re.compile(rb'(?:-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?|true|false|null)')
SPACE = re.compile(rb'[ \t\r\n]*')
MESSAGES = {
    'E_JSON': 'Invalid JSON input.', 'E_LIMIT': 'Input limit exceeded.',
    'E_SCHEMA': 'Invalid contract structure.', 'E_IDENTITY': 'Content identity mismatch.',
    'E_REFERENCE': 'Invalid evidence reference.', 'E_SOURCE': 'Inconsistent source metadata.',
    'E_TIME': 'Invalid time claim.', 'E_INTERNAL': 'Contract validation failed.',
}


class _Rejected(Exception):
    def __init__(self, code, path=()):
        self.code, self.path = code, path


def _require(condition, code='E_SCHEMA', path=()):
    if not condition:
        raise _Rejected(code, path)


def byte_hash(raw):
    return 'sha256:' + hashlib.sha256(raw).hexdigest()


def semantic_hash(value):
    """H of already normalized JSON, used internally after strict decoding."""
    return byte_hash(rfc8785.dumps(value))


def _number(token):
    # Decimal construction/comparison is exact and independent of context precision.
    exact = Decimal(token)
    _require(not (exact == exact.to_integral_value() and exact.copy_abs() > SAFE), 'E_JSON')
    value = float(token)
    _require(math.isfinite(value) and not (value == 0 and exact != 0), 'E_JSON')
    _require(not (value.is_integer() and abs(value) > SAFE), 'E_JSON')
    return int(value) if value.is_integer() else value


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        key.encode('utf-8', errors='strict')
        _require(key not in result, 'E_JSON')
        result[key] = value
    return result


def _unicode(value):
    if type(value) is str:
        value.encode('utf-8', errors='strict')
    elif type(value) is list:
        for child in value:
            _unicode(child)
    elif type(value) is dict:
        for child in value.values():
            _unicode(child)


class _Spans:
    """Grammar walk over actual bytes BEFORE JSON value decoding.

    No fixture offsets or re-encoding: escapes, whitespace and multibyte content
    count exactly as supplied. Retain only the bounded artifact content spans.
    """
    def __init__(self, raw):
        self.raw, self.contents = raw, {}

    def skip(self, index):
        return SPACE.match(self.raw, index).end()

    def string(self, index):
        match = STRING.match(self.raw, index)
        _require(match is not None, 'E_JSON')
        return match.end()

    def value(self, index, path=(), depth=0):
        start = index = self.skip(index)
        _require(index < len(self.raw), 'E_JSON')
        char = self.raw[index:index + 1]
        if char in (b'{', b'['):
            _require(depth < 32, 'E_LIMIT')
            end = b'}' if char == b'{' else b']'
            index = self.skip(index + 1)
            count = 0
            while self.raw[index:index + 1] != end:
                if char == b'{':
                    stop = self.string(index)
                    key = json.loads(self.raw[index:stop])
                    index = self.skip(stop)
                    _require(self.raw[index:index + 1] == b':', 'E_JSON')
                    index = self.skip(index + 1)
                else:
                    key = count
                    # Reject documented collection excess before full decoding.
                    limit = {'artifacts': 2000, 'cases': 1000, 'assertions': 20,
                             'events': 200}.get(path[-1] if path else None)
                    # Only schema containers, never arbitrary artifact JSON members.
                    in_content = any(p == 'content' for p in path)
                    if limit is not None and not in_content:
                        _require(count < limit, 'E_LIMIT')
                index = self.skip(self.value(index, (*path, key), depth + 1))
                count += 1
                if self.raw[index:index + 1] == end:
                    break
                _require(self.raw[index:index + 1] == b',', 'E_JSON')
                index = self.skip(index + 1)
                _require(self.raw[index:index + 1] != end, 'E_JSON')
            index += 1
        elif char == b'"':
            index = self.string(index)
        else:
            match = ATOM.match(self.raw, index)
            _require(match is not None, 'E_JSON')
            index = match.end()
        artifact_path = (len(path) == 3 and path[0] == 'artifacts') or (
            len(path) == 4 and path[:2] == ('suite_snapshot', 'artifacts'))
        if artifact_path and type(path[-2]) is int and path[-1] == 'content':
            _require(index - start <= MIB, 'E_LIMIT')
            self.contents[path] = (start, index)
        return index


def _decode(raw, owner):
    _require(type(raw) is bytes, 'E_JSON')
    _require(len(raw) <= (5 if owner == 'suite' else 25) * MIB, 'E_LIMIT')
    _require(not raw.startswith(b'\xef\xbb\xbf'), 'E_JSON')
    text = raw.decode('utf-8', errors='strict')
    spans = _Spans(raw)
    _require(spans.skip(spans.value(0)) == len(raw), 'E_JSON')
    value = json.loads(text, object_pairs_hook=_pairs, parse_int=_number,
                       parse_float=_number)
    _unicode(value)
    return value, spans.contents


def _fields(value, names, path):
    _require(type(value) is dict and set(value) == set(names.split()), path=path)


def _string(value, path, nullable=False):
    _require(type(value) is str or (nullable and value is None), path=path)


def _id(value, path):
    _require(type(value) is str and ID.fullmatch(value) is not None, path=path)


def _hash(value, path, nullable=False):
    _require((nullable and value is None) or
             (type(value) is str and HASH.fullmatch(value) is not None), path=path)


def _scalar(value, path):
    _require(type(value) in (str, bool, int, type(None)), path=path)


def _integer(value, path, minimum=0, maximum=SAFE):
    _require(type(value) is int and minimum <= value <= maximum, path=path)


def _array(value, path, maximum=None, minimum=0):
    _require(type(value) is list, path=path)
    _require(len(value) >= minimum, path=path)
    _require(maximum is None or len(value) <= maximum, 'E_LIMIT', path)


def _time(value, path):
    if value is None:
        return None
    _require(type(value) is str and TIME.fullmatch(value) is not None, 'E_TIME', path)
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        raise _Rejected('E_TIME', path) from None


def _unique(rows, key, path):
    seen = set()
    for index, row in enumerate(rows):
        value = row[key]
        _require(value not in seen, path=(*path, index, key))
        seen.add(value)


def _source(source, registry, path):
    _fields(source, 'source_id kind version digest', path)
    _id(source['source_id'], (*path, 'source_id'))
    _require(source['kind'] in ('policy', 'knowledge', 'prompt', 'model', 'tool',
                                'exporter', 'business_snapshot'), path=(*path, 'kind'))
    _string(source['version'], (*path, 'version'), nullable=True)
    _hash(source['digest'], (*path, 'digest'), nullable=True)
    identity = (source['kind'], source['version'], source['digest'])
    _require(registry.setdefault(source['source_id'], identity) == identity, 'E_SOURCE', path)


def _pointer(value, pointer, path):
    _require(type(pointer) is str and (pointer == '' or pointer.startswith('/')), 'E_REFERENCE', path)
    if pointer == '':
        return value
    for token in pointer[1:].split('/'):
        _require(re.search(r'~(?:[^01]|$)', token) is None, 'E_REFERENCE', path)
        token = token.replace('~1', '/').replace('~0', '~')
        if type(value) is dict:
            _require(token in value, 'E_REFERENCE', path)
            value = value[token]
        elif type(value) is list:
            _require(re.fullmatch(r'0|[1-9][0-9]*', token) is not None and
                     len(token) <= len(str(len(value))), 'E_REFERENCE', path)
            index = int(token)
            _require(index < len(value), 'E_REFERENCE', path)
            value = value[index]
        else:
            raise _Rejected('E_REFERENCE', path)
    return value


def _ref(ref, artifacts, path):
    _fields(ref, 'artifact_id pointer', path)
    _id(ref['artifact_id'], (*path, 'artifact_id'))
    _require(ref['artifact_id'] in artifacts, 'E_REFERENCE', path)
    artifact = artifacts[ref['artifact_id']]
    if artifact['media_type'] == 'text/plain':
        _require(ref['pointer'] is None, 'E_REFERENCE', (*path, 'pointer'))
        value = artifact['content']
    else:
        value = _pointer(artifact['content'], ref['pointer'], (*path, 'pointer'))
    return artifact, value


def _identity(value, field, expected, path):
    _hash(value[field], (*path, field))
    _require(value[field] == expected, 'E_IDENTITY', (*path, field))


def _without(value, field):
    return {key: child for key, child in value.items() if key != field}


def _artifacts(rows, registry, path):
    _array(rows, path, 2000)
    total = 0
    for index, artifact in enumerate(rows):
        p = (*path, index)
        _fields(artifact, 'artifact_id media_type content sha256 source captured_at redacted', p)
        _id(artifact['artifact_id'], (*p, 'artifact_id'))
        _require(artifact['media_type'] in ('text/plain', 'application/json'), path=(*p, 'media_type'))
        if artifact['media_type'] == 'text/plain':
            _string(artifact['content'], (*p, 'content'))
            content = artifact['content'].encode('utf-8')
        else:
            content = rfc8785.dumps(artifact['content'])
        total += len(content)
        _require(total <= 20 * MIB, 'E_LIMIT', path)
        _identity(artifact, 'sha256', byte_hash(content), p)
        _source(artifact['source'], registry, (*p, 'source'))
        _time(artifact['captured_at'], (*p, 'captured_at'))
        _require(type(artifact['redacted']) is bool, path=(*p, 'redacted'))
    _unique(rows, 'artifact_id', path)
    return {a['artifact_id']: a for a in rows}


def _assertion(assertion, registry, path):
    _fields(assertion, 'assertion_id kind operator expected effect', path)
    _id(assertion['assertion_id'], (*path, 'assertion_id'))
    _require(assertion['kind'] in ('value', 'effect'), path=(*path, 'kind'))
    _require(assertion['operator'] in ('equals', 'contains', 'not_contains'), path=(*path, 'operator'))
    _scalar(assertion['expected'], (*path, 'expected'))
    if assertion['operator'] != 'equals':
        _string(assertion['expected'], (*path, 'expected'))
    rule = assertion['effect']
    if assertion['kind'] == 'value':
        _require(rule is None, path=(*path, 'effect'))
        return
    p = (*path, 'effect')
    _require(assertion['operator'] == 'equals', path=(*path, 'operator'))
    _fields(rule, 'tool subject source_id source_version source_digest max_age_ms', p)
    _id(rule['tool'], (*p, 'tool'))
    _scalar(rule['subject'], (*p, 'subject'))
    _id(rule['source_id'], (*p, 'source_id'))
    _string(rule['source_version'], (*p, 'source_version'))
    _hash(rule['source_digest'], (*p, 'source_digest'))
    _integer(rule['max_age_ms'], (*p, 'max_age_ms'), 1, 86400000)
    identity = ('business_snapshot', rule['source_version'], rule['source_digest'])
    _require(registry.setdefault(rule['source_id'], identity) == identity, 'E_SOURCE', p)


def _suite(suite, path=()):
    _fields(suite, 'schema_version suite_id revision cases artifacts suite_hash', path)
    _require(suite['schema_version'] == '1', path=(*path, 'schema_version'))
    _id(suite['suite_id'], (*path, 'suite_id'))
    _string(suite['revision'], (*path, 'revision'))
    registry = {}
    artifacts = _artifacts(suite['artifacts'], registry, (*path, 'artifacts'))
    _array(suite['cases'], (*path, 'cases'), 1000, 1)
    for index, case in enumerate(suite['cases']):
        p = (*path, 'cases', index)
        _fields(case, 'case_id title input policy_refs assertions case_hash', p)
        _id(case['case_id'], (*p, 'case_id'))
        _string(case['title'], (*p, 'title'))
        artifact, _ = _ref(case['input'], artifacts, (*p, 'input'))
        bound = {artifact['artifact_id']: artifact}
        _array(case['policy_refs'], (*p, 'policy_refs'))
        for j, ref in enumerate(case['policy_refs']):
            artifact, _ = _ref(ref, artifacts, (*p, 'policy_refs', j))
            _require(artifact['source']['kind'] in ('policy', 'knowledge'), path=(*p, 'policy_refs', j))
            bound[artifact['artifact_id']] = artifact
        _array(case['assertions'], (*p, 'assertions'), 20, 1)
        for j, assertion in enumerate(case['assertions']):
            _assertion(assertion, registry, (*p, 'assertions', j))
        _unique(case['assertions'], 'assertion_id', (*p, 'assertions'))
        expected = semantic_hash({'definition': _without(case, 'case_hash'),
                                  'artifacts': [bound[key] for key in sorted(bound)]})
        _identity(case, 'case_hash', expected, p)
    _unique(suite['cases'], 'case_id', (*path, 'cases'))
    _identity(suite, 'suite_hash', semantic_hash(_without(suite, 'suite_hash')), path)
    return {case['case_id']: case for case in suite['cases']}


def _events(rows, artifacts, start, end, path):
    _array(rows, path, 200)
    times = {}
    for index, event in enumerate(rows):
        p = (*path, index)
        _require(type(event) is dict, path=p)
        kind = event.get('kind')
        fields = {
            'request': 'event_id kind seq occurred_at tool subject arguments',
            'completion': 'event_id kind seq occurred_at request_id status result',
            'effect': 'event_id kind seq occurred_at completion_id subject entity subject_pointer value_pointer',
        }
        _require(type(kind) is str and kind in fields, path=p)
        _fields(event, fields[kind], p)
        _id(event['event_id'], (*p, 'event_id'))
        _integer(event['seq'], (*p, 'seq'))
        stamp = _time(event['occurred_at'], (*p, 'occurred_at'))
        _require(stamp is None or ((start is None or stamp >= start) and
                                 (end is None or stamp <= end)), 'E_TIME', p)
        times[event['event_id']] = stamp
        if kind == 'request':
            _id(event['tool'], (*p, 'tool'))
            _scalar(event['subject'], (*p, 'subject'))
            _ref(event['arguments'], artifacts, (*p, 'arguments'))
        elif kind == 'completion':
            _id(event['request_id'], (*p, 'request_id'))
            _require(event['status'] in ('success', 'error'), path=(*p, 'status'))
            _ref(event['result'], artifacts, (*p, 'result'))
        else:
            _id(event['completion_id'], (*p, 'completion_id'))
            _scalar(event['subject'], (*p, 'subject'))
            _, entity = _ref(event['entity'], artifacts, (*p, 'entity'))
            for key in ('subject_pointer', 'value_pointer'):
                if event[key] is not None:
                    _pointer(entity, event[key], (*p, key))
    _unique(rows, 'event_id', path)
    _unique(rows, 'seq', path)
    events = {event['event_id']: event for event in rows}
    linked = set()
    for index, event in enumerate(rows):
        p = (*path, index)
        chain = [event]
        current = event
        while current['kind'] != 'request':
            key, kind = ('request_id', 'request') if current['kind'] == 'completion' else ('completion_id', 'completion')
            parent = events.get(current[key])
            _require(parent is not None and parent['kind'] == kind and parent['seq'] < current['seq'],
                     'E_REFERENCE', p)
            chain.append(parent)
            current = parent
        if event['kind'] != 'request':
            link = (event['kind'], chain[1]['event_id'])
            _require(link not in linked, 'E_REFERENCE', p)
            linked.add(link)
        known = [times[e['event_id']] for e in reversed(chain) if times[e['event_id']] is not None]
        _require(known == sorted(known), 'E_TIME', p)
    return events


def _bundle(bundle):
    _fields(bundle, 'schema_version bundle_id suite_snapshot provenance artifacts runs bundle_hash', ())
    _require(bundle['schema_version'] == '1', path=('schema_version',))
    _id(bundle['bundle_id'], ('bundle_id',))
    cases = _suite(bundle['suite_snapshot'], ('suite_snapshot',))
    registry = {}
    artifacts = _artifacts(bundle['artifacts'], registry, ('artifacts',))
    provenance = bundle['provenance']
    _fields(provenance, 'producer exported_at configuration', ('provenance',))
    _source(provenance['producer'], registry, ('provenance', 'producer'))
    _require(provenance['producer']['kind'] == 'exporter', path=('provenance', 'producer'))
    _time(provenance['exported_at'], ('provenance', 'exported_at'))
    _array(provenance['configuration'], ('provenance', 'configuration'))
    kinds = []
    for index, source in enumerate(provenance['configuration']):
        p = ('provenance', 'configuration', index)
        _source(source, registry, p)
        _require(source['kind'] in ('prompt', 'model', 'tool', 'knowledge'), path=p)
        kinds.append(source['kind'])
    _require(kinds.count('prompt') == kinds.count('model') == 1, path=('provenance', 'configuration'))
    _array(bundle['runs'], ('runs',), 1000)
    for index, run in enumerate(bundle['runs']):
        p = ('runs', index)
        _fields(run, 'run_id case_id case_hash started_at ended_at status error_code observations events', p)
        _id(run['run_id'], (*p, 'run_id'))
        _id(run['case_id'], (*p, 'case_id'))
        _require(run['case_id'] in cases, 'E_REFERENCE', (*p, 'case_id'))
        case = cases[run['case_id']]
        _identity(run, 'case_hash', case['case_hash'], p)
        start, end = (_time(run[key], (*p, key)) for key in ('started_at', 'ended_at'))
        _require(start is None or end is None or start <= end, 'E_TIME', p)
        _require(run['status'] in ('complete', 'error', 'timeout', 'skipped'), path=(*p, 'status'))
        if run['status'] in ('error', 'timeout'):
            _string(run['error_code'], (*p, 'error_code'))
        else:
            _require(run['error_code'] is None, path=(*p, 'error_code'))
        _array(run['observations'], (*p, 'observations'), 20)
        events = _events(run['events'], artifacts, start, end, (*p, 'events'))
        _require(run['status'] != 'skipped' or (not run['events'] and not run['observations']), path=p)
        assertions = {a['assertion_id']: a for a in case['assertions']}
        for j, observation in enumerate(run['observations']):
            q = (*p, 'observations', j)
            _fields(observation, 'assertion_id value effect_event_id', q)
            _id(observation['assertion_id'], (*q, 'assertion_id'))
            _require(observation['assertion_id'] in assertions, 'E_REFERENCE', q)
            if assertions[observation['assertion_id']]['kind'] == 'value':
                _require(observation['effect_event_id'] is None, path=q)
                if observation['value'] is not None:
                    _ref(observation['value'], artifacts, (*q, 'value'))
            else:
                _require(observation['value'] is None, path=q)
                event_id = observation['effect_event_id']
                if event_id is not None:
                    _id(event_id, (*q, 'effect_event_id'))
                    _require(event_id in events and events[event_id]['kind'] == 'effect', 'E_REFERENCE', q)
        _unique(run['observations'], 'assertion_id', (*p, 'observations'))
    _unique(bundle['runs'], 'run_id', ('runs',))
    _unique(bundle['runs'], 'case_id', ('runs',))
    _identity(bundle, 'bundle_hash', semantic_hash(_without(bundle, 'bundle_hash')), ())


def load(raw, owner='suite'):
    """Validate bytes for suite/baseline/candidate; return document+identities or diagnostic.

    No supplied identity is repaired. The returned normalized document is ordinary
    caller-owned data, not an immutable authorization token or an evaluated result.
    """
    if owner not in ('suite', 'baseline', 'candidate'):
        return {'diagnostic': {'code': 'E_SCHEMA', 'location': None, 'message': MESSAGES['E_SCHEMA']}}
    try:
        document, _ = _decode(raw, owner)
        if owner == 'suite':
            _suite(document)
        else:
            _bundle(document)
        field = 'suite_hash' if owner == 'suite' else 'bundle_hash'
        return {'document': document, 'byte_hash': byte_hash(raw), 'semantic_hash': document[field]}
    except _Rejected as error:
        code, path = error.code, error.path
    except (ValueError, UnicodeError, ArithmeticError):
        code, path = 'E_JSON', ()
    except Exception:
        code, path = 'E_INTERNAL', ()
    return {'diagnostic': {'code': code, 'location': {'kind': 'input', 'input': owner,
            'pointer': ''.join('/' + str(part) for part in path)}, 'message': MESSAGES[code]}}

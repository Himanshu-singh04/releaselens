"""Pure authoritative comparison over Contract-validated normalized documents.

No decoding or I/O. B3 evaluates only matching present runs; the authoritative
Suite supplies every expected row, assertion and denominator.
"""
from . import contract, evaluator


def _cases(suite):
    contract._fields(suite, 'schema_version suite_id revision cases artifacts suite_hash', ())
    if suite['schema_version'] != '1':
        raise ValueError
    contract._id(suite['suite_id'], ())
    contract._hash(suite['suite_hash'], ())
    cases = evaluator._index(suite['cases'], 'case_id')
    if not cases:
        raise ValueError
    registry = {}
    for case in cases.values():
        contract._fields(case, 'case_id title input policy_refs assertions case_hash', ())
        contract._id(case['case_id'], ())
        contract._hash(case['case_hash'], ())
        assertions = evaluator._index(case['assertions'], 'assertion_id')
        if not assertions:
            raise ValueError
        for assertion in assertions.values():
            contract._assertion(assertion, registry, ())
    return cases


def _bundle(bundle):
    contract._fields(bundle, 'schema_version bundle_id suite_snapshot provenance artifacts runs bundle_hash', ())
    if bundle['schema_version'] != '1':
        raise ValueError
    contract._hash(bundle['bundle_hash'], ())
    cases = _cases(bundle['suite_snapshot'])
    evaluator._index(bundle['runs'], 'run_id')
    runs = evaluator._index(bundle['runs'], 'case_id')
    for run in runs.values():
        contract._fields(run, 'run_id case_id case_hash started_at ended_at status error_code observations events', ())
        contract._id(run['run_id'], ())
        if run['case_hash'] != cases[run['case_id']]['case_hash'] or run['status'] not in (
                'complete', 'error', 'timeout', 'skipped'):
            raise ValueError
    return cases, runs


def _side(case, bundle, run, owner):
    identifiers = sorted((a['assertion_id'] for a in case['assertions']), key=evaluator._utf16)
    if run is None or run['case_hash'] != case['case_hash']:
        missing = run is None
        return {'presence': 'missing' if missing else 'changed',
                'run_id': None if missing else run['run_id'],
                'run_status': None if missing else run['status'], 'status': 'unknown',
                'outcomes': [{'assertion_id': identifier, 'status': 'unknown',
                              'reason': 'MISSING_CASE' if missing else 'CHANGED_CASE', 'citations': []}
                             for identifier in identifiers]}
    side = evaluator.evaluate_run(bundle, run['run_id'], owner)
    # Adapt the internal diagnostic at this boundary; never expose a partial Result.
    if 'diagnostic' in side:
        raise ValueError
    contract._fields(side, 'presence run_id run_status status outcomes', ())
    if type(side['outcomes']) is not list:
        raise TypeError
    for outcome in side['outcomes']:
        contract._fields(outcome, 'assertion_id status reason citations', ())
        if type(outcome['citations']) is not list or type(outcome['reason']) is not str:
            raise TypeError
    if (side['presence'] != 'present' or side['run_id'] != run['run_id'] or
            side['run_status'] != run['status'] or
            [o['assertion_id'] for o in side['outcomes']] != identifiers):
        raise ValueError
    statuses = {o['status'] for o in side['outcomes']}
    if not statuses <= {'pass', 'fail', 'unknown'}:
        raise ValueError
    aggregate = 'fail' if 'fail' in statuses else 'unknown' if 'unknown' in statuses else 'pass'
    if side['status'] != aggregate:
        raise ValueError
    return side


def _counts(rows, owner, extra, own_cases):
    keys = ('expected', 'pass', 'fail', 'unknown', 'missing', 'changed', 'extra', 'error', 'timeout', 'skipped')
    cases, assertions = ({key: 0 for key in keys} for _ in range(2))
    cases['extra'] = len(extra)
    assertions['extra'] = sum(len(own_cases[identifier]['assertions']) for identifier in extra)
    for row in rows:
        side = row[owner]
        size = len(side['outcomes'])
        cases['expected'] += 1
        assertions['expected'] += size
        cases[side['status']] += 1
        for outcome in side['outcomes']:
            assertions[outcome['status']] += 1
        for key in ('missing', 'changed'):
            if side['presence'] == key:
                cases[key] += 1
                assertions[key] += size
        for key in ('error', 'timeout', 'skipped'):
            if side['run_status'] == key:
                cases[key] += 1
                assertions[key] += size
    return cases, assertions


def compare(suite, baseline, candidate, evaluator_version):
    """Return the SDD {ok,value|error} envelope; inputs must already be validated.

    Version is an explicit JSON string, never read from ambient state. Guards
    protect comparison invariants, not an alternate public validation/import API.
    All returned collections are newly built (including B3's nested citations).
    """
    try:
        if type(evaluator_version) is not str:
            raise TypeError
        evaluator_version.encode('utf-8', errors='strict')
        contract._id(suite['suite_id'], ())
        for owner, bundle in (('baseline', baseline), ('candidate', candidate)):
            contract._id(bundle['suite_snapshot']['suite_id'], ())
            if bundle['suite_snapshot']['suite_id'] != suite['suite_id']:
                return {'ok': False, 'error': {'code': 'E_SUITE',
                        'location': {'kind': 'input', 'input': owner, 'pointer': '/suite_snapshot/suite_id'},
                        'message': 'Incompatible suite identifier.'}}
        expected = _cases(suite)
        own_baseline, baseline_runs = _bundle(baseline)
        own_candidate, candidate_runs = _bundle(candidate)
        rows = []
        deltas = {('pass', 'fail'): 'regression', ('fail', 'pass'): 'improvement',
                  ('pass', 'pass'): 'unchanged', ('fail', 'fail'): 'unchanged'}
        for identifier in sorted(expected, key=evaluator._utf16):
            case = expected[identifier]
            left = _side(case, baseline, baseline_runs.get(identifier), 'baseline')
            right = _side(case, candidate, candidate_runs.get(identifier), 'candidate')
            presence = (left['presence'], right['presence'])
            alignment = ('changed_definition' if 'changed' in presence else
                         'missing_both' if presence == ('missing', 'missing') else
                         'missing_baseline' if left['presence'] == 'missing' else
                         'missing_candidate' if right['presence'] == 'missing' else 'matched')
            delta = deltas.get((left['status'], right['status']), 'incomparable') if alignment == 'matched' else 'incomparable'
            rows.append({'case_id': identifier, 'alignment': alignment, 'baseline': left, 'candidate': right, 'delta': delta})
        extra_baseline = sorted(baseline_runs.keys() - expected.keys(), key=evaluator._utf16)
        extra_candidate = sorted(candidate_runs.keys() - expected.keys(), key=evaluator._utf16)
        case_counts, assertion_counts = {}, {}
        for owner, extra, own in (('baseline', extra_baseline, own_baseline), ('candidate', extra_candidate, own_candidate)):
            case_counts[owner], assertion_counts[owner] = _counts(rows, owner, extra, own)
        result = {'schema_version': '1', 'evaluator_version': evaluator_version,
                  'suite_hash': suite['suite_hash'], 'baseline_hash': baseline['bundle_hash'],
                  'candidate_hash': candidate['bundle_hash'], 'rows': rows,
                  'extra_baseline': extra_baseline, 'extra_candidate': extra_candidate,
                  'case_counts': case_counts, 'assertion_counts': assertion_counts,
                  'aligned_pairs': sum(row['alignment'] == 'matched' for row in rows)}
        result['result_hash'] = contract.semantic_hash(result)
        contract._hash(result['result_hash'], ())
        return {'ok': True, 'value': result}
    except Exception:
        return {'ok': False, 'error': {'code': 'E_INTERNAL', 'location': None, 'message': 'Comparison failed.'}}

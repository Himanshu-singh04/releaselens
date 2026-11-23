"""Pure present-run rules over Contract-validated, normalized Bundle values.

This internal primitive uses the run's own embedded case, not an authoritative
cross-suite alignment. Callers must retain the validated-input precondition.
Evidence and producer time/source claims are data, not execution or causal proof.
"""
from datetime import timedelta

from . import contract


def _utf16(value):
    return value.encode('utf-16-be')


def _ordered_citations(citations):
    def key(citation):
        ref = citation['ref']
        pointer = (0, b'') if ref['pointer'] is None else (1, _utf16(ref['pointer']))
        return (_utf16(citation['owner']), _utf16(citation['container']),
                _utf16(ref['artifact_id']), pointer, _utf16(citation['artifact_hash']))
    unique = {key(citation): citation for citation in citations}
    return [unique[k] for k in sorted(unique)]


def _citation(owner, artifact, pointer):
    # Fresh nested objects: mutations of returned citations cannot change inputs.
    return {'owner': owner, 'container': 'bundle',
            'ref': {'artifact_id': artifact['artifact_id'], 'pointer': pointer},
            'artifact_hash': artifact['sha256']}


def _index(rows, field):
    if type(rows) is not list:
        raise TypeError
    result = {row[field]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError
    return result


def _scalar(value):
    return type(value) in (str, bool, type(None)) or (
        type(value) is int and abs(value) <= contract.SAFE)


def _equal(left, right):
    return type(left) is type(right) and left == right


def _comparison(match, citations):
    return ('pass', 'MATCH', citations) if match else ('fail', 'MISMATCH', citations)


def _value(assertion, observation, artifacts, owner):
    artifact, actual = contract._ref(observation['value'], artifacts, ())
    expected = assertion['expected']
    if not _scalar(actual) or type(actual) is not type(expected):
        return 'unknown', 'TYPE_MISMATCH', []
    operator = assertion['operator']
    if operator == 'equals':
        match = _equal(actual, expected)
    elif operator == 'contains':
        match = expected in actual
    elif operator == 'not_contains':
        match = expected not in actual
    else:
        raise ValueError
    return _comparison(match, [_citation(owner, artifact, observation['value']['pointer'])])


def _effect(assertion, observation, events, artifacts, owner):
    effect = events[observation['effect_event_id']]
    completion = events[effect['completion_id']]
    request = events[completion['request_id']]
    if (effect['kind'], completion['kind'], request['kind']) != ('effect', 'completion', 'request'):
        raise ValueError
    artifact, entity = contract._ref(effect['entity'], artifacts, ())
    rule, source = assertion['effect'], artifact['source']
    ineligible = ('unknown', 'INELIGIBLE_EFFECT', [])
    if (completion['status'] != 'success' or request['tool'] != rule['tool'] or
            source['kind'] != 'business_snapshot' or
            (source['source_id'], source['version'], source['digest']) !=
            (rule['source_id'], rule['source_version'], rule['source_digest']) or
            artifact['media_type'] != 'application/json' or type(entity) is not dict):
        return ineligible
    selectors = (effect['subject_pointer'], effect['value_pointer'])
    # A raw slash delimits tokens; an escaped ~1 inside a token does not.
    if any(p is None or not p.startswith('/') or p.count('/') != 1 for p in selectors):
        return ineligible
    subject, actual = (contract._pointer(entity, p, ()) for p in selectors)
    if not _scalar(subject) or not _scalar(actual) or not all(
            _equal(subject, claim) for claim in (rule['subject'], request['subject'], effect['subject'])):
        return ineligible
    completed, occurred, captured = (contract._time(value, ()) for value in
        (completion['occurred_at'], effect['occurred_at'], artifact['captured_at']))
    if completed is None or occurred is None or captured is None:
        return ineligible
    # Integer-millisecond timedelta comparison, including rollover/year9999.
    # Subtraction avoids overflowing datetime when adding the allowed window.
    if not (completed <= occurred <= captured and
            captured - completed <= timedelta(milliseconds=rule['max_age_ms'])):
        return ineligible
    citations = [_citation(owner, artifact, effect['entity']['pointer'] + p) for p in selectors]
    return _comparison(_equal(actual, assertion['expected']), citations)


def evaluate_run(bundle, run_id, owner):
    """Return one present Side, or a fixed null-location E_INTERNAL diagnostic.

    No decoding, hashing, I/O, clock reads, event execution or mutation. Bundle
    must already have passed Contract; this is not a second validation API.
    Small caller/invariant guards prevent missing/empty/malformed sets from
    becoming vacuous success. Internal exceptions discard the entire result.
    """
    try:
        if owner not in ('baseline', 'candidate'):
            raise ValueError
        run = _index(bundle['runs'], 'run_id')[run_id]
        case = _index(bundle['suite_snapshot']['cases'], 'case_id')[run['case_id']]
        if run['case_hash'] != case['case_hash']:
            raise ValueError
        assertions = _index(case['assertions'], 'assertion_id')
        if not assertions:
            raise ValueError
        registry = {}
        for assertion in assertions.values():
            contract._assertion(assertion, registry, ())
        run_reason = {'error': 'RUN_ERROR', 'timeout': 'RUN_TIMEOUT', 'skipped': 'RUN_SKIPPED'}
        if run['status'] not in ('complete', *run_reason):
            raise ValueError
        if run['status'] == 'complete':
            artifacts = _index(bundle['artifacts'], 'artifact_id')
            observations = _index(run['observations'], 'assertion_id')
            events = _index(run['events'], 'event_id')
        outcomes = []
        for identifier in sorted(assertions, key=_utf16):
            assertion = assertions[identifier]
            if run['status'] != 'complete':
                status, reason, citations = 'unknown', run_reason[run['status']], []
            else:
                observation = observations.get(identifier)
                field = 'value' if assertion['kind'] == 'value' else 'effect_event_id'
                if observation is None or observation[field] is None:
                    status, reason, citations = 'unknown', 'MISSING_EVIDENCE', []
                elif assertion['kind'] == 'value':
                    status, reason, citations = _value(assertion, observation, artifacts, owner)
                else:
                    status, reason, citations = _effect(assertion, observation, events, artifacts, owner)
            outcomes.append({'assertion_id': identifier, 'status': status, 'reason': reason,
                             'citations': _ordered_citations(citations)})
        statuses = {outcome['status'] for outcome in outcomes}
        aggregate = 'fail' if 'fail' in statuses else 'unknown' if 'unknown' in statuses else 'pass'
        return {'presence': 'present', 'run_id': run['run_id'], 'run_status': run['status'],
                'status': aggregate, 'outcomes': outcomes}
    except Exception:
        return {'diagnostic': {'code': 'E_INTERNAL', 'location': None, 'message': 'Run evaluation failed.'}}

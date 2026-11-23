"""B4 oracles authored from contract177–205/220–240/255–259 and B1 paper.

Expected rows/counts/citations precede compare execution; no generated goldens.
Small test-only definitions use the unchanged independent B2 encoding recipe.
All semantic mutations are resealed and accepted by Contract first.
"""
import copy
import itertools
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
import fixture_source as ref
from releaselens import contract as c
from releaselens import comparison as m

VERSION = 'b4-test-v1'
INTERNAL = {'ok': False, 'error': {'code': 'E_INTERNAL', 'location': None, 'message': 'Comparison failed.'}}


def fixture(name):
    return json.loads((ROOT / 'fixtures/b2' / (name + '.json')).read_bytes())


def counts(expected, **values):
    result = dict(expected=expected, **{k: 0 for k in
        ('pass', 'fail', 'unknown', 'missing', 'changed', 'extra', 'error', 'timeout', 'skipped')})
    result.update(values)
    return result


def citation(bundle, owner, identifier, pointer):
    artifact = next(a for a in bundle['artifacts'] if a['artifact_id'] == identifier)
    digest = ref.digest(artifact['content'].encode()) if artifact['media_type'] == 'text/plain' else ref.H(artifact['content'])
    return {'owner': owner, 'container': 'bundle', 'ref': {'artifact_id': identifier, 'pointer': pointer},
            'artifact_hash': digest}


def outcome(identifier, status, reason, citations=()):
    return {'assertion_id': identifier, 'status': status, 'reason': reason, 'citations': list(citations)}


def side(outcomes, status, run_id, run_status='complete', presence='present'):
    return {'presence': presence, 'run_id': run_id, 'run_status': run_status, 'status': status, 'outcomes': outcomes}


def row(identifier, left, right, alignment='matched', delta='unchanged'):
    return {'case_id': identifier, 'alignment': alignment, 'baseline': left, 'candidate': right, 'delta': delta}


def result(suite, baseline, candidate, rows, case_counts, assertion_counts, aligned,
           extras=((), ()), version=VERSION):
    value = {'schema_version': '1', 'evaluator_version': version, 'suite_hash': suite['suite_hash'],
             'baseline_hash': baseline['bundle_hash'], 'candidate_hash': candidate['bundle_hash'],
             'rows': rows, 'extra_baseline': list(extras[0]), 'extra_candidate': list(extras[1]),
             'case_counts': case_counts, 'assertion_counts': assertion_counts, 'aligned_pairs': aligned}
    value['result_hash'] = ref.H(value)  # Independent stdlib restricted JCS, not Contract's helper.
    return value


def small_suite(definitions):
    suite = fixture('suite')
    template = suite['cases'][3]
    suite['cases'] = []
    for identifier, assertions in definitions.items():
        case = copy.deepcopy(template)
        case.update(case_id=identifier, title='B4 test-only definition', assertions=[
            {'assertion_id': a, 'kind': 'value', 'operator': 'equals', 'expected': 'yes', 'effect': None}
            for a in assertions])
        suite['cases'].append(case)
    return ref.seal_suite(suite)


def small_bundle(suite, states=None):
    bundle = fixture('baseline')
    bundle['suite_snapshot'] = copy.deepcopy(suite)
    src = copy.deepcopy(bundle['provenance']['configuration'][1])
    bundle['artifacts'] = [ref.artifact('observed', {'pass': 'yes', 'fail': 'no', 'wrong': True}, src)]
    bundle['runs'] = []
    for case in suite['cases']:
        statuses = (states or {}).get(case['case_id'], ['pass'] * len(case['assertions']))
        if statuses is None:
            continue
        assert len(statuses) == len(case['assertions'])
        observations = [{'assertion_id': a['assertion_id'], 'effect_event_id': None,
                         'value': None if status == 'unknown' else ref.ref('observed', '/' + status)}
                        for a, status in zip(case['assertions'], statuses)]
        bundle['runs'].append({'run_id': 'run-' + case['case_id'], 'case_id': case['case_id'],
                              'case_hash': case['case_hash'], 'started_at': None, 'ended_at': None,
                              'status': 'complete', 'error_code': None, 'events': [], 'observations': observations})
    return ref.seal_bundle(bundle)


def tiny(definitions=None, left=None, right=None):
    suite = small_suite(definitions or {'A': ['a1']})
    return suite, small_bundle(suite, left), small_bundle(suite, right)


def ordinary(bundle, owner, case_id, identifiers, statuses, aggregate):
    rows = []
    for identifier, status in zip(identifiers, statuses):
        reason = {'pass': 'MATCH', 'fail': 'MISMATCH', 'unknown': 'MISSING_EVIDENCE', 'wrong': 'TYPE_MISMATCH'}[status]
        citations = [] if status in ('unknown', 'wrong') else [citation(bundle, owner, 'observed', '/' + status)]
        rows.append(outcome(identifier, 'unknown' if status == 'wrong' else status, reason, citations))
    return side(sorted(rows, key=lambda o: o['assertion_id']), aggregate, 'run-' + case_id)


def synthetic(identifiers, presence, case_id='A', run_status='complete'):
    reason = 'MISSING_CASE' if presence == 'missing' else 'CHANGED_CASE'
    return side([outcome(a, 'unknown', reason) for a in sorted(identifiers)], 'unknown',
                None if presence == 'missing' else 'run-' + case_id,
                None if presence == 'missing' else run_status, presence)


def gaps(value, owner):
    return {reason: sum(o['status'] == 'unknown' and o['reason'] == reason
                       for r in value['rows'] for o in r[owner]['outcomes'])
            for reason in ('MISSING_EVIDENCE', 'TYPE_MISMATCH', 'INELIGIBLE_EFFECT')}


def fixed_expected(suite, baseline, candidate, version=VERSION):
    left = [('pass', 'MATCH')] * 8
    left[2] = ('fail', 'MISMATCH')
    right = [('pass', 'MATCH'), ('fail', 'MISMATCH'), ('pass', 'MATCH'),
             ('unknown', 'MISSING_EVIDENCE'), ('unknown', 'INELIGIBLE_EFFECT'),
             ('unknown', 'INELIGIBLE_EFFECT'), ('unknown', 'MISSING_CASE'), ('unknown', 'CHANGED_CASE')]
    deltas = ['unchanged', 'regression', 'improvement'] + ['incomparable'] * 5
    rows = []
    for index in range(8):
        n, cid = index + 1, f'C{index + 1:02}'
        sides = []
        for owner, bundle, expected in [('baseline', baseline, left), ('candidate', candidate, right)]:
            status, reason = expected[index]
            if status == 'unknown':
                citations = []
            elif n in (4, 8):
                citations = [citation(bundle, owner, 'reply-' + cid, None)]
            else:
                citations = [citation(bundle, owner, 'record-' + cid, p)
                             for p in ('/order_id', '/ticket_state' if n == 3 else '/refund_state')]
            presence = 'missing' if owner == 'candidate' and n == 7 else 'changed' if owner == 'candidate' and n == 8 else 'present'
            sides.append(side([outcome('a1', status, reason, citations)], status,
                              None if presence == 'missing' else ('B-' if owner == 'baseline' else 'C-') + cid,
                              None if presence == 'missing' else 'complete', presence))
        rows.append(row(cid, *sides, alignment='missing_candidate' if n == 7 else 'changed_definition' if n == 8 else 'matched',
                        delta=deltas[index]))
    totals = {'baseline': counts(8, **{'pass': 7, 'fail': 1}),
              'candidate': counts(8, **{'pass': 2, 'fail': 1, 'unknown': 5, 'missing': 1, 'changed': 1})}
    return result(suite, baseline, candidate, rows, totals, copy.deepcopy(totals), 6, version=version)


class ComparisonTests(unittest.TestCase):
    def validated(self, inputs):
        suite, baseline, candidate = inputs
        ref.seal_suite(suite)
        ref.seal_bundle(baseline)
        ref.seal_bundle(candidate)
        normalized = []
        for owner, doc in zip(('suite', 'baseline', 'candidate'), inputs):
            raw = ref.canonical(doc)
            self.assertLess(len(raw), 150000)
            imported = c.load(raw, owner)
            self.assertNotIn('diagnostic', imported, owner)
            normalized.append(imported['document'])
        return normalized

    def compare(self, inputs, expected=None, version=VERSION):
        normalized = self.validated(inputs)
        before = copy.deepcopy(normalized)
        actual = m.compare(*normalized, version)
        self.assertEqual(set(actual), {'ok', 'value'})
        self.assertIs(actual['ok'], True)
        self.assertEqual(normalized, before)
        value = actual['value']
        self.assertEqual(value['result_hash'], ref.H({k: v for k, v in value.items() if k != 'result_hash'}))
        self.assertEqual(set(value), {'schema_version', 'evaluator_version', 'suite_hash', 'baseline_hash', 'candidate_hash',
                                     'rows', 'extra_baseline', 'extra_candidate', 'case_counts', 'assertion_counts',
                                     'aligned_pairs', 'result_hash'})
        if expected is not None:
            self.assertEqual(value, expected)
        return value

    def test_full_eight_row_paper_oracle_counts_coverage_gaps_and_identity(self):
        inputs = [fixture(n) for n in ('suite', 'baseline', 'candidate')]
        expected = fixed_expected(*inputs)
        actual = self.compare(inputs, expected)
        self.assertEqual({d: sum(r['delta'] == d for r in actual['rows']) for d in
                          ('regression', 'improvement', 'unchanged', 'incomparable')},
                         {'regression': 1, 'improvement': 1, 'unchanged': 1, 'incomparable': 5})
        for level in ('case_counts', 'assertion_counts'):
            self.assertEqual([(actual[level][o]['pass'] + actual[level][o]['fail'], actual[level][o]['expected'])
                              for o in ('baseline', 'candidate')], [(8, 8), (3, 8)])
        self.assertEqual(gaps(actual, 'candidate'), {'MISSING_EVIDENCE': 1, 'TYPE_MISMATCH': 0, 'INELIGIBLE_EFFECT': 2})
        self.assertEqual(gaps(actual, 'baseline'), {'MISSING_EVIDENCE': 0, 'TYPE_MISMATCH': 0, 'INELIGIBLE_EFFECT': 0})

    def test_all_nine_status_pairs_and_unknowns_are_aligned(self):
        pairs = [('pass', 'pass', 'unchanged'), ('pass', 'fail', 'regression'), ('pass', 'unknown', 'incomparable'),
                 ('fail', 'pass', 'improvement'), ('fail', 'fail', 'unchanged'), ('fail', 'unknown', 'incomparable'),
                 ('unknown', 'pass', 'incomparable'), ('unknown', 'fail', 'incomparable'), ('unknown', 'unknown', 'incomparable')]
        for left, right, delta in pairs:
            with self.subTest(left=left, right=right):
                inputs = tiny(left={'A': [left]}, right={'A': [right]})
                s, b, d = inputs
                rows = [row('A', ordinary(b, 'baseline', 'A', ['a1'], [left], left),
                            ordinary(d, 'candidate', 'A', ['a1'], [right], right), delta=delta)]
                totals = {'baseline': counts(1, **{left: 1}), 'candidate': counts(1, **{right: 1})}
                self.compare(inputs, result(s, b, d, rows, totals, copy.deepcopy(totals), 1))

    def test_missing_changed_and_row_precedence_use_authoritative_assertions(self):
        # Old snapshot has THREE other IDs, authority has TWO. Missing run wins
        # over old snapshot; changed row wins over the other side being missing.
        for left, right in itertools.product(('present', 'missing', 'changed'), repeat=2):
            with self.subTest(left=left, right=right):
                s, b, d = tiny({'A': ['a2', 'a10']})
                sides, case_totals, assertion_totals = [], {}, {}
                for owner, bundle, presence in [('baseline', b, left), ('candidate', d, right)]:
                    if presence != 'present':
                        old = small_suite({'A': ['old1', 'old2', 'old3']})
                        bundle.clear(); bundle.update(small_bundle(old, {'A': None} if presence == 'missing' else None))
                        sides.append(synthetic(['a2', 'a10'], presence))
                        case_totals[owner] = counts(1, unknown=1, **{presence: 1})
                        assertion_totals[owner] = counts(2, unknown=2, **{presence: 2})
                    else:
                        sides.append(ordinary(bundle, owner, 'A', ['a2', 'a10'], ['pass', 'pass'], 'pass'))
                        case_totals[owner] = counts(1, **{'pass': 1})
                        assertion_totals[owner] = counts(2, **{'pass': 2})
                self.validated((s, b, d))
                alignment = 'changed_definition' if 'changed' in (left, right) else (
                    'missing_both' if left == right == 'missing' else 'missing_baseline' if left == 'missing' else
                    'missing_candidate' if right == 'missing' else 'matched')
                expected = result(s, b, d, [row('A', *sides, alignment, 'unchanged' if alignment == 'matched' else 'incomparable')],
                                  case_totals, assertion_totals, int(alignment == 'matched'))
                actual = self.compare((s, b, d), expected)
                self.assertEqual(gaps(actual, 'candidate'), {'MISSING_EVIDENCE': 0, 'TYPE_MISMATCH': 0, 'INELIGIBLE_EFFECT': 0})

    def test_changed_run_status_overlaps_use_authoritative_counts(self):
        for owner in ('baseline', 'candidate'):
            for run_status in ('error', 'timeout', 'skipped'):
                s, b, d = tiny({'A': ['a1', 'a2']})
                old = small_bundle(small_suite({'A': ['old']}))
                old['runs'][0].update(status=run_status, error_code=None if run_status == 'skipped' else 'CANARY')
                if run_status == 'skipped':
                    old['runs'][0].update(events=[], observations=[])
                if owner == 'baseline':
                    b = old
                else:
                    d = old
                actual = self.compare((s, b, d))
                self.assertEqual(actual['rows'][0][owner], synthetic(['a1', 'a2'], 'changed', run_status=run_status))
                self.assertEqual(actual['rows'][0]['alignment'], 'changed_definition')
                self.assertEqual(actual['rows'][0]['delta'], 'incomparable')
                self.assertEqual(actual['case_counts'][owner], counts(1, unknown=1, changed=1, **{run_status: 1}))
                self.assertEqual(actual['assertion_counts'][owner], counts(2, unknown=2, changed=2, **{run_status: 2}))
                other = 'candidate' if owner == 'baseline' else 'baseline'
                self.assertEqual(actual['case_counts'][other], counts(1, **{'pass': 1}))
                self.assertEqual(actual['assertion_counts'][other], counts(2, **{'pass': 2}))
                self.assertEqual(actual['aligned_pairs'], 0)

    def test_extras_on_either_or_both_sides_and_snapshot_only_cases(self):
        for owners in (('baseline',), ('candidate',), ('baseline', 'candidate')):
            s, b, d = tiny()
            extra_counts = {}
            for owner, bundle in [('baseline', b), ('candidate', d)]:
                if owner in owners:
                    count = 2 if owner == 'baseline' else 3
                    own = small_suite({'Z': ['z'], 'A': ['a1'], 'X': [f'x{i}' for i in range(count)], 'snapshot-only': ['s1', 's2']})
                    bundle.clear(); bundle.update(small_bundle(own, {'snapshot-only': None}))
                    for run in bundle['runs']:
                        if run['case_id'] != 'A':
                            run.update(status='error', error_code='EXTRA_ERROR')
                    extra_counts[owner] = (2, count + 1)
                else:
                    extra_counts[owner] = (0, 0)
            actual = self.compare((s, b, d))
            self.assertEqual([r['case_id'] for r in actual['rows']], ['A'])
            self.assertEqual(actual['aligned_pairs'], 1)
            for owner in ('baseline', 'candidate'):
                self.assertEqual(actual['extra_' + owner], ['X', 'Z'] if owner in owners else [])
                self.assertEqual(actual['case_counts'][owner], counts(1, **{'pass': 1, 'extra': extra_counts[owner][0]}))
                self.assertEqual(actual['assertion_counts'][owner], counts(1, **{'pass': 1, 'extra': extra_counts[owner][1]}))

    def test_suite_hash_differences_are_compatible_but_ids_are_fatal_baseline_first(self):
        s, b, d = tiny()
        b['suite_snapshot']['revision'] = 'other-revision'
        d['suite_snapshot']['artifacts'].reverse()
        actual = self.compare((s, b, d))
        self.assertNotEqual(s['suite_hash'], b['suite_snapshot']['suite_hash'])
        self.assertNotEqual(s['suite_hash'], d['suite_snapshot']['suite_hash'])
        self.assertEqual(actual['rows'][0]['alignment'], 'matched')
        for owners in (('baseline',), ('candidate',), ('baseline', 'candidate')):
            s, b, d = tiny()
            for owner, bundle in [('baseline', b), ('candidate', d)]:
                if owner in owners:
                    bundle['suite_snapshot']['suite_id'] = 'other-suite'
            inputs = self.validated((s, b, d))
            self.assertEqual(m.compare(*inputs, VERSION), {'ok': False, 'error': {
                'code': 'E_SUITE', 'location': {'kind': 'input', 'input': owners[0], 'pointer': '/suite_snapshot/suite_id'},
                'message': 'Incompatible suite identifier.'}})

    def test_matching_run_statuses_and_multi_assertion_count_conservation(self):
        for status, reason in [('error', 'RUN_ERROR'), ('timeout', 'RUN_TIMEOUT'), ('skipped', 'RUN_SKIPPED')]:
            s, b, d = tiny({'A': ['a1', 'a2']})
            for bundle in (b, d):
                bundle['runs'][0].update(status=status, error_code=None if status == 'skipped' else 'ERROR')
                if status == 'skipped':
                    bundle['runs'][0].update(events=[], observations=[])
            actual = self.compare((s, b, d))
            self.assertEqual(actual['aligned_pairs'], 1)
            for owner in ('baseline', 'candidate'):
                self.assertEqual(actual['rows'][0][owner], side([outcome(a, 'unknown', reason) for a in ('a1', 'a2')],
                                                              'unknown', 'run-A', status))
                self.assertEqual(actual['case_counts'][owner], counts(1, unknown=1, **{status: 1}))
                self.assertEqual(actual['assertion_counts'][owner], counts(2, unknown=2, **{status: 2}))
        for statuses, aggregate, totals in [(['pass', 'pass'], 'pass', {'pass': 2}),
                                           (['pass', 'unknown'], 'unknown', {'pass': 1, 'unknown': 1}),
                                           (['fail', 'unknown'], 'fail', {'fail': 1, 'unknown': 1}),
                                           (['unknown', 'unknown'], 'unknown', {'unknown': 2})]:
            s, b, d = tiny({'A': ['a2', 'a1']}, {'A': statuses}, {'A': statuses})
            actual = self.compare((s, b, d))
            for owner, bundle in [('baseline', b), ('candidate', d)]:
                self.assertEqual(actual['rows'][0][owner], ordinary(bundle, owner, 'A', ['a2', 'a1'], statuses, aggregate))
                self.assertEqual(actual['case_counts'][owner], counts(1, **{aggregate: 1}))
                self.assertEqual(actual['assertion_counts'][owner], counts(2, **totals))
                self.assertEqual(sum(actual['assertion_counts'][owner][k] for k in ('pass', 'fail', 'unknown')), 2)

    def test_duplicate_attempts_are_contract_rejection_not_last_run_wins(self):
        for duplicate_id in (True, False):
            _, bundle, _ = tiny()
            duplicate = copy.deepcopy(bundle['runs'][0])
            if not duplicate_id:
                duplicate['run_id'] = 'another-run'
            bundle['runs'].append(duplicate)
            imported = c.load(ref.canonical(ref.seal_bundle(bundle)), 'baseline')
            self.assertEqual(imported['diagnostic']['code'], 'E_SCHEMA')
            self.assertEqual(imported['diagnostic']['location']['pointer'], '/runs/1/' + ('run_id' if duplicate_id else 'case_id'))
            self.assertNotIn('document', imported)

    def test_r4_three_case_gaps_and_separate_type_mismatch_control(self):
        suite = fixture('suite')
        suite['cases'] = [case for case in suite['cases'] if case['case_id'] in ('C01', 'C05', 'C06')]
        bundle = fixture('baseline')
        bundle['suite_snapshot'] = copy.deepcopy(suite)
        bundle['runs'] = [run for run in bundle['runs'] if run['case_id'] in ('C01', 'C05', 'C06')]
        bundle['runs'][0]['events'] = bundle['runs'][0]['events'][:1]
        bundle['runs'][0]['observations'][0]['effect_event_id'] = None
        bundle['runs'][1].update(status='error', error_code='ERROR')
        next(a for a in bundle['artifacts'] if a['artifact_id'] == 'record-C06')['captured_at'] = '2026-01-01T12:01:02.001Z'
        actual = self.compare((suite, bundle, copy.deepcopy(bundle)))
        self.assertEqual(actual['aligned_pairs'], 3)
        for owner in ('baseline', 'candidate'):
            self.assertEqual(actual['case_counts'][owner], counts(3, unknown=3, error=1))
            self.assertEqual(actual['assertion_counts'][owner], counts(3, unknown=3, error=1))
            self.assertEqual(gaps(actual, owner), {'MISSING_EVIDENCE': 1, 'TYPE_MISMATCH': 0, 'INELIGIBLE_EFFECT': 1})
            self.assertEqual([r[owner]['outcomes'][0]['reason'] for r in actual['rows']],
                             ['MISSING_EVIDENCE', 'RUN_ERROR', 'INELIGIBLE_EFFECT'])
            self.assertEqual(actual['case_counts'][owner]['pass'] + actual['case_counts'][owner]['fail'], 0)
        actual = self.compare(tiny(left={'A': ['wrong']}, right={'A': None}))
        self.assertEqual(gaps(actual, 'baseline'), {'MISSING_EVIDENCE': 0, 'TYPE_MISMATCH': 1, 'INELIGIBLE_EFFECT': 0})
        self.assertEqual(gaps(actual, 'candidate'), {'MISSING_EVIDENCE': 0, 'TYPE_MISMATCH': 0, 'INELIGIBLE_EFFECT': 0})

    def test_ten_pure_comparisons_independent_hash_and_version_only_change(self):
        inputs = self.validated([fixture(n) for n in ('suite', 'baseline', 'candidate')])
        expected = fixed_expected(*inputs)
        before = copy.deepcopy(inputs)
        for _ in range(10):
            self.assertEqual(m.compare(*inputs, VERSION), {'ok': True, 'value': expected})
        self.assertEqual(inputs, before)
        version = 'b4-explicit-v2 \n\U0001f600'
        second = m.compare(*inputs, version)
        self.assertEqual(second, {'ok': True, 'value': fixed_expected(*inputs, version=version)})
        self.assertNotEqual(second['value']['result_hash'], expected['result_hash'])
        self.assertEqual(second['value']['rows'], expected['rows'])

    def test_object_order_whitespace_raw_identity_and_source_array_significance(self):
        originals = [fixture(n) for n in ('suite', 'baseline', 'candidate')]
        first, second = [], []
        for owner, doc in zip(('suite', 'baseline', 'candidate'), originals):
            a = c.load(ref.canonical(doc), owner)
            b = c.load(json.dumps(doc, sort_keys=False, indent=3).encode(), owner)
            self.assertNotIn('diagnostic', a); self.assertNotIn('diagnostic', b)
            self.assertNotEqual(a['byte_hash'], b['byte_hash'])
            self.assertEqual(a['semantic_hash'], b['semantic_hash'])
            first.append(a['document']); second.append(b['document'])
        self.assertEqual(m.compare(*first, VERSION), m.compare(*second, VERSION))
        prior = m.compare(*first, VERSION)['value']
        second[1]['provenance']['configuration'].reverse()
        changed = self.compare(second)
        self.assertNotEqual(prior['baseline_hash'], changed['baseline_hash'])
        self.assertNotEqual(prior['result_hash'], changed['result_hash'])
        self.assertEqual(prior['rows'], changed['rows'])

    def test_valid_reordered_inputs_have_sorted_rows_outcomes_and_extras(self):
        suite = small_suite({'Z': ['z2', 'z1'], 'A': ['a2', 'a1']})
        own = small_suite({'extra-Z': ['x'], 'Z': ['z2', 'z1'], 'extra-A': ['x'], 'A': ['a2', 'a1']})
        bundle = small_bundle(own)
        actual = self.compare((suite, bundle, copy.deepcopy(bundle)))
        self.assertEqual([r['case_id'] for r in actual['rows']], ['A', 'Z'])
        self.assertEqual(actual['extra_baseline'], ['extra-A', 'extra-Z'])
        for r, ids in zip(actual['rows'], (['a1', 'a2'], ['z1', 'z2'])):
            for owner in ('baseline', 'candidate'):
                self.assertEqual([o['assertion_id'] for o in r[owner]['outcomes']], ids)
        suite['cases'].reverse()
        bundle['runs'].reverse()
        bundle['suite_snapshot']['cases'].reverse()
        for case in bundle['suite_snapshot']['cases']:
            case['assertions'].reverse()
        # Authority must use the same reordered definitions for matching cases.
        for case in suite['cases']:
            case['assertions'].reverse()
        changed = self.compare((suite, bundle, copy.deepcopy(bundle)))
        self.assertEqual(changed['rows'], actual['rows'])
        self.assertNotEqual(changed['result_hash'], actual['result_hash'])

    def test_namespace_binding_and_bidirectional_mutation_isolation(self):
        s, b, d = tiny(right={'A': ['fail']})
        # Same ID occurs in both bundles and both snapshots, with distinct hashes.
        for bundle, word in ((b, 'baseline-only'), (d, 'candidate-only')):
            bundle['artifacts'][0]['content']['unselected'] = word
            shadow = copy.deepcopy(bundle['artifacts'][0])
            shadow['content'] = {'pass': 'wrong-snapshot'}
            shadow['source']['source_id'] = 'snapshot-only'
            bundle['suite_snapshot']['artifacts'].append(shadow)
        inputs = self.validated((s, b, d))
        before = copy.deepcopy(inputs)
        actual = m.compare(*inputs, VERSION)['value']
        for owner, bundle, status in [('baseline', b, 'pass'), ('candidate', d, 'fail')]:
            self.assertEqual(actual['rows'][0][owner]['outcomes'][0]['citations'], [citation(bundle, owner, 'observed', '/' + status)])
        saved = copy.deepcopy(actual)
        actual['rows'][0]['baseline']['outcomes'][0]['citations'][0]['ref']['pointer'] = '/unselected'
        actual['case_counts']['baseline']['pass'] = 99
        actual['extra_baseline'].append('invented')
        self.assertEqual(inputs, before)
        new = m.compare(*inputs, VERSION)['value']
        self.assertEqual(new, saved)
        inputs[1]['artifacts'][0]['content']['pass'] = 'changed-after-return'
        inputs[0]['cases'][0]['assertions'][0]['expected'] = 'changed-after-return'
        self.assertEqual(new, saved)

    def test_internal_faults_nested_diagnostics_and_invalid_version_are_fatal(self):
        inputs = self.validated(tiny())
        for version in (None, True, 1, [], {}, b'v1', '\ud800'):
            self.assertEqual(m.compare(*inputs, version), INTERNAL)
        for target, name in ((m.evaluator, 'evaluate_run'), (m.contract, 'semantic_hash')):
            with patch.object(target, name, side_effect=RuntimeError('CANARY_/private/path')):
                self.assertEqual(m.compare(*inputs, 'CANARY_VERSION'), INTERNAL)
        with patch.object(m.evaluator, 'evaluate_run', return_value={'diagnostic': {'code': 'E_INTERNAL', 'location': None,
                                                                                 'message': 'CANARY'}}):
            self.assertEqual(m.compare(*inputs, VERSION), INTERNAL)
        original = m.evaluator.evaluate_run
        def late_failure(bundle, run_id, owner):
            if owner == 'candidate':
                raise RuntimeError('CANARY')
            return original(bundle, run_id, owner)
        with patch.object(m.evaluator, 'evaluate_run', side_effect=late_failure):
            self.assertEqual(m.compare(*inputs, VERSION), INTERNAL)

    def test_invalid_caller_sets_never_partial_or_vacuous_success(self):
        for mode in ('empty-cases', 'duplicate-case', 'empty-assertions', 'duplicate-assertion', 'malformed-assertion',
                     'duplicate-run', 'duplicate-case-run', 'bad-own-binding', 'empty-snapshot'):
            inputs = self.validated(tiny())
            suite, baseline, _ = inputs
            if mode == 'empty-cases':
                suite['cases'] = []
            elif mode == 'duplicate-case':
                suite['cases'] *= 2
            elif mode == 'empty-assertions':
                suite['cases'][0]['assertions'] = []
            elif mode == 'duplicate-assertion':
                suite['cases'][0]['assertions'] *= 2
            elif mode == 'malformed-assertion':
                suite['cases'][0]['assertions'][0].pop('kind')
            elif mode in ('duplicate-run', 'duplicate-case-run'):
                duplicate = copy.deepcopy(baseline['runs'][0])
                if mode == 'duplicate-case-run':
                    duplicate['run_id'] = 'other'
                baseline['runs'].append(duplicate)
            elif mode == 'bad-own-binding':
                baseline['runs'][0]['case_hash'] = 'sha256:' + '0' * 64
            else:
                baseline['suite_snapshot']['cases'] = []
            self.assertEqual(m.compare(*inputs, VERSION), INTERNAL, mode)

    def test_malformed_nested_outcomes_and_hash_results_are_internal_failures(self):
        inputs = self.validated(tiny())
        good = ordinary(inputs[1], 'baseline', 'A', ['a1'], ['pass'], 'pass')
        for mode in ('missing-reason', 'missing-citations', 'non-list-citations', 'empty-outcomes', 'extra-outcome'):
            malformed = copy.deepcopy(good)
            if mode == 'missing-reason':
                malformed['outcomes'][0].pop('reason')
            elif mode == 'missing-citations':
                malformed['outcomes'][0].pop('citations')
            elif mode == 'non-list-citations':
                malformed['outcomes'][0]['citations'] = None
            elif mode == 'empty-outcomes':
                malformed['outcomes'] = []
            else:
                malformed['outcomes'].append(outcome('extra', 'unknown', 'MISSING_EVIDENCE'))
            with patch.object(m.evaluator, 'evaluate_run', return_value=malformed):
                self.assertEqual(m.compare(*inputs, VERSION), INTERNAL)
        with patch.object(m.contract, 'semantic_hash', return_value=None):
            self.assertEqual(m.compare(*inputs, VERSION), INTERNAL)


if __name__ == '__main__':
    unittest.main(verbosity=2)

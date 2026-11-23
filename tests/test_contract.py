"""B2 Contract tests; fixtures/reference identities are independent of Contract.

Run -I -B on the retained interpreter (via experiments/b2/check.py locally).
Boundary inputs are built and consumed serially, never written to disk.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
from releaselens import contract as c
import fixture_source as ref

MIB = 1048576
FIXTURES = ROOT / 'fixtures/b2'


def small(content=None, media='application/json'):
    a = ref.artifact('input', content, ref.source('test-source', 'knowledge', 'synthetic'), media=media)
    return ref.seal_suite({'schema_version': '1', 'suite_id': 'test', 'revision': 'v1',
        'cases': [{'case_id': 'case', 'title': '', 'input': ref.ref('input', '' if media == 'application/json' else None),
                   'policy_refs': [], 'assertions': [{'assertion_id': 'a', 'kind': 'value',
                     'operator': 'equals', 'expected': None, 'effect': None}]}], 'artifacts': [a]})


def encoded(value):
    raw = ref.canonical(value)
    assert len(raw) <= 25 * MIB + 1
    return raw


def top_hash(value, owner):
    field = 'suite_hash' if owner == 'suite' else 'bundle_hash'
    value[field] = ref.H({k: v for k, v in value.items() if k != field})
    return value


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = {name: json.loads((FIXTURES / (name + '.json')).read_bytes())
                        for name in ('suite', 'baseline', 'candidate')}

    def document(self, owner='candidate'):
        return copy.deepcopy(self.fixtures[owner])

    def accepted(self, document, owner='suite', raw=None):
        raw = encoded(document) if raw is None else raw
        self.assertLessEqual(len(raw), 25 * MIB + 1)
        result = c.load(raw, owner)
        self.assertNotIn('diagnostic', result)
        self.assertEqual(result['byte_hash'], ref.digest(raw))
        return result

    def rejected(self, document=None, owner='suite', code='E_SCHEMA', pointer=None, raw=None):
        raw = encoded(document) if raw is None else raw
        self.assertLessEqual(len(raw), 25 * MIB + 1)
        result = c.load(raw, owner)
        self.assertEqual(set(result), {'diagnostic'})
        diagnostic = result['diagnostic']
        self.assertEqual(diagnostic['code'], code)
        self.assertEqual(diagnostic['message'], c.MESSAGES[code])
        self.assertEqual(diagnostic['location']['kind'], 'input')
        self.assertEqual(diagnostic['location']['input'], owner)
        if pointer is not None:
            self.assertEqual(diagnostic['location']['pointer'], pointer)
        self.assertLess(len(json.dumps(result)), 512)
        return diagnostic

    def test_source_derived_fixture_bytes_and_fixed_identities(self):
        identities = json.loads((FIXTURES / 'identities.json').read_text())
        self.assertEqual(identities['source_sha256'], ref.SOURCE_SHA)
        for name, raw in ref.encoded_documents().items():
            with self.subTest(name=name):
                self.assertEqual(raw, (FIXTURES / (name + '.json')).read_bytes())
                result = self.accepted(None, name, raw=raw)
                fixed = identities['documents'][name]
                self.assertEqual(result['byte_hash'], fixed['byte_hash'])
                self.assertEqual(result['semantic_hash'], fixed['semantic_hash'])
                suite = result['document'] if name == 'suite' else result['document']['suite_snapshot']
                self.assertEqual({x['case_id']: x['case_hash'] for x in suite['cases']}, fixed['case_hashes'])
                self.assertEqual(len(suite['cases']), 8)
                self.assertEqual(len(suite['artifacts']), 17)
                self.assertTrue(all(len(x['assertions']) == 1 for x in suite['cases']))
        suite, baseline, candidate = (self.document(n) for n in ('suite', 'baseline', 'candidate'))
        self.assertEqual(suite, baseline['suite_snapshot'])
        self.assertEqual(suite['cases'][:7], candidate['suite_snapshot']['cases'][:7])
        self.assertNotEqual(suite['cases'][7]['case_hash'], candidate['suite_snapshot']['cases'][7]['case_hash'])
        self.assertEqual([r['case_id'] for r in candidate['runs']], ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C08'])
        self.assertEqual((len(baseline['artifacts']), len(candidate['artifacts'])), (20, 18))
        self.assertFalse(any(a['artifact_id'].endswith('C07') for a in candidate['artifacts']))
        note = next(a for a in suite['artifacts'] if a['artifact_id'] == 'kb-injection')
        self.assertEqual(note['content'], ref.HOSTILE)
        self.assertIn('\n\x1b[2J', note['content'])
        self.assertEqual(candidate['runs'][-1]['case_hash'], candidate['suite_snapshot']['cases'][-1]['case_hash'])

    def test_raw_and_semantic_hashes_and_array_order(self):
        suite = self.document('suite')
        compact = encoded(suite)
        reordered = json.dumps(suite, sort_keys=False, indent=3).encode()
        a, b = self.accepted(suite, raw=compact), self.accepted(suite, raw=reordered)
        self.assertEqual(a['semantic_hash'], b['semantic_hash'])
        self.assertNotEqual(a['byte_hash'], b['byte_hash'])
        suite['artifacts'].reverse()
        ref.seal_suite(suite)
        self.assertNotEqual(self.accepted(suite)['semantic_hash'], a['semantic_hash'])
        doc = small('é', 'text/plain')
        first = self.accepted(doc)['semantic_hash']
        doc['artifacts'][0]['content'] = 'e\u0301'
        ref.seal_suite(doc)
        self.assertNotEqual(self.accepted(doc)['semantic_hash'], first)

    def test_json_unicode_duplicates_bom_and_grammar(self):
        invalid = [b'', b'{}{}', b'NaN', b'Infinity', b'-Infinity', b'01', b'1.', b'1e',
                   b'{"a":1,}', b'[1,]', b'{"a":1,"\\u0061":2}', b'"\\ud800"',
                   b'{"\\udfff":0}', b'"\xff"', b'"\x00"', b'"\\x20"', b'\xef\xbb\xbf{}']
        for raw in invalid:
            with self.subTest(raw=raw):
                self.rejected(raw=raw, code='E_JSON', pointer='')
        doc = small('😀', 'text/plain')
        self.accepted(doc, raw=json.dumps(doc, ensure_ascii=True).encode())
        raw = encoded(doc).replace(b'"suite_id":', b'"suite_id":"test","suite_id":')
        self.rejected(raw=raw, code='E_JSON', pointer='')

    def test_numeric_normalization_and_independent_canonical_vectors(self):
        for token, expected in [('1', 1), ('1.0', 1), ('1e0', 1), ('1.0000000000000001', 1),
                                ('-0', 0), ('-0.0', 0), ('0e999', 0),
                                ('9007199254740991', 9007199254740991),
                                ('-9007199254740991', -9007199254740991)]:
            with self.subTest(token=token):
                suite = small({'nested': [expected]})
                raw = encoded(suite).replace(b'"nested":[' + str(expected).encode() + b']',
                                            b'"nested":[' + token.encode() + b']', 1)
                result = self.accepted(suite, raw=raw)
                value = result['document']['artifacts'][0]['content']['nested'][0]
                self.assertIs(type(value), int)
                self.assertEqual(value, expected)
                self.assertEqual(result['semantic_hash'], suite['suite_hash'])
        for token, canonical in [(b'5e-324', b'5e-324'), (b'1.5', b'1.5'),
                                  (b'0.000001', b'0.000001'), (b'1e-7', b'1e-7')]:
            value, _ = c._decode(token, 'suite')
            self.assertIs(type(value), float)
            self.assertEqual(c.semantic_hash(value), ref.digest(canonical))
            again, _ = c._decode(canonical, 'suite')
            self.assertEqual(value, again)
        for token in (b'9007199254740992', b'9007199254740993e0', b'1e30',
                      b'9007199254740991.5', b'1e-400', b'-1e-400', b'1e309'):
            raw = encoded(small(None)).replace(b'"content":null', b'"content":' + token)
            self.rejected(raw=raw, code='E_JSON', pointer='')
        self.assertNotEqual(self.accepted(small(True))['semantic_hash'], self.accepted(small(1))['semantic_hash'])

    def test_numbers_across_schema_fields_and_boolean_integer_separation(self):
        bundle = self.document()
        raw = encoded(bundle).replace(b'"seq":0', b'"seq":-0.0').replace(b'"seq":1', b'"seq":1e0')
        raw = raw.replace(b'"max_age_ms":60000', b'"max_age_ms":60000.0')
        self.assertEqual(self.accepted(bundle, 'candidate', raw=raw)['document'], bundle)
        for field in ('seq', 'max_age_ms'):
            raw = encoded(bundle).replace((f'"{field}":' + ('0' if field == 'seq' else '60000')).encode(),
                                          f'"{field}":true'.encode(), 1)
            self.rejected(owner='candidate', raw=raw)
        for token in (b'1.5', b'[]', b'{}'):
            raw = encoded(small()).replace(b'"expected":null', b'"expected":' + token)
            self.rejected(raw=raw, pointer='/cases/0/assertions/0/expected')
        suite = small()
        suite['cases'][0]['assertions'][0]['expected'] = 1
        ref.seal_suite(suite)
        raw = encoded(suite).replace(b'"expected":1', b'"expected":1.0')
        self.accepted(suite, raw=raw)
        # Subject normalization is structural; it does not assert effect eligibility.
        bundle['runs'][0]['events'][0]['subject'] = 1
        ref.seal_bundle(bundle)
        raw = encoded(bundle).replace(b'"subject":1', b'"subject":1e0')
        self.accepted(bundle, 'candidate', raw=raw)

    def test_required_unknown_fields_types_ids_and_hash_grammar(self):
        for mutate, pointer in [
            (lambda s: s.pop('revision'), ''),
            (lambda s: s.update({'SYNTHETIC_SECRET_/private/path': True}), ''),
            (lambda s: s.update(schema_version=1), '/schema_version'),
            (lambda s: s.update(schema_version='2'), '/schema_version'),
            (lambda s: s.update(suite_id=''), '/suite_id'),
            (lambda s: s.update(suite_id='é'), '/suite_id'),
            (lambda s: s.update(suite_id='x' * 129), '/suite_id'),
            (lambda s: s.update(cases={}), '/cases'),
            (lambda s: s['cases'][0].update(title=None), '/cases/0/title'),
            (lambda s: s['artifacts'][0].update(redacted=1), '/artifacts/0/redacted'),
            (lambda s: s['artifacts'][0].update(sha256='sha256:' + 'A' * 64), '/artifacts/0/sha256'),
            (lambda s: s['artifacts'][0].update(media_type='text/html'), '/artifacts/0/media_type'),
        ]:
            with self.subTest(pointer=pointer):
                suite = small()
                mutate(suite)
                diagnostic = self.rejected(top_hash(suite, 'suite'), pointer=pointer)
                self.assertNotIn('SYNTHETIC_SECRET', json.dumps(diagnostic))
                self.assertNotIn('/private/path', json.dumps(diagnostic))
        suite = small()
        suite['suite_id'] = 'A' + 'x' * 127
        ref.seal_suite(suite)
        self.accepted(suite)

    def test_identity_failure_layers_not_stale_unrelated_hashes(self):
        suite = small('original', 'text/plain')
        for field, pointer in [('artifact', '/artifacts/0/sha256'), ('case', '/cases/0/case_hash'), ('suite', '/suite_hash')]:
            value = copy.deepcopy(suite)
            if field == 'artifact':
                value['artifacts'][0]['content'] = 'changed'
            elif field == 'case':
                value['cases'][0]['title'] = 'changed'
            else:
                value['revision'] = 'changed'
            if field != 'suite':
                top_hash(value, 'suite')
            self.rejected(value, code='E_IDENTITY', pointer=pointer)
        changed = copy.deepcopy(suite)
        changed['artifacts'][0]['source']['version'] = 'v2'
        top_hash(changed, 'suite')
        self.rejected(changed, code='E_IDENTITY', pointer='/cases/0/case_hash')
        ref.seal_suite(changed)
        self.assertNotEqual(self.accepted(changed)['semantic_hash'], suite['suite_hash'])
        bundle = self.document()
        bundle['runs'][0]['case_hash'] = 'sha256:' + '0' * 64
        top_hash(bundle, 'candidate')
        self.rejected(bundle, 'candidate', 'E_IDENTITY', '/runs/0/case_hash')
        bundle = self.document()
        bundle['bundle_id'] = 'changed'
        self.rejected(bundle, 'candidate', 'E_IDENTITY', '/bundle_hash')

    def test_uniqueness_nonempty_and_reference_namespaces(self):
        for key in ('cases', 'artifacts'):
            suite = small()
            suite[key].append(copy.deepcopy(suite[key][0]))
            self.rejected(top_hash(suite, 'suite'))
        suite = small()
        suite['cases'][0]['assertions'] *= 2
        self.rejected(top_hash(suite, 'suite'))
        for mutate in (lambda s: s.update(cases=[]), lambda s: s['cases'][0].update(assertions=[])):
            suite = small()
            mutate(suite)
            self.rejected(top_hash(suite, 'suite'))
        bundle = self.document()
        bundle['runs'].append(copy.deepcopy(bundle['runs'][0]))
        self.rejected(top_hash(bundle, 'candidate'), 'candidate')
        bundle['runs'][-1]['run_id'] = 'another'
        self.rejected(top_hash(bundle, 'candidate'), 'candidate', pointer='/runs/7/case_id')
        bundle = self.document()
        bundle['runs'][0]['events'][2]['entity'] = ref.ref('policy-C01')
        self.rejected(top_hash(bundle, 'candidate'), 'candidate', 'E_REFERENCE', '/runs/0/events/2/entity')
        suite = self.document('suite')
        suite['cases'][0]['input'] = ref.ref('record-C01', '')
        self.rejected(top_hash(suite, 'suite'), code='E_REFERENCE', pointer='/cases/0/input')
        bundle = self.document()
        bundle['runs'] = []
        self.accepted(ref.seal_bundle(bundle), 'candidate')

    def test_source_tuples_and_provenance(self):
        bundle = self.document()
        src = next(a['source'] for a in bundle['artifacts'] if a['source']['source_id'] == 'refund-adapter')
        src['version'] = 'SYNTHETIC_SECRET'
        self.rejected(top_hash(bundle, 'candidate'), 'candidate', 'E_SOURCE')
        for mutate in (
            lambda b: b['provenance']['producer'].update(kind='model'),
            lambda b: b['provenance']['configuration'].pop(0),
            lambda b: b['provenance']['configuration'].append(copy.deepcopy(b['provenance']['configuration'][0])),
            lambda b: b['provenance']['configuration'][0].update(kind='policy'),
        ):
            bundle = self.document()
            mutate(bundle)
            self.rejected(top_hash(bundle, 'candidate'), 'candidate')
        bundle = self.document()
        bundle['provenance']['producer'].update(version=None, digest=None)
        bundle['provenance']['exported_at'] = None
        self.accepted(ref.seal_bundle(bundle), 'candidate')
        suite = small()
        suite['cases'][0]['policy_refs'] = [ref.ref('input', '')]
        self.accepted(ref.seal_suite(suite))
        suite['artifacts'][0]['source']['kind'] = 'tool'
        self.rejected(ref.seal_suite(suite), pointer='/cases/0/policy_refs/0')

    def test_pointer_escaping_arrays_null_and_selected_entity_relative_selectors(self):
        bundle = self.document()
        record = next(a for a in bundle['artifacts'] if a['artifact_id'] == 'record-C01')
        record['content'] = {'a/b': {'~key': [{'id': 'order-01', 'state': 'refunded'}]}}
        event = bundle['runs'][0]['events'][2]
        event.update(entity=ref.ref('record-C01', '/a~1b/~0key/0'), subject_pointer='/id', value_pointer='/state')
        self.accepted(ref.seal_bundle(bundle), 'candidate')
        for pointer in ('/a~2b', '/a~', 'not-a-pointer', '/a~1b/~0key/00', '/a~1b/~0key/-',
                        '/a~1b/~0key/1', '/a~1b/~0key/' + '9' * 100):
            bad = copy.deepcopy(bundle)
            bad['runs'][0]['events'][2]['entity']['pointer'] = pointer
            self.rejected(top_hash(bad, 'candidate'), 'candidate', 'E_REFERENCE')
        event['subject_pointer'] = '/a~1b/~0key/0/id'  # Exists at artifact root, not selected entity.
        self.rejected(top_hash(bundle, 'candidate'), 'candidate', 'E_REFERENCE', '/runs/0/events/2/subject_pointer')
        for media, pointer in [('text/plain', ''), ('application/json', None)]:
            suite = small('text', media)
            suite['cases'][0]['input']['pointer'] = pointer
            self.rejected(top_hash(suite, 'suite'), code='E_REFERENCE', pointer='/cases/0/input/pointer')

    def test_semantic_ineligibility_is_not_structural_rejection(self):
        for mode in ('text', 'nonobject', 'null', 'missing-selectors', 'nested-selectors', 'root-selectors',
                     'wrong-observed-subject', 'wrong-event-subject', 'wrong-tool', 'tool-source', 'stale', 'completion-error'):
            with self.subTest(mode=mode):
                bundle = self.document()
                record = next(a for a in bundle['artifacts'] if a['artifact_id'] == 'record-C01')
                run = bundle['runs'][0]
                effect = run['events'][2]
                if mode == 'text':
                    record.update(media_type='text/plain', content='refund completed',
                                  source=copy.deepcopy(bundle['provenance']['configuration'][1]))
                    effect.update(entity=ref.ref('record-C01'), subject_pointer=None, value_pointer=None)
                elif mode in ('nonobject', 'null'):
                    record['content'] = ['order-01', 'refunded'] if mode == 'nonobject' else None
                    effect.update(subject_pointer='/0' if mode == 'nonobject' else '', value_pointer='/1' if mode == 'nonobject' else '')
                elif mode == 'missing-selectors':
                    effect.update(subject_pointer=None, value_pointer=None)
                elif mode == 'nested-selectors':
                    record['content'] = {'orders': [{'id': 'order-01'}, {'state': 'refunded'}]}
                    effect.update(subject_pointer='/orders/0/id', value_pointer='/orders/1/state')
                elif mode == 'root-selectors':
                    effect.update(subject_pointer='', value_pointer='')
                elif mode == 'wrong-observed-subject':
                    record['content']['order_id'] = 'order-99'
                elif mode == 'wrong-event-subject':
                    effect['subject'] = True
                elif mode == 'wrong-tool':
                    run['events'][0]['tool'] = 'another-tool'
                elif mode == 'tool-source':
                    record['source'] = copy.deepcopy(bundle['provenance']['configuration'][2])
                elif mode == 'stale':
                    record['captured_at'] = '2026-01-01T13:00:00.000Z'
                else:
                    run['events'][1]['status'] = 'error'
                self.accepted(ref.seal_bundle(bundle), 'candidate')

    def test_event_links_order_cardinality_and_observations(self):
        for mutate, code in (
            (lambda r: r['events'][1].update(request_id='absent'), 'E_REFERENCE'),
            (lambda r: r['events'][2].update(completion_id='req'), 'E_REFERENCE'),
            (lambda r: r['events'][1].update(seq=3), 'E_REFERENCE'),
            (lambda r: r['events'][1].update(seq=0), 'E_SCHEMA'),
            (lambda r: r['events'][1].update(event_id='req'), 'E_SCHEMA'),
            (lambda r: r['observations'][0].update(effect_event_id='done'), 'E_REFERENCE'),
            (lambda r: r['observations'][0].update(assertion_id='absent'), 'E_REFERENCE'),
            (lambda r: r['observations'][0].update(value=ref.ref('result-C01')), 'E_SCHEMA'),
            (lambda r: r['observations'].append(copy.deepcopy(r['observations'][0])), 'E_SCHEMA'),
        ):
            bundle = self.document()
            mutate(bundle['runs'][0])
            self.rejected(top_hash(bundle, 'candidate'), 'candidate', code)
        for kind, parent in [('completion', 1), ('effect', 2)]:
            bundle = self.document()
            event = copy.deepcopy(bundle['runs'][0]['events'][parent])
            event.update(event_id='second', seq=4)
            bundle['runs'][0]['events'].append(event)
            self.rejected(top_hash(bundle, 'candidate'), 'candidate', 'E_REFERENCE')
        bundle = self.document()
        bundle['runs'][0]['events'].reverse()  # seq, not array order, defines linked order.
        self.accepted(ref.seal_bundle(bundle), 'candidate')
        bundle['runs'][0]['observations'][0]['effect_event_id'] = None
        bundle['runs'][0]['events'] = []
        self.accepted(ref.seal_bundle(bundle), 'candidate')

    def test_run_statuses_and_time_claims(self):
        for status in ('error', 'timeout', 'skipped'):
            bundle = self.document()
            run = bundle['runs'][0]
            run['status'] = status
            run['error_code'] = None if status == 'skipped' else 'SYNTHETIC_ERROR'
            if status == 'skipped':
                run.update(events=[], observations=[])
            self.accepted(ref.seal_bundle(bundle), 'candidate')
        for mutate in (
            lambda r: r.update(status='skipped'), lambda r: r.update(status='error'),
            lambda r: r.update(error_code='unexpected'),
        ):
            bundle = self.document()
            mutate(bundle['runs'][0])
            self.rejected(top_hash(bundle, 'candidate'), 'candidate')
        for stamp in ('2026-01-01T12:00:60.000Z', '2026-02-30T12:00:00.000Z',
                      '2026-01-01T12:00:00Z', '2026-01-01T12:00:00.000+00:00',
                      '0000-01-01T12:00:00.000Z', True):
            bundle = self.document()
            bundle['runs'][0]['started_at'] = stamp
            self.rejected(top_hash(bundle, 'candidate'), 'candidate', 'E_TIME')
        for mutate in (
            lambda r: r.update(ended_at='2026-01-01T11:00:00.000Z'),
            lambda r: r['events'][0].update(occurred_at='2026-01-01T11:59:59.999Z'),
            lambda r: r['events'][1].update(occurred_at='2026-01-01T12:00:00.500Z'),
            lambda r: (r['events'][1].update(occurred_at=None),
                       r['events'][2].update(occurred_at='2026-01-01T12:00:00.500Z')),
        ):
            bundle = self.document()
            mutate(bundle['runs'][0])
            self.rejected(top_hash(bundle, 'candidate'), 'candidate', 'E_TIME')
        bundle = self.document()
        run = bundle['runs'][0]
        run.update(started_at=None, ended_at=None)
        for e in run['events']:
            e['occurred_at'] = None
        self.accepted(ref.seal_bundle(bundle), 'candidate')

    def test_depth_exact_32_and_33_including_embedded_snapshot(self):
        for embedded in (False, True):
            for depth in (32, 33):
                content = 0
                # root/artifacts/Artifact + optional bundle/suite_snapshot.
                for _ in range(depth - (4 if embedded else 3)):
                    content = [content]
                suite = small(content)
                if embedded:
                    doc = self.document()
                    doc.update(suite_snapshot=suite, runs=[])
                    ref.seal_bundle(doc)
                else:
                    doc = suite
                owner = 'candidate' if embedded else 'suite'
                if depth == 32:
                    self.accepted(doc, owner)
                else:
                    self.rejected(doc, owner, 'E_LIMIT')
        self.accepted(small('[' * 50 + '}' * 50, 'text/plain'))

    def test_raw_input_exact_and_one_over(self):
        for owner, limit in (('suite', 5 * MIB), ('candidate', 25 * MIB)):
            doc = small() if owner == 'suite' else self.document()
            compact = encoded(doc)
            for delta in (0, 1):
                raw = compact + b' ' * (limit + delta - len(compact))
                if delta:
                    self.rejected(owner=owner, raw=raw, code='E_LIMIT')
                else:
                    self.accepted(doc, owner, raw=raw)
                del raw

    def test_actual_content_token_spans_quotes_escapes_and_whitespace(self):
        for mode in ('ascii', 'escaped', 'multibyte', 'object-whitespace'):
            for delta in (0, 1):
                size = MIB + delta
                if mode == 'object-whitespace':
                    token, content, media = b'{' + b' ' * (size - 2) + b'}', {}, 'application/json'
                else:
                    unit = {'ascii': b'x', 'escaped': b'\\u00e9', 'multibyte': 'é'.encode()}[mode]
                    n, remainder = divmod(size - 2, len(unit))
                    token = b'"' + unit * n + b'x' * remainder + b'"'
                    content, media = json.loads(token), 'text/plain'
                suite = small(content, media)
                raw = encoded(suite)
                original = b'"content":' + ref.canonical(content)
                # Escaped property spelling and external whitespace are not part of the value token.
                raw = raw.replace(original, b'"cont\\u0065nt" : \t' + token + b'\n', 1)
                if delta:
                    self.rejected(raw=raw, code='E_LIMIT')
                else:
                    self.accepted(suite, raw=raw)
                del raw, token, suite
        suite = small({'content': '" } ] content :', 'escaped': '\\"'})
        self.accepted(suite)

    def test_case_assertion_artifact_event_ceilings(self):
        for kind, limit in (('cases', 1000), ('assertions', 20), ('artifacts', 2000), ('events', 200)):
            for embedded in (False, True) if kind != 'events' else (True,):
                for delta in (0, 1):
                    suite = small()
                    if kind == 'cases':
                        suite['cases'] = [dict(copy.deepcopy(suite['cases'][0]), case_id=f'c{i}') for i in range(limit + delta)]
                    elif kind == 'assertions':
                        suite['cases'][0]['assertions'] = [dict(copy.deepcopy(suite['cases'][0]['assertions'][0]),
                            assertion_id=f'a{i}') for i in range(limit + delta)]
                    elif kind == 'artifacts':
                        suite['artifacts'] += [dict(copy.deepcopy(suite['artifacts'][0]), artifact_id=f'x{i}')
                                               for i in range(limit + delta - 1)]
                    ref.seal_suite(suite)
                    owner, doc = 'suite', suite
                    if embedded:
                        owner, doc = 'candidate', self.document()
                        doc.update(suite_snapshot=suite, runs=[])
                        if kind == 'events':
                            events = [{'event_id': f'e{i}', 'kind': 'request', 'seq': i, 'occurred_at': None,
                                       'tool': 't', 'subject': None, 'arguments': ref.ref('args-C01', '')}
                                      for i in range(limit + delta)]
                            doc['runs'] = [{'run_id': 'r', 'case_id': 'case', 'case_hash': suite['cases'][0]['case_hash'],
                                'started_at': None, 'ended_at': None, 'status': 'complete', 'error_code': None,
                                'observations': [], 'events': events}]
                        ref.seal_bundle(doc)
                    if delta:
                        self.rejected(doc, owner, 'E_LIMIT')
                    else:
                        self.accepted(doc, owner)

    def test_decoded_aggregate_text_exact_and_one_over(self):
        # 20 almost-1MiB text tokens plus one small remainder; <=25MiB input.
        for delta in (0, 1):
            bundle = self.document()
            src = ref.source('aggregate', 'knowledge', 'synthetic aggregate')
            bundle['artifacts'] = [ref.artifact(f'a{i}', 'x' * (MIB - 2), src) for i in range(20)]
            bundle['artifacts'].append(ref.artifact('tail', 'x' * (40 + delta), src))
            bundle['runs'] = []
            ref.seal_bundle(bundle)
            if delta:
                self.rejected(bundle, 'candidate', 'E_LIMIT', '/artifacts')
            else:
                self.accepted(bundle, 'candidate')
            del bundle

    def test_embedded_decoded_aggregate_and_independent_arrays(self):
        # JSON JCS expands 1e15 to16 digits: raw content stays below1MiB while
        # decoded totals hit20MiB in an embedded array (whole bundle <=25MiB).
        src = ref.source('aggregate', 'knowledge', 'synthetic aggregate')
        for delta in (0, 1):
            suite = small()
            content = [1000000000000000] * 60000  # JCS length 1,020,001.
            self.assertEqual(len(ref.canonical(content)), 1020001)
            suite['artifacts'] = [ref.artifact('input' if i == 0 else f'a{i}', content, src) for i in range(20)]
            suite['artifacts'].append(ref.artifact('tail', 'x' * (20 * MIB - 20 * 1020001 + delta), src))
            ref.seal_suite(suite)
            bundle = self.document()
            bundle.update(suite_snapshot=suite, runs=[])
            ref.seal_bundle(bundle)
            raw = encoded(bundle).replace(b'1000000000000000', b'1e15')
            self.assertLess(len(raw), 25 * MIB)
            if delta:
                self.rejected(owner='candidate', raw=raw, code='E_LIMIT', pointer='/suite_snapshot/artifacts')
            else:
                self.accepted(bundle, 'candidate', raw=raw)
            del bundle, suite, raw, content
        bundle = self.document()
        content = [1000000000000000] * 60000
        rows = [ref.artifact('input' if i == 0 else f'a{i}', content, src) for i in range(11)]
        suite = small()
        suite['artifacts'] = rows
        ref.seal_suite(suite)
        bundle.update(suite_snapshot=suite, artifacts=copy.deepcopy(rows), runs=[])
        ref.seal_bundle(bundle)
        raw = encoded(bundle).replace(b'1000000000000000', b'1e15')
        self.assertGreater(22 * 1020001, 20 * MIB)
        self.accepted(bundle, 'candidate', raw=raw)

    def test_diagnostics_never_echo_evidence_or_exception_text(self):
        secret = 'SYNTHETIC_SECRET_/private/customer'
        raw = b'{' + json.dumps(secret).encode() + b':"\\ud800"}'
        result = c.load(raw, 'baseline')
        self.assertNotIn(secret, json.dumps(result))
        self.assertEqual(result['diagnostic']['location']['pointer'], '')
        for error, code in ((ValueError(secret), 'E_JSON'), (RuntimeError(secret), 'E_INTERNAL')):
            with patch.object(c.rfc8785, 'dumps', side_effect=error):
                self.rejected(small(), code=code, pointer='')
        self.assertEqual(c.load(b'{}', secret)['diagnostic']['location'], None)


if __name__ == '__main__':
    unittest.main(verbosity=2)

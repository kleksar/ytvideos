import copy
import unittest
from ytvideos.motion_audit import audit_motion_batch
from ytvideos.util import digest


class MotionAuditTests(unittest.TestCase):
    def fixture(self):
        sha = 'a' * 64
        source = 'b' * 64
        settings = {'seconds': 7, 'resolution': 'custom'}
        contract = {'batch_sha256': 'c' * 64, 'settings_sha256': digest(settings),
                    'provider': 'example-provider', 'model': 'example-model', 'revision': 3, 'script_sha256': sha}
        run = {'id': 'generic-run', 'revision': 3,
               'approvals': {'script': {'revision': 3, 'sha256': sha, 'artifact_id': 'script'}},
               'tasks': {'script': {'status': 'complete', 'outputs': ['script']}},
               'artifacts': {'image': {'sha256': source}, 'receipt': {'sha256': 'd' * 64}},
               'motion_batch': {**contract, 'settings': settings, 'max_credits': 9, 'per_request': 9,
                                'spent': 9, 'reserved': 0,
                                'approval': {**contract, 'max_credits': 9, 'source': 'owner-event', 'message': 'approved'},
                                'scenes': {'arbitrary_scene': {'status': 'generated', 'image_sha256': source,
                                           'image_artifact_id': 'image', 'prompt': 'exact prompt', 'operation_key': 'op'}}}}
        op = {'key': 'op', 'run_id': run['id'], 'status': 'confirmed', 'attempt_id': 'attempt',
              'task_input_hash': 'e' * 64, 'receipt': 'receipt',
              'payload': {**contract, 'scene': 'arbitrary_scene', 'image_sha256': source, 'prompt': 'exact prompt'}}
        observation = {'operation_key': 'op', 'attempt_id': 'attempt', 'task_input_hash': 'e' * 64,
                       'status': 'confirmed', 'actual_units': 9}
        return run, [op], observation

    def codes(self, result):
        return {finding['code'] for finding in result['findings']}

    def test_consistent_declarations_never_authorize_dispatch_and_do_not_mutate(self):
        run, ops, observation = self.fixture(); before = copy.deepcopy((run, ops))
        result = audit_motion_batch(run, ops, resolve_document=lambda _: observation)
        self.assertEqual(result['status'], 'declared_bindings_consistent')
        self.assertFalse(result['dispatch_authorized']); self.assertEqual((run, ops), before)

    def test_stale_revision_detected(self):
        run, ops, _ = self.fixture(); run['revision'] += 1
        codes = self.codes(audit_motion_batch(run, ops))
        self.assertTrue({'script_approval_stale', 'batch_binding_mismatch', 'approval_binding_mismatch'} <= codes)

    def test_unbound_legacy_approval_and_payload_not_inferred_from_text(self):
        run, ops, _ = self.fixture(); run['motion_batch']['approval'] = {'source': 'chat', 'message': 'all approved 9 credits'}
        del ops[0]['payload']; del run['motion_batch']['revision']
        codes = self.codes(audit_motion_batch(run, ops))
        self.assertTrue({'approval_binding_missing', 'operation_payload_unbound', 'batch_binding_missing'} <= codes)

    def test_wrong_receipt_and_estimated_cost_not_confirmation(self):
        run, ops, observation = self.fixture(); observation['attempt_id'] = 'other'; del observation['actual_units']
        codes = self.codes(audit_motion_batch(run, ops, resolve_document=lambda _: observation))
        self.assertTrue({'observation_unbound', 'actual_cost_unverified'} <= codes)

    def test_unknown_is_reported_without_state_repair(self):
        run, ops, _ = self.fixture(); ops[0]['status'] = 'unknown'
        self.assertIn('operation_unresolved', self.codes(audit_motion_batch(run, ops)))
        self.assertEqual(ops[0]['status'], 'unknown')

    def test_invalid_or_exceeded_budget(self):
        run, ops, _ = self.fixture(); run['motion_batch']['reserved'] = 1
        self.assertIn('budget_exceeded', self.codes(audit_motion_batch(run, ops)))
        run['motion_batch']['reserved'] = True
        self.assertIn('budget_invalid', self.codes(audit_motion_batch(run, ops)))

    def test_no_batch_and_invalid_batch(self):
        self.assertEqual(audit_motion_batch({'id': 'run'}, [])['status'], 'not_applicable')
        self.assertIn('invalid_batch', self.codes(audit_motion_batch({'motion_batch': []}, [])))

    def test_wrong_source_and_unreadable_observation(self):
        run, ops, _ = self.fixture(); run['artifacts']['image']['sha256'] = 'z' * 64
        def unreadable(_): raise ValueError('invalid JSON')
        codes = self.codes(audit_motion_batch(run, ops, resolve_document=unreadable))
        self.assertTrue({'source_unbound', 'observation_unverified'} <= codes)


class MotionDoctorTests(unittest.TestCase):
    def test_doctor_reports_legacy_evidence_without_state_changes(self):
        self.check_doctor('invalid_json')

    def test_doctor_reports_corrupt_observation_without_state_changes(self):
        self.check_doctor('corrupt_bytes')

    def test_doctor_reports_malformed_nested_batch_data_without_state_changes(self):
        self.check_doctor('malformed_nested')

    def check_doctor(self, mode):
        import json
        from pathlib import Path
        import tempfile
        from ytvideos.doctor import inspect
        from ytvideos.service import Production
        from ytvideos.store import Store
        from ytvideos.util import canonical
        run, operations, _ = MotionAuditTests().fixture()
        run.update(schema_version=1, version=7, request_id='doctor-test', channel='generic_channel',
                   status='working', profile={'recipe': 'illustrated'}, capabilities={})
        run['tasks']['script']['capabilities'] = ['model.text']
        op = operations[0]
        op.update(kind='external_video', input_hash='f' * 64)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            store = Store(root / 'state.sqlite3')
            production = Production(store, root / 'workspace', root)
            evidence = root / 'receipt.json'
            evidence.write_text('not JSON')
            artifact = production.artifacts.put(evidence, 'operation_observation')
            run['artifacts'][artifact['id']] = artifact
            op['receipt'] = artifact['id']
            if mode == 'corrupt_bytes':
                production.artifacts.resolve(artifact).write_text('changed bytes')
            if mode == 'malformed_nested':
                run['approvals']['script'] = []
            with store.transaction() as tx:
                tx.execute('INSERT INTO runs VALUES (?,?,?,?,?)',
                           (run['id'], run['request_id'], run['channel'], run['version'], canonical(run)))
                tx.create_operation(op)
                tx.event('fixture-event', run['id'], 'fixture.created', {'test': True})
            before = store.get(run['id'])
            events = store.events(run['id'])
            with store.transaction() as tx:
                operation_before = tx.operation(op['key'])
            report = inspect(production, run['id'])
            check = next(x for x in report['checks'] if x['capability'] == 'video.saved_batch_evidence')
            self.assertEqual(check['evidence']['status'], 'evidence_incomplete')
            self.assertFalse(check['evidence']['dispatch_authorized'])
            self.assertIn('Reconcile', check['next_action'])
            self.assertFalse(check['available'])
            self.assertIn('reject existing media', check['next_action'])
            self.assertEqual(store.get(run['id']), before)
            self.assertEqual(store.events(run['id']), events)
            with store.transaction() as tx:
                self.assertEqual(tx.operation(op['key']), operation_before)
            codes = {x['code'] for x in check['evidence']['findings']}
            self.assertIn('saved_batch_structure_invalid' if mode == 'malformed_nested'
                          else 'observation_unverified', codes)

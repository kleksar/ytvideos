"""Offline contracts for a prepared textual handoff; fixtures are not creative QA."""
import hashlib
import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ytvideos.source_script import main
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.profiles import load_profile
from ytvideos.service import Production
from ytvideos.source_script import accept_source
from ytvideos.store import Store
from ytvideos.util import digest, file_digest
from ytvideos.workflow import STAGES, valid_approval

ROOT = Path(__file__).resolve().parents[1]
TEXT = ('I opened the box and saw the same two pieces of wood. '
        'One rested flat on the table; I stood the other upright. '
        'This is synthetic software test text, not a factual video script or a review. '
        'No observation, factual conclusion, human approval or independent editorial acceptance is implied.\n')


def package(profile, format='long'):
    """Only a structural fixture: does not assert artistic quality or real references."""
    return {
        'schema': 'ytv-preproduction-v1', 'channel_id': profile['id'], 'format': format,
        'script_sha256': hashlib.sha256(TEXT.encode()).hexdigest(), 'profile_sha256': digest(profile),
        'assets': [{'id': 'PROP', 'kind': 'prop', 'mode': 'generate',
                    'prompt': 'Synthetic reference sheet: two identical rectangular wooden blocks; no actual media.'}],
        'scenes': [{'id': 'S001', 'narration': {'start': 0, 'end': len(TEXT), 'text': TEXT},
                    'visual_intent': 'Synthetic comparison of flat and upright orientations.',
                    'prompt': 'Synthetic scene: two wooden blocks on a table, one upright and one flat; fixed side camera.',
                    'asset_ids': ['PROP'], 'continuity': 'The two blocks keep the same dimensions.',
                    'camera': 'Side view; both bases remain visible.',
                    'motion': {'method': 'hold', 'brief': 'Hold the whole composition.'},
                    'sound': 'No fabricated dialogue; production will bind real audio.',
                    'checks': ['Both blocks and their contact with the table are visible.']}],
        'audio_plan': 'Use the pinned channel voice; align only after recording.',
        'packaging_brief': 'Synthetic packaging intent, not a completed thumbnail.',
        'edit_plan': 'Direct cuts; final frame intervals follow the actual word map.',
        'open_items': [],
    }


class PreproductionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profile = load_profile(ROOT / 'channels', 'paper_detour')
        self.script = self.root / 'script.en.txt'
        self.script.write_bytes(TEXT.encode())
        self.plan = self.root / 'preproduction.json'
        self.data = package(self.profile)
        self.write_plan()
        self.service = Production(Store(str(self.root / 'state.sqlite3')), self.root / 'workspace', ROOT)

    def write_plan(self):
        self.plan.write_text(json.dumps(self.data), encoding='utf-8')

    def create(self, **changes):
        args = dict(format='long', source_script=self.script)
        args.update(changes)
        return self.service.create('paper_detour', 'Produce this selected prepared source', **args)

    def accept(self, run, **changes):
        values = dict(revision=run['revision'], sha256=file_digest(self.script),
                      source='fixture://actual-owner-message', message='Produce this exact fixture source.',
                      origin='fixture://immutable-commit/selected/script.en.txt', preproduction=self.plan)
        values.update(changes)
        return accept_source(self.service, run['id'], **values)

    def validate(self, **changes):
        from ytvideos.preproduction import validate_package
        return validate_package(self.data, script=TEXT, profile=self.profile, format='long', **changes)

    def test_structural_validation_is_not_a_review_or_media_gate(self):
        result = self.validate()
        self.assertEqual(result['scene_count'], 1)
        self.assertEqual(result['content_review'], 'UNVERIFIED')
        self.assertEqual(result['timing'], 'unmeasured')
        self.assertFalse(result['production_authorized'])

    def test_exact_identity_and_complete_spans_are_required(self):
        for key, value in [('script_sha256', '0' * 64), ('profile_sha256', '0' * 64),
                           ('channel_id', 'nuviko_history'), ('format', 'short')]:
            with self.subTest(key=key):
                self.data = package(self.profile)
                self.data[key] = value
                with self.assertRaises(WorkflowError):
                    self.validate()
        for span in [{'start': 1, 'end': len(TEXT), 'text': TEXT[1:]},
                     {'start': 0, 'end': len(TEXT)-1, 'text': TEXT[:-1]},
                     {'start': 0, 'end': len(TEXT), 'text': 'rewritten text'}]:
            self.data = package(self.profile)
            self.data['scenes'][0]['narration'] = span
            with self.subTest(span=span), self.assertRaises(WorkflowError):
                self.validate()

    def test_missing_planning_and_unknown_assets_are_rejected(self):
        for key in ('audio_plan', 'packaging_brief', 'edit_plan'):
            self.data = package(self.profile)
            self.data[key] = '  '
            with self.subTest(key=key), self.assertRaises(WorkflowError):
                self.validate()
        self.data = package(self.profile)
        self.data['scenes'][0]['asset_ids'] = ['UNKNOWN']
        with self.assertRaisesRegex(WorkflowError, 'asset'):
            self.validate()
        self.data['scenes'][0]['asset_ids'] = []
        with self.assertRaisesRegex(WorkflowError, 'reference_na_reason'):
            self.validate()

    def test_estimated_plan_does_not_accept_fabricated_final_frames(self):
        for key in ('start_frame', 'end_frame', 'start_seconds', 'end_seconds'):
            self.data = package(self.profile)
            self.data['scenes'][0][key] = 100
            with self.subTest(key=key), self.assertRaisesRegex(WorkflowError, 'timing'):
                self.validate()

    def test_flow_respects_real_recipe_and_format(self):
        from ytvideos.preproduction import validate_package
        self.data['scenes'][0]['motion']['method'] = 'flow_ingredients'
        with self.assertRaisesRegex(WorkflowError, 'Flow'):
            self.validate()
        self.data['format'] = 'short'
        result = validate_package(self.data, script=TEXT, profile=self.profile, format='short')
        self.assertEqual(result['flow_scene_count'], 1)
        other = load_profile(ROOT / 'channels', 'nuviko_history')
        self.data = package(other, 'short')
        self.data['scenes'][0]['motion']['method'] = 'flow_ingredients'
        with self.assertRaisesRegex(WorkflowError, 'Flow'):
            validate_package(self.data, script=TEXT, profile=other, format='short')

    def test_package_alone_is_not_approval_and_acceptance_never_dispatches(self):
        run = self.create()
        self.assertFalse(valid_approval(run, 'script'))
        self.assertNotIn('source_preproduction_id', run)
        self.accept(run)
        saved = self.service.store.get(run['id'])
        artifact = saved['artifacts'][saved['source_preproduction_id']]
        self.assertEqual(saved['pins']['source_preproduction'], file_digest(self.plan))
        self.assertEqual(self.service.artifacts.resolve(artifact).read_bytes(), self.plan.read_bytes())
        self.assertEqual(set(saved['tasks']), set(STAGES))
        self.assertEqual(saved['budget']['spent'], 0)
        with self.service.store.transaction() as tx:
            self.assertEqual(tx.execute('SELECT COUNT(*) FROM operations').fetchone()[0], 0)
        self.plan.unlink()
        self.script.unlink()
        context = self.service.context(run['id'], 'storyboard')
        self.assertEqual(context['task_guide']['preproduction']['artifact']['sha256'], artifact['sha256'])
        self.assertEqual(self.service.plan(run['id'])['source_preproduction']['sha256'], artifact['sha256'])

    def test_changed_acceptance_redelivery_cannot_replace_or_remove_package(self):
        run = self.create()
        first = self.accept(run)
        self.assertEqual(first, self.accept(run))
        self.data['audio_plan'] += ' Different planned music.'
        self.write_plan()
        with self.assertRaises(Conflict):
            self.accept(run)
        with self.assertRaises(Conflict):
            self.accept(run, preproduction=None)

    def test_invalid_package_cannot_approve_script_or_change_graph(self):
        run = self.create()
        self.data['script_sha256'] = '0' * 64
        self.write_plan()
        with self.assertRaises(WorkflowError):
            self.accept(run)
        saved = self.service.store.get(run['id'])
        self.assertEqual(saved['tasks'], run['tasks'])
        self.assertEqual(saved['approvals'], {})
        self.assertEqual(saved['pins'], run['pins'])

    def test_original_acceptance_route_keeps_package_and_two_gates(self):
        run = self.create()
        self.accept(run)
        saved = self.service.store.get(run['id'])
        self.assertTrue(valid_approval(saved, 'script'))
        self.assertEqual(set(saved['approvals']), {'script'})
        self.assertEqual(saved['tasks']['research']['status'], 'skipped')
        for stage in ('storyboard', 'audio', 'packaging', 'render'):
            context = self.service.context(run['id'], stage)
            self.assertEqual(context['task_guide']['preproduction']['mode'], 'reuse')
            self.assertEqual(context['task_guide']['preproduction']['artifact_id'], saved['source_preproduction_id'])
        self.assertEqual({x['id'] for x in self.service.next(run['id'])['tasks']},
                         {'storyboard', 'audio', 'packaging'})

    def test_changed_script_keeps_old_package_as_baseline_not_new_instructions(self):
        run = self.create()
        self.accept(run)
        different = self.root / 'revised.txt'
        different.write_text(TEXT + 'An explicit new version.')
        artifact = self.service.artifacts.put(different, 'script')
        def change(tx, state):
            state['artifacts'][artifact['id']] = artifact
            state['tasks']['script'].update(status='complete', outputs=[artifact['id']])
        self.service.store.mutate(run['id'], change)
        packet = self.service.context(run['id'], 'storyboard')
        self.assertEqual(packet['task_guide']['preproduction']['mode'], 'stale_baseline')

    def test_cli_import_and_materialized_production_packet_preserve_input(self):
        from ytvideos.entry import start_packet
        from ytvideos.packets import instruction_files
        run = self.create()
        output = io.StringIO()
        argv = ['--db', str(self.root / 'state.sqlite3'), '--workspace', str(self.root / 'workspace'),
                '--project-root', str(ROOT), '--run', run['id'], '--revision', str(run['revision']),
                '--sha256', file_digest(self.script), '--source', 'fixture://owner-message-cli',
                '--message', 'Produce the selected prepared fixture.', '--origin', 'fixture://commit/script.en.txt',
                '--preproduction', str(self.plan)]
        with patch.dict(os.environ, {}, clear=True), redirect_stdout(output):
            self.assertEqual(main(argv), 0)
        self.assertFalse(json.loads(output.getvalue())['providers_called'])
        packet = self.service.context(run['id'], 'storyboard')
        payload, files = instruction_files(packet)
        self.assertEqual(payload['task_guide']['preproduction']['artifact']['sha256'], file_digest(self.plan))
        self.assertEqual(json.loads(files['TASK.json'])['task_guide']['preproduction'],
                         packet['task_guide']['preproduction'])
        with patch.dict(os.environ, {}, clear=True):
            entry = start_packet(self.service, run['id'])
        self.assertEqual({x['task_id'] for x in entry['read_next']}, {'storyboard', 'audio', 'packaging'})

    def test_legacy_source_only_route_is_unchanged(self):
        run = self.create()
        self.accept(run, preproduction=None)
        saved = self.service.store.get(run['id'])
        self.assertNotIn('source_preproduction', saved['pins'])
        self.assertNotIn('preproduction', self.service.context(run['id'], 'storyboard')['task_guide'])
        self.assertTrue(valid_approval(saved, 'script'))
        with self.assertRaises(Conflict):
            self.accept(run)  # Cannot silently attach a plan to an already consumed source event.

    def test_tampered_package_or_pin_is_rejected(self):
        run = self.create()
        self.accept(run)
        saved = self.service.store.get(run['id'])
        artifact = saved['artifacts'][saved['source_preproduction_id']]
        target = self.service.artifacts.resolve(artifact)
        target.write_text('{}')
        with self.assertRaises(WorkflowError):
            self.service.artifacts.resolve(artifact)
        with self.assertRaises(WorkflowError):
            self.accept(run)
        self.service.store.mutate(run['id'], lambda tx, state: state['pins'].update(source_preproduction='0'*64))
        with self.assertRaisesRegex(WorkflowError, 'pin'):
            self.service.context(run['id'], 'storyboard')

    def test_required_preparation_documents_reach_script_and_production_but_not_image_workers(self):
        from ytvideos.context import PREPRODUCTION_REFERENCE, PREPRODUCTION_PROCEDURE, instruction_packet
        for stage in ('script', 'storyboard', 'audio', 'packaging', 'render'):
            packet = instruction_packet(ROOT, channel='paper_detour', format='short', stage=stage)
            for path in (PREPRODUCTION_REFERENCE, PREPRODUCTION_PROCEDURE):
                self.assertIn(path, packet['references'])
                document = next(x for x in packet['reference_documents'] if x['path'] == path)
                self.assertEqual(document['text'], (ROOT / path).read_text())
        packet = instruction_packet(ROOT, channel='nuviko_history', format='long', stage='scene_image')
        self.assertNotIn(PREPRODUCTION_REFERENCE, packet['references'])
        self.assertNotIn('channels/paper_detour/docs/FLOW_PRODUCTION.md', packet['references'])

    def test_prepared_prompt_survives_normal_storyboard_completion(self):
        from ytvideos.workflow import required_checks
        run = self.create(capabilities={'model.text': {'available': True, 'evidence': 'software fixture'}})
        self.accept(run)
        claim = self.service.claim(run['id'], 'storyboard', 'software-fixture')
        board = self.root / 'storyboard.json'
        board.write_text(json.dumps({'scenes': self.data['scenes']}))
        receipt = self.root / 'receipt.json'
        receipt.write_text(json.dumps({
            'run_id': run['id'], 'task_id': 'storyboard', 'worker': claim['worker'],
            'input_hash': claim['input_hash'], 'output_sha256': file_digest(board),
            'checks': [{'name': name, 'status': 'pass', 'method': 'synthetic software fixture only',
                        'observed': {'fixture': True}} for name in required_checks('storyboard')]}))
        self.service.complete(run['id'], 'storyboard', claim['token'], board, receipt, actual_units=0)
        task = self.service.store.get(run['id'])['tasks']['image:S001']
        self.assertEqual(task['payload']['prompt'], self.data['scenes'][0]['prompt'])
        self.assertEqual(task['payload']['asset_ids'], ['PROP'])
        self.assertEqual(task['status'], 'pending')  # No image dispatched; fixture is not media QA.

    def test_signed_host_does_not_gain_an_import_bypass(self):
        run = self.create()
        self.service.approvals.public_key = 'synthetic-configured-verifier'
        with self.assertRaisesRegex(WorkflowError, 'signed'):
            self.accept(run)
        self.assertEqual(self.service.store.get(run['id'])['approvals'], {})

    def test_active_or_unknown_work_cannot_be_overwritten_by_import(self):
        run = self.create()
        self.service.store.mutate(run['id'], lambda tx, state: state['tasks']['audio'].update(status='unknown'))
        with self.assertRaises(Conflict):
            self.accept(run)
        saved = self.service.store.get(run['id'])
        self.assertEqual(saved['approvals'], {})
        self.assertNotIn('source_preproduction_id', saved)


if __name__ == '__main__':
    unittest.main()

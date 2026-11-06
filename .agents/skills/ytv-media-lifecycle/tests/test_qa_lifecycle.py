import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import workspace as w
import qa_lifecycle as q


class QALifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.ep = self.root / 'episode'; self.ep.mkdir()
        w.initialize(self.ep); w.start(self.ep, 'qa-one', 'reviewer')
        self.source = self.put('Deliverables/film.mp4', b'original film')
        self.frames = [self.put(f'Work/qa-one/scratch/qa/{i:06}.png', b'frame' + bytes([i])) for i in range(3)]
        self.report_rel = 'Edit/QA/qa-one/report.json'
        self.report = {'media': str(self.source), 'sha256': w.inventory.sha256(self.source),
                       'technical_status': 'PASS', 'failures': [], 'policy_failures': [],
                       'plan': {'required_review_checks': ['stream_metadata', 'full_decode', 'frame_sampling']},
                       'reported_freshness': {'status': 'CURRENT'},
                       'checks': {'full_decode': 'PASS', 'frame_extraction': 'PASS'},
                       'requested_frame_indices': [0, 5, 9],
                       'frame_recipe': {'argv': ['ffmpeg', 'exact args'], 'ffmpeg_version': 'test'},
                       'frame_map': [{'index': n, 'path': os.path.relpath(p, self.ep / 'Edit/QA/qa-one')}
                                     for n, p in zip([0, 5, 9], self.frames)]}
        self.put(self.report_rel, json.dumps(self.report).encode())
        self.review_rel = 'Edit/QA/qa-one/review.json'
        self.review = {'version': 1, 'run': 'qa-one', 'file': str(self.source),
                       'sha256': self.report['sha256'], 'report_sha256': w.inventory.sha256(self.ep / self.report_rel),
                       'verdict': 'PASS', 'freshness': 'CURRENT', 'reviewer': 'actual reviewer',
                       'writer_finished': True, 'reconstruction_verified': True,
                       'required_checks': ['stream_metadata', 'full_decode', 'frame_sampling'],
                       'checks': {'stream_metadata': 'PASS', 'full_decode': 'PASS', 'frame_sampling': 'PASS',
                                  'subjective_audio_listening': 'UNVERIFIED'},
                       'inspected_frame_indices': [0, 5, 9], 'retain_indices': [5],
                       'evidence': ['Edit/QA/qa-one/edit-and-rebuild-proof.json']}
        self.put(self.review['evidence'][0], b'actual edit binding and rebuild comparison')
        self.save_review()

    def put(self, rel, content):
        p = self.ep / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(content)
        return p

    def save_review(self): self.put(self.review_rel, json.dumps(self.review).encode())

    def register(self): q.register_qa(self.ep, 'qa-one', 'reviewer', self.report_rel)

    def complete(self): w.finish(self.ep, 'qa-one', 'reviewer', 'complete', True)

    def finalize(self, execute=True, audit=None):
        return q.finalize_qa(self.ep, 'qa-one', 'reviewer', self.review_rel,
                             audit or w.fresh_audit(self.ep, self.root), execute)

    def test_batch_hashes_source_once_and_keeps_final_and_evidence(self):
        original = w.inventory.sha256
        with patch.object(w.inventory, 'sha256', wraps=original) as hashed:
            self.register()
            self.assertEqual(sum(call.args[0] == self.source for call in hashed.call_args_list), 1)
        self.complete()
        self.assertEqual(self.finalize(False)['files'], 3)
        self.assertTrue(all(p.exists() for p in self.frames))
        extra = self.put('Work/qa-one/scratch/unregistered.png', b'keep')
        self.assertEqual(self.finalize()['files'], 3)
        self.assertFalse(any(p.exists() for p in self.frames))
        self.assertTrue(extra.exists()); self.assertTrue(self.source.exists())
        self.assertEqual((self.ep / 'Edit/QA-Retention/qa-one/000000005.png').read_bytes(), b'frame\1')
        self.assertTrue((self.ep / self.report_rel).exists())
        self.assertEqual(self.finalize()['files'], 0)

    def test_active_failed_and_wrong_owner_refused(self):
        self.register()
        with self.assertRaises(ValueError): self.finalize()
        with self.assertRaises(ValueError): q.register_qa(self.ep, 'qa-one', 'other', self.report_rel)
        w.finish(self.ep, 'qa-one', 'reviewer', 'failed', True)
        with self.assertRaises(ValueError): self.finalize()

    def test_full_acceptance_and_exact_review_required(self):
        self.register(); self.complete()
        for field, value in [('verdict', 'UNVERIFIED'), ('freshness', 'STALE'),
                             ('sha256', 'wrong'), ('inspected_frame_indices', [0]),
                             ('reconstruction_verified', False), ('evidence', [])]:
            before = self.review[field]; self.review[field] = value; self.save_review()
            with self.subTest(field=field), self.assertRaises(ValueError): self.finalize()
            self.assertTrue(all(p.exists() for p in self.frames))
            self.review[field] = before
        self.review['checks']['frame_sampling'] = 'FAIL'; self.save_review()
        with self.assertRaises(ValueError): self.finalize()

    def test_source_report_frame_or_metadata_change_blocks_entire_batch(self):
        self.register(); self.complete()
        audit = w.fresh_audit(self.ep, self.root)
        self.frames[-1].write_bytes(b'changed')
        with self.assertRaises(ValueError): self.finalize(audit=audit)
        self.assertTrue(self.frames[0].exists())

    def test_changed_source_and_report_are_refused(self):
        self.register(); self.complete()
        self.source.write_bytes(b'new version')
        with self.assertRaises(ValueError): self.finalize()
        self.assertTrue(all(p.exists() for p in self.frames))

    def test_import_pin_and_other_run_reference_are_protected(self):
        self.register(); self.complete()
        package = self.root / 'test.palmier'; package.mkdir()
        (package / 'project.json').write_text('{"timelines":[]}')
        media = package / 'media.json'
        media.write_text(json.dumps({'entries': [{'source': {'external': {'absolutePath': str(self.frames[1])}}}]}))
        self.assertEqual(len(self.finalize(False)['kept']), 1)
        media.write_text('{"entries":[]}')
        policy = self.put('Edit/MediaLifecycle/policy.json', json.dumps({'version': 1, 'pins': [
            {'path': str(self.frames[1].relative_to(self.ep)), 'reason': 'comparison'}]}).encode())
        audit = w.fresh_audit(self.ep, self.root, policy)
        self.assertEqual(len(self.finalize(False, audit=audit)['kept']), 1)
        w.start(self.ep, 'other', 'other')
        self.put('Work/other/manifest.json', json.dumps({'status':'active', 'input': str(self.frames[1])}).encode())
        self.assertIn('another managed run', self.finalize(False)['kept'][0]['reason'])
        self.assertTrue(all(p.exists() for p in self.frames))

    def test_replaced_symlink_and_hardlink_refused(self):
        self.register(); self.complete()
        alias = self.ep / 'Work/qa-one/scratch/alias.png'
        os.link(self.frames[1], alias)
        with self.assertRaises(ValueError): self.finalize()
        alias.unlink(); self.frames[1].unlink(); self.frames[1].symlink_to(self.source)
        with self.assertRaises(ValueError): self.finalize()
        self.assertTrue(self.source.exists())

    def test_interrupted_unlink_resumes_from_durable_prepared_event(self):
        self.register(); self.complete()
        original = Path.unlink
        def interrupted(p, *args, **kwargs):
            original(p, *args, **kwargs)
            if p == self.frames[0]: raise OSError('simulated crash after unlink')
        with patch.object(Path, 'unlink', interrupted), self.assertRaises(OSError): self.finalize()
        self.assertFalse(self.frames[0].exists()); self.assertTrue(self.frames[1].exists())
        self.assertEqual(self.finalize()['files'], 3)
        self.assertEqual(self.finalize()['files'], 0)

    def test_legacy_registration_is_explicit_and_duplicate_is_refused(self):
        self.complete()
        with self.assertRaises(ValueError): self.register()
        q.register_qa(self.ep, 'qa-one', 'reviewer', self.report_rel, legacy=True)
        with self.assertRaises(ValueError): q.register_qa(self.ep, 'qa-one', 'reviewer', self.report_rel, legacy=True)
        self.finalize()

    def test_pinned_frame_stays_while_other_temporary_frames_are_cleaned(self):
        self.register(); self.complete()
        policy = self.put('Edit/MediaLifecycle/policy.json', json.dumps({'version': 1, 'pins': [
            {'path': str(self.frames[1].relative_to(self.ep)), 'reason': 'comparison'}]}).encode())
        result = self.finalize(audit=w.fresh_audit(self.ep, self.root, policy))
        self.assertEqual(result['files'], 2); self.assertEqual(len(result['kept']), 1)
        self.assertTrue(self.frames[1].exists()); self.assertFalse(self.frames[0].exists())

    def test_changed_evidence_during_cleanup_preserves_remaining_files(self):
        self.register(); self.complete()
        original = w.journal
        def change_after_one(episode, event):
            original(episode, event)
            if event.get('state') == 'complete':
                self.put(self.review['evidence'][0], b'changed evidence')
        with patch.object(w, 'journal', change_after_one), self.assertRaises(ValueError): self.finalize()
        self.assertFalse(self.frames[0].exists()); self.assertTrue(self.frames[1].exists())
        with self.assertRaises(ValueError): self.finalize()  # changed acceptance cannot resume

    def test_required_checks_cannot_be_dropped_from_frozen_plan(self):
        self.report['plan']['required_review_checks'].append('motion_framing')
        self.put(self.report_rel, json.dumps(self.report).encode())
        self.review['report_sha256'] = w.inventory.sha256(self.ep / self.report_rel)
        self.save_review(); self.register(); self.complete()
        with self.assertRaises(ValueError): self.finalize()

    def test_registration_refuses_source_paths_and_fails_atomically(self):
        self.report['frame_map'][-1]['path'] = os.path.relpath(self.source, self.ep / 'Edit/QA/qa-one')
        self.put(self.report_rel, json.dumps(self.report).encode())
        with self.assertRaises(ValueError): self.register()
        manifest = json.loads((self.ep / 'Work/qa-one/manifest.json').read_text())
        self.assertNotIn('qa_batch', manifest)

    def test_generic_cleanup_preserves_qa_reconstruction_source_in_other_run(self):
        w.start(self.ep, 'render', 'renderer')
        source = self.put('Work/render/scratch/native.mp4', b'original film')
        self.report['media'] = str(source)
        self.put(self.report_rel, json.dumps(self.report).encode())
        self.register()
        w.register(self.ep, 'render', 'renderer', str(source.relative_to(self.ep)), 'scratch',
                   ['Deliverables/film.mp4'], [self.review['evidence'][0]])
        w.finish(self.ep, 'render', 'renderer', 'complete', True)
        result = w.clean(self.ep, 'render', 'renderer', w.fresh_audit(self.ep, self.root), True)
        self.assertEqual(result['files'], 0)
        self.assertTrue(source.exists())


if __name__ == '__main__': unittest.main()

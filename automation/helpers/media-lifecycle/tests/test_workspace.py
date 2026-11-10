import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import workspace as w


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.ep = self.root / 'episode'; self.ep.mkdir()
        w.initialize(self.ep)
        w.start(self.ep, 'one', 'owner')
        self.source = self.put('Assets/Generated/source.mp4', b'original-payload')
        self.proof = self.put('Edit/proof.json', b'{"comparison":"verified"}')
        self.scratch = self.put('Work/one/scratch/stream.h264', b'original-payload')

    def put(self, rel, content):
        p = self.ep / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(content)
        return p

    def register(self):
        w.register(self.ep, 'one', 'owner', 'Work/one/scratch/stream.h264', 'scratch',
                   ['Assets/Generated/source.mp4'], ['Edit/proof.json'])

    def audit(self):
        return w.fresh_audit(self.ep, self.root)

    def complete(self):
        w.finish(self.ep, 'one', 'owner', 'complete', True)

    def test_init_is_idempotent_and_existing_media_is_untouched(self):
        before = self.source.read_bytes()
        layout = (self.ep / 'Edit/MediaLifecycle/layout.json').read_bytes()
        w.initialize(self.ep)
        self.assertEqual(self.source.read_bytes(), before)
        self.assertEqual((self.ep / 'Edit/MediaLifecycle/layout.json').read_bytes(), layout)

    def test_no_duplicate_run_or_wrong_owner(self):
        with self.assertRaises(FileExistsError): w.start(self.ep, 'one', 'other')
        with self.assertRaises(ValueError): w.finish(self.ep, 'one', 'other', 'complete', True)
        with self.assertRaises(ValueError): w.finish(self.ep, 'one', 'owner', 'complete', False)

    def test_exact_cleanup_dry_run_and_execution(self):
        self.register(); self.complete()
        preview = self.put('Work/one/previews/keep.mp4', b'comparison')
        self.assertEqual(w.clean(self.ep, 'one', 'owner', self.audit())['files'], 1)
        self.assertTrue(self.scratch.exists())
        result = w.clean(self.ep, 'one', 'owner', self.audit(), execute=True)
        self.assertEqual(result['logical_bytes'], len(b'original-payload'))
        self.assertFalse(self.scratch.exists())
        self.assertTrue(self.source.exists()); self.assertTrue(preview.exists())
        self.assertEqual(w.clean(self.ep, 'one', 'owner', self.audit(), execute=True)['files'], 0)

    def test_changed_file_or_reconstruction_input_blocks_cleanup(self):
        self.register(); self.complete()
        self.source.write_bytes(b'changed-source')
        with self.assertRaises(ValueError): w.clean(self.ep, 'one', 'owner', self.audit(), True)
        self.assertTrue(self.scratch.exists())

    def test_multiple_deletions_do_not_stale_their_own_manifest(self):
        self.register()
        second = self.put('Work/one/scratch/second.h264', b'original-payload')
        w.register(self.ep, 'one', 'owner', 'Work/one/scratch/second.h264', 'scratch',
                   ['Assets/Generated/source.mp4'], ['Edit/proof.json'])
        self.complete()
        rows = [{'path': rel, 'role':'scratch', 'status':'review', 'reason':'extraction',
                 'evidence':['Edit/proof.json'], 'rebuild_from':['Assets/Generated/source.mp4']}
                for rel in ['Work/one/scratch/stream.h264', 'Work/one/scratch/second.h264']]
        policy = self.put('Edit/MediaLifecycle/test-policy.json', json.dumps({'version':1,'candidates':rows}).encode())
        audit = w.fresh_audit(self.ep, self.root, policy)
        self.assertIn(str(self.ep / 'Work/one/manifest.json'), audit['inputs'])
        self.assertEqual(w.clean(self.ep, 'one', 'owner', audit, True)['files'], 2)
        self.assertFalse(self.scratch.exists()); self.assertFalse(second.exists())

    def test_active_failed_and_abandoned_runs_are_not_cleaned(self):
        self.register()
        with self.assertRaises(ValueError): w.clean(self.ep, 'one', 'owner', self.audit(), True)
        w.finish(self.ep, 'one', 'owner', 'failed', True)
        with self.assertRaises(ValueError): w.clean(self.ep, 'one', 'owner', self.audit(), True)

    def test_imported_scratch_is_never_deleted(self):
        self.register(); self.complete()
        package = self.root / 'external.palmier'; package.mkdir()
        (package / 'project.json').write_text('{"timelines":[]}')
        (package / 'media.json').write_text(json.dumps({'entries': [
            {'source': {'external': {'absolutePath': str(self.scratch)}}}]}))
        with self.assertRaises(ValueError): w.clean(self.ep, 'one', 'owner', self.audit(), True)
        self.assertTrue(self.scratch.exists())

    def test_symlink_replacement_and_hardlink_are_refused(self):
        self.register(); self.complete()
        self.scratch.unlink(); self.scratch.symlink_to(self.source)
        with self.assertRaises(ValueError): w.clean(self.ep, 'one', 'owner', self.audit(), True)
        self.assertTrue(self.source.exists())

    def test_role_and_path_escape_refused(self):
        for value, role in [('Assets/Generated/source.mp4', 'scratch'), ('../outside', 'preview')]:
            with self.assertRaises(ValueError): w.register(self.ep, 'one', 'owner', value, role)
        with self.assertRaises(ValueError): w.start(self.ep, '../escape', 'owner')

    def test_rejected_preview_cleanup_requires_exact_decision(self):
        preview = self.put('Work/one/previews/rejected.mp4', b'rejected')
        self.put('Edit/rejection.json', json.dumps({'decision':'rejected', 'file':str(preview),
                 'sha256':w.inventory.sha256(preview)}).encode())
        w.register(self.ep, 'one', 'owner', 'Work/one/previews/rejected.mp4', 'preview',
                   evidence=['Edit/rejection.json'], disposition='rejected')
        self.complete()
        w.clean(self.ep, 'one', 'owner', self.audit(), True)
        self.assertFalse(preview.exists())
        self.assertTrue(self.source.exists())

    def test_hardlinked_disposable_requires_review(self):
        self.register(); self.complete()
        os.link(self.scratch, self.ep / 'Work/one/scratch/alias.h264')
        with self.assertRaises(ValueError): w.clean(self.ep, 'one', 'owner', self.audit(), True)
        self.assertTrue(self.scratch.exists())

    def test_pending_preview_can_be_rejected_after_actual_review(self):
        preview = self.put('Work/one/previews/review.mp4', b'candidate')
        w.register(self.ep, 'one', 'owner', 'Work/one/previews/review.mp4', 'preview')
        self.complete()
        self.assertEqual(w.clean(self.ep, 'one', 'owner', self.audit())['files'], 0)
        self.put('Edit/decision.json', json.dumps({'file':str(preview),
                 'sha256':w.inventory.sha256(preview), 'decision':'rejected'}).encode())
        w.reject(self.ep, 'one', 'owner', 'Work/one/previews/review.mp4', 'Edit/decision.json')
        self.assertTrue(preview.exists())
        self.assertEqual(w.clean(self.ep, 'one', 'owner', self.audit(), True)['files'], 1)
        self.assertFalse(preview.exists())

    def test_legacy_preview_move_preserves_hash_and_old_receipt_path(self):
        p = self.put('Edit/old/review.mp4', b'review-payload')
        event = w.adopt(self.ep, 'one', 'owner', 'Edit/old/review.mp4', 'preview', self.audit(), True, True)
        target = self.ep / event['to']
        self.assertTrue(p.is_symlink())
        self.assertEqual(target.read_bytes(), b'review-payload')
        self.assertEqual(p.read_bytes(), target.read_bytes())
        self.assertIn('"state": "complete"', (self.ep / 'Edit/MediaLifecycle/locations.jsonl').read_text())

    def test_legacy_source_or_imported_file_cannot_be_moved(self):
        self.put('Source/original.mp4', b'source')
        with self.assertRaises(ValueError): w.adopt(self.ep, 'one', 'owner', 'Source/original.mp4', 'scratch', self.audit(), True)
        package = self.root / 'external.palmier'; package.mkdir()
        old = self.put('Edit/old.mp4', b'imported')
        (package / 'project.json').write_text('{"timelines":[]}')
        (package / 'media.json').write_text(json.dumps({'entries': [{'source': {'external': {'absolutePath': str(old)}}}]}))
        with self.assertRaises(ValueError): w.adopt(self.ep, 'one', 'owner', 'Edit/old.mp4', 'scratch', self.audit(), True)
        self.assertTrue(old.exists())

    def test_prepared_move_can_resume_after_observed_metadata_change(self):
        old = self.put('Edit/old.mp4', b'review')
        policy = self.put('Edit/policy.json', b'{"version":1}')
        audit = w.fresh_audit(self.ep, self.root, policy)
        policy.write_text('{"version":1,"pins":[]}')
        with self.assertRaisesRegex(ValueError, 'source preserved'):
            w.adopt(self.ep, 'one', 'owner', 'Edit/old.mp4', 'preview', audit, True, True)
        self.assertFalse(old.is_symlink()); self.assertTrue(old.exists())
        event = w.adopt(self.ep, 'one', 'owner', 'Edit/old.mp4', 'preview', self.audit(), True, True)
        self.assertTrue(old.is_symlink())
        self.assertEqual((self.ep / event['to']).read_bytes(), b'review')

    def test_promotion_preserves_previous_until_exact_new_receipt(self):
        old = self.put('Deliverables/old.mp4', b'old')
        self.put('Deliverables/current.json', json.dumps({'version':1,'items':{'full_en_mp4':{'path':'Deliverables/old.mp4'}}}).encode())
        receipt = self.put('Edit/new-qa.json', json.dumps({'file':str(self.source),'sha256':w.inventory.sha256(self.source)}).encode())
        result = w.promote(self.ep, 'Assets/Generated/source.mp4', 'new.mp4', 'full_en_mp4', 'Edit/new-qa.json')
        self.assertTrue(old.exists())
        self.assertEqual((self.ep / result['path']).read_bytes(), self.source.read_bytes())
        current_before = (self.ep / 'Deliverables/current.json').read_bytes()
        receipt.write_text('{"file":"wrong","sha256":"wrong"}')
        with self.assertRaises(ValueError): w.promote(self.ep, 'Assets/Generated/source.mp4', 'bad.mp4', 'full_en_mp4', 'Edit/new-qa.json')
        self.assertEqual((self.ep / 'Deliverables/current.json').read_bytes(), current_before)
        self.assertFalse((self.ep / 'Deliverables/bad.mp4').exists())

    def test_promotion_never_overwrites_existing_delivery(self):
        existing = self.put('Deliverables/new.mp4', b'user-file')
        self.put('Edit/qa.json', json.dumps({'file':str(self.source),'sha256':w.inventory.sha256(self.source)}).encode())
        with self.assertRaises(FileExistsError): w.promote(self.ep, 'Assets/Generated/source.mp4', 'new.mp4', 'full_en_mp4', 'Edit/qa.json')
        self.assertEqual(existing.read_bytes(), b'user-file')
        self.assertFalse(list((self.ep / 'Deliverables').glob('*.staging')))


if __name__ == '__main__': unittest.main()

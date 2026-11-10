"""Behavioral checks on synthetic files; no real episode or live app is used."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/media_lifecycle.py'
spec = importlib.util.spec_from_file_location('lifecycle', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.episode = self.root / 'episodes/001'
        self.episode.mkdir(parents=True)
        self.raw = self.put('Edit/QA/native.h264', b'video-payload')
        self.final = self.put('Edit/final.mp4', b'video-payload')
        self.evidence = self.put('Edit/QA/report.json', b'{"video_hash":"saved"}')
        self.policy = self.episode / 'Edit/MediaLifecycle/policy.json'
        self.data = {'version': 1, 'pins': [], 'current': [], 'active_work': [],
                     'candidates': [{'path': 'Edit/QA/native.h264', 'role': 'scratch',
                                     'status': 'review', 'reason': 'extracted stream',
                                     'evidence': ['Edit/QA/report.json'],
                                     'rebuild_from': ['Edit/final.mp4']}]}
        self.save_policy()

    def put(self, rel, data):
        p = self.episode / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def save_policy(self):
        self.policy.parent.mkdir(parents=True, exist_ok=True)
        self.policy.write_text(json.dumps(self.data))

    def audit(self, packages=()):
        return m.audit(self.root, self.episode, self.policy, packages)

    def row(self, audit):
        return next(r for r in audit['files'] if r['path'] == 'Edit/QA/native.h264')

    def saved_audit(self):
        p = self.root / 'audit/audit.json'
        m.write_report(self.audit(), p.parent)
        return p

    def test_audit_and_plan_preserve_all_media(self):
        before = {p: p.read_bytes() for p in (self.raw, self.final, self.evidence)}
        report = self.saved_audit()
        plan = m.plan(report)
        m.write_report(plan, self.root / 'plan')
        self.assertFalse(plan['executable'])
        self.assertFalse(plan['deletion_implemented'])
        self.assertEqual(plan['entries'][0]['classification'], 'REVIEW_CANDIDATE')
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_source_and_imported_scratch_are_protected(self):
        self.put('Source/original.png', b'image')
        package = self.root / 'external.palmier'
        package.mkdir()
        (package / 'media.json').write_text(json.dumps({'entries': [
            {'source': {'external': {'absolutePath': str(self.raw)}}}]}))
        (package / 'project.json').write_text('{"timelines": []}')
        result = self.audit([package])
        self.assertEqual(self.row(result)['classification'], 'BLOCKED')
        self.assertIn('LEGACY_PACKAGE_IMPORT_OR_SNAPSHOT_REFERENCE', self.row(result)['protections'])
        self.assertEqual(next(r for r in result['files'] if r['path'].startswith('Source/'))['classification'], 'PROTECTED')

    def test_snapshot_direct_reference_is_protected(self):
        package = self.root / 'external.palmier'
        (package / 'snapshots').mkdir(parents=True)
        (package / 'media.json').write_text('{"entries": []}')
        (package / 'project.json').write_text('{"timelines": []}')
        (package / 'snapshots/old.json').write_text(json.dumps({'source': str(self.raw)}))
        self.assertEqual(self.row(self.audit([package]))['classification'], 'BLOCKED')

    def test_active_work_pin_and_current_override_candidate(self):
        for key in ('active_work', 'pins', 'current'):
            with self.subTest(key=key):
                self.data[key] = [{'path': 'Edit/QA', 'reason': 'retained'}]
                self.save_policy()
                self.assertEqual(self.row(self.audit())['classification'], 'BLOCKED')
                self.data[key] = []

    def test_text_mention_is_not_import_and_requires_review(self):
        self.put('Edit/consumer.py', b'input_path = "Edit/QA/native.h264"')
        row = self.row(self.audit())
        self.assertFalse(row['project_references'])
        self.assertIn('TEXT_REFERENCE_REVIEW', row['blockers'])

    def test_missing_rebuild_source_blocks_candidate(self):
        self.final.unlink()  # synthetic fixture only
        self.assertTrue(any(x.startswith('MISSING_REBUILD_FROM') for x in self.row(self.audit())['blockers']))

    def test_same_size_changed_file_rejected_by_plan(self):
        path = self.saved_audit()
        self.raw.write_bytes(b'other-payload')
        self.assertIn('STALE_FILE_IDENTITY', m.plan(path)['entries'][0]['blockers'])

    def test_dependency_change_stales_plan(self):
        path = self.saved_audit()
        self.evidence.write_text('{"changed":true}')
        self.assertIn('STALE_AUDIT_INPUTS', m.plan(path)['entries'][0]['blockers'])

    def test_ownership_evidence_change_stales_plan(self):
        owner = self.put('Edit/OWNERSHIP.json', b'{"status":"active"}')
        self.data['active_work'] = [{'path': 'Edit', 'reason': 'writer',
                                     'evidence': ['Edit/OWNERSHIP.json']}]
        self.save_policy()
        path = self.saved_audit()
        owner.write_text('{"status":"complete"}')
        self.assertIn('STALE_AUDIT_INPUTS', m.plan(path)['entries'][0]['blockers'])

    def test_already_covered_package_alias_is_not_read_twice(self):
        package = self.root / 'canonical.palmier'
        package.mkdir()
        (package / 'media.json').write_text('{"entries": []}')
        (package / 'project.json').write_text('{"timelines": []}')
        alias = self.root / 'alias.palmier'
        alias.symlink_to(package, target_is_directory=True)
        result = self.audit([alias])
        self.assertFalse(result['errors'])
        self.assertEqual(len(result['packages']), 1)
        self.assertEqual(result['covered_package_aliases'][0]['covered_by'], str(package))

    def test_symlink_replacement_in_plan_is_refused(self):
        path = self.saved_audit()
        self.raw.unlink()
        self.raw.symlink_to(self.final)
        self.assertTrue(any(x.startswith('FILE_RECHECK_FAILED') for x in m.plan(path)['entries'][0]['blockers']))

    def test_hardlinks_have_distinct_logical_and_unique_inode_totals(self):
        import os
        os.link(self.raw, self.raw.with_name('alias.h264'))
        result = self.audit()
        self.assertGreater(result['totals']['logical_bytes'], result['totals']['unique_inode_logical_bytes'])
        self.assertIn('HARDLINK_REVIEW', self.row(result)['blockers'])

    def test_existing_output_or_symlink_output_not_overwritten(self):
        result = self.audit()
        out = self.root / 'output'
        m.write_report(result, out)
        before = (out / 'audit.json').read_bytes()
        with self.assertRaises(FileExistsError):
            m.write_report(result, out)
        alias = self.root / 'alias'
        alias.symlink_to(out, target_is_directory=True)
        with self.assertRaises(ValueError):
            m.write_report(result, alias / 'new')
        self.assertEqual(before, (out / 'audit.json').read_bytes())

    def test_policy_escape_and_candidate_symlink_are_refused(self):
        for value in ('../../outside.mp4', '/outside.mp4'):
            self.data['candidates'][0]['path'] = value
            self.save_policy()
            with self.assertRaises(ValueError):
                self.audit()
        self.data['candidates'][0]['path'] = 'Edit/QA/native.h264'
        self.save_policy()
        self.raw.unlink()
        self.raw.symlink_to(self.final)
        with self.assertRaises(ValueError):
            self.audit()

    def test_unknown_package_blocks_plan_and_is_reported(self):
        result = self.audit([self.root / 'missing.palmier'])
        self.assertTrue(result['errors'])
        out = self.root / 'audit'
        m.write_report(result, out)
        self.assertIn('INCOMPLETE_DEPENDENCY_SCAN', m.plan(out / 'audit.json')['entries'][0]['blockers'])

    def test_report_must_not_write_in_source_or_project(self):
        result = self.audit()
        for out in (self.episode / 'Source/new', self.root / 'target.palmier/QA'):
            with self.assertRaises(ValueError):
                m.write_report(result, out)
            self.assertFalse(out.exists())

    def test_cli_has_no_mutation_command(self):
        with self.assertRaises(SystemExit) as caught:
            m.main(['apply'])
        self.assertEqual(caught.exception.code, 2)


if __name__ == '__main__':
    unittest.main()

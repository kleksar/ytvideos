"""Exercise real FFmpeg selection for a long-film frame plan, without audio."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import unittest
import json
import sys
import tempfile


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/inspect_video.py'
SPEC = importlib.util.spec_from_file_location('inspect_video', SCRIPT)
qa = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qa)


class FrameSelectionTest(unittest.TestCase):
    def test_managed_output_traversal_is_refused_before_writing(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            with self.assertRaises(ValueError):
                qa.inspect_managed(root, 'test', 'owner', root / 'video.mp4', {},
                                   root / 'Edit/QA/../../Source/wrong')
            self.assertFalse((root / 'Source').exists())

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'AV tools unavailable')
    def test_managed_qa_registration_retention_and_retest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            episode = root / 'episode'; episode.mkdir()
            media = episode / 'Deliverables/technical.mp4'; media.parent.mkdir()
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                            'testsrc2=size=32x32:rate=10:duration=1', '-an',
                            '-c:v', 'libx264', str(media)], check=True, capture_output=True)
            plan = {'frame_count': 10, 'fps': '10/1', 'freshness': {'status': 'CURRENT'},
                    'required_review_checks': ['stream_metadata', 'full_decode', 'frame_sampling'],
                    'scenes': [{'id': 'test', 'start': 0, 'end': 10}]}
            report_dir = episode / 'Edit/QA/managed-one'
            result = qa.inspect_managed(episode, 'managed-one', 'test-owner', media, plan, report_dir)
            self.assertEqual(result['technical_status'], 'PASS')
            self.assertEqual(result['verdict'], 'UNVERIFIED')  # extraction is not a review
            import workspace as w
            import qa_lifecycle as lifecycle
            manifest = json.loads((episode / 'Work/managed-one/manifest.json').read_text())
            self.assertEqual(manifest['status'], 'complete')
            self.assertEqual(len(manifest['qa_batch']['frames']), 3)
            # Actually reconstruct the selection to another path and compare PNG hashes.
            reconstructed = episode / 'Work/managed-one/scratch/reconstructed'
            reconstructed.mkdir()
            command = list(result['frame_recipe']['argv'])
            command[-1] = str(reconstructed / '%06d.png')
            subprocess.run(command, capture_output=True, check=True)
            for frame, copy in zip(manifest['qa_batch']['frames'], sorted(reconstructed.glob('*.png'))):
                self.assertEqual(w.inventory.sha256(episode / frame['path']), w.inventory.sha256(copy))
            proof = report_dir / 'reconstruction.json'
            proof.write_text(json.dumps({'argv': command, 'comparison': 'all three PNG SHA256 equal'}))
            report_rel = str((report_dir / 'report.json').relative_to(episode))
            review = {'version': 1, 'run': 'managed-one', 'file': str(media), 'sha256': result['sha256'],
                      'report_sha256': w.inventory.sha256(episode / report_rel),
                      'verdict': 'PASS', 'freshness': 'CURRENT', 'reviewer': 'technical fixture test',
                      'writer_finished': True, 'reconstruction_verified': True,
                      'required_checks': ['stream_metadata', 'full_decode', 'frame_sampling'],
                      'checks': {'stream_metadata':'PASS', 'full_decode':'PASS', 'frame_sampling':'PASS'},
                      'inspected_frame_indices': result['requested_frame_indices'], 'retain_indices': [0],
                      'evidence': [str(proof.relative_to(episode))]}
            review_rel = 'Edit/QA/managed-one/review.json'
            (episode / review_rel).write_text(json.dumps(review))
            lifecycle.finalize_qa(episode, 'managed-one', 'test-owner', review_rel,
                                  w.fresh_audit(episode, root), True)
            self.assertTrue(media.exists())
            self.assertFalse(any((episode / f['path']).exists() for f in manifest['qa_batch']['frames']))
            # A new run performs a new inspection; never inherits PASS from this fixture.
            second = qa.inspect_managed(episode, 'managed-two', 'test-owner', media, plan,
                                         episode / 'Edit/QA/managed-two')
            self.assertEqual(second['verdict'], 'UNVERIFIED')
            self.assertEqual(second['checks']['frame_sampling'], 'UNVERIFIED')

    @unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg unavailable')
    def test_large_selection_preserves_exact_source_indices(self):
        indices = sorted(set(range(0, 900, 2)) | set(range(0, 900, 3)) | {899})
        result = subprocess.run([
            'ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
            'color=size=16x16:rate=30:duration=30',
            '-vf', qa.selection_expression(indices), '-fps_mode', 'vfr',
            '-f', 'framemd5', '-'], capture_output=True, text=True, check=True)
        actual = [int(line.split(',')[2]) for line in result.stdout.splitlines()
                  if line and not line.startswith('#')]
        self.assertEqual(actual, indices)

    def test_plan_samples_both_sides_of_cut_and_cue(self):
        indices, violations = qa.frame_plan({
            'frame_count': 300, 'fps': '30/1',
            'scenes': [{'id': 'a', 'start': 0, 'end': 150},
                       {'id': 'b', 'start': 150, 'end': 300}],
            'cues': [{'id': 'c', 'start': 30, 'end': 100,
                      'entry_end': 34, 'exit_start': 95}]})
        self.assertFalse(violations)
        self.assertTrue({0, 149, 150, 299, 29, 30, 34, 95, 99, 100} <= set(indices))


if __name__ == '__main__':
    unittest.main()

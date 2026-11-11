import copy
import tempfile
import unittest
import json
import subprocess
from unittest.mock import patch
from pathlib import Path
from inspect_video import frame_plan, inspect, verdict


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.plan = {'frame_count': 300, 'fps': '30/1', 'scenes': [
            {'id': 'S1', 'start': 0, 'end': 150},
            {'id': 'S2', 'start': 150, 'end': 300}]}

    def test_final_exclusive_end_and_cut_neighbors(self):
        frames, failures = frame_plan(self.plan)
        self.assertTrue({0, 149, 150, 299}.issubset(frames))
        self.assertNotIn(300, frames)
        self.assertFalse(failures)

    def test_cross_scene_cue_keeps_phase_and_cut_frames(self):
        self.plan['cues'] = [{'id': 'C', 'start': 140, 'end': 165,
                             'entry_end': 144, 'exit_start': 160}]
        frames, _ = frame_plan(self.plan)
        self.assertTrue({139, 140, 144, 149, 150, 160, 164, 165}.issubset(frames))

    def test_intermediate_extremum_included_and_invalid_not_clamped(self):
        self.plan['extra_frames'] = [37]
        self.assertIn(37, frame_plan(self.plan)[0])
        for value in (-1, 300, 1.5, True):
            self.plan['extra_frames'] = [value]
            with self.assertRaises(ValueError):
                frame_plan(self.plan)

    def test_missing_scene_and_bad_hold_refused(self):
        broken = copy.deepcopy(self.plan)
        broken['scenes'][1]['start'] = 151
        with self.assertRaises(ValueError):
            frame_plan(broken)
        self.plan['cues'] = [{'id': 'C', 'start': 5, 'end': 20,
                             'entry_end': 19, 'exit_start': 10}]
        with self.assertRaises(ValueError):
            frame_plan(self.plan)

    def test_profile_pacing_is_not_hardcoded(self):
        self.plan['scenes'] = [{'id': 'S', 'start': 0, 'end': 300}]
        self.assertFalse(frame_plan(self.plan)[1])
        self.plan['scene_seconds'] = [4, 6]
        self.assertEqual(len(frame_plan(self.plan)[1]), 1)

    def test_stale_export_cannot_pass_despite_technical_success(self):
        self.assertEqual(verdict([], [], 'STALE'), 'FAIL')
        self.assertEqual(verdict([], [], 'CURRENT'), 'UNVERIFIED')
        self.assertEqual(verdict(['decode error'], [], 'CURRENT'), 'FAIL')

    def test_wrong_file_hash_stops_before_external_processing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            media = root / 'wrong.mp4'
            media.write_bytes(b'not the selected media')
            self.plan['sha256'] = '0' * 64
            result = inspect(media, self.plan, root / 'qa')
            self.assertEqual(result['technical_status'], 'FAIL')
            self.assertNotIn('frame_map', result)
            self.assertFalse((root / 'qa/ffprobe.stdout').exists())

    def test_existing_evidence_directory_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            marker = root / 'keep.txt'
            marker.write_text('old evidence')
            with self.assertRaises(FileExistsError):
                inspect(root / 'missing.mp4', self.plan, root)
            self.assertEqual(marker.read_text(), 'old evidence')

    def test_decode_failure_is_not_hidden_by_valid_metadata(self):
        probe = {'streams': [{'codec_type': 'video', 'avg_frame_rate': '30/1'}]}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            media = root / 'test.mp4'
            media.write_bytes(b'read-only fixture')
            responses = [subprocess.CompletedProcess([], 0, json.dumps(probe), ''),
                         subprocess.CompletedProcess([], 1, '', 'decode error')]
            with patch('inspect_video.run', side_effect=responses):
                result = inspect(media, self.plan, root / 'qa')
            self.assertEqual(result['checks']['full_decode'], 'FAIL')
            self.assertEqual(result['verdict'], 'FAIL')
            self.assertNotIn('frame_map', result)

    def test_unsupported_expected_check_is_not_silently_ignored(self):
        self.plan['expected'] = {'video': {'framez': 300}}
        with self.assertRaises(ValueError):
            frame_plan(self.plan)

    def test_frame_samples_can_be_separated_from_permanent_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            media = root / 'test.mp4'; media.write_bytes(b'fixture')
            evidence = root / 'Edit/QA/run01'
            frames = root / 'Work/run01/previews/qa'
            count = len(frame_plan(self.plan)[0])
            def fake_run(command, output, name):
                if name == 'ffprobe':
                    return subprocess.CompletedProcess([], 0, json.dumps({'streams':[{'codec_type':'video','avg_frame_rate':'30/1'}]}), '')
                if name == 'extract':
                    for i in range(count): (frames / f'{i:06d}.png').write_bytes(b'synthetic frame')
                return subprocess.CompletedProcess([], 0, 'frame=300\n', '')
            with patch('inspect_video.run', side_effect=fake_run):
                report = inspect(media, self.plan, evidence, frames_output=frames)
            self.assertEqual(report['checks']['frame_extraction'], 'PASS')
            self.assertFalse((evidence / 'frames').exists())
            self.assertTrue((evidence / 'report.json').exists())
            self.assertEqual(len(report['frame_map']), count)
            for row in report['frame_map']:
                self.assertTrue((evidence / row['path']).resolve().is_relative_to(frames))


if __name__ == '__main__':
    unittest.main()

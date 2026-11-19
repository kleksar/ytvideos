import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('srt_tool', Path(__file__).with_name('srt_tool.py'))
srt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srt)


class SrtTests(unittest.TestCase):
    def test_resolve_sync_anchor_smoke_check(self):
        for deltas, result in [
            ((-1, 1, 0), 'WITHIN_ONE_FRAME'),
            ((8, 7, 8), 'OFFSET_CANDIDATE'),
            ((-5, -5, -6), 'OFFSET_CANDIDATE'),
            ((0, 3, 8), 'NON_UNIFORM'),
            ((0, 0, -7, -7), 'NON_UNIFORM'),
        ]:
            with self.subTest(deltas=deltas):
                anchors = [{'label': str(i), 'voice_frame': i * 100 + 10,
                            'caption_frame': i * 100 + 10 + delta}
                           for i, delta in enumerate(deltas)]
                with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()) as stdout:
                    source = Path(temp) / 'anchors.json'
                    source.write_text(json.dumps(anchors))
                    self.assertEqual(srt.main(['check-sync', '--anchors', str(source)]),
                                     int(result != 'WITHIN_ONE_FRAME'))
                report = json.loads(stdout.getvalue())
                self.assertEqual(report['result'], result)
                self.assertEqual(report['playback'], 'UNVERIFIED')
                self.assertEqual(report['coverage'], 'SUPPLIED_ANCHORS_ONLY')
                self.assertEqual([anchor['delta_frames'] for anchor in report['anchors']], list(deltas))

    def test_resolve_sync_rejects_missing_duplicate_and_noninteger_anchor_frames(self):
        good = {'label': 'word onset', 'voice_frame': 10, 'caption_frame': 10}
        for anchors in [
            [good, good],
            [good, good, dict(good, voice_frame=20)],
            [good, dict(good, voice_frame=20.0), dict(good, voice_frame=30)],
        ]:
            with self.subTest(anchors=anchors), self.assertRaises(srt.SrtError):
                srt.compare_sync_anchors(anchors)

    def test_unicode_punctuation_and_round_trip(self):
        cues = [{'start_seconds': '59.9995', 'end_seconds': 62, 'text': 'Café —\nreally?'}]
        content, report = srt.check(cues, 'Cafe\u0301 — really?\n', 63)
        self.assertIn('00:01:00,000 --> 00:01:02,000', content)
        self.assertEqual(report['text_coverage'], 'PASS')
        self.assertEqual(srt.parse_srt(content)[0]['text'], 'Café —\nreally?')
        self.assertEqual(report['playback'], 'UNVERIFIED')
        self.assertEqual(report['timing_mapping'], 'UNVERIFIED')

    def test_missing_duplicate_reordered_and_punctuation_fail(self):
        for text in ['Hello', 'Hello Hello world.', 'world. Hello', 'Hello world']:
            with self.subTest(text=text):
                _, r = srt.check([{'start_seconds': 0, 'end_seconds': 1, 'text': text}], 'Hello world.', 2)
                self.assertEqual(r['text_coverage'], 'FAIL')

    def test_portable_language_and_long_hour_counter(self):
        cues = [{'start_seconds': 360000, 'end_seconds': 360002, 'text': '你好。 Привет!'}]
        content, r = srt.check(cues, '你好。 Привет!', 360003)
        self.assertIn('100:00:00,000', content)
        self.assertEqual(r['text_coverage'], 'PASS')
        self.assertEqual(srt.parse_srt(content)[0]['text'], cues[0]['text'])

    def test_rounding_collapse_and_raw_overlap_fail(self):
        for cues in [
            [{'start_seconds': 0.0001, 'end_seconds': 0.0004, 'text': 'a'}],
            [{'start_seconds': 0, 'end_seconds': 1.0004, 'text': 'a'},
             {'start_seconds': 1.0003, 'end_seconds': 2, 'text': 'b'}],
        ]:
            _, r = srt.check(cues, ' '.join(c['text'] for c in cues), 3)
            self.assertEqual(r['structure'], 'FAIL')

    def test_no_clamp_of_out_of_bounds(self):
        _, r = srt.check([{'start_seconds': 47, 'end_seconds': 48.08, 'text': 'older.'}], 'older.', 48)
        self.assertEqual(r['structure'], 'FAIL')

    def test_nonfinite_bool_negative_rejected(self):
        for value in [float('nan'), float('inf'), True, -1]:
            with self.subTest(value=value), self.assertRaises(srt.SrtError):
                srt.check([{'start_seconds': value, 'end_seconds': 1, 'text': 'a'}], 'a', 2)

    def test_malformed_block_not_silently_skipped(self):
        valid = '1\n00:00:00,000 --> 00:00:01,000\na\n'
        for tail in ['\n2\nmalformed\nb', '\n3\n00:00:01,000 --> 00:00:02,000\nb']:
            with self.assertRaises(srt.SrtError):
                srt.parse_srt(valid + tail)
        with self.assertRaises(srt.SrtError):
            srt.parse_srt('1\n00:60:00,000 --> 00:61:00,000\na')

    def test_configurable_readability_warns_without_rewriting(self):
        cue = {'start_seconds': 0, 'end_seconds': 0.5, 'text': 'Long line\nsecond'}
        content, r = srt.check([cue], 'Long line second', 1,
                               {'max_cps': 10, 'max_lines': 1, 'max_line_chars': 5})
        self.assertEqual(r['structure'], 'PASS')
        self.assertEqual(r['readability'], 'WARN')
        self.assertIn('Long line\nsecond', content)

    def test_cli_build_validate_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            p = Path(folder)
            (p/'text.txt').write_text('Hi.', encoding='utf-8')
            (p/'cues.json').write_text(json.dumps({'cues': [{'start_seconds': 0, 'end_seconds': 1, 'text': 'Hi.'}]}))
            args = ['build', '--cues', str(p/'cues.json'), '--text', str(p/'text.txt'), '--duration', '2', '--output', str(p/'out.srt')]
            self.assertEqual(srt.main(args), 0)
            before = (p/'out.srt').read_bytes()
            self.assertEqual(srt.main(args), 1)
            self.assertEqual((p/'out.srt').read_bytes(), before)
            self.assertEqual(srt.main(['validate', '--srt', str(p/'out.srt'), '--text', str(p/'text.txt'), '--duration', '2']), 0)

    def test_invalid_build_writes_report_but_no_srt(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            p = Path(folder)
            (p/'text.txt').write_text('Hi.')
            (p/'cues.json').write_text(json.dumps({'cues': [{'start_seconds': 0, 'end_seconds': 3, 'text': 'Hi.'}]}))
            code = srt.main(['build', '--cues', str(p/'cues.json'), '--text', str(p/'text.txt'), '--duration', '2', '--output', str(p/'out.srt'), '--report', str(p/'report.json')])
            self.assertEqual(code, 1)
            self.assertFalse((p/'out.srt').exists())
            self.assertEqual(json.loads((p/'report.json').read_text())['result'], 'FAIL')


if __name__ == '__main__':
    unittest.main()

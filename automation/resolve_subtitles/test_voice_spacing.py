"""Focused tests for sample-provenance and native-frame voice spacing."""
import hashlib
import json
import math
import tempfile
import unittest
import wave
from fractions import Fraction
from pathlib import Path
from struct import pack

from automation.resolve_subtitles import voice_spacing as voice


class VoiceSpacingTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.hz = 8000

    def wav(self, name, values, channels=1):
        p = self.root / (name + ".wav")
        with wave.open(str(p), "wb") as out:
            out.setparams((channels, 2, self.hz, 0, "NONE", "not compressed"))
            out.writeframes(pack("<" + "h" * len(values), *values))
        return p

    def phrase(self, name):
        # Quiet leading and trailing phonemes should be protected; interior gap is untouched.
        return self.wav(name, [0] * 1600 + [14, -14] * 40 + [800, -800] * 400
                        + [0] * 400 + [1200, -1200] * 400 + [16, -16] * 40 + [0] * 1600)

    def test_protects_quiet_edges_and_source_samples(self):
        p = self.phrase("one")
        old = p.read_bytes()
        a = voice.analyze_wav(p, guard_ms=40)
        self.assertEqual((a["speech_start"], a["speech_end"]), (1680, 3680))
        self.assertEqual((a["trim_start"], a["trim_end"]), (1280, 4080))
        self.assertEqual(a["source_sha256"], hashlib.sha256(old).hexdigest())
        plan = voice.plan_spacing([{"cue": "ONE", "wav": p, "speed": 85}])
        voice.materialize(plan, self.root / "trim")
        row = plan["rows"][0]
        with wave.open(str(p)) as original, wave.open(row["derived_wav"]) as derived:
            original.setpos(a["trim_start"])
            n = a["trim_end"] - a["trim_start"]
            expected = original.readframes(n)
            self.assertEqual(derived.getnframes(), n)
            self.assertEqual(derived.readframes(n), expected)
        self.assertEqual(row["derived_pcm_sha256"], hashlib.sha256(expected).hexdigest())
        self.assertEqual(p.read_bytes(), old)

    def test_uniforming_uses_measured_edges_and_constant_rates(self):
        p = self.phrase("one")
        speeds = (85, 80, 100)
        plan = voice.plan_spacing([{"cue": f"c{i}", "wav": p, "speed": speed}
                                   for i, speed in enumerate(speeds)], fps="30000/1001")
        self.assertEqual(plan["fps"], "30000/1001")
        for i, row in enumerate(plan["rows"]):
            self.assertEqual(row["speed"], str(speeds[i]))
            self.assertGreater(Fraction(row["speech_end_frame"]), Fraction(row["speech_start_frame"]))
            if i:
                error = Fraction(row["gap_from_previous_frames"]) - Fraction(plan["target_gap_frames"])
                self.assertLessEqual(abs(error), Fraction(1, 2))
                self.assertGreaterEqual(row["audio_start_frame"],
                                        Fraction(plan["rows"][i - 1]["audio_end_frame"]))
        self.assertEqual(plan["duration_frames"], math.ceil(Fraction(plan["rows"][-1]["audio_end_frame"])))

    def test_rejects_silent_impulse_stereo_and_bad_input(self):
        for p in (self.wav("silence", [0] * 800), self.wav("impulse", [0] * 800 + [32000] + [0] * 800),
                  self.wav("stereo", [50] * 800, 2)):
            with self.subTest(file=p), self.assertRaises(ValueError):
                voice.analyze_wav(p)
        p = self.phrase("one")
        for changes in ({"wav_sha": "bad"}, {"speed": 0}, {"cue": "../unsafe"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                voice.plan_spacing([{**{"cue": "ok", "wav": p, "speed": 85}, **changes}])
        rows = [{"cue": c, "wav": p, "speed": 85} for c in ("one", "two")]
        with self.assertRaises(ValueError):
            voice.plan_spacing(rows, gap_ms=0)

    def test_tampered_interval_and_stale_source_cannot_materialize(self):
        p = self.phrase("one")
        plan = voice.plan_spacing([{"cue": "a", "wav": p, "speed": 85}])
        plan["rows"][0]["trim_start"] += 1
        out = self.root / "uncreated"
        with self.assertRaises(ValueError):
            voice.materialize(plan, out)
        self.assertFalse(out.exists())
        plan = voice.plan_spacing([{"cue": "a", "wav": p, "speed": 85}])
        p.write_bytes(p.read_bytes() + b"changed")
        with self.assertRaises(ValueError):
            voice.materialize(plan, out)
        self.assertFalse(out.exists())

    def test_cli_plan_only_and_explicit_new_destination(self):
        p = self.phrase("one")
        cue = self.root / "cues.json"
        cue.write_text(json.dumps({"items": [{"cue": "ONE", "wav": p.name, "speed": 85}]}))
        plan = self.root / "plan.json"
        voice.main([str(cue), "--output", str(plan)])
        self.assertNotIn("derived_wav", json.loads(plan.read_text())["rows"][0])
        out = self.root / "trim"
        plan2 = self.root / "plan2.json"
        voice.main([str(cue), "--output", str(plan2), "--materialize-dir", str(out)])
        self.assertTrue((out / "ONE.wav").is_file())
        with self.assertRaises(SystemExit):
            voice.main([str(cue), "--output", str(plan2), "--materialize-dir", str(out)])

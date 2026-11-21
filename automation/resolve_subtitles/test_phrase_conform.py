import copy
import hashlib
import json
import tempfile
import unittest
import wave
from pathlib import Path

from phrase_conform import main, plan, sha256


class PhraseConformTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        with wave.open(str(self.base / "conformed.wav"), "wb") as wav:
            wav.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
            wav.writeframes(bytes(32000))
        self.text = "“Keep clear.”\n\nAll good."
        (self.base / "approved.txt").write_text(self.text + "\n", encoding="utf-8")
        self.audio_sha = sha256(self.base / "conformed.wav")
        self.alignment = dict(status="REVIEW_REQUIRED", audio_sha256=self.audio_sha,
                              transcript_sha256=hashlib.sha256(self.text.encode()).hexdigest(),
                              words=[dict(text=t, start=a, end=b) for t, a, b in [
                                  ("Keep", "0.15", "0.27"), ("clear.", "0.27", "0.5"),
                                  ("All", "0.95", "1.05"), ("good.", "1.05", "1.6")]])
        self.write_alignment()
        self.req = dict(schema=1, fps=30, origin_frame=100, end_frame=165, audio_start_frame=103,
                        audio=dict(path="conformed.wav", sha256=self.audio_sha),
                        transcript_path="approved.txt", alignment_path="words.json", phrases=[])
        for index, text in enumerate(("“Keep clear.”", "All good."), 1):
            name = f"still-{index}.png"
            (self.base / name).write_bytes(bytes([index]))
            self.req["phrases"].append(dict(id=f"S{index}", text=text, asset_path=name,
                                            asset_sha256=sha256(self.base / name)))

    def write_alignment(self):
        (self.base / "words.json").write_text(json.dumps(self.alignment), encoding="utf-8")

    def test_frame_math_shared_start_and_silent_lead_and_tail(self):
        out = plan(self.req, self.base)
        self.assertEqual(out["status"], "OFFLINE_REVIEW_REQUIRED")
        self.assertEqual([(s["start"], s["end"]) for s in out["shots"]], [(100, 132), (132, 165)])
        self.assertEqual([(t["start"], t["end"]) for t in out["titles"]], [(108, 118), (132, 151)])
        self.assertEqual(out["titles"][0]["text"], "“Keep clear.”")
        self.assertEqual(out["initial_picture_lead_frames"], 8)
        self.assertEqual(out["audio"]["sha256"], self.audio_sha)

    def test_missing_still_only_allowed_in_explicit_timing_only(self):
        del self.req["phrases"][0]["asset_path"]
        del self.req["phrases"][0]["asset_sha256"]
        with self.assertRaisesRegex(ValueError, "approved still missing"):
            plan(self.req, self.base)
        out = plan(self.req, self.base, timing_only=True)
        self.assertEqual(out["status"], "TIMING_ONLY")
        self.assertEqual(out["missing_art"], ["S1"])
        self.assertNotIn("asset_path", out["shots"][0])

    def test_stale_audio_even_if_altered_wav_is_present(self):
        self.alignment["audio_sha256"] = "0" * 64
        self.write_alignment()
        with self.assertRaisesRegex(ValueError, "bound to this final WAV"):
            plan(self.req, self.base)

    def test_incomplete_approval_and_bad_hash_always_fail(self):
        self.req["phrases"][0]["asset_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            plan(self.req, self.base, timing_only=True)

    def test_exact_phrase_accounting(self):
        omit = copy.deepcopy(self.req)
        omit["phrases"].pop()
        with self.assertRaisesRegex(ValueError, "trailing"):
            plan(omit, self.base)
        self.req["phrases"].reverse()
        with self.assertRaisesRegex(ValueError, "transcript span"):
            plan(self.req, self.base)


    def test_explicit_title_subcues_do_not_change_picture_cut_or_word_math(self):
        self.req["phrases"][0]["titles"] = [
            {"id": "T1", "text": "“Keep"}, {"id": "T2", "text": "clear.”"}]
        out = plan(self.req, self.base)
        self.assertEqual([(t["id"], t["start"], t["end"]) for t in out["titles"]],
                         [("T1", 108, 111), ("T2", 111, 118), ("S2", 132, 151)])
        self.assertEqual(out["titles"][2]["words"][0], dict(text="All", start=132, end=135))
        self.assertEqual(out["shots"][0]["end"], 132)
        self.req["phrases"][0]["titles"].pop()
        with self.assertRaisesRegex(ValueError, "titles omit"):
            plan(self.req, self.base)

    def test_out_of_order_and_empty_map_rejected(self):
        self.alignment["words"][1]["start"] = "0.1"
        self.write_alignment()
        with self.assertRaisesRegex(ValueError, "invalid source timing"):
            plan(self.req, self.base)
        self.alignment["words"] = []
        self.write_alignment()
        with self.assertRaisesRegex(ValueError, "word count"):
            plan(self.req, self.base)

    def test_explicit_fractional_timebase(self):
        self.req["fps"] = "30000/1001"
        out = plan(self.req, self.base)
        self.assertEqual(out["fps"], "30000/1001")
        self.req["fps"] = "29.97"
        with self.assertRaisesRegex(ValueError, "fps requires"):
            plan(self.req, self.base)

    def test_cli_preserves_existing_output(self):
        request = self.base / "request.json"
        request.write_text(json.dumps(self.req), encoding="utf-8")
        output = self.base / "plan.json"
        self.assertEqual(main([str(request), "--output", str(output)]), 0)
        first = output.read_bytes()
        self.assertEqual(main([str(request), "--output", str(output)]), 2)
        self.assertEqual(output.read_bytes(), first)


if __name__ == "__main__":
    unittest.main()

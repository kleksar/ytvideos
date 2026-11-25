import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("event_map", Path(__file__).parents[1] / "event_map.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fixture():
    return {"schema_version": 1, "clock": {"fps": 60, "sample_rate": 48000, "total_frames": 600},
            "palette": {"white": [242, 237, 237], "red": [239, 64, 76]}, "nodes": [
                {"id": "S", "kind": "phrase", "asset": "voice", "start": 48000,
                 "duration_samples": 48000, "words": [{"text": "Боров!", "start_sample": 800,
                                                        "end_sample": 47201}]},
                {"id": "C", "kind": "caption", "phrase": "S",
                 "start": {"ref": "S", "point": "start", "offset_samples": -2400},
                 "end": {"ref": "S", "point": "end", "offset_samples": 4800},
                 "rows": [{"tokens": [{"text": "БОРОВ!", "colour": "red"}]}]},
                {"id": "fx", "kind": "sfx", "asset": "sfx", "duration_samples": 48000,
                 "attack": {"ref": "S", "point": "speech_end", "quantize": "ceil_frame"},
                 "attack_offset_samples": 8160},
                {"id": "light", "kind": "flash", "start": {"ref": "fx", "point": "attack"},
                 "duration_samples": 50400},
                {"id": "fall", "kind": "event", "start": 240000, "duration_samples": 800}
            ]}


def nodes(result):
    return {n["id"]: n for n in result["nodes"]}


class EventMapTests(unittest.TestCase):
    def test_one_edit_moves_voice_words_caption_attack_and_light(self):
        plan = fixture()
        before = nodes(m.compile_map(plan))
        after = nodes(m.compile_map(m.shift_node(plan, "S", 9600)))
        for ident in ["S", "C", "fx", "light"]:
            for edge in ["start_sample", "end_sample"]:
                self.assertEqual(after[ident][edge] - before[ident][edge], 9600)
        self.assertEqual(after["S"]["resolved_words"][0]["end_sample"], 104801)
        self.assertEqual(after["fx"]["points"]["attack"], 105600)
        self.assertEqual(after["light"]["start_sample"], 105600)
        self.assertEqual(after["fall"], before["fall"])
        self.assertEqual(plan, fixture(), "Authored baseline must stay immutable")

    def test_subframe_shift_preserves_word_samples_and_requantizes_attack(self):
        out = nodes(m.compile_map(m.shift_node(fixture(), "S", 101)))
        self.assertEqual(out["S"]["resolved_words"][0]["end_sample"], 95302)
        self.assertEqual(out["fx"]["points"]["attack"], 96000)
        self.assertEqual(out["fx"]["start_sample"], 87840)

    def test_duration_and_word_end_revision_reanchors_children(self):
        plan = fixture()
        plan["nodes"][0]["duration_samples"] += 4800
        plan["nodes"][0]["words"][0]["end_sample"] += 4800
        out = nodes(m.compile_map(plan))
        self.assertEqual(out["C"]["end_sample"], 105600)
        self.assertEqual(out["light"]["start_sample"], 100800)

    def test_caption_style_does_not_invalidate_audio(self):
        p = fixture()
        original = m.compile_map(p)
        p["nodes"][1]["rows"][0]["tokens"][0]["colour"] = "white"
        changed = m.compile_map(p)
        self.assertEqual(changed["audio_sha256"], original["audio_sha256"])
        self.assertNotEqual(changed["map_sha256"], original["map_sha256"])
        moved = m.compile_map(m.shift_node(p, "S", 800))
        self.assertNotEqual(changed["audio_sha256"], moved["audio_sha256"])

    def test_cycle_orphan_bounds_and_duplicate_are_rejected(self):
        for mutate in [
            lambda p: p["nodes"][0].update(start={"ref": "C", "point": "start"}),
            lambda p: p["nodes"][1]["start"].update(ref="missing"),
            lambda p: p["nodes"][0].update(start=-48000),
            lambda p: p["nodes"].append(copy.deepcopy(p["nodes"][0])),
            lambda p: p["nodes"][2].update(attack_offset_samples=48000),
            lambda p: p["nodes"][1]["start"].update(point="typo"),
        ]:
            with self.subTest(mutate=mutate):
                p = fixture()
                mutate(p)
                with self.assertRaises(m.MapError):
                    m.compile_map(p)

    def test_caption_omission_and_invalid_word_order_rejected(self):
        p = fixture()
        p["nodes"][1]["rows"][0]["tokens"][0]["text"] = "Кто?"
        with self.assertRaises(m.MapError):
            m.compile_map(p)
        p = fixture()
        p["nodes"][0]["words"][0]["end_sample"] = 48001
        with self.assertRaises(m.MapError):
            m.compile_map(p)

    def test_asset_identity_is_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "voice.wav").write_bytes(b"voice fixture")
            p = fixture()
            import hashlib
            digest = hashlib.sha256(b"voice fixture").hexdigest()
            p["assets"] = {a: {"path": "voice.wav", "sha256": digest} for a in ["voice", "sfx"]}
            self.assertEqual(len(m.verify_assets(p, root)), 2)
            (root / "voice.wav").write_bytes(b"other take")
            with self.assertRaises(m.MapError):
                m.verify_assets(p, root)


if __name__ == "__main__":
    unittest.main()

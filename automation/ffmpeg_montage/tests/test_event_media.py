import importlib.util
from pathlib import Path
import tempfile
import unittest

try:
    import numpy as np
    import soundfile as sf
    from PIL import ImageFont
except ImportError:
    np = sf = ImageFont = None


def load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).parents[1] / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipIf(np is None, "media extras not installed")
class MappedMediaTests(unittest.TestCase):
    def test_overlapping_effect_ducks_use_deepest_dip(self):
        graph, media = load("event_map"), load("event_audio")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sf.write(root / "fx.wav", np.zeros(100), 1000, subtype="FLOAT")
            sf.write(root / "music.wav", np.ones(2000) * .01, 1000, subtype="FLOAT")
            sf.write(root / "original.wav", np.zeros(2000), 1000, subtype="FLOAT")
            shape = {"lead_samples": 20, "attack_samples": 10, "hold_samples": 20,
                     "release_samples": 100, "depth_db": -6}
            p = {"schema_version": 1, "clock": {"fps": 10, "sample_rate": 1000, "total_frames": 20},
                 "palette": {}, "assets": {a: {"path": a + ".wav"} for a in ["fx", "music", "original"]},
                 "beds": {a: {"asset": a, "gain_db": 0} for a in ["music", "original"]},
                 "mix": {"peak_cap_dbfs": -1.8}, "nodes": [
                     {"id": ident, "kind": "sfx", "asset": "fx", "attack": at,
                      "duration_samples": 100, "attack_offset_samples": 20,
                      "gain_db": 0, "music_duck": shape}
                     for ident, at in [("A", 500), ("B", 520)]]}
            stems, _, _ = media.render_stems(p, graph.compile_map(p), root)
            self.assertAlmostEqual(stems["music"][515, 0], .01 * 10 ** (-6 / 20), places=8)
            self.assertAlmostEqual(stems["music"][100, 0], .01, places=8)
            self.assertAlmostEqual(stems["music"][900, 0], .01, places=8)

    def test_actual_samples_move_together_and_background_survives(self):
        graph, media = load("event_map"), load("event_audio")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, a in [("v", np.r_[np.ones(100) * .1, np.zeros(100)]),
                            ("fx", np.r_[np.zeros(20), [.2], np.zeros(79)]),
                            ("music", np.ones(3000) * .01),
                            ("original", np.ones(3000) * .005)]:
                sf.write(root / (name + ".wav"), a, 1000, subtype="FLOAT")
            p = {"schema_version": 1, "clock": {"fps": 10, "sample_rate": 1000, "total_frames": 30},
                 "palette": {}, "assets": {a: {"path": a + ".wav"} for a in ["v", "fx", "music", "original"]},
                 "beds": {a: {"asset": a, "gain_db": 0} for a in ["music", "original"]},
                 "mix": {"peak_cap_dbfs": -1.8}, "nodes": [
                     {"id": "S", "kind": "phrase", "start": 500, "duration_samples": 200,
                      "asset": "v", "gain_db": 0, "picture_bound_start_sample": 500,
                      "words": [{"text": "Word", "start_sample": 0, "end_sample": 200}]},
                     {"id": "fx", "kind": "sfx", "attack": {"ref": "S", "point": "speech_end"},
                      "attack_offset_samples": 20, "duration_samples": 100, "asset": "fx", "gain_db": 0},
                     {"id": "flash", "kind": "flash", "start": {"ref": "fx", "point": "attack"},
                      "duration_samples": 100}]}
            before, _, _ = media.render_stems(p, graph.compile_map(p), root)
            shifted = graph.shift_node(p, "S", 200)
            resolved = graph.compile_map(shifted)
            after, mix, receipt = media.render_stems(shifted, resolved, root)
            self.assertEqual(np.flatnonzero(before["voice"][:, 0])[0], 500)
            self.assertEqual(np.flatnonzero(after["voice"][:, 0])[0], 700)
            self.assertEqual(np.argmax(after["sfx"][:, 0]), 900)
            self.assertEqual(next(n for n in resolved["nodes"] if n["id"] == "flash")["start_sample"], 900)
            np.testing.assert_array_equal(before["music"], after["music"])
            np.testing.assert_array_equal(before["original"], after["original"])
            self.assertGreater(float(mix[600, 0]), 0, "Removing speech must retain bed")
            self.assertEqual(receipt["picture_review_required"], ["S"])

    def test_static_colour_stays_red_after_its_word_finishes(self):
        captions = load("semantic_caption")
        font = None
        for candidate in ["DejaVuSans.ttf", "C:/Windows/Fonts/arialbd.ttf",
                          "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
            try:
                font = ImageFont.truetype(candidate, 45).path
                break
            except OSError:
                pass
        if font is None:
            self.skipTest("No fixture font installed")
        style = {"canvas": [600, 200], "max_width": 580, "reveal_lead": .065,
                 "reveal_duration": .27, "reveal_rise": 8, "glow": [[12, .32], [4, .28]],
                 "outline_rgb": [26, 6, 13], "outline_alpha": .88, "shadow_rgb": [20, 0, 7],
                 "float_x": 3, "float_y": 7, "float_degrees": .4, "fade_in": .09, "fade_out": .07}
        card = {"id": "C", "start_seconds": 0, "end_seconds": 4,
                "rows": [{"font_size": 45, "baseline": 110, "tokens": [
                    {"text": "RED", "colour": "red"}, {"text": "WHITE", "colour": "white"}]}]}
        phrase = {"resolved_words": [{"start_sample": 100, "end_sample": 500},
                                      {"start_sample": 1200, "end_sample": 1700}]}
        caption = captions.SemanticCaption(card, phrase,
                    {"white": [242, 237, 237], "red": [239, 64, 76]}, font, 1000, style)
        first = np.asarray(caption.texture(.8)[0])
        later = np.asarray(caption.texture(2.2)[0])
        red = np.all(first[:, :, :3] == [239, 64, 76], axis=2) & (first[:, :, 3] == 255)
        self.assertGreater(int(red.sum()), 50)
        np.testing.assert_array_equal(later[red, :3], first[red, :3])
        self.assertGreater(int(np.all(later[:, :, :3] == [242, 237, 237], axis=2).sum()), 50)


if __name__ == "__main__":
    unittest.main()

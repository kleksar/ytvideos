"""Synthetic geometry/provenance tests; no episode assets, network or audio."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/render_paper_captions.py"
SPEC = importlib.util.spec_from_file_location("paper_caption_renderer", SCRIPT)
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CaptionRendererTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Image.new("RGB", (160, 240), (30, 60, 90)).save(self.root / "scene.png")
        Image.new("RGB", (160, 240), (90, 60, 30)).save(self.root / "scene2.png")
        self.make_cue("short.png", [35])
        self.make_cue("long.png", [130, 95])
        self.manifest = {
            "version": 1, "canvas": [160, 240], "face_height_px": 20,
            "min_face_height_px": 5,
            "anchors": {
                "primary": {"center": [.5, .3], "max_width_px": 140, "max_height_px": 90},
                "alternate": {"center": [.5, .7], "max_width_px": 120, "max_height_px": 90}},
            "scenes": [{"id": "s1", "path": "scene.png"}, {"id": "s2", "path": "scene2.png"}],
            "cues": [self.cue("short", "short.png", ["A"]), self.cue("long", "long.png", ["A LONG PHRASE", "TWO LINES"])],
            "pairs": [{"scene": "s1", "cue": "short", "anchor": "primary"},
                      {"scene": "s1", "cue": "long", "anchor": "alternate"},
                      {"scene": "s2", "cue": "long", "anchor": "primary"}]}

    def make_cue(self, name, widths):
        w, h = max(widths) + 16, len(widths) * 16 + 12
        im = Image.new("RGBA", (w, h))
        draw = ImageDraw.Draw(im)
        for i, width in enumerate(widths):
            x, y = (w - width) // 2, 5 + 16 * i
            draw.rectangle((x - 2, y - 2, x + width + 2, y + 12), fill=(100, 40, 20, 100))
            draw.rectangle((x, y, x + width - 1, y + 9), fill=(238, 200, 155, 255))
        im.save(self.root / name)

    @staticmethod
    def cue(cue_id, path, lines):
        return {"id": cue_id, "lines": lines,
                "backend": {"type": "existingPNG", "path": path, "face": {"mode": "creamOrange"},
                            "reference": path, "status": "synthetic fixture"},
                "provenance": {"author": "test", "purpose": "geometry only"},
                "timing": {"status": "UNVERIFIED", "external_marker": "unchanged"}}

    def run_manifest(self, manifest=None, output="out"):
        path = self.root / "input.json"
        path.write_text(json.dumps(manifest or self.manifest))
        return renderer.run(path, self.root / output)

    def test_shared_fit_multiline_and_assigned_pairs(self):
        report = self.run_manifest()
        self.assertLess(report["shared_face_height_px"], 20)
        heights = [cue["metrics"]["face_height_px"] for cue in report["cues"]]
        self.assertLessEqual(max(heights) - min(heights), 1)
        self.assertEqual(len(report["pairs"]), 3)  # not the 2×2 Cartesian product
        self.assertEqual(len(report["cues"][1]["metrics"]["face_line_boxes"]), 2)
        for cue in report["cues"]:
            self.assertEqual(cue["timing"], self.manifest["cues"][0]["timing"])
            self.assertEqual(cue["backend"]["status"], "synthetic fixture")
            source_height = 10
            self.assertAlmostEqual(cue["uniform_scale"], report["shared_face_height_px"] / source_height)
        for pair in report["pairs"]:
            self.assertEqual(len(pair["comparisons"]), 2)
            selected = next(c for c in pair["comparisons"] if c["anchor"] == pair["anchor"])
            self.assertEqual(selected["checks"]["technical"], "PASS")
            self.assertEqual(selected["checks"]["visual"], "UNVERIFIED")
        self.assertEqual(report["checks"]["sync"], "UNVERIFIED")

    def test_half_open_face_and_complete_alpha_bounds(self):
        im = Image.new("RGBA", (8, 8))
        im.putpixel((3, 4), (240, 200, 150, 255))
        im.putpixel((7, 7), (20, 10, 5, 1))  # faint shadow is still alpha
        mask = Image.new("L", (8, 8))
        mask.putpixel((3, 4), 255)
        metric = renderer.cue_metrics(im, mask, [[3, 4, 4, 5]])
        self.assertEqual(metric["face_bbox"], [3, 4, 4, 5])
        self.assertEqual(metric["face_height_px"], 1)
        self.assertEqual(metric["alpha_bbox"], [3, 4, 8, 8])
        self.assertEqual(metric["alpha_width_px"], 5)

    def test_duplicate_ids_and_pairs_leave_no_output(self):
        for field in ("cues", "scenes", "pairs"):
            with self.subTest(field=field):
                spec = copy.deepcopy(self.manifest)
                spec[field].append(copy.deepcopy(spec[field][0]))
                with self.assertRaisesRegex(ValueError, "Duplicate"):
                    self.run_manifest(spec)
                self.assertFalse((self.root / "out").exists())

    def test_case_colliding_cue_ids_fail_before_output(self):
        spec = copy.deepcopy(self.manifest)
        spec["cues"][1]["id"] = "SHORT"
        for pair in spec["pairs"]:
            if pair["cue"] == "long":
                pair["cue"] = "SHORT"
        with self.assertRaisesRegex(ValueError, "Duplicate cue ID.*case-insensitive"):
            self.run_manifest(spec)
        self.assertFalse((self.root / "out").exists())

    def test_case_colliding_scene_ids_fail_before_output(self):
        spec = copy.deepcopy(self.manifest)
        spec["scenes"][1]["id"] = "S1"
        for pair in spec["pairs"]:
            if pair["scene"] == "s2":
                pair["scene"] = "S1"
        with self.assertRaisesRegex(ValueError, "Duplicate scene ID.*case-insensitive"):
            self.run_manifest(spec)
        self.assertFalse((self.root / "out").exists())

    def test_missing_inputs_and_late_invalid_backend_leave_no_output(self):
        for field in ("path", "reference"):
            spec = copy.deepcopy(self.manifest)
            spec["cues"][1]["backend"][field] = "missing.png"
            with self.assertRaises(FileNotFoundError):
                self.run_manifest(spec)
            self.assertFalse((self.root / "out").exists())
        spec = copy.deepcopy(self.manifest)
        del spec["cues"][1]["backend"]["status"]
        with self.assertRaisesRegex(ValueError, "status"):
            self.run_manifest(spec)
        self.assertFalse((self.root / "out").exists())

    def test_inputs_unchanged_and_existing_output_refused(self):
        before = {p.name: digest(p) for p in self.root.glob("*.png")}
        self.run_manifest()
        self.assertEqual(before, {p.name: digest(p) for p in self.root.glob("*.png")})
        marker = self.root / "out" / "keep.txt"
        marker.write_text("keep")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.run_manifest()
        self.assertEqual(marker.read_text(), "keep")

    def test_deterministic_outputs(self):
        self.run_manifest(output="one")
        self.run_manifest(output="two")
        first = {str(p.relative_to(self.root / "one")): digest(p) for p in (self.root / "one").rglob("*") if p.is_file()}
        second = {str(p.relative_to(self.root / "two")): digest(p) for p in (self.root / "two").rglob("*") if p.is_file()}
        self.assertEqual(first, second)

    def test_ids_cannot_collide_with_mask_or_preview_names(self):
        spec = copy.deepcopy(self.manifest)
        spec["cues"][1]["id"] = "short__FACE"
        for pair in spec["pairs"]:
            if pair["cue"] == "long":
                pair["cue"] = "short__FACE"
        report = self.run_manifest(spec)
        self.assertEqual(report["cues"][1]["id"], "short__FACE")
        paths = [c[key] for c in report["cues"] for key in ("png", "face_mask")]
        self.assertEqual(len(set(paths)), 4)
        self.assertTrue(all((self.root / "out" / path).is_file() for path in paths))

    def test_cli_manifest_to_files(self):
        path = self.root / "cli.json"
        path.write_text(json.dumps(self.manifest))
        process = subprocess.run([sys.executable, str(SCRIPT), str(path), "--output", str(self.root / "cli-out")],
                                 text=True, capture_output=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("Visual/sync/motion UNVERIFIED", process.stdout)
        report = json.loads((self.root / "cli-out" / "manifest.json").read_text())
        self.assertEqual(len(report["pairs"]), 3)

    def test_portrait_and_landscape_previews_preserve_canvas(self):
        for size in ((160, 240), (240, 160)):
            with self.subTest(size=size):
                spec = copy.deepcopy(self.manifest)
                spec["canvas"] = list(size)
                for name in ("scene.png", "scene2.png"):
                    Image.new("RGB", size, (30, 60, 90)).save(self.root / name)
                report = self.run_manifest(spec, output=f"out-{size[0]}")
                for pair in report["pairs"]:
                    for item in pair["comparisons"]:
                        with Image.open(self.root / f"out-{size[0]}" / item["preview"]) as im:
                            self.assertEqual(im.size, size)
                        with Image.open(self.root / f"out-{size[0]}" / item["phone_preview"]) as im:
                            self.assertEqual(im.width / im.height, size[0] / size[1])

    def test_explicit_face_mask_and_authored_line_boxes(self):
        mask = Image.new("L", (51, 28))
        ImageDraw.Draw(mask).rectangle((8, 5, 42, 14), fill=255)
        mask.save(self.root / "mask.png")
        spec = copy.deepcopy(self.manifest)
        spec["cues"][0]["backend"]["face"] = {"mode": "mask", "path": "mask.png", "line_boxes": [[0, 0, 51, 28]]}
        self.run_manifest(spec)

    def test_font_texture_is_explicit_and_does_not_promote_status(self):
        # Explicit synthetic test font; this does not alter production font selection.
        font_path = Path(os.environ.get("YTV_TEST_FONT", "/System/Library/Fonts/Supplemental/Arial.ttf"))
        if not font_path.is_file():
            self.skipTest("Explicit local fixture font unavailable")
        Image.new("RGB", (7, 9), (238, 200, 155)).save(self.root / "texture.png")
        spec = copy.deepcopy(self.manifest)
        spec["cues"][1]["backend"] = {
            "type": "fontTexture", "font": str(font_path), "variation": None,
            "font_px": 40, "line_gap_px": 8, "texture": "texture.png",
            "reference": "short.png", "status": "PROVISIONAL synthetic font test",
            "edge": {"px": 2, "color": [234, 79, 22, 255]},
            "shadow": {"offset_px": [2, 3], "blur_px": 1, "color": [36, 17, 13, 150]}}
        report = self.run_manifest(spec)
        self.assertEqual(report["cues"][1]["backend"]["status"], "PROVISIONAL synthetic font test")
        self.assertEqual(report["checks"]["visual"], "UNVERIFIED")
        del spec["cues"][1]["backend"]["variation"]
        with self.assertRaisesRegex(ValueError, "explicit variation"):
            self.run_manifest(spec, output="invalid")
        self.assertFalse((self.root / "invalid").exists())

    def test_managed_run_separates_imports_from_previews(self):
        episode = self.root.resolve() / 'episode'
        episode.mkdir()
        manifest = self.root / 'managed-input.json'
        manifest.write_text(json.dumps(self.manifest))
        report = renderer.run_managed(manifest, episode, 'captions-v01')
        target = episode / 'Assets/Generated/captions-v01'
        self.assertTrue((target / report['cues'][0]['png']).is_file())
        self.assertFalse((target / 'previews').exists())
        for pair in report['pairs']:
            for comparison in pair['comparisons']:
                actual = (target / comparison['preview']).resolve()
                self.assertTrue(actual.is_relative_to(episode / 'Work/captions-v01/previews'))
                self.assertTrue(actual.is_file())
        state = json.loads((episode / 'Work/captions-v01/manifest.json').read_text())
        self.assertEqual(state['status'], 'complete')
        self.assertEqual({e['role'] for e in state['entries']}, {'dependency', 'preview'})

    def test_unreadable_minimum_rejected_without_individual_squeeze(self):
        self.manifest["min_face_height_px"] = 20
        with self.assertRaisesRegex(ValueError, "cannot fit"):
            self.run_manifest()
        self.assertFalse((self.root / "out").exists())


if __name__ == "__main__":
    unittest.main()

"""Offline regression tests; never connect to Palmier or create production media."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image


AUTOMATION = Path(__file__).resolve().parents[1]


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, AUTOMATION / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load_script("build_paper_project")
assembler = load_script("assemble_paper_layers")


class PaperProjectPreflightTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.images = self.root / "Images"
        self.images.mkdir()
        Image.new("RGB", (9, 16), "white").save(self.images / "master.png")
        for role in ("middle", "foreground"):
            image = Image.new("RGBA", (9, 16), "white")
            image.putpixel((0, 0), (255, 255, 255, 0))
            image.save(self.images / f"{role}.png")
        self.visual_path = self.root / "visual.json"
        self.build_path = self.root / "build.json"

    def scene(self, scene_id="s1", start=0, end=120, *, static=True):
        scene = {"id": scene_id, "start_frame": start, "end_frame": end,
                 "master": "Images/master.png", "foreground_anchor_side": "right"}
        if static:
            scene.update({"motion_direction": "static",
                          "speed_multipliers": {role: 0 for role in assembler.TRACK_ORDER},
                          "static_plate": "Images/master.png",
                          "static_plate_reason": "Accepted complete scene"})
        else:
            scene.update({"motion_direction": "left_to_right",
                          "layers": {"background": "Images/master.png",
                                     "middle": "Images/middle.png",
                                     "foreground": "Images/foreground.png"}})
        return scene

    def write_manifests(self, scenes, auxiliary_tracks=None):
        visual = {"version": 1, "direction_rules_version": 1,
                  "timeline_name": "test_scene_plan", "fps": 30,
                  "canvas": {"width": 1080, "height": 1920}, "scenes": scenes}
        build = {"version": 1, "episode_root": ".", "project_name": "Test project",
                 "visual_manifest": "visual.json", "auxiliary_tracks": auxiliary_tracks or []}
        self.visual_path.write_text(json.dumps(visual), encoding="utf-8")
        self.build_path.write_text(json.dumps(build), encoding="utf-8")

    def run_builder(self, *, tracks=None):
        timeline = {"width": 1080, "height": 1920, "fps": 30,
                    "totalFrames": json.loads(self.visual_path.read_text())["scenes"][-1]["end_frame"],
                    "tracks": tracks or [{"type": "video"}]}
        # All Palmier interfaces, including constructors, are mocks. The real
        # dry-run subprocess exercises validation with temporary PNG fixtures.
        with patch.object(sys, "argv", ["build_paper_project.py", str(self.build_path), "--execute"]), \
                patch.object(builder, "Palmier") as palmier, \
                patch.object(builder, "create_project", return_value="project-test-id") as create, \
                patch.object(builder, "run_visual_assembler", return_value={"timeline_id": "timeline-test-id"}) as assemble, \
                patch.object(builder, "add_auxiliary_tracks") as auxiliary, \
                patch.object(builder, "journal_call", return_value={"snapshotId": "test"}), \
                patch.object(builder, "capture_review_frames", return_value=[]), \
                contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            palmier.return_value.call.return_value = timeline
            result = builder.main()
        return result, palmier, create, assemble, auxiliary

    def test_static_project_accepts_one_picture_track(self):
        self.write_manifests([self.scene()])
        result, _, create, assemble, _ = self.run_builder()
        self.assertEqual(result, 0)
        create.assert_called_once()
        assemble.assert_called_once()
        receipt = json.loads((self.root / "build_paper_project_receipt.json").read_text())
        self.assertEqual(receipt["visual_track_roles"], ["background"])
        self.assertEqual(receipt["status"], "ready_for_review")

    def test_layered_project_still_requires_three_picture_tracks(self):
        self.write_manifests([self.scene(static=False)])
        result, _, _, _, _ = self.run_builder(tracks=[{"type": "video"}] * 3)
        self.assertEqual(result, 0)

    def test_static_project_counts_declared_overlay_and_audio(self):
        # These are placeholder bytes only; no media is decoded or rendered.
        (self.root / "approved-media.bin").write_bytes(b"existing approved media")
        auxiliary_tracks = [
            {"name": name, "type": kind, "media": "approved-media.bin",
             "clips": [{"start_frame": 0, "source_start_seconds": 0, "source_end_seconds": 4}]}
            for name, kind in (("Brand", "video"), ("Voice", "audio"))
        ]
        self.write_manifests([self.scene()], auxiliary_tracks)
        result, _, _, _, auxiliary = self.run_builder(
            tracks=[{"type": "video"}, {"type": "video"}, {"type": "audio"}])
        self.assertEqual(result, 0)
        auxiliary.assert_called_once()

    def test_missing_image_fails_before_any_palmier_access_or_receipt(self):
        self.write_manifests([self.scene()])
        (self.images / "master.png").unlink()
        result, palmier, create, assemble, _ = self.run_builder()
        self.assertEqual(result, 1)
        palmier.assert_not_called()
        create.assert_not_called()
        assemble.assert_not_called()
        self.assertFalse((self.root / "build_paper_project_receipt.json").exists())

    def test_invalid_scene_continuity_fails_before_project_creation(self):
        self.write_manifests([self.scene("first", 0, 120), self.scene("second", 121, 240)])
        result, palmier, create, _, _ = self.run_builder()
        self.assertEqual(result, 1)
        palmier.assert_not_called()
        create.assert_not_called()

    def test_excessive_legacy_motion_fails_before_project_creation(self):
        self.write_manifests([self.scene(end=900, static=False)])
        result, palmier, create, _, _ = self.run_builder()
        self.assertEqual(result, 1)
        palmier.assert_not_called()
        create.assert_not_called()
        with self.assertRaisesRegex(ValueError, "overscan"):
            assembler.validate(self.visual_path, self.root)

    def test_narration_driven_static_durations_not_limited_to_three_to_six_seconds(self):
        self.write_manifests([self.scene("one_frame", 0, 1),
                              self.scene("short", 1, 46), self.scene("long", 46, 496)])
        data, _ = assembler.validate(self.visual_path, self.root)
        self.assertEqual(data["frames"], 496)
        self.assertEqual(data["track_roles"], ["background"])

    def test_non_positive_non_integral_and_non_finite_durations_rejected(self):
        for end in (0, -1, 1.5, float("inf"), float("nan"), True):
            with self.subTest(end=end):
                self.write_manifests([self.scene(end=end)])
                with self.assertRaisesRegex(ValueError, "contiguous"):
                    assembler.validate(self.visual_path, self.root)

    def test_mixed_static_and_legacy_plan_uses_union_of_picture_roles(self):
        self.write_manifests([self.scene("still", 0, 60),
                              self.scene("legacy", 60, 180, static=False)])
        data, _ = assembler.validate(self.visual_path, self.root)
        self.assertEqual(data["track_roles"], ["foreground", "middle", "background"])


if __name__ == "__main__":
    unittest.main()

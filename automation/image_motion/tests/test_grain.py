import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("motion_grain", HERE / "run.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def scene(mode="pan-right"):
    original = {"id": "still", "frames": [0, 120], "mediaType": "image", "mediaRef": "image"}
    keys, _ = m.camera_keys(original, .75, mode, 0)
    return {"source": original, "frames": 120, "fps": 30, "width": 2560, "height": 1440,
            "keyframes": keys, "grain": m.grain_settings({}), "image_hash": "a"*64, "image": "image.png"}


class GrainPlanningTests(unittest.TestCase):
    def test_explicit_clean_path_keeps_original_media_and_camera(self):
        self.assertIsNone(m.grain_settings({"grain": "none"}))
        with tempfile.TemporaryDirectory() as tmp:
            s = scene(); s.pop("grain")
            before = copy.deepcopy(s)
            with patch.object(m, "prepare", return_value="clean.mp4"):
                self.assertEqual(m.prepare_finished(s, {}, Path(tmp), Path(tmp)), "clean.mp4")
            self.assertEqual(s, before)

    def test_all_standard_cameras_bake_once_keep_opacity(self):
        for mode in ("pan-right", "pan-left", "pan-up", "pan-down", "push-in", "pull-out"):
            with self.subTest(mode=mode):
                s = scene(mode)
                s["keyframes"]["opacity"] = [[0, 0], [10, 1]]
                before = copy.deepcopy(s["keyframes"])
                m.finish_plan(s)
                self.assertEqual(s["baked_camera"], {k: before[k] for k in ("position", "scale")})
                self.assertEqual(s["target_keyframes"], {"opacity": before["opacity"]})
                self.assertEqual(s["target_transform"]["width"], 1)
                self.assertEqual(before, s["keyframes"])

    def test_unsupported_camera_fails_before_render_or_mutation(self):
        for change in ("smooth", "edge", "rotation", "crop", "fps"):
            with self.subTest(change=change):
                s = scene()
                if change == "smooth": s["keyframes"]["position"][0][3] = "smooth"
                if change == "edge": s["keyframes"]["position"][0][1] = .1
                if change == "rotation": s["source"]["transform"] = {"rotation": 1}
                if change == "crop": s["source"]["crop"] = {"left": .01}
                if change == "fps": s["fps"] = 25
                with self.assertRaises(ValueError): m.finish_plan(s)

    def test_finished_cache_reuses_clean_depth_and_invalidates_only_changed_finish(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clean = root/"clean.mp4"; clean.write_bytes(b"clean-parallax")
            records = root/"records"; records.mkdir()
            scratch = root/"scratch"
            jobs = []
            def execute(command, log):
                job = json.loads(Path(command[-1]).read_text())
                jobs.append(job)
                Path(job["output"]).write_bytes(b"finished")
                Path(job["receipt"]).write_text("{}")
            with patch.object(m, "CACHE", root/"Cache"), patch.object(m, "prepare", return_value=str(clean)) as prepare, patch.object(m, "probe"), patch.object(m, "worker_command", return_value=["python", str(HERE/"render.py")]), patch.object(m, "execute", side_effect=execute):
                (root/"Cache").mkdir()
                s = scene(); m.finish_plan(s)
                first = m.prepare_finished(s, {}, records, scratch)
                self.assertEqual(first, m.prepare_finished(s, {}, records, scratch))
                self.assertEqual(len(jobs), 1)
                changed = scene("pan-left"); m.finish_plan(changed)
                self.assertNotEqual(first, m.prepare_finished(changed, {}, records, scratch))
                changed = scene(); changed["grain"]["rho"] = .5; m.finish_plan(changed)
                self.assertNotEqual(first, m.prepare_finished(changed, {}, records, scratch))
                self.assertEqual(len(jobs), 3)
                self.assertEqual(prepare.call_count, 4)
                self.assertTrue(Path(first).is_relative_to(root/"Cache/finished"))
                self.assertTrue(all(Path(j["output"]).is_relative_to(scratch) for j in jobs))
                self.assertEqual(clean.read_bytes(), b"clean-parallax")

    def test_verify_rejects_double_camera_and_unrelated_changes(self):
        s = scene(); m.finish_plan(s); s["mediaRef"] = "finished"
        source = {"tracks": [{"name": "Scenes", "clips": [s["source"]]},
                             {"name": "Captions", "clips": [{"id": "cue", "frames": [10, 60]}]}]}
        result = copy.deepcopy(source)
        actual = result["tracks"][0]["clips"][0]
        actual.update(mediaRef="finished", mediaType="video", trimEndFrame=2,
                      transform=s["target_transform"], keyframes=s["target_keyframes"])
        m.verify(source, result, [s], "Scenes")
        actual.pop("transform")  # Palmier can omit a semantically neutral transform.
        m.verify(source, result, [s], "Scenes")
        actual["transform"] = s["target_transform"]
        actual["keyframes"] = s["keyframes"]
        with self.assertRaises(ValueError): m.verify(source, result, [s], "Scenes")
        actual["keyframes"] = s["target_keyframes"]
        result["tracks"][1]["clips"][0]["frames"][1] += 1
        with self.assertRaises(ValueError): m.verify(source, result, [s], "Scenes")


class GrainNumericsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import numpy
        except ImportError:
            raise unittest.SkipTest("Run with pinned uv runtime for numerical checks")
        spec = importlib.util.spec_from_file_location("grain_finish", HERE/"finish.py")
        cls.f = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.f)

    def test_approved_grain_statistics_mask_and_determinism(self):
        import numpy as np
        p = m.grain_settings({})
        g = self.f.Grain(p, 800, 600, 42)
        twin = self.f.Grain(p, 800, 600, 42)
        clean = np.full((600, 800), 128, np.uint8)
        y = g.apply(clean); self.assertTrue(np.array_equal(y, twin.apply(clean)))
        old = g.state.copy(); g.apply(clean)
        self.assertAlmostEqual(float(np.std(y.astype(float)-clean)), 3, delta=.08)
        self.assertAlmostEqual(float(np.corrcoef(old.ravel(), g.state.ravel())[0, 1]), .35, delta=.015)
        for level in (16, 235):
            clean.fill(level)
            self.assertTrue(np.array_equal(clean, g.apply(clean)))
        self.assertAlmostEqual(self.f.Grain(p, 2160, 3840, 42).sigma, 1.155)
        self.assertAlmostEqual(self.f.Grain(p, 1080, 1920, 42).sigma, .5775)

    def test_camera_refuses_edge_holds_and_easing_at_render_boundary(self):
        s = scene(); m.finish_plan(s)
        keys = s["baked_camera"]
        with self.assertRaises(ValueError):
            self.f.camera_at(keys, 0, 150)  # keys only cover 120 frames
        keys["position"][0][3:] = ["easeInOut"]
        with self.assertRaises(ValueError):
            self.f.camera_at(keys, 0, 120)

    def test_affine_center_movement_and_no_camera_tied_noise(self):
        import numpy as np
        s = scene(); m.finish_plan(s)
        first = self.f.camera_at(s["baked_camera"], 0)
        last = self.f.camera_at(s["baked_camera"], 119)
        self.assertAlmostEqual((last[0]+last[2]/2)-(first[0]+first[2]/2), .045)
        plane = np.zeros((100, 200), np.uint8); plane[40:60, 90:110] = 128
        a = self.f.warp(plane, first); b = self.f.warp(plane, last)
        self.assertAlmostEqual(float(np.where(b > 80)[1].mean()-np.where(a > 80)[1].mean()), 9, delta=1)


if __name__ == "__main__": unittest.main()

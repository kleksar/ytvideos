import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("motion", Path(__file__).resolve().parents[1] / "run.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def clip():
    return {"id": "original", "frames": [0, 150], "mediaRef": "still", "mediaType": "image",
            "keyframes": {"position": [[0, -.01, -.05, "linear"], [149, -.07, -.05]],
                          "scale": [[0, 1.10, 1.10, "linear"], [149, 1.10, 1.10]]}}


class MotionTests(unittest.TestCase):
    def test_current_track_label_and_custom_framing(self):
        self.assertEqual(m.track({"tracks": [{"label": "V1", "clips": []}]}, "V1")["label"], "V1")
        c = {"frames": [0, 150], "transform": {"centerX": .725, "centerY": .48,
                                                   "width": 1.45, "height": 1.45}}
        keys, _ = m.camera_keys(c, .75, "push-in", 0)
        for position, scale in zip(keys["position"], keys["scale"]):
            self.assertAlmostEqual(position[1] + scale[1] / 2, .725)
            self.assertAlmostEqual(position[2] + scale[2] / 2, .48)
            self.assertLessEqual(position[1], 0)
            self.assertGreaterEqual(position[1] + scale[1], 1)

    def test_intermediates_use_owned_work_path_and_cache_stays_stable(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            records = root / 'Edit/ImageMotion/run01'; records.mkdir(parents=True)
            scratch = root / 'Work/image-motion-run01/scratch'
            depth = root / 'accepted-depth.npy'; depth.write_bytes(b'precomputed-depth')
            scene = {'image':'accepted.png', 'image_hash':'image-hash', 'depth_hash':'depth-hash',
                     'depth_input':str(depth), 'frames':90, 'fps':30, 'width':1920, 'height':1080,
                     'sign':1, 'depth_zoom':1.15, 'preset':{'offset':.1,'height':.1,'steady':0,'sticky':0}}
            written = []
            def execute(command, log):
                if command[0] == 'worker':
                    job = json.loads(Path(command[-1]).read_text())
                    path = Path(job['raw'])
                else:
                    path = Path(command[-1])
                path.write_bytes(b'fake-renderer-output'); written.append(path)
            with patch.object(m, 'CACHE', root / 'Shared/Cache'), patch.object(m, 'worker_command', return_value=['worker']), patch.object(m, 'execute', side_effect=execute), patch.object(m, 'probe'):
                video = Path(m.prepare(scene, {}, records, scratch_dir=scratch))
                self.assertTrue(video.is_relative_to(root / 'Shared/Cache/video'))
                self.assertTrue(video.exists())
                self.assertTrue(all(p.is_relative_to(scratch) for p in written))
                self.assertFalse(list(records.glob('*.mp4')))
                self.assertFalse(list(scratch.glob('*.mp4')))

    def test_camera_reduction_preserves_center_midpoint_and_direction(self):
        original = clip()
        keys, dx = m.camera_keys(original, .75, "existing", 0)
        self.assertAlmostEqual(dx, -.045)
        self.assertAlmostEqual(keys["position"][0][1], -.0175)
        self.assertAlmostEqual(keys["position"][1][1], -.0625)
        self.assertEqual(original, clip())

    def test_zoom_does_not_masquerade_as_horizontal_pan(self):
        c = clip()
        c["keyframes"] = {"position": [[0, 0, 0], [149, -.05, -.05]],
                          "scale": [[0, 1, 1], [149, 1.1, 1.1]]}
        keys, dx = m.camera_keys(c, .75, "existing", 0)
        self.assertAlmostEqual(dx, 0)
        self.assertAlmostEqual(keys["scale"][0][1], 1.0125)
        self.assertAlmostEqual(keys["scale"][1][1], 1.0875)

    def test_generated_camera_directions_and_vertical(self):
        c = clip(); c.pop("keyframes")
        for mode, sign in [("pan-left", -1), ("pan-right", 1), ("pan-up", 0), ("pan-down", 0)]:
            keys, dx = m.camera_keys(c, .75, mode, 0)
            self.assertEqual(0 if abs(dx)<1e-9 else (1 if dx>0 else -1), sign)
            self.assertEqual([r[0] for r in keys["position"]], [0, 149])

    def test_complex_paths_refused(self):
        c = clip(); c["keyframes"]["position"].insert(1, [75, 0, 0])
        with self.assertRaises(ValueError):
            m.camera_keys(c, .75, "existing", 0)

    def test_plan_uses_live_duration_and_media_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); (base/"image.png").write_bytes(b"source")
            (base/"sources.json").write_text(json.dumps([{"mediaRef": "still", "image": "image.png", "depth_zoom": 1.15}]))
            c = clip(); c["frames"] = [0, 180]
            state = {"tracks": [{"name": "Scenes", "clips": [c]}], "fps": 30, "width": 1920, "height": 1080}
            plan = m.make_plan({"source_manifest": "sources.json"}, state, base)
            self.assertEqual(plan[0]["frames"], 180)
            self.assertEqual(plan[0]["keyframes"]["position"][-1][0], 149)
            self.assertEqual(plan[0]["sign"], 1)  # foreground left, matching center movement
            state["tracks"][0]["clips"][0]["mediaType"] = "video"
            with self.assertRaises(ValueError):
                m.make_plan({"source_manifest": "sources.json"}, state, base)

    def test_verify_detects_unrelated_changes(self):
        c = clip()
        source = {"name": "before", "totalFrames": 150, "tracks": [
            {"id": "s", "index": 0, "name": "Scenes", "clips": [c]},
            {"id": "t", "index": 1, "name": "Titles", "clips": [{"id": "a", "frames": [10, 30], "opacity": 1}]},
            {"id": "a", "index": 2, "name": "Mix", "clips": [{"id": "b", "frames": [0, 150], "mediaRef": "audio"}]}]}
        final = copy.deepcopy(source)
        final["name"] = "copy"
        final["tracks"][0]["clips"][0].update(id="new", mediaRef="render", mediaType="video", trimEndFrame=2)
        scene = {"source": c, "mediaRef": "render", "keyframes": c["keyframes"]}
        m.verify(source, final, [scene], "Scenes")
        final["tracks"][0]["clips"][0].pop("mediaType")
        m.verify(source, final, [scene], "Scenes")
        final["tracks"][2]["clips"][0]["frames"][1] -= 1
        with self.assertRaises(ValueError):
            m.verify(source, final, [scene], "Scenes")

    def test_fingerprint_ignores_clone_ids_but_not_motion_or_content(self):
        a = {"name": "source", "timelineId": "a", "tracks": [{"id": "a", "name": "Main", "clips": [clip()]}]}
        a["tracks"][0]["trackId"] = "source-track"
        b = copy.deepcopy(a); b["name"] = "copy"; b["timelineId"] = "b"; b["tracks"][0]["id"] = "b"
        b["tracks"][0]["trackId"] = "copy-track"
        b["tracks"][0]["clips"][0]["id"] = "new"
        self.assertEqual(m.fingerprint(a), m.fingerprint(b))
        b["tracks"][0]["clips"][0]["keyframes"]["position"][0][1] += .01
        self.assertNotEqual(m.fingerprint(a), m.fingerprint(b))


if __name__ == "__main__":
    unittest.main()

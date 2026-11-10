import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location("scene_cache", Path(__file__).parents[1] / "scene_cache.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.image = self.root / "source.png"
        self.image.write_bytes(b"unit-test source identity")
        self.scene = {"image": str(self.image), "start_frame": 0, "end_frame": 120,
                      "direction": "left_to_right", "zoom": "in"}
        self.calls = 0
        self.cache = module.SceneCache(self.root / "cache", max_bytes=100, engine_identity={"version": "fixture"})

    def renderer(self, index, scene, work, *args):
        self.calls += 1
        output = work / f"scene_{index:05d}.mp4"
        output.write_bytes(b"fixture-rendered-bytes-" + str(self.calls).encode())
        return output

    def render(self, scene=None):
        work = self.root / f"work-{len(list(self.root.glob('work-*')))}"
        work.mkdir()
        return self.cache.render(self.renderer, 0, scene or self.scene, work, [64, 128], "test-encoder", "2M")

    def test_unchanged_scene_reused_across_render_runs(self):
        first = self.render()
        second = self.render()
        self.assertEqual(self.calls, 1)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertTrue(json.loads((second.parent / "scene_00000.cache.json").read_text())["hit"])

    def test_changed_image_or_movement_invalidates_cache(self):
        self.render()
        self.image.write_bytes(b"revised exact image")
        self.render()
        self.render({**self.scene, "zoom": "out"})
        self.assertEqual(self.calls, 3)

    def test_position_change_with_same_duration_preserves_scene_cache(self):
        self.render()
        self.render({**self.scene, "start_frame": 300, "end_frame": 420})
        self.assertEqual(self.calls, 1)

    def test_corrupted_cache_not_reused(self):
        self.render()
        next((self.root / "cache").glob("*.mp4")).write_bytes(b"corrupt")
        self.render()
        self.assertEqual(self.calls, 2)

    def test_eviction_never_removes_materialized_work(self):
        self.cache.max_bytes = 30
        first = self.render()
        self.render({**self.scene, "zoom": "out"})
        self.assertTrue(first.exists())
        self.assertLessEqual(sum(p.stat().st_size for p in (self.root / "cache").glob("*.mp4")), 30)


if __name__ == "__main__":
    unittest.main()

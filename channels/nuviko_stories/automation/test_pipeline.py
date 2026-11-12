import json
from pathlib import Path
import tempfile
import unittest

import pipeline


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "videos" / "2").mkdir(parents=True)
        (self.root / "videos" / "003").mkdir()
        self.runs = self.root / "automation" / "runs"
        self.runs.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_next_id_uses_existing_directories_and_runs(self):
        run = pipeline.create(self.root, self.runs, "Test")
        self.assertEqual(run["episode"], "004")
        self.assertEqual(run["directory"], "004_test")
        self.assertTrue((self.root / "videos/004_test/Source/Voice").is_dir())
        self.assertEqual(json.loads((self.runs / "004.json").read_text())["episode"], "004")
        self.assertEqual(pipeline.create(self.root, self.runs, "")["episode"], "005")

    def test_ids_include_named_dirs_and_legacy_or_broken_links(self):
        videos = self.root / "videos"
        (videos / "009_history").mkdir()
        (videos / "9").symlink_to("009_history", target_is_directory=True)
        (videos / "012").symlink_to("missing", target_is_directory=True)
        run = pipeline.create(self.root, self.runs, "Новая история / chapter 1")
        self.assertEqual(run["episode"], "013")
        self.assertEqual(run["directory"], "013_новая_история_chapter_1")
        self.assertEqual(pipeline.episode_directory(self.root, "009"), (videos / "009_history").resolve())
        with self.assertRaisesRegex(ValueError, "недоступны"):
            pipeline.episode_directory(self.root, "012")

    def test_episode_resolution_rejects_multiple_different_directories(self):
        (self.root / "videos/003_other").mkdir()
        with self.assertRaisesRegex(ValueError, "несколько разных"):
            pipeline.episode_directory(self.root, "003")

    def test_safe_slug_and_legacy_episode_resolution(self):
        self.assertEqual(pipeline.topic_slug("../../"), "untitled")
        self.assertEqual(pipeline.topic_slug("A" * 100), "a" * 60)
        self.assertEqual(pipeline.episode_directory(self.root, "002"), (self.root / "videos/2").resolve())

    def test_dependencies_failure_retry_and_independent_languages(self):
        run = pipeline.create(self.root, self.runs, "")
        with self.assertRaises(ValueError):
            pipeline.transition(run, "ru", "voice", "start")
        pipeline.transition(run, "ru", "story", "start")
        pipeline.transition(run, "ru", "story", "fail", note="Источник недоступен")
        pipeline.transition(run, "ru", "story", "start")
        source = self.root / "story.txt"
        source.write_text("История", encoding="utf-8")
        pipeline.transition(run, "ru", "story", "complete", path=str(source))
        self.assertEqual(run["languages"]["ru"]["story"]["attempts"], 2)
        self.assertEqual(run["languages"]["en"]["story"]["status"], "pending")
        self.assertEqual(len(run["languages"]["ru"]["story"]["artifact"]["sha256"]), 64)
        pipeline.transition(run, "ru", "voice", "start")
        with self.assertRaises(FileNotFoundError):
            pipeline.transition(run, "ru", "voice", "complete", path=str(self.root / "missing"))
        self.assertEqual(run["languages"]["ru"]["voice"]["status"], "in_progress")

    def test_upload_requires_youtube_url_and_note(self):
        run = pipeline.create(self.root, self.runs, "")
        for stage in pipeline.STAGES[:-1]:
            run["languages"]["ru"][stage]["status"] = "completed"
        pipeline.transition(run, "ru", "upload", "start")
        with self.assertRaises(ValueError):
            pipeline.transition(run, "ru", "upload", "complete", note="Private", url="https://example.com")
        with self.assertRaises(ValueError):
            pipeline.transition(run, "ru", "upload", "complete", url="https://youtu.be/123")
        pipeline.transition(run, "ru", "upload", "complete", note="Private; channel A", url="https://youtu.be/123")
        self.assertEqual(run["languages"]["ru"]["upload"]["status"], "completed")


if __name__ == "__main__":
    unittest.main()

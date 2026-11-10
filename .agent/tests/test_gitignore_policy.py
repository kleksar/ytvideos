"""Regression coverage for local media exclusions without hiding source evidence."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
GIT_ENV = {key: value for key, value in os.environ.items()
           if not key.startswith('GIT_')}


class GitIgnorePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory(prefix="ytvideos-ignore-test-")
        cls.root = Path(cls.workspace.name)
        subprocess.run(["git", "init", "-q", "--template=", str(cls.root)], check=True, env=GIT_ENV)
        shutil.copyfile(ROOT / ".gitignore", cls.root / ".gitignore")

    @classmethod
    def tearDownClass(cls):
        cls.workspace.cleanup()

    def assert_ignored(self, path, expected):
        result = subprocess.run(
            ["git", "-c", "core.excludesFile=/dev/null", "check-ignore",
             "--no-index", "--quiet", "--", path],
            cwd=self.root, capture_output=True, text=True, env=GIT_ENV,
        )
        self.assertIn(result.returncode, (0, 1), result.stderr)
        self.assertEqual(result.returncode == 0, expected, path)

    def test_generated_media_and_intermediates_are_ignored(self):
        paths = [
            "channels/paper_detour/research/example/Work/render/caption_states/00001_0.png",
            ".agent/research/example/production/film/Work/render/caption_states/transparent.png",
            "channels/nuviko_history/videos/001/Work/render/caption_states/00001_0.png",
            "channels/paper_detour/videos/001/Edit/QA/v01/contact-sheet.png",
            "channels/nuviko_history/research/example/Edit/QA/v01/frame.jpg",
            "channels/nuviko_history/research/example/Work/qa-v01/frame.png",
            "channels/nuviko_history/research/harrison-qa-v01/contact.jpg",
            ".agent/research/example/production/film/QA/contact.jpg",
            "channels/paper_detour/videos/001/Packaging/Thumbnails/v01/thumbnail.png",
            "channels/paper_detour/research/example/Packaging/Thumbnails/cover.jpg",
            "channels/paper_detour/videos/001/Assets/Generated/scene.png",
            "channels/paper_detour/research/example/Assets/Generated/depth.npy",
            "channels/paper_detour/videos/001/Work/render/scene_00001.command.json",
            ".agent/research/example/production/Work/render/captions.ffconcat",
            "channels/paper_detour/videos/001/Work/render/scenes.ffconcat",
            "channels/paper_detour/videos/001/Edit/ImageMotion/run/tool_schemas.json",
            ".agent/gitignore-inventory-2026-11-06.csv",
            ".agent/gitignore-review-2026-11-06.md",
        ]
        for path in paths:
            with self.subTest(path=path):
                self.assert_ignored(path, True)

    def test_source_style_references_and_evidence_stay_visible(self):
        paths = [
            "channels/paper_detour/brand/References/example/contact.jpg",
            "channels/nuviko_history/brand/References/hero.png",
            "channels/paper_detour/videos/001/Source/Images/historical-source.png",
            "channels/paper_detour/videos/001/Source/Script/narration.md",
            "channels/paper_detour/videos/001/EPISODE.md",
            "channels/paper_detour/videos/001/CURRENT_CONTEXT.md",
            "channels/paper_detour/videos/001/Work/render/plan.json",
            "channels/paper_detour/videos/001/Work/render/input_manifest.json",
            "channels/paper_detour/videos/001/Work/render/caption_groups.json",
            "channels/paper_detour/videos/001/Work/render/subtitle_contract.json",
            "channels/paper_detour/videos/001/Work/render/subtitle_review.json",
            "channels/paper_detour/videos/001/Work/render/render_provenance/engine/montage.py",
            "channels/paper_detour/videos/001/Work/render/render_provenance/render_command.json",
            "channels/paper_detour/videos/001/Edit/QA/v01/REVIEW.md",
            "channels/paper_detour/videos/001/Edit/QA/v01/report.json",
            "channels/paper_detour/videos/001/Packaging/Thumbnails/v01/manifest.json",
            "channels/paper_detour/videos/001/Assets/Generated/build.py",
            "channels/paper_detour/videos/001/Assets/Generated/image.mp4.g08.json",
            "channels/paper_detour/videos/001/RELEASE.json",
            "channels/paper_detour/videos/001/rights.json",
            ".agent/migration-map.json",
            ".agent/migration-ledger.md",
            "archive/story_text/paper_detour/001/narration.txt",
            ".agents/skills/ytv-youtube-metadata/SKILL.md",
            "automation/tests/fixtures/captions.ffconcat",
            ".agent/tests/test_gitignore_policy.py",
            "channels/paper_detour/Source/captions.ffconcat",
            "channels/paper_detour/automation/tests/fixtures/scenes.ffconcat",
            "channels/paper_detour/docs/tool_schemas.json",
            "channels/paper_detour/videos/001/Work/render/render_provenance/captions.ffconcat",
            "channels/paper_detour/videos/001/Work/render/render_provenance/scene_00001.command.json",
        ]
        for path in paths:
            with self.subTest(path=path):
                self.assert_ignored(path, False)

    def test_existing_media_credentials_and_cache_rules_remain(self):
        for path in [
            "channels/paper_detour/videos/001/review.mp4",
            "channels/paper_detour/videos/001/voice.wav",
            "automation/.venv/lib/example.py",
            "automation/__pycache__/example.pyc",
            "automation/.env",
            "automation/client_secret.json",
        ]:
            with self.subTest(path=path):
                self.assert_ignored(path, True)
        self.assert_ignored("automation/.env.example", False)


if __name__ == "__main__":
    unittest.main()

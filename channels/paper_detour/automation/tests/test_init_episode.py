"""Offline checks for exclusive, discoverable Paper Detour scaffolding."""

from pathlib import Path
import re
import json
import subprocess
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[4]
SCRIPT = PROJECT_ROOT / "channels/paper_detour/automation/init_episode.py"


class InitEpisodeTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.videos = Path(self.workspace.name) / "videos"
        self.videos.mkdir()

    def run_init(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args, "--videos-dir", str(self.videos)],
            capture_output=True, text=True, check=False,
        )

    def test_preview_writes_nothing_and_identifies_remaining_registration(self):
        result = self.run_init("987", "test_story")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.videos.iterdir()), [])
        self.assertIn("UNREGISTERED", result.stdout)
        self.assertIn(str(PROJECT_ROOT / ".agent/CHANNEL_BOOTSTRAP.md"), result.stdout)
        self.assertIn("python3.11 .agent/scripts/install-entrypoints.py", result.stdout)

    def test_create_routes_to_current_rules_without_media_or_registry_mutation(self):
        registry = PROJECT_ROOT / ".agent/episode-registry.json"
        registry_before = registry.read_bytes()
        result = self.run_init("987", "test_story", "--create")
        self.assertEqual(result.returncode, 0, result.stderr)
        episode = self.videos / "987_test_story"
        self.assertTrue((episode / "Source/Script").is_dir())
        self.assertFalse((episode / "Script").exists())
        self.assertTrue((episode / "Deliverables").is_dir())
        self.assertEqual(list((episode / "Deliverables").iterdir()), [])
        self.assertEqual(list((episode / "Source/Voice").iterdir()), [])
        layout = json.loads((episode / 'Edit/MediaLifecycle/layout.json').read_text())
        self.assertEqual(layout['roles']['dependency'], 'Assets/Generated')
        self.assertEqual(list((episode / 'Assets/Generated').iterdir()), [])
        self.assertEqual(list((episode / 'Work').iterdir()), [])
        context = (episode / "CURRENT_CONTEXT.md").read_text()
        self.assertIn("UNREGISTERED", context)
        self.assertIn("Язык продукта: EN", context)
        self.assertIn("Разрешения: UNKNOWN", context)
        self.assertNotIn("archive/legacy_stories/videos/", context)
        router = (episode / "AGENTS.md").read_text()
        for required in ["AGENTS.md", ".agent/CHANNEL_BOOTSTRAP.md",
                         ".agent/episode-registry.md", "channels/paper_detour/AGENTS.md",
                         ".agent/skill-catalog.md"]:
            self.assertIn(str(PROJECT_ROOT / required), router)
        for target in re.findall(r"\]\(([^)]+)\)", router):
            self.assertTrue((episode / target).exists(), target)
        skill_link = episode / ".agents/skills"
        self.assertTrue(skill_link.is_symlink())
        self.assertEqual(skill_link.resolve(), (PROJECT_ROOT / ".agents/skills").resolve())
        self.assertEqual(registry.read_bytes(), registry_before)

    def test_duplicate_id_preserves_existing_episode(self):
        existing = self.videos / "987_original"
        existing.mkdir()
        sentinel = existing / "CURRENT_CONTEXT.md"
        sentinel.write_text("existing user state\n")
        result = self.run_init("987", "different_slug", "--create")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(sentinel.read_text(), "existing user state\n")
        self.assertEqual(list(self.videos.iterdir()), [existing])

    def test_invalid_identity_creates_no_files(self):
        for args in [("000", "test_story"), ("12", "test_story"), ("987", "../escape")]:
            with self.subTest(args=args):
                result = self.run_init(*args, "--create")
                self.assertEqual(result.returncode, 2)
                self.assertEqual(list(self.videos.iterdir()), [])


if __name__ == "__main__":
    unittest.main()

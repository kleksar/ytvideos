"""Configuration diagnostics do not pretend that inactive recipes can produce video."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest

from ytvideos.cli import main
from ytvideos.errors import WorkflowError
from ytvideos.profiles import inspect_profiles, load_profile


ROOT = Path(__file__).resolve().parents[1]


class ProfileReadinessTests(unittest.TestCase):
    def test_all_five_identities_are_visible_without_activating_missing_recipes(self):
        result = inspect_profiles(ROOT / "channels", format="short", project=ROOT)
        rows = {row["channel"]: row for row in result["channels"]}
        self.assertEqual(set(rows), {"paper_detour", "nuviko_history", "nuviko_videos",
                                     "scenes_on_repeat", "two_ways_lab"})
        self.assertTrue(rows["paper_detour"]["configuration_ready"])
        self.assertTrue(rows["two_ways_lab"]["configuration_ready"])
        self.assertFalse(rows["nuviko_videos"]["configuration_ready"])
        self.assertTrue(any("Music-first" in text for text in rows["nuviko_videos"]["blockers"]))
        self.assertEqual(result["live_readiness"], "unverified")
        with self.assertRaisesRegex(WorkflowError, "unconfigured"):
            load_profile(ROOT / "channels", "nuviko_videos")

    def test_short_variants_are_resolved_separately_and_incomplete_long_is_visible(self):
        result = inspect_profiles(ROOT / "channels", channel="scenes_on_repeat", project=ROOT)
        row = result["channels"][0]
        self.assertTrue(row["formats"]["short"]["configuration_ready"])
        self.assertEqual(set(row["formats"]["short"]["variants"]),
                         {"scene", "character_edit", "meme_time_machine"})
        self.assertFalse(row["formats"]["long"]["configuration_ready"])
        self.assertTrue(row["formats"]["long"]["blockers"])

    def test_profile_cli_does_not_create_database_workspace_or_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["--db", str(root / "state.db"), "--workspace", str(root / "work"),
                             "--project-root", str(ROOT), "profiles", "--channel", "two_ways_lab", "--format", "short"])
            self.assertEqual(code, 0)
            self.assertEqual(list(root.iterdir()), [])
            self.assertTrue(json.loads(output.getvalue())["channels"][0]["configuration_ready"])

    def test_absent_profile_is_reported_without_substitution(self):
        result = inspect_profiles(ROOT / "channels", channel="nonexistent_channel", format="short")
        row = result["channels"][0]
        self.assertFalse(row["configuration_ready"])
        self.assertEqual(row["channel"], "nonexistent_channel")
        self.assertIn("profile is missing", row["blockers"][0])


if __name__ == "__main__":
    unittest.main()

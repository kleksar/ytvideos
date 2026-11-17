"""Rebrand the saved channel without inheriting its old production defaults."""
import json
from pathlib import Path
import tempfile

import test_pool_service as fixtures
import unittest

from ytvideos.context import instruction_packet, snapshot_references
from ytvideos.errors import WorkflowError
from ytvideos.production_contract import production_requirements, require_configured
from ytvideos.profiles import load_profile
from ytvideos.service import Production
from ytvideos.store import Store
from ytvideos.util import file_digest


ROOT = Path(__file__).resolve().parents[1]
CHANNEL = "two_ways_lab"
PROFILE = "channels/oddly_drawn/PROFILE.md"
VISUAL = "channels/oddly_drawn/brand/VISUAL_PROFILE.md"
RECIPE = "channels/oddly_drawn/docs/PRODUCTION.md"


class OddlyDrawnContracts(unittest.TestCase):
    def test_new_tasks_receive_whiteboard_rules_without_old_mandatory_mechanics(self):
        profile = load_profile(ROOT / "channels", CHANNEL)
        self.assertEqual(profile["name"], "Oddly Drawn")
        self.assertEqual(profile["youtube_channel_id"], "UCcZWXzkL_K1mD5dr8MZBYrQ")
        self.assertFalse(profile["handle_verified"])
        self.assertIsNone(profile["handle"])
        self.assertFalse(profile["release_policy"]["ab_test"])
        for form in ("short", "long"):
            snapshot = snapshot_references(ROOT, profile, form)
            for route, paths in snapshot["routes"].items():
                with self.subTest(format=form, route=route):
                    self.assertIn(PROFILE, paths)
                    self.assertNotIn("channels/two_ways_lab/AGENTS.md", paths)
                    self.assertNotIn("channels/two_ways_lab/brand/VISUAL_PROFILE.md", paths)
                    self.assertNotIn("channels/two_ways_lab/docs/SCENE_PLANNING.md", paths)
                    self.assertEqual(VISUAL in paths, route in {
                        "storyboard", "scene_image", "thumbnail", "subtitles", "render", "review", "packaging"})
                    self.assertEqual(RECIPE in paths, route in {
                        "storyboard", "scene_image", "thumbnail", "audio", "subtitles", "render", "review", "packaging"})
            for stage in ("research", "script", "storyboard", "thumbnail", "audio", "render"):
                packet = instruction_packet(ROOT, channel=CHANNEL, stage=stage, format=form)
                self.assertEqual(packet["references"], snapshot["routes"][stage])
                saved = next(item for item in packet["reference_documents"] if item["path"] == PROFILE)
                self.assertEqual(saved["sha256"], file_digest(ROOT / PROFILE))
                self.assertIn("Первое лицо участника не обязательно", saved["text"])
                self.assertIn("Детектив не является постоянной ролью", saved["text"])

    def test_editorial_run_is_saved_but_media_requests_fail_before_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = Store(str(root / "state.db"))
            service = Production(store, root / "work", ROOT)
            for form in ("short", "long"):
                run = service.create(CHANNEL, "Synthetic navigation only; no story or production", format=form)
                self.assertEqual([task["id"] for task in service.next(run["id"])["tasks"]], ["research"])
                self.assertFalse(run["approvals"])
                self.assertIn(PROFILE, service.context(run["id"], "script")["references"])
                with self.assertRaisesRegex(WorkflowError, "production requirements unresolved"):
                    service.operation_payload(run["id"], "audio", "tts")
                for stage in ("audio", "render", "review"):
                    with self.subTest(format=form, stage=stage), self.assertRaisesRegex(
                            WorkflowError, "production requirements unresolved"):
                        service._production_ready(run, run["tasks"][stage])
                policy = production_requirements(run["profile"], form)
                self.assertFalse(policy["configured"])
                self.assertIn("video.canvas", policy["unresolved"])
                self.assertIn("video.fps", policy["unresolved"])
                with self.assertRaisesRegex(WorkflowError, "production requirements unresolved"):
                    require_configured(policy)
                saved = store.get(run["id"])
                self.assertEqual(saved["pins"], run["pins"])
                self.assertEqual(saved["budget"]["reserved"], 0)
                self.assertTrue(all(task["attempt"] == 0 for task in saved["tasks"].values()))

    def test_existing_run_keeps_its_historical_profile_and_packet_after_rebrand(self):
        fixture = fixtures.PoolServiceTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        service = fixture.production
        root = service.project
        config = root / "channels/two_ways_lab/channel.json"
        config.parent.mkdir(parents=True)
        historical = ROOT / "automation/ffmpeg_montage/tests/fixtures/two_ways_lab_legacy.json"
        config.write_bytes(historical.read_bytes())
        prior = json.loads(config.read_text())
        for entry in prior["context_references"]:
            target = root / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("Synthetic historical requirement: participant A/B and old hero.\n")
        old = service.create(CHANNEL, "Synthetic existing episode")
        before = service.context(old["id"], "script")
        current = load_profile(ROOT / "channels", CHANNEL)
        config.write_text(json.dumps(current))
        for entry in current["context_references"]:
            target = root / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / entry["path"]).read_bytes())
        after = service.context(old["id"], "script")
        self.assertEqual(before, after)
        self.assertEqual(service.store.get(old["id"])["pins"], old["pins"])
        self.assertEqual(service.store.get(old["id"])["profile"], prior)
        self.assertTrue(service.requirements(old)["configured"])
        new = service.create(CHANNEL, "Synthetic new episode")
        self.assertEqual(new["profile"]["name"], "Oddly Drawn")
        self.assertNotEqual(old["pins"]["profile"], new["pins"]["profile"])
        self.assertNotEqual(old["pins"]["references"], new["pins"]["references"])
        self.assertFalse(service.requirements(new)["configured"])

    def test_the_new_brand_directory_does_not_create_a_second_channel_identity(self):
        self.assertFalse((ROOT / "channels/oddly_drawn/channel.json").exists())
        with self.assertRaisesRegex(WorkflowError, "profile is missing"):
            load_profile(ROOT / "channels", "oddly_drawn")

    def test_blank_board_reference_is_preserved_without_enabling_a_delivery_format(self):
        path = ROOT / "channels/oddly_drawn/brand/blank-board-first-frame.png"
        self.assertEqual(file_digest(path), "8c2dcccdb5cb108e0803eec69ee2166daf2de0997ee7bd82baafc311d2667119")
        from PIL import Image
        with Image.open(path) as board:
            self.assertEqual(board.size, (1672, 941))
        profile = load_profile(ROOT / "channels", CHANNEL)
        self.assertTrue(all(value is None for value in profile["voice"].values()))
        self.assertIsNone(profile["visual_profile"])
        self.assertNotIn("montage", profile)
        self.assertEqual(profile["calendar"], {"mode": "resolve_from_verified_channel_calendar"})
        # Loading the profile and diagnosing it do not perform external mutations.
        self.assertIsNone(profile["production"]["formats"]["long"]["video"]["canvas"])


if __name__ == "__main__":
    unittest.main()

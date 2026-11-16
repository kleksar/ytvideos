"""Deliver the duration policy to authors without changing production admission."""
import json
from pathlib import Path
import shutil
import unittest

import test_pool_service as fixtures
from ytvideos.cli import dispatch, parser
from ytvideos.context import instruction_packet, snapshot_references
from ytvideos.util import file_digest


ROOT = Path(__file__).resolve().parents[1]
EDITORIAL = "docs/standards/editorial.md"
WRITER = ".agents/skills/ytv-write-script/SKILL.md"
POLICY_HEADING = "## Версии на 2, 5 и 10 минут"
QUEUE_HEADING = "## Сюжетные PR и переработка"


class ScriptVariantInstructionTests(unittest.TestCase):
    def test_each_story_channel_receives_the_full_policy_before_research_and_writing(self):
        for channel in ("paper_detour", "nuviko_history"):
            profile_path = ROOT / "channels" / channel / "channel.json"
            before = profile_path.read_bytes()
            for stage in ("research", "script"):
                for form in ("short", "long"):
                    with self.subTest(channel=channel, stage=stage, format=form):
                        packet = instruction_packet(ROOT, channel=channel, stage=stage, format=form)
                        documents = {item["path"]: item for item in packet["reference_documents"]}
                        self.assertEqual(packet["scope"], "instructions_only")
                        self.assertNotIn("run_id", packet)
                        self.assertIn(EDITORIAL, packet["read_next"])
                        self.assertEqual(documents[EDITORIAL]["text"], (ROOT / EDITORIAL).read_text())
                        self.assertEqual(documents[EDITORIAL]["sha256"], file_digest(ROOT / EDITORIAL))
                        self.assertIn(POLICY_HEADING, documents[EDITORIAL]["text"])
                        self.assertEqual(packet["skill"]["text"], (ROOT / WRITER).read_text())
                        self.assertIn(QUEUE_HEADING, packet["skill"]["text"])
            # Reading Long instructions must not enable Long in a Short-only profile.
            self.assertEqual(profile_path.read_bytes(), before)


    def test_two_ways_pinned_route_receives_policy_without_enabling_a_long_profile(self):
        profile_path = ROOT / "channels/two_ways_lab/channel.json"
        before = profile_path.read_bytes()
        profile = json.loads(before)
        snapshot = snapshot_references(ROOT, profile, "short")
        for stage in ("research", "script"):
            self.assertIn(EDITORIAL, snapshot["routes"][stage])
        self.assertIn(POLICY_HEADING, snapshot["documents"][EDITORIAL]["text"])
        self.assertEqual(snapshot["documents"][EDITORIAL]["sha256"], file_digest(ROOT / EDITORIAL))
        self.assertEqual(profile_path.read_bytes(), before)


class ScriptVariantRuntimeBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.PoolServiceTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.production = self.fixture.production
        self.editorial = self.production.project / EDITORIAL
        shutil.copyfile(ROOT / EDITORIAL, self.editorial)
        shutil.copyfile(ROOT / WRITER,
                        self.production.project / "skills/ytv-write-script/SKILL.md")

    def test_start_materializes_actual_duration_rules_without_approving_or_dispatching(self):
        args = parser().parse_args(["start", "--channel", "test_channel", "--intent", "Find a story"])
        result = dispatch(self.production, args)
        reading = result["read_next"][0]
        packet = json.loads(Path(reading["task_file"]).read_text())
        self.assertEqual(packet["task_id"], "research")
        documents = {item["path"]: Path(reading["task_file"]).parent / item["local_path"]
                     for item in packet["reference_manifest"]}
        self.assertEqual(documents[EDITORIAL].read_bytes(), self.editorial.read_bytes())
        self.assertIn(POLICY_HEADING, documents[EDITORIAL].read_text())
        self.assertIn(QUEUE_HEADING, Path(reading["skill_file"]).read_text())
        run = self.fixture.store.get(result["run_id"])
        self.assertFalse(run["approvals"])
        self.assertEqual(run["budget"]["reserved"], 0)
        self.assertTrue(all(task["attempt"] == 0 for task in run["tasks"].values()))
        self.assertEqual(sum(task["stage"] == "script" for task in run["tasks"].values()), 1)

    def test_old_run_keeps_its_documents_when_checkout_policy_changes(self):
        self.editorial.write_text("Historical editorial policy without duration variants.\n")
        old = self.production.create("test_channel", "existing editorial work")
        before = self.production.context(old["id"], "script")
        shutil.copyfile(ROOT / EDITORIAL, self.editorial)
        after = self.production.context(old["id"], "script")
        self.assertEqual(before["reference_documents"], after["reference_documents"])
        self.assertEqual(self.fixture.store.get(old["id"])["pins"], old["pins"])
        new = self.production.create("test_channel", "new editorial work")
        document = new["reference_snapshot"]["documents"][EDITORIAL]
        self.assertIn(POLICY_HEADING, document["text"])
        self.assertNotEqual(old["pins"]["references"], new["pins"]["references"])

    def test_six_supporting_texts_and_comparison_do_not_complete_or_approve_script(self):
        run = self.production.create("test_channel", "compare duration variants")
        initial = self.fixture.store.get(run["id"])
        records = []
        for minutes in (2, 5, 10):
            for language in ("en", "ru"):
                path = self.fixture.root / f"{minutes}-{language}.txt"
                path.write_text(f"Synthetic artifact for {minutes} minutes, language {language}.\n")
                result = self.production.attach(run["id"], path, kind="script_variant",
                                                source=f"test:story:{minutes}:{language}",
                                                expected_sha256=file_digest(path))
                records.append(result)
        review = self.fixture.root / "story-review.md"
        review.write_text("Synthetic comparison; editorial quality and duration are UNVERIFIED.\n")
        self.production.attach(run["id"], review, kind="story_review", source="test:story:comparison")
        after = self.fixture.store.get(run["id"])
        self.assertEqual(len(records), 6)
        self.assertEqual(len(after["artifacts"]), len(initial["artifacts"]) + 7)
        self.assertEqual(after["tasks"], initial["tasks"])
        self.assertEqual(after["approvals"], initial["approvals"])
        self.assertEqual(after["profile"], initial["profile"])
        self.assertEqual(after["format"], initial["format"])
        self.assertEqual(after["budget"], initial["budget"])


if __name__ == "__main__":
    unittest.main()

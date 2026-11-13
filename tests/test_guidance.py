"""A fresh session gets the plan, current requirements and exact accepted inputs."""

import json
from pathlib import Path
import unittest

import test_pool_service as fixtures
from ytvideos.cli import dispatch, parser
from ytvideos.doctor import inspect
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.workflow import REQUIRED_CHECKS


class GuidanceTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.PoolServiceTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.production = self.fixture.production

    def test_create_returns_a_plan_without_granting_approval_or_dispatching_work(self):
        args = parser().parse_args(["create", "--channel", "test_channel", "--intent", "Make the supplied story"])
        result = dispatch(self.production, args)
        plan = result["plan"]
        self.assertEqual(plan["run_id"], result["run_id"])
        self.assertEqual(plan["channel"]["id"], "test_channel")
        self.assertEqual(plan["target"]["ready_after"], "review")
        self.assertFalse(plan["target"]["plan_is_approval"])
        self.assertEqual(plan["accepted"], {"script": False, "mp4": False})
        self.assertTrue(all(task["status"] == "pending" for task in plan["steps"]))
        self.assertEqual({task["stage"] for task in plan["release_steps"]},
                         {"upload", "configure_release", "schedule", "verify_publication"})
        self.assertNotIn("upload", {task["stage"] for task in plan["steps"]})

    def test_start_materializes_the_pinned_first_task_before_any_provider_or_claim(self):
        args = parser().parse_args(["start", "--channel", "test_channel", "--intent", "Find a story",
                                    "--request-id", "entry-request"])
        result = dispatch(self.production, args)
        run = self.fixture.store.get(result["run_id"])
        self.assertEqual(len(result["read_next"]), 1)
        reading = result["read_next"][0]
        packet = json.loads(Path(reading["task_file"]).read_text())
        self.assertEqual(packet["task_id"], "research")
        self.assertEqual(Path(reading["skill_file"]).read_text(), run["skills"]["ytv-write-script"]["text"])
        for item, path in zip(packet["reference_manifest"], reading["requirement_files"]):
            self.assertEqual(Path(path).read_text(), run["reference_snapshot"]["documents"][item["path"]]["text"])
        self.assertFalse(run["approvals"])
        self.assertTrue(all(task["attempt"] == 0 and task["status"] == "pending" for task in run["tasks"].values()))
        self.assertEqual(run["budget"]["reserved"], 0)
        self.assertEqual(result["next"]["tasks"][0]["next_action"]["kind"], "inspect_runtime_tools")
        repeated = dispatch(self.production, args)
        self.assertEqual(repeated["run_id"], result["run_id"])
        self.assertEqual(repeated["read_next"][0]["task_file"], reading["task_file"])
        self.assertEqual(len(self.fixture.store.list()), 1)

    def test_start_does_not_overwrite_a_modified_pinned_reading_packet(self):
        args = parser().parse_args(["start", "--channel", "test_channel", "--intent", "Find a story",
                                    "--request-id", "entry-request"])
        result = dispatch(self.production, args)
        skill = Path(result["read_next"][0]["skill_file"])
        skill.write_text("Untrusted replacement")
        with self.assertRaisesRegex(Conflict, "entry packet differs"):
            dispatch(self.production, args)
        self.assertEqual(skill.read_text(), "Untrusted replacement")

    def test_plan_exposes_missing_listening_before_media_work_and_is_read_only(self):
        run = self.production.create("test_channel", "new story")
        before = self.fixture.store.get(run["id"])
        plan = self.production.plan(run["id"])
        gaps = {gap["capability"]: gap for gap in plan["capability_gaps"]}
        self.assertEqual(set(gaps["audio.listen"]["tasks"]), {"audio", "review"})
        self.assertIn("image.generate", gaps)
        self.assertEqual(before, self.fixture.store.get(run["id"]))
        self.production.capabilities(run["id"], {"audio.listen": True}, evidence="isolated test audio tool")
        after = self.production.plan(run["id"])
        self.assertNotIn("audio.listen", {gap["capability"] for gap in after["capability_gaps"]})

    def test_absent_tool_observation_requires_discovery_instead_of_a_false_blocker(self):
        run = self.production.create("test_channel", "find an interesting story")
        task = self.production.next(run["id"])["tasks"][0]
        self.assertFalse(task["dispatchable"])
        self.assertEqual(task["capability_checks"][0]["state"], "unobserved")
        self.assertEqual(task["next_action"]["kind"], "inspect_runtime_tools")
        self.assertEqual(task["next_action"]["context_command"][-1], "research")
        check = next(item for item in inspect(self.production, run["id"])["checks"]
                     if item["capability"] == "web.search")
        self.assertIsNone(check["available"])
        self.production.capabilities(run["id"], {"web.search": False}, evidence="actual test host discovery has no search")
        task = self.production.next(run["id"])["tasks"][0]
        self.assertEqual(task["capability_checks"][0]["state"], "unavailable")
        self.assertEqual(task["next_action"]["kind"], "resolve_unavailable_capability")
        self.production.capabilities(run["id"], {"web.search": True}, evidence="actual test host exposes search")
        self.assertTrue(self.production.next(run["id"])["tasks"][0]["dispatchable"])

    def test_cli_claim_carries_the_actual_pinned_task_context(self):
        run = self.production.create("test_channel", "research a story")
        self.production.capabilities(run["id"], {"web.search": True}, evidence="isolated source lookup fixture")
        args = parser().parse_args(["claim", "--run", run["id"], "--task", "research", "--worker", "new-session"])
        result = dispatch(self.production, args)
        packet = result["context"]
        self.assertEqual(packet["input_hash"], result["input_hash"])
        self.assertEqual(packet["skill"]["text"], run["skills"]["ytv-write-script"]["text"])
        self.assertEqual(set(packet["task_guide"]["required_checks"]), REQUIRED_CHECKS["research"])
        self.assertEqual(packet["task_guide"]["read"], packet["references"])
        self.assertTrue(packet["reference_documents"])

    def test_subtitles_and_review_can_find_the_accepted_script_without_chat_history(self):
        run_id, _ = self.fixture.make_run(count=1)
        run = self.fixture.store.get(run_id)
        script_id = run["tasks"]["script"]["outputs"][0]
        for stage in ("subtitles", "review"):
            with self.subTest(stage=stage):
                packet = self.production.context(run_id, stage)
                ancestors = {entry["task_id"]: entry["artifacts"] for entry in packet["supporting_inputs"]}
                self.assertEqual(ancestors["script"][0]["id"], script_id)
                self.assertNotIn("packaging", ancestors)
        storyboard = self.production.context(run_id, "storyboard")
        self.assertNotIn("script", {entry["task_id"] for entry in storyboard["supporting_inputs"]})

    def test_render_and_review_receive_audio_and_visual_standards_explicitly(self):
        run = self.production.create("test_channel", "complete production")
        for stage in ("render", "review"):
            with self.subTest(stage=stage):
                packet = self.production.context(run["id"], stage)
                self.assertIn("docs/standards/audio.md", packet["references"])
                self.assertIn("docs/standards/visual.md", packet["references"])

    def test_plan_reports_code_drift_without_rewriting_the_run_or_hiding_the_next_step(self):
        run = self.production.create("test_channel", "resume existing run")
        (self.production.project / "src/ytvideos/pin.py").write_text("# changed runtime\n")
        before = self.fixture.store.get(run["id"])
        plan = self.production.plan(run["id"])
        self.assertFalse(plan["runtime"]["code_matches_pin"])
        self.assertIn("pinned checkout", plan["runtime"]["blocker"])
        self.assertEqual(plan["next"]["tasks"][0]["id"], "research")
        self.assertEqual(before, self.fixture.store.get(run["id"]))

    def test_plan_uses_saved_profile_not_edited_checkout_parameters(self):
        run = self.production.create("test_channel", "saved profile")
        path = self.production.project / "channels/test_channel/channel.json"
        changed = json.loads(path.read_text())
        changed["name"] = "Unaccepted new identity"
        path.write_text(json.dumps(changed))
        plan = self.production.plan(run["id"])
        self.assertEqual(plan["channel"]["name"], "Test channel")
        self.assertEqual(plan["pins"]["profile"], run["pins"]["profile"])

    def test_supplied_script_is_exact_input_in_fresh_context_and_does_not_grant_approval(self):
        source = self.fixture.root / "provided.en.txt"
        source.write_text("A complete supplied narration.\nThis exact text is the input.\n")
        args = parser().parse_args(["create", "--channel", "test_channel", "--intent", "Produce this text",
                                    "--source-script", str(source)])
        result = dispatch(self.production, args)
        run = self.fixture.store.get(result["run_id"])
        source.unlink()
        for stage in ("research", "script", "storyboard"):
            with self.subTest(stage=stage):
                packet = self.production.context(run["id"], stage)
                self.assertEqual(packet["source_script"]["sha256"], run["pins"]["source_script"])
                self.assertEqual(self.production.artifacts.resolve(packet["source_script"]).read_text(),
                                 "A complete supplied narration.\nThis exact text is the input.\n")
        self.assertEqual(run["approvals"], {})
        self.assertIn("присланного", self.production.context(run["id"], "research")["task_guide"]["goal"])
        self.assertEqual(result["plan"]["source_script"]["id"], run["source_script_id"])

    def test_redelivery_cannot_replace_supplied_script_under_the_same_request_id(self):
        source = self.fixture.root / "provided.en.txt"
        source.write_text("The original narration.")
        run = self.production.create("test_channel", "produce it", request_id="request-1", source_script=source)
        again = self.production.create("test_channel", "produce it", request_id="request-1", source_script=source)
        self.assertEqual(again["id"], run["id"])
        source.write_text("Different narration.")
        with self.assertRaises(Conflict):
            self.production.create("test_channel", "produce it", request_id="request-1", source_script=source)
        with self.assertRaises(Conflict):
            self.production.create("test_channel", "produce it", request_id="request-1")

    def test_corrupted_source_reference_is_not_given_to_a_worker(self):
        source = self.fixture.root / "provided.en.txt"
        source.write_text("The actual provided narration.")
        run = self.production.create("test_channel", "produce it", source_script=source)
        self.fixture.store.mutate(run["id"], lambda tx, state: state.pop("source_script_id"))
        with self.assertRaisesRegex(Conflict, "source script"):
            self.production.context(run["id"], "research")

    def test_failed_context_delivery_does_not_consume_a_claim_or_attempt(self):
        source = self.fixture.root / "provided.en.txt"
        source.write_text("The supplied narration.")
        run = self.production.create("test_channel", "produce it", source_script=source)
        self.production.capabilities(run["id"], {"web.search": True}, evidence="test source lookup")
        artifact = run["artifacts"][run["source_script_id"]]
        self.production.artifacts.resolve(artifact).unlink()
        before = self.fixture.store.get(run["id"])
        args = parser().parse_args(["claim", "--run", run["id"], "--task", "research", "--worker", "fresh"])
        with self.assertRaisesRegex(WorkflowError, "artifact"):
            dispatch(self.production, args)
        self.assertEqual(before, self.fixture.store.get(run["id"]))

    def test_review_packet_declares_all_channel_specific_completion_checks(self):
        path = self.production.project / "channels/test_channel/channel.json"
        profile = json.loads(path.read_text())
        policy = json.loads((Path(__file__).resolve().parents[1] / "channels/paper_detour/channel.json").read_text())
        profile["production"] = policy["production"]
        path.write_text(json.dumps(profile))
        run = self.production.create("test_channel", "complete review")
        packet = self.production.context(run["id"], "review")
        self.assertTrue({"motion", "music", "captions", "decorative_frame", "av_loop"}
                        <= set(packet["required_checks"]))
        self.assertEqual(packet["required_checks"], packet["task_guide"]["required_checks"])
        step = next(item for item in self.production.plan(run["id"])["steps"] if item["id"] == "review")
        self.assertEqual(packet["required_checks"], step["required_checks"])

    def test_listening_does_not_need_a_provider_billing_classification(self):
        profile_path = self.production.project / "channels/test_channel/channel.json"
        profile = json.loads(profile_path.read_text())
        policy = json.loads((Path(__file__).resolve().parents[1] / "channels/paper_detour/channel.json").read_text())
        profile["production"] = policy["production"]
        profile_path.write_text(json.dumps(profile))
        run_id, _ = self.fixture.make_run(count=1)
        self.production.capabilities(run_id, {
            "audio.produce": {"available": True, "billing": "included"}, "audio.listen": True,
        }, evidence="test runtime includes synthesis and observed audio inspection")
        claim = self.production.claim(run_id, "audio", "audio-worker")
        self.assertEqual(claim["estimated_units"], 0)


if __name__ == "__main__":
    unittest.main()

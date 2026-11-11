"""Real workflow/pool/storage with fake native generation; SQLite and PostgreSQL."""
import base64
import copy
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import test_pool_service as fixtures
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.runtime.app_server import AppServer, RpcUnavailable
from ytvideos.runtime.image_host import ImageHost
from ytvideos.util import file_digest


class NativeFixture:
    model = "test-luna"
    image_prompt = staticmethod(AppServer.image_prompt)

    def __init__(self):
        self.started = []
        self.history = {}
        self.lose_response = False
        self.disconnect = False

    def start_thread(self, directory):
        thread_id = "thread-" + str(len(self.started))
        self.started.append({"thread": thread_id, "directory": str(directory)})
        self.history[thread_id] = []
        return thread_id

    def start_image(self, thread_id, directory, prompt):
        turn_id = "turn-" + thread_id
        self.history[thread_id] = [{"id": turn_id, "status": "inProgress", "durationMs": 20000,
            "items": [{"type": "userMessage", "content": [{"type": "text", "text": prompt}]}]}]
        if self.lose_response:
            raise RpcUnavailable("simulated lost turn/start response")
        return turn_id

    def turns(self, thread_id):
        if self.disconnect:
            raise RpcUnavailable("simulated disconnected transport")
        return copy.deepcopy(self.history[thread_id])

    def finish(self, thread_id, *, saved_path=None, inline=False):
        turn = self.history[thread_id][0]
        turn["status"] = "completed"
        image = {"type": "imageGeneration", "id": "image-" + thread_id,
                 "status": "completed", "generationId": "synthetic-provider-id"}
        if inline:
            image["result"] = base64.b64encode(fixtures.png_bytes()).decode()
        else:
            directory = next(Path(item["directory"]) for item in self.started if item["thread"] == thread_id)
            path = saved_path or directory / "result.png"
            if not saved_path:
                path.write_bytes(fixtures.png_bytes())
            image["savedPath"] = str(path)
        turn["items"].append(image)


class ImageHostTests(unittest.TestCase):
    postgres = False
    make_run = fixtures.PoolServiceTests.make_run
    qa_complete = fixtures.PoolServiceTests.qa_complete

    def setUp(self):
        fixtures.PoolServiceTests.setUp(self)
        self.server = NativeFixture()
        self.config = {"host_id": "test-host", "runtime_key": "fixture-runtime", "model": "test-luna",
                       "work_root": str(self.root / "native-work"),
                       "channels": ["test_channel", "second", "third"], "estimated_units": 0}
        standards = self.production.project / "docs" / "standards"
        standards.mkdir(parents=True)
        (standards / "visual.md").write_text("Synthetic visual standard, not a real channel style.")
        for channel in self.config["channels"]:
            directory = self.production.project / "channels" / channel
            directory.mkdir(exist_ok=True)
            (directory / "PROFILE.md").write_text("Synthetic channel identity.")
        self.host = ImageHost(self.production, self.server, self.config)

    def run_fixture(self, **kwargs):
        run_id, request = self.make_run(shared_review_capacity=4, **kwargs)
        self.production.revise(run_id, "image:s0", "add exact synthetic reference")
        image = self.production.attach(run_id, self.image, kind="image", source="test-only reference")
        def reference(tx, run):
            for task in run["tasks"].values():
                if task["stage"] == "scene_image":
                    task["payload"]["references"] = [image["id"]]
        self.store.mutate(run_id, reference)
        self.pools.operate(run_id, "enqueue")
        self.pools.operate(run_id, "tick")
        return run_id

    def first_dispatch(self, **kwargs):
        run_id = self.run_fixture(**kwargs)
        result = self.host.tick()
        self.assertEqual(len(result["dispatches"]), 1, result)
        return run_id, self.host._jobs()[0]

    def test_dispatch_has_fresh_session_exact_skill_and_owned_inputs(self):
        run_id, job = self.first_dispatch(count=1)
        packet = json.loads((Path(job["directory"]) / "TASK.json").read_text())
        self.assertIn("Fixture skill", (Path(job["directory"]) / "SKILL.md").read_text())
        self.assertTrue(packet["local_inputs"])
        self.assertEqual(job["state"], "running")
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "running")
        self.assertEqual(len(self.server.started), 1)

    def test_completion_returns_bytes_but_does_not_invent_qa(self):
        run_id, job = self.first_dispatch(count=1)
        self.server.finish(job["thread_id"])
        result = self.host.tick()
        self.assertEqual(result["observations"][0]["status"], "delivered")
        state = self.store.get(run_id)
        self.assertEqual(state["tasks"]["image:s0"]["status"], "running")
        self.assertEqual(state["tasks"]["image:s0"]["outputs"], [])
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 0)
        self.assertEqual(self.pools.operate(run_id, "status")["review"]["used"], 1)

    def test_restart_recovers_lost_turn_response_without_second_send(self):
        run_id = self.run_fixture(count=1)
        self.server.lose_response = True
        self.host.tick()
        job = self.host._jobs()[0]
        self.assertIsNone(job["turn_id"])
        self.assertIsNotNone(job["thread_id"])
        self.server.finish(job["thread_id"], inline=True)
        restarted = ImageHost(self.production, self.server, self.config)
        self.assertEqual(restarted.tick()["observations"][0]["status"], "delivered")
        self.assertEqual(len(self.server.started), 1)
        self.assertFalse(self.store.get(run_id)["tasks"]["image:s0"]["outputs"])

    def test_replayed_observation_survives_worker_file_removal(self):
        _, job = self.first_dispatch(count=1)
        self.server.finish(job["thread_id"])
        with patch.object(self.host.pools, "operate", side_effect=Conflict("lost local acknowledgement")):
            with self.assertRaises(Conflict):
                self.host.poll(job)
        job = self.host._jobs()[0]
        self.assertEqual(job["state"], "observed")
        (Path(job["directory"]) / "result.png").unlink()
        result = ImageHost(self.production, self.server, self.config).poll(job)
        self.assertEqual(result["status"], "delivered")
        self.assertEqual(len(self.server.started), 1)

    def test_same_pool_allows_second_generation_before_first_finishes(self):
        _, _ = self.first_dispatch(capacity=3, count=3)
        self.now += 6
        result = self.host.tick()
        self.assertEqual(len(result["dispatches"]), 1, result)
        self.assertEqual(len(self.server.started), 2)
        self.assertNotEqual(self.server.started[0]["directory"], self.server.started[1]["directory"])

    def test_unknown_and_ambiguous_history_never_resend(self):
        _, job = self.first_dispatch(count=1)
        self.server.history[job["thread_id"]] = []
        for _ in range(2):
            result = self.host.tick()
            self.assertEqual(result["observations"][0]["status"], "unknown")
            self.assertFalse(result["dispatches"])
        self.assertEqual(len(self.server.started), 1)

    def test_turn_with_wrong_prompt_is_not_our_result(self):
        _, job = self.first_dispatch(count=1)
        self.server.finish(job["thread_id"])
        self.server.history[job["thread_id"]][0]["items"][0]["content"][0]["text"] = "Someone else's request"
        self.assertEqual(self.host.poll(job)["status"], "unknown")
        self.assertIsNone(self.host._jobs()[0]["observation"])

    def test_text_claim_and_fileid_only_do_not_count_as_generated_bytes(self):
        _, job = self.first_dispatch(count=1)
        turn = self.server.history[job["thread_id"]][0]
        turn["status"] = "completed"
        turn["items"].append({"type": "agentMessage", "text": "Image ready: result.png"})
        self.assertEqual(self.host.poll(job)["status"], "unknown")
        turn["items"].append({"type": "imageGeneration", "id": "native", "status": "completed", "fileId": "opaque"})
        with self.assertRaisesRegex(WorkflowError, "no local bytes"):
            self.host.poll(job)

    def test_output_path_escape_and_symlink_are_rejected(self):
        _, job = self.first_dispatch(count=1)
        self.server.finish(job["thread_id"], saved_path=self.image)
        with self.assertRaisesRegex(WorkflowError, "owned generated"):
            self.host.poll(job)
        link = Path(job["directory"]) / "link.png"
        link.symlink_to(self.image)
        self.server.history[job["thread_id"]][0]["items"][-1]["savedPath"] = str(link)
        with self.assertRaises(WorkflowError):
            self.host.poll(job)

    def test_changed_pinned_input_rejects_completion(self):
        _, job = self.first_dispatch(count=1)
        self.server.finish(job["thread_id"])
        (Path(job["directory"]) / "SKILL.md").write_text("changed")
        with self.assertRaisesRegex(WorkflowError, "modified a pinned input"):
            self.host.poll(job)

    def test_cancellation_collects_outcome_but_never_accepts_image(self):
        run_id, job = self.first_dispatch(count=1)
        self.production.cancel(run_id, "fixture cancellation")
        self.server.finish(job["thread_id"], inline=True)
        self.host.tick()
        state = self.store.get(run_id)
        self.assertEqual(state["status"], "cancelled")
        self.assertEqual(state["tasks"]["image:s0"]["outputs"], [])
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 0)

    def test_stale_journal_writer_cannot_overwrite_newer_state(self):
        _, job = self.first_dispatch(count=1)
        stale = copy.deepcopy(job)
        job["state"] = "newer"
        self.host._save(job)
        with self.assertRaises(Conflict):
            self.host._save(stale)
        self.assertEqual(self.host._jobs()[0]["state"], "newer")

    def test_transport_outage_does_not_claim_more_work(self):
        _, _ = self.first_dispatch(capacity=3, count=3)
        self.now += 6
        self.server.disconnect = True
        result = self.host.tick()
        self.assertEqual(result["blockers"][0]["error"], "RpcUnavailable")
        self.assertEqual(len(self.server.started), 1)
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)

    def test_worker_root_cannot_overlap_state_or_source(self):
        for root in (self.production.workspace, self.production.project, self.root):
            with self.subTest(root=root), self.assertRaises(WorkflowError):
                ImageHost(self.production, self.server, {**self.config, "work_root": str(root)})

    def test_metered_generation_without_reservation_never_calls_native(self):
        self.run_fixture(count=1, billing="metered")
        self.host.tick()
        self.assertEqual(self.server.started, [])

    def test_missing_registered_reference_stops_before_claim(self):
        run_id = self.run_fixture(count=1)
        # Enqueue a new version whose reference is explicitly unavailable.
        self.production.revise(run_id, "image:s0", "fixture reference update")
        def change(tx, run):
            run["tasks"]["image:s0"]["payload"]["references"] = ["missing-artifact"]
        self.store.mutate(run_id, change)
        self.host.tick()
        self.assertEqual(self.server.started, [])
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "pending")

    def test_duplicate_delivery_does_not_change_image_or_generate_again(self):
        _, job = self.first_dispatch(count=1)
        self.server.finish(job["thread_id"], inline=True)
        self.host.poll(job)
        observation = self.host._jobs()[0]["observation"]
        for _ in range(2):
            self.pools.operate(job["run_id"], "result", observation)
        self.assertEqual(file_digest(observation["artifact_path"]), observation["evidence"]["sha256"])
        self.assertEqual(len(self.server.started), 1)


    def test_shared_capacity_bounds_three_channels(self):
        for channel in ("test_channel", "second", "third"):
            self.run_fixture(capacity=2, count=1, channel=channel)
        self.host.tick()
        self.host.tick()
        self.host.tick()
        self.assertEqual(len(self.server.started), 2)
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 2)
        # One completion frees a physical slot, allowing another channel, but
        # its review credit remains occupied until actual QA.
        self.server.finish(self.server.started[0]["thread"])
        self.host.tick()
        self.assertEqual(len(self.server.started), 3)
        self.assertEqual(len({job["run_id"] for job in self.host._jobs()}), 3)

    def test_missing_shared_review_limit_blocks_dispatch(self):
        self.run_fixture(count=1)
        with self.store.transaction() as tx:
            tx.execute("DELETE FROM runtime_review_limits")
        result = self.host.tick()
        self.assertFalse(result["dispatches"])
        self.assertIn("shared coordinator review", result["blockers"][0]["reason"])
        self.assertEqual(self.server.started, [])

    def test_manual_or_unlisted_channel_is_not_admitted(self):
        self.run_fixture(count=1)
        host = ImageHost(self.production, self.server, {**self.config, "channels": ["manual_only"]})
        self.assertFalse(host.tick()["dispatches"])
        self.assertEqual(self.server.started, [])

    def test_missing_reference_explanation_blocks_before_claim(self):
        run_id = self.run_fixture(count=1)
        self.production.revise(run_id, "image:s0", "remove reference")
        def change(tx, run):
            run["tasks"]["image:s0"]["payload"]["references"] = []
        self.store.mutate(run_id, change)
        result = self.host.tick()
        self.assertFalse(result["dispatches"])
        self.assertEqual(self.server.started, [])

    def test_failed_turn_and_multiple_images_remain_unknown(self):
        _, job = self.first_dispatch(count=1)
        turn = self.server.history[job["thread_id"]][0]
        turn["status"] = "failed"
        self.assertEqual(self.host.poll(job)["status"], "unknown")
        self.server.finish(job["thread_id"], inline=True)
        turn["items"].append(copy.deepcopy(turn["items"][-1]))
        self.assertEqual(self.host.poll(job)["status"], "unknown")
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)

    def test_missing_thread_identifier_is_never_recreated_on_restart(self):
        self.run_fixture(count=1)
        with patch.object(self.server, "start_thread", side_effect=RpcUnavailable("lost creation response")):
            self.host.tick()
        self.assertEqual(len(self.host._jobs()), 1)
        restarted = ImageHost(self.production, self.server, self.config)
        self.assertEqual(restarted.tick()["observations"][0]["status"], "unknown")
        self.assertEqual(self.server.started, [])

    def test_corrupt_native_file_is_not_reported_complete(self):
        _, job = self.first_dispatch(count=1)
        self.server.finish(job["thread_id"])
        (Path(job["directory"]) / "result.png").write_text("not an image")
        result = self.host.tick()
        self.assertTrue(result["blockers"])
        self.assertIsNone(self.host._jobs()[0]["observation"])


@unittest.skipUnless(os.environ.get("YTV_TEST_POSTGRES_URL"), "requires isolated PostgreSQL")
class PostgreSQLImageHostTests(ImageHostTests):
    postgres = True

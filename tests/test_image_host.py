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
from ytvideos.runtime.app_server import AppServer, ImageNotSent, RpcError, RpcUnavailable
from ytvideos.runtime.image_host import ImageHost
from ytvideos.util import canonical, digest, file_digest


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

    def start_image(self, thread_id, directory, prompt, *, before_send=None):
        try:
            if before_send is not None:
                before_send()
        except (WorkflowError, OSError, ValueError) as exc:
            raise ImageNotSent(str(exc)) from exc
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
        standards.mkdir(parents=True, exist_ok=True)
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

    def test_thumbnail_worker_receives_readable_thumbnail_standard_inside_its_sandbox(self):
        profile_path = self.production.project / "channels/test_channel/channel.json"
        profile = json.loads(profile_path.read_text())
        profile["recipe"] = "licensed_clips"
        profile_path.write_text(json.dumps(profile))
        run_id, _ = self.make_run(count=1, shared_review_capacity=4)
        brief = self.root / "packaging.json"
        brief.write_text(json.dumps({"title": "Accepted synthetic packaging fixture"}))
        artifact = self.production.artifacts.put(brief, "release_spec")
        def prepared(tx, run):
            run["artifacts"][artifact["id"]] = artifact
            run["tasks"]["packaging"].update(status="complete", outputs=[artifact["id"]])
        self.store.mutate(run_id, prepared)
        self.production.add_thumbnail_task(run_id, {
            "id": "cover", "prompt": "Synthetic cover", "visual_intent": "A specific promise",
            "reference_na_reason": "Synthetic fixture has no external visual references."})
        self.pools.operate(run_id, "enqueue")
        self.pools.operate(run_id, "tick")
        result = self.host.tick()
        self.assertEqual(len(result["dispatches"]), 1, result)
        job = self.host._jobs()[0]
        directory = Path(job["directory"])
        packet = json.loads((directory / "TASK.json").read_text())
        path = "requirements/docs/standards/thumbnails.md"
        self.assertIn(path, packet["requirements"])
        self.assertEqual((directory / path).read_text(), "Synthetic requirement: docs/standards/thumbnails.md\n")
        self.assertEqual(job["inputs"][path], file_digest(directory / path))
        self.assertEqual(set(packet["requirements"]), {"requirements/" + path for path in packet["references"]})

    def test_regular_scene_worker_does_not_receive_thumbnail_playbook(self):
        _, job = self.first_dispatch(count=1)
        packet = json.loads((Path(job["directory"]) / "TASK.json").read_text())
        self.assertNotIn("requirements/docs/standards/thumbnails.md", packet["requirements"])
        for path in packet["requirements"]:
            self.assertTrue((Path(job["directory"]) / path).is_file())

    def test_requirement_manifest_cannot_omit_or_escape_declared_documents(self):
        run_id = self.run_fixture(count=1)
        run = self.store.get(run_id)
        request = next(value for value in run["pool"]["backend"]["requests"].values()
                       if value["status"] == "queued")
        for malformed in ("missing", "escape", "changed"):
            with self.subTest(malformed=malformed):
                candidate = copy.deepcopy(request)
                context = candidate["packet"]["context"]
                if malformed == "missing":
                    context["reference_documents"].pop()
                elif malformed == "escape":
                    context["reference_documents"][0]["path"] = "../escaped.md"
                    context["references"][0] = "../escaped.md"
                else:
                    context["reference_documents"][0]["text"] = "Altered contents"
                candidate["packet"]["input_hash"] = digest(context)
                with self.assertRaises(WorkflowError):
                    self.host._materialize(run, candidate)
        self.assertEqual(self.server.started, [])

    def test_rehashed_outbox_documents_or_skill_cannot_replace_the_queued_job(self):
        for altered in ("omitted", "document", "skill"):
            with self.subTest(altered=altered):
                run_id = self.run_fixture(count=1)
                def corrupt(tx, run):
                    request = next(item for item in run["pool"]["backend"]["requests"].values()
                                   if item["status"] == "queued")
                    context = request["packet"]["context"]
                    if altered == "omitted":
                        context.update(references=[], reference_documents=[])
                    elif altered == "document":
                        document = context["reference_documents"][0]
                        document["text"] = "Altered requirement with a matching checksum"
                        import hashlib
                        document["sha256"] = hashlib.sha256(document["text"].encode()).hexdigest()
                    else:
                        context["skill"]["text"] = "Substituted worker skill"
                    request["packet"]["input_hash"] = digest(context)
                self.store.mutate(run_id, corrupt)
                result = self.host.tick()
                self.assertEqual(result["dispatches"], [])
                self.assertTrue(any("queued job" in blocker["reason"] for blocker in result["blockers"]))
        self.assertEqual(self.server.started, [])

    def test_matching_outbox_and_queue_still_must_use_the_run_document_snapshot(self):
        run_id = self.run_fixture(count=1)
        def corrupt(tx, run):
            request = next(item for item in run["pool"]["backend"]["requests"].values()
                           if item["status"] == "queued")
            context = request["packet"]["context"]
            context.update(references=[], reference_documents=[])
            request["packet"]["input_hash"] = digest(context)
            record = next(item for item in run["pool"]["scheduler"]["records"]
                          if item["job"]["job_id"] == request["packet"]["job_id"])
            record["job"].update(context_json=canonical(context), input_hash=digest(context))
        self.store.mutate(run_id, corrupt)
        result = self.host.tick()
        self.assertEqual(result["dispatches"], [])
        self.assertIn("pinned task context", result["blockers"][0]["reason"])
        self.assertEqual(self.server.started, [])

    def test_missing_channel_profile_blocks_native_generation(self):
        (self.production.project / "channels/test_channel/PROFILE.md").unlink()
        self.run_fixture(count=1)
        result = self.host.tick()
        self.assertEqual(result["dispatches"], [])
        self.assertIn("PROFILE.md", result["blockers"][0]["reason"])
        self.assertEqual(self.server.started, [])

    def test_parent_symlink_cannot_move_requirements_outside_the_worker(self):
        _, job = self.first_dispatch(count=1)
        directory = Path(job["directory"])
        relocated = self.root / "outside-worker-requirements"
        (directory / "requirements").rename(relocated)
        (directory / "requirements").symlink_to(relocated, target_is_directory=True)
        with self.assertRaisesRegex(WorkflowError, "pinned input"):
            self.host._verify_inputs(job)

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
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "blocked")

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


    def test_missing_reference_does_not_starve_another_channel(self):
        bad = self.run_fixture(count=1, channel="second")
        self.production.revise(bad, "image:s0", "unavailable reference")
        def change(tx, run):
            run["tasks"]["image:s0"]["payload"]["references"] = ["missing-artifact"]
        self.store.mutate(bad, change)
        good = self.run_fixture(count=1, channel="third")
        first = self.host.tick()
        self.assertTrue(first["blockers"])
        second = self.host.tick()
        self.assertEqual(len(second["dispatches"]), 1, second)
        self.assertEqual(self.host._jobs()[0]["run_id"], good)
        self.assertEqual(self.store.get(bad)["tasks"]["image:s0"]["status"], "blocked")
        self.assertEqual(self.store.get(bad)["budget"]["reserved"], 0)

    def test_missing_reference_releases_unsent_local_slot_for_another_scene(self):
        run_id = self.run_fixture(count=2)
        # The first queued scene loses its actual reference bytes before dispatch.
        self.image.unlink()
        run = self.store.get(run_id)
        reference = run["tasks"]["image:s0"]["payload"]["references"][0]
        self.production.artifacts.resolve(run["artifacts"][reference]).unlink()
        self.host.tick()
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "blocked")
        # Other pending scenes are not permanently held behind the unsent request.
        self.host.tick()
        state = self.store.get(run_id)
        self.assertEqual(state["tasks"]["image:s1"]["status"], "blocked")
        self.assertEqual(self.server.started, [])


    def test_preflight_blocker_cannot_revoke_a_dispatched_attempt(self):
        run_id, job = self.first_dispatch(count=1)
        with self.assertRaises(Conflict):
            self.host._block_unsent({"run_id": run_id, "operation_id": job["id"]}, "late preflight result")
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "running")
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)

    def test_repaired_reference_starts_only_the_new_generation(self):
        run_id = self.run_fixture(count=1)
        self.production.revise(run_id, "image:s0", "reference unavailable")
        def change(tx, run):
            run["tasks"]["image:s0"]["payload"]["references"] = ["missing-artifact"]
        self.store.mutate(run_id, change)
        self.host.tick()
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "blocked")
        self.production.revise(run_id, "image:s0", "reference restored")
        image = self.production.attach(run_id, self.image, kind="image", source="restored fixture")
        def fix(tx, run):
            run["tasks"]["image:s0"]["payload"]["references"] = [image["id"]]
        self.store.mutate(run_id, fix)
        result = self.host.tick()
        self.assertEqual(len(result["dispatches"]), 1, result)
        self.assertEqual(len(self.server.started), 1)


    def test_cancel_during_native_preflight_does_not_start_image_turn(self):
        run_id = self.run_fixture(count=1)
        calls = []
        def native_call(method, params):
            calls.append(method)
            if method == "thread/start":
                return {"thread": {"id": "cancel-preflight"}, "model": "test-luna"}
            if method == "mcpServerStatus/list":
                self.production.cancel(run_id, "user cancelled during native preflight")
                return {"data": []}
            if method == "turn/start":
                return {"turn": {"id": "must-not-start"}}
            raise AssertionError(method)
        rpc = unittest.mock.Mock()
        rpc.call.side_effect = native_call
        host = ImageHost(self.production, AppServer(rpc, "test-luna"), self.config)
        host.tick()
        self.assertNotIn("turn/start", calls)
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 0)
        self.assertEqual(self.store.get(run_id)["budget"]["reserved"], 0)
        self.assertEqual(host._jobs()[0]["state"], "delivered")

    def test_input_mutation_during_native_preflight_stops_before_turn(self):
        run_id = self.run_fixture(count=1)
        calls, directory = [], []
        def native_call(method, params):
            calls.append(method)
            if method == "thread/start":
                directory.append(Path(params["cwd"]))
                return {"thread": {"id": "tampered-preflight"}, "model": "test-luna"}
            if method == "mcpServerStatus/list":
                (directory[0] / "SKILL.md").write_text("changed after materialization")
                return {"data": []}
            if method == "turn/start":
                return {"turn": {"id": "must-not-start"}}
            raise AssertionError(method)
        rpc = unittest.mock.Mock()
        rpc.call.side_effect = native_call
        host = ImageHost(self.production, AppServer(rpc, "test-luna"), self.config)
        host.tick()
        self.assertNotIn("turn/start", calls)
        state = self.store.get(run_id)
        self.assertEqual(state["tasks"]["image:s0"]["status"], "blocked")
        self.assertEqual(state["budget"]["reserved"], 0)
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 0)

    def test_nontext_reference_explanation_is_not_an_exemption(self):
        run_id = self.run_fixture(count=1)
        self.production.revise(run_id, "image:s0", "invalid reference exemption")
        def change(tx, run):
            run["tasks"]["image:s0"]["payload"].update(references=[], reference_na_reason=None)
        self.store.mutate(run_id, change)
        self.host.tick()
        self.assertEqual(self.server.started, [])
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "blocked")

    def test_malformed_turn_does_not_prevent_collecting_other_channel(self):
        self.run_fixture(capacity=3, count=1, channel="second")
        self.run_fixture(capacity=3, count=1, channel="third")
        self.host.tick()
        self.host.tick()
        jobs = self.host._jobs()
        self.assertEqual(len(jobs), 2)
        self.server.history[jobs[0]["thread_id"]][0]["items"] = None
        self.server.finish(jobs[1]["thread_id"], inline=True)
        result = self.host.tick()
        self.assertTrue(result["blockers"])
        self.assertTrue(any(item["operation_id"] == jobs[1]["id"] and item["status"] == "delivered"
                            for item in result["observations"]))
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)


    def test_rejected_preflight_does_not_hold_slot_or_retry_forever(self):
        run_id = self.run_fixture(count=1)
        calls = []
        def native_call(method, params):
            calls.append(method)
            if method == "thread/start":
                return {"thread": {"id": "has-connector"}, "model": "test-luna"}
            if method == "mcpServerStatus/list":
                return {"data": [{"name": "not-allowed"}]}
            raise AssertionError(method)
        rpc = unittest.mock.Mock()
        rpc.call.side_effect = native_call
        host = ImageHost(self.production, AppServer(rpc, "test-luna"), self.config)
        result = host.tick()
        self.assertFalse(result["dispatches"])
        self.assertEqual(result["blockers"][0]["error"], "ImageNotSent")
        host.tick()
        self.assertEqual(calls, ["thread/start", "mcpServerStatus/list"])
        self.assertEqual(host._jobs()[0]["observation"]["actual_units"], 0)
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "blocked")
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 0)
        self.assertEqual(self.pools.operate(run_id, "status")["review"]["used"], 0)

    def test_turn_start_error_is_not_treated_as_a_proven_unsent_request(self):
        self.run_fixture(count=1)
        calls = []
        def native_call(method, params):
            calls.append(method)
            if method == "thread/start":
                return {"thread": {"id": "uncertain-turn"}, "model": "test-luna"}
            if method == "mcpServerStatus/list":
                return {"data": []}
            if method == "turn/start":
                raise RpcError(method, -32000)
            raise AssertionError(method)
        rpc = unittest.mock.Mock()
        rpc.call.side_effect = native_call
        host = ImageHost(self.production, AppServer(rpc, "test-luna"), self.config)
        result = host.tick()
        self.assertTrue(result["blockers"])
        self.assertIn("turn/start", calls)
        self.assertEqual(host._jobs()[0]["state"], "turn_dispatching")
        self.assertIsNone(host._jobs()[0]["observation"])
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)

    def test_restart_does_not_infer_no_send_from_thread_created_state(self):
        self.run_fixture(count=1)
        with patch.object(self.server, "start_image", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.host.tick()
        self.assertEqual(self.host._jobs()[0]["state"], "thread_created")
        restarted = ImageHost(self.production, self.server, self.config)
        result = restarted.tick()
        self.assertEqual(result["observations"][0]["status"], "unknown")
        self.assertFalse(result["dispatches"])
        self.assertEqual(len(self.server.started), 1)
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)


    def test_disconnected_dispatch_does_not_consume_more_channels_slots(self):
        self.run_fixture(capacity=3, count=1, channel="second")
        self.run_fixture(capacity=3, count=1, channel="third")
        with patch.object(self.server, "start_thread", side_effect=RpcUnavailable("disconnected")) as start:
            self.host.tick()
            result = self.host.tick()
            self.assertEqual(start.call_count, 1)
        self.assertFalse(result["dispatches"])
        self.assertEqual(len(self.host._jobs()), 1)
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)


@unittest.skipUnless(os.environ.get("YTV_TEST_POSTGRES_URL"), "requires isolated PostgreSQL")
class PostgreSQLImageHostTests(ImageHostTests):
    postgres = True

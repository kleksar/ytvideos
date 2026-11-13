import base64
import json
import runpy
import unittest
from unittest.mock import patch
from uuid import uuid4

import test_workflow


class OperatorScriptApproval(unittest.TestCase):
    def test_import_records_exact_script_once_and_opens_production(self):
        fixture = test_workflow.WorkflowContract()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.addCleanup(fixture.tearDown)
        fixture.script_ready()
        service = fixture.service
        approval = service.next(fixture.run_id)["approval_requests"][0]["artifact"]
        script = service.artifacts.resolve(approval)
        tool = runpy.run_path(str(test_workflow.ROOT / "scripts" / "operator_script_approval.py"))
        key = fixture.directory / "operator.pem"
        envelope = fixture.directory / "event.json"
        observation = fixture.output({
            "record_type": "historical_codex_chat_observation",
            "thread_id": str(uuid4()), "approval_message_id": str(uuid4()),
            "approval_turn_started_at": "2026-01-01T00:00:00Z",
            "approval_message": "Approved fixture script for production.",
            "run_id": fixture.run_id, "artifact_id": approval["id"], "artifact_sha256": approval["sha256"],
        })
        main = tool["main"]
        with patch.dict(main.__globals__, {"passphrase": lambda _: b"fixture password"}), \
             patch("builtins.print") as display, patch("builtins.input", return_value="RECORD"):
            self.assertEqual(main(["init-key", "--key", str(key)]), 0)
            public_key = display.call_args.args[0]
            self.assertEqual(len(base64.b64decode(public_key)), 32)
            self.assertIn(b"BEGIN ENCRYPTED PRIVATE KEY", key.read_bytes())
            service.approvals.public_key = public_key
            command = ["sign", "--key", str(key), "--observation", str(observation),
                       "--actor", "operator-fixture", "--output", str(envelope), "--script"]
            with self.assertRaises(SystemExit), patch("sys.stderr"):
                main(command + [str(fixture.output("Changed script"))])
            self.assertFalse(envelope.exists())
            self.assertEqual(main(command + [str(script)]), 0)
        event = json.loads(envelope.read_text())
        self.assertEqual(event["event"]["scope"], "produce_video")
        service.approve(event)
        service.approve(event)
        events = [event for event in fixture.store.events(fixture.run_id) if event["kind"] == "user.approved"]
        self.assertEqual(len(events), 1)
        self.assertEqual({task["id"] for task in service.next(fixture.run_id)["tasks"]},
                         {"storyboard", "audio", "packaging"})

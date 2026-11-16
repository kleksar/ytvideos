"""Exercise the real workflow-to-subprocess boundary without provider traffic."""
from pathlib import Path
import json
import subprocess
import unittest
from unittest.mock import Mock

import test_workflow
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.executor import MediaExecutor


class MediaExecutorTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_workflow.WorkflowContract()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.fixture.production_ready()
        self.service = self.fixture.service
        self.run_id = self.fixture.run_id
        self.claim = self.service.claim(self.run_id, "audio", "fixture-audio-worker", estimated_units=2)

    def test_tts_binds_approved_text_and_voice_and_does_not_claim_audio_qa(self):
        def process(command, **kwargs):
            output = Path(command[command.index("--output-dir") + 1])
            output.mkdir(parents=True)
            # Deliberately not real audio: subprocess success cannot complete its QA task.
            (output / "voice_en.mp3").write_bytes(b"synthetic provider output fixture")
            return subprocess.CompletedProcess(command, 0, stdout="fixture", stderr="")

        runner = Mock(side_effect=process)
        executor = MediaExecutor(self.service, runner=runner)
        result = executor.execute(self.run_id, "audio", self.claim["token"], {"kind": "tts"})
        command = runner.call_args.args[0]
        run = self.fixture.store.get(self.run_id)
        self.assertEqual(command[command.index("--voice-id") + 1], run["profile"]["voice"]["id"])
        self.assertEqual(command[command.index("--speed") + 1], "1.0")
        self.assertEqual(Path(command[command.index("--en-text") + 1]).read_text(), test_workflow.SCRIPT)
        self.assertEqual(result["execution"]["state"], "completed")
        self.assertEqual(run["tasks"]["audio"]["status"], "running")
        self.assertEqual(run["tasks"]["audio"]["outputs"], [])
        self.assertFalse(result["audio_processing"]["final_speed_processing_performed"])
        with self.assertRaises(Conflict):
            executor.execute(self.run_id, "audio", self.claim["token"], {"kind": "tts"})
        runner.assert_called_once()

    def test_explicit_flash_account_is_bound_to_single_operation(self):
        def process(command, **kwargs):
            output = Path(command[command.index("--output-dir") + 1])
            output.mkdir(parents=True)
            (output / "voice_en.mp3").write_bytes(b"synthetic fixture")
            return subprocess.CompletedProcess(command, 0, stdout="fixture", stderr="")
        runner = Mock(side_effect=process)
        executor = MediaExecutor(self.service, runner=runner)
        request = {"kind": "tts", "model": "eleven_flash_v2_5", "account_slot": 2,
                   "account_sha256": "a" * 64}
        executor.execute(self.run_id, "audio", self.claim["token"], request)
        command = runner.call_args.args[0]
        self.assertEqual(command[command.index("--model") + 1], "eleven_flash_v2_5")
        self.assertEqual(command[command.index("--account-slot") + 1], "2")
        self.assertEqual(command[command.index("--account-sha256") + 1], "a" * 64)
        self.assertEqual(command[command.index("--max-credits") + 1], "2")
        with self.fixture.store.transaction() as tx:
            operation = json.loads(tx.execute("SELECT doc FROM operations WHERE run_id=?", (self.run_id,)).fetchone()[0])
        self.assertEqual(operation["payload"]["tts_selection"]["account_slot"], 2)
        with self.assertRaises(Conflict):
            executor.execute(self.run_id, "audio", self.claim["token"], request)
        runner.assert_called_once()

    def test_caller_cannot_override_canonical_tts_parameters(self):
        runner = Mock()
        with self.assertRaises(WorkflowError):
            MediaExecutor(self.service, runner=runner).execute(
                self.run_id, "audio", self.claim["token"],
                {"kind": "tts", "args": ["--voice-id", "another-voice"]})
        runner.assert_not_called()
        self.assertFalse(any(event["kind"] == "media.dispatch" for event in self.fixture.store.events(self.run_id)))

    def test_explicit_selection_rejects_unbound_or_invalid_inputs(self):
        runner = Mock()
        executor = MediaExecutor(self.service, runner=runner)
        for request in ({"kind": "tts", "model": "eleven_flash_v2_5"},
                        {"kind": "tts", "model": "other", "account_slot": 2, "account_sha256": "a" * 64},
                        {"kind": "tts", "model": "eleven_flash_v2_5", "account_slot": True, "account_sha256": "a" * 64},
                        {"kind": "tts", "model": "eleven_flash_v2_5", "account_slot": 2, "account_sha256": "invalid"}):
            with self.subTest(request=request), self.assertRaises(WorkflowError):
                executor.execute(self.run_id, "audio", self.claim["token"], request)
        runner.assert_not_called()
        self.assertFalse(any(event["kind"] == "media.dispatch" for event in self.fixture.store.events(self.run_id)))

    def test_single_attempt_rejects_prior_operation_even_from_another_input(self):
        with self.fixture.store.transaction() as tx:
            tx.create_operation({"key": "fixture-prior-tts", "run_id": self.run_id, "task_id": "audio",
                                 "kind": "tts", "input_hash": "prior", "task_input_hash": "old-revision",
                                 "status": "not_performed"})
        runner = Mock()
        request = {"kind": "tts", "model": "eleven_flash_v2_5", "account_slot": 2,
                   "account_sha256": "a" * 64}
        with self.assertRaisesRegex(Conflict, "single-attempt TTS"):
            MediaExecutor(self.service, runner=runner).execute(self.run_id, "audio", self.claim["token"], request)
        runner.assert_not_called()

    def test_default_tts_cannot_retry_prior_single_attempt_after_revision(self):
        with self.fixture.store.transaction() as tx:
            tx.create_operation({"key": "fixture-prior-single-tts", "run_id": self.run_id, "task_id": "audio",
                                 "kind": "tts", "input_hash": "prior", "task_input_hash": "old-revision",
                                 "status": "not_performed", "payload": {"tts_selection": {"model": "fixture"}}})
        runner = Mock()
        with self.assertRaisesRegex(Conflict, "single-attempt TTS"):
            MediaExecutor(self.service, runner=runner).execute(self.run_id, "audio", self.claim["token"], {"kind": "tts"})
        runner.assert_not_called()


if __name__ == "__main__":
    unittest.main()

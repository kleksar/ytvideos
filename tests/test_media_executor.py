"""Exercise the real workflow-to-subprocess boundary without provider traffic."""
from pathlib import Path
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

    def test_caller_cannot_override_canonical_tts_parameters(self):
        runner = Mock()
        with self.assertRaises(WorkflowError):
            MediaExecutor(self.service, runner=runner).execute(
                self.run_id, "audio", self.claim["token"],
                {"kind": "tts", "args": ["--voice-id", "another-voice"]})
        runner.assert_not_called()
        self.assertFalse(any(event["kind"] == "media.dispatch" for event in self.fixture.store.events(self.run_id)))


if __name__ == "__main__":
    unittest.main()

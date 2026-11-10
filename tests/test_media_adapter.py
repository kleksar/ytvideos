import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock

from ytvideos.adapters.media import LocalMediaAdapter, TOOLS, file_sha256
from ytvideos.errors import Conflict


class MediaAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.script = self.root / TOOLS['tts']
        self.script.parent.mkdir(parents=True)
        # This local script is a harmless process fixture; no provider is called.
        self.script.write_text('import pathlib,sys\npathlib.Path(sys.argv[1]).write_text(sys.argv[2])\nprint("fixture")\n')
        self.source = self.root / 'accepted.txt'
        self.source.write_text('Approved narration fixture')
        self.output = self.root / 'voice.mp3'
        self.receipt = self.root / 'receipt.json'
        self.guard = Mock()
        self.claim = {'token': 'lease-1', 'expires_at': 1000, 'input_hash': 'input-1'}

    def execute(self, **kwargs):
        adapter = LocalMediaAdapter(self.root, guard=self.guard, clock=lambda: 10, **kwargs)
        return adapter.execute('tts', [str(self.output), 'literal `$(no-shell)` ; text'],
                               run_id='run-1', task_id='audio', claim=self.claim, input_hash='input-1',
                               inputs=[{'path': str(self.source), 'sha256': file_sha256(self.source)}],
                               outputs=[str(self.output)], receipt_path=self.receipt)

    def test_real_subprocess_preserves_literal_args_and_records_outputs(self):
        result = self.execute()
        self.assertEqual(result['state'], 'completed')
        self.assertEqual(self.output.read_text(), 'literal `$(no-shell)` ; text')
        self.assertEqual(result['output_artifacts'][0]['sha256'], file_sha256(self.output))
        self.assertEqual(result['stdout'].strip(), 'fixture')
        self.guard.assert_called_once()
        self.assertEqual(json.loads(self.receipt.read_text())['state'], 'completed')
        self.assertEqual(self.receipt.stat().st_mode & 0o777, 0o600)

    def test_guard_rejection_prevents_process_and_receipt(self):
        self.guard.side_effect = Conflict('Approval missing')
        runner = Mock()
        with self.assertRaises(Conflict):
            self.execute(runner=runner)
        runner.assert_not_called()
        self.assertFalse(self.receipt.exists())

    def test_expired_claim_prevents_dispatch(self):
        self.claim['expires_at'] = 5
        runner = Mock()
        with self.assertRaises(Conflict):
            self.execute(runner=runner)
        runner.assert_not_called()
        self.guard.assert_not_called()

    def test_input_change_between_guard_and_dispatch_is_rejected(self):
        self.guard.side_effect = lambda _: self.source.write_text('Changed')
        runner = Mock()
        with self.assertRaises(Conflict):
            self.execute(runner=runner)
        runner.assert_not_called()

    def test_existing_result_requires_reconciliation(self):
        self.execute()
        with self.assertRaises(Conflict):
            self.execute()

    def test_unknown_paid_outcome_has_marker_and_no_automatic_retry(self):
        runner = Mock(side_effect=subprocess.TimeoutExpired('fixture', 10))
        adapter = LocalMediaAdapter(self.root, guard=self.guard, runner=runner, clock=lambda: 10)
        def execute():
            return adapter.execute('tts', ['--generate'], run_id='run-1', task_id='audio',
                                   claim=self.claim, input_hash='input-1',
                                   inputs=[{'path': str(self.source), 'sha256': file_sha256(self.source)}],
                                   outputs=[str(self.output)], receipt_path=self.receipt)
        result = execute()
        self.assertEqual(result['state'], 'outcome_unknown')
        self.assertTrue(self.guard.call_args.args[0]['paid'])
        self.assertEqual(json.loads(self.receipt.read_text())['state'], 'outcome_unknown')
        with self.assertRaises(Conflict):
            execute()
        runner.assert_called_once()

    def test_success_without_output_does_not_report_complete(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, stdout='OK', stderr=''))
        self.assertEqual(self.execute(runner=runner)['state'], 'failed')
        self.assertFalse(runner.call_args.kwargs['shell'])


if __name__ == '__main__':
    unittest.main()

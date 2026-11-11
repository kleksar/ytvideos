from __future__ import annotations

import os
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "composer_lock.py"


class ComposerLockTests(unittest.TestCase):
    @staticmethod
    def stop_process(process):
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=10)

    def test_interrupt_release_does_not_inherit_ignored_signal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            env = dict(os.environ, YTVIDEOS_CHATGPT_SESSION_LOCK=str(Path(temp) / 'lock'))
            launcher = ('import os, signal, sys; signal.signal(signal.SIGINT, signal.SIG_IGN); '
                        'os.execv(sys.executable, [sys.executable, *sys.argv[1:]])')
            child = subprocess.Popen([sys.executable, '-c', launcher, str(SCRIPT), '--task-id', 'background'],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
            self.addCleanup(self.stop_process, child)
            self.assertTrue(child.stdout.readline().startswith('LOCK_ACQUIRED '))
            child.send_signal(signal.SIGINT)
            output, _ = child.communicate(timeout=10)
            self.assertEqual(child.returncode, 0)
            self.assertIn('LOCK_RELEASED', output)

    def test_bad_ack_and_unresolved_eof(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            env = os.environ.copy()
            env['YTVIDEOS_CHATGPT_SESSION_LOCK'] = str(Path(temp) / 'lock')
            p = subprocess.Popen([sys.executable, str(SCRIPT), '--task-id', 'one', '--controlled'],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
            self.assertTrue(p.stdout.readline().startswith('LOCK_ACQUIRED '))
            self.assertEqual(p.stdout.readline().strip(), 'READY')
            p.stdin.write('VERIFIED\n'); p.stdin.flush()
            self.assertEqual(p.stdout.readline().strip(), 'INVALID_COMMAND')
            p.stdin.write('PENDING ' + 'c'*64 + '\n'); p.stdin.flush()
            self.assertEqual(p.stdout.readline().strip(), 'PENDING_RECORDED')
            p.stdin.close(); self.assertEqual(p.wait(timeout=3), 4)
            p.stdout.close(); p.stderr.close()
            legacy = subprocess.run([sys.executable, str(SCRIPT), '--task-id', 'legacy'],
                                    capture_output=True, text=True, env=env, timeout=3)
            self.assertEqual(legacy.returncode, 4)
            self.assertIn('NEEDS_INSPECTION', legacy.stdout)
            self.assertNotIn('LOCK_ACQUIRED', legacy.stdout)
            q = subprocess.run([sys.executable, str(SCRIPT), '--task-id', 'next', '--controlled'],
                               input='', capture_output=True, text=True, env=env, timeout=3)
            self.assertEqual(q.returncode, 4)
            self.assertIn('NEEDS_INSPECTION', q.stdout)
            self.assertNotIn('READY', q.stdout)

    def test_controlled_release_and_crash_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            env = os.environ.copy()
            env['YTVIDEOS_CHATGPT_SESSION_LOCK'] = str(Path(temp) / 'lock')
            def start(task):
                return subprocess.Popen([sys.executable, str(SCRIPT), '--task-id', task, '--controlled'],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
            first = start('one')
            self.assertTrue(first.stdout.readline().startswith('LOCK_ACQUIRED '))
            self.assertEqual(first.stdout.readline().strip(), 'READY')
            first.stdin.write('PENDING ' + 'a' * 64 + '\n'); first.stdin.flush()
            self.assertEqual(first.stdout.readline().strip(), 'PENDING_RECORDED')
            blocked = subprocess.run([sys.executable, str(SCRIPT), '--task-id', 'legacy'], env=env,
                                     capture_output=True, text=True, timeout=3)
            self.assertEqual(blocked.returncode, 3)
            first.stdin.write('VERIFIED\n'); first.stdin.flush()
            self.assertIn('LOCK_RELEASED verified', first.stdout.readline())
            first.communicate(timeout=3)
            second = start('two')
            self.assertTrue(second.stdout.readline().startswith('LOCK_ACQUIRED '))
            self.assertEqual(second.stdout.readline().strip(), 'READY')
            second.stdin.write('PENDING ' + 'b' * 64 + '\n'); second.stdin.flush()
            self.assertEqual(second.stdout.readline().strip(), 'PENDING_RECORDED')
            second.kill(); second.communicate(timeout=3)
            recovery = start('recovery')
            self.assertTrue(recovery.stdout.readline().startswith('LOCK_ACQUIRED '))
            self.assertIn('NEEDS_INSPECTION', recovery.stdout.readline())
            recovery.stdin.write('INSPECTED\n'); recovery.stdin.flush()
            self.assertEqual(recovery.stdout.readline().strip(), 'INSPECTION_RECORDED')
            self.assertEqual(recovery.stdout.readline().strip(), 'READY')
            recovery.stdin.close(); recovery.wait(timeout=3)
            recovery.stdout.close(); recovery.stderr.close()

    def test_exclusive_lock_reports_owner_and_releases_on_interrupt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            env = os.environ.copy()
            env["YTVIDEOS_CHATGPT_SESSION_LOCK"] = str(Path(temp) / "composer.lock")
            first = subprocess.Popen(
                [sys.executable, str(SCRIPT), "--task-id", "task-one"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
            )
            self.addCleanup(self.stop_process, first)
            try:
                self.assertTrue(first.stdout)
                acquired = first.stdout.readline().strip()
                self.assertTrue(acquired.startswith("LOCK_ACQUIRED "), acquired)

                blocked = subprocess.run(
                    [sys.executable, str(SCRIPT), "--task-id", "task-two"],
                    capture_output=True,
                    text=True,
                    env=env,
                    timeout=3,
                )
                self.assertEqual(blocked.returncode, 3)
                self.assertIn('"task_id":"task-one"', blocked.stderr)
            finally:
                first.send_signal(signal.SIGINT)
                first.communicate(timeout=10)

            next_owner = subprocess.Popen(
                [sys.executable, str(SCRIPT), "--task-id", "task-two"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
            )
            self.addCleanup(self.stop_process, next_owner)
            try:
                self.assertTrue(next_owner.stdout)
                self.assertTrue(next_owner.stdout.readline().startswith("LOCK_ACQUIRED "))
            finally:
                next_owner.send_signal(signal.SIGINT)
                next_owner.communicate(timeout=10)


if __name__ == "__main__":
    unittest.main()

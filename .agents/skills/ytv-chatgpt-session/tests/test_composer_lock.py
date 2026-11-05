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
                first.communicate(timeout=3)

            next_owner = subprocess.Popen(
                [sys.executable, str(SCRIPT), "--task-id", "task-two"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
            )
            try:
                self.assertTrue(next_owner.stdout)
                self.assertTrue(next_owner.stdout.readline().startswith("LOCK_ACQUIRED "))
            finally:
                next_owner.send_signal(signal.SIGINT)
                next_owner.communicate(timeout=3)


if __name__ == "__main__":
    unittest.main()

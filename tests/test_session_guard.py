"""Hook contract tests; no live Codex hook activation or provider execution."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import threading
import time
import unittest
from unittest.mock import patch

import test_pool_service as fixtures
from ytvideos.cli import dispatch, parser
from ytvideos.session_guard import MAX_CONTINUATIONS, bind_session, decide, registry_path
from ytvideos.util import canonical


class SessionGuardTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.PoolServiceTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.production = self.fixture.production
        self.production.clock = time.time
        self.project = self.production.project
        self.run = self.production.create("test_channel", "Find and verify a story")
        self.run_id = self.run["id"]
        self.environment = patch.dict(os.environ, {"CODEX_THREAD_ID": "writer-session"})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def event(self, **overrides):
        return {"hook_event_name": "Stop", "session_id": "writer-session", "turn_id": "user-turn",
                "cwd": str(self.project), "stop_hook_active": False, **overrides}

    def stop(self, **overrides):
        return decide(self.event(**overrides), self.project)

    def bind(self):
        return bind_session(self.production, self.run_id)

    def mutate(self, function):
        self.production.store.mutate(self.run_id, lambda tx, run: function(run))

    def assertAllowed(self, result):
        self.assertNotIn("decision", result, result)
        self.assertIn("systemMessage", result)

    def test_unbound_missing_and_different_sessions_never_choose_an_existing_run(self):
        self.assertAllowed(self.stop())
        self.assertFalse(registry_path(self.project).exists())
        self.bind()
        self.assertAllowed(self.stop(session_id="unrelated-maintenance"))
        self.assertAllowed(self.stop(session_id=None))
        self.assertAllowed(self.stop(cwd=str(self.fixture.root)))
        self.assertAllowed(self.stop(hook_event_name="SubagentStop", agent_id="independent-reader"))
        self.assertAllowed(self.stop(hook_event_name="SubagentStop"))

    def test_cli_start_and_resume_bind_exact_run_but_reads_create_and_claim_do_not(self):
        for command in ("status", "next", "plan"):
            dispatch(self.production, parser().parse_args([command, "--run", self.run_id]))
        self.assertFalse(registry_path(self.project).exists())
        created = dispatch(self.production, parser().parse_args(["create", "--channel", "test_channel", "--intent", "another story"]))
        self.assertFalse(registry_path(self.project).exists())
        started = dispatch(self.production, parser().parse_args(["start", "--channel", "test_channel", "--intent", "a new story"]))
        self.assertEqual(started["session_guard"]["session_id"], "writer-session")
        self.assertIn(started["run_id"], self.stop()["reason"])
        self.assertNotIn(created["run_id"], self.stop()["reason"])
        resumed = dispatch(self.production, parser().parse_args(["resume", "--run", self.run_id, "--session-id", "explicit-host"]))
        self.assertEqual(resumed["session_guard"]["session_id"], "explicit-host")
        self.assertIn(self.run_id, self.stop(session_id="explicit-host")["reason"])

    def test_unknown_capabilities_continue_with_exact_context_and_no_workflow_writes(self):
        self.bind()
        before = self.production.store.get(self.run_id)
        result = self.stop()
        self.assertEqual(result["decision"], "block")
        for expected in (self.run_id, "inspect_runtime_tools", "awaiting_script_approval", "context", str(self.production.workspace), str(Path(self.fixture.db).resolve())):
            self.assertIn(expected, result["reason"])
        self.assertEqual(before, self.production.store.get(self.run_id))
        self.production.capabilities(self.run_id, {"web.search": True}, evidence="synthetic exposed tool")
        self.assertIn("read_context_then_claim", self.stop(stop_hook_active=True)["reason"])

    def test_confirmed_unavailable_is_a_blocker_but_false_without_evidence_is_not(self):
        self.bind()
        self.mutate(lambda run: run["capabilities"].update({"web.search": {"available": False}}))
        self.assertEqual(self.stop()["decision"], "block")
        self.production.capabilities(self.run_id, {"web.search": False}, evidence="synthetic complete host inventory")
        self.assertAllowed(self.stop(stop_hook_active=True))

    def test_three_atomic_continuations_survive_rebind_versions_and_new_continuation_turn_ids(self):
        self.bind()
        first = self.stop()
        self.production.capabilities(self.run_id, {"web.search": True}, evidence="synthetic inventory")
        self.bind()
        self.assertAllowed(self.stop(hook_event_name="UserPromptSubmit", prompt=first["reason"], turn_id="auto-2"))
        second = self.stop(turn_id="auto-2", stop_hook_active=True)
        third = self.stop(turn_id="auto-3", stop_hook_active=True)
        self.assertIn("1/3", first["reason"])
        self.assertIn("2/3", second["reason"])
        self.assertIn("3/3", third["reason"])
        self.assertAllowed(self.stop(turn_id="auto-4", stop_hook_active=True))
        self.bind()
        self.assertAllowed(self.stop(turn_id="auto-5", stop_hook_active=True))

    def test_concurrent_stops_cannot_exceed_retry_budget(self):
        self.bind()
        with ThreadPoolExecutor(max_workers=6) as workers:
            results = list(workers.map(lambda _: self.stop(), range(8)))
        self.assertEqual(sum(result.get("decision") == "block" for result in results), MAX_CONTINUATIONS)

    def test_prompt_redelivery_cannot_reset_the_bounded_chain(self):
        prompt = self.event(hook_event_name="UserPromptSubmit", prompt="Find a story")
        decide(prompt, self.project)
        self.bind()
        first = self.stop()
        self.stop(hook_event_name="UserPromptSubmit", prompt=first["reason"], turn_id="continuation")
        decide(prompt, self.project)
        self.assertIn("2/3", self.stop(turn_id="continuation", stop_hook_active=True)["reason"])

    def test_rebind_racing_interruption_does_not_restart_interrupted_turn(self):
        self.bind()
        self.stop(hook_event_name="Interrupt")
        self.bind()
        self.assertAllowed(self.stop())

    def test_interrupt_during_store_read_wins_without_waiting_for_the_read(self):
        from ytvideos.session_guard import _read_run
        self.bind()
        reading, proceed = threading.Event(), threading.Event()
        def delayed(binding):
            reading.set()
            self.assertTrue(proceed.wait(timeout=3))
            return _read_run(binding)
        with patch("ytvideos.session_guard._read_run", side_effect=delayed), ThreadPoolExecutor(max_workers=1) as workers:
            result = workers.submit(self.stop)
            self.assertTrue(reading.wait(timeout=3))
            self.assertAllowed(self.stop(hook_event_name="Interrupt"))
            proceed.set()
            self.assertAllowed(result.result(timeout=3))

    def test_new_user_prompt_detaches_old_run_and_explicit_resume_rearms_new_scope(self):
        self.bind()
        self.stop()
        self.assertAllowed(self.stop(hook_event_name="UserPromptSubmit", turn_id="maintenance-turn", prompt="Check repository tests"))
        self.assertAllowed(self.stop(turn_id="maintenance-turn"))
        dispatch(self.production, parser().parse_args(["resume", "--run", self.run_id]))
        self.assertIn("1/3", self.stop(turn_id="maintenance-turn")["reason"])

    def test_interrupt_detaches_without_restart_and_new_turn_without_scope_does_not_resume(self):
        self.bind()
        self.stop()
        self.assertAllowed(self.stop(hook_event_name="Interrupt"))
        self.assertAllowed(self.stop(stop_hook_active=True))
        self.bind()
        self.assertAllowed(self.stop(turn_id="different-user-turn"))

    def test_subagent_uses_its_own_binding_not_parent(self):
        self.bind()
        other = self.production.create("test_channel", "Other assigned task")
        bind_session(self.production, other["id"], "assigned-agent")
        result = self.stop(hook_event_name="SubagentStop", agent_id="assigned-agent")
        self.assertIn(other["id"], result["reason"])
        self.assertNotIn(self.run_id, result["reason"])

    def test_cancelled_unknown_blocked_attempt_exhaustion_and_pin_drift_allow_stop(self):
        self.bind()
        self.mutate(lambda run: run["tasks"]["research"].update(attempt=run["budget"]["max_task_attempts"]))
        self.assertAllowed(self.stop())
        for status in ("blocked", "unknown"):
            self.mutate(lambda run: run["tasks"]["research"].update(status=status, attempt=0, blocker="observed failure"))
            self.assertAllowed(self.stop())
        self.mutate(lambda run: run["tasks"]["research"].update(status="pending", blocker=None))
        (self.project / "src" / "ytvideos" / "pin.py").write_text("# changed code\n")
        self.assertAllowed(self.stop())
        self.production.cancel(self.run_id, "explicit test cancellation")
        self.assertAllowed(self.stop())

    def test_exhausted_paid_budget_does_not_stop_independent_editorial_work(self):
        self.run_id, _ = self.fixture.make_run(count=1, billing="metered")
        self.production.capabilities(self.run_id, {"audio.produce": False, "audio.listen": False, "model.text": False},
                                     evidence="synthetic observed unavailable tools")
        self.mutate(lambda run: (run["tasks"]["research"].update(status="complete"),
                                 run["budget"].update(max_paid_units=0)))
        self.bind()
        self.assertAllowed(self.stop())
        self.production.capabilities(self.run_id, {"model.text": True}, evidence="synthetic available editorial model")
        self.assertIn("packaging: read_context_then_claim", self.stop()["reason"])

    def test_script_gate_and_verified_mp4_boundary_allow_stop_without_release_authorization(self):
        self.bind()
        source = self.fixture.root / "script.txt"
        source.write_text("Synthetic script artifact for state boundary testing.")
        artifact = self.production.artifacts.put(source, "script")
        def script_gate(run):
            run["artifacts"][artifact["id"]] = artifact
            for task in ("research", "script"):
                run["tasks"][task].update(status="complete", outputs=[artifact["id"]])
        self.mutate(script_gate)
        self.assertIn("awaiting_script_approval", self.stop()["systemMessage"])
        def mp4_gate(run):
            # Synthetic state setup only: real approval signatures are tested separately.
            run["approvals"]["script"] = {"artifact_id": artifact["id"], "revision": run["revision"]}
            run["tasks"]["review"]["status"] = "complete"
            run["tasks"]["render"].update(status="complete", outputs=[artifact["id"]])
        self.mutate(mp4_gate)
        self.assertIn("awaiting_mp4_approval", self.stop()["systemMessage"])
        self.mutate(lambda run: run["approvals"].update({"mp4": {"artifact_id": artifact["id"], "revision": run["revision"]}}))
        self.assertIn("release needs", self.stop()["systemMessage"])

    def test_cli_claim_tracks_owned_token_without_restarting_foreign_lease(self):
        self.bind()
        self.production.capabilities(self.run_id, {"web.search": True}, evidence="synthetic tool")
        claim = dispatch(self.production, parser().parse_args(["claim", "--run", self.run_id, "--task", "research", "--worker", "arbitrary-author-name"]))
        self.assertIn("Continue your existing research lease", self.stop()["reason"])
        self.assertNotIn(claim["token"], self.stop(stop_hook_active=True)["reason"])
        bind_session(self.production, self.run_id, "foreign-coordinator")
        self.assertAllowed(self.stop(session_id="foreign-coordinator"))
        self.mutate(lambda run: run["tasks"]["research"]["claim"].update(expires_at=0))
        self.assertIn("lease expired", self.stop(stop_hook_active=True)["reason"])

    def test_missing_store_is_not_created_and_missing_session_is_not_faked(self):
        with patch.dict(os.environ, {"CODEX_THREAD_ID": ""}):
            self.assertFalse(self.bind()["bound"])
        self.bind()
        Path(self.fixture.db).unlink()
        self.assertAllowed(self.stop())
        self.assertFalse(Path(self.fixture.db).exists())

    def test_explicit_host_id_tracks_only_its_actual_claim_and_claim_does_not_bind(self):
        bind_session(self.production, self.run_id, "explicit-other-host")
        self.production.capabilities(self.run_id, {"web.search": True}, evidence="synthetic tool")
        dispatch(self.production, parser().parse_args(["claim", "--run", self.run_id, "--task", "research",
                                                      "--worker", "author", "--session-id", "explicit-other-host"]))
        self.assertIn("Continue your existing", self.stop(session_id="explicit-other-host")["reason"])
        self.assertAllowed(self.stop())

    def test_driver_error_is_redacted_in_direct_decide_api(self):
        self.bind()
        with patch("ytvideos.session_guard._read_run", side_effect=RuntimeError("dsn_password=do-not-leak")):
            result = self.stop()
        self.assertAllowed(result)
        self.assertIn("RuntimeError", result["systemMessage"])
        self.assertNotIn("do-not-leak", canonical(result))

    def test_registry_failure_preserves_started_run_and_committed_claim_token(self):
        with patch("ytvideos.session_guard._registry", side_effect=OSError("private detail")):
            started = dispatch(self.production, parser().parse_args(["start", "--channel", "test_channel", "--intent", "new draft"]))
        self.assertFalse(started["session_guard"]["bound"])
        self.assertNotIn("private detail", canonical(started["session_guard"]))
        self.production.capabilities(self.run_id, {"web.search": True}, evidence="synthetic tool")
        with patch("ytvideos.session_guard.record_claim", side_effect=OSError("private detail")):
            claim = dispatch(self.production, parser().parse_args(["claim", "--run", self.run_id, "--task", "research", "--worker", "author"]))
        self.assertEqual(claim["token"], self.production.store.get(self.run_id)["tasks"]["research"]["claim"]["token"])
        self.assertIn("context", claim)
        self.assertNotIn("private detail", canonical(claim["session_guard"]))

    def test_postgres_binding_contains_only_reference_digest_and_changed_env_cannot_connect(self):
        location = "postgresql://test_user:do-not-leak-password@invalid.test/example"
        with patch.object(self.production.store, "location", location), patch.object(self.production.store, "postgres", True), patch.object(self.production.store, "get", return_value=self.run), patch.dict(os.environ, {"YTV_DATABASE_URL": location}):
            self.assertTrue(self.bind()["inspection_ready"])
        with sqlite3.connect(registry_path(self.project)) as connection:
            stored = connection.execute("SELECT doc FROM sessions").fetchone()[0]
        self.assertNotIn(location, stored)
        self.assertNotIn("do-not-leak-password", stored)
        result = self.stop()
        self.assertAllowed(result)
        self.assertNotIn("do-not-leak-password", canonical(result))

    def test_hook_command_quotes_git_root_and_runs_offline_from_subdirectory(self):
        root = Path(__file__).resolve().parents[1]
        configuration = json.loads((root / ".codex" / "hooks.json").read_text())
        commands = {item["command"] for entries in configuration["hooks"].values()
                    for entry in entries for item in entry["hooks"]}
        self.assertEqual(len(commands), 1)
        command = commands.pop()
        self.assertIn("--offline --no-sync", command)
        strange = self.fixture.root / "git root with ' quote $dollar ; semicolon"
        (strange / "nested").mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(strange)], check=True, capture_output=True)
        (strange / ".codex" / "hooks").mkdir(parents=True)
        shutil.copyfile(root / ".codex" / "hooks" / "entrypoint.py", strange / ".codex" / "hooks" / "entrypoint.py")
        tools = self.fixture.root / "tools"
        tools.mkdir()
        uv = tools / "uv"
        uv.write_text("#!/usr/bin/env python3\nimport json, sys\nprint(json.dumps(sys.argv[1:]))\n")
        uv.chmod(0o755)
        result = subprocess.run(["sh", "-c", command], cwd=strange / "nested", capture_output=True, text=True,
                                env={**os.environ, "PATH": str(tools) + os.pathsep + os.environ["PATH"]}, check=True)
        arguments = json.loads(result.stdout)
        self.assertEqual(arguments[arguments.index("--project") + 1], str(strange.resolve()))
        self.assertEqual(arguments[-1], str(strange.resolve() / ".codex" / "hooks" / "entrypoint.py"))


@unittest.skipUnless(os.environ.get("YTV_TEST_POSTGRES_URL"), "requires PostgreSQL integration database")
class PostgresSessionGuardTests(unittest.TestCase):
    def test_actual_read_only_store_inspection_and_bounded_error_redaction(self):
        from ytvideos.session_guard import _read_run
        fixture = fixtures.PoolServiceTests()
        fixture.postgres = True
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        production = fixture.production
        run = production.create("test_channel", "A PostgreSQL bound run")
        with patch.dict(os.environ, {"YTV_DATABASE_URL": fixture.db}):
            bind_session(production, run["id"], "pg-writer")
            with sqlite3.connect(registry_path(production.project)) as connection:
                binding = json.loads(connection.execute("SELECT doc FROM sessions").fetchone()[0])["binding"]
            before = fixture.store.get(run["id"])
            self.assertEqual(_read_run(binding), before)
            event = {"hook_event_name": "Stop", "session_id": "pg-writer", "turn_id": "turn",
                     "cwd": str(production.project)}
            result = decide(event, production.project)
            self.assertEqual(result["decision"], "block")
            self.assertNotIn(fixture.db, result["reason"])
            self.assertEqual(fixture.store.get(run["id"]), before)


if __name__ == "__main__":
    unittest.main()

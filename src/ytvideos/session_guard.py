"""Bounded host continuation, scoped to an explicitly started/resumed run.

Thread IDs are correlation labels, not authority. This hook reads workflow state;
it never claims work, grants approval, invokes a provider, or changes hook trust.
"""
from contextlib import closing, contextmanager
import json
import os
from pathlib import Path
import shlex
import sqlite3

from .errors import WorkflowError
from .service import Production
from .util import canonical, digest
from .workflow import valid_approval

MAX_CONTINUATIONS = 3


def registry_path(project):
    return Path(project).resolve() / ".ytvideos" / "session-guard.sqlite3"


@contextmanager
def _registry(project):
    path = registry_path(project)
    if path.is_symlink() or path.parent.is_symlink():
        raise WorkflowError("session guard registry must stay in its owned project workspace")
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path, timeout=2, isolation_level=None)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            connection.execute("CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, doc TEXT NOT NULL)")
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise


def _load(connection, session):
    row = connection.execute("SELECT doc FROM sessions WHERE id=?", (session,)).fetchone()
    return json.loads(row[0]) if row else {"binding": None, "turn": None, "user_turn": None, "count": 0, "reason": None}


def _save(connection, session, state):
    connection.execute("INSERT INTO sessions VALUES (?,?) ON CONFLICT(id) DO UPDATE SET doc=excluded.doc",
                       (session, canonical(state)))


def _database(production):
    location = production.store.location
    if production.store.postgres:
        return {"backend": "postgresql", "sha256": digest(location),
                "env": "YTV_DATABASE_URL" if os.environ.get("YTV_DATABASE_URL") == location else None}
    return {"backend": "sqlite", "path": str(Path(location).resolve())}


def bind_session(production, run_id, session_id=None):
    session = session_id if session_id is not None else os.environ.get("CODEX_THREAD_ID")
    if not isinstance(session, str) or not session.strip() or "\x00" in session:
        return {"bound": False, "reason": "No host session ID; Stop guard is not bound."}
    production.store.get(run_id)  # Never bind a guessed run or select a newest run.
    database = _database(production)
    binding = {"run_id": run_id, "project": str(production.project), "workspace": str(production.workspace),
               "database": database, "claims": {}}
    try:
        with _registry(production.project) as connection:
            state = _load(connection, session)
            previous = state.get("binding")
            if previous and all(previous.get(key) == binding[key] for key in ("run_id", "project", "workspace", "database")):
                binding["claims"] = previous.get("claims", {})
            state["binding"] = binding  # Rebinding/revisions cannot reset the continuation counter.
            _save(connection, session, state)
    except Exception as exc:
        return {"bound": False, "run_id": run_id, "reason": f"Session registry unavailable ({type(exc).__name__})."}
    return {"bound": True, "run_id": run_id, "session_id": session, "worker_id": session,
            "max_continuations": MAX_CONTINUATIONS,
            "inspection_ready": database["backend"] == "sqlite" or database["env"] is not None,
            "activation": "Requires the exact project hooks to be trusted in the local host /hooks."}


def record_claim(production, run_id, task_id, claim, session_id=None):
    """Remember a CLI-issued lease only for an already bound originating session."""
    session = session_id if session_id is not None else os.environ.get("CODEX_THREAD_ID")
    if not session or not registry_path(production.project).is_file():
        return
    with _registry(production.project) as connection:
        state = _load(connection, session)
        binding = state.get("binding")
        if (binding and (binding["run_id"], binding["workspace"], binding["database"])
                == (run_id, str(production.workspace), _database(production))):
            binding["claims"][task_id] = claim["token"]
            _save(connection, session, state)


def _read_run(binding):
    """No Store constructor: it initializes/migrates and takes write locks."""
    database = binding["database"]
    if database["backend"] == "postgresql":
        location = os.environ.get(database.get("env") or "")
        if not location or digest(location) != database["sha256"]:
            raise WorkflowError("bound PostgreSQL environment reference is absent or changed")
        import psycopg
        with psycopg.connect(location, connect_timeout=3) as connection:
            connection.read_only = True
            connection.execute("SET LOCAL statement_timeout = '1500ms'")
            row = connection.execute("SELECT version,doc FROM runs WHERE id=%s", (binding["run_id"],)).fetchone()
    else:
        uri = Path(database["path"]).as_uri() + "?mode=ro"
        with closing(sqlite3.connect(uri, uri=True, timeout=1)) as connection:
            row = connection.execute("SELECT version,doc FROM runs WHERE id=?", (binding["run_id"],)).fetchone()
    if row is None:
        raise WorkflowError("bound run is absent in its exact store")
    run = json.loads(row[1])
    run["version"] = row[0]
    if run["id"] != binding["run_id"]:
        raise WorkflowError("bound run identity differs from stored state")
    return run


def _command(binding, *arguments):
    database = binding["database"]
    # PostgreSQL resolves the verified environment reference; never echo its DSN.
    database_args = ["--db", database["path"]] if database["backend"] == "sqlite" else []
    return shlex.join(["uv", "run", "--no-sync", "--project", binding["project"], "ytv",
                       "--project-root", binding["project"], "--workspace", binding["workspace"],
                       *database_args, *arguments])


def _next_action(production, run, binding, session):
    if run["status"] in {"cancelled", "scheduled"}:
        return None, run["status"]
    production._runtime(run)  # Preserve existing code/context pins; never auto-migrate.
    current = production._next_state(run)
    if current["approval_requests"]:
        return None, current["status"]
    if run["tasks"]["review"]["status"] == "complete":
        return None, "verified MP4 boundary; release needs its own explicit user instruction"
    for task in current["tasks"]:
        saved = run["tasks"][task["id"]]
        if (task["production_blocker"] or saved["attempt"] >= run["budget"]["max_task_attempts"]
                or any(item["state"] == "unavailable" for item in task["capability_checks"])):
            continue
        provider_caps = {"audio.produce", "image.generate", "media.licensed_clip"} & set(saved["capabilities"])
        allowance = run["budget"].get("task_allowances", {}).get("audio", 0) if task["id"] == "audio" else 0
        available_budget = run["budget"]["max_paid_units"] + allowance - sum(run["budget"][key]
                                                                 for key in ("spent", "reserved", "unknown_reserved"))
        if (provider_caps and task["dispatchable"] and available_budget <= 0
                and any(run["capabilities"].get(cap, {}).get("billing") != "included" for cap in provider_caps)):
            continue
        command = _command(binding, *task["next_action"]["context_command"])
        return (f"{task['id']}: {task['next_action']['kind']}. Read the pinned task/skill/requirements: {command}. "
                "Inspect unobserved host tools and record actual evidence, then claim/complete the task. "
                "Missing observations are not confirmed blockers."), None
    def owned(task):
        claim = task.get("claim") or {}
        return claim.get("worker") == session or (claim.get("token") is not None
                and binding["claims"].get(task["id"]) == claim["token"])
    running = [task for task in run["tasks"].values() if task["status"] == "running"]
    for task in running:
        if not owned(task):
            continue
        if task["claim"]["expires_at"] > production.clock():
            return (f"Continue your existing {task['id']} lease; wait/read back its recorded tool or provider handle "
                    "and complete with actual evidence. Do not create a second claim or repeat an UNKNOWN operation."), None
        if not any(other["claim"]["expires_at"] <= production.clock() and not owned(other) for other in running):
            return (f"Your {task['id']} lease expired. Inspect its recorded operations, then "
                    f"{_command(binding, 'resume', '--run', run['id'])}; reconcile UNKNOWN before any retry."), None
    return None, "no ready work within observed capabilities/budget; respect blockers, UNKNOWN and foreign leases"


def decide(event, project_root):
    """Return only the documented hook output shape; all allow reasons are explicit."""
    project = Path(project_root).resolve()
    kind = event.get("hook_event_name")
    session = event.get("agent_id") if kind == "SubagentStop" else event.get("session_id")
    def allow(reason):
        return {"systemMessage": "ytvideos session guard: " + reason}
    if kind not in {"Stop", "SubagentStop", "Interrupt", "UserPromptSubmit"}:
        return allow("event has no continuation action")
    if not isinstance(session, str) or not session or not event.get("cwd"):
        return allow("missing session/cwd; no run selected")
    if not Path(event["cwd"]).resolve().is_relative_to(project):
        return allow("event belongs to a different project; no run selected")
    if not registry_path(project).is_file() and kind != "UserPromptSubmit":
        return allow("session is unbound; no run selected")
    try:
        with _registry(project) as connection:
            state = _load(connection, session)
            if kind == "Interrupt":
                state["binding"] = None
                state["interrupted"] = True
                _save(connection, session, state)
                return allow("interruption honored; no restart")
            if kind == "UserPromptSubmit":
                # An exact guard-produced prompt continues the same bounded chain.
                if not state["reason"] or event.get("prompt") != state["reason"]:
                    if event.get("turn_id") and event["turn_id"] in {state["turn"], state.get("user_turn")}:
                        return allow("prompt redelivery preserved existing scope and continuation count")
                    state = {"binding": None, "count": 0, "reason": None,
                             "turn": event.get("turn_id"), "user_turn": event.get("turn_id")}
                else:
                    state["turn"] = event.get("turn_id")
                _save(connection, session, state)
                return allow("prompt scope recorded; only start/resume binds production")
            binding = state.get("binding")
            if not binding or state.get("interrupted"):
                return allow("session is unbound; no run selected")
            if (state["turn"] and state["turn"] != event.get("turn_id") and not event.get("stop_hook_active")):
                state["binding"] = None
                _save(connection, session, state)
                return allow("new turn without an observed production binding; no restart")
            if state["count"] >= MAX_CONTINUATIONS:
                return allow("continuation budget exhausted; report unfinished run " + binding["run_id"])
            scope = state.get("user_turn") or event.get("turn_id")
        # Do not hold the registry lock during store I/O: Interrupt must detach
        # promptly, including while a PostgreSQL read is timing out.
        if binding["project"] != str(project) or not (Path(binding["workspace"]) / "artifacts").is_dir():
            raise WorkflowError("bound project/workspace is unavailable")
        run = _read_run(binding)
        production = Production(None, binding["workspace"], project)
        action, stopped = _next_action(production, run, binding, session)
        if action is None:
            return allow(f"run {run['id']}: {stopped}")
        completion = ("completed research/script with independent review and awaiting_script_approval"
                      if not valid_approval(run, "script") else "completed video review and awaiting_mp4_approval")
        with _registry(project) as connection:
            state = _load(connection, session)
            if (state.get("binding") != binding or state.get("interrupted")
                    or state.get("user_turn") not in {None, scope}):
                return allow("scope changed during inspection; no restart")
            if state["count"] >= MAX_CONTINUATIONS:
                return allow("continuation budget exhausted; report unfinished run " + binding["run_id"])
            state["count"] += 1
            state["user_turn"] = state.get("user_turn") or event.get("turn_id")
            state["turn"] = event.get("turn_id") or state["turn"]
            reason = (f"ytvideos run {run['id']} is unfinished (version {run['version']}). "
                      f"Required completion: {completion}, or a confirmed blocker. Next action: {action} "
                      f"Continue within existing permissions/budget; no approval or publication is granted. "
                      f"Continuation {state['count']}/{MAX_CONTINUATIONS}.")
            state["reason"] = reason
            _save(connection, session, state)
            return {"decision": "block", "reason": reason}
    except WorkflowError as exc:
        return allow(f"inspection unavailable: {exc}; no restart")
    except Exception as exc:
        # Driver/DSN/paths may contain secrets. The hook report must not echo them.
        return allow(f"inspection unavailable ({type(exc).__name__}); inspect the exact bound store/pins; no restart")


def main(project_root):
    import sys
    try:
        result = decide(json.load(sys.stdin), project_root)
    except Exception as exc:
        result = {"systemMessage": f"ytvideos session guard: inspection unavailable ({type(exc).__name__}); no restart"}
    print(json.dumps(result, ensure_ascii=False))

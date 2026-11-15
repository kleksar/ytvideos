"""Import an owner-selected exact source into the existing script approval gate.

This trusted-coordinator action is not an editorial review. It neither writes
reviewer evidence nor calls providers; all downstream production guards remain.
"""
import argparse
import copy
import json
import os
from pathlib import Path
import re
import sys

from .errors import Conflict, WorkflowError
from .media_script import read_script
from .util import digest, require_text, utc_now
from .workflow import configure_speech_tasks


def accept_source(production, run_id, *, revision, sha256, source, message, origin, preproduction=None):
    """Bind a real production instruction to immutable source bytes, atomically.

    A topic or a file alone is not permission. The local coordinator must supply
    the actual owner message and its stable reference, just as for approve_local.
    A blocked/running attempt must be resolved using normal recovery first.
    """
    if production.approvals.public_key:
        raise WorkflowError("this host uses signed approvals; source import requires its trusted signed ingress")
    if type(revision) is not int or revision < 1:
        raise WorkflowError("source approval requires the positive revision shown to the user")
    if not isinstance(sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", sha256):
        raise WorkflowError("source approval requires the exact source SHA-256")
    require_text(source, "source reference to the actual user decision")
    require_text(message, "actual user production instruction")
    require_text(origin, "immutable source location, such as PR commit and script path")
    event_id = "local-approval:" + digest(source)
    prepared = production.artifacts.put(preproduction, "source_preproduction") if preproduction is not None else None

    def change(tx, run):
        production._runtime(run)
        if run["revision"] != revision:
            raise Conflict("source approval targets an earlier or different revision")
        original = run["artifacts"].get(run.get("source_script_id"))
        if original is None:
            raise WorkflowError("no pinned source script; supply the selected exact text through start --source-script")
        if original["sha256"] != sha256 or run["pins"].get("source_script") != sha256:
            raise Conflict("source approval must match the pinned source script, not a rewritten draft")
        path = production.artifacts.resolve(original)
        parsed = read_script(path, run["profile"], run["format"])
        if prepared:
            from .preproduction import read_package, validate_package
            validate_package(read_package(production.artifacts.resolve(prepared)),
                             script=path.read_bytes().decode("utf-8"), profile=run["profile"], format=run["format"])
        artifact = production.artifacts.put(path, "script")
        prior = tx.execute("SELECT payload FROM events WHERE id=?", (event_id,)).fetchone()
        event = {"event_id": event_id, "actor": "local-owner", "source": source,
                 "run_id": run_id, "kind": "script", "artifact_id": artifact["id"], "sha256": sha256,
                 "revision": revision, "created_at": json.loads(prior[0])["created_at"] if prior else utc_now(),
                 "message": message, "scope": "produce_video", "authority": "local_session",
                 "source_input": {"artifact_id": original["id"], "origin": origin}}
        if prepared:
            event["source_input"]["preproduction_sha256"] = prepared["sha256"]
        if prior:
            if run.get("source_preproduction_id"):
                saved_plan = run["artifacts"][run["source_preproduction_id"]]
                production.artifacts.resolve(saved_plan)
                if not prepared or saved_plan["sha256"] != prepared["sha256"]:
                    raise Conflict("source acceptance already binds a different preproduction package")
            if json.loads(prior[0]) != event:
                raise Conflict("user decision was already bound to different content")
            return production._approve_event(tx, run, event)

        script = run["tasks"]["script"]
        research = run["tasks"]["research"]
        if script["status"] != "pending" or script.get("outputs"):
            raise Conflict("source import requires a pending script; resolve blocked work or use normal approval for a completed script")
        if research["status"] not in {"pending", "complete"}:
            raise Conflict("resolve the research blocker or active attempt before source import")
        if any(task.get("claim") or task["status"] in {"running", "unknown", "blocked"}
               for task in run["tasks"].values()):
            raise Conflict("resolve active leases, unknown outcomes and blockers before source import")
        if any(task["status"] != "pending" or task.get("outputs")
               for key, task in run["tasks"].items() if key not in {"research", "script"}):
            raise Conflict("production has already started; do not replace its accepted script")
        if run["approvals"]:
            raise Conflict("run already has an approval; preserve it or revise explicitly")
        if tx.execute("SELECT key FROM operations WHERE run_id=?", (run_id,)).fetchone():
            raise Conflict("run has external operations; reconcile rather than importing over production")

        previous = {"research": copy.deepcopy(research), "script": copy.deepcopy(script)}
        if research["status"] == "pending":
            research.update(status="skipped", blocker=None)
            research["skip_reason"] = "owner selected a complete source; no new topic research requested"
            script["dependencies"] = []
        if prepared:
            run["artifacts"][prepared["id"]] = prepared
            run["source_preproduction_id"] = prepared["id"]
            run["pins"]["source_preproduction"] = prepared["sha256"]
        run["artifacts"][artifact["id"]] = artifact
        script.update(status="complete", outputs=[artifact["id"]], claim=None, blocker=None,
                      receipt=None, completed_at=utc_now())
        script["source_import"] = {"source_artifact_id": original["id"], "approval_event_id": event_id,
                                   "origin": origin, "review_performed": False}
        configure_speech_tasks(run, parsed["mode"])
        approval = production._approve_event(tx, run, event)
        tx.event("source-import:" + digest(event_id), run_id, "script.source_imported",
                 {"source_artifact": original, "script_artifact": artifact, "origin": origin,
                  "approval_event_id": event_id, "previous_tasks": previous,
                  "review_performed": False, "providers_called": False})
        return approval

    return production.store.mutate(run_id, change)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Accept an exact owner-selected source; no editorial review or media generation.")
    parser.add_argument("--db", default=os.environ.get("YTV_DATABASE_URL", ".ytvideos/state.sqlite3"))
    parser.add_argument("--workspace", default=os.environ.get("YTV_WORKSPACE", ".ytvideos"))
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--run", required=True)
    parser.add_argument("--revision", required=True, type=int)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--origin", required=True)
    parser.add_argument("--preproduction", type=Path,
                        help="Optional exact textual handoff for this source; copied and pinned, never auto-completed")
    args = parser.parse_args(argv)
    from .service import Production
    from .store import Store
    try:
        production = Production(Store(args.db), args.workspace, args.project_root,
                                approval_public_key=os.environ.get("YTV_APPROVAL_PUBLIC_KEY"))
        approval = accept_source(production, args.run, revision=args.revision, sha256=args.sha256,
                                 source=args.source, message=args.message, origin=args.origin, preproduction=args.preproduction)
        print(json.dumps({"approval": approval, "next": production.next(args.run),
                          "review_performed": False, "providers_called": False}, ensure_ascii=False))
    except (WorkflowError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

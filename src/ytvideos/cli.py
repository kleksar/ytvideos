"""Small JSON CLI used by the host application and the seven project skills."""
import argparse
import json
import os
import sys
from pathlib import Path

from .doctor import inspect
from .errors import WorkflowError
from .profiles import inspect_profiles
from .service import Production
from .store import Store


def read_json(path):
    return json.loads(Path(path).read_text())


def parser():
    cli = argparse.ArgumentParser(description="Channel-independent video production. All results are JSON.")
    cli.add_argument("--db", default=os.environ.get("YTV_DATABASE_URL", ".ytvideos/state.sqlite3"))
    cli.add_argument("--workspace", default=os.environ.get("YTV_WORKSPACE", ".ytvideos"))
    cli.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[2])
    cli.add_argument("--profiles", type=Path)
    sub = cli.add_subparsers(dest="command", required=True)
    profiles = sub.add_parser("profiles", help="Inspect all channel/format requirements before creating a run")
    profiles.add_argument("--channel")
    profiles.add_argument("--format", choices=("short", "long"))
    create = sub.add_parser("start", aliases=["create"],
                            help="Start a new story/video with its saved plan and first pinned reading packet")
    create.add_argument("--channel", default="paper_detour")
    create.add_argument("--intent", required=True)
    create.add_argument("--format", choices=("short", "long"), default="short")
    create.add_argument("--request-id", help="Stable ID for a retried incoming user request")
    create.add_argument("--budget-units", type=int)
    create.add_argument("--source-script", type=Path,
                        help="Preserve supplied full narration or licensed edit-script bytes; does not invent approval")
    create.add_argument("--session-id", help="Explicit host correlation ID; default CODEX_THREAD_ID (not approval)")
    cross = sub.add_parser("cross-promotion-plan", help="Read-only plan for Shorts links, posts, end screens and playlists")
    cross.add_argument("--release-spec", type=Path, required=True)
    cross.add_argument("--inventory", type=Path, required=True)
    cross.add_argument("--video-id", required=True)
    sub.add_parser("list", help="Show all runs without loading their creative histories")
    for name in ("status", "next", "plan", "resume", "export", "events", "deferred-actions"):
        command = sub.add_parser(name)
        command.add_argument("--run", required=True)
        if name == "resume":
            command.add_argument("--session-id", help="Explicit host correlation ID; default CODEX_THREAD_ID")
    context = sub.add_parser("context")
    context.add_argument("--run", required=True)
    context.add_argument("--task", required=True)
    context.add_argument("--output", type=Path, help="Optionally write the packet for an independent session")
    claim = sub.add_parser("claim")
    claim.add_argument("--run", required=True)
    claim.add_argument("--task", required=True)
    claim.add_argument("--worker", required=True)
    claim.add_argument("--session-id", help="Existing host binding for lease tracking; default CODEX_THREAD_ID")
    claim.add_argument("--lease-seconds", type=int, default=900)
    claim.add_argument("--estimated-units", type=int, default=0)
    heartbeat = sub.add_parser("heartbeat")
    heartbeat.add_argument("--run", required=True)
    heartbeat.add_argument("--task", required=True)
    heartbeat.add_argument("--token", required=True)
    heartbeat.add_argument("--lease-seconds", type=int, default=900)
    complete = sub.add_parser("complete")
    complete.add_argument("--run", required=True)
    complete.add_argument("--task", required=True)
    complete.add_argument("--token", required=True)
    complete.add_argument("--output", required=True, type=Path)
    complete.add_argument("--receipt", required=True, type=Path)
    complete.add_argument("--actual-units", type=int, help="Measured cost; omission retains the reservation as unknown")
    approval = sub.add_parser("approve", help="Ingest a signed event from the trusted user-event bridge")
    approval.add_argument("--event", required=True, type=Path)
    caps = sub.add_parser("capabilities")
    caps.add_argument("--run", required=True)
    caps.add_argument("--file", required=True, type=Path, help="JSON mapping of actually observed capability -> boolean")
    caps.add_argument("--evidence", required=True)
    doctor = sub.add_parser("doctor")
    doctor.add_argument("--run")
    fail = sub.add_parser("fail")
    fail.add_argument("--run", required=True)
    fail.add_argument("--task", required=True)
    fail.add_argument("--token", required=True)
    fail.add_argument("--reason", required=True)
    fail.add_argument("--known-not-sent", action="store_true")
    for name in ("unblock", "revise"):
        command = sub.add_parser(name)
        command.add_argument("--run", required=True)
        command.add_argument("--task", required=True)
        command.add_argument("--reason", required=True)
    cancel = sub.add_parser("cancel")
    cancel.add_argument("--run", required=True)
    cancel.add_argument("--reason", required=True)
    settle = sub.add_parser("settle-cancelled")
    settle.add_argument("--run", required=True)
    settle.add_argument("--task", required=True)
    settle.add_argument("--evidence", required=True)
    settle.add_argument("--actual-units", type=int)
    release = sub.add_parser("prepare-release")
    release.add_argument("--run", required=True)
    release.add_argument("--spec", required=True, type=Path)
    release.add_argument("--asset", action="append", default=[], type=Path,
                         help="Import an exact thumbnail/caption/A-B asset named by the spec hash")
    operation = sub.add_parser("begin-operation", help="Commit dispatch intent; the returned permit is single-use")
    operation.add_argument("--run", required=True)
    operation.add_argument("--task", required=True)
    operation.add_argument("--token", required=True)
    operation.add_argument("--action", required=True)
    operation.add_argument("--payload", required=True, type=Path)
    payload = sub.add_parser("operation-payload")
    payload.add_argument("--run", required=True)
    payload.add_argument("--task", required=True)
    payload.add_argument("--action", required=True)
    media = sub.add_parser("execute-media")
    media.add_argument("--run", required=True)
    media.add_argument("--task", required=True)
    media.add_argument("--token", required=True)
    media.add_argument("--request", required=True, type=Path)
    pool = sub.add_parser("pool")
    pool.add_argument("action", choices=("initialize", "configure-review-limit", "enqueue", "tick", "pending", "claim", "submitted", "result", "accept", "reconcile", "recover", "status", "cancel"))
    pool.add_argument("--run", required=True)
    pool.add_argument("--payload", type=Path)
    pool.add_argument("--expected-version", type=int)
    candidates = sub.add_parser("pool-candidates")
    candidates.add_argument("--runtime", required=True)
    candidates.add_argument("--estimated-units", type=int, default=0)
    observe = sub.add_parser("observe-operation")
    observe.add_argument("--run", required=True)
    observe.add_argument("--key", required=True)
    observe.add_argument("--status", required=True, choices=("confirmed", "not_performed", "unknown"))
    observe.add_argument("--receipt", required=True, type=Path)
    observe.add_argument("--event-id", required=True)
    reconcile = sub.add_parser("reconcile-task")
    reconcile.add_argument("--run", required=True)
    reconcile.add_argument("--task", required=True)
    reconcile.add_argument("--worker", required=True)
    reconcile.add_argument("--outcome", choices=("completed", "not_performed", "continue"), required=True)
    reconcile.add_argument("--evidence", required=True)
    import_ = sub.add_parser("import-legacy", help="Import identified source evidence; never infer approvals from prose")
    import_.add_argument("--bundle", required=True, type=Path)
    attach = sub.add_parser("attach-artifact")
    attach.add_argument("--run", required=True)
    attach.add_argument("--file", required=True, type=Path)
    attach.add_argument("--kind", required=True)
    attach.add_argument("--source", required=True)
    attach.add_argument("--expected-sha256")
    thumbnail = sub.add_parser("add-thumbnail-task")
    thumbnail.add_argument("--run", required=True)
    thumbnail.add_argument("--brief", required=True, type=Path)
    return cli


def dispatch(service, args):
    command = args.command
    if command in {"start", "create"}:
        run = service.create(args.channel, args.intent, format=args.format, request_id=args.request_id,
                             profiles=args.profiles, budget_units=args.budget_units, source_script=args.source_script)
        if command == "start":
            from .entry import start_packet
            return start_packet(service, run["id"], session_id=args.session_id)
        return {"run_id": run["id"], "pins": run["pins"], "next": service.next(run["id"]),
                "plan": service.plan(run["id"])}
    if command == "list":
        return [{"run_id": r["id"], "channel": r["channel"], "status": r["status"], "intent": r["intent"]}
                for r in service.store.list()]
    if command in {"next", "status"}:
        return service.next(args.run)
    if command == "resume":
        from .session_guard import bind_session
        result = service.resume(args.run)
        return {**result, "session_guard": bind_session(service, args.run, args.session_id)}
    if command in {"plan", "export"}:
        return getattr(service, command)(args.run)
    if command == "events":
        return service.store.events(args.run)
    if command == "deferred-actions":
        return service.deferred_actions(args.run)
    if command == "context":
        packet = service.context(args.run, args.task)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
        return packet
    if command == "claim":
        from .session_guard import record_claim
        result = service.claim(args.run, args.task, args.worker, lease_seconds=args.lease_seconds,
                               estimated_units=args.estimated_units, with_context=True)
        try:
            record_claim(service, args.run, args.task, result, args.session_id)
        except Exception as exc:
            # The workflow claim already committed. Preserve its token/context
            # even if optional host bookkeeping is unavailable.
            result["session_guard"] = {"tracking": "unavailable", "error": type(exc).__name__}
        return result
    if command == "heartbeat":
        return service.heartbeat(args.run, args.task, args.token, lease_seconds=args.lease_seconds)
    if command == "complete":
        result = service.complete(args.run, args.task, args.token, args.output, args.receipt,
                                  actual_units=args.actual_units)
        service.export(args.run)
        if args.task == "verify_publication":
            service.deferred_actions(args.run)
        return result
    if command == "approve":
        return service.approve(read_json(args.event))
    if command == "capabilities":
        return service.capabilities(args.run, read_json(args.file), evidence=args.evidence)
    if command == "doctor":
        return inspect(service, args.run)
    if command == "fail":
        return service.fail(args.run, args.task, args.token, args.reason, known_not_sent=args.known_not_sent)
    if command in {"unblock", "revise"}:
        return getattr(service, command)(args.run, args.task, args.reason)
    if command == "cancel":
        return service.cancel(args.run, args.reason)
    if command == "settle-cancelled":
        return service.settle_cancelled(args.run, args.task, evidence=args.evidence, actual_units=args.actual_units)
    if command == "prepare-release":
        return service.prepare_release(args.run, args.spec, assets=args.asset)
    if command == "begin-operation":
        return service.begin_operation(args.run, args.task, args.token, args.action, read_json(args.payload))
    if command == "operation-payload":
        return service.operation_payload(args.run, args.task, args.action)
    if command == "execute-media":
        from .executor import MediaExecutor
        return MediaExecutor(service).execute(args.run, args.task, args.token, read_json(args.request))
    if command == "pool":
        from .pool_service import PoolService
        return PoolService(service).operate(args.run, args.action, read_json(args.payload) if args.payload else {},
                                            expected_version=args.expected_version)
    if command == "pool-candidates":
        from .pool_service import PoolService
        return PoolService(service).candidates(args.runtime, estimated_units=args.estimated_units)
    if command == "observe-operation":
        return service.observe_operation(args.run, args.key, args.status, args.receipt, event_id=args.event_id)
    if command == "reconcile-task":
        return service.reconcile_task(args.run, args.task, worker=args.worker, outcome=args.outcome, evidence=args.evidence)
    if command == "import-legacy":
        bundle = read_json(args.bundle)
        run = service.create(bundle["channel"], bundle["intent"], format=bundle.get("format", "short"),
                             request_id=bundle["request_id"], profiles=args.profiles)
        def import_evidence(tx, state):
            artifacts = []
            for entry in bundle["artifacts"]:
                artifact = service.artifacts.put(args.bundle.parent / entry["path"], entry["kind"])
                if artifact["sha256"] != entry["sha256"]:
                    raise WorkflowError("legacy input hash mismatch")
                state["artifacts"][artifact["id"]] = artifact
                artifacts.append(artifact["id"])
            state["legacy_import"] = {"source_version": bundle["source_version"], "artifacts": artifacts,
                                      "owner": bundle["owner"], "checkpoint": "unverified"}
            state["tasks"]["research"].update(status="blocked", blocker="Imported source evidence requires checkpoint mapping; approvals are not inferred.")
            return state["legacy_import"]
        result = service.store.mutate(run["id"], import_evidence)
        return {"run_id": run["id"], "import": result}
    if command == "attach-artifact":
        return service.attach(args.run, args.file, kind=args.kind, source=args.source, expected_sha256=args.expected_sha256)
    if command == "add-thumbnail-task":
        return service.add_thumbnail_task(args.run, read_json(args.brief))
    raise WorkflowError("unknown command")


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "profiles":
            result = inspect_profiles(args.profiles or args.project_root / "channels",
                                      channel=args.channel, format=args.format, project=args.project_root)
        elif args.command == "cross-promotion-plan":
            from .cross_promotion import build_plan
            from .release import ReleaseSpec
            result = build_plan(ReleaseSpec.from_dict(read_json(args.release_spec)),
                                video_id=args.video_id, inventory=read_json(args.inventory))
        else:
            service = Production(Store(args.db), args.workspace, args.project_root,
                                 approval_public_key=os.environ.get("YTV_APPROVAL_PUBLIC_KEY"))
            result = dispatch(service, args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (WorkflowError, ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

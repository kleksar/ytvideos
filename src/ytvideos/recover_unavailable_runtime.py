"""Recover an early, quiescent run when the original code checkout is unavailable."""

import copy
import json

from .context import reference_path, snapshot_references, validate_reference_routes
from .errors import Conflict, WorkflowError
from .migration import _operations, _put_json, _quiescent, _slots, _source_context
from .service import code_identity
from .util import digest, require_text, utc_now


def _build(service, tx, run, version):
    if type(version) is not int or run["version"] != version:
        raise Conflict("stale source state version")
    _source_context(run)
    operations, slots = _operations(tx, run["id"]), _slots(tx, run["id"])
    _quiescent(run, operations, slots)
    if run["status"] == "cancelled" or operations or slots or run.get("pool") or run.get("motion_batch"):
        raise Conflict("unavailable-source recovery requires no provider operations, slots or saved pool")
    if any(task["status"] == "complete" for name, task in run["tasks"].items()
           if name not in {"research", "script"}):
        raise Conflict("unavailable-source recovery requires no completed production tasks")
    for artifact in run["artifacts"].values():
        service.artifacts.resolve(artifact)
    source = run["artifacts"].get(run.get("source_script_id"))
    if (source["sha256"] if source else None) != run["pins"].get("source_script"):
        raise Conflict("source script differs from its saved pin")
    catalog = json.loads((service.project / ".agent/skill-catalog.json").read_text())
    skills = {}
    for entry in catalog["skills"]:
        path = reference_path(entry["path"])
        target = (service.project / path).resolve()
        if not target.is_relative_to(service.project) or not target.is_file() or entry["name"] in skills:
            raise WorkflowError("invalid target skill catalog")
        skills[entry["name"]] = {"path": path, "text": require_text(target.read_text(), "target skill")}
    if any(task["skill"] not in skills for task in run["tasks"].values()):
        raise WorkflowError("target catalog does not cover the saved tasks")
    references = snapshot_references(service.project, run["profile"], run["format"])
    for path, document in run["reference_snapshot"]["documents"].items():
        if path.startswith("channels/") and references["documents"].get(path) != document:
            raise Conflict(f"target channel document differs from pinned source: {path}")
    validate_reference_routes(references, run["profile"], run["format"])
    pins = {**run["pins"], "code": code_identity(service.project),
            "skills": digest(skills), "references": digest(references)}
    plan = {"schema": "ytv-unavailable-runtime-recovery-v1", "run_id": run["id"],
            "source": {"version": version, "state_sha256": digest(run), "pins": run["pins"],
                       "code_checkout": "unavailable_unverified"},
            "target": {"root": str(service.project), "pins": pins},
            "preserved": {"profile": run["pins"]["profile"], "revision": run["revision"],
                          "approvals": run["approvals"], "budget": run["budget"]},
            "operations": operations, "slots": slots, "external_dispatch": False}
    plan["plan_sha256"] = digest(plan)
    return plan, skills, references


def plan_recovery(service, run_id, *, expected_version):
    with service.store.transaction() as tx:
        return _build(service, tx, tx.get_run(run_id, lock=False), expected_version)[0]


def apply_recovery(service, run_id, plan, *, source, message):
    source = require_text(source, "owner decision source")
    message = require_text(message, "owner decision message")
    if (not isinstance(plan, dict) or plan.get("run_id") != run_id
            or plan.get("plan_sha256") != digest({k: v for k, v in plan.items() if k != "plan_sha256"})):
        raise WorkflowError("invalid recovery plan")
    with service.store.transaction() as tx:
        run = tx.get_run(run_id)
        rebuilt, skills, references = _build(service, tx, run, plan["source"]["version"])
        if rebuilt != plan:
            raise Conflict("recovery state or target changed since planning")
        snapshot = _put_json(service, {"schema": "ytv-runtime-recovery-snapshot-v1",
                                       "run": copy.deepcopy(run), "operations": plan["operations"],
                                       "slots": plan["slots"]}, "runtime_snapshot")
        receipt = _put_json(service, {"schema": "ytv-runtime-recovery-receipt-v1", "plan": plan,
                                      "snapshot_artifact": snapshot, "source": source, "message": message,
                                      "created_at": utc_now()}, "runtime_recovery")
        if _build(service, tx, run, plan["source"]["version"])[0] != plan:
            raise Conflict("recovery inputs changed during archival")
        run["pins"] = copy.deepcopy(plan["target"]["pins"])
        run["skills"], run["reference_snapshot"] = skills, references
        if run["profile"]["recipe"] == "illustrated":
            capabilities = run["tasks"]["storyboard"]["capabilities"]
            if "sessions.independent" not in capabilities:
                capabilities.append("sessions.independent")
        for artifact in (snapshot, receipt):
            run["artifacts"][artifact["id"]] = artifact
        run.setdefault("runtime_recoveries", []).append({"plan_sha256": plan["plan_sha256"],
                                                        "receipt_artifact_id": receipt["id"]})
        service._context_pins(run)
        tx.event("runtime-recovery:" + run_id + ":" + plan["plan_sha256"], run_id,
                 "run.runtime_recovered", {"receipt": receipt})
        tx.save(run)
        return {"run_id": run_id, "snapshot": snapshot, "receipt": receipt}

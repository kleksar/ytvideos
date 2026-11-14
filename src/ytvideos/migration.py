"""Explicit, local-only migration of runtime rules for one preserved run.

This is not a workflow/schema upgrade, a repair of old evidence, or permission
to dispatch a provider. The source checkout is read as data, never executed.
"""
import copy
import json
from pathlib import Path
import tempfile

from .context import reference_path, snapshot_references, validate_documents, validate_reference_routes
from .errors import Conflict, WorkflowError
from .profiles import load_profile
from .util import canonical, digest, require_text, utc_now
from .workflow import WORKFLOW_VERSION, valid_approval


PLAN_SCHEMA = "ytv-runtime-migration-plan-v1"


def _operations(tx, run_id):
    return [json.loads(row[0]) for row in tx.execute(
        "SELECT doc FROM operations WHERE run_id=? ORDER BY key", (run_id,)).fetchall()]


def _slots(tx, run_id):
    exists = (tx.execute("SELECT to_regclass(?)", ("runtime_slots",)).fetchone()[0] if tx.postgres
              else tx.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                              ("runtime_slots",)).fetchone())
    if not exists:
        return []
    return [dict(zip(("id", "runtime_id", "run_id", "operation_id", "state"), row))
            for row in tx.execute("SELECT id,runtime_id,run_id,operation_id,state FROM runtime_slots "
                                  "WHERE run_id=? ORDER BY id", (run_id,)).fetchall()]


def _quiescent(run, operations, slots):
    if any(task.get("claim") or task.get("status") in {"running", "unknown"}
           for task in run["tasks"].values()):
        raise Conflict("reconcile active or uncertain task claims before runtime migration")
    if any(op.get("status") not in {"confirmed", "not_performed"} for op in operations):
        raise Conflict("reconcile dispatched or unknown external operations before runtime migration")
    if any(slot["state"] != "released" for slot in slots):
        raise Conflict("release active or uncertain runtime slots before runtime migration")
    if any(run["budget"].get(key, 0) != 0 for key in ("reserved", "unknown_reserved")):
        raise Conflict("reconcile reserved or uncertain budget before runtime migration")
    motion = run.get("motion_batch")
    if motion is not None:
        if not isinstance(motion, dict) or not isinstance(motion.get("scenes", {}), dict):
            raise WorkflowError("cannot verify the saved motion batch is quiescent")
        if (motion.get("reserved", 0) != 0 or motion.get("status") in {"running", "dispatched", "unknown"}
                or any(not isinstance(scene, dict) or scene.get("status") in {"running", "dispatched", "unknown"}
                       for scene in motion.get("scenes", {}).values())):
            raise Conflict("reconcile reserved or uncertain saved motion batch before runtime migration")
    pool = run.get("pool")
    if pool is not None:
        if (not isinstance(pool, dict) or not isinstance(pool.get("backend"), dict)
                or not isinstance(pool.get("scheduler"), dict)
                or not isinstance(pool["backend"].get("requests"), dict)
                or not isinstance(pool["scheduler"].get("records"), list)):
            raise WorkflowError("cannot verify the saved pool is quiescent")
        from .workers import AdaptivePool
        if (any(record.get("status") not in AdaptivePool.TERMINAL for record in pool["scheduler"]["records"])
                or any(request.get("status") not in {"completed", "failed", "not_started"}
                       for request in pool["backend"]["requests"].values())):
            raise Conflict("reconcile queued, active or uncertain pool work before runtime migration")


def _source_context(run):
    if run.get("schema_version") != 1 or run["pins"].get("workflow") != WORKFLOW_VERSION:
        raise WorkflowError("runtime migration does not upgrade run schema or workflow version")
    for name in ("profile", "skills"):
        if digest(run[name]) != run["pins"].get(name):
            raise Conflict(f"source {name} differs from its saved pin")
    for name, skill in run["skills"].items():
        require_text(skill.get("text"), f"source skill {name}")
    references = run.get("reference_snapshot")
    if not isinstance(references, dict) or digest(references) != run["pins"].get("references"):
        raise Conflict("source references differ from their saved pin")
    if not isinstance(references.get("routes"), dict) or not isinstance(references.get("documents"), dict):
        raise WorkflowError("invalid source reference snapshot")
    # Validate original declarations, not the newer code's required route set.
    for paths in references["routes"].values():
        if not isinstance(paths, list) or any(path not in references["documents"] for path in paths):
            raise WorkflowError("incomplete source reference snapshot")
        validate_documents(paths, [references["documents"][path] for path in paths])


def _target_context(service, run):
    target_profile = load_profile(service.project / "channels", run["channel"])
    profile_compatibility = None
    if target_profile != run["profile"]:
        # PR #75 added this optional guard after some episodes had already
        # pinned their profile. The migrated episode keeps its old profile;
        # this exception must never silently adopt the new value.
        pinned_video = run["profile"].get("production", {}).get("video", {})
        target_video = target_profile.get("production", {}).get("video", {})
        candidate = copy.deepcopy(target_profile)
        candidate_video = candidate.get("production", {}).get("video", {})
        if ("minimum_shot_seconds" not in pinned_video
                and type(target_video.get("minimum_shot_seconds")) is int
                and target_video["minimum_shot_seconds"] == 2):
            candidate_video.pop("minimum_shot_seconds")
            if candidate == run["profile"]:
                profile_compatibility = {
                    "mode": "preserve_pinned_missing_optional_minimum_shot_seconds",
                    "path": "production.video.minimum_shot_seconds",
                    "pinned": "absent", "target": 2,
                    "effective_profile": "unchanged_pinned_profile",
                    "source": "PR #75 (636386783a13b7b11d2173c233b68654f43d9848)",
                }
        if profile_compatibility is None:
            raise Conflict("runtime-only migration must preserve the exact channel profile")
    catalog = json.loads((service.project / ".agent/skill-catalog.json").read_text(encoding="utf-8"))
    skills = {}
    for entry in catalog["skills"]:
        path = reference_path(entry["path"])
        target = (service.project / path).resolve()
        if not target.is_relative_to(service.project) or not target.is_file() or entry["name"] in skills:
            raise WorkflowError("invalid target skill catalog")
        skills[entry["name"]] = {"path": path, "text": require_text(
            target.read_text(encoding="utf-8"), f"target skill {entry['name']}")}
    if any(task["skill"] not in skills for task in run["tasks"].values()):
        raise WorkflowError("target catalog does not cover every existing task skill")
    references = snapshot_references(service.project, run["profile"], run["format"])
    validate_reference_routes(references, run["profile"], run["format"])
    for path, document in run["reference_snapshot"]["documents"].items():
        if path.startswith("channels/") and references["documents"].get(path) != document:
            raise Conflict(f"runtime-only migration must preserve pinned channel document: {path}")
    return skills, references, profile_compatibility


def _build(service, tx, run, source_root, expected_version):
    from .service import code_identity
    if type(expected_version) is not int or run["version"] != expected_version:
        raise Conflict("stale source state version; prepare a new migration plan")
    source_root = Path(source_root).resolve(strict=True)
    if not (source_root / "src/ytvideos").is_dir():
        raise WorkflowError("source checkout has no runtime sources")
    _source_context(run)
    source_code = code_identity(source_root)
    if source_code != run["pins"]["code"]:
        raise Conflict("source checkout does not match the run's saved code pin")
    operations, slots = _operations(tx, run["id"]), _slots(tx, run["id"])
    _quiescent(run, operations, slots)
    for artifact in run["artifacts"].values():
        service.artifacts.resolve(artifact)
    if not valid_approval(run, "script"):
        raise WorkflowError("runtime migration requires the existing exact accepted script")
    approval = run["approvals"]["script"]
    script = run["artifacts"].get(approval["artifact_id"])
    if not script or approval.get("sha256") != script["sha256"]:
        raise Conflict("accepted script approval does not match its exact artifact")
    supplied = run["artifacts"].get(run.get("source_script_id"))
    if (supplied["sha256"] if supplied else None) != run["pins"].get("source_script"):
        raise Conflict("source script differs from its saved pin")
    skills, references, profile_compatibility = _target_context(service, run)
    target_pins = {**run["pins"], "code": code_identity(service.project),
                   "skills": digest(skills), "references": digest(references)}
    if target_pins == run["pins"]:
        raise WorkflowError("run already matches the target runtime; no migration is needed")
    old_documents = run["reference_snapshot"]["documents"]
    new_documents = references["documents"]
    plan = {"schema": PLAN_SCHEMA, "run_id": run["id"], "channel": run["channel"],
            "format": run["format"], "revision": run["revision"],
            "source": {"root": str(source_root), "version": run["version"], "pins": run["pins"],
                       "state_sha256": digest(run), "operations_sha256": digest(operations),
                       "runtime_slots_sha256": digest(slots)},
            "target": {"root": str(service.project), "pins": target_pins,
                       "reference_routes": references["routes"]},
            "preserved": {"profile_sha256": run["pins"]["profile"],
                          "script_artifact_id": script["id"], "script_sha256": script["sha256"],
                          "artifact_count": len(run["artifacts"]), "operation_count": len(operations),
                          "channel_documents": {path: doc["sha256"] for path, doc in old_documents.items()
                                                if path.startswith("channels/")}},
            "changes": {"skills": sorted(name for name in set(run["skills"]) | set(skills)
                                          if run["skills"].get(name) != skills.get(name)),
                        "references_added": sorted(set(new_documents) - set(old_documents)),
                        "references_removed": sorted(set(old_documents) - set(new_documents)),
                        "references_changed": sorted(path for path in set(old_documents) & set(new_documents)
                                                     if old_documents[path] != new_documents[path])},
            "scope": "runtime_rules_only", "external_dispatch": False,
            "approval_and_qa_evidence_created": False}
    if profile_compatibility is not None:
        plan["target"]["profile_compatibility"] = profile_compatibility
    plan["plan_sha256"] = digest(plan)
    return plan, skills, references, operations, slots


def plan_runtime_migration(service, run_id, source_root, *, expected_version):
    """Read and verify a concrete migration proposal without saving run or CAS data."""
    with service.store.transaction() as tx:
        run = tx.get_run(run_id, lock=False)
        return _build(service, tx, run, source_root, expected_version)[0]


def _put_json(service, value, kind):
    with tempfile.TemporaryDirectory(prefix="ytv-migration-") as directory:
        path = Path(directory) / (kind + ".json")
        path.write_text(canonical(value), encoding="utf-8")
        artifact = service.artifacts.put(path, kind)
    service.artifacts.resolve(artifact)
    return artifact


def apply_runtime_migration(service, run_id, source_root, plan, *, source, message, continue_receipt=None):
    """Compare the exact proposal under lock, archive old state, then save once."""
    source = require_text(source, "actual owner decision source")
    message = require_text(message, "actual owner decision message")
    if continue_receipt is not None and (not isinstance(continue_receipt, str)
            or len(continue_receipt) != 64 or any(c not in "0123456789abcdef" for c in continue_receipt)):
        raise WorkflowError("continue receipt must be an exact lowercase SHA-256")
    if (not isinstance(plan, dict) or plan.get("schema") != PLAN_SCHEMA or plan.get("run_id") != run_id
            or plan.get("plan_sha256") != digest({key: value for key, value in plan.items() if key != "plan_sha256"})):
        raise WorkflowError("invalid or modified runtime migration plan")
    decision = {"authority": "local_session", "source": source, "message": message}
    with service.store.transaction() as tx:
        run = tx.get_run(run_id)
        history = run.get("runtime_migrations", [])
        for prior in history:
            if prior["plan_sha256"] == plan["plan_sha256"]:
                receipt = json.loads(service.artifacts.resolve(run["artifacts"][prior["receipt_artifact_id"]]).read_text())
                service.artifacts.resolve(receipt["snapshot_artifact"])
                if (receipt["decision"] != decision or receipt["source"]["root"] != str(Path(source_root).resolve())
                        or receipt.get("continued_from_receipt_sha256") != continue_receipt):
                    raise Conflict("migration retry differs from the original decision or source checkout")
                if run["pins"] != receipt["target"]["pins"]:
                    raise Conflict("historical migration was applied, but the current runtime has since changed")
                return {"run_id": run_id, "version": run["version"], "duplicate": True,
                        "receipt": receipt, "receipt_artifact": run["artifacts"][prior["receipt_artifact_id"]]}
        if continue_receipt is not None:
            if not history:
                raise Conflict("continuation requires the latest recorded migration receipt")
            previous_artifact = run["artifacts"][history[-1]["receipt_artifact_id"]]
            if previous_artifact["sha256"] != continue_receipt:
                raise Conflict("continuation must name the latest migration receipt")
            previous = json.loads(service.artifacts.resolve(previous_artifact).read_text())
            previous_snapshot = json.loads(service.artifacts.resolve(previous["snapshot_artifact"]).read_text())
            if previous["decision"] != decision:
                raise Conflict("continuation must preserve the exact owner decision")
            if (previous["run_id"] != run_id or run["version"] != previous["to_version"]
                    or run["revision"] != previous_snapshot["run"]["revision"]
                    or run["pins"] != previous["target"]["pins"]
                    or plan["source"]["pins"] != previous["target"]["pins"]):
                raise Conflict("continuation state version, source pins or revision differ from the latest migration")
            if any(plan["preserved"][key] != previous["preserved"][key]
                   for key in ("profile_sha256", "script_artifact_id", "script_sha256", "channel_documents")):
                raise Conflict("continuation must preserve the same accepted script and channel")
        elif any(prior["decision_source"] == source for prior in history):
            raise Conflict("owner decision source was already used for another migration plan")
        rebuilt, skills, references, operations, slots = _build(
            service, tx, run, source_root, plan["source"]["version"])
        if canonical(rebuilt) != canonical(plan):
            raise Conflict("source state, operations, checkout or target rules changed since migration plan")
        before = copy.deepcopy(run)
        snapshot = _put_json(service, {"schema": "ytv-runtime-migration-snapshot-v1", "run": before,
                                      "operations": operations, "runtime_slots": slots,
                                      "source_root": rebuilt["source"]["root"],
                                      "state_sha256": rebuilt["source"]["state_sha256"]}, "runtime_snapshot")
        # Files are outside the database transaction: check again after archival.
        if _build(service, tx, run, source_root, plan["source"]["version"])[0] != rebuilt:
            raise Conflict("migration inputs changed during archival; source state was retained")
        receipt = {"schema": "ytv-runtime-migration-receipt-v1", "run_id": run_id,
                   "plan_sha256": plan["plan_sha256"], "source": plan["source"], "target": plan["target"],
                   "from_version": before["version"], "to_version": before["version"] + 1,
                   "snapshot_artifact": snapshot, "preserved": plan["preserved"],
                   "decision": decision, "created_at": utc_now(), "external_dispatch": False,
                   "approval_and_qa_evidence_created": False}
        if continue_receipt is not None:
            receipt["continued_from_receipt_sha256"] = continue_receipt
        receipt_artifact = _put_json(service, receipt, "runtime_migration")
        if _build(service, tx, run, source_root, plan["source"]["version"])[0] != rebuilt:
            raise Conflict("migration inputs changed during receipt archival; source state was retained")
        run["pins"] = copy.deepcopy(rebuilt["target"]["pins"])
        run["skills"], run["reference_snapshot"] = skills, references
        for artifact in (snapshot, receipt_artifact):
            run["artifacts"][artifact["id"]] = artifact
        entry = {"plan_sha256": plan["plan_sha256"],
            "receipt_artifact_id": receipt_artifact["id"], "snapshot_artifact_id": snapshot["id"],
            "decision_source": source, "created_at": receipt["created_at"]}
        if continue_receipt is not None:
            entry["continued_from_receipt_sha256"] = continue_receipt
        run.setdefault("runtime_migrations", []).append(entry)
        service._context_pins(run)
        tx.event("runtime-migration:" + run_id + ":" + plan["plan_sha256"], run_id,
                 "run.runtime_migrated", receipt)
        tx.save(run)
        return {"run_id": run_id, "version": run["version"], "duplicate": False,
                "receipt": receipt, "receipt_artifact": receipt_artifact}

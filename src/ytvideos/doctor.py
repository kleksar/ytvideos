"""Read-only local capability checks, not inferred provider access."""
import os
import shutil
import json

from .capabilities import capability_check


def inspect(production, run_id=None, *, run_snapshot=None):
    checks = [dict(capability="state.store", available=True, evidence=production.store.health()),
              dict(capability="artifact.local_storage", available=os.access(production.artifacts.root, os.W_OK),
                   evidence=str(production.artifacts.root))]
    signed = bool(production.approvals.public_key)
    checks.append(dict(capability="approval.verifier" if signed else "approval.local_session", available=True,
                       evidence="Ed25519 public verifier configured; signed-only ingress" if signed else
                       "Record the owner's explicit reply with approve --run; no key, bridge or hooks required"))
    for binary in ("ffmpeg", "ffprobe"):
        path = shutil.which(binary)
        checks.append(dict(capability=f"local.{binary}", available=bool(path), evidence=path or "binary not found"))
    if run_id:
        run = run_snapshot if run_snapshot is not None else production.store.get(run_id)
        if run["id"] != run_id:
            raise ValueError("doctor snapshot belongs to another run")
        if run.get("motion_batch") is not None:
            from .motion_audit import audit_motion_batch
            from .errors import WorkflowError
            def read_observation(artifact):
                try:
                    return json.loads(production.artifacts.resolve(artifact).read_text())
                except WorkflowError as exc:
                    raise ValueError(str(exc)) from exc
            try:
                with production.store.transaction() as tx:
                    operations = [json.loads(row[0]) for row in tx.execute(
                        "SELECT doc FROM operations WHERE run_id=?", (run_id,)).fetchall()]
                audit = audit_motion_batch(run, operations, resolve_document=read_observation)
            except (ValueError, TypeError, KeyError, AttributeError):
                # Diagnosis must remain available for malformed legacy data.
                # Preserve the original state; do not manufacture repaired bindings.
                audit = {"schema": "ytv-motion-audit-v1", "run_id": run_id,
                         "status": "evidence_incomplete", "dispatch_authorized": False,
                         "findings": [{"code": "saved_batch_structure_invalid", "path": "motion_batch",
                                       "severity": "error", "detail": "Saved batch/operation structure cannot be audited"}]}
            checks.append(dict(capability="video.saved_batch_evidence", available=False,
                               evidence=audit, state="unverified",
                               next_action="Reconcile recorded bindings before a new paid operation; this audit is never dispatch authority or a decision to reject existing media."))
        for name, observation in sorted(run["capabilities"].items()):
            if name not in {"approval.verifier", "approval.local_session"} and (signed or name != "approval.bridge"):
                checks.append(capability_check(name, observation))
        known = {entry["capability"] for entry in checks}
        required = {name for task in run["tasks"].values() for name in task["capabilities"]}
        # Scene tasks do not exist until storyboard completion. Report the
        # recipe's generation/extraction requirement before paying for audio.
        required.add("image.generate" if run["profile"]["recipe"] == "illustrated" else "media.licensed_clip")
        for name in sorted(required - known):
            checks.append(capability_check(name, None))
    if signed and not any(check["capability"] == "approval.bridge" for check in checks):
        checks.append(capability_check("approval.bridge", None))
    return {"checks": checks, "policy": "Missing downstream capability does not block independent upstream work.",
            "limits": ["Local files are not a verified shared backup.",
                       "The CLI does not create ChatGPT sessions by itself; a supported host dispatcher is required.",
                       ("A configured verifier is not proof that a live user-event bridge is connected." if signed else
                        "Local approvals trust the owner/coordinator; message references are audit data, not authentication.")]}

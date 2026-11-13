"""Read-only diagnostics for saved external-video batches, including legacy forks.

This checks declared bindings, not consent, actual playback, or provider truth.
A clean report is never a dispatch permit. No state or media is modified.
"""
from .util import digest


def audit_motion_batch(run, operations, *, resolve_document=None):
    """Inspect a saved run and operation documents without repairing missing evidence.

    ``resolve_document`` may read an artifact record and return its parsed JSON.
    Without it receipt contents remain unverified. Legacy absent bindings are
    reported explicitly instead of inferred from a nearby approval or prose.
    """
    findings = []

    def add(code, path, detail, severity="unverified"):
        findings.append({"code": code, "path": path, "severity": severity, "detail": detail})

    def result(status):
        return {"schema": "ytv-motion-audit-v1", "run_id": run.get("id"),
                "status": status, "dispatch_authorized": False, "findings": findings}

    batch = run.get("motion_batch")
    if batch is None:
        return result("not_applicable")
    if not isinstance(batch, dict):
        add("invalid_batch", "motion_batch", "Expected a structured saved batch", "error")
        return result("evidence_incomplete")
    approval = run.get("approvals", {}).get("script", {})
    script_hash = approval.get("sha256")
    if (not script_hash or approval.get("revision") != run.get("revision")
            or approval.get("artifact_id") not in run.get("tasks", {}).get("script", {}).get("outputs", [])
            or run.get("tasks", {}).get("script", {}).get("status") != "complete"):
        add("script_approval_stale", "approvals.script", "No current exact accepted script", "error")
    expected = {"revision": run.get("revision"), "script_sha256": script_hash}
    for key, value in expected.items():
        if key not in batch:
            add("batch_binding_missing", "motion_batch." + key, "Batch does not declare its accepted input binding")
        elif batch[key] != value:
            add("batch_binding_mismatch", "motion_batch." + key, "Batch belongs to different accepted inputs", "error")
    settings = batch.get("settings")
    settings_hash = digest(settings) if isinstance(settings, dict) and settings else None
    contract = {"batch_sha256": batch.get("batch_sha256"), "settings_sha256": settings_hash,
                "provider": batch.get("provider"), "model": batch.get("model"), **expected}
    decision = batch.get("approval", {})
    if not isinstance(decision, dict):
        decision = {}
    for key, value in contract.items():
        if value is None or value == "":
            add("batch_contract_missing", "motion_batch." + key, "Batch contract field is unavailable")
        if key not in decision:
            add("approval_binding_missing", "motion_batch.approval." + key, "Owner decision has no explicit exact-batch binding")
        elif value is not None and decision[key] != value:
            add("approval_binding_mismatch", "motion_batch.approval." + key, "Decision identifies different batch inputs", "error")
    for key in ("source", "message"):
        if not isinstance(decision.get(key), str) or not decision[key].strip():
            add("approval_evidence_missing", "motion_batch.approval." + key, "Actual owner decision/source is absent")
    budget_keys = ("max_credits", "per_request", "spent", "reserved")
    valid_budget = all(type(batch.get(key)) is int and batch[key] >= 0 for key in budget_keys)
    if not valid_budget:
        add("budget_invalid", "motion_batch", "Budget must contain nonnegative integer units", "error")
    elif batch["spent"] + batch["reserved"] > batch["max_credits"]:
        add("budget_exceeded", "motion_batch", "Spent plus reserved exceeds the approved limit", "error")
    if decision.get("max_credits") != batch.get("max_credits") or "max_credits" not in decision:
        add("budget_approval_unbound", "motion_batch.approval.max_credits", "Limit is not bound to the exact owner decision")
    scenes = batch.get("scenes")
    if not isinstance(scenes, dict) or not scenes:
        add("scenes_invalid", "motion_batch.scenes", "No structured scene inventory", "error")
        return result("evidence_incomplete")
    by_key = {}
    for op in operations:
        if isinstance(op, dict):
            key = op.get("key")
            if key in by_key:
                add("operation_duplicate", "operations", "Repeated operation key in input", "error")
            by_key[key] = op
    for scene, item in scenes.items():
        path = "motion_batch.scenes." + str(scene)
        if not isinstance(item, dict):
            add("scene_invalid", path, "Expected a structured scene", "error")
            continue
        source = run.get("artifacts", {}).get(item.get("image_artifact_id"), {})
        if not item.get("image_sha256") or source.get("sha256") != item.get("image_sha256"):
            add("source_unbound", path, "Scene has no matching exact source artifact", "error")
        if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
            add("prompt_missing", path, "Exact submitted prompt is absent")
        if item.get("status") == "pending":
            continue
        op = by_key.get(item.get("operation_key"))
        if not op:
            add("operation_missing", path, "Non-pending scene has no recorded provider operation", "error")
            continue
        if op.get("run_id") != run.get("id"):
            add("operation_wrong_run", path, "Operation belongs to another run", "error")
        if op.get("status") in {"dispatched", "unknown"}:
            add("operation_unresolved", path, "Reconcile before considering any further dispatch")
        payload = op.get("payload", {})
        if not isinstance(payload, dict):
            payload = {}
        requested = {**contract, "scene": scene, "image_sha256": item.get("image_sha256"), "prompt": item.get("prompt")}
        if any(payload.get(key) != value or key not in payload for key, value in requested.items()):
            add("operation_payload_unbound", path, "Stored operation does not identify the exact approved payload")
        receipt_id = op.get("receipt") or op.get("observation_artifact_id")
        artifact = run.get("artifacts", {}).get(receipt_id)
        if not artifact or resolve_document is None:
            add("observation_unverified", path, "No readable hash-verified operation observation")
            continue
        try:
            observation = resolve_document(artifact)
        except (OSError, ValueError, KeyError, TypeError):
            add("observation_unverified", path, "Operation observation cannot be verified")
            continue
        bindings = {"operation_key": op.get("key"), "attempt_id": op.get("attempt_id"),
                    "task_input_hash": op.get("task_input_hash"), "status": op.get("status")}
        if (not isinstance(observation, dict) or any(value is None or observation.get(key) != value
                                                   for key, value in bindings.items())):
            add("observation_unbound", path, "Observation does not bind exact attempt, inputs and outcome")
        if op.get("status") == "confirmed":
            actual = observation.get("actual_units") if isinstance(observation, dict) else None
            if type(actual) is not int or actual < 0:
                add("actual_cost_unverified", path, "Estimated request cost is not measured provider billing")
        if item.get("status") == "reviewed":
            add("review_requires_separate_audit", path, "Status alone proves neither motion playback nor creative acceptance")
    return result("evidence_incomplete" if findings else "declared_bindings_consistent")

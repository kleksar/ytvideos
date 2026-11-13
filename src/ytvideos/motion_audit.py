"""Read-only diagnostics for saved external-video batches, including legacy forks.

This checks declared bindings, not consent, actual playback, or provider truth.
A clean report is never a dispatch permit. No state or media is modified.
"""
from .util import digest


# An optional diagnostic encoding, not a production adapter or migration format.
# Legacy markdown/file hashes have no reconstructible payload encoding; report
# those as unverified instead of assuming that equal hash labels bind the prompt.
BATCH_DIGEST_SCHEMA = "ytv-motion-batch-canonical-v1"


def batch_manifest(batch):
    """Exact immutable projection for the explicitly declared digest encoding."""
    return {"schema": BATCH_DIGEST_SCHEMA,
            **{key: batch.get(key) for key in ("provider", "model", "revision", "script_sha256",
                                               "settings", "max_credits", "per_request")},
            "scenes": {scene: {key: item.get(key) for key in ("image_sha256", "prompt")}
                       for scene, item in batch["scenes"].items()}}


def audit_motion_batch(run, operations, *, resolve_document=None):
    """Inspect a saved run and operation documents without repairing missing evidence.

    ``resolve_document`` may read an artifact record and return its parsed JSON.
    Without it receipt contents remain unverified. Legacy absent bindings are
    reported explicitly instead of inferred from a nearby approval or prose.
    Structured terminal observations declare ``actual_units`` and generated
    output bytes as ``output_sha256``; matching these fields checks bindings,
    not provider authenticity, visual quality, or a safe dispatch route.
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
    script_artifact = run.get("artifacts", {}).get(approval.get("artifact_id"), {})
    if (not script_hash or approval.get("revision") != run.get("revision")
            or script_artifact.get("sha256") != script_hash
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
    # A saved digest is a binding, not evidence by itself. Check it against the
    # exact settings object before declaring the recorded batch consistent.
    if settings_hash is not None and "settings_sha256" not in batch:
        add("settings_digest_missing", "motion_batch.settings_sha256",
            "Legacy batch has no explicit saved settings digest binding")
    elif settings_hash is not None and batch.get("settings_sha256") != settings_hash:
        add("settings_digest_mismatch", "motion_batch.settings_sha256",
            "Saved settings digest differs from actual request settings", "error")
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
    if (batch.get("batch_digest_schema") != BATCH_DIGEST_SCHEMA
            or any(not isinstance(item, dict) for item in scenes.values())):
        add("batch_digest_unverified", "motion_batch.batch_sha256",
            "No supported exact manifest encoding; equal hash labels do not bind current scene prompts")
    elif digest(batch_manifest(batch)) != batch.get("batch_sha256"):
        add("batch_digest_mismatch", "motion_batch.batch_sha256",
            "Current batch inputs do not match the declared exact manifest digest", "error")
    by_key = {}
    for op in operations:
        if isinstance(op, dict):
            key = op.get("key")
            if not isinstance(key, str) or not key:
                add("operation_key_invalid", "operations", "Operation key must be a nonempty string", "error")
                continue
            if key in by_key:
                add("operation_duplicate", "operations", "Repeated operation key in input", "error")
            by_key[key] = op
    measured_total = 0
    measured_complete = True
    seen_operations = set()
    for scene, item in scenes.items():
        path = "motion_batch.scenes." + str(scene)
        if not isinstance(item, dict):
            add("scene_invalid", path, "Expected a structured scene", "error")
            measured_complete = False
            continue
        source = run.get("artifacts", {}).get(item.get("image_artifact_id"), {})
        if not item.get("image_sha256") or source.get("sha256") != item.get("image_sha256"):
            add("source_unbound", path, "Scene has no matching exact source artifact", "error")
        if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
            add("prompt_missing", path, "Exact submitted prompt is absent")
        expects_output = item.get("status") in {"generated", "reviewed"}
        clip = run.get("artifacts", {}).get(item.get("clip_artifact_id"), {})
        if expects_output and not clip.get("sha256"):
            add("output_artifact_missing", path, "Generated scene has no exact saved clip artifact")
        if item.get("status") == "pending" and not item.get("operation_key"):
            continue
        op = by_key.get(item.get("operation_key"))
        if not op:
            add("operation_missing", path, "Non-pending scene has no recorded provider operation", "error")
            measured_complete = False
            continue
        reused = op["key"] in seen_operations
        if reused:
            add("operation_reused", path, "Multiple scenes refer to one operation", "error")
        seen_operations.add(op["key"])
        if op.get("run_id") != run.get("id"):
            add("operation_wrong_run", path, "Operation belongs to another run", "error")
        if expects_output and op.get("status") != "confirmed":
            add("scene_operation_outcome_mismatch", path,
                "Generated/reviewed scene does not have a confirmed operation", "error")
        if op.get("status") in {"dispatched", "unknown"}:
            add("operation_unresolved", path, "Reconcile before considering any further dispatch")
            measured_complete = False
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
            measured_complete = False
            continue
        try:
            observation = resolve_document(artifact)
        except (OSError, ValueError, KeyError, TypeError):
            add("observation_unverified", path, "Operation observation cannot be verified")
            measured_complete = False
            continue
        bindings = {"operation_key": op.get("key"), "attempt_id": op.get("attempt_id"),
                    "task_input_hash": op.get("task_input_hash"), "status": op.get("status")}
        observation_bound = (isinstance(observation, dict) and all(value is not None and observation.get(key) == value
                                                                 for key, value in bindings.items()))
        if not observation_bound:
            add("observation_unbound", path, "Observation does not bind exact attempt, inputs and outcome")
            measured_complete = False
        if expects_output:
            output_hash = observation.get("output_sha256") if isinstance(observation, dict) else None
            if not isinstance(output_hash, str) or not output_hash:
                add("output_binding_missing", path,
                    "Structured output_sha256 binding is absent; reconcile any legacy output fields separately")
            elif clip.get("sha256") and clip["sha256"] != output_hash:
                add("output_binding_mismatch", path,
                    "Saved clip differs from the exact operation output observation", "error")
        if op.get("status") in {"confirmed", "failed", "not_performed"}:
            actual = observation.get("actual_units") if isinstance(observation, dict) else None
            if type(actual) is not int or actual < 0:
                add("actual_cost_unverified", path,
                    "No verified actual_units cost; reconcile any legacy billing fields separately")
                measured_complete = False
            elif observation_bound and not reused:
                measured_total += actual
        else:
            measured_complete = False
        if item.get("status") == "reviewed":
            add("review_requires_separate_audit", path, "Status alone proves neither motion playback nor creative acceptance")
    for key, op in by_key.items():
        payload = op.get("payload")
        if (key not in seen_operations and isinstance(payload, dict) and batch.get("batch_sha256")
                and payload.get("batch_sha256") == batch["batch_sha256"]):
            add("operation_outside_scene_inventory", "operations",
                "Operation declares this batch but is absent from its saved scene inventory")
            measured_complete = False
            if op.get("status") in {"dispatched", "unknown"}:
                add("operation_unresolved", "operations", "Unmapped batch operation requires reconciliation")
    if valid_budget:
        if measured_total + batch["reserved"] > batch["max_credits"]:
            add("measured_cost_exceeds_limit", "motion_batch.max_credits",
                "Verified operation costs plus reserved units exceed the declared limit", "error")
        if measured_complete and measured_total != batch["spent"]:
            add("actual_cost_ledger_mismatch", "motion_batch.spent",
                "Spent ledger differs from the sum of verified operation costs", "error")
    return result("evidence_incomplete" if findings else "declared_bindings_consistent")

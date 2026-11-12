# Storage migration — Paper Detour / 2 November 2026

Storage layout is active: Source; Assets/Generated; Work/<run>/{scratch,previews}; Edit; Deliverables/current.json. Canonical procedure: [media lifecycle](../../../../../../../.agents/skills/ytv-media-lifecycle/SKILL.md).

State: **NO_VERIFIED_LOCAL_FINAL_INDEXED**. Current pointer is an operational identity index, not a new AV acceptance. Existing acceptance and limitations remain in episode context and original QA.

Preserved local imported dependencies: 78; external/shared paths indexed: 0. Imported media remain at stable legacy paths; no relinking or Palmier mutation performed. [Dependency index](../dependencies.json); [current pointer](../../../Deliverables/current.json).

No media moved or deleted in this episode. Existing source, QA frames, evidence, projects and pending work retained.

Fresh scans cover accessible known packages, current library and retained snapshot metadata; inaccessible/external consumers remain bounded coverage. Global pre-existing unresolved imports are listed in audits; no new missing import may be attributed to this rollout without before/after comparison. Physical APFS reclaimed bytes are unknown. No new voice, mix, render or YouTube mutation.

[Before audit](before.json) · [After audit](after.json) · [Verification](verification.json).

Post-operation live Palmier API read-back was unavailable (connection refused after the app disconnected). Verification continued with fresh on-disk project metadata and source/import hashes; the coordinator did not restart or modify another session’s app. See the root rollout timeline verification record for the exact scope.

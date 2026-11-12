# Storage migration — Paper Detour / 2 November 2026

Storage layout is active: Source; Assets/Generated; Work/<run>/{scratch,previews}; Edit; Deliverables/current.json. Canonical procedure: [media lifecycle](../../../../../../../.agents/skills/ytv-media-lifecycle/SKILL.md).

State: **NO_VERIFIED_LOCAL_FINAL_INDEXED**. Current pointer is an operational identity index, not a new AV acceptance. Existing acceptance and limitations remain in episode context and original QA.

Preserved local imported dependencies: 19; external/shared paths indexed: 0. Imported media remain at stable legacy paths; no relinking or Palmier mutation performed. [Dependency index](../dependencies.json); [current pointer](../../../Deliverables/current.json).

Deleted 0 reviewed disposable files, 0 logical bytes. Moved 3 retained comparison files into owned Work with verified old-path aliases. [Operation decisions](operation-policy.json) apply only if present; actual append-only events are [locations](../locations.jsonl).

- move_keep_alias: `Edit/Previews/028_CRT_ripple_visual_sample_4s.mp4` → `Work/storage-rollout-20261102/previews/legacy/Edit/Previews/028_CRT_ripple_visual_sample_4s.mp4`; SHA256 `906602440610b9ed5db7a1503070545773da748ea85409670c8849a9d78263fc`.
- move_keep_alias: `Edit/Previews/028_taj_mahal_en_short_1080x1920_30fps_voice_v01_palmier_audio64_review_20261101.mp4` → `Work/storage-rollout-20261102/previews/legacy/Edit/Previews/028_taj_mahal_en_short_1080x1920_30fps_voice_v01_palmier_audio64_review_20261101.mp4`; SHA256 `9ea4c67aa992df470c64649acef4283b7333d88c9b69e0a5cfb71720fcd4362e`.
- move_keep_alias: `Edit/Previews/028_en_v05_CRT_ripple_20261102.mp4` → `Work/storage-rollout-20261102/previews/legacy/Edit/Previews/028_en_v05_CRT_ripple_20261102.mp4`; SHA256 `ce3d74232d03f485cf28b65c4d1105a06c09142be910070dcdc0419cb68aae73`.

Fresh scans cover accessible known packages, current library and retained snapshot metadata; inaccessible/external consumers remain bounded coverage. Global pre-existing unresolved imports are listed in audits; no new missing import may be attributed to this rollout without before/after comparison. Physical APFS reclaimed bytes are unknown. No new voice, mix, render or YouTube mutation.

[Before audit](before.json) · [After audit](after.json) · [Verification](verification.json).

Post-operation live Palmier API read-back was unavailable (connection refused after the app disconnected). Verification continued with fresh on-disk project metadata and source/import hashes; the coordinator did not restart or modify another session’s app. See the root rollout timeline verification record for the exact scope.

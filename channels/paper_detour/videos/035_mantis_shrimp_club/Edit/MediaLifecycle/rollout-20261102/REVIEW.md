# Storage migration — Paper Detour / 2 November 2026

Storage layout is active: Source; Assets/Generated; Work/<run>/{scratch,previews}; Edit; Deliverables/current.json. Canonical procedure: [media lifecycle](../../../../../../../.agents/skills/ytv-media-lifecycle/SKILL.md).

State: **PREVIEW_HELD_QA_PACING_FAIL_NO_FINAL_PROMOTION**. Current pointer is an operational identity index, not a new AV acceptance. Existing acceptance and limitations remain in episode context and original QA.

Preserved local imported dependencies: 24; external/shared paths indexed: 18. Imported media remain at stable legacy paths; no relinking or Palmier mutation performed. [Dependency index](../dependencies.json); [current pointer](../../../Deliverables/current.json).

Deleted 1 reviewed disposable files, 56792861 logical bytes. Moved 1 retained comparison files into owned Work with verified old-path aliases. [Operation decisions](operation-policy.json) apply only if present; actual append-only events are [locations](../locations.jsonl).

- delete: `Edit/Previews/Paper Detour 035 Mantis Shrimp Evolution Motion Review v01.mp4` → `Work/storage-rollout-20261102/previews/legacy/Edit/Previews/Paper Detour 035 Mantis Shrimp Evolution Motion Review v01.mp4`; SHA256 `4c2d9291a5082b7d23eaa5f096dd36df020b91cc1a68970fea52346bdd8687de`.
- move_keep_alias: `Edit/Previews/Paper Detour 035 Mantis Shrimp Evolution Static Review v01.mp4` → `Work/storage-rollout-20261102/previews/legacy/Edit/Previews/Paper Detour 035 Mantis Shrimp Evolution Static Review v01.mp4`; SHA256 `7f7ba14155dfd9c64977eb3c5b61ab096a4bbae536f4f13850c8225aa39dc842`.

Motion Safe Review v02 remains at its original active path. Fresh QA reports pacing failure; it was not promoted. The old motion v01 cropping defect is documented in the retained edit log; its frames/source/timelines remain available.

Fresh scans cover accessible known packages, current library and retained snapshot metadata; inaccessible/external consumers remain bounded coverage. Global pre-existing unresolved imports are listed in audits; no new missing import may be attributed to this rollout without before/after comparison. Physical APFS reclaimed bytes are unknown. No new voice, mix, render or YouTube mutation.

[Before audit](before.json) · [After audit](after.json) · [Verification](verification.json).

Post-operation live Palmier API read-back was unavailable (connection refused after the app disconnected). Verification continued with fresh on-disk project metadata and source/import hashes; the coordinator did not restart or modify another session’s app. See the root rollout timeline verification record for the exact scope.

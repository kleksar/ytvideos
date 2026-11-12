# Storage migration — Paper Detour / 2 November 2026

Storage layout is active: Source; Assets/Generated; Work/<run>/{scratch,previews}; Edit; Deliverables/current.json. Canonical procedure: [media lifecycle](../../../../../../../.agents/skills/ytv-media-lifecycle/SKILL.md).

State: **SRT_RETAINED_LOCAL_MP4_REMOVED_IN_PRIOR_CLEANUP**. Current pointer is an operational identity index, not a new AV acceptance. Existing acceptance and limitations remain in episode context and original QA.

Preserved local imported dependencies: 220; external/shared paths indexed: 44. Imported media remain at stable legacy paths; no relinking or Palmier mutation performed. [Dependency index](../dependencies.json); [current pointer](../../../Deliverables/current.json).

Deleted 4 reviewed disposable files, 275254968 logical bytes. Moved 0 retained comparison files into owned Work with verified old-path aliases. [Operation decisions](operation-policy-v02.json) apply only if present; actual append-only events are [locations](../locations.jsonl).

- delete: `Edit/publication_20261030/mix_candidate.wav` → `Work/storage-rollout-20261102/previews/legacy/Edit/publication_20261030/mix_candidate.wav`; SHA256 `f2c90fac1404cc1096c5fb29be8c746c243f997fb5849db91939abb10a85d76c`.
- delete: `Edit/publication_20261030/mix_candidate_pcm_voice_20261031.wav` → `Work/storage-rollout-20261102/previews/legacy/Edit/publication_20261030/mix_candidate_pcm_voice_20261031.wav`; SHA256 `856cb577840498c6f34ff51d0e965f4b00a8896282fa8d7e70149bfba14ab1f7`.
- delete: `Edit/publication_20261030/mix_candidate_pcm_voice_unity_pan_20261031.wav` → `Work/storage-rollout-20261102/previews/legacy/Edit/publication_20261030/mix_candidate_pcm_voice_unity_pan_20261031.wav`; SHA256 `0ea9f2750b43ff053a393292972438e460323a22bab71767c336f397746199f2`.
- delete: `Edit/publication_20261030/mix_candidate_no_sfx_20261031.wav` → `Work/storage-rollout-20261102/previews/legacy/Edit/publication_20261030/mix_candidate_no_sfx_20261031.wav`; SHA256 `039b8aa00a1a594ddefa5e05ec068c17dee0d6433863f94694103f5a14b44418`.

The retained corrected full WAV and separate corrected no-SFX WAV remain protected. The historical final MP4 was removed by an earlier user-authorized cleanup, before this rollout; no replacement is invented. The retained SRT keeps its original SHA.

Fresh scans cover accessible known packages, current library and retained snapshot metadata; inaccessible/external consumers remain bounded coverage. Global pre-existing unresolved imports are listed in audits; no new missing import may be attributed to this rollout without before/after comparison. Physical APFS reclaimed bytes are unknown. No new voice, mix, render or YouTube mutation.

[Before audit](before.json) · [After audit](after.json) · [Verification](verification.json).

Post-operation live Palmier API read-back was unavailable (connection refused after the app disconnected). Verification continued with fresh on-disk project metadata and source/import hashes; the coordinator did not restart or modify another session’s app. See the root rollout timeline verification record for the exact scope.

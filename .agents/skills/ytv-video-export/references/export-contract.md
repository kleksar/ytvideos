# Pre-render contract and QA handoff

Maintain one episode-specific versioned contract beside the current edit, for example `Edit/Export/EXPORT_CONTRACT_v01.json`. Reuse an equivalent existing handoff instead of creating another registry. The [template](../assets/export-contract.template.json) is a draft with nulls; fill it from actual accepted inputs and the channel profile before marking it ready.

Required contents:

- Exact episode/language/format/purpose and settings-profile version or hash.
- Saved project/timeline ID, revision/snapshot evidence, fresh settings read and dependency references/hashes. If the engine has no revision ID, retain the relevant timeline read/hash plus save/snapshot evidence; do not invent a revision.
- Canvas width/height/aspect, square pixels, rational FPS, actual exclusive end frame and derived duration.
- Required container/video/pixel format/colour/range and the complete-mix audio contract copied **as episode data** from its owner: exact mix source/edit mapping, codec/profile and applicable rate/channels/bitrate constraints. Preserve source rate and mapping separately. For Paper's native engine-managed voice-only path, record accepted mono/44.1 kHz and automatic encoder controls as such; do not invent an exact required bitrate, 48 kHz or stereo target.
- Encoding mode, actual supported requested arguments, preferred quality controls and engine-managed fields with reason/evidence. `AUTO_ENGINE_MANAGED` is a known capability limitation, not a measured value. `UNKNOWN` for a required target/input prevents readiness.
- Absolute new output path, writer/application occupancy, current authorizations, preflight author/time/evidence. Fields are data, not permission grants.
- For the shared renderer, link `subtitle_contract.json` and its fingerprint, final audio hash/speed evidence, exact transcript, [checked word map](../../ytv-srt/SKILL.md#validate-alignment-against-the-retained-recording), resolved channel/format profiles and the actual subtitle review evidence. After encoding link `VIDEO.mp4.delivery.json` and record user acceptance against its exact media SHA-256. The machine schema and release validator belong to the [renderer contract](../../../../automation/ffmpeg_montage/README.md#приёмка-и-загрузка).

Pass the shared renderer this passport with `--export-contract`; `--check-settings` compares it with the actual command without encoding. Retain `render_provenance.json` and its frozen command, passport and engine snapshots as release dependencies. AAC stream copy records `target_bit_rate: "STREAM_COPY"`, not an encoder target. Machine coverage belongs to the renderer contract linked above.

`DRAFT → READY_TO_RENDER → RENDERED_PENDING_QA`. Ready requires verified current inputs/settings, a feasible engine mapping and a resolved destination. Every relevant accepted edit/settings/mix/motion change makes readiness stale; refresh affected checks. Rendered adds file path/SHA, exact submitted arguments, job result/warnings and edit binding. Keep requested values intact when actual values differ; record differences in QA. A later renderer source update alone does not establish a media defect. Compare historical outputs with their original passport and actual saved commands; audit missing provenance before deciding whether media must change. Git HEAD is not evidence of the code used for a particular file.

## Existing QA helper

Pass this same contract into [video QA](../../ytv-video-qa/SKILL.md). A QA sampling plan may project its `frame_count`, `fps` and supported expected fields; store the contract path/hash in the reviewer receipt and verify both plans agree. The helper's `freshness` is an asserted input, not proof. Actual scene/cue intervals still come from their owners.

The current helper accepts video `width,height,codec_name,pix_fmt,color_space`, audio `required,codec_name,channels,sample_rate`. It does **not** compare container, SAR, progressive cadence, profile/level, transfer, primaries, range, audio profile, target bitrate, GOP, Fast Start or edit lists automatically. QA must record explicit checks/evidence for those applicable contract fields using raw stream/frame/container data and, where needed, packet/atom inspection. Unknown metadata stays UNVERIFIED, not an inferred match. Do not put unsupported keys in `expected` or claim the helper checked them. True CFR requires timestamp/cadence evidence, not just equal average/r-frame-rate labels.

Quality preferences and platform recommendations are identified separately from required properties. A variable measured bitrate need not equal the encoder target. No automatic final AV PASS is derived from a complete passport or a successful render. QA remains the single owner of post-render checks/coverage and suitability findings.

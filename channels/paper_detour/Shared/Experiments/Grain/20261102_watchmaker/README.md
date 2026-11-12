# Ten grain presets — watchmaker still

Current entry: [CURRENT_CONTEXT.md](CURRENT_CONTEXT.md). User-requested shared technical preview, not a narrative episode. On 2026-11-02 the user selected G08 as the common grain preset; see [acceptance](Edit/G08_ACCEPTANCE_20261102.md) and [machine preset](/Users/diplomat/ytvideos/automation/image_motion/grain_presets.json). One-command motion/grain implementation is in `automation/image_motion/run.py apply`; G08 is default, explicit `grain:none` keeps the original motion-only path. See [grain contract](/Users/diplomat/ytvideos/.agents/skills/ytv-image-motion/references/grain.md) and `Edit/CommonG08/` for scoped developer checks. No production timeline was changed.

[Current moving comparison v02](https://www.youtube.com/watch?v=W1ap6Q8Otuo). Ten identical4s pan-right/depth passes,each preceded by a1s settings card:50s,silent,1440p30. Full settings remain below each image. Same ten grain settings as the table. [Previous static control v01](https://www.youtube.com/watch?v=OFqQ5PQwyMI) retained. ExistingTest02/Test03 uploads untouched.

Current implementation/provenance/QA:[Matrix10_v02](Edit/Matrix10_v02). Canonical image-motion helper reused once; final parallax sign−1 matchespan-right,framing1.00 andcamera1.10. Identical common120-frame sequence repeatedten times. Grain is added after movement;holdinggrainfieldsat15/10Hzdoesnotfreezethe30fpsscene. Source and previousstaticcontrol remain pinned. G08 selected by the user on2026-11-02.

|Number|Name|Luma RMS codes|Gaussian sigma1440p px|Updates/sec|AR rho|
|---|---|---|---|---|---|
|01|Balanced Base|3.0|0.77|30|0.65|
|02|Soft Amplitude|2.4|0.77|30|0.65|
|03|Upper Amplitude|4.0|0.77|30|0.65|
|04|Fine Grain|3.0|0.60|30|0.65|
|05|Coarse Grain|3.0|0.95|30|0.65|
|06|Slow Refresh15|3.0|0.77|15|0.65|
|07|Slow Refresh10|3.0|0.77|10|0.65|
|08|Short Persistence|3.0|0.77|30|0.35|
|09|Long Persistence|3.0|0.77|30|0.85|
|10|Test03 Scaled|3.6|0.77|30|0.65|

RMS is noise contrast in eight-bitY codes, not opacity/coverage. Sigma is the Gaussian filter radius, not measured grain diameter. All presets use the same source,seed and luma-dependent mask(20/64/208/235limited),and preserveUVabove the caption panel. Innovation normalized to unit standard deviation;AR update uses`rho*state+sqrt(1-rho²)*innovation`.15/10Hz hold each field2/3frames;output remains30fps. Lower technical text is not grained.

Consultation: [completed personal Extra High result](../../../../../../.agent/consultations/2026-11-02-grain-matrix10.md). Source PNG has an sRGB tag; FFmpeg converts transfer/matrix/range before noise. Local source1672×940 scales once to2560×1440withminimal fill/crop;no extra detail claimed. X264CRF16/fast/tunegrain is an explicit experimental encode choice, not a changed normal channel export default. Final mux correctsSARandPTSwithout re-encoding;[decoded pixel hashes match](Edit/Matrix10_v01/MUX_PIXEL_IDENTITY.json).

Historical static v01 reconstruction inputs: preservedPNG,[SOURCE conversion command](Edit/Matrix10_v01/SOURCE.json),[presets](Edit/Matrix10_v01/presets.json),[renderer](Edit/Matrix10_v01/render_matrix.py),[exact initial encode and final mux commands](Edit/Matrix10_v01/render_receipt.json). Run the source conversion from this workspace directory so its`Work/...`destination resolves here. Render with project`automation/image_motion/.venv/bin/python`. The renderer refuses to overwrite the retained comparison;future revisions need a new owned run/output. Renderer now includes explicitSARand signedcompositionoffset flags;the actual first-run commands and correction remain in receipts. Raw base/expected frames and initial duplicate encode were owned scratch;removed after verification,not permanent media dependencies.

Historical static v01 QA: [scoped report](Edit/Matrix10_v01/QA/REPORT.json),[frozen contract](Edit/Matrix10_v01/EXPORT_CONTRACT_v01.json),[YouTube receipt](Edit/Matrix10_v01/youtube_receipt.json). Full decode and40visually inspected card/scene samples,10labelstrips andfour native grain patches;sampling is not continuous subjective playback or independent review. At the time of this historical v01 QA no winner was chosen. User subsequently selected G08 from moving v02 on2026-11-02.

Storage: [bounded preflight](Edit/MediaLifecycle/preflight-audit/audit.json),[post-upload audit](Edit/MediaLifecycle/postupload-audit/audit.json),[plan](Edit/MediaLifecycle/postupload-plan/plan.json),ownedrunmanifestandappend-onlylocationjournal. Original,currentpendingpreviewandQAprotected. Only12registered scratchfiles removed,logical329972116bytes;physicalAPFSreclaimunknown. No external video removed.

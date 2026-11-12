# Paper Detour: pre-render settings audit — 2026-11-02

Scope: channel workflow/settings only. No timeline, app preference, video export, sound or YouTube mutation performed. User explicitly chose 2K / 30 FPS; total frames are derived from actual timeline length.

Subsequent user correction and channel-layout recommendation are recorded in the [Full HD / stereo follow-up](followup_fhd_stereo/REPORT.md). It supersedes this receipt's initial geometry/audio default; retain this document as source/decision history, not the current settings profile.

## Evidence

- Live Palmier MCP `tools/list`, all 58 tools saved in [palmier-tools.json](palmier-tools.json). Only export/settings schemas were printed. `set_project_settings` supports dimensions/aspect/quality/FPS/output colour; `export_project` exposes codec/resolution/IDs/output path, not bitrate/CRF/GOP/AAC. No export job was submitted.
- [Palmier export documentation](https://www.palmier.io/docs/export): available codecs/resolutions; rate and colour follow selected timeline. Public source was retrieved through `gh` at commit **5b806b35165da70d2834b53dfc022abc8e00a12e**; installed-app commit is **UNVERIFIED**.
- [ExportOptions.swift](https://github.com/palmier-io/palmier-pro/blob/5b806b35165da70d2834b53dfc022abc8e00a12e/Sources/PalmierPro/Export/ExportOptions.swift): `.r1440p = "2K"`, short edge 1440, preserve aspect/even dimensions. [ProjectSettingsPresets.swift](https://github.com/palmier-io/palmier-pro/blob/5b806b35165da70d2834b53dfc022abc8e00a12e/Sources/PalmierPro/Project/Settings/ProjectSettingsPresets.swift) independently maps `twoK` to1440. Thus 9:16→1440×2560,16:9→2560×1440. Downloaded source is retained alongside this receipt.
- [ExportService.swift](https://github.com/palmier-io/palmier-pro/blob/5b806b35165da70d2834b53dfc022abc8e00a12e/Sources/PalmierPro/Export/ExportService.swift): lines598–620 map H.2642K/Match Timeline to HighestQuality, ProRes to AppleProRes422LPCM. SDR path attaches composition/audioMix without explicit bitrate/AAC overrides. HDR writer's separate192kbps/48k/stereo settings do **not** prove SDR settings.
- [Apple HighestQuality](https://developer.apple.com/documentation/avfoundation/avassetexportpresethighestquality): H.264/AAC, no promised numeric bitrate. Saved [Markdown](apple-highest-quality.md).
- [YouTube detailed encoding recommendations](https://support.google.com/youtube/answer/1722171?hl=en), [aspect ratios](https://support.google.com/youtube/answer/6375112?hl=en): source for platform references in the maintained profile. Detailed encoding page carries a Content Manager applicability notice; its recommendations are not a mandatory rejection list for ordinary uploads.
- [FFmpeg libx264](https://ffmpeg.org/ffmpeg-codecs.html#libx264_002c-libx264rgb), [MP4 muxer](https://ffmpeg.org/ffmpeg-formats.html#mov_002c-mp4_002c-ismv): reference for controlled fallback/CRF and Fast Start/edit lists. HTML saved after web fetch timed out. No encoding command executed.

## Consultation and resulting ownership

Coordinator personally used Chrome ChatGPT. Before both submitted narrow requests: **GPT-6**, **Extra High, 4 из 5.** The UI also showed a usage-limit notice, but both requests produced visible substantive completed answers. [Conversation](https://chatgpt.com/c/6ae815e7-6aa0-83ed-b1d7-f9e2760ee251), [saved transcript](../../../.agent/consultations/paper_export_settings_20261102.txt), [receipt](../../../.agent/consultations/paper_export_settings_20261102.md).

1. Technical SDR delivery profile. Read complete response after streaming finished; an early continuation draft was **not submitted** and was cleared. Consultant's 20Mbps / CRF17–18 suggestions are practical starting choices, not YouTube requirements. Do not adopt the grain rationale as a new effect or force stereo for a mono source. Numeric bitrate alone does not establish visual quality. ffprobe alone does not establish full CFR cadence, closed GOP, edit-list safety or final AV acceptance.
2. Ownership question. Adopt separate `ytv-video-export` for one pre-render contract/capability map. Audio owner retains full mix and audio parameters; edit owner executes; QA consumes the same frozen contract; production routes automatically. Do not duplicate specifications in QA or add fictional controls.

## Maintained outcome / limits

Canonical owner: [ytv-video-export](../../../.agents/skills/ytv-video-export/SKILL.md), with Paper profile, Palmier adapter, handoff reference and draft contract template. Audio settings updated at their existing owner: new Paper delivery48k/AAC-LC, mono192kbps, stereo384kbps target. Source channels preserved, original files retained. 384 is a chosen target, not an assertion that256 is invalid.

Preferred native path is HighestQuality H.264 from a correctly configured timeline; fully controlled encoding is a fallback for an actual required discrepancy or defect. No mandatory ProRes master for every episode. Required versus preferred/engine-managed settings are explicit. Preflight readiness is distinct from output conformance and final QA.

**Not performed:** actual new2K portrait/landscape render, encoder/audio characterization of installed build, media frame/listening QA, independent reviewer, native skills/list discovery. These remain actual-run qualification work, not completed tests. The new workflow does not change accepted historical deliveries or authorize a pilot render. Local validation is recorded separately in [validation.json](validation.json).

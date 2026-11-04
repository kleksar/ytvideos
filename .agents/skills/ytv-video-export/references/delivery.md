# Shared video delivery profile

Common delivery settings for Paper Detour and Nuviko, updated by the user's direct instruction of 2026-11-03: **2K for every new review/upload export, 30 FPS**. In this project 2K means a 1440-pixel short edge, with exact orientation dimensions below. Audio uses the shared audio owner's delivery contract and the channel's voice setting. Earlier export experiments are historical evidence, not current size defaults: [original source audit](../../../../channels/paper_detour/research/2026-11-02-export-settings/REPORT.md).

## Canvas and required delivery properties

| Property | Default |
|---|---|
| Short | 1440×2560, 9:16, square pixels, no baked bars |
| Long film | 2560×1440, 16:9, square pixels; explicit creative aspect overrides |
| Timeline and output rate | Exactly 30/1 FPS, constant presentation cadence, progressive |
| Frame count | Actual final saved timeline end frame, exclusive; not a fixed default |
| Container / codec | MP4 / H.264 AVC |
| Pixel format | 8-bit YUV 4:2:0 (`yuv420p`) |
| SDR colour | Timeline `rec709`; output primaries / transfer / matrix all `bt709` |
| Signal range | Limited/video (`tv`), correctly converted pixels and matching tags |
| Audio | Accepted full mix and [Paper audio delivery settings](../../ytv-audio-delivery/references/delivery-checks.md#paper-detour-youtube-delivery) |
| Output | Accepted episode `Deliverables/` path, explicit language and purpose |

The frame rate is established before timing captions, speech and motion. Example only: 60 seconds × 30 FPS = 1800 frames. A 1502-frame film lasts 50.066667 seconds; it must not be rounded to 1500 frames.

Use this output geometry when briefing images and generating motion derivatives. Record native source sizes and effective resolution after crop/zoom; enlarging an image does not add detail. Low-resolution accepted sources need an explicit quality decision before expensive rendering, not automatic rejection or regeneration. Apply the shared geometry before rendering the review MP4, through the edit owner with saved versions and refreshed framing/timing/dependency checks. Imported media keep their paths until a verified relink.

## Quality and engine-managed controls

**Normal path: FFmpeg.** Render to the requested canvas and frame rate using the selected channel profile and a supported encoder. Record actual command and encoder settings; do not describe project-specific trial scripts as a universal production tool.

YouTube's SDR30 reference is **8 Mbps for1080p** and **16 Mbps for1440p**, not hard minima or guarantees of quality. Our practical starting points **when an encoder exposes rate control** are **20 Mbps VBR for 2K outputs of either orientation**; with x264 constant-quality encoding use **CRF18, preset medium** for either, instead of also imposing an average bitrate. These are local starting choices, subject to paper-texture/gradient/letter-edge inspection; CRF does not translate to another encoder's Quality slider. A smaller static-scene VBR average alone is not failure.

Preferred H.264 settings when exposed: High profile, automatic compliant level, CABAC, two consecutive B frames, closed GOP. YouTube's detailed guide specifies half the frame rate for GOP: **15 frames at 30 FPS**. Encoder-specific controls depend on the selected FFmpeg encoder. Record measured profile/keyframe behaviour; recommendation deviations do not by themselves prove an upload is invalid. Prefer Fast Start (`moov` before media) and no edit lists when achievable without changing sync. Their absence requires a documented compatibility decision, not a false PASS.

**Controlled fallback:** if native output violates a required property or shows an encoding defect, diagnose first. If a suitable retained lossless/high-quality master with the full accepted mix exists, encode from it. Otherwise prepare an appropriate high-quality intermediate only when needed and authorized. Do not export/store a master for every video by default. For video-only correction preserve the accepted audio when appropriate; for audio-only correction stream-copy accepted video. Full-mix reconstruction and audio scope remain with its owner. Do not use another lossy encode as a quality-restoration source. ProRes is an editing intermediate; H.265/HDR are not the default for this SDR channel.

Converting tagged sRGB source graphics to the Rec.709 output is colour management, not simply replacing metadata. Do not relabel full-range/HDR pixels as limited SDR. Range conversion and gradients/shadows must agree with final frame checks. No automatic loudness normalization, creative grade, sharpening or new effects are implied by the export preset.

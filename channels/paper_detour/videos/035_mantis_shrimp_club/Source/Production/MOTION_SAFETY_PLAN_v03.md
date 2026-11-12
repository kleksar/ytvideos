# Motion safety plan v03 — Paper Detour Short 035

**Source:** final selected `Source/Images/paper_v03/` set, portrait source 941×1672 RGB. Delivery timeline is 1080×1920, 30 fps. Baseline last camera preset was `framing-safe` (`offset=0.12`, `height=0.2`, `camera_factor=0.35`) with `depth_zoom=1.0`; it is a candidate, not a universal safety guarantee. Before import, use that exact measured plan with per-scene paths and check source and intermediate extremes.

| Scene | Frames | Intended camera path | Protected details | Framing note / motion constraint |
|---|---:|---|---|---|
| S01 | `[0,122)` | push-in | Both whole animals, spear tip, club, eyes, center gap, title C03 | Wide master; keep both terminal ends visible throughout. Reuse exact file at loop. |
| S02A | `[122,242)` | pull-out | Complete early animal, eyes, repeated limbs, tail | Full-body view; no crop of side limbs or tail. |
| S02B | `[242,362)` | pull-out | Complete early animal and similar front limb pairs | Similar but wider alternate; all limb tips stay in frame. |
| S03 | `[362,482)` | pan-right | Whole animal, modestly distinct front pair, C01 | Keep left antenna and right tail inside; no zoom during pan. |
| S04 | `[482,612)` | push-in | Both complete specialists, both weapon ends, separation, C04 | Small centered pair; keep left/right forms separate. |
| S05 | `[612,782)` | pan-right | Complete spearer, connected front limb, all spines | Tip is right-of-center; rightward screen travel protects it. Limit scale change; verify left body boundary. |
| S06 | `[782,962)` | pan-left | Complete smasher, connected limb, full club, C02 | Club sits right-of-center; leftward travel protects right tip. Limit scale change; verify full tail. |
| S07 | `[962,1082)` | pan-left | Complete early animal, similar limbs, C05 | Broad setting; inspect antenna and tail at opposite pan extrema. |
| S08 | `[1082,1202)` | pan-right | Both full specialists, spear tip, club and gap | Wide separated figures; inspect both weapon ends and opposite boundaries. |
| S09 | `[1202,1325)` | push-in | Whole early animal and ordinary front limb | Central wide composition; preserve full limb at loop setup. |

The selected files were visually compared with a conservative **camera-only** 1.08× crop and ±1% horizontal-center mock in `Source/Images/paper_v03/MOTION_ENVELOPE_MOCK_v03.png`. This is a planning preview only: it does not simulate DepthFlow, proves no intermediate extrema, and does not grant import readiness. The exact `plan.json`, generated per-scene depth map, all intermediate extrema and actual scene/cue path must be reviewed before acceptance. If an animal or protected limb is clipped, reduce that scene’s movement/scale or regenerate the image; do not hide cropping behind an overlay.

Current assigned cue geometry uses the existing primary/alternate anchor and remains fixed to the canvas, without parallax. Verify all five cues at entry, hold, exit and adjacent frames over the actual scene movement. The new opening S01 file is used unchanged at the direct loop.

## Implemented review — 2026-11-02

The selected set was imported on still timeline `D4A45BE0`, then rendered to the separate motion target `2436013F` using `framing-safe`, `depth_zoom=1.0` and `grain: none`. The actual paths/keyframes, output cache references and structural status are recorded in `Edit/ImageMotion/8ff6b74af43523239e3a/run.json`; target snapshot `B4AF2610`.

Offline QA sampled the actual camera/depth cache at five local frames for each scene and recomposited nine states for every assigned cue, including the loop-boundary setup, entry, hold, fade and adjacent scene boundary. The sampled subjects and tips remain inside frame; all five phrases remain legible and clear of the animals. Evidence and exact global frame samples: `Edit/ImageMotion/8ff6b74af43523239e3a/qa/MOTION_QA_v01.md`. This sample review does not certify every intermediate frame, playback or export.

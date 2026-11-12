# Paper Detour 038 — layered motion status EN v03

**User decision:** continue with the current layered-motion standard. **Current state:** S001 and S002 have scene-specific FG/BG preparations and 2560×1440 layered motion pilots with G08. These are visual trials only: no motion media has been imported into Palmier, and the accepted 144-scene set is not complete. S003 has a refined mask/inpaint and a 2560×1440 G08 pilot; all three pilots remain author-inspected trials only.

## Required method

The current `ytv-image-motion` standard (3 November 2026) uses the original still, one separately prepared RGBA foreground, and one restored opaque background. Render layered parallax first, move the whole image in the opposing direction second, apply G08 third, then add editor overlays. The approved renderer takes `foreground` and `background`; it does not take a separate middle-ground input. See `../../../../../.agents/skills/ytv-image-motion/references/layered-motion.md`.

## Verified Palmier state

- Project `FE6B0E4C`; source assembly `AC510A6E` is retained. Production/music branch `51E4D60B` is separate.
- The legacy `run.py apply` prepared 144 temporary derivatives, then returned HTTP 404 before recording any Palmier operation. No `pending.json`, receipts, `target_before.json` or target ID exist for that run.
- Direct Palmier MCP readback confirmed `51E4D60B` still contains the original 142 story stills, two endscreen stills, 13 accent clips, voice `[0,18424)` and music `[420,18420)`. No motion clip has been imported or applied.
- The second legacy apply attempt stopped at preflight because DepthFlow does not implement the accepted opposed layered motion. No mutation followed. `Work/image-motion-531dbf2675c38b40310c/scratch/` was observed empty (0 files, 0 bytes). No project file or shared cache was deleted.

## S001 — layered pilot

- Local SAM 2.1 runs in `/Users/diplomat/paper-detour-sam2-local`. The automatic Vision instance mask was too broad. A first LaMa pass removing both figures and the gate visibly damaged the gate; that result was rejected.
- Tight manual SAM2.1 point/box prompts separated four raiders. A hand-held lantern was added to the FG mask; the mounted gate lantern was not separated. LaMa restored the wall and ground behind the raiders with a 31-pixel expanded inpaint mask. The padded LaMa output was cropped back to the exact source canvas of 1672×941.
- The static recomposite retained the gate and architecture. `layered_render.py` rendered `parallax-right-camera-left`, 163 visible frames at 30fps, scale 1.10 and 4.5% travel, to 2560×1440. G08 followed the layered render. The encoded G08 file contains 165 frames (163 visible plus two tail frames), H.264/yuv420p, BT.709 limited. Full-frame and subject-crop contacts at start/middle/end were inspected. This is author inspection of one scene, not independent review or full-video QA.
- Trial assets: `../../Work/image-motion-038-v01/layered-trial/S001/`; contact sheet: `../../Work/image-motion-038-v01/layered-trial/S001/motion_2k_contact.png`.

## S002 — layered pilot

- Automatic SAM2 proposals selected roofs and small fragments rather than the raiders, so they were not used as matte content. Prompted SAM2.1 separated a near pair of raiders for the FG. LaMa restored the original 1672×941 canvas behind them; the static recomposite was inspected at full frame and enlarged subject crop. The layer is a pilot and still needs review within the actual timeline context.
- `layered_render.py` rendered `parallax-left-camera-right`, 166 visible frames at 30fps, scale 1.10 and 4.5% travel, to 2560×1440. G08 followed the layered render. The encoded file contains 168 frames (166 visible plus two tail frames), H.264/yuv420p, BT.709 limited. `ffprobe` confirmed dimensions, frame rate, pixel format and color tags. Start/middle/end contact images were inspected; the whole-image pan keeps the procession in frame. This remains author inspection, not independent review or approval for import.
- Trial assets and receipt: `../../Work/image-motion-038-v01/layered-trial/S002/`; contact sheet: `../../Work/image-motion-038-v01/layered-trial/S002/motion_contact.png`; G08 receipt: `../../Work/image-motion-038-v01/layered-trial/S002/G08_FINISH_RECEIPT.json`.

## S003 — layered pilot

- Prompted SAM2.1 masks cover the three visible raiders and the overlapping dark figure behind the center raider. A small manual matte addition closes a remaining gap. LaMa restored the background with a 51-pixel expanded inpaint mask; the recomposite was checked full-frame and in an enlarged subject crop.
- `layered_render.py` rendered `parallax-left-camera-right`, 124 visible frames at 30fps, scale 1.10 and 4.5% travel, to 2560×1440. G08 followed the layered render. The encoded file contains 126 frames (124 visible plus two tail frames), H.264/yuv420p, BT.709 limited. Start/middle/end contact frames were inspected; this is author inspection only, not independent review.
- Receipt: `../../Work/image-motion-038-v01/layered-trial/S003/SCENE_MOTION_RECEIPT.json`. No pilot is imported into Palmier.

## Remaining work

Prepare and inspect a scene-specific foreground matte and opaque background repair for S004–S142 and ES01–ES02; then render each exact timeline span, apply G08 after camera, inspect vulnerable subjects/cue edges and start/middle/end frames. The source images are 1672×941 and the timeline is 2560×1440 at 30fps. Preserve original stills, IDs and hashes. Do not apply legacy DepthFlow or claim complete motion based on these two pilots.

Before publication, check the terms for the actual SAM2 checkpoint, LaMa package/model and any generated-background derivatives. The pilot notes record implementation provenance; they do not establish licensing or public-use acceptance.

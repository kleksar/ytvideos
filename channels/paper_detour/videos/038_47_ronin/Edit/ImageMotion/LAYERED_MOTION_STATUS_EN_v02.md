# Paper Detour 038 — layered motion status EN v02

**User decision:** continue with the current layered-motion standard. **Current state:** one S001 mask/inpaint/motion pilot is visually inspected; a 144-scene production batch has not been prepared or applied.

## Required method

The current `ytv-image-motion` standard (3 November 2026) uses the original still, a separately prepared RGBA foreground, and a restored opaque background. The clean layered parallax is rendered first, then the whole image moves in the opposing direction, then G08 and editor overlays. For the approved renderer, input is `foreground` plus `background`; there is no separate middle-ground input. See `../../../../../.agents/skills/ytv-image-motion/references/layered-motion.md`.

## Verified Palmier state

- Project `FE6B0E4C`; source assembly `AC510A6E` is retained. Production/music branch `51E4D60B` is separate.
- The legacy `run.py apply` prepared 144 temporary derivatives, then returned HTTP 404 before recording any Palmier operation. No `pending.json`, receipts, `target_before.json` or target ID exist for that run.
- Direct Palmier MCP readback confirmed `51E4D60B` still contains its original 142 stills, two endscreen stills, 13 accent clips, voice `[0,18424)` and music `[420,18420)`. No motion clip was imported or applied.
- The second apply attempt stopped at the current preflight because legacy DepthFlow cannot implement the accepted opposed layered motion. No mutation followed. `Work/image-motion-531dbf2675c38b40310c/scratch/` is now observed empty (0 files, 0 bytes). No project file or shared cache was deleted.

## S001 pilot — not yet a production asset

- Local SAM 2.1 runs in `/Users/diplomat/paper-detour-sam2-local`. The Vision automatic foreground instance mask was too broad. A first LaMa attempt that removed both the figures and the gate visibly damaged the gate; it was rejected and not used.
- Manual SAM 2.1 point/box prompts for the four small raiders produced a much tighter foreground mask. A small lantern held by a raider was added manually to the same foreground; the mounted gate lantern was not separated.
- LaMa restored the wall and ground behind only the raiders, using a 31-pixel expanded inpaint mask. The background was cropped back to the exact original 1672×941 canvas after the package returned a padded 1672×944 result. The static recomposite was visually compared with the original and retained the gate/architecture.
- `layered_render.py` rendered S001 as `parallax-right-camera-left`, 163 frames at 30fps, camera scale 1.10 and 4.5% travel. Actual output is H.264 1920×1080 `yuv420p`, 30/1, 163 frames. Start, middle and end frame contacts were inspected at full-frame and subject crop; this is one-scene visual evidence only, not a full-motion or independent review.
- Trial inputs and outputs are in `../../Work/image-motion-038-v01/layered-trial/S001/`. Preview file: `../../Work/image-motion-038-v01/layered-trial/S001/motion_contact.png`. No trial output was imported into Palmier.

## Remaining work

Prepare a scene-specific foreground matte and background repair for each accepted S002–S142 and ES01–ES02, inspect each before layered rendering, and verify the resulting start/mid/end and vulnerable subject/cue edges. Source images are 1672×941; the current renderer encodes 1920×1080 before Palmier scales clips to the 2560×1440 timeline, so inspect softness against the export profile. Retain G08 after camera. Do not fall back to legacy DepthFlow or claim full motion based on the S001 pilot.

Before publication, check the terms for the actual checkpoint, inpainting package/model, and any generated-background derivatives. The current pilot note records implementation provenance; it does not clear licensing or public-use acceptance.

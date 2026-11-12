# Scene 05 — walking-date environment

**Status:** `DRAFT`. This folder has a clean environment plate and one candidate foreground cutout. Whole-character poses for N/B/M now exist in `../character_continuity/poses/`, but they have not been registered to this path or assembled into a tested three-plane composite.

## Files

- `scene05_walk_background_v01.png` — initial opaque RGB environment, 940×1672. Anonymous outdoor passage with generic architecture, windows and greenery; not the preferred version because some details may look like a shop or imply fair weather.
- `scene05_walk_background_v02.png` — preferred clean background, opaque RGB, 941×1672. Same broad perspective and path, but removes clouds, doors/windows and close foliage. It reads as an anonymous everyday walkway, distinct from the explicit park geography of scenes 12–18.
- `scene05_walk_foreground_v01.png` — one small leafy paper sprig entering from the bottom-left edge, RGBA with non-opaque alpha, 941×1672. Its canvas matches background v02 exactly. Keep its footprint restrained so it does not cover narrator N in the planned left position or become a full-screen curtain.

## Planned assembly

Candidate order: `scene05_walk_background_v02.png` (BG) → registered whole-character planes for N, B and Matt from `../character_continuity/poses/` (MG; not yet registered to this scene) → `scene05_walk_foreground_v01.png` (FG) → the spoken accent `THERE TOO` at the Matt reveal → continuous moving grain at the final montage stage.

The scene score calls for a waist-up three-quarter composition, with N left, B center, Matt right; legs remain below the crop so no walking-limb animation is required. The foreground sprig is only an authored depth edge. Do not invent a particular city, shop, season, weather event, props, or motive. This walk geography must stay distinct from the later park scene.

## Source and checks

- Generated with the built-in OpenAI imagegen tool. Approved Paper Detour diorama art was used as paper-material reference; the user-selected Paper 004 scene 38.08 was used only for depth and paper-edge principles. Its room, phone, character and furniture were not copied.
- Background v01 source: `/Users/diplomat/.codex/generated_images/01a194ca-6f84-7360-b821-dda96d304209/exec-a5844c0d-9b13-4707-ace8-8789a11bb312.png`.
- Background v02 source: `/Users/diplomat/.codex/generated_images/01a194ca-6f84-7360-b821-dda96d304209/exec-54c0fb9c-f70d-4217-a1b0-4e79d7cbb056.png`.
- Foreground v01 source: `/Users/diplomat/.codex/generated_images/01a194ca-6f84-7360-b821-dda96d304209/exec-ca385e8b-f228-49b9-99a3-4f87383ca558.png`.
- Verified file properties: preferred BG and FG are both 941×1672; BG is opaque RGB; FG is RGBA and non-opaque.
- Visually inspected all selected images. BG v02 has no people, readable signs or products. FG v01 is a small bottom-left leaf cutout; a narrow warm edge remains visible and must be checked against the true composite.
- Not checked: registration to the future character master, actual size/occlusion in Palmier, alpha fringe against BG, contact shadows, parallax or phone-size readability. These assets are not imported into Palmier and do not establish completed movement.

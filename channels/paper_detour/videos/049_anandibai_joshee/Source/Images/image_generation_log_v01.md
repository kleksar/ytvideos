# Generation and review log v01

Scope: early representative subset for the accepted storyboard. Requested video canvas is 2560×1440, 30 fps. imagegen exposed no resolution control; observed native PNGs are 1672×941 (16:9), so output preparation must disclose the upscale. All selected images are whole-scene handmade paper-stage illustrations. Source images remain in `/Users/diplomat/.codex/generated_images/01a1a8c1-33fb-7581-a23c-2b6065a4dee2/`; selected immutable copies are under this episode's `Source/Images/Long/en/`.

## Accepted early subset

| ID | Generated result | Narrative job / review | Supplied references |
|---|---|---|---|
| 01 | `scene_01_v01.png` — SHA256 `6952444401d833a562f5bc9861d8237d7bae6f0167583807951e73a83413ade3`; 1672×941 | Empty cradle, screen, white chair and readable symbolic absence; detailed scene floor continues through the lower area, no blank subtitle banner. | P04 style only. |
| 03 | `scene_03_v01.png` — SHA256 `ad89b8293415f1af4bbeeda1bfa8986b93664a277e256f4ee4adbf40470eab8b`; 1672×941 | Wide layered ocean, India/US landforms and a symbolic path; not marked as an exact voyage route. | P04 style only. |
| 04 | `scene_04_v01.png` — SHA256 `e4e69f3fd6ca1d947133b855a9271daae7591b9dc5aa8544fbfedaf0e1d390e3`; 1672×941 | Threshold figure, Philadelphia medical college, women in a distinct Indian space. Building and identity use separate references; no lower banner. | P04 style; North College Avenue 1875 building; 1885 group portrait for identity/clothing, not pose/framing. |
| 19 | `scene_19_v01.png` — SHA256 `7fcb90f15ce792713f514dbbf74085583c021cb94a8a6ccd969f7eebdb0ceff0`; 1672×941 | Transfer of a covered plate and prepared books make Bodley's practical help legible. Actual faces/hands still need close inspection at final source size before final acceptance. | P04 style; 1885 group portrait for identity/clothing only. |

Early review is provisional: all four are individually inspected at displayed full-frame resolution; no motion/subtitle composites or other final PNGs have been accepted yet. Images shown as final assets must be the selected versions above, not rejected alternates.

## Exact generation prompts

### S01 — selected generation `exec-70036f8f-eec7-48be-833a-b3744290fa43.png`

> A complete single 16:9 layered cardstock Paper Detour diorama, full-bleed composition edge to edge; visible hand-cut paper edges, folds, subtle paper grain, dimensional cast shadows, crafted theater set. An intimate Indian home in 1878, strong diagonal overhead view. Place a small empty infant cradle at left-center, its woven paper form clearly readable, and a small white physician's chair behind a partially open screen at right-center; the chair casts a long theatrical shadow toward the cradle. Show a room with continuous richly patterned terracotta-and-indigo paper floor, low-salience floor detail even in the bottom subtitle line; no empty lower margin, blank panel, banner, or framing border. Keep only the line across the very bottom-center clear of the cradle and chair, while surrounding floor remains part of the scene. Warm narrow light, strong hook. No baby or person, no death depiction, no text, no labels, no watermark, no photorealism.

### S03 — selected generation `exec-e7544364-1dcf-4fff-a986-dc846db3a91e.png`

> One 16:9 Paper Detour cut-paper diorama photographed almost vertically from above: a broad Indian coastline at left, vast layered deep-blue paper ocean across the middle, distant American coastline at right. A thin cream paper path begins at the Indian shore and reaches toward the far coast, a symbolic future journey, not a precise historic route. Very wide scale, restrained terracotta/indigo/cream, fine paper edges and cast shadows, coherent composition with subtitle region free of essential landmarks. No labels, no compass, no text, no ships, no photorealism, no watermark, one scene.

### S04 — selected generation `exec-d10670cd-892c-498a-a537-b69b940c4960.png`

> Create a complete full-bleed 16:9 Paper Detour handmade layered-paper diorama of an early-1880s Philadelphia medical college entrance. The supplied 1875 North College Avenue photo is the exact exterior-construction/location-era anchor: retain its real brick, fenestration and massing as recognizable visual clues, then make a new low camera view with a central open doorway. The supplied 1885 group photo is only identity/clothing reference for Anandibai Joshee, shown as a small figure from behind at the threshold; do not copy the source pose or framing. Compose the important college architecture on the right and an integrated, clearly symbolic Indian home scene on the left with several women, connected by a band of light to her educational purpose. Crafted paper layers and visible cut edges, rich depth, no lower blank banner, foreground paving remains detailed and physically part of the scene. No text, no inscriptions, no modern elements, no photorealism, no historical event beyond the spoken narration.

### S19 — selected generation `exec-24d80b16-3eb7-4fcc-bb0f-aee3d74dd8b2.png`

> Create one complete 16:9 Paper Detour diorama, an unmistakably handmade layered paper-cut theater set, not photorealistic and not a realistic 3D miniature. Show a quiet Philadelphia home interior in 1884. A young Indian woman based on the woman at the far left of the historical group-photo reference sits at a simple table; a middle-aged white woman dean stands opposite, gently offering a covered plate. Suggest the dean's practical support through the meal and a prepared place for books and personal belongings, without melodrama, illness symptoms, or a specific identifiable dish. Use visibly cut cardstock faces and clothing, paper folds, exposed cut edges, layered planes and soft cast shadows; crafted textures should read as paper, not stone, wood or fabric. Medium side view, intimate but clear, warm doorway light. Keep both women's hands, the plate, and the prepared books visibly above the lower-center subtitle area. Historically restrained late-19th-century dress. One scene only, no text, no collage grid, no watermark, no sources, no modern objects, no photorealism.

## Rejected generations

- Scene 01 first attempt: cradle crossed the subtitle baseline; do not use.
- Scene 01 second attempt: major objects were shifted up, but the lower half became a largely empty floor field contrary to the approved full composition; do not use.
- Scene 02 first attempt and scene 04 first attempt: each introduced a large blank lower banner/base; do not use.
- Scene 04 no-accurate-building-reference attempt: not used because the episode has an actual 1875 WMCP building anchor.

## Reference identities and current limitations

- P04 style anchor: `channels/paper_detour/brand/References/meaningful_staging_20261105_v01/P04_last_radio.png` (style only).
- Anandibai identity: `Research/VisualRefs/anandibai_joshee_1885_group.jpg` (1885 group portrait; identity/clothing only; subject is leftmost; not a pose/camera template).
- Building: `Research/VisualRefs/wmcp_north_college_1875_nlm.jpg` (period campus anchor; not the earlier Arch Street building).
- Native output is below the 2K delivery canvas and will need a measured upscale in FFmpeg. Do not label generated source files 2K/4K.
- Still unresolved for every not-yet-generated scene: exact pose/prop/protected-detail review; planned camera envelopes; final subtitle and motion compositing; independent playback review.

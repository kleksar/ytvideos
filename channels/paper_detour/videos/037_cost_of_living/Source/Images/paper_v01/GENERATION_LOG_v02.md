# Paper scene image reframe log v02

**Scope:** four targeted edits to remove per-scene zoom caps before motion work. The previous versions remain unchanged. Selection is the author’s under the user’s standing “на твой вкус” delegation; no independent review.

Built-in imagegen edit mode; local project files used as edit targets. No destination path control was applied. 4K UHD landscape was requested in each prompt; all returned PNGs measured 1672×941 RGB (the actual native size, not 4K). All four are the same pixel dimensions as their superseded images.

Style references used in every edit:
- `channels/paper_detour/Shared/References/Paper/paper004_user_38.png` — SHA-256 `238bb11958c8e59224edcd006db060df0bddd0c9e100f795e44eeb537ebdc166`.
- `channels/paper_detour/videos/033_time_stop/Source/Images/paper_v01/S01_v01.png` — SHA-256 `700b11da5d3c4c0bc1032eb1f48b3bdb7373378865b94cdf33184e9921b048f0`.

| Scene | Edit target | Selected new image | SHA-256 | Content/style/framing review |
|---|---|---|---|---|
| S05 | `S05_v02.png` | `S05_v03.png` | `ee8d77d89ef9a2d8ff93484a359c1223bd3bf6d6eafee216c7c1a2a68fcd7604` | 20-segment ring and empty basket retained; amber/pale proportions remain legible; whole pair moved into a generous central margin. |
| S45 | `S45_v05.png` | `S45_v06.png` | `3ba65e80a9881a796a44ddcc3bcc94e10c4dee1fb1ad34c9caa09df113c65ada` | Full symbolic tile row and empty four-part basket retained; complete row now centered with large side margins. |
| S60 | `S60_v03.png` | `S60_v04.png` | `4643090a2860faa35d24ee573b02138c651c916973a90896e000b8d18ed0db4e` | Both tables and both matching baskets with existing contents retained; left/right budget-space relation preserved; margins widened. |
| S65 | `S65_v03.png` | `S65_v04.png` | `22eedff90ece575d3f7a81ad5df5b5225995dbb8c4211737cfecb29e8268de13` | All three empty baskets retained in same order and size relation; generous centered framing. |

The images were viewed individually full-frame. The protected objects visually remain within a conservative centered camera-safe window; image-level review does not prove depth-mask quality, parallax edge fill, intermediate-motion safety or final-film QA. Recheck those on actual frame samples before accepting motion.

## Prompts

### S05

> Edit target image S05_v02 only. Preserve its exact instructional scene: one complete landscape 16:9 handmade paper/card diorama, an overhead paper year-ring with exactly 20 equal segments, exactly 14 consecutive amber segments and 6 pale cream segments, plus one separate empty low woven-paper basket. Preserve the current objects, colors, count, visual meaning, paper texture and overhead camera. Recompose by reducing the entire ring-and-basket group modestly and placing it centrally, with all physical objects and shadows comfortably inside the central 78% of the frame width and central 78% of frame height. Keep full-bleed background to all four edges. This added margin must safely preserve every segment and the complete basket during gentle centered zoom and depth parallax. Style references: Paper004 is the primary guide for tactile layered card, lighting and depth; 033 S01 is a secondary guide to paper material. Do not copy either reference's story, people or layout. Maximum available image quality and native resolution; request 4K UHD 3840x2160 landscape. No people, food in basket, additional props, text, labels, numbers, symbols, logos, borders, empty bands, photorealism, vector art or glossy 3D.

### S45

> Edit target image S45_v05 only. Preserve its exact scene: one long horizontal trail of identical small amber paper wage-day tiles leading into a plain empty four-compartment paper needs basket at the right end, on a dark ink-blue paper field. The tile count is symbolic, not exact. Preserve the table-level/overhead clean composition, no people, no new props and no text. Recompose by reducing the entire tile-row-and-basket group modestly and placing it centrally, with all tiles, basket and shadows inside the central 78% of the frame width and central 78% of frame height. Keep full-bleed ink-blue background all the way to all four edges. Added margin must preserve the full tile row and complete basket during a gentle centered zoom and depth parallax. Style references: Paper004 is primary guide for tactile layered card, lighting and depth; 033 S01 is secondary guide to paper material. Do not copy reference content or layout. Maximum available image quality/native resolution; request 4K UHD 3840x2160 landscape. No room, buildings, extra objects, food, people, coin faces, writing, numbers, labels, symbols, logos, borders, empty bands, photorealism, vector art or glossy 3D.

### S60

> Edit target image S60_v03 only. Preserve its exact comparison and all existing meaningful objects: two handmade paper tables side by side; on the left table, the benchmark annual-needs basket occupies most of its smaller budget field; on the right table, the matching but smaller basket sits in a larger earnings field with a clearly visible perimeter. Keep the same basket contents and the left/right size relationship exactly as in the target. Preserve overhead/table-level perspective, paper materials, lighting, shadows and dark blue background. Recompose by reducing the entire paired-table-and-basket group modestly and centering it so both full tabletops, the large basket, small basket, all contents and shadows lie within the central 78% of frame width and central 78% of frame height. Keep full-bleed background to all four edges. The extra margins must protect every prop during gentle centered zoom and depth parallax. Style references: Paper004 is primary guide to tactile layered card, light and depth; 033 S01 is secondary paper-material reference. Do not copy subjects or layout from style references. Maximum available image quality and native resolution; request 4K UHD 3840x2160 landscape. No new objects, people, symbols, writing, labels, numbers, logos, borders, empty bands, photorealism, vector art or glossy 3D.

### S65

> Edit target image S65_v03 only. Preserve its exact meaning and objects: three empty woven handmade paper baskets with clearly different sizes, side by side on an ink-blue tabletop, no contents, people or labels. Keep each basket's relative size and order unchanged; keep their paper weave, contact shadows, warm edge light and blue background. Recompose by reducing the entire three-basket group modestly and centering it so all three complete baskets and their contact shadows are inside the central 78% of frame width and central 78% of frame height. Keep full-bleed paper background across all four image edges. Added margin should safely preserve each basket during gentle centered zoom and depth parallax. Style references: Paper004 is the primary guide for tactile layered card, lighting and depth; 033 S01 is secondary guide for paper material. Do not copy reference subjects or layout. Maximum available image quality and native resolution; request 4K UHD 3840x2160 landscape. No extra baskets, items, writing, numbers, symbols, logos, borders, blank bands, photorealism, vector art or glossy 3D.


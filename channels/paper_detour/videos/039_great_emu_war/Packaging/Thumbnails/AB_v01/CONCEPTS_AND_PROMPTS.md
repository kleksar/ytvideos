# Paper Detour 039 — title/thumbnail A/B package v01

Release status (2026-11-03): A was used for the initial upload. After the user's direct request to make the film Public, Studio showed the native title-and-thumbnail experiment running with all three pairings A/B/C; no result is available yet. Local master PNGs, previews and the accepted MP4 were removed under the TEXT_ONLY archive; the Studio-side experiment remains active and does not depend on these local files. See `../../Metadata/Release_v02/RELEASE_REPORT_v02.json` and `../../../Edit/MediaLifecycle/TEXT_ONLY_DELETE_RECEIPT_v01.json` for current release and archive status, and `../../Metadata/Release_v01/RELEASE_REPORT_v01.json` for the original upload snapshot. All pairings refer to the accepted long film. The script is locked and was not revised or rechecked for this packaging work.

## Paired concepts

| Variant | Viewer promise | Exact title | Exact lettering | Scene |
| --- | --- | --- | --- | --- |
| A | What went wrong at the dam? | The Machine Gun Jammed. The Emus Kept Coming. | THE FLOCK CLOSES IN | Static defensive position beside the dam; the advancing flock is the visual focus, with soldiers and gun smaller in frame. |
| B | Why couldn't the truck stop the emus? | Why a Machine Gun Truck Couldn't Catch the Emus | ROUGH TERRAIN, FAST BIRDS | Dynamic side view of a period truck bucking over rough ground while emus run ahead; truck movement is the focus. |
| C | What remained for farmers after the army left? | The Army Left. The Emus Came Back. | FARMERS LEFT EXPOSED | Farmer at a broken fence in the foreground, with emus beyond it and the empty road receding behind. |

The pre-generation distinction check found all three angles separate. A/B is the closest pair, so A centers the approaching flock at a fixed dam position and B centers the moving truck and pursuit. A/B, A/C, B/C are all distinct enough for a package comparison. This is an editorial distinction check, not a prediction of click performance.

## Post-generation comparison

- **Titles:** A is about the jam at the dam; B asks why the truck could not catch the birds; C is about the army's departure and the emus' return. Each tells a different part of the accepted film. Lengths are 45, 47 and 34 characters respectively, before any separately approved hashtags.
- **Covers without relying on lettering:** A is a static position beside water with the flock advancing as the largest shape. B is a left-to-right truck pursuit over rough ground. C is a farmer at a broken fence looking toward emus in the field after the army has left. These are visibly different story moments and hierarchies.
- **Pairwise result:** A↔B pass; A shows the encounter at the dam while B shows the moving truck on the track. A↔C pass; an impending military encounter is distinct from a farmer facing the aftermath. B↔C pass; a pursuit in motion is distinct from the quiet consequence at the farm. The phrase/title pairs add context without simply repeating each other.
- Preview size inspected: 320×180 local render from the thumbnail preview helper. Exact phrase spelling and legibility pass on all three. Lower-right essential content is left clear in B and C; A's lower-right holds water/background. No live YouTube card/overlay or physical mobile display was inspected.
- Package state: three title/cover pairs and complete descriptions are in the Release_v01/v02 metadata package. The user approved the film and packaging and directly requested Public access plus A/B testing; Studio now reports the native title-and-thumbnail experiment active. Current release state is recorded in `../../Metadata/Release_v02/RELEASE_REPORT_v02.json`.

## Visual construction

Create three landscape 16:9 YouTube covers as complete handmade matte paper/card dioramas. Use `../../../../Shared/References/Paper/paper004_user_38.png` only for paper material, layered cut edges, tactile fibers, physical volume and soft contact shadows. Its people, room, lighting palette and composition do not belong to this story. Match the accepted 1932 Western Australian farming world described in `../../Source/Images/VISUAL_BIBLE_v02.md`: dry ochre ground, restrained wheat gold, weathered timber and wire, pale dusty sky, muted dam water, khaki soldiers and large dark gray-brown emus. Use a clear foreground, middle ground and background, believable physical support, rich craft detail and legible silhouettes. No photorealism, CGI gloss, split panels, collage, borders, watermark or extra lettering.

### A — `PD039_AB_v01_A.png`

Single landscape 16:9 composition. A wide, slightly low view from the dam bank: a compact khaki soldier position and period machine gun sit off to one side; a large flock of emus advances toward the water as the dominant shape and visual direction. The flock is the largest, clearest element; the weapon is visible but secondary. Leave clean upper-left sky for exact large rounded handmade paper lettering: `THE FLOCK CLOSES IN`. Add no other text. The moment communicates the impending dam encounter without depicting a shot or inventing casualties.

### B — `PD039_AB_v01_B.png`

Single landscape 16:9 composition. Dynamic three-quarter side view of the recurring simple period truck on rutted dry ground, its mounted gun secured to the bed; wheels jolt over uneven terrain while a small group of whole-body emus runs ahead into open space. The truck motion and rough track are the dominant diagonal; keep the birds clearly in front. Reserve clean upper-left dusty sky for exact large rounded handmade paper lettering: `ROUGH TERRAIN, FAST BIRDS`. Add no other text. No muzzle flash, firing, injury or exaggerated speed marks.

### C — `PD039_AB_v01_C.png`

Single landscape 16:9 composition. A broad farm view after the army has departed: anonymous recurring farmer in a broad-brimmed hat and plain light shirt stands at a broken timber-and-wire fence in the foreground, looking toward emus beyond it; an empty dirt road recedes toward the pale horizon. The farmer, gap in the fence and birds form one readable cause-and-consequence line. Leave clean upper-left sky for exact large rounded handmade paper lettering: `FARMERS LEFT EXPOSED`. Add no other text. Do not depict the army or imply a specific new attack.

## References and checks

- Paper style reference: `../../../../Shared/References/Paper/paper004_user_38.png` (material and lighting reference only).
- Accepted story visual reference: `../../Source/Images/VISUAL_BIBLE_v02.md` (period, recurring cast/objects, landscape palette and continuity).
- Title consultation: project Extra High chat “Английские заголовки фильма”, 2026-11-03.
- Thumbnail lettering consultation: project Extra High chat “Надписи для обложек”, 2026-11-03.
- Distinction consultation: project Extra High chat “Оценка различимости концепций”, 2026-11-03.
- Generated masters, native sizes, actual spelling inspection, 320×180 previews and image-by-image observations are appended after generation.
- The user approved the packaging for the upload. Variant A is the current display while native A/B/C testing runs. Live experiment outcome remains pending; see `../../Metadata/Release_v02/RELEASE_REPORT_v02.json`.

## Final generation prompts

The accepted Paper004 reference was included in each call for material, cut edges, fibers, volume and physical shadows only.

### C final prompt

Create a 16:9 landscape YouTube thumbnail as one finished edge-to-edge handmade matte paper/card diorama. Use the reference only for tactile paper material, visible fibers, layered hand-cut edges, physical volume and soft shadows. Story world: Western Australian farm in 1932, dry ochre land, wheat gold, pale dusty sky, weathered timber and wire fence, recognizable dark gray-brown emus, anonymous farmer in broad-brimmed hat and light work shirt. Show the aftermath of the army leaving: farmer stands beside a broken fence gap and looks toward emus still in the field. Compose the farmer at center-right around mid-height, fully visible and not at the right or bottom frame edge; place the broken fence gap in the center, with several emus beyond it at center-left. Keep the lower-right corner as clear open ground/grass with no essential subject, reserved for YouTube duration overlay. An empty dirt road recedes toward the horizon; no soldiers or truck. Calm unresolved mood, no attack. Rich layered paper diorama with believable supports and contact shadows. Leave clean upper-left sky for exact large rounded dimensional handmade-paper lettering “FARMERS LEFT EXPOSED”, all caps. Only those words, no other text, border, watermark or panels. Readable at 320×180.

### B final prompt

Create a 16:9 landscape handmade paper/card diorama thumbnail for a YouTube long film, edge-to-edge. Reference only controls tactile paper, hand-cut layered edges, visible fibers, dimensionality and soft contact shadows. Story: 1932 Western Australian farm track. Put a plausible modest period truck in the LEFT-CENTER, viewed three-quarter side, jolting across uneven ochre ruts. Two small khaki soldiers ride it; a compact infantry-sized Lewis gun on a simple mount is visible in the truck bed, no larger than a person, not firing. Ahead of it, a small group of 4–5 dark gray-brown whole-body paper emus runs across the CENTER toward open ground at middle-right. The truck and birds form a clear left-to-right pursuit diagonal, with visible rough terrain explaining the truck's jolting. Distinct dynamic action rather than a static dam scene. Reserve the UPPER-RIGHT pale sky for the only text, exact all-caps lettering on two lines: “ROUGH TERRAIN” / “FAST BIRDS”. Render large rounded dimensional handmade paper letters, clear and crisp with soft shadows. Keep important story elements out of the lower-right corner, which stays open dusty ground for duration overlay. Rich crafted paper detail, believable support and silhouettes; no photorealism, blur, muzzle flash, injury, extra words, labels, panel, collage, border or watermark. Readable at 320×180.

### A final prompt

Create a polished YouTube long-film thumbnail, landscape 16:9, one edge-to-edge finished handmade paper/card diorama. Reference image is strictly a material reference for paper texture, physical layered cut edges, tactile fibers, volume and soft contact shadows only; do not copy its room, character, colors or layout. Story: Western Australian farming landscape in 1932, dry ochre soil, muted water at a farm dam, pale dusty sky, restrained khaki soldiers, recognizable large dark gray-brown paper emus. Wide slightly low viewpoint from the dam bank. Composition: a compact soldier position and period machine gun placed off to one side; weapon clearly visible but secondary; a large flock of emus advances toward the water as the dominant shape and visual direction. The flock is the largest, clearest element; the weapon is visible but secondary. The moment is tense but nonviolent; no firing, no casualties, no blood. Layered matte paper, hand-cut rounded edges, visible fibers, credible physical support and contact shadows, rich crafted material detail, strong readable silhouettes. Keep the upper-left dusty sky clean as a lettering field. Render exactly this phrase as large, crisp, rounded, slightly irregular handmade paper letters with physical thickness and soft shadows: “THE FLOCK CLOSES IN”. Exact spelling, all caps. This is the only text anywhere in the image. No labels, no title beyond the phrase, no borders, watermark, panels or collage. High-contrast readable composition at 320×180.

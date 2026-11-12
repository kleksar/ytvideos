# Text revision v03 — generation record

Tool: built-in `image_gen.imagegen`, edit mode, `transparent_background=false`. Requested high quality 2560×1440 or greater, landscape 16:9; actual result 1672×941. Quality and size were specified in prompts; the built-in interface provided no separate quality/size controls. Images remain original native size; export scales proportionally. Exact inputs and output paths are indexed in `Edit/Production/v03/plan.json`, while the actual tool requests and result paths were emitted in the session. Image 025 was omitted from montage because the oversized sign was implausibly placed on the runway. Editing was performed with the actual prior image as target, not an overlay.

Common brief: Regenerate the existing documentary scene, preserve its subject, pose, viewpoint, lighting and photorealistic setting. Integrate specified exact English text as a physical exhibit sign or card, never a screen-space overlay, no other lettering or watermark. Keep the bottom quarter clear for the separate subtitles. Protect the composition through gentle full-frame movement.

| Shot | Edit target | Text on generated object | Additional actually supplied references |
|---|---|---|---|
| 004 | scene_003_v01.png | TU-160 / WHITE SWAN | traveler turnaround, traveler emotions, Tu-160 photo |
| 011 | scene_008_v01.png | LONG RANGE / HIGH SPEED | traveler turnaround, traveler emotions |
| 039 | scene_031_v02.png | A NEW DESIGN | Tu-160 photo |
| 043 | scene_035_v01.png | WINGS EXTENDED | Tu-160 photo |
| 062 | scene_051_v01.png, then shot_062_text_v01.png | FORWARD / SWEPT | Tu-160 photo, both passes |
| 064 | scene_053_v01.png | NK-32 | traveler turnaround, traveler emotions, NK-32 photo |
| 074 | scene_062_v01.png | SPEED COSTS FUEL | Tu-160 photo |
| 102 | scene_083_v01.png, then shot_102_text_v01.png | NOT ALONE | traveler turnaround, traveler emotions, Tu-160 photo, both passes |
| 108 | scene_087_v01.png, then shot_108_text_v01.png | AIR • LAND • SEA | Tu-160 photo, both passes |
| 119 | scene_096_v02.png, then shot_119_text_v01.png | SERIAL PRODUCTION | Tu-160 photo, both passes |

The prompts for character scenes additionally require the 2D illustrated traveler to retain dark outlines and color shading, facial identity, mustard coat, backpack, existing gesture and both hands, as a present-day guide outside the historical action. Aircraft and engine references are construction anchors, not purported archive images. All generated scenes are explanatory reconstructions. Reference hashes and provenance of the real photographs remain in `Research/VisualReferences/README.md`; the two character-anchor hashes are in the channel visual profile.

Four final legibility refinements used the following exact shared prompt followed by the relevant specific instruction below:

> Edit input 1, the existing 16:9 documentary scene, to make its existing physical text legible on a phone. Preserve viewpoint, lighting, all aircraft and the real material environment. No screen-space caption, no watermark. Request high quality 2560x1440 landscape, framing safely clear of the lower quarter for subtitles. One precise change:

- 062: Replace the two small nameplates with much larger physical exhibit placards positioned behind their respective model planes, at a readable viewing angle with large bold high-contrast sans-serif words exactly 'FORWARD' and 'SWEPT'. Do not cover the wings, keep both aircraft unchanged. Nothing else should be written.
- 102: Replace the existing lengthy card wording with large bold high-contrast exact words 'NOT ALONE'. Enlarge this physically plausible card somewhat while keeping it on the table, the single aircraft and globe visible. Preserve the traveler as a drawn 2D character with dark outlines and colored shading, his face and mustard jacket, right palm raised, left finger pointing to the aircraft. Do not add people or writing.
- 108: Enlarge the existing rear museum sign and its lettering to be legible on a phone; exact words 'AIR • LAND • SEA' in large bold light letters. Keep sign within image margins above the models. Keep the plane, silo and submarine intact and no people.
- 119: Enlarge the existing cream exhibit card and its lettering in the same position for phone readability, with exact large bold words 'SERIAL PRODUCTION'. Keep every aircraft model and the assembly rail visible. No people or extra writing.

The exact selected initial call components are recorded below. The first-pass outputs and the final versions have distinct names and hashes. No synthetic archive or original historical quotation was asserted.

## Initial exact prompt components

The exact outgoing prompt was the relevant shared component joined verbatim with the shot-specific suffix. Reference lists above identify the actual target and anchors.

### Early sample shared component (004 and 043)

Create a finished cinematic 16:9 still image for an English-language historical documentary, requested high quality 2560x1440 or higher, with safe central composition for gentle whole-image pan/zoom and subtitle bar at bottom. Regenerate the given scene with meaning-bearing English text physically present in the photographed space, not digitally overlaid. Preserve the exact narrative action, photography, viewpoint, daylight, aircraft geometry and other objects in the source; the space must remain photographic. Do not place text on the aircraft, do not add logos, captions, interface, random lettering or watermark. The text must be spelled exactly, large, readable, and not in the bottom quarter.

004 suffix: Input 1 is the actual scene to revise; inputs 2 and 3 are the character identity and illustration style; input 4 is an aircraft identity reference, not a photo to copy. Preserve the 2D drawn traveler at right, with visible dark drawn outlines and soft coloured shading on face, hair and clothes; his right palm remains open toward the aircraft, his left hand holds his backpack strap. Do not make him photographic or 3D. He is a present-day guide at an exhibit, not a historical participant. On a physically plausible, large museum panel in the background, install clearly readable exact English words 'TU-160' with 'WHITE SWAN' below. The panel is a real object in the space, perspective- and light-matched, framed near the aircraft without concealing the host, aircraft, or subtitle region. No other readable text.

043 suffix: Input 1 is the actual scene to revise; input 2 is an aircraft silhouette reference. Present-day photorealistic demonstration model on a metal table, wide extended wings fully visible, no person. Integrate a large real angled exhibit display fixed behind the model, with exactly the English text 'WINGS EXTENDED' prominently visible. The physical sign belongs to the present-day explanatory exhibit, has clean legible letters and no other writing. Keep its typography clear of the bottom quarter and protect the aircraft outline.

### Middle batch shared component (011, 039, 062 first pass, 064, 074)

Regenerate input 1, a scene still for an English historical documentary. Input 1 is the actual target composition, other images are identity/construction references. High quality, landscape 16:9, request 2560x1440 or greater. Preserve scene action, viewpoint, photorealistic world, props, light and construction; do not introduce new people. Integrate the exact English text on a real physical object belonging to this contemporary explanatory setting, never as an overlay. The text should be prominent, letter-perfect and high contrast, and stay above the bottom quarter reserved for separate subtitles. Do not add other text, logos, watermarks, graphics or invented historical documents.

Character component for 011 and 064: Preserve the drawn 2D traveler, no photoreal or 3D person: fine dark contours, colored shading, mustard jacket and backpack, same face as the two traveler reference images. Preserve his existing distinctive pose, gaze and both hands. He is a present-day guide outside the historical action.

011 suffix: The host indicates two physical aircraft models. On the back wall, create two separate real exhibit panels with exact text 'LONG RANGE' on the left and 'HIGH SPEED' on the right, relating each to its respective aircraft model. Preserve both models and all hands. No extra words.

039 suffix: Maintain the actual overhead camera and paper aircraft model and tools on the dark gridded cutting mat. Place one physical clean cream card in the upper-left open region of the mat, with exact large black printed words 'A NEW DESIGN'. Match shadows and perspective. No people; maintain aircraft and all tools; this is a contemporary explanatory model rather than an archival document.

062 first-pass suffix: Preserve exactly two physical models showing the same aircraft's extended and swept-back wings in the warm present-day explanatory setting. Add two real small museum name cards on the table behind their respective models, exact text 'WINGS FORWARD' for left and 'WINGS SWEPT' for right, readable with distinct materials. No other lettering. Keep two aircraft shapes and positions unchanged.

064 suffix: Preserve the traveler's open hand gesture toward the engine and his other hand resting at his hip. Preserve the single large jet engine and museum setting. Add one large real dark exhibit board behind and beside the engine, naturally lit and unobstructed, with exact large white lettering 'NK-32'. The engine reference is only a construction anchor. No extra writing.

074 suffix: Keep the physical relief world map, aircraft model and container of fuel as an illustrative model, not a real route. Add a single large physical card, located within the map's open northern ocean area, with exact text 'SPEED COSTS FUEL' in readable black letters. Do not add any extra route or assert a real mission.

### Final batch shared component (102, 108, 119 first pass)

Regenerate the supplied actual scene for a 16:9 English documentary, with requested native output 2560x1440 or more and high quality. Preserve scene composition, subject, pose, number of objects, viewpoint, lighting and photorealistic setting. Add specified exact English words printed or engraved on an actual physical museum card or panel within this contemporary explanatory scene, not an overlay or historical record. Clear high-contrast text, no other lettering or logos, keep text away from bottom quarter for subtitles; preserve margins for gentle zoom and pan.

102 first-pass suffix: The actual illustrated traveler at left raises his right palm to caution the viewer while pointing with left hand toward one model aircraft in front of a globe: keep both hands, 2D face and clothing, dark outlines and soft color shading, he is not a photorealistic person or historical participant. Place a real modern museum panel within the right side of the scene with exact text 'ONE PART OF A LARGER FORCE'. Do not obscure the globe, the aircraft model or the traveler; realistic lighting, no others.

108 first-pass suffix: Keep the single aircraft model in the foreground and the silo model and submarine model behind it in a contemporary museum. Place one real elegant museum display sign in open space behind the models with the exact English words 'AIR • LAND • SEA'. Do not change the three objects or their relative positions; no people.

119 first-pass suffix: Preserve the three-dimensional exploded aircraft assembly model with its sections separated along rails. This is a contemporary explanatory construction, not a historical document. Add one real cream paper exhibit card on the tabletop in a clear empty area, with the exact words 'SERIAL PRODUCTION' in large dark print. Preserve the aircraft construction and blank display signs; no people.

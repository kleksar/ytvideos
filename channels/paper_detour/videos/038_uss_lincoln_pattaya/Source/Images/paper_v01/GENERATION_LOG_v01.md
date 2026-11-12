# Scene image generation log v01

**Episode:** Paper Short 038 · Paper Detour  
**Storyboard input:** [storyboard v01](../../../Storyboard/storyboard_v01.md)  
**Visual contract:** [visual bible v01](VISUAL_BIBLE_v01.md) and [Paper Detour image profile](../../../../../../../.agents/skills/ytv-scene-images/references/paper-detour.md)  
**Generation date:** 2026-11-03  
**Tool:** built-in `image_gen` (default tool mode); no CLI/API fallback.  
**Tool controls:** `transparent_background: false` explicitly set for every selected image; `referenced_image_paths` are listed per scene. The prompt requested portrait 9:16 and 2160×3840, but the tool exposed no independent size/quality parameter.  
**Actual output:** all selected images are opaque 941×1672 PNGs; do not call them native Full HD or 4K. Prompt and controls are not proof of applied resolution.  
**Scene text:** no editorial accents were baked into images. Functional street labels in S10/S11 were checked verbatim. Incidental background `PATTAYA` lettering appeared in some scenes and is legible/correct.

The exact selected prompt for each scene is recorded below. S17 reuses S01 exactly.

## Selected prompts

### S01 — `S01_v01.png`

Reference: Paper004 style. Output: `exec-36e02930-a25c-4616-99f8-4a6dda128cd1.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 opening scene still. Generate one complete, static, opaque, full-bleed handmade paper/card diorama in portrait 9:16, requested native target 2160×3840 (4K UHD). Match Image 1 as a style reference only: tangible layered cut-paper, visible fibers and cut edges, folded forms, physical miniature-set depth, warm realistic practical light, soft cast shadows, textured matte card. Do not copy its character or room.

Scene: a vertical diptych divided by a clear folded-paper seam, two distinct locations within one complete diorama. LEFT: one adult male Pattaya local volunteer, three-quarter view, neutral dark-blue civilian clothes, calm and alert, medium shot with a generic stylized paper face. Fictional stand-in, not an authentic portrait of Hooman Peseshk. RIGHT: separate Laem Chabang harbor quay at cool dawn, a small group of U.S. Navy sailors in ordinary shore-leave clothing walking down a gangway toward land; carrier hull and port cranes behind them. No interaction or eye-line between the volunteer and sailors; the locations must not read as one street.

Medium-wide composition: volunteer in the left midground; sailors and gangway in right midground; layered paper city silhouettes left, port cranes and ship right. Warm amber Pattaya lights contrast with cool blue harbor light. Keep a textured but low-detail area in the upper left for a separate caption overlay and keep the bottom subtitle-safe area clear of faces and important objects. Extend both scene panels to all four image edges without margins.

No in-image text, logos, flags, overt national symbols, ethnic caricature, sexualized imagery, police action, arrests, barricades, sewage, photoreal people, flat vector art, glossy digital 3D, blank surrounding canvas, watermark or border. Every figure and object is layered paper/card with visible edges, natural contact shadows, consistent miniature perspective and static poses only.
```

### S02 — `S02_v01.png`

Reference: Paper004 style. Output: `exec-b4074c15-ec15-4856-9322-9bbff4152abe.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S02 full-frame still. One complete, static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested native target 2160×3840 (4K UHD). Use Image 1 only for the tactile Paper Detour material style: visible fibers, cut edges, folded shapes, miniature set depth, realistic physical shadows and layered light. Do not copy its room or person.

Scene: high oblique aerial view of a U.S. carrier strike group moving across a dark blue paper sea, with one central aircraft carrier and a few escort-ship silhouettes. Small static aircraft on the carrier deck. Far above the sea, a restrained paper-map silhouette of Iran as a separate distant layer, not on a screen or official document. This visual summarizes the carrier's campaign context; do not depict a specific attack or event.

Composition: portrait frame, carrier angled diagonally through the middle, escorts small and spaced, map shape softly visible in upper background; use layered card contours for sea and clouds. Steel-blue diffuse light with a restrained warm glint on the ship; clear textures and strong foreground/background depth. Keep the subtitle-safe lower region free of crucial details and no editorial text.

No explosions, weapons firing, casualties, smoke columns, flags, readable text, logos, watermark, border, empty bars, photo-real ship render, flat vector shapes or glossy CGI. Every ship, sea, cloud and aircraft is visibly cut and layered paper/card with tangible folds and physical shadows; all poses static.
```

### S03 — `S03_v01.png`

Reference: Paper004 style. Output: `exec-b2d68823-b151-4c56-9329-2243c3acfd7f.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S03 still. One complete, opaque, static, full-bleed handmade paper/card diorama, portrait 9:16, requested native target 2160×3840. Use Image 1 for Paper Detour material style only: textured fibers, layered cut edges, folded miniature forms, physical light and shadows; do not copy its character or room.

Scene: low wide water-level view of a large U.S. aircraft carrier nearing a real working harbor. The carrier bow dominates the right two-thirds of the frame, with port cranes and shoreline infrastructure already visible behind it. Dark paper waves in the foreground, the harbor horizon behind the ship, cool early morning light. This depicts arrival after a long deployment without a full port call; do not imply nine months of continuous open-sea sailing.

Full-frame portrait composition with dramatic scale; matte gray-blue card for ship and water, restrained pale dawn sky, layered sea. Keep the bottom subtitle-safe zone simple, but allow richly textured sea. No people foregrounded, no visual month counter, no lettering or hull numbers, no battle, no flags, no explosion, no photorealism, no flat vector, no glossy CGI, no borders, no blank margin, no watermark. Static physical paper set only.
```

### S04 — `S04_v01.png`

References: Paper004 style; S03 port continuity. Output: `exec-8dc881f3-709b-465d-a31f-ab0e5e7537c6.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S04 still. One complete static opaque full-bleed paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is style reference only (handmade fibers, folded cut edges, physical depth, real cast shadows and practical light). Image 2 is a carrier/port visual continuity reference only; change the angle and composition.

Scene: very wide high-angle port establishing view at Laem Chabang. A large aircraft carrier is moored beside a working container terminal; several tall paper cranes, port transport, and just a few tiny people provide scale. Carrier centered at middle depth, cranes and terminal layered behind, quay edge as volumetric foreground. No crowd of 5,000 people. Pale sunny morning light through vellum, cool harbor blue and muted industrial card colors.

Portrait 9:16, clear harbor geometry and strong scale, composition distinct from the low bow view in Image 2. Leave the lower subtitle-safe region without tiny people or important detail. No readable signage, text, hull numbers, logos, flags, or claimed documentary markings. No empty bars, border, watermark, photorealism, vector art or glossy CGI. Keep every crane, ship and person as static layered paper with visible cut edges and physical shadows.
```

### S05 — `S05_v01.png` (selected variant v02)

References: Paper004 style; S04 carrier/port. Output: `exec-e97fe2e1-1a66-4349-bd6a-585d33fe82bb.png`.

```text
Use case: illustration-story. Asset type: replacement Paper Detour Short 038 scene S05 still. One complete opaque static full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is style reference only. Image 2 is carrier and port continuity only. Do not copy people or composition from any reference.

Scene: medium-wide side view at an aircraft-carrier gangway. Show exactly four U.S. sailors/Marines in ordinary shore-leave clothes walking together toward land; show a separate pair of similarly dressed service members farther back waiting to go. All six are visiting service members. No local volunteer or other distinct civilian character in the scene. Gangway creates a strong diagonal from ship to quay. Foreground quay edge, midground two small groups, background gray carrier hull and a few port structures. Daylight, tactile matte cardstock.

People must read as service members on shore leave in civilian clothing: casual shirts, shorts or trousers, practical shoes, small travel bags; no camouflage, no insignia, no weapons. Keep them visually distinct from a local patrol volunteer; do not include a man resembling the local in the previous opening image. Avoid a crowd or visual suggestion that 5,000 people came ashore at once.

Portrait composition, clean silhouettes and natural proportions; lower subtitle-safe zone free of important people/objects. No text, logos, flags, border, blank bars, watermark, police, arrests, photorealism, flat vector, or glossy CGI. Every person, gangway and ship detail is layered paper/card with visible cut edges, realistic contact shadows and one consistent miniature perspective. Static poses only.
```

### S06 — `S06_v01.png`

Reference: Paper004 style. Output: `exec-b9464f7d-2bf9-41bc-af4a-2db5e148a89b.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S06 still, an illustrative metaphor for crew accounts rather than documentary reconstruction. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is the accepted Paper Detour tactile-material style reference only.

Scene: a single shipboard mess and service corner shown in medium view as one cohesive miniature cross-section. Foreground: one modest meal tray with a small plain portion, a metal spoon, no branded packaging. Midground: plain tables and a closed technical service hatch with a visible pipe below; no leak, no water. Background: orderly supply shelving with only a few visible packages, suggesting dwindling supplies without implying total starvation. No people. Muted graphite/gray card, worn paper texture, restrained yellow practical light.

Keep the image human-scale, understated and dignified; no mess, no sewage, no flooded corridor, no panic, no extreme deprivation. Leave the subtitle-safe bottom area without important details. No readable text, labels, logos, watermark, border, empty bars, photorealism, flat vector, or glossy CGI. Layered paper fibers, cut edges, realistic physical shadow and consistent miniature perspective throughout.
```

### S07 — `S07_v01.png`

Reference: Paper004 style. Output: `exec-0f7ec6bc-fb79-424f-98a1-a003beaeea51.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S07 still. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 supplies the accepted Paper Detour tactile paper style only.

Scene: a restrained night-time police worktable in a Pattaya office, an illustrative setting for the reported August 29 detentions. Foreground: a closed neutral case folder, open blank notebook with a few neutral lines, a pen, and a clipboard with several simple unidentifiable marks. Midground: a generic Thai police officer silhouette seated behind the desk, face not identifiable and no badge detail. Background: window onto an ordinary Pattaya street after dark. Warm desk lamp inside against a soft blue exterior glow. No one is being arrested or accused in the image; the suspects are not shown.

Compose as a medium close view with clear desk objects; retain a quiet lower strip for subtitles. Do not include any legible names, numbers, accusations, or invented official documents. No handcuffs, jail bars, detainees, sexualized context, women posed as suspects, violence, evidence photos, text, logos, border, watermark, photorealism, flat vector art or glossy CGI. All elements built from layered paper/card with visible fibers/cut edges and natural shadows; one static miniature diorama.
```

### S08 — `S08_v01.png`

Reference: Paper004 style. Output: `exec-796bccb7-3cef-4d0e-803a-bedc5f465c59.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S08 still, visual context for a public mayoral statement. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is an accepted Paper Detour material/style reference only.

Scene: calm, symmetrical frontal view of a Pattaya municipal building entrance in daylight. Cream-colored layered facade and broad steps, glass entry reflecting a quiet street and pale sky. No identifiable mayor, no press event, no documents, no raid, no detainees, no sailors. This is a symbolic civic setting for a statement; it must not look like a direct response to a particular police operation. Clean architectural geometry with soft neutral daylight and subtle paper grain.

Portrait composition, facade centered in the upper and middle area, steps in foreground, keep lower subtitle-safe band simple. No Thai flag, no official seal, no legible sign, no papers or blank notices, no text, no logos, no border, no watermark, no empty bars, no photorealism, flat-vector appearance, or glossy CGI. Physical paper folds, cut edges, vellum glass and natural shadows; one static miniature set.
```

### S09 — `S09_v01.png`

Reference: Paper004 style. Output: `exec-2fcc9102-9828-45cc-86e8-bc1533025a90.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S09 still. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Use Image 1 only as the accepted Paper Detour tactile-material reference: visible fibers, layered cut edges, folded forms, physical light and shadow.

Scene: a calm, busy Pattaya evening street with ordinary pedestrians and two uniformed tourist-police officers walking separate patrol routes in the same broad street space. They are spaced apart, not stopping, chasing, checking or surrounding anyone. Show normal traffic and lit storefronts in the background; no nightlife sex-work cues. No Hooman Peseshk or recurring volunteer figure. Warm practical shop light; restrained realistic urban atmosphere.

Portrait wide shot with depth: foreground pavement and a few walkers, midground two officers far apart, layered buildings/signboards in background but all signage unreadable and generic. Keep the subtitle-safe lower band free of faces and essential details. No arrests, barricades, crowds, weapons, sirens, accusations, text, logos, national flags, watermark, border, empty bars, photoreal people, flat-vector look or glossy CGI. Static handmade paper miniatures with natural shadows and visible cut edges.
```

### S10 — `S10_v02.png` (selected variant v02)

Reference: Paper004 style. Output: `exec-cc014d02-8d4d-4277-9a56-490f5668a381.png`.

```text
Use case: illustration-story. Asset type: replacement Paper Detour Short 038 scene S10 still. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is Paper Detour tactile material style only.

Scene: close three-quarter view of a neutral folded paper street map card resting on a wooden service-room table. The card shows a simplified local street grid with exactly two highlighted street labels, spelled verbatim: “SOI 6” and “SOI 7”. One small crescent-moon symbol beside the highlighted routes indicates after-dark context. This is a generic explanatory map, not a real or reproduced military document.

The map is the clear subject in the central upper half; keep the lower subtitle-safe band simple and unoccupied. Visible paper fibers, rough cut edges, folded card, pin or soft natural contact shadow, warm neutral practical light.

No headline, header, official document, “U.S. Navy” wording, logo, seal, flag, invented legal language, other legible text, police tape, barricades, blocked public streets, gates or people being turned away. Only “SOI 6” and “SOI 7” may be legible. No watermark, border, empty bars, photorealism, flat vector art or glossy CGI. One static physical paper diorama.
```

### S11 — `S11_v01.png`

References: Paper004 style; S10 card/map style. Output: `exec-a222105a-fd8c-4138-b631-13efe870f9f6.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S11 still. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is Paper Detour material style only. Image 2 is continuity reference for the restricted-area paper/map style only; change to a separate top-down three-quarter composition.

Scene: a small cream paper restricted-area list resting on a service-room tabletop, viewed diagonally from above. The only legible text is the exact street label “SOI 6/1”, clearly highlighted once. No other street names, no moon symbol, no clock, no mention of after dark or hours. The card should look like a simple fictional visual aid, not a reproduced official document. Warm neutral light, visible cut paper edge and soft contact shadow. Keep the lower subtitle-safe zone free of the paper card.

No logos, seals, flags, extra writing, dates, names, stamps, invented legal language, police barricades, closed street, text distortion, watermark, border, empty bars, photorealism, flat vector, or glossy CGI. Static paper still only, one coherent miniature perspective.
```

### S12 — `S12_v01.png`

Reference: Paper004 style. Output: `exec-626221be-c2e1-4d90-8bd7-ebedeb2a9cd3.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S12 still. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is the accepted Paper Detour style reference only.

Scene: a lively but calm Pattaya Walking Street at night, shown as an open accessible public street. Open illuminated storefronts and ordinary adult pedestrians on the sidewalk; a small number of U.S. sailors in civilian shore-leave clothes stroll freely among other visitors, with no police stopping or watching them. Do not depict sex workers, solicitation, or an encounter with Peseshk. One small simple clock on a shop wall has hands pointing to 2 o’clock; its meaning is expected departure from nightlife venues by 2 a.m., not closing or blocking the street. Keep every gate and street entrance open.

Wide diagonal street view within a portrait frame, warm amber and restrained pink light, layered paper facades, pedestrians in midground, open road extending into depth. Keep the lower subtitle-safe area clear of faces/important objects. No signs with legible text, no 2 a.m. typography, no police barricades, barriers, closed gates, empty street, turned-away sailors, explicit sexual content, nudity, caricature, text, logos, flags, watermark, border, blank bars, photorealism, vector art or glossy CGI. Static layered paper miniature, visible fibers/cut edges and physical shadows.
```

### S13 — `S13_v01.png`

References: Paper004 style; S01 fictional-identity anchor. Output: `exec-ca450576-5d4f-4d69-9008-e403524e6be3.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S13 still, the first clear view of the volunteer patrol. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is the accepted Paper Detour material style reference only. Image 2 is an identity design anchor for the fictional recurring visual stand-in only; keep his generic paper-face, short tousled dark hair, dark-blue civilian overshirt and shoulder strap consistent, but do not copy the harbor diptych or imply a real likeness.

Scene: human-height wide view of an ordinary Pattaya night street. Three local volunteer patrol members walk calmly along the public sidewalk; the recurring dark-blue-shirt figure is among them, looking ahead, hands relaxed. A separate small group of uniformed tourist police is visible much farther down the street, clearly not paired with or directing the recurring figure. Ordinary adult pedestrians and layered storefronts in the background. Warm street lamps, no confrontation or stop.

Composition: several depth layers, volunteer group in midground, passersby foreground silhouettes, Pattaya facades and lighted windows behind. Keep the bottom subtitle-safe area free of faces/action. No sailors, detainees, sex workers, solicitation, checking papers, arrest, pointing, surveillance pose, police partner beside the named figure, visible badges/text/logos/flags, barricades, watermark, border or empty bars. No photoreal people, flat vector look or glossy CGI. Paper fibers, cut edges and natural physical shadows, all figures static.
```

### S14 — `S14_v01.png` (selected variant v02)

References: Paper004 style; S01 fictional-identity anchor. Output: `exec-eb29c282-e516-44ef-9bb6-4fb77b663da4.png`.

```text
Use case: illustration-story. Asset type: replacement Paper Detour Short 038 scene S14, composed for narration subtitles. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is accepted Paper Detour material style only. Image 2 is the identity anchor for the same fictional recurring paper stand-in only; preserve generic face, short tousled dark hair and dark-blue civilian overshirt/shoulder strap. Do not copy the harbor background or imply an authentic portrait.

Scene: chest-up three-quarter portrait of this adult man standing alone beside a softly lit shop window on a quiet Pattaya residential street at night. He looks toward the street, calm and thoughtful. Layered apartment facades and warm windows recede in the background; amber shop light on the figure contrasts with cool blue night. No passport, map, flag, badge or police credentials.

Composition is deliberately high in the portrait: head and shoulders in the upper half, with the figure ending above the middle of the frame. Leave the entire lower 35 percent as softly textured, unoccupied sidewalk/background for subtitles; no body, bag, face, hand or important object enters that lower strip. Preserve a distinct medium close-up rather than a full-height figure. No sailors, police, war symbols, political leaders, text, logos, watermark, border, empty bars, photorealism, vector style or glossy CGI. All materials are tangible layered paper/card, visible cut edges, natural shadows; one static scene.
```

### S15 — `S15_v01.png`

References: Paper004 style; S01 and S14 identity anchors. Output: `exec-8a735d9c-acf0-4787-afe4-de52cffb8e98.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S15 still for the opening sentence of Peseshk's direct quote. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is the Paper Detour tactile material reference. Image 2 is the identity anchor for the recurring fictional paper stand-in only; keep the same generic face, short tousled dark hair and dark-blue civilian overshirt, but do not copy the shopfront composition or claim a real likeness.

Scene: close side portrait of the same adult man in a quiet Pattaya night street. He occupies the left half in a chest-up profile, composed and thoughtful, speaking calmly. The right half recedes into layered blue-violet paper city facades and distant warm windows. Soft amber light falls on his face, restrained cool light behind him. No war imagery, soldiers, politicians, fighting or flags.

Place the head and face in the upper half, keep the lower 35 percent clear of the figure and important details for subtitles, and leave a quiet area at upper right for possible typography (but do not add any text). Clear paper facial construction, natural proportions, visible layered edges, physical shadows. No microphone, badge, text, logo, watermark, border, empty bars, photorealism, flat vector or glossy CGI. Static portrait still.
```

### S16 — `S16_v01.png`

References: Paper004 style; S01 and S15 identity anchors. Output: `exec-f624b105-a174-4133-91cd-923f4d88ac85.png`.

```text
Use case: illustration-story. Asset type: Paper Detour Short 038 scene S16 still for the final sentence of the quote. One complete static opaque full-bleed handmade paper/card diorama, portrait 9:16, requested target 2160×3840. Image 1 is accepted Paper Detour material style only. Image 2 and Image 3 are identity anchors for the same fictional recurring paper stand-in only; preserve generic face, short dark hair, dark-blue civilian overshirt and shoulder strap, but change scale and composition. He is not an authentic portrait of Hooman Peseshk.

Scene: a wide, human-centered night view of ordinary adults sharing an open Pattaya street. The recurring man is one distinct calm figure in the midground, not addressing anyone. Other pedestrians move naturally through the same public space, with warm windows and open street depth behind them. No staged interaction, handshake, group embrace or encounter with American sailors. The image communicates a shared city, not a specific meeting.

Portrait wide composition with the figure in the upper-middle area, several small ordinary pedestrians distributed around the scene, layered warm windows and deep street perspective. Leave a quiet upper-center field for a separate static caption overlay and keep the whole bottom 35 percent simple and free of faces/important objects for subtitles. Warm gold light contrasts gently with the cool beginning of the story. No in-image text, no war imagery, sailors, police, sex-work cues, national symbols, logos, watermark, border, empty bars, photorealism, vector art or glossy CGI. Handmade paper figures and facades with visible fibers/cut edges, natural physical shadows and static poses.
```

## Rejected variants

- S05 first render (`exec-7fae1b9a-914b-44b9-8cb1-fd7a62c98ed6.png`): not copied into the project. Its use of S01 as a reference put the volunteer stand-in among the sailors and implied he came ashore with them. The selected S05 call removed S01 as a reference and depicts only service members.
- S14 first render: not copied into the project. The figure entered the planned subtitle-safe band. Selected S14 v02 was composed higher in frame.
- S10 v01 (`S10_v01.png`; output `exec-4bb70ad5-a301-45d1-bb94-f200acf18d1d.png`): retained in the workspace for provenance but rejected as selected art because the generator added a “U.S. Navy Shore-Leave Notice” headline, making a generic policy appear to be a specific official document. S10 v02 removes the header and keeps only the street labels and night symbol.

## Sources and delivery

- Selected output files were copied from `/Users/diplomat/.codex/generated_images/01a19e92-58c1-7d10-9da8-7626efa8e45c/` into `Source/Images/paper_v01/`; originals were left in place.
- Exact reference paths/hashes, selected file hashes, measured dimensions, fit, acceptance and limitations are in [handoff v01](HANDOFF_v01.md).

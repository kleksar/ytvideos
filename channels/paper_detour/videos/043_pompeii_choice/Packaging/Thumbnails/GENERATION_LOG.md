# 043 — журнал генерации обложек

Каждая запись: дата, концепция, назначение, точный запрос, инструмент и модель
(если известна), входные референсы и их роль, исходник, производные файлы,
статус, проверки, ограничения и необходимые SHA-256. Фиксировать подтверждение
пользователя и результаты теста только после фактического получения.

## 2026-11-03 — paired Short package A/B concepts v01

Status: two local proposal variants; no user package approval, upload, metadata change, or experiment. Native YouTube A/B cannot run on Shorts ([official Help](https://support.google.com/youtube/answer/16391400?hl=en)). The actual artwork is one finished handmade paper/card diorama per concept; full masters are 9:16. Central 2:3 crop checked visually at 360×540 and 180×270; these are local previews only, not live YouTube/device evidence. Current YouTube Shorts custom thumbnail recommendations checked on 2026-11-03: 2160×3840, at least 640 px high, PNG/JPG, desktop limit 50 MB ([official Help](https://support.google.com/youtube/answer/72431?hl=en)). Upload copies were resized from the generated masters with Lanczos; generated source dimensions are retained separately below.

### Style references reviewed

- `channels/paper_detour/brand/paper_world_reference/paper_diorama_approved.png` — complete paper/card world, material depth, contact shadows.
- `channels/paper_detour/videos/037_cost_of_living/Packaging/Thumbnails/Exploration_50_v05/Masters/PD037_v05_07.png` — accepted Paper thumbnail material richness, cut-paper lettering and clear small-screen hierarchy.
- `channels/paper_detour/brand/TYPOGRAPHY_STANDARD.md` points to `A_MESSAGE.png`, `MATCH.png`, `D.png`, `A.png`, and `T.png` in film 001; those paths did not resolve in the current workspace, so those individual glyph samples were not inspected. Shape/texture was checked against the available accepted thumbnail PNG.

### A — decision at the doorway

- Title: `Pompeii: Run Through Falling Stones or Stay Inside?`
- In-image wording: `NO EASY CHOICE`
- Built-in image_gen; historical-scene; 9:16; no reference input to initial generation. Initial composition: a single Pompeian resident pauses at a doorway between falling pumice outside and a dark interior, integrated three-dimensional paper/card scene, large rounded cream cut-paper lettering in the upper central region; no safe-choice implication, gore, extra text, watermark, or modern objects.
- Initial master v01 failed the local crop check because lettering entered the top crop boundary; replaced with a targeted lettering-position edit.
- Final edit prompt: “Edit the provided portrait 9:16 Paper Detour thumbnail. Preserve the whole scene, resident, face, doorway, pumice street, architecture, materials, lighting, and framing exactly. Change only the integrated lettering placement: keep the exact phrase ‘NO EASY CHOICE’ and move the complete two-line title downward by about 90 pixels (about 5% of image height) so every letter, edge, and shadow clears the central 2:3 safe crop with visible margin. Keep it in the upper central area, fully above the resident's hair and face, without covering the doorway action. Preserve the rounded broad cream hand-cut card letters, paper fibers, thickness, and soft shadows. Do not add, remove, or alter any other content or text.”
- Final master: `Masters/PD043_A_no_easy_choice_v02.png`, 941×1672, SHA-256 `6fcb18719fae41a95e8a6fbce4056c95ea0073dce7ee04b52114871005679e15`.
- Upload copy: `Uploads/PD043_A_no_easy_choice_upload_v01.png`, 2160×3840, 9,468,245 bytes, SHA-256 `d327b92e8a8fb88edf4efba8b919c1b5f6d8578f0353c711fcf8cca6d346a5b9`.
- Preview evidence: `QA/A_v02/`; exact phrase fully visible in full and 2:3 reductions. Live card not checked.

### B — load on the roof

- Title: `Pompeii: When Shelter Became a Trap`
- In-image wording: `THE WEIGHT ABOVE`
- Built-in image_gen; historical-scene; 9:16; no reference input to initial generation. Initial composition: two residents inside a Pompeian home look up at a timber beam bowed beneath accumulated pumice; roof remains standing; full handmade paper/card diorama and exact broad rounded cut-paper phrase.
- Initial master v01 failed the local crop check because bottom lettering crossed the crop edge. A first lettering-only edit moved it upward but still touched the crop boundary. A second targeted edit reduced and positioned the phrase in the upper sky. Current v02 passes the checked central crop; earlier candidate files remain unselected.
- Final edit prompt: “On this portrait 9:16 image, preserve every scene detail exactly. Adjust only the existing exact lettering ‘THE WEIGHT ABOVE’: reduce the full three-line text block to about 72% of its current size and place it slightly lower so its top edge is at least 145 pixels from the top and its bottom edge stays above the roof tiles, entirely inside the central 2:3 crop with a visible margin. Keep it in the upper central sky, not on the faces, smoke plume, roof beam or pumice. Retain exact spelling and the same broad rounded cream cut-paper letters, texture and natural shadow. Do not change anything else or introduce any additional text.”
- Final master: `Masters/PD043_B_weight_above_v02.png`, 942×1670, SHA-256 `6edeeb53d9517ac7b5a639560297d99bce689ddfc054de1657bee12745761d44`.
- Upload copy: `Uploads/PD043_B_weight_above_upload_v01.png`, 2160×3840, 8,305,424 bytes, SHA-256 `95934fcc7375912c71320cc8fde835197c398fa277592bcf1158dab6539a3503`.
- Preview evidence: `QA/B_v02/`; phrase is legible at 180×270; pumice load, beam and faces remain clear in the central crop. Live card not checked.

No performance evidence exists. The pair tests an editorial hypothesis only.

### Prompt archive (verbatim)

**A initial generation prompt:**

> Use case: historical-scene. Asset type: finished YouTube Shorts thumbnail, portrait 9:16. Scene: Pompeii during the AD 79 eruption. One complete handmade paper-and-card diorama with visible layered cut-paper edges, tactile fibers, carefully formed ancient Roman clothing and architecture, believable support and soft contact shadows, rich detailed material texture, dramatic but grounded light. Show one Pompeian resident paused in a doorway, one hand gripping the wooden doorpost, face tense and turned toward the street where pumice is falling and accumulating on the road; the darker interior behind them is the other side of the dilemma. One clear frozen moment of hesitation, not a split-panel graphic. Three-dimensional paper miniature, refined craftsmanship, readable silhouette at phone size. Text (verbatim): “NO EASY CHOICE”. Render exactly these three English words, uppercase, no other writing, no extra letters, no misspelling. Integrate the lettering into the artwork as large, broad, rounded hand-cut paper/card letters with slightly irregular handmade contours, visible paper thickness, subtle fiber texture, and soft natural shadows, matching the tactile Paper Detour typography reference. Place the complete phrase in the upper central safe area, clear of the face and door action. Keep the entire face, doorway, main action and lettering within the central 2:3 region of the 9:16 canvas, with generous margins. Avoid gore, bodies, flames, a predictable warning, any implication that the doorway or interior is safe, modern objects, extra characters, logos, watermarks, borders, captions, labels, symbols, or any other text.

**B initial generation prompt:**

> Use case: historical-scene. Asset type: finished YouTube Shorts thumbnail, portrait 9:16. Scene: Pompeii during the AD 79 eruption. One complete handmade paper-and-card diorama with tactile fibers, visible clean layered cut edges, a miniature Roman interior with credible timber construction, believable physical support and soft contact shadows, finely crafted paper figures and dramatic but grounded light. Inside a modest Pompeian house, two residents look up as a heavy wooden roof beam bends under a visible layer of accumulated pumice stones above the roof. Capture the instant of strain while the roof is still standing; do not show collapse. The bowed beam is the main diagonal, faces below it. A small roof cutaway reveals the pumice resting on top, clearly explaining the pressure. This is a unified three-dimensional paper miniature, distinct from a doorway scene, readable at phone size. Text (verbatim): “THE WEIGHT ABOVE”. Render exactly these three English words, uppercase, no other writing, no extra letters, no misspelling. Integrate the lettering into the artwork as large, broad, rounded hand-cut paper/card letters with slightly irregular handmade contours, visible paper thickness, subtle fiber texture, and soft natural shadows, matching the tactile Paper Detour typography reference. Place the exact phrase across the lower central safe area, clear of the faces and the roof beam. Keep the entire text, faces and bowed beam within the central 2:3 region of the 9:16 canvas, with comfortable margin. Avoid gore, bodies, blood, fire, graphic collapse, modern objects, implausible architecture, floating props, extra characters, logos, watermarks, borders, captions, labels, symbols, or any other text.

**B first edit attempt (still failed crop):**

> Edit the provided portrait 9:16 Paper Detour thumbnail. Preserve the scene exactly: Pompeian house, roof tiles, pumice resting above, bowed timber beam, two residents looking up, faces, clothing, lighting, textures and framing. Change only the integrated title lettering: keep the exact phrase “THE WEIGHT ABOVE” with no other text, but move the complete three-line phrase from the bottom to the upper central sky area, just above the roofline, within the central 2:3 safe crop with visible margin. Make the lettering slightly smaller if needed so all letters and shadows fit comfortably in that area; keep the same broad rounded cream hand-cut card letters, paper fibers, thickness and natural soft shadows. Do not cover the roof beam, pumice, volcano silhouette, or either face. Do not add, remove or alter any other content.

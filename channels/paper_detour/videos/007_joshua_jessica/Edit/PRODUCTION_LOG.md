# Paper Detour 007 — production log

## 1 November 2026 — final render candidate v06

The user asked to finish and render the short. This authorizes a local render; YouTube upload or scheduling was not requested and was not performed.

### P12 visual correction

A timeline review found that the spoken line “Only fifty-five percent remained” needed a visual anchor. The earlier board had held the 55% paper accent, so the active Palmier timeline received the approved Source/Graphics/Final_v01/55_PERCENT_v01.png on its own overlay track. It rises from behind the laptop, over the dark wall: not on the laptop screen and clear of the lamp. The clip spans P12 at f1028–1163; the first visible pixels appear at f1030, the number is fully readable by f1036, and the P13 cut begins at f1164. The prior independent timeline review marked the occlusion and small-preview readability PASS.

### Sound and render

A single 0.7-second CC0 page gesture was placed with the 55% reveal. It is not looped; no music or device sounds were added. The final stereo mix was rebuilt from the approved Lawrence v3 narration and the source page gesture at /channels/paper_detour/videos/001_radio_game/Source/Audio/paper_motion_cc0_20261030/book-page-02.wav; the mix recipe and receipt are in Edit/Sound/.

Palmier project 652FD175, timeline 221D8873; snapshot E7B112CE, export job E66CD6DD-DB5F-4CBC-8D65-03AFEC845C6C. The Palmier render supplied the approved H.264 video stream. The final MP4 was muxed with a separately rendered stereo mix because Palmier’s audio bitrate was below the project delivery standard.

### Current candidate and measurements

- File: Deliverables/007_joshua_jessica_en_short_1080x1920_30fps_paper_foley_aac256_v06_20261101.mp4
- SHA-256: d05ed452d7b6950592c4847e4a5b87acd288fdadf00e4e33f31d536a18c2474ad8
- 1080×1920, H.264 High, 30 fps, 1344 frames / 44.800 s.
- Audio: AAC-LC, stereo, 44.1 kHz, measured 256,022 bit/s.
- Measured audio: −22.0 LUFS integrated, LRA 2.4 LU, −4.1 dBFS true peak.
- Full FFmpeg decode passed. The raw render and final MP4 H.264 elementary stream SHA-256 values match: 4410c9900e233d9253801aa1076f20c1f1161a6c167389d15fca2829e0363a75.
- Frame grabs for P12 (35.0 s), the P13 cut (38.7 s), and first/last frames are saved in Edit/QA/v06/.

### Review limits

The prior independent timeline reviewer confirmed P12 visibility and its P13 disappearance timing. Independent read-only final review of v06: PASS in the checked scope. The reviewer confirmed the 55% reveal/occlusion and disappearance by f1163, the P13 cut at f1164, matching sampled loop composition (blurred grayscale RMSE 0.00492), no obvious artifact in inspected frames, and audio-to-source correlation at 0 ms in sampled windows. The reviewer noted tight but visible clearance between the percent sign and lamp. Audio stream duration is 44.790 s versus 44.800 s video/container (10 ms shorter). No full-length normal-speed watch or human audio listening was available in this session, so spoken delivery, pronunciation, perceived sound onset, mix balance, and the loop’s subjective audio feel remain unverified. The first/last frame grabs show a matching composition; they do not substitute for playback across the loop seam. The reviewer’s sampled checks do not certify continuous motion across the seam. See Edit/QA/FINAL_REVIEW_V06.md. After the approved v06 passed checks, the previous v01–v05 MP4 candidates were removed from Deliverables; source, Edit materials, receipts, and the Palmier project remain.


## 1 ноября 2026 — user rejection and screen rewrite

The user rejected v06 as a final delivery because the laptop display remains empty throughout the short and asked for a writer-led rethink of every shot. v06 remains only as a reference; it is not accepted as the current final export. The approved story premise and recorded narration remain the starting inputs unless the writer identifies a specific reason to propose a change. The current task is to create a complete screen-content/action arc across all 14 compositions, fact-check any visible words, verify overlay feasibility, and then revise the visual package and Palmier timeline. No new render has been made yet. YouTube remains unchanged.

### P09 geometry correction — 1 November 2026

After viewing the full P09 master and a close crop, the coordinator found that the master shows the outside of the laptop lid; the display faces Joshua and is hidden. The earlier `SCREEN_OVERLAY_FEASIBILITY_v01.md` count of ten visible screens was wrong; the addendum now records nine display-visible compositions and supersedes its P09 row. At 10:51 Europe/Belgrade the coordinator submitted a focused correction request in the same Chrome ChatGPT project chat, after the visible selector again showed Extra High. ChatGPT recommended keeping P09 as an intentional no-screen pause, then clarified that it should remain fully static to honor the no-body-part-animation rule. A direct P08→P09 cut marks the time ellipsis; P10 starts with an unreadable outgoing strip before the longer incoming answer. `SCREEN_CONTENT_SCRIPT_v03.md` now records this decision. No P09 image, screen overlay, or Palmier change has been made.

### Process correction

The first attempt routed the creative shot rewrite to a writer subagent. The user clarified that the required writer-led creative pass must be made directly in ChatGPT.com through Google Chrome with the visible Extra High / «Очень высокий» mode checked; a subagent is not a substitute. Project guidance was updated accordingly. The direct Chrome answer is complete and v03 is recorded in `Storyboard/SCREEN_CONTENT_SCRIPT_v03.md`. The coordinator checked the literal text and timeline assumptions against the existing screen fact-bound memo, including moving the sleep/wake time ellipse before the promise in P09. The answer remains a dramatic proposal, not factual or visual verification. Screen assets and Palmier have not been changed yet.

At 10:39 Europe/Belgrade, the coordinator opened the project chat “Сценарная постановка 14 кадров” in Chrome (`6ae704c0-f1d0-83ed-873c-1f6e465d8dc9`). Immediately before sending the substantive request, the visible model selector showed **Extra High**. The request asked for a fresh, complete P01–P14 dramatic pass, retaining the approved VO and factual boundaries, challenging v02, and spelling out screen state/action, emotion, shot, loop, and production risk. ChatGPT’s answer took 3m03s and says the model could not itself verify the UI mode; the coordinator had directly recorded the visible selector before sending and again afterward. The resulting v03 keeps the approved VO and distinguishes all 14 screen states. v02 remains an unaccepted comparison draft. No timeline changes have been made.

### Repeated process correction — 1 November 2026

The user again flagged that invoking a subagent was the wrong first action: for this creative pass the coordinator must work directly in Chrome on ChatGPT.com with Extra High. The earlier v03 direct answer remains the recorded creative proposal; agent work is not treated as its substitute. The coordinator reopened the existing project chat and confirmed the visible selector reads **Extra High**. The shared workflow is now an explicit gate: direct Chrome request, completed read-through, and record first; no creative subagent for a task the user assigned to ChatGPT.com. Any later delegation must be a distinct permitted review or mechanical task. No new creative prompt was sent in this documentation correction, and no media, Palmier project, timeline, or export was changed by it.

### P12 duplicate resource strip — 1 November 2026

After the user’s process correction, the coordinator used the existing Chrome project chat directly; the visible selector read **Extra High** immediately before the substantive P12 request. The request described the inspected master and Palmier composite without claiming ChatGPT had seen either file. Its recommendation was to remove only the white/turquoise strip from the table, restore the surface in the source composition and compatible registered layers, and leave the display’s **55% REMAINING / THIS VERSION** and brown bar intact. This avoids two visually similar meters and does not change the story facts or VO.

The original P12 master was inspected at 941×1672. Two full-frame image-edit candidates were generated: one retains the 55% screen state and one keeps the display blank for the base layer set. Both remove the table strip visually, but pixel comparison found changes in 97.80% and 97.96% of their respective source frames, so neither is accepted as a localized correction or imported. A review composite of the existing BG→MG→FG package is at `Edit/QA/v07_p12_base_layer_stack_review_20261101.png`; the FG contains only the unwanted strip, while the BG already supplies tabletop underneath. ChatGPT.com Extra High then recommended stopping P12 import until a real boundary map confirms a valid foreground, explicitly cautioning against assuming the blurry leaf or an arbitrary table band is valid. Next: map the actual leaf, laptop/attached hand, and hidden background against the corrected intended master; proceed only if the silhouette and fill can be separated without an artificial boundary, and require a zero-offset composite plus movement-endpoint review. Do not hide the old strip with a flat overlay.

A draft bounds JSON and guide were prepared at `Source/Images/QUICK_IMPORT_V04_CANDIDATE/12_resource_meter/layer_bounds_P12_v04_draft.json` and `bounds_map_P12_v04_draft.png`. The close-up `Edit/QA/p12_fg_leaf_detail_20261101.png` shows that the defocused plant edge blends into the tabletop. An imagegen FG extraction trial (`FG_leaf_candidate_NOT_READY.png`) failed the draft bounds: at alpha > 8 its nonzero-alpha bounds reach x=444 although the marked FG bound ends at x=235; 29,778 alpha-positive pixels lie outside the marked region. Mark **FAIL / NOT READY**. Do not use this layer or generate BG/MG from the unconfirmed boundary. No replacement assets were imported and no Palmier clips were changed.

### Current v07 status after P12 review

The isolated draft is Palmier project `01CB00DB`, timeline `92BD1E43`, 1080×1920/30 fps, 1344 frames / 44.8 s. It carries the v03 screen states, the corrected no-screen/static P09 direction, existing approved audio, and continuous grain. The P12 source-layer defect is still present in its current media references; the image candidate has not been mounted. The v07 timeline therefore remains a work-in-progress and is not ready to export or deliver. No audio was generated and nothing was published to YouTube.

### Смена визуального метода: цельные неподвижные кадры — 1 ноября 2026

Пользователь отменил для Paper Detour 007 глубинную постановку BG/MG/FG и потребовал обычную смену отдельных картинок. Общие правила `AGENTS.md`, `PAPER_DETOUR_CREW_WORKFLOW.md`, `RAROVISTA_PRODUCTION_GUIDE.md`, `RAROVISTA_EDITING_STANDARD.md` и роли специалистов обновлены: один цельный still на монтажный кадр, прямые склейки; прежние послойные процедуры архивны. Изучены сессии «Визуальная постановка Paper Detour» и «Сравнение концепций ролика», а также утверждённый одноизображенческий план 004. Перенесён режиссёрский метод, не история/образы других выпусков.

В существующем Chrome-чате «Постановка Paper Detour 007» (conversation `6ae72b05-8c08-83eb-8928-e86c86faefc5`) перед содержательным запросом видимая модель была **Extra High**. Получена новая партитура на 14 статичных кадров, 13 уникальных изображений, P14 = точное повторное использование P01. Записана в `Storyboard/FULL_FRAME_STORYBOARD_v02_20261101.md`. Сценарий и утверждённая озвучка не меняются; тайминги предварительные.

Старый `PARTITURE_REBUILD_EXTRA_HIGH_v01_20261101.md`, полный послойный пакет и Palmier v07 отмечены как устаревшие для текущей переделки; старые материалы не удалялись и в новый монтаж не включать. Все новые still-файлы предназначены для `Source/Images/full_frame_rebuild_v02_20261101/`. На момент записи новые изображения ещё не созданы/не проверены, Palmier не изменён, новый звук не генерировался, экспорт не выполнялся.

## 1 November 2026 — full-frame v02 rebuild

The user changed the visual method: use one complete still image per editorial cut, with ordinary direct cuts; no independent BG/MG/FG planes, masks, scene parallax, camera motion, or object/body animation. The current channel and episode documentation now reflects this. Older layer assets, manifests and automation are retained only as archives and must not be imported into this rebuild.

The complete P01–P14 direction was prepared in the existing ChatGPT project chat through Chrome with the visible selector showing **Extra High** before each of two substantive prompts. Thirteen full-frame 941×1672 PNGs were generated, reviewed as still images, and logged in `Source/Images/full_frame_rebuild_v02_20261101/GENERATION_LOG.md`. P14 reuses the exact P01 source. Readable strings were checked: `Jessica?`; `I will be here waiting for you.`; `55% REMAINING`; and `THIS VERSION`. The first P04 generation showed an avatar and was rejected; its replacement has only unreadable paper message strips. This inspection does not certify full video playback or final render quality.

A separate timeline was duplicated from source project `01CB00DB`, source timeline `92BD1E43`; source timeline was not edited. New timeline: `007_joshua_jessica_full_frame_v02_20261101` (`820854CD`). Snapshot before rebuilding: `0B758DA2`. Current build snapshot before render: `37F5B4D2`. Legacy scene-picture tracks on the duplicate were removed; 14 full-still clips now occupy one `Main` track. Existing 44.8-second narration and the one previously approved paper SFX were retained without regeneration. The `Grain` overlay remains above the images. Timeline is 1080×1920 at 30 fps, 1344 frames / 44.8 seconds; still boundaries are the approximate intervals in the storyboard, converted to exact project frames. P14 references the same media asset as P01.

Palmier export job `80441CC2-E6DD-4DD1-BB3D-99A60A72DA3A` is rendering to `Deliverables/007_joshua_jessica_en_short_1080x1920_30fps_paper_full_frame_v02_20261101.mp4`. It is not accepted or published until the file completes and frame/audio checks are recorded.

### Voice alignment correction — 1 November 2026

The first v02 render used provisional timings from the generated storyboard. Before treating it as a candidate, the coordinator compared the same fourteen story positions against the original source timeline and found the approved voice-aligned cut boundaries: 0, 90, 183, 273, 366, 456, 546, 636, 726, 816, 906, 996, 1164, 1254, 1344. The P12 hold is 168 frames / 5.6 seconds; all other frames are 90 or 93 frames / 3.0–3.1 seconds. The storyboard and active timeline now use those existing boundaries. The first render and two intermediate audio exports were temporarily staged under QA, then removed after the corrected final passed technical checks; no intermediate MP4 remains. Corrected Palmier export job: `0E91F306-2AAC-491B-9697-D741AEC7C9BA`.

### Superseded full-frame v02 export and checks — 1 November 2026

This first voice-aligned export was superseded by the f1028 cut correction below. Its old hashes and timing are retained only as production history. Final file: `Deliverables/007_joshua_jessica_en_short_1080x1920_30fps_paper_full_frame_v02_20261101.mp4`.

- H.264 1080×1920, 30 fps, 1344 frames / 44.800 seconds; AAC-LC stereo 44.1 kHz, 256,022 bit/s / 44.790 seconds.
- SHA-256 MP4: `b21b9e2731331afd3590cd6e1f1ea4ced356da8c9f62190b3e21ea7e066b1355`.
- H.264 elementary stream SHA-256: `7dbf2e404ca521d8fb38224a5cb652bc8a85383b2ed928e36a9b56b80b310b4d`. It matches the Palmier video export before remux.
- AAC elementary stream SHA-256: `205f5a20b87583180f8318fc9eafaed830d2ffa5396aa664869a72940373c790`. It matches the already existing v06 AAC exactly; no audio was generated or re-encoded for this final file.
- Full FFmpeg decode passed. `ffprobe` confirmed the streams and duration. A 14-frame contact sheet was checked, and `blackdetect` reported no black segment. `Edit/QA/full_frame_v02/RENDER_CONTACT_SHEET_v02.jpg` shows one representative frame from every cut.
- Audio measurements on the copied AAC: −22.0 LUFS integrated, 2.4 LU LRA, −4.1 dBFS true peak. No human listening or continuous normal-speed watch was completed. Therefore spoken delivery, perceived SFX timing, the full-length visual rhythm, grain seams in motion, and subjective loop quality remain unverified.
- The rejected v06 MP4 and temporary render files were removed after v02 passed format/decode checks. Only the current v02 MP4 remains in `Deliverables`. No YouTube upload or publication occurred.

### P12 cut-to-spoken-anchor correction — 1 November 2026

Review of the first voice-aligned still sequence found that the baked `55% REMAINING` card appeared at f996 / 33.20 s, 0.88 s before “Only” and more than a second before “fifty-five.” In the existing sound plan the voice marker for `fifty-five` is f1028, and the previously approved one-shot paper effect crosses its measured −25 dBFS onset at f1028. Since the new method bakes the complete card into one still, the P12 cut was moved to f1028 to place that image at the spoken reveal; P11 now lasts 122 frames / 4.07 s and P12 lasts 136 frames / 4.53 s. Voice and SFX positions are unchanged. The new boundaries were verified on timeline `820854CD` and saved in snapshot `8CC05D5D`. Re-render job `E2A7183E-FF8C-44AB-A9FD-0528A54FC8BD` supersedes the previous v02 file, which was moved temporarily to QA so its already-existing AAC could be retained byte-for-byte.


### Final f1028 full-frame export — 1 November 2026

The P12 reveal was moved from f996 to f1028 after checking the spoken anchor and existing SFX onset. The corrected timeline was rendered as Palmier job `E2A7183E-FF8C-44AB-A9FD-0528A54FC8BD`, snapshot `8CC05D5D`. P11 now holds for 122 frames / 4.07 s; P12 holds for 136 frames / 4.53 s. The deliverable uses the newly rendered H.264 video and the already-existing approved AAC master, stream-copied without generating or re-encoding audio.

- Final file: `Deliverables/007_joshua_jessica_en_short_1080x1920_30fps_paper_full_frame_v02_20261101.mp4`
- 1080×1920, 30 fps, 1344 frames / 44.800 s; H.264 at about 10.51 Mbit/s. AAC-LC stereo, 44.1 kHz, 256,022 bit/s / 44.790 s.
- SHA-256 MP4: `e70a54effe45746aee7783a753148b867810a80d1c8f0901c9669ba499b5a9f7`.
- H.264 elementary-stream SHA-256: `b198cc55c5d26f43a13bc80e8d75736a04c359b07571d20ca0d6a355c85ea193`. AAC elementary-stream SHA-256: `205f5a20b87583180f8318fc9eafaed830d2ffa5396aa664869a72940373c790`, identical to the existing master.
- Full FFmpeg decode passed. `ffprobe` confirmed streams, format and duration; black-frame check returned no black segments. The rendered 14-cut contact sheet and exact frames immediately before and after f1028 were visually inspected; the cut changes from P11 to the `55% REMAINING` card on the selected frame boundary.
- No continuous normal-speed watch or human listening was completed. The render was not uploaded or published. The two intermediate MP4 files were deleted from QA after verification; Deliverables contains only this current MP4.

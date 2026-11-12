# Paper Short 038 — caption cue sheet v01

**Channel:** Paper Detour  
**Narration:** EN v05; exact wording is not yet user-approved.  
**Scenes:** storyboard v01; selected stills in Paper v01 handoff.  
**Canvas:** 1080×1920 portrait.  
**State:** Static PNG and scene-pair geometry checked by coordinator. Cue timing is estimated; recording, listening, subtitle overlap, motion path and final-video sync remain unverified.

## Shared geometry and selected assets

- One common nominal face height: 70 px per line at 1080×1920. Helper-measured face lines vary by 0–5 px due rasterization: C01 68 px; C16 65/67 px.
- Primary anchor: normalized center `(0.66, 0.16)` = `(713, 307)` px. Alternate anchor: `(0.285, 0.16)` = `(308, 307)` px. The alternate is the only one and is used only by S01.
- C01 selected alpha bounds on S01: `[100, 235, 516, 370]` px. The word sits over the dark upper-left sky, left of the central fold; the rendered alpha edge clears the visible fold by about 20 px and begins at the storyboard's x=100 safe boundary.
- C16 selected alpha bounds on S16: `[496, 230, 957, 386]` px. The two lines are centered in the clear upper-right sky, away from the figure and foliage; right edge remains inside x=980 safe limit.
- Lower subtitle-safe region remains clear in both composites. There is no subtitle file yet, so simultaneous subtitle overlap is not checked.
- Preview scenes are proportional LANCZOS derivatives of the selected 941×1672 source stills at exactly 1080×1920; this is a uniform 0.053% ratio adjustment for the rounded native dimensions. Source images remain unchanged.
- Coordinator visually inspected exact spelling, phrase line breaks, paper texture, color, edge, shadow, alpha, full-frame readability and 360×640 previews. No independent visual reviewer has checked these assets.

## Cue map

| ID / version | Text / lines | Scene / anchor | Narration and semantic function | Spoken trigger → end | Window and source | Status |
|---|---|---|---|---|---|---|
| C01 v01 | `IRAN-BORN` / 1 line | S01 / alternate `(0.285, 0.16)` | EN v05. Concisely supplies Peseshk's Iranian origin, which the image cannot establish, and makes the opening contrast legible. | After the spoken word `Iranian-born` → through the completion of `ashore`; never precede `Iranian-born`. | Estimated `S01 +1.0–4.0 s`; scene duration is a 5.5-second storyboard estimate. No recording, measured speed, word alignment or audition. | Static pair geometry and phone preview: coordinator visual PASS. Recording sync and future caption motion: UNVERIFIED. |
| C16 v01 | `WE ARE ALL` / `BROTHERS` / 2 lines | S16 / primary `(0.66, 0.16)` | EN v05 direct quote. Verbatim accent marks the central answer without adding interpretation or emotion. | Trigger on `brothers`, after the word begins; end with completion of `Pattaya`. | Estimated `S16 +1.5–4.0 s`; scene duration is a 4.0-second storyboard estimate. No recording, measured speed, word alignment or audition. | Static pair geometry and phone preview: coordinator visual PASS. Recording sync and future caption motion: UNVERIFIED. |

All times are relative to scene start and are not frame-accurate. The provisional full cue windows are 3.0 s (C01) and 2.5 s (C16), inside the channel's usual 1.2–3.0 s accent range; after any approved recording, revise exact frames to word alignment and confirm there is enough hold after entry/exit. Do not use these estimates as final timeline positions.

## Candidate comparison and pair preflight

- Current selected render: [managed output manifest](../../../Assets/Generated/captions-v01-current/manifest.json), generated from [input manifest](caption-input_v01.json). Static and 360×640 composites: [S01/C01 alternate](../../../Work/captions-v01-current/previews/S01/C01/alternate.png), [S01/C01 phone](../../../Work/captions-v01-current/previews/S01/C01/alternate__phone.png), [S16/C16 primary](../../../Work/captions-v01-current/previews/S16/C16/primary.png), and [S16/C16 phone](../../../Work/captions-v01-current/previews/S16/C16/primary__phone.png). Combined contact sheet: [CONTACT_SHEET.png](../../../Work/captions-v01-current/CONTACT_SHEET.png).
- S01/C01 selected alternate: helper technical PASS. Visual PASS: readable cream letters against dark sky, intact safe margins, no face/object obstruction, full phrase remains left of fold. S01/C01 primary comparison: helper technical PASS but visually rejected because the word crosses the strong diptych fold.
- S16/C16 selected primary: helper technical PASS. Visual PASS: clear upper sky, no figure or foliage obstruction, readable at phone size. S16/C16 alternate comparison: helper technical FAIL because its alpha bound begins at x=91, outside the x=100 safe boundary; not selected.
- Tool-level `visual`, `sync`, and `motion` states remain UNVERIFIED; manual visual checks do not verify audio sync or a future animation path. The images are static caption-preflight composites, not a video review or export QA.
- S17 intentionally has no cue. It reuses the clean S01 scene PNG; only the separate opening overlay is absent on the final loop frame.

## Asset provenance

- Original candidate PNGs: [IRAN-BORN_v01.png](IRAN-BORN_v01.png), SHA-256 `4705f8e03189c0ee44d1382084dd141dcdb07703181bf195e72a5edbfafae531`; [WE_ARE_ALL_BROTHERS_v01.png](WE_ARE_ALL_BROTHERS_v01.png), SHA-256 `94562033be64459b0e140f4eebcc31d44a3d27069041ba61c1090ac8c9f4e06d`.
- Both source PNGs were created with built-in `image_gen`, using accepted Paper typography PNGs `A_MESSAGE.png`, `MATCH.png`, `REPORTED.png`, and `FORMAT_MATTERS.png` as positive references. Both are 2172×724 with real alpha. The helper prepared the selected production cue rasters and face masks in `Assets/Generated/captions-v01-selected/`.
- Selected cue hashes: C01 `c5ed0a3c513c40bdffdaef2ab5df8ec758d837ec36476de88015fc0e239bc3dd`; C16 `2adb802bdd84a4bf0cd4d8fcab21d49ee7213ab4db0d199d08d81766b9e04dd8`.
- Other generated runs (`captions-v01-preflight-2`, `-3`, `-4`) remain as comparison provenance; the first geometry placed C01 across the S01 fold, the next two refined and verified the alternate location. An initial helper attempt failed because the cream face mask split the hyphen/line into multiple row bands; explicit measured face-line boxes fixed the input. No source scene or source caption was overwritten.

## Handoff boundary

Use the selected PNGs only with the stated scene and anchor. Do not place `IRAN-BORN` in S17. Do not move, scale independently, or animate portions of the scene image. Cue entrance/exit motion belongs to Palmier edit and requires exact timeline timing. After the narration is accepted and an authorized recording exists, listen at the actual edit speed, update the word-level timing and recheck the rendered cue path. Final cue/frame QA belongs to the video QA skill.

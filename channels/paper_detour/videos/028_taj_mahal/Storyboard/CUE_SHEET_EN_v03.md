# English text-cue sheet — v03

**Episode:** Paper Detour 028 — Taj Mahal  
**Timeline:** `028 Rough Cut EN v01`, 30 fps, frames `[0,1066)`  
**Alignment source:** `../Source/Voice/lawrence_v01/voice_en.alignment_clipped.json`  
**Cue assets:** `../Source/Images/Text_Cues_EN_v03/production/`  
**Preflight:** `Text_Cue_Preflight_EN_v03/manifest.json`, selected full-size/phone pairs and contact sheets.  
**Role:** selective English phrase accents synced to speech; these are not subtitles.

## Cue schedule

Clip intervals use timeline frames `[start,end)` with end exclusive. The cue begins on the aligned trigger; the end includes a short visual tail after the last spoken word. Every ordinary cue fades in over four frames, holds, and fades out over five frames. Text rises into its preflight anchor, pauses, then drifts slightly away. Cue PNG pixels and their preflight size/position are scaled from the 941×1672 helper canvas to the 1080×1920 Palmier canvas.

| ID | Accent words | Spoken trigger → end | Spoken time | Clip frames | Scene(s) | Anchor | Preflight layer top-left / asset size (px @941×1672) | Cue motion (normalized canvas Y) |
|---|---|---|---:|---:|---|---|---|---|
| C01 | OF COURSE. / I'M GOOD AT IT. | “Of course” → “at it” | 0.000–1.680s | [0,56) | S01 | primary | (234,127) / 467×178 | +0.070 → 0 → +0.030 |
| C02 | THE PRICE OF / ONE ANSWER | “That answer” → “his hands” | 2.400–4.640s | [72,145) | S01 → S02 | primary | (246,122) / 451×185 | +0.070 → 0 → +0.030 |
| C04 | 22 YEARS | “twenty-two” → “years” | 9.200–10.160s | [276,310) | S03 | alternate | (160,227) / 340×117 | +0.020 → 0 → −0.020 |
| C06 | ANYTHING / COMPARABLE | “anything” → “comparable” | 18.680–19.440s | [560,589) | S06 | primary | (292,118) / 357×183 | +0.070 → 0 → +0.030 |
| C08 | COULD NEVER / WORK AGAIN | “could never” → “work again” | 25.520–26.560s | [766,802) | S07 → S10 | primary | (264,122) / 416×186 | +0.070 → 0 → +0.030 |
| C10 | TOO GOOD AT / YOUR JOB? | “too good” → “your job” | 28.920–29.760s | [868,898) | S10 | primary | (285,123) / 373×187 | +0.070 → 0 → +0.030 |
| C11 | WILL YOU KEEP / WORKING AS AN / ARCHITECT? | “Will you keep working” → “an architect?” | 33.680–35.400s | [1010,1066) | S11 | alternate | (112,140) / 435×290 | +0.020 → 0; loop hold |

## Cue behavior

- C01, C02, C06, C08 and C10 use the primary zone; C04 and C11 use the alternate left zone. This preserves the Taj Mahal silhouette on S03 and keeps the final king question distinct from the preceding hook.
- C02 and C08 stay in one screen position across their scene cut. Their background diorama changes directly underneath the phrase accent.
- C11 fades in and holds through frame 1065, with no exit movement, so the king’s question remains legible at the loop point and clears on the S11→S01 cut.
- The PNGs use cream paper letters, warm orange edging and a physical shadow, based on the accepted `A_MESSAGE.png` channel reference. The seven production copies are byte-identical to their v03 preflight cue renders; hashes are in the local generation/provenance record.

## Motion and placement QA

The nine assigned still/cue pairs were checked at full 941×1672 and phone preview size before import. The geometry pass is recorded as technical PASS in the helper manifest; cap height is approximately 60 px on the 941×1672 composite. Motion-path readability and text sync are checked again on the edited Palmier timeline before handoff. No dialogue, music or sound-effect edit is included in this pass.

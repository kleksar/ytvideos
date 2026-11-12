# Independent asset QA — Paper Detour Short 008

**Date:** 1 November 2026  
**Status:** Partial PASS for DRAFT source assets.  
**Scope:** files under `Source/Images/` for scenes 01, 04, 05, 06 and 12; the cast lineup and character pose packs; accent art A01–A45; orange tab and story-fork branches.

## Method and limits

I visually inspected the named PNGs, compared the diorama material with `channels/paper_detour/brand/paper_world_reference/paper_diorama_approved.png`, and compared lettering with `001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png` and `MATCH.png`. I checked current file dimensions, color mode, alpha range and corner samples with Pillow/ImageMagick. Accent wording was checked manually against `Storyboard/scene_accent_score_en.md`; this was not OCR.

This is a static source-file review. I did not build or inspect a composite in Palmier. Layer registration, contact and pivot points, hidden background fill, actual text placement, movement, phone-size composition, continuous grain, and timing remain unverified.

## PASS

### Text and paper lettering

The visible wording matches the score throughout A01–A45; punctuation and meaningful spelling details are present. A18 intentionally reuses A02 (`BREAK UP`), and A42 reuses A04 (`THREE MONTHS`). A30 has the acute accent in `FIANCÉE`; A10, A16 and A37 use curly apostrophes; A06 has its question mark; A34 includes `40`.

Current preferred revisions inspected:

| Cue | Preferred file | Static check |
|---|---|---|
| A01 | `accent_words/A01_every_single_date_v02.png` | `EVERY SINGLE / DATE`; 2027×776 RGBA, alpha 0–255, all corners 0; alpha>8 margins L42/T100/R32/B45 px. No detached mark visible. |
| A15 | `accent_words/batch_A02_24/A15_double_date_v02.png` | `DOUBLE / DATE`; 1802×872 RGBA, alpha 0–255, all corners 0. Text and backing are isolated from the canvas background. A few 1–7 px alpha flecks remain near the lower edge; see FIX. |
| A20 | `accent_words/batch_A02_24/A20_talk_alone_v03.png` | `TALK / ALONE`; 1581×995 RGBA, alpha 0–255, all corners 0; margins L50/T111/R36/B53 px. No broad red backdrop is visible. |
| A24 | `accent_words/batch_A02_24/A24_feeling_guilty_v03.png` | `FEELING / GUILTY`; 2024×777 RGBA, alpha 0–255, all corners 0; margins L268/T59/R263/B27 px. No broad red backdrop is visible. |
| A40 | `accent_words/batch_A25_45/A40_different_stories_v02.png` | `DIFFERENT / STORIES`; 1873×840 RGBA, alpha 0–255, all corners 0; margins L48/T99/R40/B63 px. Clean replacement for the narrow v01. |
| A43 | `accent_words/batch_A25_45/A43_the_whole_time_v03.png` | `THE WHOLE / TIME`; 1866×843 RGBA, alpha 0–255, all corners 0; margins L19/T87/R19/B54 px. The top speck from v02 is absent on visual inspection and the right edge is no longer clipped. Fine orange-red fringe pixels remain below the lower line on magnified transparency; judge them over the actual scene. |

Across the other accent files, the cream cut-paper faces, orange-red backing and dimensional shadow match the 001 references in broad style. The lettering is heavy enough to remain bold when scaled; actual phone-size legibility still depends on the edit layout. Batch A25–A45 assets have transparent corners and mostly consistent 32–34 px saved margins. A two-line layout in A01/A40/A43 preserves the exact phrase.

### Character and scene source art

- `scene01/scene01_pre_reveal_v02.png` is a clean two-person full-frame master. N and B have light shoes, no shoulder bag, and clothing colors consistent with `scene01_hook_master_v02.png` and the current lineup. The room background is visually continuous with the hook master. The frame contains no Matt or later-story information.
- `character_continuity/character_lineup_v01.png` is a clear four-person reference sheet. Current `poses/CHAR_N_STAND34_v02.png`, `CHAR_B_STAND34_v02.png`, `CHAR_M_STAND34_v02.png`, and `CHAR_F_STAND34_v02.png` share the lineup’s color and paper-texture language. The phone in `CHAR_N_PHONE_READING_v01.png` has a blank screen; I saw no ring or hidden message in the reviewed poses.
- `scene04_movies_background_v01.png` has a blank screen and no film title or audience. The seated trio depicts N/B/M facing the screen. `scene05_walk_background_v02.png` is an anonymous walkway; `scene06_shop_background_v01.png` has a blank display with no brand, products or readable labels; `scene12_park_background_master_v01.png` is an empty park. The reviewed scene plates do not disclose Matt’s family facts or invent a cause for the breakup.
- `motifs/orange_place_tab_v01.png` and `two_story_fork_left_v01.png` / `two_story_fork_right_v01.png` have real alpha with transparent corners. The tab is blank; the fork strips carry no quotes or extra story facts. Their paper texture fits the established world.

## FIX

Priorities apply to the named asset or workflow step, not to the whole pack.

| Priority | File(s) | Finding and action |
|---|---|---|
| P1 — exclude stale version | `accent_words/batch_A02_24/A15_double_date_v01.png` | Red background defect. Do not use; select v02. |
| P1 — exclude stale versions | `accent_words/batch_A02_24/A20_talk_alone_v01.png`, `A20_talk_alone_v02.png`; `A24_feeling_guilty_v01.png`, `A24_feeling_guilty_v02.png` | Broad red-orange glow/backdrop remains visible around the words, even though corners sample transparent. Do not use; select v03 for A20/A24. |
| P1 — exclude stale versions | `accent_words/A01_every_single_date_v01.png`; `accent_words/batch_A25_45/A40_different_stories_v01.png`, `A43_the_whole_time_v01.png`, `A43_the_whole_time_v02.png` | A01 v01 has detached red specks; A40 v01 has very tight sides; A43 v01’s lettering reaches the right edge and appears clipped; A43 v02 still has a faint isolated alpha-1 pixel above the first line. Prefer A01 v02, A40 v02 and A43 v03. |
| P1 — stale wardrobe | `scene01/scene01_pre_reveal_v01.png`, `scene01/scene01_narrator_cutout_v01.png` | N carries a dark shoulder bag and wears dark shoes, unlike the chosen hook/lineup look. Keep these out of the current opening; `scene01_pre_reveal_v02.png` fixes the pair-only master. |
| P2 — visible stray marks / tight margin | `accent_words/batch_A02_24/A04_three_months_v01.png`, `A05_matt_v01.png`; `accent_words/batch_A25_45/A26_confused_v01.png`, `A37_didnt_like_being_alone_v01.png`, `A41_never_found_out_why_v01.png` | A04 v01 has a noticeable single red dot above the phrase; A05, A26, A37 and A41 have smaller detached red/orange flecks. A04 v02/v03 attempts were rejected for adding a red background and were not copied into the project. Keep A04 v01 as DRAFT; do not programmatically retouch it. If the point distracts in the shot, the clean path is another imagegen pass. A04 also has only 10–11 px of side margin; A08 has 12 px on the right; A10 has 12 px on the right. Add transparent padding if these phrases need appreciable travel. |
| P2 — small residual alpha flecks | `accent_words/batch_A02_24/A15_double_date_v02.png`; `character_continuity/poses/CHAR_M_STAND34_v02.png` | A15 v02 has tiny isolated 1–7 px alpha components near the lower edge. M stand v02 has two isolated 1 px alpha components within the hair area by threshold inspection; they are not apparent at normal preview size. Clean only if they show in the actual comp. |
| P2 — align registered canvases | `scene04_movies/seated_cutouts/scene04_seated_M_v03.png` | This file is 941×1671; the corresponding N/B cutouts, BG/FG and other scene planes are 941×1672. Make the shared canvas height identical before expecting 1:1 placement. |

The transparent previews of several cutouts show a warm red/orange edge fringe: `scene04_movies/scene04_cinema_seat_fg_v01.png`, `scene04_movies/scene04_seated_trio_mg_v01.png`, current neutral character poses, and the separate fork strips. Some may be intended rim light/paper shadow, and I cannot judge its effect over the intended backgrounds from these isolated files. Confirm those edges in the actual composite before cleaning them.

## UNVERIFIED

- **Palmier composite and movement:** no registration or transformation has been tested. `scene01_pre_reveal_v02.png` and `scene01_hook_master_v02.png` are opaque 941×1672 RGB full-frame masters; the latter already shows Matt. The pair-only v02 supplies a clean start image, but neither master by itself demonstrates the planned reveal. Current separate poses need placement against the background before a moving reveal can be counted as working. The older `scene01_*_cutout_v01.png` set is not a reliable substitute for the current look.
- **Character grounding and anatomy in scene:** standalone character PNGs have no scene-specific contact shadows or checked floor/seat contact. No finger animation is recommended. In the close crop of `CHAR_N_PHONE_READING_v01.png`, fingertips overlap the phone edge; confirm that contact at intended scale. `CHAR_B_INSIST_34_v01.png` reads gently/neutral in isolation, so whether it supports the “insisted” beat needs a shot check.
- **Scene depth:** scene04’s BG already includes distant seat rows and its FG supplies two nearer seat backs; trio-to-seat contact and occlusion are unverified. The separate `scene04_seated_{N,B,M}_v03.png` cutouts allow separate planes; the grouped `scene04_seated_trio_mg_v01.png` does not allow independent character motion. Scene05 has a BG and a small FG sprig, but no character MG in that folder yet; the sprig intentionally touches the lower-left edge (corner alpha 250), so any movement must be checked for a hard cut at frame edge. Scene06’s FG v02 duplicates part of the jamb/sill already present in the BG and has no clean plate underneath; treat it as a static occluder at its original registration until a composite confirms the edge. Scene12 is one opaque BG master; the score’s character planes can supply MG/FG.
- **Typography in frame:** actual size/position, safe margins against the phone UI, reading duration, overlap with faces/objects, and the `BREAK UP` / `THREE MONTHS` reuses are untested in the edit. The source art is bold, but no full-size frame or phone mock-up was reviewed.
- **Motion, continuity and finish:** no parallax/pivots, hidden fill, scene-to-scene movement, continuous moving grain, transitions or full-length viewing were checked. All statements above describe actual PNG inspection and metadata, not an assembled video.

## Result

Most current source candidates pass spelling, broad paper style, basic alpha presence and absence of unintended story information. Keep the superseded red-background, stale-wardrobe and clipped A43 versions out of use; resolve the listed small edge/margin and one-pixel canvas items as needed. Scene registration, phone-size layout and movement still require an actual Palmier composite before these assets can be accepted as shots.

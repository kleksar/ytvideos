# Paper Detour Short 008 — phrase asset index

**Status:** v04 has 43 unique phrase PNGs for its 45 cue events. v05 adds 16 generated PNGs (four revised phrases plus twelve new ones) for a total of 57 timeline cue events; A19 reuses the existing `A05_matt_v01.png` and needs no duplicate. For active v06, the authored line-count map is [`title_line_counts_v06.json`](title_line_counts_v06.json), and the measured per-clip transforms are recorded in [`Edit/title_size_v06_face_plan_20261101.json`](../../../Edit/title_size_v06_face_plan_20261101.json). Use [`normalize_paper_accent_cues.py`](../../../../../automation/normalize_paper_accent_cues.py) to calculate consistent face height and full-alpha width for later Paper batches. See the [v05 montage delta](../../../Storyboard/PALMIER_V05_EDIT_20261101.md) and independent static QA of the older assets in [`Storyboard/asset_qa_independent.md`](../../../Storyboard/asset_qa_independent.md).

The table below records the original 45 cue IDs in [`Storyboard/scene_accent_score_en.md`](../../../Storyboard/scene_accent_score_en.md) and their v04 assets. Added and revised v05 cues are listed separately below. Cue repeats are separate timeline moments and intentionally reuse the same image file.

| Cue | Display text | PNG |
|---|---|---|
| A01 | EVERY SINGLE DATE | `A01_every_single_date_v02.png` (v01 has isolated alpha specks; use v02) |
| A02 | BREAK UP | `batch_A02_24/A02_break_up_v01.png` |
| A03 | AGAIN | `batch_A02_24/A03_again_v01.png` |
| A04 | THREE MONTHS | `batch_A02_24/A04_three_months_v01.png` — DRAFT; visible red dot above the phrase, no clean ImageGen retry accepted |
| A05 | MATT | `batch_A02_24/A05_matt_v01.png` — DRAFT; small detached red/orange fleck |
| A06 | MOVIES? | `batch_A02_24/A06_movies_v01.png` |
| A07 | THERE TOO | `batch_A02_24/A07_there_too_v01.png` |
| A08 | TAG ALONG | `batch_A02_24/A08_tag_along_v01.png` — DRAFT; only 12 px right margin, add transparent pad if it travels |
| A09 | ALONE | `batch_A02_24/A09_alone_v01.png` |
| A10 | HE’D TELL ME | `batch_A02_24/A10_hed_tell_me_v01.png` — DRAFT; only 12 px right margin, add transparent pad if it travels |
| A11 | HAD DIED | `batch_A02_24/A11_had_died_v01.png` |
| A12 | NO GIRLFRIEND | `batch_A02_24/A12_no_girlfriend_v01.png` |
| A13 | ALMOST NOBODY | `batch_A02_24/A13_almost_nobody_v01.png` |
| A14 | TERRIBLE PERSON | `batch_A02_24/A14_terrible_person_v01.png` |
| A15 | DOUBLE DATE | `batch_A02_24/A15_double_date_v02.png` — DRAFT; v01 has a red background (**DO NOT USE**), v02 has tiny 1–7 px alpha flecks near the lower edge |
| A16 | DIDN’T WORK OUT | `batch_A02_24/A16_didnt_work_out_v01.png` |
| A17 | HAD ENOUGH | `batch_A02_24/A17_had_enough_v01.png` |
| A18 | BREAK UP | Reuse A02: `batch_A02_24/A02_break_up_v01.png` |
| A19 | WITH MATT | `batch_A02_24/A19_with_matt_v01.png` |
| A20 | TALK ALONE | `batch_A02_24/A20_talk_alone_v03.png` (v01 has a red background; v02 retains a red halo; **DO NOT USE v01/v02**) |
| A21 | IN FRONT OF HIM | `batch_A02_24/A21_in_front_of_him_v01.png` |
| A22 | ANYMORE | `batch_A02_24/A22_anymore_v01.png` |
| A23 | ALL OUR DATES | `batch_A02_24/A23_all_our_dates_v01.png` |
| A24 | FEELING GUILTY | `batch_A02_24/A24_feeling_guilty_v03.png` (v01 has a red background; v02 retains a red halo; **DO NOT USE v01/v02**) |
| A25 | MISERABLE LIFE | `batch_A25_45/A25_miserable_life_v01.png` |
| A26 | CONFUSED | `batch_A25_45/A26_confused_v01.png` — DRAFT; small detached red/orange fleck |
| A27 | MOM WAS ALIVE | `batch_A25_45/A27_mom_was_alive_v01.png` |
| A28 | A BROTHER | `batch_A25_45/A28_a_brother_v01.png` |
| A29 | A SISTER | `batch_A25_45/A29_a_sister_v01.png` |
| A30 | A FIANCÉE | `batch_A25_45/A30_a_fiancee_v01.png` |
| A31 | STUDYING IN EUROPE | `batch_A25_45/A31_studying_in_europe_v01.png` |
| A32 | MAKE SENSE | `batch_A25_45/A32_make_sense_v01.png` |
| A33 | WE BROKE UP | `batch_A25_45/A33_we_broke_up_v01.png` |
| A34 | ABOUT 40 MINUTES LATER | `batch_A25_45/A34_about_40_minutes_later_v01.png` |
| A35 | MATT TEXTED ME | `batch_A25_45/A35_matt_texted_me_v01.png` |
| A36 | HAD TOLD HIM | `batch_A25_45/A36_had_told_him_v01.png` |
| A37 | DIDN’T LIKE BEING ALONE | `batch_A25_45/A37_didnt_like_being_alone_v01.png` — DRAFT; small detached red/orange fleck |
| A38 | I WAS THE ONE | `batch_A25_45/A38_i_was_the_one_v01.png` |
| A39 | ASKING MATT | `batch_A25_45/A39_asking_matt_v01.png` |
| A40 | DIFFERENT STORIES | `batch_A25_45/A40_different_stories_v02.png` (v01 has minimal edge padding) |
| A41 | NEVER FOUND OUT WHY | `batch_A25_45/A41_never_found_out_why_v01.png` — DRAFT; small detached red/orange fleck |
| A42 | THREE MONTHS | Reuse A04: `batch_A02_24/A04_three_months_v01.png` |
| A43 | THE WHOLE TIME | `batch_A25_45/A43_the_whole_time_v03.png` — DRAFT; v01 clipped the last letter and v02 had a stray pixel (**DO NOT USE**); v03 has fine red-orange pixels under its lower line |
| A44 | THOUGHT | `batch_A25_45/A44_thought_v01.png` |
| A45 | DOING ME A FAVOR | `batch_A25_45/A45_doing_me_a_favor_v01.png` |

Phrase overlays sit on a dedicated graphic track above the complete scene stills. Do not split the scene still into BG/MG/FG, create cutouts, or put text behind a character. Place each cue in the shared safe area, away from faces and meaningful gestures; keep it hidden until its narration trigger. Soft grain is added once in the final timeline and is not part of these PNGs.

## v05 revised and added assets

All PNGs below are complete transparent phrase overlays using the accepted cream cut-paper lettering with burnt-orange backing. Keep original v01 files intact. For v06, size from the cream face bounds, fit the full alpha bounds inside the approved safe width, and use the single anchor/three-level motion in the [v06 title calibration](../../../Storyboard/PALMIER_V06_TITLE_SIZE_20261101.md).

| Cue | Exact text | PNG |
|---|---|---|
| A11 | MOM HAD DIED | `batch_v05/A11_mom_had_died_v05.png` |
| A34 | ABOUT FORTY / MINUTES LATER | `batch_v05/A34_about_forty_minutes_later_v05.png` |
| A44 | MATT THOUGHT | `batch_v05/A44_matt_thought_v05.png` |
| A45 | DOING ME A | `batch_v05/A45_doing_me_a_v05.png` |
| N01 | WALK | `batch_v05/N01_walk_v05.png` |
| N02 | SHOPPING | `batch_v05/N02_shopping_v05.png` |
| N03 | HIS DAD WOULDN’T / SPEAK TO HIM | `batch_v05/N03_his_dad_wouldnt_speak_to_him_v05.png` |
| N04 | NO BROTHERS | `batch_v05/N04_no_brothers_v05.png` |
| N05 | OR SISTERS | `batch_v05/N05_or_sisters_v05.png` |
| N06 | SAY WHATEVER / IT WAS | `batch_v05/N06_say_whatever_it_was_v05.png` |
| N07 | DIDN’T WANT THIS / KIND OF RELATIONSHIP | `batch_v05/N07_didnt_want_this_kind_of_relationship_v05.png` |
| N08 | WHAT MY BOYFRIEND / HAD BEEN TELLING ME | `batch_v05/N08_what_my_boyfriend_had_been_telling_me_v05.png` |
| N09 | NOT JUST A / GIRLFRIEND | `batch_v05/N09_not_just_a_girlfriend_v05.png` |
| N10 | WITH MY / BOYFRIEND | `batch_v05/N10_with_my_boyfriend_v05.png` |
| N11 | ON OUR DATES | `batch_v05/N11_on_our_dates_v05.png` |
| N12 | FAVOR | `batch_v05/N12_favor_v05.png` |

The scenes in v05 remain one complete static full-frame diorama apiece. These PNGs are timed graphic cues over the scene images; they do not create BG/MG/FG scene plates, cutouts, masks, parallax or character motion. Add soft grain once in the final composition, not to the phrase files.

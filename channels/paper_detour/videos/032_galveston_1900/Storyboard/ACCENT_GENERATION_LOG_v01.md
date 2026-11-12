# Accent PNG generation log v01

- Episode: `032_galveston_1900`; Paper Detour; English long-form film.
- Source narration/audio unchanged. No audio rendering or editing.
- Reference images used: `channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png` and `MATCH.png`.
- Source output: `Source/Images/accent_v01/accent_atlas_imagegen_v01.png` (1536×1024 RGBA). Source alpha is transparent outside the generated title artwork.
- Generation method: one AI-rendered 4×4 contact sheet, then deterministic crops at equal 384×256 cells with 24px safe gutters; horizontal crop stays within the cell. Final individual PNGs are recreated after the editorial decision record. Transparent alpha retained.
- Manual visual check of source sheet: all 16 spellings present as requested; capitalization is uppercase for display while cue text preserves source capitalization. Material uses cream paper faces, orange edges and dimensional shadows. Glyph proportions are more condensed than the references; the set is a candidate pending final actual-scene comparison and independent review.
- No OCR or automated spelling check; phrase spelling was visually checked. Alpha checked; contact sheet has zero-alpha samples in the empty gutters. No claim of typographic acceptance or playback sync.
- Timings remain `PRELIMINARY`: source alignment only; recording was not auditioned for pauses, stress or cadence.

## Exact ImageGen prompt

> Create a transparent-background typography contact sheet only, intended to be cropped into sixteen separate Paper Detour accent title PNGs. Use the supplied accepted Paper Detour title PNGs as the precise visual style reference: broad heavy rounded handmade uppercase letters cut from warm cream paper, tactile fibers, slightly irregular hand-cut silhouette, rich orange paper thickness/outline, soft dimensional contact shadow. Match their material, color, rounded proportions and handmade finish; do not copy the reference words. A strict 4-column by 4-row grid of exactly sixteen separate wordmark groups. Keep every group centered within its own equal invisible cell and leave broad fully transparent gutters between cells; no connecting strokes or decorative elements between groups. Transparent pixels everywhere except the title lettering, edge and soft shadow. No backgrounds, no paper cards, no scene, no grid lines, no cell borders, no extra text, no numbers, no icons, no logos. Render these exact words with the exact line breaks below, one title per cell in row-major order. Preserve every letter and spacing; do not add or omit anything: Row 1: cell 1 EMPTY / AIR; cell 2 TOO / LOW; cell 3 LESS THAN / NINE FEET; cell 4 NO WEATHER / SATELLITES. Row 2: cell 1 NEARLY SIXTEEN / FEET; cell 2 AT LEAST / SIX THOUSAND; cell 3 BETTER CHANCE / NEXT TIME; cell 4 TWO CONNECTED / DEFENSES. Row 3: cell 1 RAISE THE / GROUND; cell 2 SEVENTEEN / FEET; cell 3 ABOUT / TWO THOUSAND / BUILDINGS; cell 4 A LIVING / CITY. Row 4: cell 1 THE NEW / GROUND; cell 2 SEVEN HUNDRED / JACKS; cell 3 MANY SMALLER / LIFTS; cell 4 CHANGED THE / GROUND. The image is a typographic asset sheet, not a poster or illustration.

## Cue crops
- `C01_empty_air_v01.png`: EMPTY / AIR; assigned scene `001`; contact-sheet cell 1, row 1.
- `C02_too_low_v01.png`: TOO / LOW; assigned scene `006`; contact-sheet cell 2, row 1.
- `C03_less_than_nine_feet_v01.png`: LESS THAN / NINE FEET; assigned scene `013`; contact-sheet cell 3, row 1.
- `C04_no_weather_satellites_v01.png`: NO WEATHER / SATELLITES; assigned scene `022`; contact-sheet cell 4, row 1.
- `C05_nearly_sixteen_feet_v01.png`: NEARLY SIXTEEN / FEET; assigned scene `035`; contact-sheet cell 1, row 2.
- `C06_at_least_six_thousand_v01.png`: AT LEAST / SIX THOUSAND; assigned scene `056`; contact-sheet cell 2, row 2.
- `C07_better_chance_next_time_v01.png`: BETTER CHANCE / NEXT TIME; assigned scene `068`; contact-sheet cell 3, row 2.
- `C08_two_connected_defenses_v01.png`: TWO CONNECTED / DEFENSES; assigned scene `069`; contact-sheet cell 4, row 2.
- `C09_raise_the_ground_v01.png`: RAISE THE / GROUND; assigned scene `074`; contact-sheet cell 1, row 3.
- `C10_seventeen_feet_v01.png`: SEVENTEEN / FEET; assigned scene `078`; contact-sheet cell 2, row 3.
- `C11_about_two_thousand_buildings_v01.png`: ABOUT / TWO THOUSAND / BUILDINGS; assigned scene `083`; contact-sheet cell 3, row 3.
- `C12_a_living_city_v01.png`: A LIVING / CITY; assigned scene `090`; contact-sheet cell 4, row 3.
- `C13_the_new_ground_v01.png`: THE NEW / GROUND; assigned scene `096`; contact-sheet cell 1, row 4.
- `C14_seven_hundred_jacks_v01.png`: SEVEN HUNDRED / JACKS; assigned scene `109`; contact-sheet cell 2, row 4.
- `C15_many_smaller_lifts_v01.png`: MANY SMALLER / LIFTS; assigned scene `110`; contact-sheet cell 3, row 4.
- `C16_changed_the_ground_v01.png`: CHANGED THE / GROUND; assigned scene `125`; contact-sheet cell 4, row 4.

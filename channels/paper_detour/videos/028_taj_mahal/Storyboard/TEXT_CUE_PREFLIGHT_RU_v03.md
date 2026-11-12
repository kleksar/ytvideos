# Paper Detour 028 — text cue preflight RU v03

## Scope

Static placement mockups for the seven accepted accent lines in `Source/Script/NARRATION_RU_v07.md` and `Storyboard/STORYBOARD_RU_v01.md`. Each cue is a separate transparent PNG in `Source/Images/Text_Cues_RU_v03/`; each preview composites it over the corresponding complete scene PNG. The source dioramas remain static.

No voice, timing, alignment, cue animation, Palmier import, timeline edit, export, or publication was done. The `trigger` and `end` fields in the manifest are transcript landmarks for later alignment, not timings.

## Placement and type

- Scene and preview canvas: 941×1672 px.
- Shared cream-face cap height: 50 px, measured from the separate horizontal row runs of cream face pixels; the previous 0.055H estimate is superseded.
- Main anchor: center x=0.50, y=0.13; visible alpha safe width 847 px (90% of canvas width).
- S11 alternate anchor: center x=0.35, y=0.17; visible alpha safe width 659 px (70% of canvas width), keeping the question away from Ahmad's hair on the right and the king's head below.
- Size calculation: render every cue at one base size, measure cream-face cap height and full alpha width, compute the maximum shared cap height allowed by each cue's safe width, then round down to the next 10 px. S01 is the limiting line: at a 50 px cap its alpha width is 707 px; at 60 px it would exceed the 847 px main safe width.
- Provisional mockup typeface: SF NS Rounded, Black variation, which supports the Russian glyphs. This is a local visual substitute, not a confirmed Paper Detour brand font. The cream texture, orange cut edge/extrusion and soft shadow are sampled to match the approved 001 title PNG reference.

## Cue sheet

| Scene | Text and line breaks | Zone | Landmark trigger → end |
|---|---|---|---|
| S01 | Конечно. У меня<br>хорошо получается. | Main | `Конечно.` → `получается.` |
| S02 | Цена одного<br>ответа | Main | `Именно за этот ответ` → `руки.` |
| S04 | 22 года точности | Main | `двадцать два года` → `мелочь.` |
| S06 | Никакого<br>повторения | Main | `чтобы кто-то построил` → `подобное.` |
| S08 | Работа вне<br>досягаемости | Main | `взяться за следующую работу` → `нечем.` |
| S10 | За шедевром —<br>человек | Main | `слишком хорошо выполнить свою работу` → `Ахмада.` |
| S11 | Ты будешь<br>дальше<br>работать<br>архитектором? | Alternate | `ты будешь` → `архитектором?` |

## Review

All seven full-frame composites were inspected individually, followed by a 360 px wide phone-size contact sheet. Text remains inside the frame and the approved safe-width limits. S01, S02, S04, S06, S08, and S10 fit the open upper-center areas. S04 clears the scaffold top; S10 clears the Taj finial; S08 clears Ahmad's head. S11 uses the sole alternate zone and clears both figures. S03, S05, S07 and S09 remain text-free.

The 270 px contact sheet is an overview only. Full-size composites and the 360 px phone-size sheet are in `Text_Cue_Preflight_RU_v03/`; machine-measured bounds, line counts, anchors, landmarks and untimed status are in `manifest.json` and `manifest.csv`.

## Consultation record

The required Extra High consultation was attempted three times in the YT Видео project chat; the visible mode was `Extra High` before each send. The UI returned process notes and `Ответ готов`, but no substantive recommendation appeared in the page or DOM. No external layout advice is represented as received or approved. The v03 placement is a coordinator preflight based on the accepted cue text, the current channel standard, and inspection of the actual scene PNGs; user approval is still required before import or use on a timeline.

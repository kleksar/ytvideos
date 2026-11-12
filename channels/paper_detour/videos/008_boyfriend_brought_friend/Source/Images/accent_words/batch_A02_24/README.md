# Paper Detour 008 — phrase accents A02–A24

## Scope

This folder contains standalone, transparent PNG phrase layers prepared for the accent words named in scenes 02–24. A18 intentionally reuses the A02 asset (`BREAK UP`); no separate A18 PNG was requested or created. A01 already exists elsewhere and is outside this batch.

Each image is one complete phrase layer. The letters are not separated into individually animatable pieces.

## Style references

- `/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png`
- `/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/MATCH.png`

The requested look follows those Paper Detour 001 samples: chunky rounded cut-paper capitals, warm ivory paper faces, orange-red backing/edges, light paper grain and a restrained paper shadow. The preliminary A01 asset was not used as the style authority. No system font was used.

## Prompt brief

Each phrase was generated separately with the built-in image generator, using the exact phrase below and its listed line break. The common prompt asked for one standalone, tightly cropped, transparent PNG phrase layer; exact visible wording only; a cohesive phrase rather than separate letters; handmade dimensional cut-paper typography matched to the two 001 references; a small transparent margin; and no card, scene, props, extra marks or added text. For A16, the prompt additionally specified the curly apostrophe U+2019 in `DIDN’T`.

The full verbatim prompt transcripts for A02–A10 were not retained in this folder; the index records their exact phrases and the line arrangements visible in the PNGs, alongside the reference/style brief used for the batch. A11–A24 were prompted using the common brief above, with the phrase-specific wording and line breaks below.

## Asset index

Folder: `/Users/diplomat/ytvideos/channels/paper_detour/videos/008_boyfriend_brought_friend/Source/Images/accent_words/batch_A02_24/`. Asset paths below are relative to it. The dimensions are the saved PNG canvas sizes.

| ID | Exact visible text and line break | PNG | Size |
|---|---|---|---:|
| A02 | `BREAK UP` | `A02_break_up_v01.png` | 2158 × 729 |
| A03 | `AGAIN` | `A03_again_v01.png` | 2057 × 764 |
| A04 | `THREE MONTHS` | `A04_three_months_v01.png` | 2206 × 713 |
| A05 | `MATT` | `A05_matt_v01.png` | 2080 × 756 |
| A06 | `MOVIES?` | `A06_movies_v01.png` | 2132 × 738 |
| A07 | `THERE TOO` | `A07_there_too_v01.png` | 2141 × 734 |
| A08 | `TAG ALONG` | `A08_tag_along_v01.png` | 2142 × 734 |
| A09 | `ALONE` | `A09_alone_v01.png` | 2022 × 778 |
| A10 | `HE’D TELL ME` | `A10_hed_tell_me_v01.png` | 2164 × 727 |
| A11 | `HAD` / `DIED` | `A11_had_died_v01.png` | 1423 × 1105 |
| A12 | `NO` / `GIRLFRIEND` | `A12_no_girlfriend_v01.png` | 1749 × 899 |
| A13 | `ALMOST` / `NOBODY` | `A13_almost_nobody_v01.png` | 1648 × 954 |
| A14 | `TERRIBLE` / `PERSON` | `A14_terrible_person_v01.png` | 1774 × 887 |
| A15 | `DOUBLE` / `DATE` | `A15_double_date_v01.png` — **DO NOT USE: red background defect** | 1536 × 1024 |
| A15 | `DOUBLE` / `DATE` | `A15_double_date_v02.png` — preferred DRAFT; tiny 1–7 px alpha islands remain near lower edge | 1802 × 872, sRGBA |
| A16 | `DIDN’T` / `WORK OUT` | `A16_didnt_work_out_v01.png` | 1827 × 861 |
| A17 | `HAD` / `ENOUGH` | `A17_had_enough_v01.png` | 1570 × 1002 |
| A18 | Reuses A02: `BREAK UP` | — | — |
| A19 | `WITH` / `MATT` | `A19_with_matt_v01.png` | 1516 × 1038 |
| A20 | `TALK` / `ALONE` | `A20_talk_alone_v01.png` — **DO NOT USE: red background/halo defect** | 1536 × 1024 |
| A20 | `TALK` / `ALONE` | `A20_talk_alone_v02.png` — **DO NOT USE: wide red halo defect** | 1536 × 1024 |
| A20 | `TALK` / `ALONE` | `A20_talk_alone_v03.png` — current DRAFT; static text and background QA passed | 1581 × 995, sRGBA |
| A21 | `IN FRONT` / `OF HIM` | `A21_in_front_of_him_v01.png` | 1684 × 934 |
| A22 | `ANYMORE` | `A22_anymore_v01.png` | 2206 × 713 |
| A23 | `ALL OUR` / `DATES` | `A23_all_our_dates_v01.png` | 1536 × 1024 |
| A24 | `FEELING` / `GUILTY` | `A24_feeling_guilty_v01.png` — **DO NOT USE: red background/halo defect** | 1536 × 1024 |
| A24 | `FEELING` / `GUILTY` | `A24_feeling_guilty_v02.png` — **DO NOT USE: wide red halo defect** | 1536 × 1024 |
| A24 | `FEELING` / `GUILTY` | `A24_feeling_guilty_v03.png` — current DRAFT; static text and background QA passed | 2024 × 777, sRGBA |

## Checks performed

- Visually checked phrase text, punctuation and line arrangements. `MOVIES?` includes its question mark; `HE’D` and `DIDN’T` use curly apostrophes. A15 v01 has a red background defect; A20 and A24 v01 and v02 have red background/halo defects. All are marked **DO NOT USE**.
- The other 19 original PNGs were checked with ImageMagick: each is `sRGBA`, has non-opaque pixels, and all four corner alpha samples are zero.
- A15 v02 metadata: `1802 × 872`, `sRGBA`, non-opaque, all four corner alpha samples zero. Independent static review found tiny 1–7 px alpha islands near the lower edge; keep DRAFT and inspect against the actual scene before use.
- A20 v02 and A24 v02 are unusable because independent QA found wide red halos; do not use them despite their transparent corner samples.
- A20 v03 and A24 v03 are current drafts. Metadata checked: `sRGBA`, non-opaque, with zero alpha at all four corners. Independent static QA found the text correct and no broad red background; scene-scale edge/placement review remains open.
- Composited selected assets over a bright QA color to confirm that the apparent dark field in some previews is transparency, not a baked rectangular background. The saved PNGs themselves were not altered for this check.
- Visually checked outer letter/backing edges on the reviewed assets for obvious clipping. A15 v02 retains tiny isolated alpha islands; A20/A24 v03 pass the static text/background review. The generated shadow and antialiased edge pixels are retained.

## Limits

- These are image-generator outputs matched by visual reference, not vector lettering or a pixel-identical recreation of the 001 typography.
- A15 v01, A20 v01/v02, and A24 v01/v02 must not be used. A20 v03 and A24 v03 are the preferred DRAFT versions. A15 v02 has tiny lower-edge alpha islands; inspect all three at scene scale.
- No Palmier import, timeline composite, final on-screen scale/position, animation, overlap, phone-size readability, or synchronization check has been performed. They are prepared source layers, not a finished montage.
- The file dimensions vary with phrase length and generator composition. Place and scale each phrase in its own shot; do not assume a shared baseline, canvas, or registration across files.
- A18 should point to A02 during assembly; importing a duplicate A18 render would be unnecessary.

# Galveston 1900 — paper accent cue sheet v02

**Status:** 14 phrase PNGs delivered; static full-frame and phone-size author preflight complete; timing remains `PRELIMINARY`; sync and motion `UNVERIFIED`.

**Inputs:** unchanged English narration in `channels/nuviko_history/videos/017_galveston_1900/Source/Scripts/film_en.txt`; Odom `channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en_105.wav`, 1.05×, 574.402608 s; character alignment `channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en.alignment.json`; 30 fps. The source alignment is for 1.0× and these provisional times are divided by 1.05. Exact text/alignment coverage is available, but pronunciation and synchronization have not been checked by listening.

**Timing convention:** `start_frame` is floored to the first aligned character of the displayed phrase; `end_frame_exclusive` is ceiled to the end of its final aligned character. These are phrase windows, not approved animation or hold durations. Scene cuts, legibility hold and entrance/exit remain to be finalized after the actual cue PNGs and all assigned scene pairs are reviewed.

| ID | Text | Exact spoken trigger / end | Start–end (s, estimated) | Frames `[in, out)` | Scene | Function | Anchor / line plan | Pair preflight |
|---|---|---|---:|---:|---|---|---|---|
| C02 | `too low` | “when the ground beneath it is too low?” / `low` | 24.381–25.067 | 731–752 | 006 | Central problem | primary `[0.50, 0.20]` / `TOO LOW` | Technical `PASS`; static visual author review `PASS` |
| C03 | `less than nine feet` | “was estimated to be less than nine feet above sea level” / `feet` | 51.505–52.724 | 1545–1582 | 013 | Qualified vulnerability scale | primary `[0.50, 0.20]` / `LESS THAN` / `NINE FEET` | Technical `PASS`; static visual author review `PASS` |
| C04 | `no weather satellites` | “there were no weather satellites, no radar maps on a phone” / `satellites` | 84.190–85.333 | 2525–2560 | 022 | Period information gap | primary `[0.50, 0.20]` / `NO WEATHER` / `SATELLITES` | Technical `PASS`; static visual author review `PASS` |
| C05 | `nearly sixteen feet` | “The storm surge was later estimated at nearly sixteen feet” / `feet` | 151.543–153.067 | 4546–4592 | 035 | Qualified surge scale | primary `[0.50, 0.20]` / `NEARLY SIXTEEN` / `FEET` | Technical `PASS`; static visual author review `PASS` |
| C06 | `at least six thousand` | “At least six thousand people died” / `thousand` | 236.114–237.562 | 7083–7127 | 056 | Human cost, preserving lower-bound wording | primary `[0.50, 0.20]` / `AT LEAST` / `SIX THOUSAND` | Technical `PASS`; static visual author review `PASS` |
| C07 | `better chance next time` | “how to give it a better chance next time” / `time` | 294.527–296.076 | 8835–8883 | 068 | Turn toward prevention | primary `[0.50, 0.20]` / `BETTER CHANCE` / `NEXT TIME` | Technical `PASS`; static visual author review `PASS` |
| C09 | `raise the ground` | “They would raise the ground” / `ground` | 316.571–317.943 | 9497–9539 | 074 | Surprising engineering idea | primary `[0.50, 0.20]` / `RAISE THE GROUND` | Technical `PASS`; static visual author review `PASS` |
| C10 | `seventeen feet` | “Its top rose seventeen feet above mean low water” / `feet` | 335.010–336.000 | 10050–10080 | 078 | Seawall scale | primary `[0.50, 0.20]` / `SEVENTEEN FEET` | Technical `PASS`; static visual author review `PASS` |
| C11 | `About two thousand buildings` | “About two thousand buildings were raised” / `buildings` | 356.724–358.248 | 10701–10748 | 083 | City-scale operation; preserve “About” | primary `[0.50, 0.20]` / `ABOUT` / `TWO THOUSAND` / `BUILDINGS` | Technical `PASS`; static visual author review `PASS` |
| C12 | `a living city` | “It was a living city, full of structures that had to be kept in place” / `city` | 388.876–390.095 | 11666–11703 | 090 | Ongoing life amid construction | primary `[0.50, 0.20]` / `A LIVING CITY` | Technical `PASS`; static visual author review `PASS` |
| C13 | `the new ground` | “sand gradually became the new ground on which the city would stand” / `ground` | 422.248–423.162 | 12667–12695 | 096 | Tangible grade-raising result | primary `[0.50, 0.20]` / `THE NEW GROUND` | Technical `PASS`; static visual author review `PASS` |
| C14 | `seven hundred jacks` | “workers used seven hundred jacks to raise it five feet” / `jacks` | 483.276–484.419 | 14498–14533 | 109 | Attributed church-lift detail | primary `[0.50, 0.20]` / `SEVEN HUNDRED` / `JACKS` | Technical `PASS`; static visual author review `PASS` |
| C15 | `many smaller lifts` | “by the patient coordination of many smaller lifts” / `lifts` | 492.952–494.248 | 14788–14828 | 110 | Counterintuitive lifting method | primary `[0.50, 0.20]` / `MANY SMALLER` / `LIFTS` | Technical `PASS`; static visual author review `PASS` |
| C16 | `changed the ground` | “They changed the ground beneath it” / `ground` | 557.105–558.095 | 16713–16743 | 125 | Concluding transformation | primary `[0.50, 0.20]` / `CHANGED THE GROUND` | Technical `PASS`; static visual author review `PASS` |

## Final geometry and assets

- Canvas `1672×941`; shared measured face height `88 px` (minimum `68 px`). All 14 active cues use one primary anchor centered at `[0.50, 0.20]`; there is no active alternate anchor.
- Importable transparent PNGs: `Source/Images/accent_png_v03/` (14 phrase files, one per active cue). Source title art and its provenance remain in `Source/Images/accent_v01/` and `accent_v02/`; scene-aware omissions C01 and C08 are documented in [cue_layout_review_v02.md](cue_layout_review_v02.md).
- Exact per-cue line breaks, measured alpha/face bounds, scales, input hashes and pair output paths are recorded in [accent_preflight_v04/manifest.json](accent_preflight_v04/manifest.json). The input geometry is [accent_render_input_v04.json](accent_render_input_v04.json).
- All 14 assigned scene/cue pairs were checked as actual full-frame and 360-pixel phone-size composites. Renderer geometry reports `technical: PASS`; full-frame and phone-size visual status is the author’s static review, not an independent review. Contact sheets: [full frame](accent_preflight_v04/review_contact_sheets/accent_pairs_full_v04.jpg) and [phone size](accent_preflight_v04/review_contact_sheets/accent_pairs_phone_v04.jpg).
- Scene/cue positions are still static. Entrance, exit, hold durations and motion path are `PENDING`; they must be planned and reviewed before edit. The phrase windows above are estimates from the 1.0× character alignment scaled to the existing 1.05× voice.
- Existing voice was not auditioned during this caption work. Timing remains `PRELIMINARY`; spoken cadence, exact sync, motion, Palmier import, edit and MP4 playback QA remain `UNVERIFIED` or not performed.

## Excluded candidate cues

- C01 `empty air`, scene 001: omitted because both tested anchors covered important raised-doorway or house-façade evidence; the scene and narration already establish the exposed space.
- C08 `two connected defenses`, scene 069: omitted because the top-right trial touched/overlapped an engineer’s hair and the centered trial was worse; keep all three engineers and the tabletop model unobstructed.
- Both omissions follow [cue_layout_review_v02.md](cue_layout_review_v02.md). Earlier candidate text, timing and artwork remain in the v01 sheet, source PNG folders and original phrase-selection record.

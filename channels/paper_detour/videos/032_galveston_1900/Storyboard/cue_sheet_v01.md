# Galveston 1900 — paper accent cue sheet v01

**Status:** working selection; timing `PRELIMINARY`; PNG/composite preflight pending.

**Inputs:** unchanged English narration in `channels/nuviko_history/videos/017_galveston_1900/Source/Scripts/film_en.txt`; Odom `channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en_105.wav`, 1.05×, 574.402608 s; character alignment `channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en.alignment.json`; 30 fps. The source alignment is for 1.0× and these provisional times are divided by 1.05. Exact text/alignment coverage is available, but pronunciation and synchronization have not been checked by listening.

**Timing convention:** `start_frame` is floored to the first aligned character of the displayed phrase; `end_frame_exclusive` is ceiled to the end of its final aligned character. These are phrase windows, not approved animation or hold durations. Scene cuts, legibility hold and entrance/exit remain to be finalized after the actual cue PNGs and all assigned scene pairs are reviewed.

| ID | Text | Exact spoken trigger / end | Start–end (s, estimated) | Frames `[in, out)` | Scene | Function | Anchor / line plan | Pair preflight |
|---|---|---|---:|---:|---|---|---|---|
| C01 | `empty air` | “the front doors of Galveston opened onto empty air” / `air` | 3.581–4.343 | 107–131 | 001 | Opening paradox | Pending typography/contact-sheet review | Scene accepted; PNG and geometry pending |
| C02 | `too low` | “when the ground beneath it is too low?” / `low` | 24.381–25.067 | 731–752 | 006 | Central problem | Pending typography/contact-sheet review | Scene accepted; PNG and geometry pending |
| C03 | `less than nine feet` | “was estimated to be less than nine feet above sea level” / `feet` | 51.505–52.724 | 1545–1582 | 013 | Qualified vulnerability scale | Pending typography/contact-sheet review | Scene accepted; PNG and geometry pending |
| C04 | `no weather satellites` | “there were no weather satellites, no radar maps on a phone” / `satellites` | 84.190–85.333 | 2525–2560 | 022 | Period information gap | Pending typography/contact-sheet review | Scene accepted; PNG and geometry pending |
| C05 | `nearly sixteen feet` | “The storm surge was later estimated at nearly sixteen feet” / `feet` | 151.543–153.067 | 4546–4592 | 035 | Qualified surge scale | Pending typography/contact-sheet review | Scene accepted; PNG and geometry pending |
| C06 | `at least six thousand` | “At least six thousand people died” / `thousand` | 236.114–237.562 | 7083–7127 | 056 | Human cost, preserving lower-bound wording | Pending typography/contact-sheet review | Scene PNG pending |
| C07 | `better chance next time` | “how to give it a better chance next time” / `time` | 294.527–296.076 | 8835–8883 | 068 | Turn toward prevention | Pending typography/contact-sheet review | Scene PNG pending |
| C08 | `two connected defenses` | “A board of engineers proposed two connected defenses” / `defenses` | 297.981–299.733 | 8939–8992 | 069 | Paired solution | Pending typography/contact-sheet review | Scene PNG pending |
| C09 | `raise the ground` | “They would raise the ground” / `ground` | 316.571–317.943 | 9497–9539 | 074 | Surprising engineering idea | Pending typography/contact-sheet review | Scene PNG pending |
| C10 | `seventeen feet` | “Its top rose seventeen feet above mean low water” / `feet` | 335.010–336.000 | 10050–10080 | 078 | Seawall scale | Pending typography/contact-sheet review | Scene PNG pending |
| C11 | `About two thousand buildings` | “About two thousand buildings were raised” / `buildings` | 356.724–358.248 | 10701–10748 | 083 | City-scale operation; preserve “About” | Pending typography/contact-sheet review | Scene PNG pending; onset placed at scene 083 cut (difference <1 frame) |
| C12 | `a living city` | “It was a living city, full of structures that had to be kept in place” / `city` | 388.876–390.095 | 11666–11703 | 090 | Ongoing life amid construction | Pending typography/contact-sheet review | Scene PNG pending |
| C13 | `the new ground` | “sand gradually became the new ground on which the city would stand” / `ground` | 422.248–423.162 | 12667–12695 | 096 | Tangible grade-raising result | Pending typography/contact-sheet review | Scene PNG pending |
| C14 | `seven hundred jacks` | “workers used seven hundred jacks to raise it five feet” / `jacks` | 483.276–484.419 | 14498–14533 | 109 | Attributed church-lift detail | Pending typography/contact-sheet review | Scene PNG pending |
| C15 | `many smaller lifts` | “by the patient coordination of many smaller lifts” / `lifts` | 492.952–494.248 | 14788–14828 | 110 | Counterintuitive lifting method | Pending typography/contact-sheet review | Scene PNG pending |
| C16 | `changed the ground` | “They changed the ground beneath it” / `ground` | 557.105–558.095 | 16713–16743 | 125 | Concluding transformation | Pending typography/contact-sheet review | Scene PNG pending |

## Shared geometry and assets

- Exact typography reference: `channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png` and `MATCH.png`; exact scene/style reference remains `channels/paper_detour/videos/004_last_video/Storyboard/user_reference_parallax_20261101.png`.
- Phrase PNGs, line breaks, face/alpha bounds, shared face height, canvas coordinates, primary anchor and the single allowed alternate anchor: `PENDING` until the complete 16-phrase set and all assigned scene PNGs are available for joint review.
- Per-pair full-frame/phone-size composites and visual collision review: `PENDING`. No title PNG is ready for Palmier import.
- In/out motion and hold durations: `PENDING`; phrase windows above only locate the narration. Any final movement must use the Paper Detour accent-motion procedure.
- Playback sync/MP4 QA: `UNVERIFIED`; no edit or export exists.

# Paper Detour 028 — English text-cue preflight v01

## Scope

Static mockups of seven working English adaptations, composited over the accepted full-frame scene PNGs. The 95-word English narration v01 is user-approved, and a voice-only recording exists at `Source/Voice/lawrence_v01/voice_en.mp3` (35.520 s). Cue timing/alignment, animation, and Palmier import are not part of this preflight.

## Cue set and geometry

Canvas: 941 × 1672 px. Shared visible cream-face cap height: **60 px**. Primary visible-text center: **x=0.50, y=0.13** with a 847 px alpha-width limit (90% of frame). S11 uses the previously reserved alternate left zone at **x=0.35, y=0.17**, with a 659 px width limit (70% of frame). S11 keeps the same cap height.

| Scene | Working English cue | Line breaks | Center | Alpha width | Placement review |
|---|---|---|---:|---:|---|
| S01 | Of course. I'm good at it. | Of course. / I'm good at it. | 0.50, 0.13 | 405 px | Pass — clear dark arch opening; both speakers' faces and gestures remain visible. |
| S02 | The Price of One Answer | The Price of / One Answer | 0.50, 0.13 | 461 px | Pass — reads in the upper dark-blue opening; clear of the king's gesture and Ahmad. |
| S04 | 22 Years of Precision | 22 Years of Precision | 0.50, 0.13 | 788 px | Pass — fits the primary safe width; clear of Ahmad, the model, dome and scaffolding. This is the widest line and the tightest width fit. |
| S06 | No One Else Could Replicate It | No One Else / Could Replicate It | 0.50, 0.13 | 540 px | Pass — stays inside the arch opening, above the king and Taj Mahal. |
| S08 | A Craft Beyond His Reach | A Craft Beyond / His Reach | 0.50, 0.13 | 494 px | Pass — clear of Ahmad's head, hands, model and drawing. |
| S10 | Behind the Masterpiece: A Man | Behind the / Masterpiece: A Man | 0.50, 0.13 | 612 px | Pass — text sits above the central finial with visible separation. |
| S11 | Will You Keep Working as an Architect? | Will You Keep / Working as an / Architect? | 0.35, 0.17 | 426 px | Pass — reserved alternate clears both heads and keeps the king's question readable. |

## Visual system

The cream-paper fill, orange cut edge and soft shadow were compared visually with the Paper Detour accent reference. `/System/Library/Fonts/SFNSRounded.ttf` in its Black variation is a local Latin-capable mockup substitute only; it is **not** the confirmed brand typeface. Final letterforms must be checked against the actual approved accent PNGs before any import.

The actual 941 × 1672 composites were inspected individually and together on the 270 px overview and 360 px phone-size contact sheet. All seven preserve their scene's primary faces, action and architectural clues in this static hold. The contact sheets do not validate an animated entrance/exit path or Shorts UI safe-zone during motion.

## Files

- Transparent working cue layers: `Source/Images/Text_Cues_EN_v01/`
- Full-frame composite previews, manifest and contact sheets: `Storyboard/Text_Cue_Preflight_EN_v01/`
- Generator: `Storyboard/render_text_cue_mockups.py`

## Timing and approval boundary

Cue strings are working English adaptations of the previously accepted Russian cue set. The English narration and recording now exist, but the cue phrases still need their exact spoken triggers/end words and frame mapping. The 35.520 s default-speed narration is shorter than the 44 s minimum implied by 11 scenes at 4 s each; reconcile scene holds against actual timing before animation or timeline work. No animation was rendered; no Palmier project was edited or imported. Existing RU cue files are retained for provenance and have not been deleted.

# English narration → accepted still mapping — 031 Jascon-4

## Consultation record

- Date/task/stage: 2026-11-01; choose one exact split to map 15 spoken paragraphs to 16 accepted Paper Detour stills, then review measured timing transitions.
- Coordinator/interface/URL: coordinator personally in Google Chrome, ChatGPT project `YT Видео`; [Narration Image Mapping](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0/c/6ae7a173-399c-83ed-a31e-ed2a6049fa5c).
- Exact visible mode before first request: `Extra High`.
- Inputs: working English narration `Source/Voice/voice_en_tts_v01.txt`; accepted stills `Source/Images/paper_v01/`; image meanings and accepted order from `Storyboard/storyboard_v01.md`.

### Narrow prompt sent

> You are the consultant in the already-open ChatGPT Extra High session; the coordinator requirement is satisfied by this request. One narrow task: resolve the mapping between this approved English narration and the 16 already-approved Paper Detour stills. The narration has 15 paragraphs, the image set 16 frames. Keep the wording and images unchanged. Choose exactly one paragraph to split across two adjacent images, and return a 16-row ordered map: image number + asset slug + exact spoken phrase shown over it. Mark the one split and phrase boundary. Do not assign durations/timecodes, propose new visuals, write accents/SFX, or re-edit the narration.
>
> Approved image order: 01_search_wreck (diver searches wreck), 02_hand_contact, 03_survivor_found, 04_tug_at_sea, 05_depth_section, 06_divers_arrive, 07_search_continues, 08_same_ship_missed_pass, 09_attempt_find, 10_air_pocket, 11_depth_time, 12_preparation, 13_diving_bell, 14_decompression, 15_surface_survivor, 16_surface_to_wreck.
>
> Approved English narration, 15 paragraphs:
> 1. At a depth of about 30 metres, a diver was searching for bodies inside a sunken tugboat.
> 2. He reached for a hand—and felt it grab him.
> 3. Someone was still alive in there. Could they bring him up?
> 4. To understand how he ended up inside, let's go back to the Jascon-4 disaster.
> 5. On May 26, 2013, the tugboat sank off the coast of Nigeria. There were twelve people on board.
> 6. The divers had come to recover the bodies. By then, they had already brought up four.
> 7. Harrison Okene, the ship's cook, was still inside the hull. The diver had not seen him on his first pass.
> 8. According to Okene, he tried to find the diver in the darkness, but returned to the air pocket.
> 9. There was still an air pocket inside the hull.
> 10. Okene spent more than sixty hours in it, at a depth of about 30 metres.
> 11. Now they had to get him out of the hull.
> 12. They guided him to the diving bell along a backup umbilical line.
> 13. After he was brought up, Okene was placed in a decompression chamber.
> 14. Okene was the only survivor. The other eleven crew members died.
> 15. The divers went down to search for bodies—and saved a man they never expected to find alive.

## Completed consultant answer

| Image | Asset | Exact spoken phrase |
|---:|---|---|
| 01 | `01_search_wreck` | At a depth of about 30 metres, a diver was searching for bodies inside a sunken tugboat. |
| 02 | `02_hand_contact` | He reached for a hand—and felt it grab him. |
| 03 | `03_survivor_found` | Someone was still alive in there. Could they bring him up? |
| 04 | `04_tug_at_sea` | To understand how he ended up inside, let's go back to the Jascon-4 disaster. |
| 05 | `05_depth_section` | On May 26, 2013, the tugboat sank off the coast of Nigeria. There were twelve people on board. |
| 06 | `06_divers_arrive` — split 1/2 | The divers had come to recover the bodies. |
| 07 | `07_search_continues` — split 2/2 | By then, they had already brought up four. |
| 08 | `08_same_ship_missed_pass` | Harrison Okene, the ship's cook, was still inside the hull. The diver had not seen him on his first pass. |
| 09 | `09_attempt_find` | According to Okene, he tried to find the diver in the darkness, but returned to the air pocket. |
| 10 | `10_air_pocket` | There was still an air pocket inside the hull. |
| 11 | `11_depth_time` | Okene spent more than sixty hours in it, at a depth of about 30 metres. |
| 12 | `12_preparation` | Now they had to get him out of the hull. |
| 13 | `13_diving_bell` | They guided him to the diving bell along a backup umbilical line. |
| 14 | `14_decompression_chamber` | After he was brought up, Okene was placed in a decompression chamber. |
| 15 | `15_surface_survivor` | Okene was the only survivor. The other eleven crew members died. |
| 16 | `16_surface_to_wreck` | The divers went down to search for bodies—and saved a man they never expected to find alive. |

**Only split:** paragraph 6 at the sentence boundary after “The divers had come to recover the bodies.” All wording and image assignments remain unchanged.

**Asset name normalization:** the consultant's output shortened frame 14 to `14_decompression`; the accepted PNG basename is `14_decompression_chamber_v01.png`. The mapping uses the actual accepted asset name; no image changed.

## Review and limits

The mapping fills all 16 accepted stills, preserves narrative order and the suspense of the hand contact and later air-pocket reveal. It is a phrase-to-image mapping only; it does not contain scene durations. The draft cut timings are recorded separately in `SCENE_TIMING_en_v01.md`. This mapping was not a request to make or edit a video.

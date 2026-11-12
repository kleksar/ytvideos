# How the Black Death Changed Work — Short remake v01

- Channel: Nuviko History (single-video remake requested by user).
- Source: exact 42.237098 s downloaded Short; H.264 picture replaced, source AAC retained without audio processing.
- Picture plan: 9 distinct generated portrait scenes, direct cuts, 30 fps; 1,267 frames (42.233333 s video), 4.63–4.70 s per scene.
- Story source: retained source audio, aligned with WhisperX large-v3-turbo and English forced alignment; use exact word sequence and timing in `Source/Shorts/05_labour/audio_word_times_v01.json`. “Nuviko” casing follows the source’s baked caption. Alignment scores are model-derived; this is not an audible review.
- Subtitle treatment: Nuviko centered one-line field-notes style, light text and current word amber on fixed dark panel; montage renderer supplies grouping.
- Output: 1440×2560, 30 fps, H.264/yuv420p/Rec.709, source AAC stream copied.
- Scene images are 941×1672 and upscaled to the 1440×2560 canvas; this does not add source detail.

| Scene | Frames | Seconds | Spoken beat | Image |
|---|---:|---:|---|---|
| S01 | 0–141 | 4.700 | Sparse hands in the field; introduce the labour shortage. | `Images/S01_labour_field_v01.png` |
| S02 | 141–282 | 4.700 | Empty workshop follows the line about fallen worker supply. | `Images/S02_empty_workshop_v01.png` |
| S03 | 282–423 | 4.700 | A survivor seeks better wages or another employer. | `Images/S03_employer_offer_v01.png` |
| S04 | 423–564 | 4.700 | A worker weighs another employer or conditions. | `Images/S04_worker_choice_v01.png` |
| S05 | 564–705 | 4.700 | Higher costs bring workers and landowners into negotiation. | `Images/S05_owner_worker_negotiation_v01.png` |
| S06 | 705–846 | 4.700 | Government attempts to restrain wages. | `Images/S06_labour_council_v01.png` |
| S07 | 846–987 | 4.700 | Workers face restrictions in practice. | `Images/S07_worker_stopped_v01.png` |
| S08 | 987–1128 | 4.700 | Labour law sets conditions and forces work. | `Images/S08_field_work_rules_v01.png` |
| S09 | 1128–1267 | 4.633 | Nuviko traveler presents the coin display during the retained CTA. | `Images/S09_traveler_cta_v01.png` |

## Acceptance and limits

The nine stills and CTA traveler image received author inspection before render. The word map is an ASR/forced-alignment draft; rendered MP4 will be delivered for user review without additional post-render QA, per project instruction. No separate SRT was requested.

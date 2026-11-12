# Short 03 accent cue sheet — review assembly

User authorized five proposed phrases and requested the complete video with accents; original voice remains unchanged. Editorial decision record: `ACCENT_EDITORIAL_DRAFT.md`. Recording identity and full render receipt are preserved under `Work/rework_20261102/full_review_accents_v02/`. Input pro_v2 recording, 1×; subtitle timings and spoken delivery remain unverified by listening. These timings are review candidates, not final editorial sync acceptance.

| Cue | Text / two lines | Frames [start,end) at 30 fps | Scene | Trigger / end semantic beat | Anchor |
|---|---|---|---|---|---|
| C01 | READ THE / RADIO? | 12–78 | S01 | Opening question before screen explanation | primary |
| C02 | TWO / CHANNELS | 390–456 | S03 | two channels / different jobs | primary |
| C03 | TEXT AS / SOUND | 621–690 | S05 | representing same text / Japanese | alternate |
| C04 | DECODE, NOT / TRANSLATE | 951–1023 | S07 | computer's job / read it | primary |
| C05 | LISTEN OR / READ | 1143–1224 | S08 | listen in Portuguese / Japanese | primary |

Geometry at 1080×1920: shared maximum face-height per line 80 px, primary center (0.5,0.675), alternate (0.5,0.16). C03 primary rejected for cable overlap; alternate visually checked. All five real source PNGs, face line boxes and normalized bounds are in `accent_input_v02.json` and `Assets/Generated/accents-v03/manifest.json`. Half-scale compositing into 540×960 review, no per-cue size changes. Four-frame fade in and fade out, stable hold. No letter SFX or new sound.

Inspection: all five actual scene×cue static pairs checked, C03 alternate checked separately. Final decoded review frames sampled at start+4, midpoint, end−5 for each cue (15 frames), no apparent protected-object or subtitle overlap in these samples. This is coordinator self-review and limited coverage, not full/independent release QA or audible sync. Sampling contact sheet `Work/rework_20261102/full_review_accents_v02/cue_checks.jpg`. Full decode completed without error; copied AAC packet hash equals the continuous base review's hash, `e1e23bf59cef9353c3e47898eb17e4d8ad1a1bef9c82129f9d0e351adc84f456`.

Corrected preview-only scene concatenation to trim each cached motion clip to its planned frame count: caches contain two extra video frames each. Original cache and Palmier draft were not mutated. Full preview is 40.9 seconds and uses one continuous voice input; adding accents copies that preview's audio stream without re-encoding. This is a review video; canonical Palmier installation, delivery master and release QA remain pending.

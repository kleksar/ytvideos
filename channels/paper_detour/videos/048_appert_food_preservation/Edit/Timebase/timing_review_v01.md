# Paper 048 — timing and subtitle preparation record

- Audio duration from ffprobe: 163.280 s; MP3 mono, 44.1 kHz, 128 kb/s.
- Transcript alignment adapter: 450 words; exact transcript token count is also 450. This is machine alignment, not listening evidence.
- Independent WhisperX forced-alignment draft: 450 words, REVIEW_REQUIRED. Pause diagnostic reports 54 flags (53 onset differences >150 ms, 1 word spanning a measured quiet interval). Provider timing remains the current draft; no global offset applied.
- At tested anchors, provider vs WhisperX differences: word 1 `Pastry` +80 ms; word 81 `different` −137 ms; word 101 `preserved` −56 ms; word 201 `The` −11 ms; word 250 `a` +11 ms; word 351 `set` −4 ms; word 448 `a` −60 ms; final `guide` −220 ms. These are machine comparisons; speech onsets not audibly verified.
- Draft picture grouping: 30 plans, source frames 0–4896 at 30 fps; each interval 155–171 frames (5.167–5.700 s). Uses provider word boundaries and punctuation-aware transcript tokens; final cuts must conform to accepted scene plan and may change.
- Existing SRT v02 passes machine structure, literal text coverage and configured readability limits (≤2 lines, ≤42 characters) for duration 163.28 s. Timing mapping and playback remain UNVERIFIED. Manual segmentation review found cues splitting `Board of Arts and Manufactures`, `twelve thousand`, `Appert’s book`, and a cue ending in `with`; revise grouping before final sidecar/render. No subtitle/audio playback performed.

## Exact inputs and SHA-256

- `Source/Voice/en_v02_lawrence/voice_en.mp3` — `f2783158a8435e6114b10e98307c8991813611ca7cb44e90b365c9162910fb48`
- `Source/Script/narration_en_v01.txt` — `1bef1922911dacb6d0ffe7f35240a5d1dc6e71234c5b900b6358e2e4bc8e35be`
- `Source/Voice/en_v02_lawrence/voice_en.alignment.json` — `b959dedc0d2a91e730862da71024740e623259d910ee289d2f8970b9d1098edd`
- `Edit/Timebase/word_times_en_v01.json` — `5aefc7fc8f38e38e046dda94da3e3d44c3446aaa2e78ba3a985d0bcbd4559971`
- `Edit/Timebase/word_times_whisperx_v01.json` — `7129afb688f848a352f7ddc420305be2b6e833364bf74fe46618d9200ea98b7f`
- `Edit/Timebase/pause_diagnostic_v01.json` — `fa2770a7bac5383294a71e57c7db78873cf50e06328a28a0dd77258f87d1e1e2`
- `Deliverables/048_appert_food_preservation_en_v02.srt` — `5d2fac4e6e3a92d272063581a4305c4d01e0d0368bc1e92c1fcc752dac287307`
- `Edit/Consultations/srt_validation_v02.json` — `40d22923fcc43292318abfdc14b441cc75c95485e2dcf1bf6c0124cd8d46ff8a`
- `Edit/Consultations/timing_groups_draft_v02.tsv` — `8ee319904db359b8d8c59cf0acd944762f3dba448ee85eebcfa084278f6e2550`

The word map is diagnostic only; matching hashes and model agreement do not establish synchronization. Repeat changed-cue checks against the exact final audio and edit before the full render.

# Short 03 alignment diagnostic — 2026-11-02

Exact uncut recording: `Source/Voice/pro_v2/voice_en.mp3`, SHA-256 `2a6c71d187c8ecc835f134c5982322d2b774ab0085729567c0f07f1cdc62c871`; timeline starts at frame 0, 30 fps, no speed changes reported. Source map `voice_en.words.json` is provider-aligned, not accepted against listening. Independently ran local Whisper small on that exact MP3 with English word timestamps, output `whisper_draft/voice_en.json`; this is a second model estimate, not ground truth. 97 of 100 source tokens match its 99 tokens after normalization; `nineteen eighty-eight` / `1988` and `tenth` / `10th` are tokenization differences requiring reconciliation, not a change to narration.

| Word | Provider source onset (s) | Whisper estimate onset (s) | Difference (s) |
|---|---:|---:|---:|
| carried | 1.28 | 1.04 | +0.24 |
| Portuguese | 1.84 | 1.58 | +0.26 |
| channels | 13.04 | 12.94 | +0.10 |
| decode | 25.68 | 25.40 | +0.28 |
| receive | 36.48 | 36.46 | +0.02 |

Estimates differ unevenly, so neither a single global offset nor one machine map can be accepted as an audible correction. No listening perception is available to this agent; actual spoken onsets, word highlighting and full-track speech sync remain UNVERIFIED. Before importing the full subtitle track or final render, establish the word boundaries from the retained audio using the project alignment procedure and document frame-level evidence. These values are source seconds with identity mapping to the current untrimmed 30 fps timeline; candidate frames are onset × 30, rounded to the nearest frame for checking, not accepted cues. Voice remains unchanged.

# Short 02 subtitle timing comparison — 2026-11-02

## Inputs

- Review render: `../../../Deliverables/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_REVIEW_20261102_v02.mp4`, SHA-256 `629644be7a4f6c0ca6accd567cd0409c00556f948062846609c00cc52f6da01b`.
- Whisper word map: `../subtitle_asr_retime_20261102/asr_word_timing_map.json`, bound to the exact base video SHA-256 `460e308754dc3cdb7d477d37e3e1d0e816c3114bb51eb3e9eb9a00df30c0fc7c`.
- Original conformed provider alignment: `../subtitle_build_20261102/voice_alignment_conformed_1p05.json`, conformed to the same 1.05× timeline.
- Transcript: `../subtitle_build_20261102/narration_exact.txt`.
- New estimate: `forced_alignment_draft.json`, generated against the exact review render with WhisperX forced alignment. The input recording and transcript were read only.

## Comparison

All three maps contain 87 words in exact transcript order. Compared word-by-word, forced alignment is close to the conformed provider map: median onset difference +13 ms (mean +5 ms), with 3 onsets differing by more than 150 ms; endpoint difference median +19 ms, with 8 over 150 ms. The ASR map is systematically earlier than the provider map: median onset difference −131 ms (mean −163 ms), with 41 onsets differing by more than 150 ms. WhisperX vs ASR gives median +135 ms.

For “one hundred and two,” provider starts are 11.886, 12.038, 12.457 and 12.686 s; forced alignment estimates 11.945, 12.085, 12.406 and 12.586 s. Their onset differences are +59, +47, −51 and −100 ms. Whisper's starts (11.660, 11.777, 12.097 and 12.273 s) are earlier than both. The new estimate independently separates the four words instead of splitting one Whisper token proportionally.

## Decision

The provider alignment and forced-alignment estimate agree closely, while the ASR map is consistently earlier. This supports using the already conformed provider timing for a new **review-only** subtitle candidate, with local review on the few wider disagreements. It does **not** resolve audible synchronization; all maps remain machine-derived. Keep V3 and v02 review-only until the new candidate is visually rechecked and its speech timing is heard. `audible_sync=UNVERIFIED`; do not point `Deliverables/current.json` at v02 or use either review file as a release master. The retained narration/mix was not edited.

Next required check: compare representative openings, middles, endings, pauses, the disputed number, and the final cue against the retained speech by listening, then bind any accepted corrections to the exact edit and re-check the resulting export.

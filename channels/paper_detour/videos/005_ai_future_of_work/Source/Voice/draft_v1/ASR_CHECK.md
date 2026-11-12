# Automatic speech check — 31 October 2026

Whisper `tiny`, English, was run locally against `voice_en.mp3`; its JSON output is in `asr/voice_en.json`. A lowercase token comparison to `../narration_en_draft_v1.txt` gives 1225 source tokens, 1222 recognized tokens and a `difflib.SequenceMatcher` ratio of 0.992. This is a rough comparison, not a word error rate or proof that the words and timing are correct. `tiny` recognized the opening name as “Keden Mayashik”; an interrupted earlier run with Whisper `small` rendered the opening as “Kiran Maya Sheikh” but did not complete the audio. ASR spelling is not a reliable pronunciation judgment.

The recording, names (including Kiran Maya Sheikh, Anthropic and Julian Pintat), pacing, mix and provisional SRT have not been checked by listening. The full Whisper `small` run was interrupted before completion; it produced no complete output artifact. A complete viewing and listening check remains necessary before delivery.

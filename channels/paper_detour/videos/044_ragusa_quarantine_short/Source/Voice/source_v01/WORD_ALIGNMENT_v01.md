# Source speech alignment v01

- Decoder: local OpenAI Whisper `base.en`, CPU FP32; input: decoded 36-second source audio cut.
- Raw timed-word JSON: `source_audio_trim.json`; transcript has 109 Whisper token fragments over 9 segments.
- Conformed map: `Edit/Timeline/word_times_v01.json`, 107 tokens after merging hyphen fragments (`plague-affected`, `40-day`) and correcting ASR `Regusa` to `Ragusa` against the user-provided video title/description.
- Final recognized content word: “quarantine.” (35.46 s); audio tail continues to nominal 36.00 s. The old-channel CTA is outside the cut.
- The ASR output and timing are not independently listened to. The source audio has not been auditioned by a human reviewer; onset, spelling other than Ragusa, and sync remain machine-derived.

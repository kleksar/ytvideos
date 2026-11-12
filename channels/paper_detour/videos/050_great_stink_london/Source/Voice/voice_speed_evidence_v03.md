# English voice v03 speed and conform evidence

- ElevenLabs Lawrence v02 requested `speed=1.1` exactly once; source request and voice speed evidence: `voice_en_v02.request.json`, `voice_speed_evidence_v02.md`.
- Final mix `voice_en_v03_end_silence.wav`, SHA-256 `97e04a40368b7686ed28f16b97abb1d1b818aa97a187ff00cb4a4cb9c4f006db`, 44.1 kHz, mono, 252.8 seconds.
- Decoded v02 has 10,707,480 16-bit mono samples. The v03 PCM prefix is byte-identical to that decoding, followed by exactly 441,000 zero-valued samples (10 seconds); no offset or additional speed change.
- `word_times_v02_end_silence.json` preserves original timestamps and binds to the new mix; auditory validation is pending.

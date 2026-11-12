# Audio delivery v02 — exact end-card silence

- Accepted spoken source: `Source/Audio/narration_en_v26_110.wav`, SHA-256 `c4f81d49216ffb1c8767180ecef5f9199b3901c478946b3c582e105a4a38cf2a`, PCM S16LE mono 44.1 kHz, 149.459206 s. Original voice generation and single 1.10x atempo operation are documented in `speed_evidence_v01.md`.
- Derived final film mix: `Source/Audio/narration_en_v26_110_endcard_silence.wav`, SHA-256 `aec3ec03a8da8ea8df8252458814ba9e92331ad69eead732101c0c7b63899d75`, PCM S16LE mono 44.1 kHz, 159.466667 s.
- Operation: preserve every original PCM sample unchanged; append 10.007461 s of digital silence to cover the two 5 s silent end-screen scenes. No speech, speed, offset, fade, gain, music, SFX or other audio processing was added.
- Verification: exact decoded PCM prefix equality and a zero-valued trailing PCM tail were checked; ffprobe reports matching sample rate/channel/codec and 159.466667 s duration.
- Speech word map remains on the original speech-relative times; every spoken word is before the appended silence. Audible alignment remains unverified.

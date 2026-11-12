# Voice-only mix — EN v01 (superseded)

- Source: locked Lawrence TTS render `Source/Voice/en_v04_lawrence/voice_en.mp3` (52.88s). No words or timing were changed.
- Treatment: FFmpeg loudness normalization, two-pass analysis/render, `I=-16 LUFS`, `TP=-1 dBTP`, `LRA=7`; output 48 kHz, 24-bit PCM, stereo.
- Measured source: -24.48 LUFS integrated, -4.51 dBTP, LRA 2.10 LU.
- Measured output: -16.25 LUFS integrated, -3.74 dBTP, LRA 1.80 LU; PCM WAV duration remains 52.88s.
- Superseded by v02 after correcting the channel layout to mono. Its temporary stereo master was removed from the project and the local derivative was deleted; it is not part of the current timeline.
- This pass is deliberately voice-only. The sound-design consultation recommends a continuous ambient bed and a few quiet SFX, but the available Palmier balance is 1 credit and the viable bed dry-runs exceeded it. No top-up was attempted; no unrelated episode score was substituted.
- Playback and final export QA remain pending.

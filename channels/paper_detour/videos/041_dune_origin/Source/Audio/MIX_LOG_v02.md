# Voice-only mix — EN v02

- Source: locked Lawrence TTS render `Source/Voice/en_v04_lawrence/voice_en.mp3` (52.88s). No words, order, speed, or pauses were edited.
- Treatment: FFmpeg two-pass `loudnorm=I=-16:TP=-1:LRA=7`, dynamic mode, PCM master. No music or SFX were used in this pass.
- Measured source: -24.48 LUFS integrated, -4.51 dBTP, LRA 2.10 LU.
- Accepted mono master: 44.1 kHz, 24-bit PCM, 52.88 s; measured -16.2 LUFS integrated and -1.0 dBTP.
- Palmier import: mediaRef `7107A439`, swapped onto narration clip `9BF34941` on Timeline 1. The unused stereo intermediate v01 was removed from the project and local `Source/Audio`.
- Voice-only design choice: no unrelated episode music was substituted; generation dry-runs exceeded the remaining credit balance. The final MP4 must still be measured and played back during QA.

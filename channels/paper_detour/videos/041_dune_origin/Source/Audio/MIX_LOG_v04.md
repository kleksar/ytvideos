# Voice-only mix — EN v04, 1.10x with visual tail

- User direction: accelerate voice only to 1.10x; do not accelerate whole-video picture playback.
- Speech source: accepted voice-only master v02 (44.1 kHz mono PCM S24LE, 52.88 s). FFmpeg `atempo=1.1` applied once; result is 48.078277 s.
- To preserve the unchanged 52.9 s picture timeline and satisfy the FFmpeg renderer's full-length audio input requirement, 4.821723 s of silence is appended after speech. No music/SFX or loudness processing added. Final file: `voiceonly_master_en_v04_1p1_padded_to_52p9.wav`, mono PCM S24LE, 44.1 kHz.
- Word map v04 retimes the v02 official alignment by exact factor `1/1.1` and references the final padded audio. Last subtitle remains on-screen through the ending hold.
- Listening and final MP4 QA have not been performed.

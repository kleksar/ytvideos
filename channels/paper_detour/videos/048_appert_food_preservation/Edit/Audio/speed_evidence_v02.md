# Paper 048 — complete voice mix v02

- Accepted narration voice file: `/Users/diplomat/ytvideos/channels/paper_detour/videos/048_appert_food_preservation/Source/Voice/en_v02_lawrence/voice_en.mp3` (SHA-256 `f2783158a8435e6114b10e98307c8991813611ca7cb44e90b365c9162910fb48`), MP3 mono 44.1 kHz, 163.280 s.
- Voice generation speed was 1.10x exactly once in the source request; this file received no further speed transform.
- To fill the storyboard's 10-second end-card tail, FFmpeg `apad` extended the voice-only signal with digital silence to 173.200 s, PCM s16le mono 44.1 kHz. No music or effects added.
- Complete mix: `/Users/diplomat/ytvideos/channels/paper_detour/videos/048_appert_food_preservation/Work/production_local_v01/voice_fullmix.wav` (SHA-256 `1978cc6346ee7e3335221e6c3e89c0f93fd667d9b3e99e676ee8d7a4d6fc38b2`).
- Word timings copied unchanged from the prior WhisperX machine forced-alignment map and explicitly conformed to this mix by retaining the same speech start at 0.000 s; the appended interval begins after the source audio ends. Synchronization and pronunciation remain unverified by listening.

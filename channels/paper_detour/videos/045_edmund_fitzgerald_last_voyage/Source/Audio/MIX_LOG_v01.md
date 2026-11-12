# Audio mix EN v01

- Mix: [mix_en_v01.wav](mix_en_v01.wav), SHA-256 `46e4a989af29d5807e999acd711d68b0ea08b874076e46e76d85aaafab7b67da`.
- Source voice: [voice_en.mp3](../Voice/en_v01_lawrence/voice_en.mp3), SHA-256 `7f738c68beb162bb612133622697e7c280644efb7a74f985d7e568ee2ac012e9`; mono MP3, 44.1 kHz.
- Speed: 1.10× was applied once during TTS generation. The mix operation did not change speed, gain, pitch, cuts, or spoken timing.
- Contents: voice only; no music or SFX sources were assigned. Appended 10.006667 seconds of silence after the 212.96-second narration so the audio spans the complete 6689-frame, 30 fps film including two silent 5-second end screens.
- Mix format: PCM signed 16-bit, mono, 44.1 kHz, 222.966667 seconds. Created with FFmpeg `apad=whole_dur=222.966667`, trimmed to that exact duration.
- Alignment remains mapped to the unchanged opening narration interval; the silent tail is outside the spoken word map. Audible pronunciation, naturalness, balance and listening checks remain UNVERIFIED.

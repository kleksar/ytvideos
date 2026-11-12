# Voice record v01 — Paper Detour 042

- Script: `Source/Script/narration_en_v01.txt` (143 words; accepted EN narration).
- TTS request: ElevenLabs `eleven_v4`, Lawrence (`ktkP7Nsj67dw2zcplQYt`), one request; 44.1 kHz mono MP3; stability 1.0, similarity 0.0; provider speed unset.
- Original generated voice: `voice_en.mp3`, SHA-256 `cd35e960707e9a1b1901a1a9c6847ac490b45419143deab47d935f6a4853d4e4`, 57.040 s.
- Required Paper speed applied exactly once with FFmpeg `atempo=1.10`: `voice_en_1.10x.wav`, SHA-256 `76229d806087673875fd138091f21fe11436978fc06d41c92284cedc445fd326`; duration 51.859410 s; PCM 24-bit, 44.1 kHz, mono.
- Aligned character timing: `channels/paper_detour/videos/042_bird_migration_short/Source/Voice/en_v01_lawrence/voice_en_1.10x.alignment.json`. Provider character times were divided by 1.10; this is a mapped alignment, not forced alignment against the sped file.
- Human listening / subjective performance assessment: NOT DONE. No claim of naturalness, pronunciation acceptance or final-mix listening.
- Final audio is narration only at this stage; no music/SFX accepted or mixed.

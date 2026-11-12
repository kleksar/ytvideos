# Voice generation — EN v04 / Lawrence

- Input: `narration_tts.txt`, exact spoken text copied from user-approved `narration_en_v04.md`; narration words and order unchanged.
- Provider/model: ElevenLabs `eleven_v4` through `automation/elevenlabs/tts.py`.
- Voice: Lawrence `ktkP7Nsj67dw2zcplQYt`.
- Settings: stability 1.0; similarity 0.0; output `mp3_44100_128`; speed not set.
- Output: `voice_en.mp3`, mono, 44.1 kHz, 128 kbps, 52.88 s by ffprobe; alignment in `voice_en.alignment.json`.
- Palmier import: project `2C016BF5`, mediaRef `3259A64A` (ready).
- Raw alignment’s last character ends at 52.96 s, slightly beyond MP3’s 52.88 s reported duration; inspect final spoken word and encoded tail during final audio QA.

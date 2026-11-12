# Voice generation — Paper Detour 040

- Product language: English.
- Input: `../voice_en_tts_v01.txt` (8,884 characters; 1,407 whitespace-separated words), derived verbatim from the accepted narration with the markdown title removed.
- Narration source: `../../Script/narration_en_v01.md`; no wording changes were made for TTS.
- Provider/model: ElevenLabs / `eleven_v4`.
- Voice: Lawrence (`ktkP7Nsj67dw2zcplQYt`).
- Settings: stability 1.0, similarity 0.0, speed unset.
- Format requested: `mp3_44100_128`.
- Audio: `voice_en.mp3`; SHA-256 `c4d0974e5c9990386c4336d412fa86394ba015f532146f24669a935298126594`; 8,701,117 bytes.
- Alignment: `voice_en.alignment.json`; paragraph timing index: `PARAGRAPH_ALIGNMENT_v01.csv` (90 paragraph ranges derived from this alignment; scene ranges await storyboard review). SHA-256 `fde141efb7ea51b1d3df4fe36bd729c68a20160d89724bf2ba806f585bfb8d94`.
- Measured stream: MP3, 44,100 Hz, mono, 128,000 bit/s; duration 543.76 s; reported average bitrate 128,014 bit/s.
- Full FFmpeg decode: PASS.
- Alignment: 8,884 aligned characters match the stripped TTS input exactly. Last raw alignment end: 544.08 s, 0.32 s beyond the MP3 duration; clamp any derived word end to actual audio duration.
- Human listening/naturalness/pronunciation: UNVERIFIED. Machine checks and transcript alignment do not establish audible correctness.
- Speed remains unset pending scene/edit timing. Timing estimates must now be replaced from this audio and alignment.

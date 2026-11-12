# Audio mix v02 — speed 1.10x

- Source: accepted `Source/Voice/en_v04_lawrence/voice_en.mp3`, mono MP3 44.1 kHz, 332.24 s. The source generation log says the speed parameter was omitted; ElevenLabs documents its default speed as 1.0.
- Processing: FFmpeg `atempo=1.1` once, followed by 10 seconds of silence for the two end-screen scenes; trimmed to the 30 fps timeline duration of 312.033 s.
- Output: `full_mix_v02_speed110.m4a`, AAC-LC, mono, 44.1 kHz, encoded at 192 kb/s. Measured container duration 312.033 s; the original voice source is preserved.
- Text is unchanged. `Edit/Versions/word_times_v02_speed110.json` applies the same 1/1.1 conform to the existing provider alignment.

# TWL E001 v22 — author QA

MP4 SHA-256 `79c2583c78f89f80b055044803cc96918bef2459693e6e7ad42c64e58e1a14d7`, 30.8 s, 1080×1920, 30 fps, H.264 / AAC stereo 24 kHz. Settings preflight passed and the entire file decoded without errors. Frames 60, 150, 250, 310, 410, 530, 690, 820, 890 were visually inspected (`v22_sheet.jpg`); these do not cover every frame.

Audio: exact user text, ElevenLabs Mike `zfc8CJQpe8Kqyl0vvCzo`, `eleven_v4`, synthesis speed 1.10, mix playback 1.00; one authorized request, retained original music. Source files, full mix, request and edit operations are in `Source/Audio/v06`. FFmpeg silence detector at -40 dB and 250 ms found no qualifying intervals in the voice track or two concatenated iterations; this threshold method does not prove naturalness or absence of audible pauses or edits.

Local Whisper base recovered the narrative but recognized “he” instead of “you” around 12 s; the independently run small model recognized “you” as scripted (`whisper_small_v22.json`). These are machine results, not listening. SRT text coverage and structure pass (`srt_v22.json`); timings use ElevenLabs alignment remapped through the cuts and loop seam. Audible synchronization and quality of the silence cuts remain unverified. Subjective listening, phone playback, independent review and user acceptance: UNVERIFIED.

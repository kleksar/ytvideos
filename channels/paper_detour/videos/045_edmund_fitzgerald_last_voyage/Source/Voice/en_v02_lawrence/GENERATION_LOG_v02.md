# Voice generation — EN v02 attempt

- Purpose: test the subtitle-safe English production adaptation recorded in `Source/Production/EXTRA_HIGH_SUBTITLE_ADAPTATION_v01.md`.
- Input: `Source/Script/narration_en_tts_v02.txt`; request SHA-256 recorded in `voice_en.request.json`.
- Channel voice: Paper Detour / Lawrence `ktkP7Nsj67dw2zcplQYt`; model `eleven_v4`; MP3 44.1 kHz / 128 kbps; stability 1.0; similarity 0.0; speed 1.10.
- Result: HTTP 401 from the synthesis request. No audio or alignment file was created. The existing v01 voice/mix remain the only production audio. No blind retry or alternate account was used.
- Status: FAILED; this adaptation is not the narration used for a video until it has a matching generated voice and alignment.

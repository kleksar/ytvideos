# Paper Detour 033 — TTS provenance, narration v02

- Request result: SUCCESS; one EN job completed on 2026-11-02, exit 0. Both MP3 and alignment saved. No retry performed.
- User authorization: 2026-11-02, “Да: narration v02 + акценты v01, один TTS-запрос в ElevenLabs”. Scope: exactly one English narration request for the accepted v02 text. No music, SFX, additional takes, or retry authorized.
- Exact input: `Source/Script/NARRATION_EN_v02.txt` (667 UTF-8 bytes including final newline; 119 words; SHA-256 `af69eb8db211c132960531cf1a299ceda20d341a0483175b887e6c401214caba`).
- Destination: `Source/Voice/en_v02_lawrence/voice_en.mp3` and `voice_en.alignment.json`; versioned output directory was absent during preflight.
- Helper: `automation/elevenlabs/tts.py`; one English job only; dry-run completed without network.
- Planned endpoint: ElevenLabs `POST /v1/text-to-speech/ktkP7Nsj67dw2zcplQYt/with-timestamps?output_format=mp3_44100_128`.
- Voice ID: Lawrence `ktkP7Nsj67dw2zcplQYt`; model `eleven_v4`; output `mp3_44100_128`; stability `1.0`; similarity `0.0`; speed omitted.
- Request policy: one invocation, helper makes one request and has no automatic retry. If outcome is ambiguous, inspect destination and provider history before any new action; no second call under this authorization.
- Result: `voice_en.mp3` is MP3, mono, 44.1 kHz, 128,181 bit/s reported, 48.000 s container duration; 769,087 bytes. Alignment and normalized_alignment each contain 667 characters and end at 48.080 s; character string exactly matches accepted narration.
- Acoustic listening: UNVERIFIED. No playback QA claim is made; pronunciation, prosody, and final cue timing remain pending playback review.
- Review: after generation, verify both files and metadata, compare alignment to exact text, and listen to the actual MP3 before judging delivery or building final sync.

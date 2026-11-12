# Lawrence voice recording — v2

Generated 1 November 2026 after the user explicitly requested the narration. Service/tool documentation: [`automation/elevenlabs/README.md`](../../../../../../automation/elevenlabs/README.md); generator: [`tts.py`](../../../../../../automation/elevenlabs/tts.py).

- Text: [`narration_en_tts_v2.txt`](narration_en_tts_v2.txt), 660 characters, exact text supplied to ElevenLabs. It includes the ending “Because…” for the video loop and excludes the bracketed editorial loop instruction.
- Voice: Lawrence `ktkP7Nsj67dw2zcplQYt` (Paper Detour channel reference).
- Model/settings: `eleven_v4`; `stability=0.5`; `similarity_boost=0.0`; no generation-speed override.
- Audio: [`lawrence_v2/voice_en.mp3`](lawrence_v2/voice_en.mp3), MP3, mono, 44.1 kHz, 128 kbps, 44.80 s by ffprobe.
- Timing: raw API `voice_en.alignment.json` preserved. Every aligned character matches the 660-character request exactly. The final punctuation timing extended beyond decoded audio by 0.08 s; [`voice_en.alignment_clipped.json`](lawrence_v2/voice_en.alignment_clipped.json) clips timing ends to the physical MP3 duration. This derived file does not alter the audio.
- Integrity: full FFmpeg decode with `-xerror` passed. Whisper tiny on CPU and an independent Whisper base run transcribed the whole narrative and final “Because…”; expected text normalization (e.g. `55%`) is present. These are automated transcript checks only.
- Independent audio metrics: source voice measured at `−24.6 LUFS integrated` and `−4.1 dBTP` via FFmpeg ebur128. These are not final-mix measurements. At a `−45 dBFS` silence threshold, the file edge contains about `0.211 s` combined quiet at an untrimmed end-to-start splice (0.175 s tail + 0.036 s start); this does not establish perceived smoothness or lack of a click.
- First draft v1 is preserved in `lawrence_v1/`; its “bot's limited resource” phrasing was unclear in automated transcription, so v2 changed it to “this version had a limited number of credits … He couldn't add more.”

Human listening, pronunciation/acting review, and the audible loop into the first word have not been verified. The user has not yet approved this voice take. No video timeline, music, effects, subtitles, export, or publication were created.

## Dependency update — current script no longer matches v2

`Script/narration_en.txt` was edited after this recording (filesystem time 1 November 2026, 02:38 local). Its current resource line is: “But their conversation had used nearly half the bot's limited resource. Only fifty-five percent remained. He couldn't add more credits to this version.” The TTS v2 text and MP3 instead say: “But this version had a limited number of credits. After that night, only fifty-five percent remained. He couldn't add more.” The v2 MP3 and alignment remain valid records of what was generated, but are stale for the current script and must not be used to sync its shots or captions. No replacement audio has been generated.

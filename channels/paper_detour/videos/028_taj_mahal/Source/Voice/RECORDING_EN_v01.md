# Paper Detour 028 — English narration recording v01

Status: voice-only recording produced after the user approved `Source/Script/NARRATION_EN_v01.md` and said “озвучивай”. The English script is 95 words. The raw TTS input is `narration_en_tts_v01.txt` (541 characters after trimming its final newline).

## Current take

- File: `lawrence_v01/voice_en.mp3`
- Voice: Lawrence, `ktkP7Nsj67dw2zcplQYt`
- Model/settings: Eleven v4; stability 0.5; similarity boost 0.0; generation speed unset; output `mp3_44100_128`.
- `ffprobe`: MP3, mono, 44,100 Hz, 128,000 bit/s, 35.520 s, 569,303 bytes.
- Full decode: `ffmpeg -v error -xerror` completed with no errors.
- Voice-only measurements: −24.1 LUFS integrated, −4.7 dBFS true peak via FFmpeg `ebur128`. No gain adjustment or mastering was applied.
- API alignment: `voice_en.alignment.json` contains 541 characters and matches the TTS text exactly after stripping the input file's final newline. Its final closing quote ends at 35.60 s, 0.08 s beyond the MP3 duration. `voice_en.alignment_clipped.json` clips that endpoint to the physical 35.52 s file end; the audio is unchanged.
- Human listening, acting and pronunciation review have not been performed. The technical decode and alignment checks do not verify audible quality.

## Alternate speed request and pacing

A second full narration request used `speed=0.8` and is preserved in `lawrence_v02/`. It measured 36.240 s, only 0.720 s longer than the current default-speed take, so it does not solve the scene-duration fit and is retained as an alternate. The current take remains v01 because it follows the established Paper Lawrence settings without a generation-speed override.

The accepted storyboard has 11 scenes planned for roughly 4–6 seconds each (44–66 seconds overall). The current 35.520 s recording is shorter than that minimum; cue-frame/scene timing must be reconciled against the actual edit before animation or timeline work. No manual time-stretch was applied. ElevenLabs credit usage was not checked.

No music, SFX or mix was created. No Palmier timeline was edited and no assets were imported, exported or published.

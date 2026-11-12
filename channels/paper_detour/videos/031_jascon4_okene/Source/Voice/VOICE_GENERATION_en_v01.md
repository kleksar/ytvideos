# English voice generation — 031 Jascon-4 / Harrison Okene

## User direction and scope

- On 2026-11-01 the user corrected the prior language error and explicitly directed: “на английской делай”. The intended channel narration is English.
- Created one English voice file from a working English translation of the accepted Russian narration. No music, SFX, mix, editing, export, upload, or publication was performed.
- The Russian MP3 at `voice_ru.mp3` is the prior wrong-language artifact. It is retained for provenance and is not the current voice deliverable.
- Paper Detour voice: Lawrence (`ktkP7Nsj67dw2zcplQYt`), per `channels/paper_detour/AGENTS.md`.
- Speed was left unset because no accepted edit or actual scene timings exist.

## Text and translation provenance

- English working narration/TTS text: `Source/Voice/voice_en_tts_v01.txt` (1,106 characters, 15 paragraphs).
- English translation was produced in ChatGPT.com, project `YT Видео`, Google Chrome; exact visible model label before both narrow requests: `Extra High`.
- Translation consultation and exact prompts/responses: `Source/Voice/ENGLISH_TRANSLATION_EXTRA_HIGH_v01.md`; [consultation chat](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0/c/6ae79f8e-5e2c-83eb-82f3-6b8d49f965eb).
- The translation preserves the 15 narration blocks and factual claims in `Source/Script/narration_ru_v01.md`; a clumsy phrase was refined to “They guided him to the diving bell along a backup umbilical line,” matching the fact-check wording without implying a separate backup air supply.
- This English wording was created under the user's direct language instruction; it has not yet received a separate user read-through.
- SHA-256 TTS text: `57977e2264f06a5d5e0ec76fdbad681f37913b161988b52a4e3b98f58eb88fcc`.

## Generation

- Date: 2026-11-01.
- Provider/model/format: ElevenLabs / `eleven_v4` / `mp3_44100_128`.
- Voice: Lawrence (`ktkP7Nsj67dw2zcplQYt`).
- Settings: stability 1.0, similarity 0.0; speed unset; one request, no automatic retries.
- Status: **GENERATED**.
- MP3: `Source/Voice/voice_en.mp3`.
- Character alignment: `Source/Voice/voice_en.alignment.json`.
- SHA-256 MP3: `3c628dbdb72b5960d8dcb9289eaf653c3163d2b3751c4af7eb4e8dd293312a5e`.
- SHA-256 alignment: `97dfe9391b5fadbfa33f4327e2fb0386e1c4e81756ac500de6b993abc3694917`.

## Technical QA

- File size: 1,141,489 bytes.
- `ffprobe`: MP3, 44,100 Hz, mono, 128,000 bit/s; duration 71.28 s; average bitrate 128,113 bit/s.
- Full FFmpeg decode: **PASS**, no decode errors.
- Character alignment and normalized alignment each contain 1,106 characters, starts, and ends; concatenated characters match the stripped TTS text exactly. Last alignment end: 71.36 s, 0.08 s after the MP3 duration.
- `volumedetect`: mean −24.8 dB, peak −3.8 dB; no processing or normalization applied.
- Local Whisper base ASR recognizes the narration content and cue order, while normalizing spelled-out numbers. It transcribed `Jascon-4` phonetically as “jask on Ford” and `Okene` as “O’Kean”; this makes human listening especially important for those names. ASR is not pronunciation QA.
- Human listening review of naturalness, stress, and proper-name pronunciation: **NOT DONE**. The user should listen before scene timing is finalized.

## Open timing dependency

The English narration has 15 cue paragraphs while the accepted Paper storyboard has 16 diorama images. No scene assignment or timing edit was made here. Resolve the cue-to-image mapping before precise scene timings and downstream Paper accents.

# English narration voice — Short 035 v01

**Authorization:** On 2026-11-02 the user said: “го дальше. разрешаю озвучку.” Scope: English narration for Paper Detour Short 035. The user subsequently wrote “озвучка ок” on 2026-11-02; this accepts this voice version for continuation, not a final MP4/AV review. Music and SFX were not authorized.

**Input:** accepted `Source/Script/NARRATION_EN_v06.txt`, with only its service note `Стык (не озвучивать)` omitted. The exact spoken text is preserved in `voice_text_en.txt` (SHA-256 `69f7011e430d9d13632449a59aa9e04ccd9c2f53e41707a2ee46336278b70b55`).

**Voice / request plan:** Lawrence `ktkP7Nsj67dw2zcplQYt`; ElevenLabs `eleven_v4`; MP3 `mp3_44100_128`; stability 1.0; similarity 0.0; no generation speed parameter. One request through `automation/elevenlabs/tts.py --generate`, with character alignment requested by the project helper. No music/SFX.

**Direction source:** `Source/Voice/VOICE_DIRECTION_EXTRA_HIGH_20261102.md` (Google Chrome project consultation; exact visible label `Очень высокий`).

## Generation and technical checks

- One request completed successfully; no retries. Input is the exact accepted narration with the service loop note omitted.
- MP3: 44.16 s, mono, 44.1 kHz, declared 128 kb/s; `ffprobe` average format bitrate 128196 bit/s. Full `ffmpeg` decode completed without errors.
- `volumedetect`: mean -24.7 dB, peak -3.1 dB. `silencedetect` found pauses across the reading; no clipping signal was detected by this peak check.
- API character alignment and normalized alignment each contain 686 character entries. Raw alignment text exactly matches the 686-character TTS input; timestamps are monotonic and end at 44.24 s.
- Exact API-alignment trigger windows for current cue sheet: C01 13.28–15.60 s; C02 26.56–32.08 s. These are character-alignment-derived seconds, not frame placement or playback-verified sync.
- The user accepted this voice take with “озвучка ок” on 2026-11-02. No corrective regeneration is requested. Independent/recorded playback QA of pronunciation and the full loop remains unverified; no music/SFX were created.

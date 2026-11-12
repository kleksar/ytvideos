# 020 — Rarovista: long film for private review

Created 30 October 2026. This report covers the English long film only; Shorts have separate delivery and verification records.

## Deliverables

- `Deliverables/020_en_long_radio_game.mp4` — SHA-256 `5c3fd3206bf0347406e3ea0b711c305b9f252505b844ad1ba443224406eaf538`.
- `Deliverables/020_en_long_radio_game.en.srt` — SHA-256 `9a5064cff289471fa967ebb36f78b2ab03dda66a10ea4a43c734f8ead3ab4533`. The SRT is separate, not burned into the MP4.

The file is 273.066667 seconds, H.264 High, 1920×1080, 30 fps, 8192 video frames. Audio is AAC-LC mono, 44.1 kHz; encoder target 192 kbit/s, measured average approximately 179 kbit/s. The original ElevenLabs narration was supplied as a 128 kbit/s MP3; exporting AAC at a higher rate cannot recover information lost from that source.

## Montage and sound

The video uses 18 original still illustrations across 47 shots with slow zooms and pans. It is a moving illustrated montage, not character animation. At 02:52–03:09, the single repeated image was replaced by three shots: two recordings, investigation on a laptop, then comparison of waveform speeds. These are illustrative graphics, not representations of an actual archive, game screen or verified launch. The version retains the original v3 narration without speeding it up or shifting it.

An original synthesized sound effect accompanies the opening three seconds and the image is marked “ILLUSTRATIVE SOUND RECONSTRUCTION” from 00:00.2 to 00:03.15. The effect stem generated from the same formula and mix settings is `channels/paper_detour/videos/001_radio_game/Source/Audio/signal_reconstruction_3s.wav`. There is no music. The montage manifest is `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_manifest.json`; rendering is performed by `channels/paper_detour/automation/render_working_draft.py`. The separate Palmier project was not changed by this render.

## Verification

- FFmpeg `-xerror` decoded the whole exported file with no errors. Copy in Deliverables matched the source render by SHA-256.
- `ffprobe -count_frames` confirmed format, duration and 8192 frames. FFmpeg black detection reported no fully black frames under the chosen threshold (`pix_th=0.10`, `pic_th=0.99`).
- Decoded sound peak −1.9 dBFS, mean −24.2 dBFS. Correlation against the source narration at 10, 135 and 260 seconds yielded zero measured offset to 0.125 ms resolution. This is a technical sync check, not a listening review of voice quality or mix balance.
- Eight selected output frames were inspected, including the opening label and changes around 02:52–03:09; this is not a complete visual review of every transition.
- The separate SRT contains 85 chronologically ordered, non-overlapping cues ending at 04:33.000, within the 04:33.040 audio duration. It is derived from character alignment and has not been checked by listening.
- Full viewing and listening have not been performed. The signal and any pronunciation, audio balance, subtitles, visual continuity and chapter boundaries therefore remain subject to human playback review.

## Chapter cues

The narration is unchanged from v3, so the existing upload package remains applicable. Approximate cue starts are alignment-derived, not verified by listening. The left column is the YouTube whole-second timestamp, rounded down; the right column is the approximate speech start.

| YouTube | Approximate voice start | Chapter |
| --- | --- | --- |
| 00:00 | 00:00.000 | A sound worth recording |
| 00:34 | 00:34.240 | Two recordings, one question |
| 01:16 | 01:16.400 | A message written in whistles |
| 02:06 | 02:06.640 | A program takes the air |
| 02:54 | 02:54.960 | Decoding the old recording |
| 03:31 | 03:31.360 | The reported match |
| 04:06 | 04:06.400 | The sound and the message |

Visibility is intended to be private; this report does not assert that a YouTube upload has happened. The publication copy and limitations are in `channels/paper_detour/videos/001_radio_game/UPLOAD_READY.md`.
# Дополнительная проверка читаемости SRT

30 октября 2026 скрипт измерил длину строки относительно длительности каждой реплики: у фильма одна из 85 реплик превышает 22 знака/с (около 23,1); у Shorts 01 — две из 22 (до 24,0), у Shorts 02 — одна из 20 (22,4), у Shorts 03 — ни одной из 22. Это приблизительная проверка, не замена просмотру и проверке синхронизации на слух.

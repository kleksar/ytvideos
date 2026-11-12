# 053 technical export QA v01

File: `../full_technical_v01.mp4`; SHA-256 `52bba1e886eb98fe7ad1cee19f0c45e89d324bcf333cf004680492f704cbe562`.

- Technical: FFmpeg decoded entire file without error. ffprobe reports H.264 1440×2560 yuv420p bt709/tv, 1309 frames, 30/1 FPS, 43.633333 s; AAC mono 44100 Hz. Measured peak -4.5 dBFS, mean -24.5 dBFS. Video stream/frame timestamps, fast-start and full subjective playback were not separately checked.
- Visual: nine midpoint frames of actual export inspected in `contact.jpg`; full-frame paper images, no decorative outer frame. Subtitles visible in sampled frames. Actual crop/motion extremes and all word transitions not exhaustively reviewed.
- Timing: provider conform and WhisperX word onset estimates were compared, with differences up to 0.161 s. Audible voice, name pronunciation and word-level sync have not been verified. No audio listening is claimed. SRT is a draft with machine coverage only.
- Outcome: TECHNICAL CANDIDATE; NOT full AV QA PASS. No user acceptance or publishing permission.

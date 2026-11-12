# Paper 050 continuous music v03 — review mix

- Voice `Source/Voice/voice_en_v03_end_silence.wav`, SHA-256 `97e04a40368b7686ed28f16b97abb1d1b818aa97a187ff00cb4a4cb9c4f006db`. The existing 1.10× is retained. Voice is duplicated into two identical channels with no delay, trim, resampling, speed or gain change.
- Base `Source/Music/satiate_percussion.mp3`, SHA-256 `b6db5b3b74f17eeb013afd065d7bf6ecbc33c4f4db59bf1d797419cd0bb7ae35`. Kevin MacLeod — Satiate - only percussion, ISRC USUAN1200057, CC BY 4.0. Official card and pieces.json identify Satiate Percussion.mp3. Verified download https://incompetech.com/music/royalty-free/mp3-royaltyfree/Satiate%20Percussion.mp3, 7,705,211 bytes, 192.575 s. See CONSULTATION_BASE_20261106.md.
- Theme `Source/Music/signal_to_noise_no_piano.mp3`, SHA-256 `8e20b496b0614053565d4f43c80f469c84abd2aefb3ba01e29dfa813f49b9594`. Scott Buckley — Signal to Noise (No Piano Melody), CC BY 4.0. The author lists the exact alternative and requires the YouTube-description credit.
- Mix `Edit/Audio/mix_continuous_v03.wav`, SHA-256 `1cce49d58c9015a0c2911974566dc0b6118dd6214198bf53652f248d51c21967`. Stereo PCM s24 44.1 kHz, 11,148,480 samples per channel. Exact FFmpeg graph `Edit/Audio/music_continuous_v03.ffgraph`, SHA-256 `198c2e9326bfcb88e6a96009fb3fdd1e6592f57648d20c67124234fa82ffeca4`.
- Opening bed offset 3 s, gain 0.17, 80 ms anti-click fade; crossfade 104.5–109.1 s. Theme offset 8 s, gain 0.17. Return crossfade 212.2–217.0 s. Closing bed offset 120 s, gain 0.14. Base high-pass 60 Hz. Final fade 248.8–252.8 s after last word at 242.44 s. No planned gaps.
- Measured music via subtraction of sample-aligned voice. Lowest one-second stereo RMS outside final fade −43.0 dBFS. Transition RMS stereo/mono −38.1/−38.6 and −35.7/−36.4 dBFS. Audible balance, music fit and audible sync UNVERIFIED.
- `Edit/Audio/word_times_music_v03.json` retains the word array from `Work/visual_redesign_v01/word_times_trial_mix_v01.json`. Burned-in subtitle frames remain in the original video stream.

## Description credits for this edit

Music: “Satiate - only percussion” by Kevin MacLeod (incompetech.com), https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1200057. CC BY 4.0, https://creativecommons.org/licenses/by/4.0/. Edited, filtered and mixed with narration.

Music: “Signal to Noise” (No Piano Melody) by Scott Buckley, https://www.scottbuckley.com.au/library/signal-to-noise/. CC BY 4.0, https://creativecommons.org/licenses/by/4.0/. Edited and mixed with narration.

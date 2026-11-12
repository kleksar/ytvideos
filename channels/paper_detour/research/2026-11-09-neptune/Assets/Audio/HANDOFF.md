# EN review audio v01

Authorized for user review MP4, 2026-11-09. Voice source `/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-neptune/Source/Voice/en_v01/voice_en.mp3` SHA-256 `3f1ab751e1be694c7bf2d6a8d59045a9bacebe2cd5a3625edeec0eabd64ecd53`. Dry mono ElevenLabs recording, placed at zero; only one FFmpeg `atempo=1.10`, no cuts. Measured conformed voice 32.365833s; full stereo PCM 24-bit / 48 kHz mix 32.366667s, 971 frames at 30 fps. Voice center with −2 dB gain in full mix.

Mix SHA-256 `3967e47dc5fe0ba529fa8afb18b7b99badfb3a67bf54c7e05b344caeb6268fe3`. Exact provider alignment compared character for character to script. End time of the final word omits punctuation duration (provider clock extends past MP3); for US, the last letter timing also slightly exceeds the measured clip, so the final word terminates at the physical clip end. FFmpeg tail `silencedetect` detected trailing quiet from raw 476.988 s through 477.120 s, supporting this endpoint. No shift applied to earlier words. All intervals finite and monotonic; final map `/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-neptune/Work/word-times-final-v01.json` SHA-256 `88d4e6349e84829efd8b0e3f4efe5b3d6f85502b78a462fd1411b012bb927b63`.

Music: Signal to Noise — No Piano Melody, Scott Buckley, CC BY 4.0, https://www.scottbuckley.com.au/library/signal-to-noise/. For US, five-second crossfade to Night Vigil, Kevin MacLeod, CC BY 4.0, https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1900047.

Exact processing and measurement:

```json
{
  "voice": [
    "ffmpeg",
    "-nostdin",
    "-v",
    "error",
    "-n",
    "-i",
    "/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-neptune/Source/Voice/en_v01/voice_en.mp3",
    "-af",
    "atempo=1.10",
    "-ar",
    "48000",
    "-c:a",
    "pcm_s24le",
    "/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-neptune/Assets/Audio/voice-conform-v01.wav"
  ],
  "mix": [
    "ffmpeg",
    "-nostdin",
    "-v",
    "error",
    "-n",
    "-i",
    "/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-neptune/Assets/Audio/voice-conform-v01.wav",
    "-ss",
    "72",
    "-t",
    "33",
    "-i",
    "/Users/diplomat/ytvideos/channels/paper_detour/videos/050_great_stink_london/Source/Music/signal_to_noise_no_piano.mp3",
    "-filter_complex",
    "[0:a]pan=stereo|FL=c0|FR=c0,volume=-2dB[vox];[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=-22dB[m1];[m1]afade=t=in:d=0.6,afade=t=out:st=30.066667:d=2.3[music];[vox][music]amix=inputs=2:normalize=0,apad,atrim=end_sample=1553600[mix]",
    "-map",
    "[mix]",
    "-ar",
    "48000",
    "-c:a",
    "pcm_s24le",
    "/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-neptune/Assets/Audio/full-mix-v01.wav"
  ],
  "music": [
    {
      "path": "/Users/diplomat/ytvideos/channels/paper_detour/videos/050_great_stink_london/Source/Music/signal_to_noise_no_piano.mp3",
      "sha256": "8e20b496b0614053565d4f43c80f469c84abd2aefb3ba01e29dfa813f49b9594",
      "in_seconds": 72,
      "duration_seconds": 33,
      "gain_db": -22
    }
  ],
  "ebur128": {
    "voice-conform-v01.wav": "Integrated loudness:\n    I:         -24.0 LUFS\n    Threshold: -34.3 LUFS\n\n  Loudness range:\n    LRA:         2.0 LU\n    Threshold: -44.4 LUFS\n    LRA low:   -25.3 LUFS\n    LRA high:  -23.2 LUFS\n\n  True peak:\n    Peak:       -2.7 dBFS\n[out#0/null @ 0x7c1b00c6c0] video:0KiB audio:3034KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown\nsize=N/A time=00:00:32.36 bitrate=N/A speed= 378x elapsed=0:00:00.08",
    "full-mix-v01.wav": "Integrated loudness:\n    I:         -22.9 LUFS\n    Threshold: -33.3 LUFS\n\n  Loudness range:\n    LRA:         1.9 LU\n    Threshold: -43.3 LUFS\n    LRA low:   -24.1 LUFS\n    LRA high:  -22.2 LUFS\n\n  True peak:\n    Peak:       -4.7 dBFS\n[out#0/null @ 0x7547050180] video:0KiB audio:6069KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown\nsize=N/A time=00:00:32.36 bitrate=N/A speed= 211x elapsed=0:00:00.15"
  }
}
```

Subjective listening: UNVERIFIED.

# EN review audio v01

Authorized for user review MP4, 2026-11-09. Voice source `/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-atlantic-cable/Source/Voice/en_v01/voice_en.mp3` SHA-256 `b3188d2d2cbf875ba027f5824c17d37e08a59a45a95b8279316f1501397656fa`. Dry mono ElevenLabs recording, placed at zero; only one FFmpeg `atempo=1.10`, no cuts. Measured conformed voice 274.547521s; full stereo PCM 24-bit / 48 kHz mix 284.566667s, 8537 frames at 30 fps. Voice center with −2 dB gain in full mix.

Mix SHA-256 `fb57047c6a43ba4ce483fc2307eb1ccb22c05fc11bc5bb5cedbe1e054779796a`. Exact provider alignment compared character for character to script. End time of the final word omits punctuation duration (provider clock extends past MP3); for US, the last letter timing also slightly exceeds the measured clip, so the final word terminates at the physical clip end. FFmpeg tail `silencedetect` detected trailing quiet from raw 476.988 s through 477.120 s, supporting this endpoint. No shift applied to earlier words. All intervals finite and monotonic; final map `/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-atlantic-cable/Work/word-times-final-v01.json` SHA-256 `7c818e3133a67741e835131771cfcca9bd328c6694d8d7573b23b50a049d0c1c`.

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
    "/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-atlantic-cable/Source/Voice/en_v01/voice_en.mp3",
    "-af",
    "atempo=1.10",
    "-ar",
    "48000",
    "-c:a",
    "pcm_s24le",
    "/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-atlantic-cable/Assets/Audio/voice-conform-v01.wav"
  ],
  "mix": [
    "ffmpeg",
    "-nostdin",
    "-v",
    "error",
    "-n",
    "-i",
    "/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-atlantic-cable/Assets/Audio/voice-conform-v01.wav",
    "-ss",
    "4",
    "-t",
    "285",
    "-i",
    "/Users/diplomat/ytvideos/channels/paper_detour/videos/050_great_stink_london/Source/Music/signal_to_noise_no_piano.mp3",
    "-filter_complex",
    "[0:a]pan=stereo|FL=c0|FR=c0,volume=-2dB[vox];[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=-22dB[m1];[m1]afade=t=in:d=0.6,afade=t=out:st=282.266667:d=2.3[music];[vox][music]amix=inputs=2:normalize=0,apad,atrim=end_sample=13659200[mix]",
    "-map",
    "[mix]",
    "-ar",
    "48000",
    "-c:a",
    "pcm_s24le",
    "/Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-09-atlantic-cable/Assets/Audio/full-mix-v01.wav"
  ],
  "music": [
    {
      "path": "/Users/diplomat/ytvideos/channels/paper_detour/videos/050_great_stink_london/Source/Music/signal_to_noise_no_piano.mp3",
      "sha256": "8e20b496b0614053565d4f43c80f469c84abd2aefb3ba01e29dfa813f49b9594",
      "in_seconds": 4,
      "duration_seconds": 285,
      "gain_db": -22
    }
  ],
  "ebur128": {
    "voice-conform-v01.wav": "Integrated loudness:\n    I:         -24.4 LUFS\n    Threshold: -34.7 LUFS\n\n  Loudness range:\n    LRA:         1.9 LU\n    Threshold: -44.7 LUFS\n    LRA low:   -25.6 LUFS\n    LRA high:  -23.8 LUFS\n\n  True peak:\n    Peak:       -2.8 dBFS\n[out#0/null @ 0x7918c30180] video:0KiB audio:25739KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown\nsize=N/A time=00:04:34.54 bitrate=N/A speed= 345x elapsed=0:00:00.79",
    "full-mix-v01.wav": "Integrated loudness:\n    I:         -23.3 LUFS\n    Threshold: -33.7 LUFS\n\n  Loudness range:\n    LRA:         2.0 LU\n    Threshold: -43.7 LUFS\n    LRA low:   -24.6 LUFS\n    LRA high:  -22.6 LUFS\n\n  True peak:\n    Peak:       -4.8 dBFS\n[out#0/null @ 0x7a47050180] video:0KiB audio:53356KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown\nsize=N/A time=00:04:44.56 bitrate=N/A speed= 213x elapsed=0:00:01.33"
  }
}
```

Subjective listening: UNVERIFIED.

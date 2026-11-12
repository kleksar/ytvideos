# EN review audio v01

Authorized for user review MP4, 2026-11-09. Voice source `/Users/diplomat/ytvideos/channels/nuviko_history/research/us-history/Source/Voice/en_v01/voice_en.mp3` SHA-256 `964fb8b93c9b9a5e9b61bb0967c19bc9928cbf54ba19d9855a7ed1830ab1e79b`. Dry mono ElevenLabs recording, placed at zero; only one FFmpeg `atempo=1.10`, no cuts. Measured conformed voice 433.749625s; full stereo PCM 24-bit / 48 kHz mix 443.766667s, 13313 frames at 30 fps. Voice center with −2 dB gain in full mix.

Mix SHA-256 `526dc8cbfc4950ca2ddf37fc527ed00ceb215f57d9601442bc5ca4fd397d9f69`. Exact provider alignment compared character for character to script. End time of the final word omits punctuation duration (provider clock extends past MP3); for US, the last letter timing also slightly exceeds the measured clip, so the final word terminates at the physical clip end. FFmpeg tail `silencedetect` detected trailing quiet from raw 476.988 s through 477.120 s, supporting this endpoint. No shift applied to earlier words. All intervals finite and monotonic; final map `/Users/diplomat/ytvideos/channels/nuviko_history/research/us-history/Work/word-times-final-v01.json` SHA-256 `1950a00368b0baaa66a7a2879986dc37a97ab6f5770caf383c21b97a10f265d1`.

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
    "/Users/diplomat/ytvideos/channels/nuviko_history/research/us-history/Source/Voice/en_v01/voice_en.mp3",
    "-af",
    "atempo=1.10",
    "-ar",
    "48000",
    "-c:a",
    "pcm_s24le",
    "/Users/diplomat/ytvideos/channels/nuviko_history/research/us-history/Assets/Audio/voice-conform-v01.wav"
  ],
  "mix": [
    "ffmpeg",
    "-nostdin",
    "-v",
    "error",
    "-n",
    "-i",
    "/Users/diplomat/ytvideos/channels/nuviko_history/research/us-history/Assets/Audio/voice-conform-v01.wav",
    "-ss",
    "23",
    "-t",
    "221",
    "-i",
    "/Users/diplomat/ytvideos/channels/paper_detour/videos/050_great_stink_london/Source/Music/signal_to_noise_no_piano.mp3",
    "-ss",
    "12",
    "-t",
    "228",
    "-i",
    "/Users/diplomat/ytvideos/channels/nuviko_history/research/molasses-flood/Source/Music/Night_Vigil.mp3",
    "-filter_complex",
    "[0:a]pan=stereo|FL=c0|FR=c0,volume=-2dB[vox];[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=-23dB[m1];[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=-24dB[m2];[m1][m2]acrossfade=d=5:c1=tri:c2=tri[bed];[bed]afade=t=in:d=0.6,afade=t=out:st=441.466667:d=2.3[music];[vox][music]amix=inputs=2:normalize=0,apad,atrim=end_sample=21300800[mix]",
    "-map",
    "[mix]",
    "-ar",
    "48000",
    "-c:a",
    "pcm_s24le",
    "/Users/diplomat/ytvideos/channels/nuviko_history/research/us-history/Assets/Audio/full-mix-v01.wav"
  ],
  "music": [
    {
      "path": "/Users/diplomat/ytvideos/channels/paper_detour/videos/050_great_stink_london/Source/Music/signal_to_noise_no_piano.mp3",
      "sha256": "8e20b496b0614053565d4f43c80f469c84abd2aefb3ba01e29dfa813f49b9594",
      "in_seconds": 23,
      "duration_seconds": 221,
      "gain_db": -23
    },
    {
      "path": "/Users/diplomat/ytvideos/channels/nuviko_history/research/molasses-flood/Source/Music/Night_Vigil.mp3",
      "sha256": "315009fda5154a093570b9f49c1d98202ab5ba4906078713380d130710ada442",
      "in_seconds": 12,
      "duration_seconds": 228,
      "gain_db": -24
    }
  ],
  "ebur128": {
    "voice-conform-v01.wav": "Integrated loudness:\n    I:         -21.5 LUFS\n    Threshold: -31.8 LUFS\n\n  Loudness range:\n    LRA:         3.6 LU\n    Threshold: -41.8 LUFS\n    LRA low:   -23.6 LUFS\n    LRA high:  -20.0 LUFS\n\n  True peak:\n    Peak:       -1.0 dBFS\n[out#0/null @ 0x7b5500c6c0] video:0KiB audio:40664KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown\nsize=N/A time=00:07:13.74 bitrate=N/A speed= 372x elapsed=0:00:01.16",
    "full-mix-v01.wav": "Integrated loudness:\n    I:         -20.5 LUFS\n    Threshold: -30.8 LUFS\n\n  Loudness range:\n    LRA:         3.6 LU\n    Threshold: -40.8 LUFS\n    LRA low:   -22.6 LUFS\n    LRA high:  -19.0 LUFS\n\n  True peak:\n    Peak:       -3.0 dBFS\n[out#0/null @ 0x78b500c6c0] video:0KiB audio:83206KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown\nsize=N/A time=00:07:23.76 bitrate=N/A speed= 202x elapsed=0:00:02.20"
  }
}
```

Subjective listening: UNVERIFIED.

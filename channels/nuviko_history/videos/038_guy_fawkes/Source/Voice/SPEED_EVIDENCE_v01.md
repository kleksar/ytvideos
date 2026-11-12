# Nuviko narration speed evidence v01

- Episode: `038_guy_fawkes`, English production narration v01.
- Input: `voice_en.mp3`; SHA-256 `d05eab3dba4edf1cb4abd4aef96772a3aaaf9e4680c6b08054c752fa63369c3b`.
- Source properties observed with ffprobe: MP3, mono, 44,100 Hz, 128,000 bit/s, 234.160 s.
- Operation: FFmpeg `atempo=1.10` once; output encoded as PCM signed 16-bit WAV, mono, 44,100 Hz.
- Output: `voice_en_speed110_v01.wav`; SHA-256 `04367fb1f184cdb234db0386f870683521d9175259803d768a5179ca559a21d4`.
- Output duration observed with ffprobe: 212.879660 s. Expected duration by rate ratio: 234.160 / 1.10 = 212.872727 s; difference 0.006933 s.
- The generated speech source was not auditioned here. Timing is generated from the TTS character alignment and mapped through the 1.10× speed ratio; audible synchronization remains unverified pending QA.

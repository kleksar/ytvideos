# Audio timing and speed record

The accepted narration is Source/NARRATION_EN.md (SHA-256 20363f3e0180169e697e37310a02045c38c7455f76cb8ce7ba04f5f0de12d266). ElevenLabs generated Work/production-v02/Source/Voice/voice_en.mp3 directly at 1.10x with voice ktkP7Nsj67dw2zcplQYt, model eleven_v4, MP3 mono 44.1 kHz/128 kbps. The request receipt is Work/production-v02/Source/Voice/voice_en.request.json. No second speed change, trimming or offset was applied.

- Speech source MP3 SHA-256: 38bfb84125e764dcdddbd8a20f3c1226c496af0abf0e5bee5552db15f722a356; duration 566.560 s.
- Full timeline mix: Work/production-v02/Source/Voice/voice_en_fullmix.wav, SHA-256 36a021c6609f605fc2fe0bf6b25bbf838d6901b29ed70df5b5d14289ba65b53b, PCM mono 44.1 kHz, duration 576.566667 s. It preserves the MP3 speech by decoding once to PCM and appending 10.006667 s of digital silence for the two end-screen cards.
- WhisperX forced alignment: Work/production-v02/Source/Voice/voice_en.whisperx_alignment.json; 1,458 words. Final spoken word found. is estimated at 565.94–566.24 s, before the speech MP3 ends at 566.56 s. Provider alignment placed its final punctuation beyond the file; the independent WhisperX estimate replaces that draft timing.
- Word map: Work/production-v02/Edit/Captions/word_times.json; bound to full timeline mix and exact transcript. Speech-to-frame audible review: UNVERIFIED.
- Mix contents: mono narration followed by digital silence; no music or sound effects.

# TTS receipt — Paper Detour 049

- Authorized scope: user's request to produce the accepted story as a complete video/MP4 on 2026-11-05; root §5 authorizes voice creation from the accepted script.
- Exact transcript: `Source/Script/narration_en_v26.md`, 431 words, 2,701 characters; SHA-256 `52c534de62209629257213f49a5c6c3301010d2f5bae1c87426a9bbc66ff6956`.
- Canonical voice: Lawrence `ktkP7Nsj67dw2zcplQYt`; model `eleven_v4`; requested format `mp3_44100_128`; stability `1.0`; similarity `0.0`; synthesis speed unset.
- Result: account/key slot 1 reported insufficient credits; slot 2 completed generation. No retry was issued after success. Console confirmed `voice_en.mp3`, voice ID, model, format, and completion.
- Source: `Source/Voice/en_v26/voice_en.mp3`; duration 164.400 s; MP3 44,100 Hz mono, 128 kbps; SHA-256 `6c1432020315f5eafd607dd15c4c7aa5b75d90406cc3cd80e8ddeb5ab140247c`.
- Provider alignment: `Source/Voice/en_v26/voice_en.alignment.json`, SHA-256 `5758646f98e7ccf434068e7eace8ad7c297fa44ec15488420879bd00b8325062`.
- The project profile's one and only `atempo=1.10` operation produced PCM S16LE 44,100 Hz mono at `Source/Audio/narration_en_v26_110.wav`, duration 149.459206 s; SHA-256 `c4f81d49216ffb1c8767180ecef5f9199b3901c478946b3c582e105a4a38cf2a`.
- `word_times_provider_source_v01.json` was made by the channel word-timing adapter against the approved transcript and exact provider alignment. `word_times_en_v26_110.json` scales word timings once by 1/1.10; final lexical word ends at 149.3091 s. The provider's trailing punctuation alignment exceeds the file boundary; it is excluded from spoken-word timing. No listening review has been performed; timing remains a machine estimate pending alignment review.
- Evidence files: `Source/Voice/en_v26/voice_en.request.json`, `Source/Voice/en_v26/voice_en.alignment.json`, `Edit/Audio/speed_evidence_v01.md`, and the two time maps above.

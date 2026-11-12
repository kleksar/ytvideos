# Alignment review v02 — Paper Detour 042

- Exact recording: `voice_en_1.10x.wav`; SHA-256 `13191bf664a7a15c10c43aadc5b4d1a984bf95df86273dfc170ff2ab297ca836`; duration 50.766077 s.
- Transcript: `narration_en_v02.txt`, 142 words; exact token count matched by ElevenLabs character alignment converter and WhisperX forced aligner (142/142).
- Provider map: `word_map_provider_1.10x_v02.json`, with one 1/1.10 speed-time conversion preserved in `word_map_provider_mapped_1.10x_v02.json`.
- Independent forced alignment: `word_map_forced_whisperx_1.10x_v02.json`; audio-hash bound; status REVIEW_REQUIRED.
- Montage map: `word_times_for_montage_v02.json` uses forced-aligner boundaries in the final WAV's seconds.
- Provider minus forced timing: median onset -0.012s; median end -0.024s; largest absolute onset difference 0.238s; largest absolute end difference 0.093s.
- No human listening or speech-to-frame inspection was performed. These machine maps do not establish audible sync, pronunciation quality, or perceived word onset.

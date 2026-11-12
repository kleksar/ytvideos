# Скорость и звук: черновик v01

ElevenLabs source: `../Source/Voice/voice_en.mp3`, SHA-256 `423f3ead3931ddb74fcb7d63311d9f06b0a01610f1913dce77604c9c032f4115`; native generation speed unset. FFmpeg `atempo=1.10` applied exactly once to `voice_en_110_v01.wav`, SHA-256 `742603315e4459e8e985184855a6f3b07d5dd46375e5476895fa336f41d0e550`. Mixer does not change speed: it places speech 0.3 s after start, adds selected music and a tail. `../Work/audio-v01/mix_32s_draft.wav` SHA-256 `ebcbbdda4f4ff20fa8f69f7a5348385f39abe37bc92ef0d955c9fb37208b9ab9`; word map `source / 1.10 + 0.3`. Mix remains UNVERIFIED pending audible review; not a final sound acceptance.

Final production mix `../Work/audio-v01/mix_33s_v01.wav`, SHA-256 `e499943d42efc2e29a6344994a85dfd495631de3116380275714c38bf975a7ae`; same single atempo and 0.3 s delay, 33.1 s total. Subjective listening UNVERIFIED.

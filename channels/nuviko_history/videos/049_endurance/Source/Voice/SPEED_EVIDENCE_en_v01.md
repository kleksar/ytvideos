# Endurance English voice speed evidence v01

- Source narration: `Source/Voice/voice_en_text_v01.txt` (8,506 UTF-8 characters; SHA-256 `77674fd879312fc574139b0f4689d9cb015f200b248d36915d59eae39b1b41d3`).
- Generated voice file: `Source/Voice/voice_en_v01/voice_en.mp3` (SHA-256 `b972311d983172c43d6a48b568824c3ef94650b8e6bfe4868997da7258893ce3`).
- ElevenLabs request receipt: `Source/Voice/voice_en_v01/voice_en.request.json`; voice ID `5vsgZsi667xMyGinrNIM`, model `eleven_v4`, requested generation speed `1.10`, MP3 44.1 kHz mono. Request status is `success`.
- The voice API generated the only speech track at 1.10×. No second speed operation has been applied.
- FFprobe reports MP3, 44.1 kHz, mono, container duration 559.840 s. Provider character alignment ends the final spoken word at 559.920 s and punctuation at 560.160 s; the last MP3 packet reports 767 discarded padding samples. Decoded waveform RMS is below 0.0001 from 559.79 s to end (measured, not auditioned). The word map bounds the final token at 559.840 s with that adjustment recorded; audible ending and alignment remain UNVERIFIED.
- No independent listening check has been performed. The audio file is the production speech source pending the normal synchronized-video review.

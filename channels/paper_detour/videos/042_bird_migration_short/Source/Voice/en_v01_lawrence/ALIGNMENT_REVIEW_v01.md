# Alignment review v01 — Paper Detour 042

- Exact recording: `voice_en_1.10x.wav`; SHA-256 `76229d806087673875fd138091f21fe11436978fc06d41c92284cedc445fd326`; duration 51.859410 s.
- Transcript: accepted `narration_en_v01.txt`, 143 words; exact token count matched by ElevenLabs character-map converter and WhisperX forced-aligner.
- Provider word map: `word_map_provider_1.10x_v01.json`; source character alignment was scaled once from original provider time by 1/1.10.
- Independent forced alignment: `word_map_forced_whisperx_1.10x_v01.json`; audio-hash bound, WhisperX estimate against the exact sped WAV; status from helper remains REVIEW_REQUIRED.
- Montage input map: `word_times_for_montage_v01.json`; copies WhisperX word boundaries in the final WAV's seconds. It is a draft, not audibly accepted.
- Provider vs forced timing comparison over 143 same-token pairs: median onset difference +21.6 ms; median end difference +31.5 ms; mean WhisperX score 0.837. One boundary flag over the stated diagnostic threshold: word #27 `returned` forced start 8.563s vs provider 8.727s (difference -164 ms); ends differ -2 ms.
- No human listening or speech-to-frame inspection was performed. The maps and model scores do not establish audible sync, pronunciation quality or perceived word onset. The final word ends at 51.639s; timeline end is 51.866667 s.
- Use as provisional for a review draft only; a reviewer should inspect the returned word boundary and listening limitation before release.

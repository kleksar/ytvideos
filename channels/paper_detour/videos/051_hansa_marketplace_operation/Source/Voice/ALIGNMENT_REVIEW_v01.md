# Voice and alignment record v01

- Audio: `voice_en.mp3`; SHA-256 `84e95cde9f4dc86c6dec491a9e12566470a9c34abc5fb716e01478bdcb4fdf8b`.
- TTS receipt: `voice_en.request.json`; ElevenLabs helper, Lawrence `ktkP7Nsj67dw2zcplQYt`, `eleven_v4`, requested speed 1.10× once; generated MP3, 44.1 kHz, mono, 128 kbps.
- Measured duration: 34.080 s. TTS character alignment covers 506 characters and ends at 34.080 s, including punctuation/tail. The final spoken word `worked` ends at 33.68 s in provider timing.
- Provider word map: `word_map_provider_v01.json`, 82 entries; it splits `50,000` and `10,000` into two entries each.
- Independent forced-alignment draft: `word_map_whisperx_v01.json`, 80 entries, exact audio hash above and accepted transcript hash; it keeps each number as one token and aligns the full 80-token transcript. Raw model result: `alignment_whisperx_raw_v01.json`.

## Comparison and current choice

WhisperX is the better structural draft for the accepted narration because its 80 entries match the narration's whitespace-token count; the provider map produces 82 entries by splitting the two comma-formatted quantities. The two alignments are broadly close in the beginning and middle but differ locally: e.g. provider begins `After` at 0.000 s while WhisperX places it at 0.140 s; near `controlled`, provider start is 15.560 s and WhisperX is 15.389 s. Do not apply one global offset. Retain both maps for review; use WhisperX as the provisional map for cue work, subject to audible/manual reconciliation.

The maps differ in tokenization and boundary estimates, so they do not establish audible synchronization. No listening review has been completed. The production still needs onset/phrase checks near the opening, middle and ending against this exact recording. Do not mark audible sync PASS or describe this timing as heard/accepted until those checks are performed.

The SRT and burned-in subtitle timings will bind to the final mix. If the final mix preserves this voice byte-for-byte and introduces no leading offset or speech edit, its word boundaries can be conformed without resynthesis; otherwise regenerate/conform the timing evidence against that exact retained voice.

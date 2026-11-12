# Voice generation log — accepted English v04

- Input: `Source/Script/narration_en_v04.md` (user approved; spoken text requested verbatim).
- Voice: Lawrence `ktkP7Nsj67dw2zcplQYt`.
- Model/format: `eleven_v4`, `mp3_44100_128`; stability 1.0, similarity 0.0; speed omitted (provider default).
- Provider returned audio and character alignment. CLI returned exit 1 with a save error after the request; no retry was made. The files were present on disk and inspected afterward.
- `voice_en.mp3`: 5,316,901 bytes; SHA-256 `b73ba08066497817115d40395e4fe709a52511e53f15d1bcff91668fe5730f4b`; ffprobe: MP3, 44,100 Hz, mono, 128,000 bit/s, 332.24 s.
- `voice_en.alignment.json`: 409,618 bytes; valid JSON; character alignment and normalized alignment present; 5,281 character entries; last aligned character ends at 332.4 s.
- This records file and machine-readable alignment checks only; it is not a listening or pronunciation QA result.

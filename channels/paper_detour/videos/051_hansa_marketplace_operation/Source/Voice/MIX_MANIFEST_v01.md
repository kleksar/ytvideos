# Narration mix manifest v01

- Mix scope: narration only; the accepted script does not specify music or sound effects.
- Full retained mix: `voice_en.mp3`, SHA-256 `84e95cde9f4dc86c6dec491a9e12566470a9c34abc5fb716e01478bdcb4fdf8b`.
- Source: ElevenLabs helper; Lawrence (`ktkP7Nsj67dw2zcplQYt`), `eleven_v4`, speed requested 1.10× once as shown by `voice_en.request.json`. The supplied source is already at that rate; do not apply a second speed change.
- Format: MP3, mono, 44.1 kHz, 128 kbps; measured duration 34.080 s. No trims, fades, leading offset, music or SFX are applied; use the byte-identical accepted narration for picture export.
- Timing: WhisperX forced alignment, 80 transcript-token entries. Source-hash matched and structurally aligned, but estimated only; no one has completed a listening-based onset/sync pass. `ALIGNMENT_REVIEW_v01.md` records the unresolved differences from provider timings.
- Output contract: renderer converts mono MP3 to AAC at 192 kbps without speed/offset changes. Export timeline is 1,023 frames at 30 fps (34.100 s), giving the final frame grid a 20 ms tail beyond the source; narration itself is not extended or retimed.

# Voice-only mix — EN v03, 1.10x

- Source: accepted mono PCM master v02 (`voiceonly_master_en_v02.wav`), 44.1 kHz, 24-bit, 52.88 s.
- User direction: apply 1.10x to voice only; do not accelerate picture playback.
- Treatment: FFmpeg `atempo=1.1`; no word/order edits, loudness normalization, music, or SFX added. Output is mono PCM S24LE, 44.1 kHz, measured duration 48.078277 s.
- Subtitle timing: derived from alignment for the exact source voice; every token start/end divided by 1.1 in `Source/Subtitles/word_times_en_v03_1p1.json`.
- Runtime handling was resolved by the user: the montage was shortened to the final voice duration, yielding 48.1 s at 30 fps.
- The user fully watched exact v08 with sound and accepted its sync; no independent audio listening by Codex was performed. The final public video and read-back are recorded in `Packaging/Metadata/YOUTUBE_RELEASE_20261103.md`. The local voice asset was retired after verified Public.

# Export QA — Paper Detour 028 English v04

2026-11-02. Current local delivery with stronger, full-source-alpha grain, following the user's report that v03 grain was imperceptible.

- Project `25A8FF9A`, timeline `8565580B`; snapshot before change `0FB8B4BF`; snapshot after `C9FABBC0`.
- Replaced only grain media on clip `29CFE306`. Stack remains V3 accents → V2 grain → V1 scenes → A1 dialogue. Timeline interval [0,1066); cues, scenes, dialogue and their keyframes unchanged.
- Overlay `Edit/Overlays/028_film_grain_full_length_v02_540x960_30fps_full_alpha.mov`: same loop and 6-frame overlaps as v03, but restored to 100% source alpha (rather than source alpha ×0.4). Item opacity remains 100%.
- Exported picture from Palmier, then muxed the accepted MP3 as AAC-LC mono 192 kb/s under existing authorization; H.264 copied without re-encoding.
- Delivery `028_taj_mahal_en_short_1080x1920_30fps_v04_full_alpha_grain_voice192_20261102.mp4`, 45,019,853 bytes, SHA-256 `dfb028861702bba06157d9bc02fcaf55a289c21d986460e07b8bbbc4f9d9b8a0`.
- H.264 High 1080×1920, 30fps, 1066 frames; AAC-LC mono 44.1kHz 192112bps. Full ffmpeg decode with -xerror passed.
- Contact sheet `QA_Grain_v04_contact.png` samples representative scenes/cues. Need confirm subjective grain strength by continuous 1× playback; do not describe perceptual acceptance as complete until checked. Independent reviewer not used.
- Supersedes v03. No upload or publication.

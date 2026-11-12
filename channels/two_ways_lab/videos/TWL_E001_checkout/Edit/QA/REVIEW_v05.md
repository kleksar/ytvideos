# TWL_E001 review v05

MP4 SHA-256: `9e65624cc14e58b680b0c602741fdeeb4e877c5cdecde7ab2d8de14e578299a7`. Review draft; no user approval or upload.

- Existing v01 narration was processed using FFmpeg atempo=1.1; music remains at its original tempo, SFX conformed to speech, subtitles retain their style and were retimed. Original synthesis speed 0.91; original playback was 1.0. Mix evidence: ../../Source/Audio/v02/mix-evidence.md.
- 100/100 words received timestamps in offline WhisperX forced alignment of the exact v02 voice; mean absolute difference against scaled model start timings 0.068 s, maximum 0.132 s. This is automated alignment, not a subjective listening check. Separate SRT timings were scaled from v03 and need human playback review.
- Full FFmpeg decode succeeded; ffprobe data is in ffprobe_v05.json. Inspected nine representative rendered frames at 270x480 in v05_sheet.jpg. The separately generated labels have the intended spelling; no sampled caption overlap. The two conditions use separate labels to improve legibility. Not every frame or actual phone playback was checked.
- Whole-scene images are text-free generated edits; lettering is independent transparent generated image assets with 4% scale and 4-degree rotation amplitudes. See ../timeline_v05.json and ../lettering_manifest_v05.json.
- Audio quality, final seam and independent review remain unverified.

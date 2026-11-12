# Paper Detour 009 — interim upload hold (superseded)

**Historical status:** this recorded the initial hold before the user explicitly accepted the below-target AAC bitrate and requested upload. It has been superseded by [YOUTUBE_UPLOAD_PRIVATE_v04_20261101.md](YOUTUBE_UPLOAD_PRIVATE_v04_20261101.md), which records the completed Private upload and current readbacks.

## Requested release

- Channel: Paper Detour (`UCMVfdfaNxV3ZkI3_J3Eejzw`)
- Requested visibility: Private
- Timeline: `PD009_story_titles_retimed_v04_20261101` (`E2ABDF4C`), project `9A0EE170`
- Accepted title, description and hashtags: [YOUTUBE_METADATA_v01_20261101.md](YOUTUBE_METADATA_v01_20261101.md)
- Accepted thumbnail JPEG: [pd009_cat_on_monument_v02_20261101.jpg](../Thumbnails/Upload/pd009_cat_on_monument_v02_20261101.jpg)

## Render inspection

- File: [009_knorozov_asya_en_short_1080x1920_30fps_fullmix_v04_20261101.mp4](../../Deliverables/009_knorozov_asya_en_short_1080x1920_30fps_fullmix_v04_20261101.mp4)
- SHA-256: `c3f9885dd7b4708c29f0cb0d8b8dd3bfa3266ec92d193151c882ee29d74e6a36`
- Video: H.264, 1080×1920, 30 fps, 34.000 s
- Audio: AAC stereo, 44.1 kHz, 110,214 bit/s
- File size: 45,405,216 bytes
- `ffmpeg -v error -xerror` full decode completed with exit code 0. A contact sheet sampled every 3 seconds was reviewed. Full subjective 1× playback with audio and Shorts UI safe-margin review remain unverified.

## Why upload stopped

The channel delivery check targets at least 256 kbit/s for stereo AAC. The Palmier export sheet exposes no audio bitrate control, and this render measures 110,214 bit/s. Increasing the bitrate of this already compressed AAC would not restore the missing quality. Rebuilding/rendering the mix from source tracks would create new audio, which has not been separately authorized. The file was therefore not sent to YouTube.

No YouTube upload, thumbnail, metadata, playlist, visibility or schedule change was made. No video ID exists for this attempt. The render and accepted packaging remain local.

To continue, provide a render/export path that produces stereo AAC at or above 256 kbit/s, or explicitly authorize a new mix render from the existing source tracks.

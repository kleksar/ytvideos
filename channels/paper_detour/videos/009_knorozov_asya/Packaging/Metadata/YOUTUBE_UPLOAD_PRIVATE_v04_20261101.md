# Paper Detour 009 — private YouTube upload receipt

**Status:** uploaded and verified Private on 2026-11-01. The user explicitly accepted the 110 kbit/s AAC render and instructed us to upload it as-is. No new audio was rendered.

## Video

- Channel: Paper Detour (`UCMVfdfaNxV3ZkI3_J3Eejzw`)
- Video ID: `orQiLIvOL-8`
- Link: https://www.youtube.com/watch?v=orQiLIvOL-8 (Private; channel-owner access required)
- Source MP4: [009_knorozov_asya_en_short_1080x1920_30fps_fullmix_v04_20261101.mp4](../../Deliverables/009_knorozov_asya_en_short_1080x1920_30fps_fullmix_v04_20261101.mp4)
- SHA-256: `c3f9885dd7b4708c29f0cb0d8b8dd3bfa3266ec92d193151c882ee29d74e6a36`
- Timeline: `PD009_story_titles_retimed_v04_20261101` (`E2ABDF4C`), project `9A0EE170`
- YouTube processing: `processed`; processing status `succeeded`; failure and rejection reasons `null`

## Saved metadata and access

- Title: **Why Is There a Cat on a Monument to a Maya Scholar?**
- Description saved with `#YuriKnorozov #MayaScript #AsyaTheCat` at the end.
- Category: Education (`27`); title/description language `en`; audio language `en`.
- Audience readback: not made for kids (`false`).
- Separate YouTube tags: none supplied; API readback returned `null`.
- API readback confirmed the exact title and description, channel ID, and `privacyStatus=private`.
- The upload request included `contains_synthetic_media=false`; the subsequent API readback omitted `containsSyntheticMedia` (`null`), so that field is not claimed as independently verified.
- No playlist, schedule, or external SRT was requested or added.

## Thumbnail

- Approved image: [pd009_cat_on_monument_v02_20261101.jpg](../Thumbnails/Upload/pd009_cat_on_monument_v02_20261101.jpg), phrase “SHE CAME LATER”.
- `thumbnails.set` via API returned accepted and URL readback `matched`, but Studio initially continued to display a frame from the Short.
- YouTube Help currently directs creators to add custom Shorts thumbnails in Studio on a computer and notes that changes can take time to appear: [Add custom thumbnails on YouTube](https://support.google.com/youtube/answer/72431?hl=en).
- The same approved JPEG was then selected through Studio's thumbnail uploader and saved. After reloading, Studio still showed the approved cover, and access remained Restricted/Private.

## Render and remaining review

- Video: H.264, 1080×1920, 30 fps, 34.000 s. Full technical decode succeeded.
- Audio: AAC stereo, 44.1 kHz, 110,214 bit/s. The user explicitly accepted the below-target bitrate for this upload.
- Full subjective 1× playback with audio and Shorts UI safe-margin review were not completed; contact-sheet samples at 3-second intervals were visually reviewed.
- The uploaded video remains Private; it was not scheduled or made public.

## Operations

- New video uploaded using the project YouTube API adapter with a unique state file at `/Users/diplomat/.local/share/story-youtube/paper-detour/pd009_v04_20261101_private_upload.json`.
- API status readback verified channel ownership, Private visibility, and completed processing.
- Thumbnail was saved in Studio because the API result did not update the visible Shorts thumbnail. Studio confirmed “Changes saved”; a reload retained the approved cover and Private setting.

> Historical pre-upload record. Current saved YouTube state: [release receipt](YOUTUBE_UPLOAD_20261102.md) and [exact current metadata](YOUTUBE_METADATA_CURRENT_20261102.json).

# Paper Detour 028 — pre-upload review, 2026-11-02

Status: local technical and packaging checks completed, with the open checks below. No upload, playlist mutation, scheduling or publication performed. User explicitly accepted v10 fine grain at 25%.

## Current delivery

[Final MP4](../../Deliverables/028_taj_mahal_en_short_1080x1920_30fps_v10_fine_grain25_voice192_20261102.mp4): 35.533333 s, 1066 frames, 1080×1920, 30 fps, H.264 High, AAC-LC mono 44.1 kHz at measured 192112 bps. Full decode and frame count previously passed. File hash is recorded in [export QA](../../Storyboard/QA_Export_v10.md) and the preparation manifest.

Actual QuickTime playback was set to Normal and started; the beginning, punishment scene and final question were observed. This was sampled visual observation, not continuous subjective review. A [36-image contact sheet](../../Storyboard/QA_v10_1s_contact_sheet_20261102.jpg) covering 0–35 s was inspected: all eight scenes and seven phrase accents were present, with no empty sampled frames. This does not prove every intervening frame or audible sync. Fine texture remains visible in actual full-size v10 samples; user acceptance supplies the appearance approval. Scene motion and cue timing were already preserved in the v09→v10 timeline comparison.

Final AAC technical measurement: −24.1 LUFS integrated, 1.9 LU loudness range, −4.8 dBFS true peak; no clipping indicated. No normalization or new audio was rendered. The accepted source MP3 and final AAC were decoded to memory and compared without time shifting: correlation 0.99994895; active signal above −50 dB starts at 0.037778 s and ends at 35.323311 s in both. Source duration 35.52 s; AAC decode padding extends its stream slightly. [Measurement](../../Storyboard/AUDIO_METRICS_v10_20261102.txt), [comparison](../../Storyboard/AUDIO_SOURCE_COMPARISON_v10_20261102.json). These results do not establish pronunciation, naturalness or subjective listening quality.

## Existing packaging retained

Title: **The Architect Who Was Too Good at His Job** (41 characters).

Cover: **PRAISED. THEN PUNISHED.** [Upload JPEG](../Thumbnails/taj_mahal_architect_thumbnail_v01_praised_then_punished_20261101_upload.jpg), 941×1672, 647697 bytes. PNG/JPEG decode and saved JPEG hash checked. Full original reviewed earlier; the actual centered 2:3 crop (941×1412, y=130) was rechecked at 320×480 in this pass: complete lettering, central faces, empty sleeves and Taj Mahal remain visible. [Phone preview](../../Storyboard/QA_cover_phone_20261102.png). This is a local crop test, not the platform card.

The existing description and three hashtags remain in [metadata draft](YOUTUBE_METADATA_DRAFT_20261101.md). [Extra High consistency consultation](../../.agents/consultations/20261102-packaging-consistency-check.md) was read and checked against the accepted narration. Its initial objection to PRAISED was corrected using the actual narration line about the king praising the work; final response found no new content promise. No historical verification is implied.

Read-only YouTube API confirmed Paper Detour `UCMVfdfaNxV3ZkI3_J3Eejzw` and its public playlist **Legends & Personal Stories** `PLa2eDoWjSKkA`, currently three items. [Dated API receipt](YOUTUBE_READ_ONLY_PREFLIGHT_20261102.json). Existing recommendation retained; the preparation plan preserves current members/order and proposes appending 028 only after upload authorization. Manual sorting was recorded in the channel registry previously, not rechecked in this pass. Playlist access does not authorize public video access.

## Open checks

- **Subjective listening and continuous audiovisual review at 1× remain unverified.** The available computer-use tool exposes pictures and controls, not system audio. No independent reviewer was used.
- Exact title/cover wording is a local candidate; no new user acceptance of that pair is claimed.
- Actual Shorts card, thumbnail application and processing can be verified only after an authorized upload draft. No draft exists from this task.
- Required audience/synthetic-content fields must use applicable channel policy and actual material when uploading. No declaration values were invented.

[Preparation manifest](UPLOAD_PREPARATION_20261102.json) contains exact file paths, hashes, English fields and the proposal-only playlist handoff. It is an internal manifest, not an executable YouTube API request. An authorized new upload starts Private under project policy; publication/scheduling remains separate.

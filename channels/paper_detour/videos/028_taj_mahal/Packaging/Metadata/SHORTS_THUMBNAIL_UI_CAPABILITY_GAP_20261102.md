# Shorts-specific thumbnail surface

API-first completed: thumbnails.set accepted the existing portrait JPEG; videos.list reports hasCustomThumbnail=true; actual returned maxres image was opened in Chrome and visually matched the intended PRAISED. THEN PUNISHED. image. This verifies the standard API thumbnail image, not every Shorts surface.

After processing succeeded and Studio reloads, Studio preview and the actual Shorts start screen still referenced automatic sd2/mq2 frames. No blind repeat of thumbnails.set was performed.

Current official Help https://support.google.com/youtube/answer/72431?hl=en checked 2026-11-02 explicitly says custom Shorts thumbnails are currently only available to add in YouTube Studio on a computer and gives a separate Shorts upload flow. The current API thumbnails.set schema exposes videoId and ordinary thumbnail bytes, no Shorts-specific selection field. This is the capability gap for applying/verifying the separate Shorts thumbnail selection; Studio is used only for that operation. No new cover/scene or new video upload is authorized by this fallback.

Existing destination video fvRm9Vxwagk, channel UCMVfdfaNxV3ZkI3_J3Eejzw, Private. Studio selected channel verified through its exact home URL. Preserve title/description/languages/tags/playlist/privacy. Existing JPEG: ../Thumbnails/taj_mahal_architect_thumbnail_v01_praised_then_punished_20261101_upload.jpg.

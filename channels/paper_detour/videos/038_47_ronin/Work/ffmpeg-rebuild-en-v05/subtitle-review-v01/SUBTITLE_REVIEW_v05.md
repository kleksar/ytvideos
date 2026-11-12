# Paper 038 — subtitle review evidence for v05

- Media: `new_channel/videos/038_47_ronin/Deliverables/47_ronin_en_v05.mp4`
- Media SHA-256: `a1e897b48b87d000a7dcccff9d376b147ec559c87e633cfcc1d2132b7199512c`
- Reviewer: coordinator/renderer; not independent of the edit.
- Subtitle contract fingerprint: `377b54c9e7da13463e386d306272b51c53da2e9ab45d8033577fdc5fdc6b6f0e`.

## Semantic grouping — checked

Read all 418 English caption groups from `scratch/prepare-subtitles-v09/caption_groups.json` against the exact EN v09 transcript. The exact transcript is preserved in order; no missing or repeated words were found. The 54 generated boundary warnings were checked in their surrounding phrases. The selected breaks remain readable as sequential short caption phrases; the explicit reviewed exceptions are preserved in montage v03. This is the author/coordinator's review, not an independent review.

## Visual placement — checked at stated scope

- Scanned all 1,669 generated caption-state PNG alpha bounds. The widest rasterized caption was 1,295 px, within the 1,344 px Paper width limit on the 2,560 px canvas.
- Inspected decoded v05 frames at 8.0, 98.0, 339.0, 490.5 and 556.0 seconds. Captions are centered at the profile baseline and remain inside the frame; the image contains no additional burned-in text layer. The 98-second caption sits over the scroll pictured in that shot; this remains visible and was not changed after the user's acceptance.
- Sample-frame scope does not claim inspection of every frame or independent full-film visual QA.

## Audible synchronization — checked at stated scope

The user reviewed and accepted this exact v05 MP4 and said the subtitles fit. A fresh second WhisperX forced-alignment run against the exact retained 1.10× voice matched all 1,668 token strings and every start/end time in the bound final-time map exactly (0 ms maximum difference). The final MP4 audio and video streams both start at 0.000 s. This supports the subtitle timing check; it is not a claim of coordinator continuous listening, pronunciation review, or independent QA. The alignment tool itself reports `REVIEW_REQUIRED`, so this evidence is interpreted together with the user's review of the exact final MP4, not as standalone proof.

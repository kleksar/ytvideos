# IQ Gallery — 4-pair typography reset samples

**Status:** review samples only. These are not a new approved cut or a replacement for the v19 project.

Each entry has three distinct files: a full-scene paper image (`*_scene.png`), a full-canvas transparent paper-title layer (`*_title.png`), and a review composite (`*_preview.png`). The contact sheet is `contact_4_pairs.jpg`.

## Draft pairs

| Person | Draft title |
|---|---|
| John F. Kennedy | JOHN F. / KENNEDY / IQ 119 |
| Garry Kasparov | GARRY / KASPAROV / IQ 123 |
| Kanye West | KANYE / WEST / IQ 133 |
| Marilyn vos Savant | MARILYN / VOS SAVANT / IQ 228 |

These IQ figures are inherited from the previous working list and remain unverified estimates. They are included here only to review the visual pairing.

## Visual references and constraints

- Studied the approved Paper Detour 004 reference `channels/paper_detour/videos/004_last_video/Storyboard/user_reference_parallax_20261101.png` and the earlier accepted paper-title assets under `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/prepared_full_scenes_v17/` and `prepared_labels_v13/`.
- Scene images are separate from text. All four use a handmade layered paper-diorama look, chest-up framing, similar head scale and gaze direction; the lower center is open but remains part of the setting rather than a flat title plate.
- Titles reuse the established textured paper-glyph assets from `prepared_labels_v13/`, preserving their cream face, warm cut edge, volume and soft shadow. No system-font typesetting is used.
- A single title layout is used for every pair: transparent 1080×1920 canvas, optical center x=540, row centers y=1304/1426/1560, name-row visible heights 96px and IQ-row height 108px. Rows are individually cropped and centered to keep the same vertical rhythm.

## Creative consultation log

On 2026-11-01, the coordinator asked one narrow title-system question in the Paper Detour project chat using Google Chrome. The visible model label immediately before sending was **Extra High**. The response recommended a fixed title grid, consistent per-row sizing, cream handmade paper with a warm dimensional edge and soft shadow, irregular individual glyph contours, and the existing JFK / Paper Detour 001 title assets as shape and material references. The grid values above record the chosen implementation. Chat: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae74b79-d8d0-83eb-8e7f-7d2ab9ea2de0

Rebuild the PNGs with:

```sh
python3 channels/paper_detour/videos/003_iq_gallery/Edit/typography_reset_v20_samples/build_samples.py
```

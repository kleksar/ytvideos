# IQ Gallery v21 — four scene/title pairs

**Status:** review sample, pending user approval. The user accepted the v20 card format and asked to make the lower foreground meaningful and the lettering closer to Paper Detour's actual handmade type.

## Review sheet

`contact_4_pairs.jpg` shows all four pairs at once. Each pair also has a full-size 1080×1920 `*_scene.png`, a separate transparent 1080×1920 `*_title.png`, and a flattened `*_preview.png` for visual review.

## Scene changes

- Kennedy and Kasparov are carried over unchanged from the v20 approved scene sample: the White House desk and pen; the chess table, hand, and close chess pieces.
- Kanye now sits in a recording studio behind a continuous wooden desk, with the mixer at left and keyboard at right. The title-safe center remains clear.
- Marilyn sits in a library reading room behind a wooden table. Closed books frame the left; a completed generic shape puzzle sits on an open page at far right, away from the title. It contains no text or purported historical material.
- The lower field is part of each setting. There are no isolated solid-color slabs.

## Type treatment

The title remains a separate PNG. Name rows and digits reuse the IQ Gallery v13 cut-paper assets; the shared `IQ` glyph is newly generated against the accepted Paper Detour 001 `A_MESSAGE.png` / `MATCH.png` and existing IQ digit references. This keeps the block in the channel's thick, rounded handmade paper family without system-font typesetting. All four cards share cream faces, warm paper edges, soft shadows, row centers x=540 and y=1304/1426/1560, and visible row heights 96/96/108 px. The score line uses 10 px between I/Q, 26 px between IQ and the first digit, and 10 px between digits. Scene-specific sticker motifs from the initial v21 attempt were removed after full-size review.

The four values remain inherited estimates from earlier drafts and are not verified IQ measurements or a comparable ranking.

## Rebuild and limits

Run from the project root:

```sh
python3 channels/paper_detour/videos/003_iq_gallery/Edit/typography_reset_v21_samples/build_review.py
```

This rebuilds the scene/title PNGs, previews, and contact sheet. It does not create a video or audio. No Palmier timeline or YouTube state was changed.

Generation and review notes: [`TITLE_DIRECTION_20261101.md`](TITLE_DIRECTION_20261101.md) and [`../../Source/Images/iq_gallery_subject_relevance_v21/GENERATION_LOG.md`](../../Source/Images/iq_gallery_subject_relevance_v21/GENERATION_LOG.md).

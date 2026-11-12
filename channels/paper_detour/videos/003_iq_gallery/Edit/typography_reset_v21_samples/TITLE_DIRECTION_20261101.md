# IQ Gallery v21 — title direction

**Status:** approved direction for a visual sample; not yet accepted as final card artwork.

## Project references reviewed

- `channels/paper_detour/brand/TYPOGRAPHY_STANDARD.md`
- `channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png`
- `channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/MATCH.png`
- Exact Paper Detour 004 reference: `channels/paper_detour/videos/004_last_video/Storyboard/user_reference_parallax_20261101.png`
- Current 4-pair sample and layered scene/title previews: `channels/paper_detour/videos/003_iq_gallery/Edit/typography_reset_v20_samples/`

The channel standard confirms that the tested title PNGs are the authoritative visual reference; no approved system font is known. Keep the wide rounded, slightly irregular uppercase paper glyphs, cream face, visible warm cut edge, matte grain, depth, and soft object shadow. Do not rebuild this with a system font.

## Extra High consultation

Coordinator personally checked ChatGPT.com in Google Chrome. The visible setting immediately before sending the prompt was **Extra High**. A single focused prompt requested a common title treatment and one restrained scene cue for each of four titles. Completed response in the Paper Detour project chat: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae74b79-d8d0-83eb-8e7f-7d2ab9ea2de0

### Fixed geometry and material

- Separate transparent RGBA title PNG, 1080×1920.
- Optical center x=540; row centers y=1304 / 1426 / 1560.
- Visible name glyph height 96 px; `IQ + number` height 108 px (ratio 1.125); maximum row width 820 px.
- 8–12 px visible gap between glyphs, 22–26 px between words, 26 px between the two name rows, 32 px before IQ.
- Cream face `#F1E3C9`, warm edge normally `#C47D45`, 6–9 px visible depth, soft deep-navy object shadow offset 8 px down-right with 10–14 px softness. Keep slight individual glyph contour variation.
- Add exactly one small scene-linked paper detail to each title PNG, attached behind the lettering and limited to at most 14% of the title block area. No plaque, rectangular backing, full underline, logo, or extra decoration.

### Four scene-linked details

1. **JOHN F. / KENNEDY / IQ 119:** change the edge to mahogany orange `#B86446`; add a thin dark-indigo ink-like paper stroke, about 290×22–26 px, starting behind the lower-right of KENNEDY and passing under only the right half of IQ 119.
2. **GARRY / KASPAROV / IQ 123:** use a slightly cooler brown terracotta edge `#B86F4D`; add a short three-cell stepped paper motif, 210–230×24–28 px, in dark indigo and muted cream, peeking behind the lower-right of KASPAROV and leading toward IQ 123.
3. **KANYE / WEST / IQ 133:** use a copper-amber edge `#C96F4A` and deepen the shadow by only 1–2 px; add a low three-peak indigo paper rhythm, 260–300×24–30 px, behind the center of IQ 133 and barely touching the lower edge of WEST. It must read as an abstract paper rhythm, not an audio icon/equalizer.
4. **MARILYN / VOS SAVANT / IQ 228:** warm the face slightly to `#F3E6CF` and use a dusty-orange edge `#CB7A4D`; add two thin, slightly offset page-edge shapes, 280–320×26–32 px, behind the lower part of VOS SAVANT and continuing subtly beneath IQ 228.

The four PNGs must remain one family with identical visible geometry and mass; only the edge nuance and one small paper detail vary. These are design instructions pending visual generation and review.

## Current v21 implementation note

The first v21 full-size review showed that scene-specific lines, chess cells, rhythm marks, and page strips read as detached stickers, so that decoration was removed. The scene itself now supplies the link through the real desk/table surface and relevant foreground objects.

The original IQ letters also read more serifed than the rounded name glyphs. A shared `IQ` pair was generated in the broad, rounded paper style of `A_MESSAGE.png` and `MATCH.png`; the score digits remain individual paper glyphs from IQ Gallery v13. This produces a more coherent rounded cut-paper title family while keeping the separate transparent title layer and the fixed 1080×1920 grid. See [`GENERATION_LOG.md`](../../Source/Images/iq_gallery_subject_relevance_v21/GENERATION_LOG.md) for sources and exact asset-generation prompt.

A second narrow Extra High review confirmed the serif I/Q should be replaced, with a reusable rounded paper-glyph pair and fixed score spacing: 10 px between I and Q, 26 px from IQ to the first digit, and 10 px between digits. The current builder uses those values and retains the approved 96/108 px row-height ratio.

**Current status:** four scene/title pairs generated and visually inspected; pending user review. The original scene-specific motif recommendations above are historical and were not retained in the current images.

# v03 approved thin frame — validation 2026-11-05

Both masters: ProRes 4444 with straight alpha, 30 fps, 480 frames, 16 seconds. Full-frame streamed decode completed; the central half of every frame has alpha 0, and all outer-edge pixels have alpha 255. MAE compares premultiplied RGBA on a 0–255 scale.

- 16x9: `paper-border-16x9-16s-v03.mov`, 527323309 bytes; SHA-256 `5f994a7f2abfc7612793e65afadc0f596c612c97ede2dc3ef72f747adf6f9b38`; wrap MAE 0.086811, final adjacent MAE 0.086947.
- 9x16: `paper-border-9x16-16s-v03.mov`, 558117103 bytes; SHA-256 `27427c87a53e01d6af07bcf39858a5e251a864fccf76136f1e44ef745411d425`; wrap MAE 0.087237, final adjacent MAE 0.087360.

The approved source recipe uses `render_master_v03.py`, with layer-normal factor 0.67 × 0.67 of v02 and periods 16, 8 and 16/3 seconds. Existing v01/v02 files and their consumers remain unchanged.

# Historical v02 master validation — 2026-11-04

The v02 masters are versioned v02 outputs generated from `render_master.py` after changing its default duration to 16 seconds and assigning layer periods `(16.0, 8.0, 16.0 / 3.0)` seconds. The 8-second v01 masters were retained unchanged under their original names and are superseded.

## Files and stream properties

- Horizontal v02 master: `paper-border-16x9-16s-v02.mov` — 844,827,575 bytes; SHA-256 `90313c452cee0b594adde27a8ab3f6b449d30ed085d7fee583d7e0990ae15985`.
- Vertical v02 master: `paper-border-9x16-16s-v02.mov` — 874,675,657 bytes; SHA-256 `072119faa983ce8364b99430c026fd51c2f3bc6326fc7a1ea9602b855c0ec434`.
- Both are ProRes 4444, decoded as `yuva444p12le`, 30/1 fps, progressive, 480 frames, exactly 16.000000 s. Full FFmpeg decode completed without errors for each.

## Alpha coverage

Checked all 480 decoded frames in each master. The central half of every frame is fully transparent (`alpha=0`). Every pixel across the top, bottom, left and right outermost edges is fully opaque (`alpha=255`) in every frame; no edge gaps were found.

## Formula periodicity and loop seam

- Rendered stills at `t=0` and `t=16` from the updated generator for both canvases. Maximum channel difference was 1/255 for both formats; mean normalized differences were 3.8563e-08 (horizontal) and 4.2552e-08 (vertical).
- Premultiplied-RGBA mean absolute error for frame 479 → frame 0 versus ordinary adjacent frame 478 → 479:
  - Horizontal: 0.1678033 versus 0.1680749 (ratio 0.99838).
  - Vertical: 0.1690744 versus 0.1695874 (ratio 0.99697).
- The wrap seam is no larger than the ordinary last-frame motion for either format. Layer periods are 16, 8, and 16/3 seconds (5⅓ s); the common loop period is 16 seconds.

## Preserved superseded masters

The prior 8-second masters were not overwritten or removed:

- `paper-border-16x9.mov` — 2560×1440, 240 frames, 8 s; SHA-256 `861ca2b08d1f635f8b0beb30c7fca16db17a30a58fd79a2186c467bf868ace6`.
- `paper-border-9x16.mov` — 1440×2560, 240 frames, 8 s; SHA-256 `5cae4121e02b515d97b172c0b0913583cc76b4bb90c1e96370e3d181efd466c2`.

These preserved files are not the current masters. Do not overwrite them when generating later revisions; use new versioned names.

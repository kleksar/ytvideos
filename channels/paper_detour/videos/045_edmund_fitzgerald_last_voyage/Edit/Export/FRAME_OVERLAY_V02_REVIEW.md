# Paper Frame overlay — review receipt v02

- Episode: Paper Detour 045; separate overlay review derivative only.
- Source v01: `Work/render_final_20261104/previews/edmund_fitzgerald_full_film_en_v01.mp4`; SHA-256 `2f0d0d0ec4f8f2f752cb1042b4be5b475bb7299b841981c783674611a4266c7b` (unchanged).
- Overlay master: `paper-border-16x9.mov`; SHA-256 `861ca2b08d1f635f8b0beb30c7fca16db17a30a58fd79a2186c467bf868ace6`; 2560×1440, 30 fps, 240-frame loop, ProRes 4444 straight alpha.
- Final v02: `Work/render_final_20261104/previews/edmund_fitzgerald_full_film_en_frame_v02.mp4`; SHA-256 `21c54c07e577f0d6ec2f80af55a5a0f83005012f05f07e4832e147ee52ec839d`; 569,988,023 bytes.

## Technical checks

- `ffprobe`: H.264 High, 2560×1440, 30/1 fps, 6764 frames, 225.466667 s; BT.709 limited range, yuv420p.
- Audio: AAC-LC mono, 44.1 kHz, 9712 packets. SHA-256 packet payload list compared with source v01: exact match for all 9712 packets.
- Full decode of final bytes: PASS (video and audio decoded to null output without errors; the checked candidate and final file have the same SHA-256).
- Source v01 file/hash: unchanged.
- Rejected attempts: `-t 225.466667` cut the final 3 AAC packets; removing `-t` alone while retaining `-frames:v` still cut the same 3. Final render was promoted from the validated remux where video is stream-copied and original AAC runs to EOF. Exact rejected render hashes and dispositions are recorded in `Work/frame_overlay_v02/render.log`.

## Visual review

Inspected contact sheet `Work/frame_overlay_v02/qa/contact_sheet.jpg`, extracted from final video at frames 0, 239, 240, 479, 480, 900, 3360, 6750, and 6763: opening, both sides of the 8-second loop seams, caption-bearing moments at 30 and 112 seconds, near-end and last frame. Border is composited around all four edges; captions remain legible and do not cross the frame. At frames 239→240 the repeated paper edge has no visible jump; at 479→480 the picture changes at a direct scene cut while the border remains consistent.

Full real-time film playback and subjective listening were not performed. This receipt covers ffprobe, full decode, exact AAC packet identity, and the listed sampled visual frames only. The v02 file is for user review; no YouTube state was changed.

# Paper Frame overlay — v03 review receipt

- Reviewed: 2026-11-05.
- Episode: Paper Detour 045; separate 16-second frame overlay preview, derived from verified v02.
- Base v02: `Work/render_final_20261104/previews/edmund_fitzgerald_full_film_en_frame_v02.mp4`; SHA-256 `21c54c07e577f0d6ec2f80af55a5a0f83005012f05f07e4832e147ee52ec839d`.
- Overlay master: `/Users/diplomat/Documents/Codex/2026-11-04/task-3/paper-border-source-kit/paper-border-kit/masters/paper-border-16x9-16s-v02.mov`; SHA-256 `90313c452cee0b594adde27a8ab3f6b449d30ed085d7fee583d7e0990ae15985`; 2560×1440, 480 frames, 16 s, straight-alpha ProRes 4444.
- v03 review preview: `/Users/diplomat/ytvideos/channels/paper_detour/videos/045_edmund_fitzgerald_last_voyage/Work/frame_overlay_v03/previews/edmund_fitzgerald_full_film_en_frame_v03.mp4`; SHA-256 `c372b380c94b857fd746284114bf8922fcfaf467e1ca75a0322f43ba2dd0d0e3`; 569,632,453 bytes.

## Technical checks

- `ffprobe`: H.264 High, 2560×1440, 30/1 fps, 6764 frames, 225.466667 s; yuv420p, BT.709 limited range.
- Audio: AAC-LC mono, 44.1 kHz, 9712 packets. SHA-256 packet payload lists compared with base v02: exact match for all 9712 packets.
- Full FFmpeg decode of video and audio: PASS, no decode errors.
- Source v01 and base v02 remain unchanged: hashes match the recorded originals.
- Render method: video-only H.264 overlay encode capped at the 6764 base frames; original AAC copied separately in a remux through EOF without `-t`, `-shortest`, or a frame cap. Exact commands are in `Work/frame_overlay_v03/render_command.json`.

## Visual review

Inspected `Work/frame_overlay_v03/qa/contact_sheet.jpg`, extracted from v03 at frames 0, 479, 480, 959, 960, 900, 3360, 4500, 6750, and 6763: opening; both sides of the 16-second and 32-second loop seams; subtitle moments at 30 and 112 seconds; middle, near-end and last frame. The frame appears consistent across loop resets and direct scene cuts; captions are legible and remain inside the paper edge.

Full real-time playback and subjective listening were not performed. This receipt covers ffprobe, full decode, packet-level audio identity and the listed sampled frames only. v03 remains a review preview pending the user's decision; it is not an accepted master and was not uploaded or published.

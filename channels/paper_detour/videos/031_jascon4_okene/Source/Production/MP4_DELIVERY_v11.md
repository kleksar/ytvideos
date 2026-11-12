# v11 MP4 export and file QA

User explicitly requested direct MP4 output instead of a separate ProRes picture master. Sharedgrain README already defined this; Palmier skill now links the single-MP4 rule.

- Project8BE390BC, timeline1BD3395C,snapshotD61DD23A; export jobD5D641F6-C68E-4E1B-AC51-3C552E097AAB completed.
- File: `/Users/diplomat/ytvideos/channels/paper_detour/videos/031_jascon4_okene/Deliverables/031_jascon4_okene_en_short_1080x1920_30fps_v11_fine_grain25.mp4`;94,415,065bytes; SHA-256 `d124dd1714d3088167bb3f527b41aff6a3a6c4d22808707b13fe9da2bea9a16e`.
- MP4,H.264,yuv420p,1080×1920,30fps,71.300s,video10524kb/s; AAC mono44.1kHz,~64kb/s,71.300s. Full audio/video decoder run returned0. Twelve actual MP4 frame samples reviewed at opener, cues, dark scenes, and ending: [`contact`](../../Edit/v11_full_composite_qa/MP4_CONTACT.jpg).
- Grain visible in sampled frames. Full1×playback, every internal cycle seam, and subjective AV/listening QA remain UNVERIFIED. No independent reviewer.
- **Audio delivery caveat:** mono AAC measured ~64kb/s; audio-delivery standard expects AAC-LC192kb/s mono. No secondary audio render/encode was applied. Keep this output as review MP4; not audio-delivery-final until the bitrate issue is resolved from original media under the applicable audio authorization and rechecked.
- Palmier API did not expose CRF or `tune grain`; no such flags claimed. No ProRes picture master produced. No upload/publication.

Detailed readback in `../../Edit/MP4_DELIVERY_RECEIPT_v11.json`; timeline edit is preserved in Palmier.

# Paper Detour 008 — unified accent layout v03

**Updated:** 1 November 2026  
**Active Palmier timeline:** `008_en_boyfriend_friend_voice_v03_unified_cues_20261101` (`B6614DFE`), project `845D33BD`.

## Layout standard

- All 45 cue events share one visible-text center: normalized X `0.50`, Y `0.18` on the 1080×1920 canvas (about 540×346 px).
- Letter height is 90 px for each text line. Two-line phrases use a taller text block but keep the same per-line height.
- PNG aspect ratios are preserved. Scale and center offsets are calculated from the solid visible alpha bounds (`alpha ≥128`), not the full PNG canvas; transparent padding therefore does not change the apparent size or position.
- Existing images and phrase wording are unchanged. A18 reuses A02, and A42 reuses A04. The 37 scene clips, cue order, cue timing and `VO` audio are unchanged from v02.
- Per-cue source image, line count, alpha bounds and exact transform values are recorded in [`accent_layout_v03_unified_20261101.csv`](accent_layout_v03_unified_20261101.csv).

## Decision and visual review

The placement pass was consulted in ChatGPT.com in Google Chrome; the visible mode was **Extra High**. Its proposed anchor was X `0.50`, Y `0.18`; its generic 52 px letter size looked too small against this episode's existing accent artwork. The final pass keeps the same anchor and uses 90 px per line for phone-size readability.

Reviewed contact sheets of all 45 cue midpoints from the final MP4. The accents stay in the upper central safe area, align consistently, and do not cover faces or key objects. The longest phrases remain within the frame. No cue content or timing changed.

## Render and version history

- Final MP4: [`../Deliverables/008_boyfriend_friend_en_1080x1920_30fps_voice_v03_unified_cues_20261101.mp4`](../Deliverables/008_boyfriend_friend_en_1080x1920_30fps_voice_v03_unified_cues_20261101.mp4).
- H.264, 1080×1920, 30 fps, 128.600 s; AAC mono, 44.1 kHz. Full-file decode passed. Decoded PCM audio matches the v02 render exactly.
- v02 timeline `CA237DA7` remains. Its local MP4 render was removed on 2026-11-02 after the newer v06 result was checked; the v02/v03 timeline versions remain. See [cleanup receipt](../Edit/cleanup_008_intermediate_2026-11-02.json). v03 was duplicated from v02; edits affect only the 45 accent transforms.
- Rollback snapshots on v03: `Before unified accent layout 20261101` (`B05D2A01`) and `Before significant-alpha glyph normalization 20261101` (`9B59DD69`).

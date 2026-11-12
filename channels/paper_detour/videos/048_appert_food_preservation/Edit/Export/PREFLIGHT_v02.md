# Paper Detour 048 — render preflight v02

- Full export: `Deliverables/048_appert_food_preservation_review_v02.mp4` (unique path; absent at preflight).
- Saved plan: `Work/production_local_v01/Edit/plan.json`, 5196 frames, 2560×1440, 30 fps, 173.2 s. Complete scene/cue track and current Paper Frame overlay over `[0,5196)`.
- Paper Frame source: current horizontal v02 portable VP9 alpha master, correctly decoded with libvpx-vp9 and converted to a frame-count-matched ProRes 4444 overlay at `Work/production_local_v01/paper_frame_full_v02.mov`; SHA and full edit dependency are in the export contract.
- Plan color input transfer is explicitly sRGB; output is Rec.709 limited-range SDR per delivery profile.
- Export settings PASS: `Work/production_local_v01/settings_check_v03/settings_check.json`.
- Lifecycle audit: `Edit/MediaLifecycle/audit-prerender-v02/audit.json`, 0 coverage errors; no files deleted.
- Audio: voice-only PCM mono 44.1 kHz, 173.2 s; accepted voice is 163.28 s plus 9.92 s digital silence. Word map timings are machine forced alignment; listening remains unverified.
- Scene PNGs are 1672×940/941 and enlarged proportionally to the 16:9 delivery canvas; suitability check must include the framed composition.
- This is a review MP4; no upload/publication authorization. Earlier v01 lacks the now-required Paper Frame and is superseded.

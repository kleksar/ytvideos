# Paper Detour030 — v13 author sample review

Final local film: `Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v13.mp4` and separate EN SRT. SHA256 `17fa8c7bfc1f915c203875f955330a7a84e1ad6f8fec65a77929a49975499680`.

## Result and scope

- Actual MP4:190s,5700frames,1920×1080,30fps,H264; stereoAAC48kHz,260787bit/s.
-39continuous scenes,4.1667–6s; all39 use depth-parallax MP4s and whole-image camera position/scale keys. Direct cuts; no Grain/Ripple tracks.
-33existing paper accents. D06 removed because it obscured the stone blade; D10 moved to its approved alternate anchor. Original PNGs retained.
- Full video and audio decode PASS. Video payload equals the completed native export; AAC payload equals the accepted v05 mix. SRT matches the preserved accepted SRT and spoken EN text;83cues. SRT playback/sync remains UNVERIFIED.
- Author viewed all3actual exported scene sheets and all4cue sheets:277unique actual frames, including first/mid/end of each scene and entry/hold/exit samples of every cue. Also reviewed117depth-render samples and framing/caption preflight composites.
- V27/V29/V31 camera paths were too tight in the first export. Addressed only their camera position/scale, then exported again and reviewed corrected native samples: hats/feet fit; no empty edges or face occlusions observed in samples. V30 remains an intentional torso detail already present in the accepted PNG. D23 visibly holds to its clip cut; C06 intentionally holds to film end.

**Full190s1×playback with sound, subjective listening of pronunciation/balance/sync: UNVERIFIED. Independent AV review: NOT_PERFORMED.** Decode, hashes and sampled frames do not establish those checks.

## Exact edit and receipts

Project `B1BA2D18`; baseline `A7C273C5`; final isolated timeline `82684371`. Final snapshot `948BCAAD`. Native export job `4261EC7B-07B7-4482-9CB3-E3DAEBD2EA86` completed100%. `POST_EDIT.json`, `CAMERA_HEADROOM_APPLIED.json`, `timeline_final.json` and receipts record addressed changes; source/archive timelines preserved.

Common pipeline run: `Edit/ImageMotion/f2eb90506b76cbdabfa3`. `gentle-aligned` preset, DepthFlow1.0.1 stable runtime, scene-specific depth_zoom. The helper result predates addressed caption/headroom fixes; current authoritative fingerprint is in `Edit/v13/POST_EDIT.json`. Do not rerun apply over this edited target.

## Cleanup and delivery

Unused renders/library imports were removed after dependency inventory. After final QA,51additional files (792604402bytes) were removed, including one duplicate old SRT, rejected/native duplicate exports and unreferenced helper/probe derivatives. All imported motion MP4s, original PNGs, audio/mix, depth cache, edit files, receipts and QA images retained. See `RENDER_CLEANUP.json` and `FINAL_RENDER_CLEANUP.json` for exact paths/hashes. Native export has deliberately been removed after payload identity verification; final MP4 remains.

Grain removal was performed by the concurrent user-authorized global cleanup; this task verified its result and made no duplicate grain mutation. See `grain_removal_verified.json`.

No YouTube upload/publication in this task.

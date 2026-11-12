# Paper Detour 048 — render preflight v04

- Full export is the 5196-frame, 2560×1440, 30 fps plan at `Work/production_local_v01/Edit/plan.json` (SHA-256 `47bc9d12cf4e83a865497223824281977b9b7b0d9f31220cbe91c03faba184d4`).
- Output: `Deliverables/048_appert_food_preservation_review_v02.mp4`; absent before render.
- Current Paper Frame overlay: 2560×1440 ProRes 4444, exactly 5196 frames, transparent alpha; current v02 design master retained as dependency.
- Current scene selection includes S02_v03 to prevent the title/subtitle/frame overlap. The sample review covers the precise subtitle/overlay composition at 1.0, 4.5, 5.7 and 9.0 seconds.
- Current subtitle contract/fingerprint is in `Work/production_local_v01/subtitle_prep_v09/`. Semantic grouping PASS; sample visual placement PASS; audible synchronization UNVERIFIED (no direct listening).
- Input color transfer: sRGB; output SDR Rec.709 limited range. PNGs are native 1672×940/941 and upscale to canvas without invented detail.
- Lifecycle audit and final settings check must pass before encoding. Scope remains user review MP4 only; no upload/publication.

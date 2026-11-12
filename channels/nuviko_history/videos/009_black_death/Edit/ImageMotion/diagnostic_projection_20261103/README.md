# Black Death — projection diagnosis

Source: scene001_london_excavation_v02.png; cached DepthAnything depth referenced in job JSON; still → clean DepthFlow 1.0.1 at 960×540, 30 fps, 4 s. Isolated diagnostic; no timeline, release, project presets or final MP4 changed. No camera, grain, subtitles or audio. Input source crop in comparison is rescaled, while DepthFlow uses zoom 1.05, so framing and compression differ.

A: height .2, isometric .3 (DepthFlow default), offset 0. B: same but isometric 1, offset 0. C: isometric 1 and offset .12*sin(pi*tau), D: .06*sin(pi*tau). Compare A and B to isolate default projection; C/D start and end at neutral and move through maximal displacement midshot. Compared frames 0, 1, 2, 3.9 seconds. Source and B differ in zoom, resampling and encoding; visual inspection confirms A has pronounced streaks, B much cleaner. C has visible displacement, and D is subtler; movement may still reveal new disocclusion artifacts. No full-frame/all-scenes QA or independent review performed.

A/B/C/D parameters are experiments, not approved production settings. `comparison_source_and_motion.mp4` is an enlarged crop of the source and A/C/D. Production workflow starts from original still, then depth/parallax, then camera, grain and subtitles; this experiment only examines the depth stage.

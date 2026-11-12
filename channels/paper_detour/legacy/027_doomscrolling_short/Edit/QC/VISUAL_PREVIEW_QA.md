# Silent technical visual preview — 027

`visual_preview_silent.mp4` is an **intermediate QC preview**, not a Palmier export or final deliverable. It was generated without opening, modifying, or exporting any Palmier project. It combines the seven stills at the exact frame intervals in `Edit/short_manifest.json`, the separate `captions_105_upper_scene05_v2.mov` graphic layer, and a small synthetic zoom. This preview's motion is not proof of the eventual Palmier timeline's motion.

Technical checks: H.264, 540×960 (half-size preview), 30 fps, 1,132 frames, duration 37.733333 s. `ffprobe` shows one video stream and **no audio streams**. Full decoding using `ffmpeg -xerror` completed without errors. Generation script: `render_visual_preview.py`.

Visual inspection used `contact_sheet.png`, containing individual frames 30, 190, 300, 400, 514, 515, 600, 754, 755, 800, 1010 and 1100, including the beginning, middle, end, and both boundaries of scene 05. Scene 05 captions are above the smartphone at the inspected frames, including 515 and 754; at frame 755 the following scene and its lower caption appear. This is a **12-frame sample**, not a whole-video composite inspection.

Open concern: in scene 06, the lower captions at frames 755 and 800 touch or cover part of the notebook while the character is writing. That object contributes to the action. Consider a higher placement for scene 06 and check throughout its interval. These samples do not prove that the remaining captions avoid faces and important objects at every frame or that captions match audio by ear. The clip is silent by design.

## v2: corrected captions for phone and writing scenes

`visual_preview_silent_v2.mp4` is another intermediate visual preview, with the same existing seven silent segments and `captions_105_scenes05_06_v3.mov`. H.264, 540×960, 30 fps, 1132 frames, 37.733333 s; one video stream, no audio streams. Full `ffmpeg -xerror` decode passed. Script: `render_visual_preview_v2.py`. Original preview and scene renders remain unchanged.

`contact_sheet_v2.png` shows frames 30, 400, 514, 515, 600, 754, 755, 800, 930, 978, 979, 1100. Scene 05 text is above the phone; scene 06 text is elevated above the writing hand and notebook and below the face. The longest scene 06 sample partially overlaps the resting forearm, while the face, writing hand and notebook remain uncovered. 754/755 and 978/979 switch the vertical position on the scene cut. This is a **12-frame visual sample**, not a full composite or audio review.

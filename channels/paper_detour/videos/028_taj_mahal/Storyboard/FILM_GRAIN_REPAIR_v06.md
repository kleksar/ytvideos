# Visible film grain repair v06 - 2026-11-02

User explicitly wants film grain across the entire frame, not CRT stripes. CRT v05 rejected. Root cause in v04 overlay proved: decoded alpha max1/255 mean0.93, instead of originalmax64/mean17.8. Prior full_alpha filename and claims were incorrect; do not use that overlay.

Shared master: channels/paper_detour/Shared/Overlays/Film_Grain/paper_film_grain_visible_15min_270x480_30fps_v01.mov.900s27000frames30fps, ProRes4444 alpha,10959590612bytes,sha256 eabd925c71ab523abd8dfc3164d03d73f588f767bf44460b75f918f233ce7d55. Derived from original vertical grain alpha multiplied3 using aa2 then1.5. Final master at24s decoded alpha max193 mean53.576. Prepared540x960 cycle mean53.649. Master uses270x480 source to avoid44GB storage and increase visible grain size; actual playback size must be checked. No edge fades,240-frame repeated cycle.900s terminal boundary not loopable.

Completed Extra High consultation and risks saved beside sharedmaster. One initial answer failed to load; second substantive answer read: check finalalpha and actual1080x1920 for coarse pixels. Silent4-second composited sample inspected at actual pixel crop;100% masteropacity excessively coarse/strong,45% remains visible without covering details. This illustrative sample is externally composited above flattened text; it is not the final saved timeline export.

Project25A8FF9A,timeline8565580B,grainclip29CFE306 replaced with media2200F995,opacity0.45,normalblend,no fades,normalized fullframe. V3 cues,V2grain,V1scenes,A1dialogue. Existing scene/cue/dialogue clip arrays and keyframes match original. Snapshot before023DDDC2,afterA863E57D. Exportjob51DCAC90-CC8E-4332-801F-249B7859543C currently preparing to Edit/Previews/028_en_v06_visible_film_grain_20261102.mp4. Not a completed delivery yet.

No publication. v04 delivery retained for provenance until verified replacement; it is rejected and visually invalid. Full final playback with sound remains unverified.

## User feedback and v07
User viewed the45% illustrative sample and said grain too strong. Reduced sharedmaster clip opacity to0.25; geometry and source unchanged. Snapshot1D78D235. Cancel requested for incorrect-strength v06 job51DCAC90-CC8E-4332-801F-249B7859543C; last state canceling. New v07 job0F4ACF1B-55D3-4959-A026-8F2F0A4E5459 queued to Edit/Previews/028_en_v07_film_grain_25pct_20261102.mp4. Neither completion nor perceptual acceptance claimed. New silent illustrative preview028_film_grain_25pct_4s_check.mp4 demonstrates reduced level; external flattened-text limitations remain as above.

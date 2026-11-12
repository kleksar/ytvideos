# Safe composition consultation — 2026-11-02

Visible mode before request: «Очень высокий».
URL: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae7efbd-75a4-83ed-ae0c-d762127296eb
Scope: whether preplanned source-image bounds can replace final motion/cue QA.

Completed visible response read by coordinator: safe composition is a preliminary geometric constraint, not a replacement for final QA. With fixed motion limits and accurate object bounds/masks, affine camera containment and caption collision can be checked mathematically over their entire swept areas, including intermediate extrema. DepthFlow can introduce inaccurate boundary depth, local stretching of faces/hands/architecture, disocclusion holes and changed silhouettes/occlusion. Each scene needs protected regions, a bound for their movement plus uncertainty margin, the complete camera path and the entire caption entrance/hold/exit corridor. No universal safe percentage. The final moving result still requires framing, scene×cue and depth-warp inspection.

Accepted: apply current canonical images/storyboard/image-motion requirements; do not waive final QA. Existing docs already include motion-safe composition before generation. No process-doc changes commissioned in this turn.

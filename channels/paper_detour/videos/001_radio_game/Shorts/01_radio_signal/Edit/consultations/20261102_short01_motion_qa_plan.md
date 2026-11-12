# ChatGPT Extra High consultation — Short 01 motion QA

- Date, task and stage: 2026-11-02; define targeted motion-framing QA for the existing Short 01 candidate, without editing it.
- Coordinator / browser / chat URL: `/root`, Google Chrome, https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0/c/6ae8da79-7a90-83eb-b17b-34d93423204b
- Exact visible mode immediately before sending: «Очень высокий».
- Inputs: Short01 review candidate SHA-256 `2046934add0e8647d35228d7d9d702e23e4cc9ff05a3fa4504ce85e52f7885a4`; six scene intervals; 279 prior visual samples; baked scene camera/depth assets.
- One narrow prompt: request the minimum final-MP4 sample that can support a targeted motion-framing status without claiming a full-frame review.
- Completed answer: five frames per scene at start, 25%, midpoint, 75%, and last frame (30 total), plus actual motion extrema not covered; check borders, cropping, depth-edge artifacts, caption safety and accent entries/exits. A targeted PASS remains separate from overall QA.
- Applied: exact quartile/end frames and 0.5-second actual-output samples across all six scenes; motion-cache keyframes establish endpoint extrema for linear camera paths, while depth artifacts are checked on rendered frames.
- Limitation: the consultation is advisory; actual inspection is recorded in `Edit/QA/short01_motion_review_20261102_v01/motion_review.json`.

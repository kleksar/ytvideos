# QA review — Paper Detour 048, render v02

- File: `Deliverables/048_appert_food_preservation_review_v02.mp4`
- SHA-256: `0a5938f3941ea7a2aae9a7e40437b59aee3cb3d556d20d59623896bba219d739`
- Technical report SHA-256: `b1f7942bb5ff988799403055547b0b7a78388964b35939729bbabb3f40b95431`
- Freshness: CURRENT against export contract v02 and frozen production plan.
- Overall verdict: **UNVERIFIED**. The export remains an internal review file.

## Checks

| Check | Result | Evidence / scope |
|---|---|---|
| Stream metadata | PASS | H.264 High, 2560×1440, progressive, yuv420p, 30/1 fps, Rec.709; AAC LC mono 44.1 kHz; both streams 173.2 s. |
| Full decode | PASS | Managed QA decoded all 5,196 frames. |
| Frame sampling | PASS | Reviewed all 730 requested frame samples in 30 chronological contact sheets, spanning 32 scenes and 117 caption groups. |
| Paper Frame | PASS | Visible on opening, scene transitions, body scenes and end cards; no apparent missing edge or seam in reviewed samples. |
| Motion framing | UNVERIFIED | Sampled frames show no visible crop defect, but every planned camera path and intermediate extremum was not checked scene by scene against the motion plan. |
| Word highlighting | PASS | Entry/hold/exit states visible across sampled groups; active word styling remains legible. |
| Cue timing | PASS | Visual cue sequence agrees with subtitle frame map and rendered sample states. This does not verify audible synchronization. |
| Audio signal | PASS | Measured mean −25.1 dBFS, sample peak −4.4 dBFS. Signal measurement only. |
| Subjective audio listening | UNVERIFIED | No direct listening completed; speech quality and caption-to-speech sync remain open. |
| Independent review | UNVERIFIED | This is coordinator self-review. |

## Findings

No visible frame loss, missing Paper Frame, caption collision, or unexpected scene gap was found in the sampled sequence. The opening cork remains inside the canvas. The old v01 render lacked the now-required Paper Frame and is superseded by v02.

The overall verdict remains UNVERIFIED because direct listening/audio-caption sync, motion-path coverage, and independent review are outstanding in the frozen QA plan. QA sample cleanup was not run; extracted QA frames remain held until a profile PASS permits lifecycle finalization.

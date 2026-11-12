# Paper 046 v31 review export preflight

One accepted v31 story, exact 288-word English adaptation and voice-only recording, 23 static paper sources with approved whole-image motion and direct cuts. Picture and captions cover 3428 frames at 30 fps (114.266667 s). This is the first full user-review export. Visual/technical input review and actual limited decoded sample are distinct from release QA.

## Selected sources and composition

Inspected all 23 actual PNGs in scene order at reduced portrait size. Reused exact earlier v02 files for S05, S13 and S20 after checking the new job and crop. Generated remaining sources for this storyboard. Corrected S04 and S22 plaques inside caption space, raised S16's workroom and S21's equipment clear of subtitles, and removed a misleading airship from S17. The cutaway omits a precise cable route. S01/S19 relief maps and reconstructed equipment are illustrative. Check precise sources, measured resolution, shot intervals and crop endpoints in `Source/Images/paper_v31/manifest_v31.json`.

Inspected three offline composites per scene (69 samples) from the selected PNG, planned crop and the shared renderer's actual caption PNG state. Samples cover entry, exit and the widest caption starting in each shot. Nine labeled contact sheets under `Work/paper-v31-prod-20261105/scratch/frame-review-final-*.jpg` preserve the frame indices. The revised images keep critical labels, objects and faces legible; some foreground scenic texture sits behind the subtitle line. This is a sampled preflight, with no assertion of continuous playback or final MP4 review. Raw image native dimensions are below the delivery canvas, so the export upscales shallow whole-image moves for review.

## Subtitle implementation

Built the first 341 frames as a sample MP4 through the same FFmpeg profiles at 1440×2560, 30 fps. Excerpt starts at source 0 and is decoded directly to 44.1 kHz PCM without speed or timing changes. Actual decoded video frames 0, 2, 3, 6, 7, 17, 18, 27, 28, 164, 165, 177, 178, 316, 317, 325, 331, 339 and 340 were examined at 216×384. The first group is neutral at frame 0; The/French/army switch individually at frames 3/7/18. The next phrase begins at 28. The shot cuts at 165 without a missing subtitle. The next group begins at 178. The final word retains yellow through the sampled pause at 331–340. Placement over the map and balloon protects the selected details. Evidence in `subtitle-trial-frames.jpg` and `subtitle-trial-transitions.jpg`.

The full shared caption generator produced 125 groups, each one to three words, and 289 initial/word states for all 288 tokens. Group interval endpoints form a continuous chain from frame 0 to exclusive frame 3428. Font is Chalkboard SE Bold, 104 pixels, baseline at row 1993; no episode styling override. All text compared to exact narration. Forced syntax boundaries remain in the review version due to the fixed three-word width and retained narration (for example, “not for the / military, could” and “tower's southern / leg.”). The group plan protects proper-name pairs where the profile permits. Editorial grouping remains open for release.

Audio timings use forced alignment against the retained waveform, with provider differences and hearing limits in `Edit/Subtitles/alignment_review_en_v31.md`. No subjective listening or pronunciation sign-off. Structural continuity and visual word changes on sample are separate from audible sync. The separate SRT has full literal coverage from the same map and awaits listening verification.

## Scope and lifecycle

Render is authorized for review. Existing source, archived previous output and retained references are held. Dedicated owned work run; preflight auditor scanned this episode and its bounded local reference scope, with no reported read errors, cleanup candidates or deletions. No external write or publication. No extra post-render MP4 inspection requested.

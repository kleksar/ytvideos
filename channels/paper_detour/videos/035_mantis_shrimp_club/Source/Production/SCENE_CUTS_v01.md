# Draft scene cuts v01 — Paper Detour Short 035

**Status:** production timing handoff for accepted narration EN v06 and user-accepted Lawrence voice v01. The 30 fps frame mapping, scene/cue composites, playback sync, and final MP4 review remain `UNVERIFIED` until the Palmier assembly is inspected and played.

**Timing source:** `Source/Voice/en_v01_lawrence/voice_en.alignment.json` (character alignment for the accepted voice) plus the visible Extra High consultation recorded in `CONSULTATIONS_20261102.md`. The voice file `Source/Voice/en_v01_lawrence/voice_en.mp3` is 44.16 s; this is the hard video end. Alignment's final endpoint is 44.24 s, 0.08 s beyond the file, and must not extend the timeline.

**Cut rule:** each scene begins at its spoken start. Natural pauses before the next spoken line remain on the preceding still. Every transition is a direct cut. S09 holds the final open phrase and cuts directly to the unchanged S01 opening master; no black, title, fade, or extra pause is added.

| Scene | Start | End | Duration | Spoken line / cut boundary |
|---|---:|---:|---:|---|
| S01 | 0.00 | 4.08 | 4.08 s | “A spear in one mantis shrimp. A hammer in another.” → cut on “At first…” |
| S02 | 4.08 | 11.72 | 7.64 s | “At first, the difference was not so dramatic. Early mantis shrimps had several pairs of hunting limbs that looked broadly alike.” → cut on “Over time…” |
| S03 | 11.72 | 15.80 | 4.08 s | “Over time, the front pair began to stand apart from the others.” → cut on “Across different lineages…” |
| S04 | 15.80 | 20.40 | 4.60 s | “Across different lineages, that front pair took two very different shapes.” → cut on “In spearers…” |
| S05 | 20.40 | 25.44 | 5.04 s | “In spearers, it developed a slender, spined end for catching and piercing.” → cut on “In smashers…” |
| S06 | 25.44 | 32.16 | 6.72 s | “In smashers, its striking end became a compact, thickened club, built to deliver a powerful blow.” → cut on “As the front pair…” |
| S07 | 32.16 | 36.32 | 4.16 s | “As the front pair changed, it stopped being just another pair of limbs.” → cut on “It became…” |
| S08 | 36.32 | 41.36 | 5.04 s | “It became the animal's defining weapon — a spear here, a hammer there.” → cut on “And that is how…” |
| S09 | 41.36 | 44.16 | 2.80 s | “And that is how one shared hunting limb became:” → direct loop to S01. Final spoken endpoint is aligned at 44.24 s, beyond the MP3 by 0.08 s; check the last word in actual playback, and do not lengthen this scene beyond 44.16 s. |

S02 and S06 are the longest holds; S09 is the shortest. The storyboard's original estimates were rough and pre-recording; no claim of exact deviation is made. Current narration and actual voice alignment supersede those estimates.

## Cue handoff

Use the accepted PNGs and spoken intervals in `CUE_SHEET_v01.md`; do not use superseded text suggestions embedded in storyboard v01. C01 remains within S03 (13.28–15.60 s; scene ends 15.80 s). C02 remains within S06 (26.56–32.08 s; scene ends 32.16 s). Seconds are alignment-derived, not yet frame-quantized or playback-verified. Use cue-sheet geometry and Palmier motion defaults only after verifying target project fps, safe-zone, and the final scene/cue path.

## Provenance and limits

Extra High was visibly set to `Очень высокий` immediately before the narrow prompt; consultation title `Карта сцен Short 035`, URL `https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae7ed96-9c8c-83eb-a63c-5b0157d22f7f`. It supplied a draft cut map from the exact narration/alignment. The coordinator saved the timing and checked the durations against the 44.16 s MP3 limit. This consultation is editorial input, not playback QA. The clip end at 44.16 s may truncate the final 0.08 s alignment tail; resolve only by inspecting the unchanged accepted voice and the assembled playback, not by silently extending or altering audio.

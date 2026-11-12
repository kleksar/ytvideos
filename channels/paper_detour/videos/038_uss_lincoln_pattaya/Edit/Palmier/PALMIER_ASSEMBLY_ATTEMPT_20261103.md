# Palmier assembly — 2026-11-03

**User instruction:** put the Paper 038 visual sequence on a timeline; the user will add animation and inspect the result.

## Target and method

- Dedicated project: `Paper 038 USS Lincoln Pattaya Visual Assembly v01.palmier` in this directory; active timeline: `Timeline 1`.
- Paper Short profile: 1080×1920, 30 fps, 9:16, Rec.709.
- Storyboard v01 timing; 17 scene slots, 81.4 seconds total. Sixteen unique still images; S17 reuses S01.
- No sound, subtitles, camera motion, transitions, or export. Caption accents were not placed in this pass.
- Palmier's project and timeline IDs were not exposed in the accessible UI; the target was identified by its project path/name and visible timeline tab.

## Completed assembly

- Created and saved `Paper 038 USS Lincoln Pattaya Visual Assembly v01.palmier` here using Palmier UI.
- Verified settings visibly in project inspector: 1080×1920, 30 fps, 9:16, Rec.709.
- Imported current scene stills: S01–S09, S10_v02, and S11–S16. Rejected S10_v01 was not used.
- Arranged 17 clips in order on `Timeline 1`, with hard cuts and no gaps. S01_v01 is reused for final S17 hold.
- Verified sequence report from Palmier montage agent: 2,442 frames at 30 fps, 81.4 seconds, `00:01:21:12`. Clip durations: S01 5.5; S02 5.0; S03 4.7; S04 4.1; S05 4.1; S06 4.3; S07 5.1; S08 5.9; S09 4.0; S10_v02 5.0; S11 4.0; S12 5.4; S13 4.6; S14 5.2; S15 5.7; S16 4.0; S17/S01 reuse 4.8 seconds.
- Palmier montage agent reported verifying exact order, clip durations, gap-free placement and a composited frame from every clip. Current UI visibly showed the beginning of the sequence with exact first clip timecodes and the project media item `1:21`.
- Saved the project with Command-S after assembly. Left the project open for the user to add animation.

## Earlier recovery

- The initial visible editor was an unrelated Nuviko 009 project; it was not edited. A save panel for an unrelated Black Death export also appeared during recovery and was left untouched.
- The new project's 16-PNG import caused the Palmier UI bridge to time out while the app remained open. Activity Monitor's normal Quit returned the app to its project list; reopening the named 038 project showed all 16 imports and persisted vertical settings. Assembly then completed through the in-app Palmier montage agent.

## Handoff

- Continue in this saved project and `Timeline 1`. User owns the animation pass.
- Scene and caption timing remains storyboard-estimated until narration is recorded and timed. No audio or export was created.
- If the user asks to place the two accepted caption accents, use the documented cue sheet anchors; they are absent from this timeline pass.

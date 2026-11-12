# Plan 09 — Daylight pause, v05

**Status: NOT READY — stopped at the composition gate.** No BG/MG/FG layers or t0/t4 endpoint stills were created because the generated master violates both explicit safety conditions.

## Candidate and provenance

- Candidate: `06_daylight_v05_master_candidate_NOT_READY.png` — 941×1672 RGB, opaque.
- Generated with ImageGen using the existing daylight master `Source/Images/06_daylight_master_v2.png` and character reference `Source/Images/05_joshua_profile_master_v03.png`. The generated original remains in `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-d4b703c3-161a-4d87-867b-2c417db5a617.png`; this copy is retained as a draft and does not overwrite either reference.
- SHA-256: `9db3e3b654f41e3bd358cb43b33492f4dc12922387f9cb143509658069a4d9b2`.

## Stop findings

- The table is large and runs off the left edge. The Joshua+table+laptop group therefore does not fit within the requested approximate x=125…805 safe region, and a full-table MG cannot move right by +8 px without revealing its cropped left edge inside the frame.
- The near-right plant touches the right and bottom canvas edges. It cannot safely take the required +11 px horizontal move without exposing a cropped plant edge.
- The face is visible and aimed toward the laptop; Joshua appears paused rather than exiting. The visible left hand rests on the table; the right hand hangs at his side. Those successful composition details do not resolve the table/plant edge failures.

Required motion was BG/MG/FG L→R by +4/+8/+11 px over four seconds, y=0 with no zoom or deformation. No layers were produced, so no offsets, alpha bounds, static endpoints, contact continuity, or motion were verified. The set is not ready for independent approval or import.

# Plan 09 — Daylight pause, v08

**Status: NOT READY — stopped before layer extraction.** The master improves the framing but misses the safe margin on the left side of the MG and the right-edge margin for the FG plant. No layers or t0/t4 stills were created.

## Candidate and provenance

- `06_daylight_v08_master_candidate_NOT_READY.png` — 941×1672 RGB, opaque.
- Generated with ImageGen from `layer_sets_v02/06_daylight_v07/06_daylight_v07_master_candidate_NOT_READY.png` and `Source/Images/05_joshua_profile_master_v03.png`. The generated original remains at `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-92933116-6029-4ea0-8790-c9d245eebf12.png`. No imported files were overwritten.
- SHA-256: `891624ecaacf59005d252d65348cf6cca1de7a1c783ce72c4041d42b60d4927b`.

## Stop findings

- Joshua sits left of the compact table and looks toward the open laptop. Chair and table supports are visible; the pose reads as a pause in the room.
- Approximate MG union begins at x≈76 at the chair and reaches about x≈810 at the table. The requested safe left bound is x≈120, so the full group does not fit in the planned x≈120…810 window with the required margin.
- The separate lower-right plant reaches approximately x≈937. After its required +11 px move, it would be cropped at the right edge and would not retain ≥40 px of margin.
- Required motion was BG/MG/FG L→R `+4/+8/+11 px` over four seconds, y=0 and no zoom/warping. Since the master failed the pre-layer gate, no alpha layers, endpoints, contact-drift checks, or playback were produced or verified. No independent review was requested.

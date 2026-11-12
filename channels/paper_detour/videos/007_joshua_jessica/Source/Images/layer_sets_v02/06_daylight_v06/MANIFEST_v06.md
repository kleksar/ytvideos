# Plan 09 — Daylight pause, v06

**Status: NOT READY — stopped before layer extraction.** The master misses the required safe bounds for both the moving MG group and the FG book/stool. No layers or t0/t4 endpoint stills were made.

## Candidate and provenance

- Candidate: `06_daylight_v06_master_candidate_NOT_READY.png` — 941×1672 RGB, opaque.
- Generated with ImageGen using `Source/Images/06_daylight_master_v2.png` and `Source/Images/05_joshua_profile_master_v03.png` as visual references. The source original remains at `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-cbfa272d-ddf0-4790-aff0-22a7995bc987.png`; no imported reference was overwritten.
- SHA-256: `39dc03a0f889f6969ec94ddd1608bb7ecc5c3917a23810a5f81825f30272e5f7`.

## Stop findings

- The visible Joshua/table/chair union spans approximately x=48…916, outside the required x=125…805 moving-group window. The table itself starts near x=48; the chair reaches near x=916. The required +8 px MG movement would leave unsafe edge clearance, so no layer pass was attempted.
- The FG book is on a low stool, but the stool is cropped at the left edge and extends beyond the requested x=80…220 region. This cannot safely satisfy the separate FG `+11 px` move.
- The daylight pause and gaze toward the laptop read clearly; Joshua’s left hand rests by the laptop and his right hand touches the chair. Fine finger count is not confidently verifiable at this scale. The composition defects block further use.
- Requested motion was BG/MG/FG L→R `+4/+8/+11 px` over four seconds, with y=0 and no zoom/deformation. No layer offsets, alpha bounds, contacts during movement, endpoint composites, or playback were verified. No independent review was requested because the composition failed the stated pre-layer gate.

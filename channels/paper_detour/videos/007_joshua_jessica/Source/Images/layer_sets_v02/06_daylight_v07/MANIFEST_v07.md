# Plan 09 — Daylight pause, v07

**Status: NOT READY — stopped at the composition gate.** The pose now follows the updated direction (Joshua seated to the left of the laptop table), but the moving group and FG plant miss their safe bounds. No layer extraction or t0/t4 endpoint stills were made.

## Candidate and provenance

- `06_daylight_v07_master_candidate_NOT_READY.png` — 941×1672 RGB, opaque.
- ImageGen source: existing references `Source/Images/06_daylight_master_v2.png` and `Source/Images/05_joshua_profile_master_v03.png`. Generated original retained at `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-6d2603f9-a8f4-4d20-8878-81a38b2622c3.png`; imported references were not modified.
- SHA-256: `8827ef53bac3984dae4687db4750cf406fc094f7e73f5f5da90a055c355a78fd`.

## Review notes

- Joshua is seated on the left, calm and facing the blank laptop on the separate table. His body, chair, table, laptop and support feet are visible; no empty chair is present. The character reads as paused in the room.
- Approximate MG union spans x≈20…920, beyond the requested x≈120…810. The chair reaches toward the left edge; the table extends close to the right edge. The prescribed +8 px movement would not have safe crop margins.
- The lower-right plant reaches the right frame edge, so it cannot safely move +11 px with the required ≥40 px post-move margin.
- The only requested motion was BG/MG/FG L→R `+4/+8/+11 px` over four seconds, y=0, without zoom or warping. No layers, alpha bounds, endpoint composites, contact-motion checks, or playback were verified. No independent review was requested because the candidate failed the pre-layer edge gate.

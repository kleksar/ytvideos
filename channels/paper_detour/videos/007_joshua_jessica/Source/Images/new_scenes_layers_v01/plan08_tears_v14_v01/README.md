# Plan 08 — tears v14 composition candidate

**Status: NOT READY — left shoulder margin is below 40 px.** This was the single bounded v14 master-only attempt. No BG/MG/FG layers were extracted and no independent review was requested because the t0 framing check failed.

## Composition and edge check

- Master: `masters/08_tears_master_v14_composition.png`, 941×1672 RGB.
- The image keeps the frontal 3/4 face, one static tear, simple blue night wall, hands outside the frame and small lower-left foreground lip. Joshua's face, hair, beard, sweater and restrained expression remain recognizable from v13.
- The correction moved the character left and reduced his size. Right shoulder now has safe room for a later +8 px MG test.
- The guide preview `previews/08_tears_v14_margin_QA.png` marks x=40 and x=893 (red), plus x=70 and x=850 (yellow). The left shoulder crosses x=40 and reaches approximately x=18–25 around y=1200–1300. This violates the required ≥40 px left margin at t0; no layer extraction or endpoint review was performed.
- The generated composition contains no extra people, text/UI, or added props. Hands are intentionally out of frame, so no finger count is claimed.

## Provenance

- Generated with built-in ImageGen from the preserved v13 master as face/style reference; this new image is versioned separately and v13 remains untouched.
- ImageGen output: `/Users/diplomat/.codex/generated_images/01a194de-e95f-7233-95be-7f11b3636ee3/exec-5c293330-a430-4ef5-a24d-0dce3e1d424c.png`.
- SHA-256: `9f25c81c1ca86f7001aa1c31860f10910a0352b0bfdd47a6717534fe86774c0b`.
- No audio, video or Palmier project was created or changed.

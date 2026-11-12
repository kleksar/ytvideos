# v08 render review — visual and caption-state coverage

- Exact MP4: `Work/production-v08-render/previews/041_dune_origin_EN_v08_review.mp4`
- SHA-256: `246f363529587216ce022fca83e4056d2d2c0998dc438c82e601e9249df94f1a`
- Technical helper result: `technical_status=PASS`, `verdict=UNVERIFIED`; stream metadata and full decode PASS, no technical failures.
- Visual review: PASS for the inspected samples. Human inspection covered 36 full-frame scene start/middle/end samples across all 12 scenes and 345 extracted frames covering scene/caption boundaries and 265 word-transition samples. No upper text overlays, caption clipping, blank sampled caption states, or multiple-yellow-word states were observed. Contact sheets are in this QA directory.
- Subtitle continuity: PASS for the complete authored timeline interval `[0,1443)`; 58 successive group intervals have no gaps, and sampled frames at the boundaries/pauses retain a visible caption.
- Word colour state: PASS in the sampled frames; the yellow fill advances one mapped word at a time. Audible synchronization was not assessed and remains UNVERIFIED.
- Semantic grouping: UNVERIFIED. The retained 58-group sequence is unchanged from v07 as requested, but the generated plan reports 8 syntax-boundary warnings; `grew beyond any / newspaper article` is one concrete unresolved break. This is not marked PASS.
- Audible synchronization: UNVERIFIED; this session has no audio-perception input. Word timing metadata and decoded audio do not prove heard synchronization.
- Motion framing between sampled frames and independent review remain UNVERIFIED.

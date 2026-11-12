# Caption exception approval

- Episode: Paper Detour 047 — Franklin search.
- Scope: the subtitles for one narration sentence; narration text remains unchanged.
- User instruction (2026-11-05): “Да, длинную фразу можешь там разбить, разрешаю такое исключение сделать.”
- Exact sentence: “Before Erebus was found, searchers knew where Franklin's crews had abandoned the ships, but not where either had finally sunk.”
- Authorized groups, preserving all words and punctuation:
  1. `Before Erebus was found,`
  2. `searchers knew where`
  3. `Franklin's crews had abandoned`
  4. `the ships, but not where`
  5. `either had finally sunk.`
- User-approved exception boundaries required by measured single-line width and syntax checks: `where | Franklin's`; `abandoned | the ships`; `where | either`. The third boundary continues the relative clause “where either had finally sunk” across the two adjacent groups; it is included because the renderer correctly flags a line ending on “where”.
- Chalkboard SE Bold, 84 px, local width measurements: 1027.0 / 894.1 / 1273.9 / 995.9 / 949.9 px; Paper safe width is 1298 px.
- Approval applies only to these exact adjacent groups in this sentence. It does not change the narration, font, geometry or general syntax checks.
- Evidence: user message in this conversation, 2026-11-05. Extra High consultation and local measurement: `CAPTION_EXCEPTION_REVIEW.md`.

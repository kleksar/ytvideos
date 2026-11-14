EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Transfer handoff — Paper Detour, fake Olympic torch (1956)

- Channel/format: `paper_detour`, `short`, English illustrated narration; RU is full semantic translation only, not a planned second voice.
- Verified prewrite `main` SHA: `636386783a13b7b11d2173c233b68654f43d9848`; source files were read on that SHA. See `research.md` for selection and URL/claim/evidence/uncertainty.
- This PR changes only its story package. No change to `docs/`, `.agents/skills/`, channel status, production or published materials.
- Script version: first candidate for this event; exact source text is `script.en.txt`, exact RU translation `script.ru.txt`. S001–S014 are mapped verbatim in `storyboard.json`. Duration not measured. No audio, images, video, external paid tool, upload or publication.
- Source dates/limitations: Barry Larkin interviewed in 2004 by The Independent; Irish Times 2000-06-10; historian's 2018-01-10 account; ABC description 2023-08-20 (audio NOT played); official 1956 torch collection; competing 2026-09-23 Short. Historical quotes NOT invented.
- Author checks: interest/clarity/fact/reach/loop discussed separately in `story-review.md`; text seam author PASS only. Independent, text-to-voice, subtitles and AV checks UNVERIFIED.
- Missing capability **in this execution host**: accessible repository checkout/runtime for `uv run ytv start` and live `sessions.independent` reviewer. GitHub connector can read/write Git objects but does not create a local run or produce a reviewer receipt.
- **Local transfer** (NOT executed): in an authorized clone at the exact remote revision, invoke `uv run ytv start --channel paper_detour --format short --intent 'Оценить сюжет о поддельном олимпийском факеле Сиднея 1956 года'`; read actual `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`; import `research.md`, `script.en.txt` and `script.ru.txt` as **candidate inputs** following the actual task contract (do not invent run ID/lease/receipt). Give the unprimed reviewer the opening, then the exact entire EN narration twice with seam, without author verdict/beat map. Only afterwards provide source ledger and strongest alternative. Record their original `ytv-script-review-v1` on the exact EN hash and rerun if changed.
- `awaiting_script_approval` is NOT achieved; no script approval, MP4 approval, production permission, provider reservation or upload permission is implied.
- Prior version handling: if script edited, preserve exact old EN/RU bytes as distinct versions, update every scene span and narrative statement, invalidate review/word timings and obtain a new independent response.

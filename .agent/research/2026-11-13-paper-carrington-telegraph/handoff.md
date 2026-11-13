# Local producer handoff

- **Channel:** Paper Detour (`paper_detour`), English voice Lawrence only per current pinned channel profile when the run is created.
- **Format:** Short portrait 9:16.
- **Base:** review the PR against its `main` base SHA; exact tracked content is on its branch, not yet a registered episode.
- **Bundle:** `research.md` (sources/claims), `script.en.txt` (full English narration, voice and subtitle source of truth), `script.ru.txt` (full Russian reading copy for editorial review; not for TTS), `storyboard.json` (preliminary per-line AI image briefs, not completed storyboard task), `editorial-review.md` (checks), `packaging-brief.md` (proposals).
- **Narration:** 184 English words; 14 provisional scenes at a summed 72.9s *planning grid*. This is **not** TTS-derived duration. After approved TTS with channel voice speed 1.10x applied once, recompute exact frame/word boundaries and adapt scene count; do not force speech into estimates.
- **Images:** none generated. The paper airplane is assigned to S008; obtain actual reference asset from the channel media bundle and verify its hash, or mark image verification pending.
- **Camera:** stage proposals are whole-frame pan or zoom only, no parallax. After images, choose actual focus and executable crop envelopes; if adjacent pans/zooms conflict, adjust per current visual standard.
- **Narration status:** not owner-approved; no task `create`, `approve`, `complete`, production lease, TTS, renderer, release spec or YouTube action has been executed.

## On local review
1. Read `script.ru.txt` to understand the story, then inspect `script.en.txt` cold for English narration quality and compare both texts, then research/source evidence and scene cards. Test beginning, development, payoff, natural loop and factual accuracy. Record PASS/FAIL with lines; do not accept on checklist presence alone.
2. If approved, merge according to project policy and create a new episode with CLI `ytvideos create` for `paper_detour` under current workflow; the run assigns the ID. Register reviewed script exactly using supported task outputs/approved user event—do **not** manufacture approval data from the fact that a PR merged.
3. Follow actual `status` → `next` → `context`, preserve pinned references and revisions. Resolve image-source assets, generate AI images, TTS, word timings, subtitles, then exact final MP4 QA and explicit owner approval before any release.
4. If the English script changes substantively, update the corresponding Russian paragraph in `script.ru.txt` and `narration_ru` in `storyboard.json` before the next review. Replace preliminary scene timing with measured English speech duration. Do not generate images from this draft before text acceptance.

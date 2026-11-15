EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Handoff — Nuviko History / Tham Luang rescue

## Integrity

- Remote `main` read at editorial selection: `5d3222c8888c775d2195c8b2949949f2d992e98d`; new PR **must be based on a fresh verification of that exact remote ref before branch creation**. If it moved, stop/reconcile, don't silently rebase an approval.
- ChannelSpec: `channels/nuviko_history/channel.json` reports `status=active`, `language=en`, `recipe=illustrated`; **not** musical `nuviko_videos`.
- Intent: English historical Long 16:9, proposed ~3–5 min **not measured**, 48 preliminary visual compositions.
- EN TTS/SRT text master candidate (not authorized): `script.en.txt` Git blob **`26749edac4f4b4735e8026f81d3312264dda35b2`**.
- RU meaning-preserving translation: `script.ru.txt` Git blob **`bedc69ff9d3089ddd9422dd1d6ea7d7a40312d6c`**.
- Supporting docs: `research.md` sources and counter-signal; `story-review.md` **author-only** audience-first-v1 eight scores; `storyboard.md` exact sentence spans and unexecuted visual prompts; `packaging-brief.md` promises, first proof and payoff.
- Source verification date: 2026-11-15; medical evidence NEJM 2019-04-03; Guardian contemporaneous timeline July 2018; full links in research.
- Revision history: initial complete original draft in exact blobs above; one author speech consistency/clarity pass. No later alternative approved. No prior measured timings or review to carry forward.
- Permissions: user requested **only editorial Draft PR**. NO merge; NO TTS, image generation, render, external video, upload, publication, channel status change; NO production media approval or script approval.
- Blocked capabilities: this host has GitHub read/write connector and web, but no usable local checkout/matching `uv run ytv` runtime; attempted local git network failed DNS and `/mnt/data` contained no checkout. Consequently **no official run ID, plan_summary, read_next, pinned task_guide or independent reviewer receipt exists**. The `sessions.independent` / approved external reviewer is not exposed by the host. vidIQ credit balance is zero through 2026-12-06; private audience metrics and comments unverified.
- CI after opening PR: verify actual run status for exact branch SHA; never turn pending or blocked into SUCCESS.

## Exact local transfer (requires authorised host)

In an actual local clone with working runtime, start **a NEW official run**, do not infer a fake one from this PR:

```bash
git fetch origin main
# Check the cloned repository's current main, channel profile and this Draft PR before using any candidate.
uv run ytv start --channel nuviko_history --format long --intent 'Проверить и зарегистрировать редакционную заявку Tham Luang 2018 как новый сценарий, без производства'
```

Read the **actual** JSON `plan_summary`, `read_next`, pinned `task_file`, `task_guide`, `skill_file`, and every pinned `reference_documents` before an output. Verify current registered topics again. For the subsequent **research task** use `research.md` only as unregistered input and confirm all source access; for the subsequent **script task** transfer the literal UTF-8 bytes from `script.en.txt` and `script.ru.txt` as **unapproved candidate** (do **not** present them as an approved `--source-script`). Compare their exact Git blob hash and re-run language, factual, storyboard-span and audience-interest checks in the pinned version. A fresh independent host must read EN hook then whole exact script twice **without** author scores or beat map; store its original `ytv-script-review-v1` receipt and rerun if EN bytes change. Only actual user approval can advance script gate; even an approved script doesn't authorize media under this PR. Generated media later requires separate direct user permission.

No automatic promotional action or external upload is scheduled by this handoff.

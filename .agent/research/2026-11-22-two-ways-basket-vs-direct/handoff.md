EDITORIAL_CANDIDATE_UNREGISTERED

# Git-only handoff
Source remote `main` recorded immediately before work: `131ef24068d75967b1e43aa88e5f1370f6775054`. Canonical #124 **merged** and included in current main (proposed owner revision originally `7d6bdf7702a2a241a33a21677fce29f26ada9b72`; it is historical provenance, **not** an alternative runtime pin or imported diff). Branch parent must be exactly current remote main. Do not modify docs/skills/ChannelSpec/status.

Story: Two Ways Lab / “One Sock, Eight Objects: When the Basket Wins”. Paths `variants/02m/|05m/|10m/script.en.txt` and `script.ru.txt` all complete. Exact English/Russian SHA256 and word counts in [story-review.md](story-review.md). Shared model/source comparison in [research.md](research.md). Proposed editorial master: **02m EN** hash `aea6306a0ffeea438472d5d7bb2a8a5f9c616577e588f75daed4cec6a37bbd85`, RU `87c2234d51e98ae5c13cd28b8adb999ac153a707fc7080710e210c2129d37d88`. Owner has not approved this exact text.

### Precise blockers (observed)
1. `uv run ytv start --channel two_ways_lab --format short ...` was attempted in available shell and returned `Failed to spawn: ytv; No such file or directory`: no runnable checked-out package/runtime here. Thus **no actual run ID, lease, plan_summary, read_next, pinned reference_documents, task_guide, receipt or script gate**. PR is editorial only.
2. No independent reviewer tool/session invoked; no blind first read of exact six texts nor `ytv-script-review-v1`. Self-scoring in story-review is not that review. Changed hash requires new independent review. Let reviewer read exact selected text cold *without* author's verdict/beat map, then show sources, honor rejection.
3. Channel profile `channels/two_ways_lab/channel.json` has `production.formats.long.video.canvas=null` and `fps=null`: 5m and 10m are **editorial-only Long**. No Long run authorization, no recipe import. 02m has about 301 EN words, materially above ordinary 35–50 second Short guidance; actual VO duration and format acceptance need explicit check. No speed adjustment authorized.
4. Actual text loop with two full blind readings, audible/visual seam, artwork rights, real reference bytes, voice and approved media assets **UNVERIFIED**.
5. Competing same-author Shorts baseline and current YouTube-comments unavailable; vidIQ balance observed **0** Nov 22, no paid tool calls. Audience demand is a hypothesis; no fabricated CTR/retention.

### Local continuation
With real source checkout and approved runtime, first read pinned task packet. Run `uv run ytv start --channel two_ways_lab --format short --intent 'basket vs direct delivery: source editorial story PR'` in an environment where `ytv` actually exists, inspect `plan_summary`, `read_next`, `task_guide`, `reference_documents`, and preserve one exact selected master only after actual independent reviewer and owner decision. Import true source commit/path/hash with task contract's `attach-artifact --kind script_variant` and `--kind story_review` where available; no fabricated IDs. Long variants are supporting/editorial artifacts only. If existing pinned run conflicts, use explicit documented migration, never overwrite its pins. Do not generate images, TTS, MP4 or publish without later authorization. CI pending/queued ≠ PASS.

### Scope / ownership
Git tree adds only this new research folder and its 11 files, does not touch previous story PRs, channel configuration, common docs, schedule or media. Review/quality gates all explicitly separate.

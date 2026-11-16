EDITORIAL_CANDIDATE_UNREGISTERED. This is a Git-only editorial review and DOES NOT represent a registered run or approval.

## 2026-11-16 meaningful revision — PR #99

- Baseline `2c3f479ded348828fac3d51c7b1c59f8fe0e76a7`; original EN/RU blobs `8dab171aad21914e37171459619815fbacc88934` / `e30442b52d29d681b157f512a8993c7f7361493e`, preserved.
- Three independently complete EN/RU variants: [02m](variants/02m/script.ru.txt), [05m](variants/05m/script.ru.txt), [10m](variants/10m/script.ru.txt); exact SHA-256 each language and separate judgments in [story-review](story-review.md); common sources in [research](research.md).
- Recommended for owner review: **05m Long**, no automatic production. 02m is the unchanged baseline with the old storyboard tied to the same exact hash. 05m/10m need new storyboards; old spans are invalid for them. Do not copy source script into a pinned run without explicit review/migration.
- Existing PR showed no owner approval comments or inline threads at baseline. GitHub inspection cannot prove no local active run/agent; coordinator must check shared store and concurrent sessions before any production or script-gate action.
- Proposed policy from Draft #124 exact `7d6bdf7702a2a241a33a21677fce29f26ada9b72`, not canonical main. Main `ddafebf5aec10ff4158b4ea8aabac4dd1d576b67`; no unrelated rules or profiles modified.
- Independent review `UNVERIFIED`, actual duration `UNVERIFIED`, Short AV seam `UNVERIFIED`, owner approval `NOT_GRANTED`, YouTube metrics `UNVERIFIED`. No TTS/MP4/Flow/image generation/upload.
- Next queue candidate after #99: #98 Demon Core, only after actual HEAD/owner-production check. Continue reviewing all open technical PRs separately for their own code contracts.

---

## Original handoff context, retained

EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Handoff — Nuviko History / FedEx Flight 705

- **Base:** main `5d3222c8888c775d2195c8b2949949f2d992e98d`, checked 2026-11-15; new branch `work/story-drafts/nuviko-fedex705-cockpit-1994-20261115`. Exact resulting branch HEAD and file blob IDs must be read from GitHub after commit, never invented here.
- **Status:** separate unregistered editorial hypothesis. This is **NOT** a ytv episode/run or user-approved production script. No merge/TTS/imagegen/render/upload/scheduling.
- **Channel:** `nuviko_history`, `active` from current `channels/nuviko_history/channel.json`, English narrative Short 9:16; RU is owner translation.
- **Files:** `research.md`, `script.en.txt`, `script.ru.txt`, `story-review.md`, `storyboard.md`, `packaging-brief.md`, `README.md`, `handoff.md`.
- **Sources:** U.S. Court of Appeals 1997 https://caselaw.findlaw.com/court/us-6th-circuit/1058021.html ; captain eyewitness 2011 https://stateaviationjournal.com/index.php/news/life-changer-horrific-story-fedex-flight-705 ; contemporary Reuters 1994 https://www.washingtonpost.com/archive/politics/1994/04/08/jet-lands-safely-after-attack-on-crew/d6481a01-a4ee-4e63-9c23-29504c5f9ee3/ . Audience signals with limitations are in research.
- **Production attempt:** `uv run ytv start --channel nuviko_history --format short --intent 'Подобрать один сильный документальный сюжет для Nuviko History с исследованием зрительского интереса'` returned `Failed to spawn: ytv (No such file or directory)`; no local project checkout/store or pinned plan was available. Independent `sessions.independent` host and `ytv-script-review-v1` were not provided. Do not fake run ID or approval.
- **Local transfer:** use authorized checkout with shared store: first `uv run ytv start --channel nuviko_history --format short --intent 'Оценить редакционный кандидат FedEx 705 и подготовить полный EN script к согласованию без медиа'`, read genuine `plan_summary`, `read_next`, `task_guide`, pinned skill/reference docs, and hand in research and **unapproved** full EN/RU. If an existing run for this exact request exists, use `status`/`resume`/`plan`, not duplicate start. Obtain fresh independent `ytv-script-review-v1` on exact EN hash with full double reading and literal seam. Only then show owner exact texts at `awaiting_script_approval` for explicit decision.
- **Checks:** current artifact paragraph alignment self-check planned on GitHub readback; independent factual/interest/translation/loop review is **UNVERIFIED**. Any script revision invalidates prior review and storyboard text/timing assumptions. A real voice/music/subtitle/AV seam is testable only with actual MP4, which was neither made nor authorized.
- **Scope/permissions:** no changes to global docs/skills, code, ChannelSpec, production media, YouTube or approved original #20/#25.

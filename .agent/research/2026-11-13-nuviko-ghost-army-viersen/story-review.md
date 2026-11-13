# Story review — Ghost Army Operation Viersen, editorial revision r1

**Review status:** `EDITORIAL_CANDIDATE_UNREGISTERED`; official ytv script gate **NOT PASSED**. Exact EN is `script.en.txt`; RU is `script.ru.txt`. Review below is **author/editorial self-check**, NOT a fresh independent reviewer. No actual `ytv-script-review-v1`, independent session ID, run ID or receipt exists.

## Before storyboard: interest / first listener / natural spoken prose

- **Stop (author check: provisional PASS):** immediate tanks-in-field image followed by rubber reveal, with no unfamiliar unit name needed.
- **Stay (author check: provisional PASS):** objective changes: real divisions secretly depart; small unit impersonates a much larger force; visual, audible and radio signals make the decoy plausible; real engineers add evidence; actual troops cross; captured map tests the ruse. The end map is *new evidence*, not a repeat of the hook.
- **Payoff (author check: provisional PASS):** captured enemy order-of-battle overlay placed the 79th approximately near the portrayed sector and lost the 30th. This is more precise than saying “the Germans were fooled completely.” Limited resistance after crossing was reported in museum source; the ruse was part of wider Ninth Army activity.
- **First-listener clarity (author check: provisional PASS):** “Ninth Army,” “two divisions,” “old positions,” “decoy area,” “captured map” are introduced through actions; avoids corps numbering, German city names, radio technical jargon and an unverifiable victory count.
- **Speech / narration (author check: provisional PASS):** concrete action rather than character labels; sentences vary in length; no invented soldier dialogue or motives. First thought includes “Up close, they were made of rubber,” so viewer learns the *what* early; later middle develops *how* and outcome rather than hiding obvious answer. Potential snag: “eleven hundred” and “thirty thousand” are two large numbers in succession, but the contrast is the mechanism.
- **Factual support (author check: provisional PASS for selected claims; source limits explicit in research):** G1–G4. “Little resistance” is museum summary, not a claim of no resistance. The map supports mistaken deployment intelligence, not quantitative proof of Ghost Army contribution.
- **Originality vs PBS and other stories:** no source script copied. Prior queue has warfare PRs but no precise fake-camp/radio/captured-order-of-battle construction.

## Literal seam and full repeated-read self-check

Full `script.en.txt` and `script.ru.txt` were each displayed **two consecutive times** during author editing, then checked conceptually as a repeat. These were silent **text readings**, not synthesized voice, not an independent review, and not an AV test.

**EN — exact last two sentences → first two sentences**:

> But the map showed the Germans were wrong about where the divisions were. And if you'd looked where that map pointed, what would you have seen? | Rows of American tanks stood near the Rhine. Up close, they were made of rubber.

**RU — exact last two sentences → first two sentences**:

> Но карта показала, что немцы ошибались в расположении дивизий. А что увидел бы наблюдатель там, куда указывала эта карта? | У Рейна стояли ряды американских танков. Вблизи было видно: они резиновые.

**Textual seam: author PASS, independent UNVERIFIED.** The loop is a *question → visually specific answer*, after the map evidence and full payoff. The question names the location of the earlier fake force, so the next first sentence answers it even for a first-time viewer; no unresolved outcome is deferred. The closing question is a possible stylistic weakness and could feel like a scripted restart; an independent reviewer is free to **FAIL the concept**. The second viewing does not add an invented second battle or alter chronology.

**AV/voice/music/subtitle/physical edit seam: UNVERIFIED.** Only actual MP4 can test matching pose, duration, sound and restart. A title or punctuation mark is not seam evidence.

## EN/RU equivalence table (self-check only)

| Check | EN → RU |
|---|---|
| Date/roles | March 1945; US Ninth Army; 2 real infantry divisions; after-dark movement: present in both |
| Scale | ~1,100 secret-unit personnel vs >30,000 pretended troops: present in both (no extra numeric survival claim) |
| Actions | Rubber tanks and guns; recorded troop/bridge sounds; fake radio traffic; genuine engineer bridge gear; concealed real forces: present in both |
| Result | Mar 23 crossing and little resistance: EN “little”, RU “почти не” (same qualitative limit) |
| Evidence | Captured German map places one division roughly near decoys; other missing: in both |
| Caveat | Wider Ninth Army operation means no sole-cause claim: present in both |
| Ending | Hypothetical observer looking at map's marked area and receiving opening tank image: same question→answer |

**Independent bilingual-review: UNVERIFIED.** Minor nuance for later reviewer: EN “made of rubber” and RU “резиновые” refer to rubberized-canvas decoys, not mechanically functioning tanks.

## Required independent method — not performed

No usable checked-out repository/CLI for `uv run ytv start` in current host; no genuine `plan_summary`, `read_next`, `task_guide`, pinned runtime documents, run ID, leases or research/script receipts. No `sessions.independent`/fresh agent host tool was actually available; generic external session management is not a new independent reviewer. Therefore no `ytv-script-review-v1` on exact EN hash, no literal independent double-read, and no `awaiting_script_approval`.

When locally registered, ask the new independent reviewer (without author beats): reason to continue after opening; exact line of attention loss; one unnatural stock phrase, if any; whether the ending provides payoff and becomes the first line naturally. Permit “understandable but not worth watching,” change of theme, and FAIL. Only after their **first** cold read disclose G1–G4 and strongest alternative (Vincent Coleman). Preserve verbatim answer and hash; later edits require new review.

**Repository checks:** exact EN/RU scene-span equality can be checked in Draft PR. Local `scripts/check_repository.py`, actual ytv runtime gates and video checks NOT RUN without checkout. GitHub CI must be checked separately at resulting commit.

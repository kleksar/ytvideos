EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Two Ways Lab / sock grouping versus direct matching

## Canonical and immutable references

- **Repository:** `kleksar/ytvideos`.
- **Working source:** remote `main` `131ef24068d75967b1e43aa88e5f1370f6775054` (must be revalidated at write time), tree `c92263f9171a6a4500dcfcdb3afa37b180bb1c79`.
- **Policy:** PR [#124](https://github.com/kleksar/ytvideos/pull/124) is merged 2026-11-16; current `main` `docs/standards/editorial.md`, `narration.md`, `.agents/skills/ytv-write-script/SKILL.md` used. Historic proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is **not** the source/main revision.
- **New editorial branch:** `story/twl-sock-pairing-20261122`, started from current `main` with no modifications to shared docs, skills, channels or old PRs. Actual PR and commit state must be checked remotely after write.
- **Channel:** `two_ways_lab`; `channel.json` supports illustrated Short and has unresolved Long production parameters.
- **Recommended exact master:** `variants/02m/script.en.txt` SHA-256 `acdad2e474507905712613933cc239b5f6cbbcb0d35e73c9d4effa19ecb265e5`.
- **Matching complete RU:** `variants/02m/script.ru.txt` SHA-256 `5e2223c891af5007e78d36f6a4e793260b432662aa38ef2764d9316fec4388f4`.
- **Long editorial alternatives:** 05m EN `dde1b996a2a82b509ee4965ded8c67412ad1e56d41fbef4a8987b609b33a6358`, RU `40fe8621a47bd184198d650a01a012e72b7384f8f4a38c9258ce50bd1f1feb1d`; 10m EN `bc00fec620e360a2a40bf23de649d394a07c8c48b4ab7f90df84dbcb76fc7485`, RU `610ad419e501be8781803227e61875660e0210c793ea99f0b47d05c4133eecfa`.
- Other exact variant paths/hashes and per-criterion judgments: `story-review.md`. Primary facts and model reproducibility: `research.md`. Packaging: `packaging-brief.md`.

## What was actually blocked

1. **Runtime:** attempted `uv run ytv start --channel two_ways_lab --format short --intent 'Редакционное исследование новой истории Two Ways Lab и пакет 2/5/10 EN/RU'` in the available environment; error `Failed to spawn: ytv / No such file or directory`. Not a registered episode. **No read_next, plan_summary, pinned task_guide, pinned reference_documents, lease, artifact IDs, reviewer receipt or owner script approval exist from this environment.**
2. **Independent reviewer:** no separate blinded reviewer session/capability actually executed. Full 02m text must be read once cold and twice consecutively, without the author's scoring/beat map; sources shown only after initial judgment. Do not fake `ytv-script-review-v1`. New text hash invalidates any later review.
3. **Audience analytics:** vidIQ current 0 credits; limited publicly indexed YouTube metadata and genuine Reddit discussion only; same-author controlled baseline, last-30–90-day breakout and YouTube comments/CTR/retention UNVERIFIED.
4. **Long:** `channel.json` has `production.formats.long.video.canvas=null` and `fps=null`, no complete Long recipe. The 05m and 10m texts are editorial alternatives only; do not create a fake Long run or alter ChannelSpec.
5. **Visual/assets:** brand image references, licensing, actual captions, measured TTS, picture-to-picture continuity, and AV seam remain UNVERIFIED; no bytes or handles for those objects invented.

## Local continuation — not yet performed

In a functioning authorized repository/runtime at the same canonical version, read the full skills and channel pinned instructions and identify an existing compatible run before starting a new one. For a new story/Short and only if none exists:

```bash
uv run ytv start --channel two_ways_lab --format short --intent 'Проверить выбранный 02m sock-pairing script и полный 2/5/10 EN/RU пакет'
```

Read actual `plan_summary`, `read_next`, `task_guide`, `reference_documents` and claimed context. Attach exact six current texts as `script_variant` and `story-review.md` as `story_review` using the existing runtime receipt/tool procedures and real IDs; never invent them. Give a fresh independent reviewer the exact 02m input without these author's grades; only later give the common evidence, capture reviewer-produced unmodified response under existing schema. Correct substantive issues with one exact new revision/hash and get a new review, or classify REWORK/REJECT without production.

If the 02m English exact text passes applicable checks, present it at the existing **single** script approval gate. Before media, require owner approval and the actual channel brand reference bytes/hashes. Create detailed storyboard/prompts only for that chosen **exact hash**, follow `channels/two_ways_lab/docs/SCENE_PLANNING.md` and `brand/VISUAL_PROFILE.md`; do not reuse spans/word timing from other variants. Do not spend credits/generate media, render, upload, alter schedule or merge from this editorial PR. If owner later chooses a Long, follow documented format migration and solve Long production blocker first.

This is a story Draft PR candidate in the editorial queue, not official production readiness.

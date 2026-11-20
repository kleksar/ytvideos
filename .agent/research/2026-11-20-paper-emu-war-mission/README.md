EDITORIAL_CANDIDATE_UNREGISTERED

# Paper Detour — When the Machine Gun Had to Chase the Birds

**Логлайн:** Во время засухи 1932 года австралийским фермерам угрожали многочисленные эму. На помощь прислали солдат с пулемётами. Птицы разбегались, а попытка преследовать их на грузовике провалилась. В итоге пришлось защищать поля иначе.

| Цель | Предлагаемый формат | Чистая озвучка на русском | Full English narration | Редакционное решение |
|---|---|---|---|---|
| 2 min | Short, possible per ChannelSpec; speed TBD | [RU](https://github.com/kleksar/ytvideos/blob/story/paper-emu-war-20261120/.agent/research/2026-11-20-paper-emu-war-mission/variants/02m/script.ru.txt) | [EN](https://github.com/kleksar/ytvideos/blob/story/paper-emu-war-20261120/.agent/research/2026-11-20-paper-emu-war-mission/variants/02m/script.en.txt) | STRONG_CANDIDATE; natural textual seam, AV UNVERIFIED |
| **5 min** | **Long, supported by ChannelSpec** | [RU](https://github.com/kleksar/ytvideos/blob/story/paper-emu-war-20261120/.agent/research/2026-11-20-paper-emu-war-mission/variants/05m/script.ru.txt) | [EN](https://github.com/kleksar/ytvideos/blob/story/paper-emu-war-20261120/.agent/research/2026-11-20-paper-emu-war-mission/variants/05m/script.en.txt) | **STRONG_CANDIDATE — recommended** |
| 10 min | Long, supported by ChannelSpec | [RU](https://github.com/kleksar/ytvideos/blob/story/paper-emu-war-20261120/.agent/research/2026-11-20-paper-emu-war-mission/variants/10m/script.ru.txt) | [EN](https://github.com/kleksar/ytvideos/blob/story/paper-emu-war-20261120/.agent/research/2026-11-20-paper-emu-war-mission/variants/10m/script.en.txt) | REWORK: extended explanation loses tempo |

**Recommendation: 05m.** It gives the farmers a concrete problem, lets the soldiers attempt a second tactic after the first failure, then reveals why a high kill count would not by itself protect a harvest. The 02m version already supplies a complete payoff but loses much of that cause/effect. The 10m is a self-contained text, not a truncated master, but a historical-method discussion slows its last third.

**Status:** exactly six full EN/RU texts, one shared [research](research.md), [per-version review](story-review.md), [packaging](packaging-brief.md), [handoff](handoff.md). No official `ytv` run, independent reviewer, source approval, TTS, imagery, MP4 or publication. Do not import as a production approval. Current source main: `ea314fc36a798ded8d8ec684085e5a4c3aca80aa` (2026-11-20); #124 was merged on 2026-11-16; no separate proposed revision was imported.

Narration is archival documentary **not** a claim that Australia formally declared war on birds. No unverified soldier dialogue or bird strategy is presented as a fact. Estimated audio duration only; Lawrence voice / 1.10 speed not yet generated. Rights to the historical newsreel are **not** granted; do not embed it.

Hashes: [story-review](story-review.md). Production migration: on equipped local host check canonical pinned documents, run `uv run ytv start --channel paper_detour --format long --intent 'Produce approved emu-war 05m text from editorial candidate'`, ingest the chosen exact master following the accepted-source workflow; retain approved hash, run/pins and independent review before script gate. This editorial recommendation is not that approval.

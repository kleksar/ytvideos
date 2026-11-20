# Giannini 1906 — comparative story-review (editorial only)

Status **EDITORIAL_CANDIDATE_UNREGISTERED / UNVERIFIED**. Author inspection only; this is NOT independent review, not an official ytv script gate, and not an approval. Baseline PR head before migration: `cbf7b307b68d0d8db8a6417c6920ca7f9f5a982e`. Earlier editorial pass used `7f6c9fb4ce98535aeb11de0973ae9f2459886e23`; current canonical main confirmed `17e14e451a06704c880f9b8fe606b3411ac06dee` on 2026-11-20. No runtime pins migrated.

## Exact six texts (verified read-back)

| Duration | Full EN | Full RU | SHA-256 EN | SHA-256 RU | EN words | Intended format |
|---|---|---|---|---|---:|---|
| 02m | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | `510071c68cb39df6a744bc45546ba3ce75acfc03602210c959fe2a7b02cc65bc` | `01fb5c13fff313f1ac41b7ea60c2b25775ca4535ff4d89a9584a121494c5ecf0` | 258 | Short 9:16 |
| 05m | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | `49dd373aa127974928c33c4832fc528a030cd7be94db006c1656467948b05e10` | `7462ec14312b4d5d94941bb99add8993e09981de9cfa58c79a0aa4d7e9a1c8be` | 562 | Long 16:9 |
| 10m | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | `39c473c3d500e04a7661c7f527ebd8026d8daa2e963d1bdd2973f00210aa47a9` | `5f619a3588276d68ef6b105af7e4f90ba89d6a111cf77a35b1ab37bea09c023f` | 1379 | Long 16:9 |

For approximate duration, 125–145 spoken English words/minute plus meaningful pauses. Two-minute version may exceed 2:00 at some natural rates; five-minute version may be shorter than 5:00. **No TTS timing was measured.** Do not alter pinned voice speed for a target. Current `nuviko_history/channel.json` supports both Short and Long, but no Long runtime is registered by this editorial PR.

## Story maps / questions and answers

**02m — rewritten on 2026-11-20:** wharf plank and burnt office prove the premise at once → quake/fire threaten saved deposits → Giannini carries cash and records under oranges to San Mateo → rival vaults remain inaccessible → surviving cash is useless without customer transactions → temporary counter and handshake rebuilding loans → separate timber bottleneck → captains finance supply → deposits sustain lending → later Bank of America name with explicit non-causal caveat → need for a usable counter leads directly into opening wharf. Human line: clients need savings, loans and building materials; Giannini makes each transaction possible. New final does not ask a forced question after the answer. Root `script.en.txt` Git blob `3ec5d6c7b266fd21f52b6644631fd6514083d78d`, root RU blob `dd57569800bb323de9332972f95c16395a2e0722`: original source preserved byte-for-byte; NO storyboard transfer to revised 02m.

**05m — new Long:** Questions: how to run a bank without a building and why customers would trust it → background on immigrant customers and produce trade → earthquake/fire puts cash at risk (main hook) → disguised wagons save access → ruin and blocked vaults create new obstacle → barrel counter restores contact → loans to rebuild → surprising material bottleneck → finance northbound timber ships → new deposits sustain transactions → growth through subsequent branch expansion → two questions answered by actual banking activity, not the wooden prop. Human line is Giannini serving local residents and ship captains, not a heroic myth about rebuilding the entire city.

**10m — new Long:** Three questions on customers' savings, extending credit and future institution → before-fire customer base and fruit-trade background → growing bank already established → fire threatens assets (main hook) → evacuation of cash and records → ruined office and rival vaults → two temporary service points → resident loans plus limits of handshake myth → lumber delivery as new bottleneck → local deposits and financial liquidity risk → 1907 panic tests reserves again → 1909 California branching law enables further expansion → 1930 Bank of America name → final barrel counter reframed as functional continuity. This pays off all three questions but second-half explanations risk becoming a banking lesson.

## Eight exact-text criteria (author ratings, not measured performance)

| Criterion | 02m | 05m | 10m | Concrete basis / main limitation |
|---|---:|---:|---:|---|
| Interest / significance | 7 | 8 | 7 | Barrel bank is strange and relatable; 05m develops practical timber problem; 10m may lose casual viewers in liquidity details |
| Opening | 8 | 8 | 7 | 02m immediate picture; 05m two specific questions and real quake before main hook; 10m adds a third question and longer setup |
| Development / cause to stay | 8 | 8 | 7 | Revised 02m makes cash-without-counter insufficient, then timber a second obstacle; 05m expands both decisions; 10m branches into a second crisis |
| Payoff | 8 | 8 | 8 | Revised 02m shows both lending and timber arriving before explaining the counter; 05m retains more mechanics; 10m takes longer to pay off liquidity |
| Freshness of angle | 7 | 7 | 7 | Familiar barrel anecdote; lumber-finance mechanism and 1907 stress test provide some distinctive perspective, no proven uniqueness |
| Visual specificity | 8 | 8 | 7 | Wagons, oranges, hot vaults, waterfront counter and timber ships; banking reserves/branch rules much less visual |
| Natural, clear oral speech | 8 | 8 | 7 | Revised 02m removes the quiz-question ending and ties a place to an actual customer need; still needs an independent repeated read; 10m remains expository |
| Verified audience interest | UNVERIFIED | UNVERIFIED | UNVERIFIED | No comparable public/owned CTR, retention or controlled audience measurement; no 1–10 estimate invented |

**Author / confidence:** all scored lines are author/editor judgments, **moderate confidence** for text clarity and historical narrative structure, **low confidence** for predicted audience attention and format-specific pacing. Main weakness: the intriguing counter image is revealed early, so 10m cannot justify every later paragraph through suspense alone.

## Hard checks (do not blend with ratings)

- EN/RU equivalence: author inspected matching events, date, banking structure, explicit nonexclusive growth, dispute on amount of cash. External native language listener **UNVERIFIED**.
- Factual grounding: shared [research](research.md) plus 2026-11-16 additions support pre-1906 banking, 1907 panic/reserves, 1909 branch law and 1930 name. Figures for rescued sum omitted due to conflicting reports; no invented conversations, personal motives or unverified victim actions.
- Long opening: 05m and 10m start with meaningful questions → substantive pre-quake context → fire threatens usable bank assets as main hook; no scripted question after every paragraph. **Author text check**, independent first-listener UNVERIFIED.
- Revised 02m Short: author reread complete EN/RU twice, including literal last→first join. EN last `he had saved the money, but still needed a place where customers could put it back to work.` → first `On a San Francisco wharf, a banker reopened for business behind a plank laid across two barrels.` RU last `теперь нужно было место, где клиенты смогут снова пустить их в дело.` → first `На причале Сан-Франциско банкир снова принимал клиентов за доской, положенной на две бочки.` Proposed causal join: saved money requires a usable transaction point, and the first line names it, with payoff already supplied. **AUTHOR TEXT CANDIDATE**, NOT independent PASS; MP4 AV seam **UNVERIFIED**. Long loop **N_A**.
- Storyboard: `storyboard.json` S001–S020 remains bound ONLY to the byte-identical unchanged ROOT Short EN/RU. Changed 02m and untouched 05m/10m have different text hashes and MUST receive their own version-bound scenes/spans/visual intent after choosing one; no measured timings or accepted variant storyboard. Visual production **NOT_STARTED**.
- Independent reviewer: no independent review result, session id or `ytv-script-review-v1` receipt. Author/self-review is NOT independent. Fresh unprimed reviewer may prefer original or reject all versions and must receive exact scripts without this verdict first; source ledger is shown only after first reading.
- Approval/runtime: official `ytv start`, pinned task context, attach-artifact IDs, `awaiting_script_approval`, owner choice and future MP4 checks all **NOT_STARTED / UNVERIFIED**. No implied approval of 3 productions.

## Comparative added value and decision

**02 → 05:** damaged offices and overheated vaults explain why saved cash matters; new physical bottleneck of lumber moves the story beyond the barrel trick; deposits show the bank actually functioning. Stronger action→new fact→cause→consequence chain.

**05 → 10:** gains Giannini's customer-acquisition context, a second test in the 1907 financial panic, and a source-supported reason for branch growth. However the rescue has been resolved before the 1907/1909 material; the section beginning with liquidity risk is likely the first interest drop. In revised 02m, the shorter 1930 name-change coda is still a possible attention drop after timber financing, but the arbitrary branch-count tail and redundant test question are gone; in 05m, 1930–1949 expansion is a small coda. These are **editorial hypotheses, not retention data**.

**Recommend 05m** as best balance of self-contained answers, human stakes, additional obstacles and payoff. This remains one *proposal*, not approval. The rewritten two-minute text now offers a coherent alternative without a forced final question; independent reviewer may prefer it, the preserved original, or neither.

**Progress (2026-11-20):** original one Short → three full EN/RU durations completed previously → original 02m had authored loop FAIL → substantive 02m EN/RU rewrite with current hashes and new independent storyboard requirement → author text checked, 05m still recommended; reviewer, owner master choice, TTS/AV and runtime UNVERIFIED. Next unreviewed candidate must be selected by current open PR/head and overlap/owner check, not by stale numbering.

## 2026-11-20 exact-hash revision evidence (02m)

- **Baseline before current pass:** branch HEAD `a7fe08af1e542ccaef619a85ab7e6b75cab3dc9d`, old 02m EN SHA-256 `637adb05a288e016b24f299a59baa92ca20f3a639811b72b5d7ab891c83778fc`, RU `66f372959c7d3db876808bf47a2a672b57093ffa6f49c62ea7ebc9bccdec0cb4`. Root sources unchanged and protected from this edit. Exact new 02m hashes are in the version table above.
- **Before → after:** previously the narrator quizzed the audience about a counter already named twice. New complete Short establishes the counter, turns salvaged cash into a practical challenge of customer access, introduces lumber transport as a separate obstacle and returns from the completed answer to why a functional counter was necessary. New text is 9 paragraphs in each language, same facts/causal order. Original root and both Long versions remain unchanged.
- **Eight criteria, 02m (author only, medium confidence for narrative, low for attention):** interest 7/10 (strange but familiar bank-revival image); opening 8/10 (counter and lost premises immediately); causal development 8/10 (cash access → customers → timber); payoff 8/10 (transactions and supply finance complete the promise before restart); fresh angle 7/10 (lumber finance, not a new topic); visual 8/10 (wharf/oranges/vaults/ships); spoken clarity 8/10 (no forced quiz ending, still unlistened); demand UNVERIFIED (no baseline). These are author ratings, not independent review or predicted retention.
- **Hard checks:** EN/RU semantic match author-checked including 1906/1930, oranges, vault restrictions, timber origins, nonexclusive future growth and attribution limits; no new unsupported amount, quotes or motives. Author reread doubled Short texts; independent first listener, measured speech, AV seam and genuine audience interest UNVERIFIED. Existing storyboard spans/timings do not apply to revised 02m. Longs require questions→immersion→hook and remain as previously inspected; no new independent acceptance for either.
- **Added value comparison:** 02m now gives a complete causal chain without its former weak quiz; 05m still explains why customers trusted new access and what lumber financing means, while 10m adds a later banking panic and law but slows after the 1906 rescue. **Provisional choice remains 05m**, not owner approval or three productions.

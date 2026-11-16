# Giannini 1906 — comparative story-review (editorial only)

Status **EDITORIAL_CANDIDATE_UNREGISTERED / UNVERIFIED**. Author inspection only; this is NOT independent review, not an official ytv script gate, and not an approval. Baseline PR head before migration: `cbf7b307b68d0d8db8a6417c6920ca7f9f5a982e`. Main editorial rules read from `7f6c9fb4ce98535aeb11de0973ae9f2459886e23`.

## Exact six texts (verified read-back)

| Duration | Full EN | Full RU | SHA-256 EN | SHA-256 RU | EN words | Intended format |
|---|---|---|---|---|---:|---|
| 02m | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | `637adb05a288e016b24f299a59baa92ca20f3a639811b72b5d7ab891c83778fc` | `66f372959c7d3db876808bf47a2a672b57093ffa6f49c62ea7ebc9bccdec0cb4` | 242 | Short 9:16 |
| 05m | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | `49dd373aa127974928c33c4832fc528a030cd7be94db006c1656467948b05e10` | `7462ec14312b4d5d94941bb99add8993e09981de9cfa58c79a0aa4d7e9a1c8be` | 562 | Long 16:9 |
| 10m | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | `39c473c3d500e04a7661c7f527ebd8026d8daa2e963d1bdd2973f00210aa47a9` | `5f619a3588276d68ef6b105af7e4f90ba89d6a111cf77a35b1ab37bea09c023f` | 1379 | Long 16:9 |

For approximate duration, 125–145 spoken English words/minute plus meaningful pauses. Two-minute version may exceed 2:00 at some natural rates; five-minute version may be shorter than 5:00. **No TTS timing was measured.** Do not alter pinned voice speed for a target. Current `nuviko_history/channel.json` supports both Short and Long, but no Long runtime is registered by this editorial PR.

## Story maps / questions and answers

**02m — unchanged original:** plank counter immediately → date/fire → rescue cash under oranges → ruined office and inaccessible vaults → counter on wharf → handshake loans → northern timber shipments → customers deposit again → name change / branches → forced question returning to original image. Full narrative, but loop is visibly writer-driven. Root `script.en.txt` Git blob `3ec5d6c7b266fd21f52b6644631fd6514083d78d`, root RU blob `dd57569800bb323de9332972f95c16395a2e0722`: both preserved byte-for-byte.

**05m — new Long:** Questions: how to run a bank without a building and why customers would trust it → background on immigrant customers and produce trade → earthquake/fire puts cash at risk (main hook) → disguised wagons save access → ruin and blocked vaults create new obstacle → barrel counter restores contact → loans to rebuild → surprising material bottleneck → finance northbound timber ships → new deposits sustain transactions → growth through subsequent branch expansion → two questions answered by actual banking activity, not the wooden prop. Human line is Giannini serving local residents and ship captains, not a heroic myth about rebuilding the entire city.

**10m — new Long:** Three questions on customers' savings, extending credit and future institution → before-fire customer base and fruit-trade background → growing bank already established → fire threatens assets (main hook) → evacuation of cash and records → ruined office and rival vaults → two temporary service points → resident loans plus limits of handshake myth → lumber delivery as new bottleneck → local deposits and financial liquidity risk → 1907 panic tests reserves again → 1909 California branching law enables further expansion → 1930 Bank of America name → final barrel counter reframed as functional continuity. This pays off all three questions but second-half explanations risk becoming a banking lesson.

## Eight exact-text criteria (author ratings, not measured performance)

| Criterion | 02m | 05m | 10m | Concrete basis / main limitation |
|---|---:|---:|---:|---|
| Interest / significance | 7 | 8 | 7 | Barrel bank is strange and relatable; 05m develops practical timber problem; 10m may lose casual viewers in liquidity details |
| Opening | 8 | 8 | 7 | 02m immediate picture; 05m two specific questions and real quake before main hook; 10m adds a third question and longer setup |
| Development / cause to stay | 7 | 8 | 7 | 02m jumps from rescue to growth; 05m creates new material bottleneck after loans; 10m branches into a second crisis |
| Payoff | 7 | 8 | 8 | Actual deposits/loans explain barrel story; 10m makes deposit/liquidity constraints explicit but takes longer |
| Freshness of angle | 7 | 7 | 7 | Familiar barrel anecdote; lumber-finance mechanism and 1907 stress test provide some distinctive perspective, no proven uniqueness |
| Visual specificity | 8 | 8 | 7 | Wagons, oranges, hot vaults, waterfront counter and timber ships; banking reserves/branch rules much less visual |
| Natural, clear oral speech | 7 | 8 | 7 | Original forced closing question; 05m uses concrete actions; 10m contains extended explanation beyond rescue tension |
| Verified audience interest | UNVERIFIED | UNVERIFIED | UNVERIFIED | No comparable public/owned CTR, retention or controlled audience measurement; no 1–10 estimate invented |

**Author / confidence:** all scored lines are author/editor judgments, **moderate confidence** for text clarity and historical narrative structure, **low confidence** for predicted audience attention and format-specific pacing. Main weakness: the intriguing counter image is revealed early, so 10m cannot justify every later paragraph through suspense alone.

## Hard checks (do not blend with ratings)

- EN/RU equivalence: author inspected matching events, date, banking structure, explicit nonexclusive growth, dispute on amount of cash. External native language listener **UNVERIFIED**.
- Factual grounding: shared [research](research.md) plus 2026-11-16 additions support pre-1906 banking, 1907 panic/reserves, 1909 branch law and 1930 name. Figures for rescued sum omitted due to conflicting reports; no invented conversations, personal motives or unverified victim actions.
- Long opening: 05m and 10m start with meaningful questions → substantive pre-quake context → fire threatens usable bank assets as main hook; no scripted question after every paragraph. **Author text check**, independent first-listener UNVERIFIED.
- Original Short: entire EN/RU texts assessed twice. Cold opening understandable, barrel answer already supplied, but final explicit question artificially repeats starting image, so **natural text seam FAIL** (not PASS by a shared object or punctuation). MP4 AV seam **UNVERIFIED**. Long loop **N_A**.
- Storyboard: `storyboard.json` S001–S020 remains bound to exact unchanged ROOT Short EN/RU and therefore also byte-identical 02m variants. It is NOT usable for 05m/10m; no measured timings, accepted Long visual span mapping or new prompts. Visual production **NOT_STARTED**.
- Independent reviewer: no independent review result, session id or `ytv-script-review-v1` receipt. Author/self-review is NOT independent. Fresh unprimed reviewer may prefer original or reject all versions and must receive exact scripts without this verdict first; source ledger is shown only after first reading.
- Approval/runtime: official `ytv start`, pinned task context, attach-artifact IDs, `awaiting_script_approval`, owner choice and future MP4 checks all **NOT_STARTED / UNVERIFIED**. No implied approval of 3 productions.

## Comparative added value and decision

**02 → 05:** damaged offices and overheated vaults explain why saved cash matters; new physical bottleneck of lumber moves the story beyond the barrel trick; deposits show the bank actually functioning. Stronger action→new fact→cause→consequence chain.

**05 → 10:** gains Giannini's customer-acquisition context, a second test in the 1907 financial panic, and a source-supported reason for branch growth. However the rescue has been resolved before the 1907/1909 material; the section beginning with liquidity risk is likely the first interest drop. In 02m, branch-count coda followed by redundant loop is the weak spot; in 05m, 1930–1949 expansion is a small but necessary coda. These are **editorial hypotheses, not retention data**.

**Recommend 05m** as best balance of self-contained answers, human stakes, additional obstacles and payoff. This remains one *proposal*, not approval. A stronger two-minute rewrite may win later independent comparison, but the current original is preserved rather than overwritten.

**Progress:** not processed (one Short) → six texts complete → author-checked with exact SHA-256 → 05m recommended; independent first listener, master choice and format-specific storyboard blocked pending actual runtime/owner decision. Next unchecked existing history: #81 Sydney fake Olympic torch, subject to fresh remote head/owner check.

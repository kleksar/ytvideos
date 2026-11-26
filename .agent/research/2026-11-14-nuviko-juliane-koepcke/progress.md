# PR #70 progress — 2026-11-17

| Phase | Before | After | Evidence |
|---|---|---|---|
| Inventory | One complete EN/RU Short at baseline `60a61531bb46da0b16c12db7de5b7100bbb0d718`; old 16-scene visual plan | Same originals retained, six complete variant files | `variants/02m`, `variants/05m`, `variants/10m`, exact SHA-256 in `story-review.md` |
| Editorial | One concise survival story | 05m adds father/route decision, other seat-row victims, empty shelter; 10m adds storm uncertainty, ecology, lost food, public aftermath | Read full EN/RU and research; no invented fall aerodynamics |
| Evaluation | One short authorial review | Three separate eight-criterion assessments, story maps, hard checks and comparison | `story-review.md`; audience/independent reviewer UNVERIFIED |
| Recommendation | Original short only | **05m Long recommended**, not approved | Additional 2→5 beats strengthen central human line; 10m weakens after rescue |
| Storyboard | S001–S016 original | Same storyboard bound exclusively to 02m exact hashes | `storyboard.json` |
| Runtime | Git-only candidate | Git-only candidate, not official production | `EDITORIAL_CANDIDATE_UNREGISTERED` |

Exact script hashes: 02m EN `b13bd78664370f0592f1b7b5508753f16584f4b098d45ab8a108abe5a1b3811d`, RU `bbf9cd7e89dc0d868cb3cb047dad401580d2f043c3f16ee2e4cb692ec967805b`; 05m EN `15de58915f42cc391dda170cd04e9e27a68d45d4750781d5361bb42b35684acb`, RU `2ce93efa86ff450e0fe06f92649dca7c7253050985de804e582142d02c0b4aa7`; 10m EN `04fa648735c3ad7a7c151ee39582140c532e87d0aa53470946b433d25fe794e4`, RU `8bd0ead794410799ee02811a1a6b4ad6bf02b9577205d9fdceb9b99cb1b238b9`.

**Uncompleted:** independent listener/reviewer receipt on exact hashes, formal ytv registration/approval, 05m Long storyboard, voice duration/AV, real audience demand. No production actions permitted. Next narrative #69; technical #77/#78 remain in scope. Remote HEAD/CI to be rechecked after write; no CI SUCCESS inferred from previous HEAD.


### 2026-11-19 — 05m editorial rework

Baseline HEAD `63e3adcc3a2f7be659575c088574074c43eff066` → new script EN `c2f746ad3e1db2f7e93b23933f0930b40cdaf6bc573b093628260004fb5fc311` / RU `93530a8cd2196a33c2b990346837ae62842995640376922347a2ce722c30ddc6`. Was: unoccupied hut → rescuers. Now: empty hut → infected wound, fuel and painful historical attempt → rescuers. Source ABC 2022 rechecked; shared research updated; bilingual script, reviews, README, packaging, handoff synchronized. Existing 02m/10m and source master untouched. Status: three complete variants, 05m author-revised and provisionally recommended, not owner approved. Blockers: independent reviewer/receipt, scene timing for exact text, true runtime run/approval, actual TTS/MP4. Next unrelated technical review #77/#78.


## 2026-11-26 — revision of 02m and 10m; current candidate

Baseline `c58e07c562b5ce5bd95f42c316e936df03ced6a0`, canonical main `7c779c4b2fd379c85166ae1b164fa53d1ea08843` (#124 merged). 05m remains byte-identical and recommended. Original root scripts and storyboard are preserved as historical exact evidence, NOT the storyboard of the revised 02m. The other two candidate pairs were revised; new exact SHA-256 and spans are in story-review.md. No owner approval or production action. No external runtime / Codex session visibility; no owner acceptance or production evidence in available PR discussion. Independent reviewer capability not found in available host tools; no fabricated review. Exact runtime pins must be checked at handoff.

Was → now: 02m thematic restart → direct answer after full rescue; 10m repeated travel and generic aftermath → documented bird cues, recognition of other passenger, rescue encounter and concrete conservation work. Exact package:

| Target | EN | RU | Words EN/RU | SHA-256 EN | SHA-256 RU |
|---|---|---|---:|---|---|
| 02m | [Full EN](variants/02m/script.en.txt) | [Full RU](variants/02m/script.ru.txt) | 289/245 | `a024abb9009c3933c6d8c8111b56d58937fc598bd00bf0ab378b234664c0782a` | `94fbbe652fe82b19cffcdf0745cc6ca4c5df448cd137a3bfc65bd40bd0ca6d1a` |
| 05m | [Full EN](variants/05m/script.en.txt) | [Full RU](variants/05m/script.ru.txt) | 717/590 | `c2f746ad3e1db2f7e93b23933f0930b40cdaf6bc573b093628260004fb5fc311` | `93530a8cd2196a33c2b990346837ae62842995640376922347a2ce722c30ddc6` |
| 10m | [Full EN](variants/10m/script.en.txt) | [Full RU](variants/10m/script.ru.txt) | 1455/1223 | `d363fd526d43dc904954007fa3aa03f0d1aad539b79c8850640e800296523118` | `d16c52781a0cc8e983932226fcb72ee7121d94f0c3f082454422301e63a637aa` |

Status: three complete texts in each language → author checks/comparison → 05m recommended; runtime/reviewer/owner/AV/demand UNVERIFIED. Root and original storyboard preserved. Next narrative #69; technical #77/#78 separately. No merge, main, production or media action.

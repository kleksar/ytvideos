# Progress addendum — 2026-11-19, PR #86 Gimli Glider

Baseline HEAD `08cfdd9782b3b94d5137edafa955f6fc48efb0df`. Full 02m and 10m EN/RU untouched. 05m EN changed from historical `88e2a0ce09e0214746b375e00ab7fe37ddf3fab3bcc4bd1bd50c532acf0fc199` to **`ea1a189be00e0b392c820557ef46ddb349183ca12608a49b59246067543b8d07`**; RU changed from `d5b88e9924a600ff25528a5e4b34a1137101678b598dfd1372b11293b9d8ff69` to **`b60bd3bb5ac4d742cde6de3ab49ba1c842ff7f9e976c629f8dad4b506e393cdc`**. Commit SHA of this change is the new PR HEAD after fast-forward.

| Stage | Before | After |
|---|---|---|
| 02m | Complete Short EN/RU, original | Preserved; [RU](variants/02m/script.ru.txt) |
| 05m | Complete but 616 EN words; safe landing followed by general commentary | **702 EN words with substantive Quintal / landing gear / evacuation actions**, full [RU](variants/05m/script.ru.txt), [EN](variants/05m/script.en.txt) |
| 10m | Complete 1587-word Long with slow inquiry ending | Preserved; [RU](variants/10m/script.ru.txt) |
| Fact register | 1985 inquiry pp.25–29 and sibling references | New source readings pp.100–102 G7–G10 |
| Assessments | Historical 05m scores/hashes | New eight-criterion EN/RU review, exact hashes and hard checks in story-review |
| Recommendation | 05m candidate | **05m still provisional**; extra events justify time, unlike 10m procedural tail |

Story chain: two falsely reassuring calculations → both engines out → Quintal's improvised glide calculations → new single-use runway → delayed gravity gear → sideslip/collapsed nose wheel → unexpectedly difficult evacuation → all 69 survive. Next unreviewed storyline: #83 May Pierstorff, only after checking its current owner/production state; #77/#78 remain technical code-review scope. No approval/independent reviewer/ytv run/TTS/MP4, no merge.

---

# Existing PR #86 progress — content rework, 2026-11-16

| Step | Before `4932f666cd3d850b71e5756083f949ea170333b1` | After (candidate commit parent `4932f666cd3d850b71e5756083f949ea170333b1`) |
|---|---|---|
| 2m | One English/Russian Short master only | Original exact text retained; copied byte-identically into `variants/02m/`; no change to original storyboard |
| 5m | Missing | Complete EN+RU 05m Long reused from exact same-story PR #137 `38425d26a3d3c44a45323b593cee9127b6568ef0`, with blob/SHA-256 provenance |
| 10m | Missing | Complete EN+RU 10m Long reused from #137 exact commit; documented weaker editorial pacing, not falsely labelled best |
| Assessment | Original self-review for Short only | Six-file manifest, eight criteria per edition, maps, pair checks and comparison in `story-review.md`; **05m Long recommended** |
| Duplicate | #137 not identified in old #86 package | Verified same Flight 143 event; cross-PR ownership explicitly documented; neither PR closed or rewritten |

**Fact evidence:** official 1985 Canadian Board of Inquiry in `research.md`, with 10m-only additions traced to #137 research and caveats. Independent source/first-listener recheck **UNVERIFIED**. Public viewer demand, MP4 and TTS **UNVERIFIED**. Git-only editorial status: `EDITORIAL_CANDIDATE_UNREGISTERED`.

**Remaining:** independent original first-listener without author scores; exact reviewer receipt on selected hash; source/owner approval or official runtime import; new storyboard for 05m/10m selection. #137 remains open and must not be produced as another release without deliberate owner choice. Next untouched story in queue after handling this same-topic pair: #83 May Pierstorff, subject to rechecking current open state and priority.

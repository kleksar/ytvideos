# Castle Itter — exact-script editorial comparison

## Scope and state

PR #22 original branch; baseline HEAD `56507c30db1b3482127998c4646f4d83b0f24164`, previous accepted-looking but **unapproved** root text blobs: EN `4504ba43a69fde8f2c953badfcaf2e4eb72cfd50`, RU `37b6890f6a817bbbfc2ac603ed73dc45ae786ebd`. Root scripts and root storyboard unchanged. Historic spoken revision below remains relevant only to those root bytes, not to these six versions.

New candidates are **EDITORIAL_CANDIDATE_UNREGISTERED** (Git-only, not a ytv script task or awaiting_script_approval). Editor's assessment only; no independent reviewer evidence, no owner approval, no production authorization.

## Full texts, exact SHA-256 and format

| Target | EN words | EN full / SHA-256 | RU full / SHA-256 | Format |
|---|---:|---|---|---|
| 02m | 228 | [02m EN](variants/02m/script.en.txt) — `419db0415c4ad3097f09322ab0d2c4d257ca4779a6dc13a7645cc860ceed8559` | [02m RU](variants/02m/script.ru.txt) — `4c589dc00d90e6fe2bf598bcd5a77fb55474032016dbc5a654b92e59076113c8` | Short 9:16 |
| 05m | 630 | [05m EN](variants/05m/script.en.txt) — `bb0e36f5560d0447211014b83346fb40f2bd1f30ae12013640f2c470331f615b` | [05m RU](variants/05m/script.ru.txt) — `73c1f602aa9d8b382aaf942a824458efae6657ff808fb6c3f3d6a7cb98ac8e6e` | Long 16:9 |
| 10m | 1281 | [10m EN](variants/10m/script.en.txt) — `0297ffcc7a735d05f8002edb1e6e7f2d4321e4d6273e9b5d0d0be6656ab6c3b6` | [10m RU](variants/10m/script.ru.txt) — `eaa27a030c98cdef3852e7583ceba07edafeb4cde1b82280d662be029e88110d` | Long 16:9 |

Hashes are for exact UTF-8 bytes including terminal newline, not normalized text. Calculated with a SHA-256 implementation checked against the standard `abc` vector and from actual staged Git blob contents. Recheck after any editorial change; all hashes and downstream checks then become stale.

At 125–150 EN words/minute before any narrator speed and pauses: 02m about 1:31–1:49, 05m about 4:12–5:02, 10m about 8:32–10:15. Short pauses/score/end elements may change elapsed runtime; actual voice at pinned channel speed and mixed MP4 are **UNVERIFIED**. The 10-second Long endscreen is additional production planning and has not been built. These are targets, not duration claims.

## Story maps (same historical event, different finished construction)

- **02m:** unusual request → threatened French political captives → Gangl contacts Lee → small convoy and one Sherman → guard reorganized → SS fire takes tank → prisoners defend, Borotra goes for help → Gangl dies → relief and survival → last first-move phrase connects to opening. Promise fulfilled before loop.
- **05m:** three concrete opening questions → French imprisonment and SS risk → Gangl and Austrian resistance → Lee personally verifies → **Lee's false overwhelming-force claim** helps clear route → bridge/position losses strip the column → Lee re-arms guards at castle → patrol, subsequent guard departure → exposed Sherman hit → prisoners join → Borotra helps relief → death of Gangl and other defenders → relief. Central causal payoff is why opposite-uniform soldiers held the gate long enough.
- **10m:** questions about alliance / only tank / destruction → prison and local resistance → Lee's reconnaissance → removal of bridge charges and bluff → armored force shrinks → guard prepares to leave → mixed defense → night patrol and morning defection → guns disable tank and strike tower → French prisoners resist → Borotra aids outside relief → Gangl killed → handoff to US infantry → limits of temporary cooperation. Additional mechanisms are documented but the account becomes more explanatory after the battle.

## Editor scores (1–10, not audience metrics)

Each number below is an author's judgment tied to the actual finished text, not independent review, predicted retention, or evidence of audience preference. Confidence is **medium** for factual/structure checks, **low** for interest and attention. The eighth criterion is **UNVERIFIED**, not an invented score.

| Criterion | 02m: basis / limit | 05m: basis / limit | 10m: basis / limit |
|---|---|---|---|
| Interest / significance | **8** — former adversaries protecting captives; compressed motivations | **8** — same moral contradiction with stakes at gate | **8** — unusual military rescue; history of routes risks narrowing appeal |
| Opening | **8** — request first, clear actors; no questions-first Short requirement | **8** — asks why German officer contacted tank commander, why prisoners remain, who approaches | **8** — asks alliance, missing tanks and attack; substantial answer follows |
| Development / reason to continue | **7** — shrinking party → tank lost → rescue, little space for Lee's decisions | **9** — bluff, bridge restriction, desertion, artillery, prisoner defense and messenger each change options | **7** — more contextual steps; back half revisits familiar pressure and explanations |
| Payoff | **8** — prisoners survive and Gangl dies before they escape | **9** — rescue completes promised causal chain and individual sacrifice | **8** — prisoners alive and handoff clear; final reflection repeats some explanation |
| Angle freshness | **7** — known unlikely alliance, but human decisions | **7** — details of Lee's route/bluff distinguish retelling | **7** — added bridge charges and handoff; same well-known paradox |
| Visual expressiveness | **8** — uniforms, Sherman, gate, woods; staging still unverified | **9** — bridge, guarded roads, castle, patrol, gun line, rescue give distinct visual actions | **8** — more geography and soldiers; some repetitive exposition harder to visualize |
| Oral clarity/naturalness | **8** — short physical verbs, clear people; literal loop not independently tested | **8** — actions and consequences, one complex passage around bluff | **7** — several explanatory clauses and summarizing final paragraphs may slow oral rhythm |
| Verified audience demand | **UNVERIFIED** — no comparable public 2m baseline or owned metrics | **UNVERIFIED** — no measured CTR/retention for this cut | **UNVERIFIED** — no measured demand or retention for long expansion |

Primary limits: **02m** introduces almost no geography and the shift from rescue to reflection may feel like a restart at the second loop. **05m** is dense at the bluff/route explanation and needs first-listener testing. **10m** loses urgency around the later repeated explanation of the one tank and unusual uniforms; its final two paragraphs could be removed if actual pacing confirms it. Do not average a failed hard check into an artistic PASS.

## Separate hard checks and evidence

| Check | 02m | 05m | 10m |
|---|---|---|---|
| Both full texts / semantic EN-RU parity | AUTHOR CHECK: major, Lee, prisoners, Sherman, Borotra, Gangl, relief, risk aligned | AUTHOR CHECK: bluff is speech to Germans, not real strength; defection not proven cause | AUTHOR CHECK: same qualifications and end-of-operation handoff; no fake quote |
| Factual causality | AUTHOR CHECK with [research](research.md), **independent source review UNVERIFIED** | AUTHOR CHECK, AAR for Lee's move/bluff/night patrol/guard and battle, secondary for Borotra | AUTHOR CHECK, AAR for bridge charges, tower fire, transfer; secondary for Borotra |
| Format (current ChannelSpec) | Short supported, loop required | Long 16:9 supported, no loop required | Long 16:9 supported, no loop required |
| Cold open / complete payoff | AUTHOR CHECK: request → actual rescue & death before return | AUTHOR CHECK: questions answered by actions and rescue | AUTHOR CHECK: three opening questions answered; no Short loop |
| Literal narrative seam | AUTHOR TEXT CHECK ONLY: ending `Before these soldiers could defend the same gate, one of them had to make the first move.` → opening `A German major asked American tank crews to fight beside him against the SS.` A specific first action follows the final setup; not just repeated noun; possible unnatural restart | N_A — Long | N_A — Long |
| Two full Short cycles, genuinely independent | **UNVERIFIED** — author reread only, no independent reviewer session | N_A | N_A |
| AV seam / voice / MP4 timing | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** |
| First listener and bilingual reviewer | **UNVERIFIED** — no genuine session/response ID | **UNVERIFIED** — no genuine session/response ID | **UNVERIFIED** — no genuine session/response ID |
| Owner approval / official run | **NOT_STARTED** | **NOT_STARTED** | **NOT_STARTED** |

The original 14-scene `storyboard.json` is bound exclusively to unchanged root `script.en.txt` / `script.ru.txt` at baseline HEAD, **not** to variants/02m (different 228-word text), variants/05m or variants/10m. All script-specific timing, word spans, approvals and media artifacts for the variants are absent. None of these candidates may be silently substituted as runtime pinned master.

## Comparison and editorial choice

**2 → 5:** the extra minutes buy verified decisions and obstacles (Lee's bluff, guard disarming, dawn patrol, defecting guard, why Borotra needed to leave). This changes the answer from 'unlikely allies survived' to 'how an improvised defense held after its initial plan failed'. The precise potential slow point in 05m is the 60-tank bluff paragraph: listen to whether the numerical contrast is understood without reading.

**5 → 10:** adds bridge charge removal, longer geography and explicit castle-to-infantry handoff, but the extra exposition around collapsed German forces, flags and post-rescue summary begins to repeat information. In 10m attention may weaken after `The French detainees survived`, when the story turns from danger to recap; 05m ends nearer the consequential payoff. The 02m weakest point is the jump from minimal setup to `The next morning SS troops moved through the trees`; this may feel too fast.

**Recommendation: 05m as a Long editorial candidate**, not approval, not automatic production of three videos. If independent review prefers the sharper 02m or rejects both, retain that verdict. The 10m text is kept as a finished alternative, not deleted.

## Review and source procedure still required

No genuine `sessions.independent` reviewer response was obtained through the available connected tools. No `ytv-script-review-v1` artifact, independent session ID or owner approval is claimed. For local continuation, prepare canonical reviewer input from chosen exact script without this authored scorecard; first read opening and full script without verdict, then provide sources; get original output bound to exact SHA. For 02m reviewer must read two *entire* cycles and inspect literal seam; then bilingual fact/meaning review. Report actual outcomes. Git-only content is not official `ytv start`; use canonical pinned runtime context, `attach-artifact` and real coordinator approvals before preparing a storyboard or media.

## Historical spoken revision at source HEAD

The pre-existing root scripts had already received oral editing; no reason to rewrite them for this length comparison. They remain readable at root. Their prior author review and old storyboard are evidence of that distinct text, not a PASS for variants. See historical commit `56507c30db1b3482127998c4646f4d83b0f24164`.


---

# Historical author review — unchanged root scripts (pre-variant)

# Current spoken revision — Castle Itter

**Editorial candidate, independent review UNVERIFIED.** Exact baseline scripts, source ledger and original visual plan remain at `1c19548c0edf5898f65244ab0de08f078f84e0ec`. This wording pass follows the owner's request and the standard proposed in #35; no production approval is implied.

Removed unsupported access to prisoners' private fear and the second announcement of Gangl's death. The opening states the actual request, the middle follows vehicles, tank, rifles, messenger and ammunition, and the ending delivers rescue without a generic moral. Corrected the spoken transition from night to the **next** morning. Main events and existing source caveats remain; no new historic quote, precise casualty count or personal motive added. The new text is fourteen rather than fifteen blocks.

EN seam: `What had brought American and German soldiers to the same gate?` → `A German officer asked American tank crews to help him fight the SS.`

RU seam: `Как американские и немецкие солдаты оказались у одних ворот?` → `Немецкий офицер попросил американских танкистов помочь ему сражаться против СС.`

The question recalls an answered part of the story; cold opening has clear actors and action. A genuine independent reviewer must read both full cycles and may reject a question that sounds too editorial. The author's reasoning is not a passed audience experiment or a `ytv-script-review-v1` receipt.

Scene narration is synchronized in both languages; S014 reuses S001, while all old timings and any old exact-script reviews are invalidated. The former full art briefs can be compared at the baseline commit, not mistaken for generated assets. Actual image references, TTS, word map, MP4, visual geometry and sound/visual seam remain UNVERIFIED. No fresh historical source verification claimed in this language-only revision.

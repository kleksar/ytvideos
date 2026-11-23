# Story review — Sony BMG's CD rootkit (2026-11-23)

**Method / authorship:** authored and checked by this automation's script author, not by an independent listener. Reading was textual; no narration audio or MP4 was produced. Scores are editorial judgments, NOT CTR, retention, market forecast or probabilities. Independent reviewer, actual user attention, AV seam, live rights: **UNVERIFIED**. One self-editorial pass, no fabricated receipt.

## Exact source files and SHA-256 (UTF-8, with final LF)

| Target | EN master (path / SHA-256) | Full RU review version (path / SHA-256) | Word counts EN/RU | Estimated timing, NOT measured |
|---|---|---|---|---|
| 02m | [script.en.txt](variants/02m/script.en.txt) — `e2cd31331714d02266299f6f557c4d5ba7a4f530937a7ca00484164992ed0c26` | [script.ru.txt](variants/02m/script.ru.txt) — `91c4304649785fb182d5b26f4e18432647dbc206343d70205a8eb82186065dcd` | 254 / 218 | ~1:50–2:15 EN (115–140 wpm + pauses); portrait Short proposed |
| 05m | [script.en.txt](variants/05m/script.en.txt) — `b257f1a9f88030d9083607e5b08ded19879868cdc9c5df7a8bf0bc4dafbebfcd` | [script.ru.txt](variants/05m/script.ru.txt) — `0e5d3e7de584c54d764109e736f7a5245d0dad6e04f07dfa0fc4114666bdc767` | 596 / 470 | ~4:45–5:15 EN (120–130 wpm + brief pauses); landscape Long proposed |
| 10m | [script.en.txt](variants/10m/script.en.txt) — `a71457d92f4b3d860e7f7c1640a52762bde6b2abdfc6a27e42961daa81f8c313` | [script.ru.txt](variants/10m/script.ru.txt) — `6cfd3c16dc746b0c8daf5d47229a40f19f9be31db44ff6fd895681359da14ffd` | 1156 / 892 | ~9:10–10:15 EN (115–130 wpm + pauses); landscape Long proposed |

Estimates use spoken word ranges and small intro/pacing pauses; voice Lawrence 1.10× is **not auditioned**. Counting whitespace-separated tokens is approximate. Every script is a standalone completed story, not three differently cut sections of one file.

## Eight criteria scored separately (1–10, or UNVERIFIED)

`Interest`, `Opening`, `Development`, `Payoff`, `Angle freshness`, `Visual potential`, `Natural speech`, `Evidenced audience demand`.

### 02m — REWORK (full text, weak Short seam)

| Criterion | Author score | Exact observation / reason |
|---|---:|---|
| Interest/importance | 8 | “A music CD from a store could hide software” turns a familiar purchase into a personal-computer risk |
| Opening | 8 | Cold opener names the object, action and stakes without jargon |
| Development / stay | 8 | Russinovich's disappearing files → XCP hide mechanism → MediaMax unwanted components → unsafe removal tool |
| Payoff | 8 | FTC response plus “placed risky code on customers' machines”; the conflict is resolved rather than teased |
| Freshness | 7 | Rootkit story has several established video explainers; physical consumer-object angle is only a treatment difference |
| Visual potential | 8 | Disc/case, ordinary file list with a missing item, attempted uninstall, recall in paper/card dioramas |
| Speech naturalness | 7 | Understandable but 2m condensation compresses XCP/MediaMax distinctions |
| Evidence of audience interest | UNVERIFIED | Public video views cannot prove this version's demand, CTR, retention or audience match |

**Main defect:** literal last→first is **“Sometimes it was A music CD from a store could hide software...”**, which is not grammatical. Merely repeating the product at both ends is insufficient for a narrative loop. Author self-test **FAIL**; do not present 02m as Short-ready or a passed script gate. EN/RU endings both intentionally unfinished; same concern applies to both. Narration story itself has full payoff. Independent reviewer remains UNVERIFIED. No artificial loop marker accepted.

### 05m — STRONG_CANDIDATE; editorial recommendation

| Criterion | Author score | Exact observation / reason |
|---|---:|---|
| Interest/importance | 9 | “What if the tool meant to remove that protection makes the problem worse?” frames a second reversal relevant to anyone who uses a computer |
| Opening | 8 | Two linked questions → familiar physical CD → software installation; core incident arrives before an extended history lesson |
| Development / stay | 9 | Russinovich's find, XCP's concealment, MediaMax pre-consent installs, unsafe uninstallers: each changes the viewer's understanding |
| Payoff | 9 | Recall/FTC settlement and the line “It was who controlled the machine” completes the ownership question |
| Freshness | 7 | Historic case with other public explainers; new paper-medium framing is untested, not a novel discovery |
| Visual potential | 9 | Physical disk and computer, vanished paper file slips, overlapping remove/fix panels, recall shelf/settlement—distinct scene states |
| Speech naturalness | 8 | Defines unfamiliar terms through effect on a buyer, then “These were two different pieces of software” prevents conflation |
| Evidence of audience interest | UNVERIFIED | Sparse and noncomparable publicly indexed videos; own analytics unavailable |

**Main defect:** XCP and MediaMax technical names can still slow a casual viewer; narrator's 5m estimated length must be measured before production. **Confidence:** medium on editorial merit, high on underlying event sourced to USENIX/FTC, low on predicted audience performance. Two-person independent review NOT performed. Long format is allowed by the Paper ChannelSpec but real runtime script gate/approval unavailable.

**Exact story map:** familiar physical purchase → computer changed by installer → surprise XCP concealment → second system weakens consent → removal itself dangerous → recall and federal agreement → resolved question of computer ownership. Full payoff in the spoken story, not an end card.

### 10m — REWORK for pace (full text with new sourced detail)

| Criterion | Author score | Exact observation / reason |
|---|---:|---|
| Interest/importance | 9 | Three opening questions establish concealment, unwanted installation and dangerous cleanup |
| Opening | 8 | Clear consumer dilemma; first major discovery only after explaining buying/copying context |
| Development / stay | 8 | Adds autorun, RootkitRevealer mechanism, the `$sys$` prefix, MediaMax telemetry, security vendor response, separate state/federal action |
| Payoff | 8 | Returns to the physical CD case and explains the ownership/consent failure |
| Freshness | 7 | Same well-documented scandal; lengthy technical recap may overlap generic DRM videos |
| Visual potential | 8 | Wider stages possible but legal paragraphs risk a run of generic papers and computer screens |
| Speech naturalness | 7 | The last third lists institutions and settlements, with a likely attention dip |
| Evidence of audience interest | UNVERIFIED | No matched 10-minute creator baseline, real audience or analytics |

**Main defect:** after the uninstall reversal, another block of technical and regulatory context dilutes momentum. It does add verified differences from 05m, so it is a **complete long script**, not padding copied word for word; still less strong as current production master. **Confidence:** medium on accuracy subject to fact review, medium-low on entertainment value, very low on audience demand.

## Length comparison and selection

**2 → 5:** five-minute version uses room for ordinary purchase and why autorun matters, gives the researcher a causal entrance, differentiates XCP/MediaMax, and develops the risky-uninstaller surprise before regulatory resolution. 2m cannot supply these naturally and currently fails its literal Short seam.

**5 → 10:** longer version makes genuinely new observations: how RootkitRevealer found hidden items, generalized filename concealment, effects of refusing EULA, reported listening data, responses by Microsoft/EFF and different 2006/2007 settlements. Those are source-supported and material, but not every added paragraph changes the central question. The 10m legal portion can lose a first-time viewer. No automatic preference for length.

**RECOMMEND 05m EN `b257f1a9f88030d9083607e5b08ded19879868cdc9c5df7a8bf0bc4dafbebfcd`.** This is **authorial recommendation only**, not owner master selection or runtime approval.

## Independent validity checks

| Check | 02m | 05m | 10m | Limit |
|---|---|---|---|---|
| Core documented event/numbers/causality | Author PASS | Author PASS | Author PASS | Independent fact verification still UNVERIFIED; primary research USENIX + FTC; no unverifiable infection counts |
| Complete EN + full semantic RU | Author PASS | Author PASS | Author PASS | Same mechanisms, legal caveats and outcomes; review of precise complete texts, not machine diff |
| Format | PROPOSED Short, compatibility UNVERIFIED | ChannelSpec Long supports, runtime UNVERIFIED | ChannelSpec Long supports, runtime UNVERIFIED | Length after recording unmeasured |
| Narrative loop | FAIL: literal grammar | N_A (Long) | N_A (Long) | MP4 boundary always UNVERIFIED |
| Rights / real reference assets | UNVERIFIED | UNVERIFIED | UNVERIFIED | No source video, CD artwork or brand reference bytes used |
| Independent review `ytv-script-review-v1` | UNVERIFIED | UNVERIFIED | UNVERIFIED | Tool/session unavailable; author self-check is not a receipt |
| Voice and physical timing | UNVERIFIED | UNVERIFIED | UNVERIFIED | No audio rendered or listened |
| Production approval | NONE | NONE | NONE | No runtime run/lease/source script gate / owner approval |

**Reviewer handoff:** supply exact 05m EN and RU files by SHA **without** this evaluation or beat map. First request the opening expectation and full cold read; then give source material and strongest alternative (Max Headroom). Do not copy author grades into the prompt or fabricate output.

## Revision accounting and limits

This initial package uses one authorial composition/editing round; no independent reviewer revision round used. 02m seam failure is explicitly an outstanding REWORK, not silently promoted to STRONG_CANDIDATE. A real independent review of any changed hash must be repeated. No storyboard spans from this text can be reused for a different version.

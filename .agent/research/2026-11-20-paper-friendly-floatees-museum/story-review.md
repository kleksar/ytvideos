# Editorial review — Friendly Floatees
EDITORIAL_CANDIDATE_UNREGISTERED
Date 2026-11-20. Reviewer: author/self-review only, not independent. Confidence: medium on editorial scoring, high on museum/specimen and original paper, low on audience demand. Source main 09fa62d02a85f5fdcbfcc73c5acb2dcbe99aa035.

## Exact scripts and SHA-256
- [02m/script.en.txt](variants/02m/script.en.txt): **268 words**, SHA-256 `af8dd990093a4fd954b5d6441b9322a13988de3ef35004a1a7dded2accf0c5af`
- [02m/script.ru.txt](variants/02m/script.ru.txt): **232 words**, SHA-256 `7cc8bf94a82f5d6030673f72dc452a229b55dadc00cb9bc585c3c55d043736b1`
- [05m/script.en.txt](variants/05m/script.en.txt): **688 words**, SHA-256 `b377a41851ec701a5a7f6d7046845b462f652604eb8f005ded3a4c32a18a6f66`
- [05m/script.ru.txt](variants/05m/script.ru.txt): **586 words**, SHA-256 `c24586789b4730ea6c228aac4745f27f2cb6993b1a1ce6b0f8fe735fdba3a8e6`
- [10m/script.en.txt](variants/10m/script.en.txt): **1714 words**, SHA-256 `3c5a0901ca89be975165fe9291eb54e376aca2697d9c9813684b542016f6d45a`
- [10m/script.ru.txt](variants/10m/script.ru.txt): **1463 words**, SHA-256 `9da9436f626f21257822e86f421c600231866346821565592e33866c6f59f4e0`

## Format and estimates
- 02m: proposed Short; 268 EN words at assumed ~140-165 wpm and modest pauses suggests ~1:50-2:20 before actual TTS. Paper narrative loop required. **Loop FAIL (author):** final sentence returns to the Alaska duck but does not flow into the opening as uninterrupted speech; must REWORK before script gate. AV seam UNVERIFIED.
- 05m: proposed Long; 688 EN words at ~140-165 wpm plus small breath/visual pauses suggests roughly 4:25-5:15; exact Lawrence 1.10× production duration UNVERIFIED.
- 10m: proposed Long; 1714 EN words at ~140-165 wpm plus small pauses suggests about 9-11 minutes (estimate only). The dense scientific explanation risks dragging. Exact duration UNVERIFIED.
- Paper Detour ChannelSpec allows short and long; long has a 10-second end-screen production requirement. No end-screen media target/intro verified in this Git-only draft.

## Individual eight-criterion scores (1-10 author judgment, not analytics)
Each row applies to exact EN and meaning-equivalent RU text at the linked hash; audience-demand score is UNVERIFIED, not a synthetic 8. Criterion order: importance/interest; opening; development; payoff; angle freshness; visual potential; spoken clarity; verified audience demand.

| Variant | Interest | Opening | Development | Payoff | Freshness | Visual | Speech | Demand | Classification |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 02m | 8 | 8 | 8 | 7 | 6 | 8 | 8 | UNVERIFIED | REWORK |
| **05m** | **8** | **8** | **9** | **9** | **7** | **9** | **8** | **UNVERIFIED** | **STRONG_CANDIDATE, recommended** |
| 10m | 8 | 8 | 8 | 8 | 7 | 9 | 7 | UNVERIFIED | REWORK (overlong explanatory middle) |

### Exact observations / chief weakness per version
02m: Interest=8 because “A yellow bath duck washed onto an Alaskan beach” is an immediately graspable incongruity; opening=8, visible beach object before jargon; development=8, ten-month wait then model-versus-find; payoff=7, museum object established but the ending repeats the beach rather than transforming the question; freshness=6, BBC and TED have similar central fact; visual=8, 4 toy shapes and map against tactile scene; speech=8, ordinary terms, some scientist names; demand UNVERIFIED (SciShow episode roughly 0.88× its immediate previous comparator, not controlled evidence). Main blocker: literary return is NOT a genuine Short loop. Author only; no independent observation. Format/loop FAIL; facts PASS within sourced claims; translation PASS author check; rights UNVERIFIED until media; independent UNVERIFIED.

05m: Interest=8 because museum specimen is physical payoff; opening=8, exact three questions with concrete answer destinations; development=9, lost cargo -> 10-month gap -> shoes precedent -> drift-model test -> uncertain Arctic accounts; payoff=9, “The proof is not a perfect map of a toy's entire voyage. It is a small yellow duck ...”; freshness=7, well-known story but focuses on limits of evidence and actual museum specimen; visual=9, container/storm/toys/Sitka shoreline/museum record provide changing compositions; speech=8, explanation of model is short and intelligible but opening must survive actual voice; demand UNVERIFIED, competing TED/BBC evidence is evergreen not fresh appeal. Main weakness: midpoint modelling paragraph must be checked by first listener; no measured retention. Author only, medium confidence. Facts PASS author/primary-source cross-check; EN/RU meaning PASS author comparison; format PASS proposal; loop N_A Long; rights UNVERIFIED; independent UNVERIFIED.

10m: Interest=8, case retains curiosity and real museum destination; opening=8, asks origin/long travel/evidence; development=8, explains shoes, modeling, geography, beachcomber reporting, arctic uncertainty and verification; payoff=8, exact science insight “The toys didn't measure the ocean. People measured where the toys ended up”; freshness=7, evidence-quality angle differs from familiar duck montage; visual=9, multiple tactile maps/objects/museum scenes; speech=7, extended modelling and several qualifications risk sounding like lecture; demand UNVERIFIED. Main weakness: the passage about what models can/cannot infer after the science museum reveal slows the final third. Author only, medium/low confidence. Facts PASS on verifiable events, model boundaries author check; meaning-equivalent translation PASS author comparison; format PASS Long proposal; loop N_A; rights and independent review UNVERIFIED. REWORK is not a claim that 10m is factually wrong.

## Story map, exact events and interest leakage
02m: Alaska duck -> ship lost toys -> beach find -> models/1990 shoes -> limitation -> actual museum duck -> thematic return. Likely losing viewers at second restatement of model limitations; failed Short loop.
05m: Questions -> spill + not-all-ducks correction -> arrival after ten months (main hook) -> shoes precedent -> how models are tested -> why Arctic claims require caution -> museum object + persistent plastic -> answer. Possible drop in long explanation of observation bias; otherwise self-contained and finished.
10m: Questions -> physical museum teaser -> 1992 spill -> container damage uncertainty -> 1990 shoe precedent -> toy arrivals -> model-vs-find -> wind/reporting uncertainty -> doubtful distance claims -> 1994 publication -> citizen reports -> museum objects/faded beaver -> interpretation limits -> pollution -> final distinction. Likely drop after museum reveal when explanations continue; fix only if truly new evidence is available.

## Compare actual texts rather than topics
From 2 -> 5: additional value is why the scientists already had a testable model, who supplied observation and why distant-route legends are not equal to a found specimen. 5 completes the museum mystery without circling the question. From 5 -> 10: expanded methodology, 1994 publication, reporting bias, a faded real beaver and scientific reasoning, but it costs pacing, especially after the payoff. **Recommend 05m only**, not because long is inherently preferred; it retains physical artifact payoff and has a more substantive development than 02m. No version approved by owner.

## Independent verification
No actual second model/session reviewer was available through the current GitHub-only context; self-review explicitly cannot replace ytv-script-review-v1. No reviewer receipt, reading input generated by canonical helper, run, lease, approval or TTS exists. To continue: on runnable checkout use `uv run ytv start --channel paper_detour --format long --intent 'produce verified Friendly Floatees variant from editorial PR'`; read returned pinned documents and register exact chosen text/variants per task contract; do not overwrite existing runs. Independent blind first listener should receive only exact 05m EN text first; evidence source list afterwards. If text changes, sha and review must change.

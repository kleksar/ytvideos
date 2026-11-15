# Search-first evergreen strategy — this THREE-story editorial slate

**Scope:** only the three candidate scripts in this PR. Not a change to canonical docs, production gates, channel formats or upload policy. Observed 2026-11-15. Hypothesis: some catalogue videos can attract continuing YouTube Search visits many months after release. The owner scenario of 500 videos and 5–10% evergreen contributors implies 25–50 contributing videos, **not a demonstrated conversion rate, guaranteed monthly views or monetization**.

## Selection process and explicit gates

1. Identify a persistent, explicit **viewer question**, not an interesting fact or a famous event. Query prompts were worded as people might type: `why were titanic lifeboats half empty`, `who destroyed the library of alexandria`, `why did chernobyl explode when they pressed az-5`. We have **not** measured whether these are the exact queries viewers currently submit. Alternatives in each research.md.
2. Test whether a complete short/medium/long answer has real progression: first contradiction → successive verified causes/evidence → answer with limits. The answer must actually match the search query; do not conceal it for watch time or stretch a simple fact to a target length. Query determines title/intro; verified development determines final length.
3. Search YouTube for multiple authors and both strong and normal/weak videos **of a similar format and age on the same channel**. Capture URL, publish and observation dates, language, duration and public views with provenance. At present the direct same-author baseline for every example is n=0; all demand in story scorecards stays **UNVERIFIED**. Public views do not show Search traffic source, search ranking, CTR, retention, estimated revenue or current velocity.
4. Avoid direct topic/angle duplication with the current main tree, existing production runs, open/closed PR titles and owner rejections; check remote again immediately before write. Search titles avoid keyword stuffing and answer a concrete human question. The film's first sentences confirm that promise; metadata can link to source material once script is accepted. Actual packaging/thumbnail needs its normal independent approval and QA.
5. After *future authorized publication*, measure 7/28/90/180-day results of **YouTube Search** separately from Home/Browse/Suggested, with top observed query strings, search impressions where provided, watch time, retention, audience geography, revenue/RPM only when explicitly returned, and comparable video-age cohorts. After sufficient uploads, rank long-tail monthly views by episode and identify whether they remain recurrent or are one-time search spikes. Do not infer evergreen success from lifetime view counts.

## Selection table — hypotheses, not search-volume measurements

| Video | Search question | Value after hook | Main counter-signal | Current evidence |
|---|---|---|---|---|
| Titanic ~2m | Why were lifeboats half empty? | Failed loading PLUS total capacity insufficiency | Very crowded historical topic | public YouTube titles, UNVERIFIED search volume |
| Alexandria ~5m | Who destroyed the library? | Contradictory source traditions and slow institutional loss | Existing strong long explainers | independent public videos, UNVERIFIED matched baseline |
| Chernobyl AZ-5 ~10m | Why did emergency stop make it worse? | Feedback physics + rods' first movement + history of design knowledge | Technical density and major existing explainers | public examples, actual expert sources, demand UNVERIFIED |

## Revenue model and hard limitations

Search-oriented catalogue is a **diversification hypothesis**, not a policy that every upload must be search-only. Revenue requires actual YPP eligibility/active monetization, eligible traffic and real RPM data. A catalogue can be 500 uploads yet produce few search impressions or views. A regular cohort readback, and ideally a comparison against equally aged recommendation-first videos, is required before changing allocation based on this hypothesis. Zero available vidIQ credits means no paid keyword queries and no credits have been purchased for this MR.

No user approval for media, release, merge or changing a channel status is implied.

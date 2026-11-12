# Paper 044 — expanded hashtag proposal

Status: applied and verified by YouTube API read-back on 2026-11-03; exact write receipt is `HASHTAGS_UPDATE_RECEIPT_v01.json`.

## Current YouTube baseline

Before the update, a fresh authenticated Data API read verified channel ownership and video `Y_TB6r4jI9I`. Title: `Even Coming Home Meant 30 Days of Waiting`; the user identifies it by the `SO CLOSE TO HOME` cover. The description had five hashtags; title had none:

`#Ragusa #Quarantine #History #Shorts #PaperDetour`

The separate YouTube Tags field includes Black Death and Dubrovnik; those plain keyword entries do not establish corresponding hashtags in the description. Exact baseline: `HASHTAGS_BASELINE_20261103_v01.json`.

## Proposed complete selection

Preserve the five existing tags and add 31, for 36 total. Exact full block: `HASHTAGS_DESCRIPTION_BLOCK_v01.txt`; each addition and its content basis: `HASHTAGS_PROPOSAL_v01.json`.

| Direction | New hashtags | Content basis |
|---|---|---|
| Place | #Dubrovnik #DubrovnikHistory | Explicit modern name of Ragusa. |
| Period/context | #MedievalHistory #MiddleAges #14thCentury #EuropeanHistory | The rule in 1377 and medieval city setting. |
| Plague | #BlackDeath #Plague #PlagueHistory #EpidemicHistory #PandemicHistory | Named Black Death context and arrivals from plague-affected places. |
| Quarantine/public health | #QuarantineHistory #OriginsOfQuarantine #PublicHealth #PublicHealthHistory #MedievalPublicHealth #DiseasePrevention #PlaguePrevention #DiseaseControl #Isolation #TravelRestrictions | Required separation, reduced contact/risk, restrictions on arrivals including returning residents. |
| Medical history | #MedicalHistory #HistoryOfMedicine | Historical prevention before knowing the causal bacterium. These are both observed labels for the field, not treatment advice. |
| Trade/port | #MedievalTrade #MaritimeTrade #TradeHistory #MaritimeHistory #PortCity | The narration expressly explains keeping trade going at a dependent port. |
| Language | #Etymology #WordOrigins | The last sentence explains the origin of quarantine. This direction was absent from the consultant pool. |
| Format | #HistoryShorts | The subject and short-form format together. |

The 36 count is an outcome of this selection, not a target or proved optimum. No promise of increased reach follows from adding tags. Source content was the accepted retained-narration transcript; it remains machine-derived. No new listening, film playback or scene-by-scene review is claimed.

## Significant exclusions

- #COVID19, #Coronavirus, #DubrovnikTravel, #CroatiaTravel: different events/viewing purposes absent from this story.
- #YersiniaPestis, #BubonicPlague, #Lazaretto: named organism, clinical subtype and facility specifics are not developed in the accepted narration; do not add precision that the film does not establish.
- #Homecoming, #Waiting, #SoCloseToHome: dramatic wording does not identify the historical subject; these are broadly ambiguous.
- #Food, #Cooking, #HumanitarianAid: the line about needing food/support does not make this a cooking or aid-organisation story.
- #1377: a bare number has no historical subject qualifier and is ambiguous; the dated context is represented by #14thCentury. This exclusion concerns meaning/utility, not an assumed lack of demand.
- #30DayIsolation, #30DayQuarantine: descriptive restatements of the central rule rather than additional topic coverage; keep the exact thirty-day detail in the narrative description. Unobserved demand alone is not grounds to reject an otherwise useful tag.
- #40DayQuarantine: risks confusing the later forty-day explanation with the rule at the centre of the video.

## Usage research and limits

Consultation completed personally in visible Chrome Extra High; exact prompt and response in `CONSULTATION_HASHTAGS_v01.md`. This is advice, not source or demand evidence.

Public English web searches were actually run on 2026-11-03. Initial site-restricted combinations returned no results; broader exact-hashtag queries produced the observations below. Direct web opens of YouTube watch pages failed/throttled, so indexed results are not labelled as pages watched or opened. Market-specific Studio Trends, search volume and trend direction were not measured.

| Exact usage | Observed source | Evidence type |
|---|---|---|
| #BlackDeath #MedievalHistory | https://www.youtube.com/watch?v=X4kZJVnY-i0 | YouTube video description exposed in search result. |
| #Etymology #WordOrigins | https://www.youtube.com/watch?v=tKjGOPL4rVQ and https://www.youtube.com/watch?v=nAezO7L0oo8 | YouTube titles exposed in search results, case-insensitive matching. |
| #MedicalHistory #HistoryOfMedicine | https://www.linkedin.com/posts/drnareshchauhan_historyofmedicine-medicaleducation-mbbs-activity-7511413985317916672-ygPu | Author's own post using both tags and linking https://youtu.be/Q0DdXM3CWXg; not verified as that video's description. |

Focused queries also checked #QuarantineHistory, #OriginsOfQuarantine, #MedievalPublicHealth, #PublicHealthHistory, #Ragusa/#Dubrovnik/#Quarantine, #PlagueHistory, #EpidemicHistory, #PandemicHistory, #MedievalTrade, #MaritimeTrade and #DubrovnikHistory. No sufficiently strong direct YouTube usage evidence was established for these exact labels during this pass; broader/other-platform hits do not establish YouTube demand. Remaining added tags are content-based selections, with usage unestablished on YouTube and demand `unknown`, as recorded per tag in JSON. This does not prove absence of use.

## Platform policy

Official YouTube help opened and read on 2026-11-03: https://support.google.com/youtube/answer/6390658?hl=en. Hashtags must directly relate to the content; over-tagging is discouraged independently of the numeric threshold. More than 60 causes all to be ignored. Up to three displayed above the title is not a three-tag limit. Count across actual title and description: 36 proposed occurrences, no duplicates. Being below 60 is not a performance or quality certificate.

## Handoff

YouTube read-back confirms the complete proposed hashtag block in the description. The narrative text and title are unchanged; the separate video Tags field still has six entries; privacy remains Unlisted. Current metadata is `upload_v02.json` and live snapshot is `HASHTAGS_BASELINE_20261103_v02.json`. No video file or thumbnail was changed. Usage evidence is partial; exact-tag demand is unknown. The general behaviour is maintained in the canonical hashtag skill, not copied from this episode into a universal tag list.

# 032 Galveston — A/B experiment current state (2026-11-03)

## Lifecycle
**active**. The previous saved-state note was stale: on the user's report that the test had been canceled, a fresh Studio inspection opened a new A/B setup form with no active report. The native test was reconstructed from the approved three-pair manifest, saved, and verified running on 2026-11-03. See [restart receipt](AB_RESTART_RECEIPT_20261103.md).

## Target and before-state
- Channel: Paper Detour, UCMVfdfaNxV3ZkI3_J3Eejzw.
- Video: [Galveston: The City That Raised Its Ground](https://www.youtube.com/watch?v=lRkxm3mij5o), lRkxm3mij5o.
- Current title: Galveston: The City That Raised Its Ground.
- Current thumbnail lettering: WHERE'S THE GROUND?; visually confirmed in Studio.
- API read on 2026-11-03: privacy public, upload status processed, processing succeeded, no failure/rejection reason. Read-back: ../Metadata/ab_test_target_status_20261103.json.
- Fresh pre-write Studio state: the create form was open with the current title/thumbnail as option 1 and no active test report. Account/channel was switched explicitly to Paper Detour before writing.

## Contract
- Test type: title_thumbnail_pair; three paired variants. It compares each title/image combination as a package, not the separate effect of title or image.
- One question: Which truthful framing of Galveston's post-hurricane rebuilding earns the strongest watch-time share: the overall raised-city story, the church-lifting method, or the raised-street transformation?
- Primary metric/method: YouTube native concurrent test and its watch-time-based selection. CTR can be read as context only; it is not the winner rule.
- Description: hold the existing complete description unchanged for every variant; descriptions cannot be tested in the native interface.
- Stop/result: let YouTube complete its native test (up to two weeks as described in Studio). Do not manually stop or choose a winner from a transient lead. Preserve the raw platform outcome; if there is no clear winner, the first submitted option becomes default. No recurring check configured.
- Start authorization: user confirmed on 2026-11-03 after being told native A/B excludes descriptions.

## Exact variants
| Option | Title | Thumbnail |
|---|---|---|
| 1 / baseline | Galveston: The City That Raised Its Ground | Existing current Studio image, WHERE'S THE GROUND? (the original full-size local image was absent at preflight; current Studio rendering is verified) |
| 2 | How Galveston Lifted Buildings After the 1900 Hurricane | HOW DID IT RISE? — church on screw jacks and timber cribbing; [master](../Thumbnails/AB_20261103/variant_b_church_lift_master.png), [Studio upload](../Thumbnails/AB_20261103/variant_b_church_lift.jpg), [320x180 preview](../Thumbnails/AB_20261103/qa_b/qa_full_320x180.jpg) |
| 3 | Galveston Built a Seawall — Then Raised Its Streets | THE GROUND ROSE — house on an elevated grade with former grade shown below; [master](../Thumbnails/AB_20261103/variant_c_raised_grade_master.png), [Studio upload](../Thumbnails/AB_20261103/variant_c_raised_grade.jpg), [320x180 preview](../Thumbnails/AB_20261103/qa_c/qa_full_320x180.jpg) |

## Editorial / visual checks
The two generated alternatives are historical illustrations, not documentary photographs. The church concept limits lifting to the building; the raised-grade concept shows earth and street level rising, not the whole city lifted. Exact lettering and the full 16:9 composition were visually inspected, then both JPG uploads were checked at 320x180. Native source images are 1672x941. Studio's upload spec in the A/B dialog: 1280x720, JPG or PNG, max 50 MB; uploads retain native 16:9 ratio and are below the file-size limit. Live destination A/B report preview confirms all three uploaded covers and their paired titles.

## Execution
Studio native capability is the justified UI route; project API documentation records no public Data API A/B endpoint. In Studio, title-and-thumbnail mode is selected and the two exact alternate title fields are filled. The user attached the two image files and saved the test in Studio. Fresh Studio read-back shows the active native experiment and all three paired title/thumbnail variants. The active report is open; this is the first-option baseline if the platform reports no clear winner.

## Consultation
A ChatGPT.com consultation was made while the visible mode label was Extra High in the existing browser chat. It returned the two alternate titles above and factual pair rationales. The input was visibly mangled by the browser text-entry layer, so consultation output is retained as ideation only; the exact titles and image claims were independently checked against accepted episode materials. Chat URL: https://chatgpt.com/c/6ae943b7-fdc4-83ed-8d22-0e0d065fa562.

## Evidence and limitations
Generated masters, uploads, and previews are preserved under ../Thumbnails/AB_20261103/. Helper manifests record preview dimensions/source hashes. API ownership/visibility/processing read-back is separately saved. The active Studio report is direct evidence of the saved test. No experiment ID was exposed in the report.


## Native restart read-back — 2026-11-03

Studio Reach report header: “A/B-тестирование”. Raw status: “Тестирование…” (Testing…). Studio lists all three exact thumbnail/title pairs, including the baseline cover, church/jacks cover, and raised-grade cover. Each watch-time-share value is “–”; record as unavailable, not zero. Studio estimates 13 days 23 hours remaining at read time. The existing description was visible unchanged in the Studio details page. No winner selected and no manual stop made.

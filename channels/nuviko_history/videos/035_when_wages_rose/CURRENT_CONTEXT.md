# Current context — 035

Updated 2026-11-02.

## Scope

- **Channel / format:** Nuviko History, English long film, 16:9; target 8–10 minutes.
- **Provisional title:** *How Many Days' Wages Would Cover the Basics?*
- **Provisional central question:** How much work, measured in days' worth of wages, did it take to cover a reconstructed basket of basic necessities in different periods of English history?
- **Working story spine:** concrete necessities and pre-Black-Death basket equivalent (~333 wage-days) → post-plague struggle over wages, evidenced by the 1351 statute → fifteenth-century earnings generally above the modeled poverty line (no exact days claimed) → 1500–1549 equivalent (~176) → prediction after daily silver pay more than doubles → 1600–1649 equivalent rises to ~216 because prices rose faster → 1850–1899 equivalent (~116) → return to goods and a day's purchasing power.
- **Primary evidence:** Robert C. Allen, “The Great Divergence in European Wages and Prices from the Middle Ages to the First World War,” *Explorations in Economic History* 38 (2001), 411–447, DOI: https://doi.org/10.1006/exeh.2001.0775; readable copy: https://web.mit.edu/14.731/papers/greatdivergence.pdf.
- **Source limits:** Allen's welfare ratio is a model built from assumed annual income and a reconstructed basket, not an observed family budget. It uses 250 workdays per year, a notional man/woman/two-children household, and a 5% minimum rent allowance. Claims and exact locations in the paper are in `Source/Research/claims_and_sources.md`.
- **Model-consultation records:**
  - `../../../.agent/consultations/20261102-history-editorial-promise.md`
  - `../../../.agent/consultations/20261102-history-cost-of-living-angle.md`
  - `../../../.agent/consultations/20261102-history-cost-of-living-structure.md`
  - `../../../.agent/consultations/20261102-history-price-wage-reversal.md`
  - `../../../.agent/consultations/20261102-history-labor-days-angle.md`
  - `../../../.agent/consultations/20261102-history-script-v02-factcheck.md`
  - `../../../.agent/consultations/20261102-history-script-v02-story-review.md`
  - `../../../.agent/consultations/20261102-history-script-v03-rewrite.md`
  - `../../../.agent/consultations/20261102-history-visual-score.md`
- **Current script:** `Source/Scripts/film_en_v06.md` — 1,050 spoken words; `Source/Scripts/film_ru_review_v06.md` — corresponding Russian review text. Applies the user's approved direct opening without the confusing technical introductory phrase. Accepted story basis remains v04; the four-person family, three-quarters of the annual bill, 333 daily payments required and 250 paid days assumed are preserved. Only narration paragraph P02 changed from v05 in each language. Prior versions are preserved. Acceptance: `Source/Scripts/ACCEPTANCE_v04_20261102.md`; editorial changes including v06: `Source/Scripts/EDITORIAL_UPDATE_v05_20261102.md`. Runtime remains an estimate until actual voice.
- **Visual score:** `Storyboard/VISUAL_SCORE_v03.md` — current complete proposal synchronized with v06, without researcher cards. Twenty-four meaning-based sequences cover all 39 narration paragraphs; `Storyboard/COVERAGE_v03.json` stores the ordered mapping and current-script SHA-256. No separate acceptance or cold-viewer test of the score is claimed. This is a planning document, not generated images or an edit.
- **Storyboard:** `Storyboard/STORYBOARD_v01.md` — first concrete shot plan for all 24 score sequences, linked in order to P01–P39. Specifies framing, graphics, transitions and host continuity. It does not alter the narration. Period details not covered by the three image drafts still need item-level checking. No independent review or cold-viewer test is claimed.
- **Visual references/specification:** `Storyboard/VISUAL_REFERENCES_v01.md` — checked museum/archive item references, future asset roles, composition constraints and open evidence gaps for pre-plague, Tudor and Victorian visuals. It identifies which sequences can stay as native graphics and flags that no 1600–1649 scene is presently needed. No images were generated or reused; media rights are not assumed.
- **Image tasks:** `Storyboard/IMAGE_TASKS_v01.md` — prompts for the undated necessity still-life, optional low-detail Tudor London skyline, and generic late-Victorian London construction scene; the pre-plague worker reconstruction is explicitly replaced by a neutral native-design map card until better evidence is found. Text/number cards remain vector work.
- **Image drafts:** `Source/Images/IMG-02_necessities_still_life_v01.png`, `IMG-05_tudor_london_panorama_v01.png`, and `IMG-07_victorian_worksite_v02.png` were generated with built-in `image_gen` and copied into the episode workspace. First visual inspection and provenance are in `Storyboard/IMAGE_QA_v01.md`. These are drafts, not user-accepted final images. Medieval workers, 1351 document graphics, data cards and other charts were not generated.
- **Current check:** all 47 current score quotation anchors match v06; coverage has no gaps or overlaps, and claim IDs resolve. Only P02 changed in each language; historical data, calculations and remaining narration are unchanged. Source/editorial review of the earlier factual basis remains in `Source/Research/SCRIPT_v03_CHECK_20261102.md`. Three image drafts received an author visual review; no independent historical review, cold-viewer test, or in-film review has been completed. Fine costume/tool detail remains open.
- **Earlier versions and external attempts:** v01 and v02 are preserved. v02 (1,191 words) remains unaccepted. The user supplied the Thrinaxodon and clothing-history threads as presentation examples only. The earlier Extra High v03 attempt produced only a partial response and no complete saved script; it is distinct from the complete locally authored v03 candidate. The factual audit and story review of v02 and visual-score attempt for v01 did not return visible complete assessments/deliverables. Their limitations remain in the consultation records above; none is represented as a review of current v03.

## Permissions and next gates

- The user asked to develop and make a film on the topic. This authorizes project-local research, story, script, and later production planning within channel rules.
- Latest user instruction, 2026-11-02: «Короче, я улучшил модельку, давай продолжать сами без чата.» Continue this episode here without external ChatGPT.com consultations. This episode-local override supersedes the mandatory consultation procedure for this ongoing work; project-wide rules are unchanged.
- Latest editorial instruction, 2026-11-02: «А, теперь понял. Давай так и объясним в сценарии, чтобы зритель тоже не запутался. Внеси эту правку, и можно переходить к визуальной партитуре.» Requested change completed in accepted v04; authorized separate visual score v01 is complete. No repeat textual acceptance is needed. No image generation or editing has begun.
- Subsequent general instruction: omit unnecessary researcher/scientific-publication mentions from all stories. Canonical owner is root `AGENTS.md` §11. Applied to this episode in v05 and visual score v02; no new acceptance request for the directed wording edit. Internal source attribution and factual limits remain intact.
- Latest clarity instruction: apply the approved direct opening, read the current documentation before changing rules, and fix shared standards and dependent files together. Completed in v06 / score v03 and root AGENTS §§10–11. No renewed acceptance gate is introduced.
- Latest image-generation instruction, 2026-11-02: «го дальше» after the proposed image-generation/review stage. This authorized separate generation of the three selected still-life/Tudor/Victorian draft assets from `IMAGE_TASKS_v01.md`; completed with built-in `image_gen` and documented in `IMAGE_QA_v01.md`. The user has not yet accepted any generated image as final.
- No new audio has been authorized. Ask separately when the episode reaches voice/audio production.
- No upload, public release, or schedule is authorized.

## Next action

Review the image drafts and decide whether IMG-02/05/07 should be retained or revised. If retained, the next separate stage is constructing/assembling the native graphics and fitting scene assets into the film plan. Do not reintroduce research-author cards or scientific-source narration. New audio still requires separate direct authorization. No upload or public release is authorized. Continue here without external ChatGPT.com consultations.

# Extra High consultation — semantic one-line caption boundaries

- Date: 2026-11-04
- Channel/episode: Paper Detour / The Last Voyage of the Edmund Fitzgerald
- Visible model label before each request: Extra High
- Browser: Google Chrome, project chat “Английская адаптация narration”
- Chat URL: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6aeb35d8-a6dc-83ed-894f-b0bdc5458074
- Scope: assess only 11 auto-generated one-line grouping boundaries. Narration, story, word order, and claims remain unchanged.

## First request and response

The task asked the consultant to assess 11 exact pairs from the renderer's `boundary_warnings`, recommending whether to keep or move each caption boundary. It required no change to narration and preservation of Paper's one-line safe width and exclusive yellow-word highlighting.

Recommendations: keep pairs 1, 2, 4, 5, 7, 9, 10, and 11; move pair 3 to `located the wreck / at a depth of about 160 meters.`; move pair 6 to `Guard concluded that / water had probably been entering`; move pair 8 to `In its theory, / water may also have been building`. The consultant noted that moves 6 and 8 still required actual renderer-width checks. Pair 7 was retained despite the forced continuation into `watertight.` because no safer alternative was supplied in that response.

## Width verification and follow-up

The actual Paper geometry is Chalkboard SE TTC index 2 at 84 px, with 1344 px maximum text width. Exact PIL raw glyph measurements (renderer safe glyph width is 1298 px; 1344 px is the full visible envelope) showed: `at a depth of about 160 meters.` = 1337.6 px (fits); `The United States Coast Guard concluded that` = 1903.6 px (does not fit); `water had probably been entering` = 1381.8 px (does not fit); `that were not sufficiently watertight.` = 1549.4 px (does not fit); `that has never been fully reconstructed.` = 1657.8 px (does not fit); `while the stern was upside down.` = 1348.0 px (does not fit).

A second narrow request was submitted with the measured safe width to resolve only the long Coast Guard clause, `that were not sufficiently watertight`, the NTSB theory caption, and the final relative clause. The completed follow-up recommended: (6) `The United States Coast Guard / concluded that / water had probably been / entering the cargo hold / gradually through hatch covers / that were not / sufficiently watertight.`; (7) `through hatch covers / that were not / sufficiently watertight.`; (8) `In its theory, / water may also have been / building up inside the ship.`; (11) `there is still a gap / that has never been / fully reconstructed.` It could not measure these exact candidate lines and identified the agency name and `gradually through hatch covers` for width checking.

The follow-up variants are evaluated against the exact channel rule before use. In particular, candidate endings `that`, `been`, and `not` remain grammatical hooks under the grouping contract; candidate lines must also fit the measured 1344 px safe width. They are not accepted as a reviewed plan solely because the model proposed them. The only correction directly supported by both semantic review and pixel measurement is pair 3: `located the wreck / at a depth of about 160 meters.`; pair 4 can only be joined if it fits (measured at 1348 px, so it does not). Other forced boundaries will remain disclosed as constraints in the caption review record, pending real-scene review. No narration edits are proposed by this consultation.

## Follow-up result

The second request completed with these candidate partitions: (6) `The United States Coast Guard / concluded that / water had probably been / entering the cargo hold / gradually through hatch covers / that were not / sufficiently watertight.`; (7) `through hatch covers / that were not / sufficiently watertight.`; (8) `In its theory, / water may also have been / building up inside the ship.`; (11) `there is still a gap / that has never been / fully reconstructed.` The model said the exact width was not measured and called out `The United States Coast Guard` and `gradually through hatch covers` for checking.

PIL glyph widths using the actual face and font size are: `The United States Coast Guard` 1265.7 px; `concluded that` 602.9 px; `water had probably been` 1016.8 px; `entering the cargo hold` 954.9 px; `gradually through hatch covers` 1266.9 px; `that were not` 565.9 px; `sufficiently watertight.` 948.5 px; `water may also have been` 1287.1 px; `building up inside the ship.` 1084.0 px; `that has never been` 816.0 px; `fully reconstructed.` 806.9 px. Visible width also includes the profile's outline and horizontal padding. The candidate endings `that`, `been`, and `not` remain hooks under the channel grouping rule. The final choice and its open checks are recorded in `SUBTITLE_BOUNDARY_REVIEW_v01.md`.


Correction to the second request: the renderer contract reports 1344 px as the full visible subtitle envelope, not the text-only safe width. The renderer subtracts two 20 px pads and two 3 px outlines, leaving 1298 px for glyphs. The consultant's suggestions were therefore not evaluated against the correct limit, and the 1337.6 px `at a depth of about 160 meters.` line does not fit. The v04 `keep_together` experiment increased the warning count from 11 to 12 and introduced no accepted improvement; its files were removed. The active edit remains montage manifest v02 and subtitle prep v02.

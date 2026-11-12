# Paper 038 — product-language correction / 2026-11-03

Status: `product_language=en`; Russian production assignment withdrawn. User correction: Paper videos are exclusively English. The user's request to see/review the Russian script and acceptance of the latest text did not request a Russian film. Earlier records claiming such a language selection were the coordinator's error.

## Production inputs

- Preserve `Source/Script/narration_ru_v06.md` as the user-selected story text and RU v07 as the subsequent working source; neither is an English TTS input.
- A faithful English production version of the latest accepted story is still required. Historical EN v05 predates the selected Russian revision and is not automatically current.
- SHOTLIST v89 preserves the visual plan and source references, but Russian spoken rows, cue wording and estimated timings are `STALE_LANGUAGE`. Reconcile it with the English production narration and actual EN alignment before assembly.
- Nine Cyrillic cue PNGs in captions_v01 are `FAIL_LANGUAGE` / excluded from the current production selection. Their historical static fit checks remain records of geometry, not acceptance for the English film. They have not been regenerated in this correction pass.
- C07 `47`, C09 `46`, C10 `1748` contain numbers only and are eligible for reuse after pairing/timing review against the English edit. No file deletion or pixel editing is implied.
- English text replacements below are translation candidates, not generated/accepted PNGs or timed cues. Final wording must fit the actual English narration and scene function.

| Cue | Old visible text | English replacement candidate | Required work |
|---|---|---|---|
| C01 | ЧУЖАЯ СХВАТКА | SOMEONE ELSE’S FIGHT | New English PNG + pair review |
| C02 | ПРЕСТУПЛЕНИЕ? | A CRIME? | New English PNG + pair review |
| C03 | ДВА УДАРА | TWO STRIKES | New English PNG + pair review |
| C04 | СЭППУКУ | SEPPUKU | New English PNG + pair review |
| C05 | БЕЗ ГОСПОДИНА | MASTERLESS | New English PNG + pair review |
| C06 | ПОПЫТКА ПРОВАЛИЛАСЬ | THE PLAN FAILED | New English PNG + pair review |
| C07 | 47 | 47 | Reuse candidate; EN timing/fit review |
| C08 | МЕСТЬ СВЕРШИЛАСЬ | REVENGE COMPLETE | New English PNG + pair review |
| C09 | 46 | 46 | Reuse candidate; EN timing/fit review |
| C10 | 1748 | 1748 | Reuse candidate; EN timing/fit review |
| C11 | ЦЕНА МЕСТИ | THE PRICE OF REVENGE | New English PNG + pair review |
| C12 | БЕЗ ОТВЕТА | UNANSWERED | New English PNG + pair review |

## Other dependent outputs

- End-screen copy becomes `WATCH NEXT`; Russian `СМОТРИ ДАЛЬШЕ` is excluded. ES01/ES02 backgrounds remain reuse candidates, conditional on no baked Cyrillic text and the final overlay/native-widget fit. Existing native end-screen status remains NOT_CONFIGURED.
- RU title proposal and `VIDEO_DESCRIPTION_v01.txt` are `FAIL_LANGUAGE` for this film. Packaging status v01 is STALE; English title/thumbnail/description/post text must follow the final EN production version. Existing thumbnail image is not declared rejected without checking its actual lettering.
- Subtitle geometry referring to Cyrillic is historical. EN word groups, subtitle fit, cues and cut timings require English narration/alignment. Numeric scene labels in working files are not viewer text.

## Next production step

Prepare the English production narration from the latest accepted story; reconcile the English storyboard/cues, then regenerate the nine English cue PNGs using the captions/typography procedure and review all actual scene×cue pairs. Use only the corrected English selection for Palmier assembly. This pass updates rules, selection state and the replacement plan; it does not claim new PNGs, narration, voice, fit QA, export or YouTube changes.

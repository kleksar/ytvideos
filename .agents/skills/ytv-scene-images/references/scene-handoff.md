# Scene selection and evidence contract

Use this for a scene set or a versioned-series resume. Keep the existing episode manifest/current state as selection owner. Add missing evidence or a linked supplement; do not create a competing current-version list. Paths are relative to an explicitly stated base directory.

For the set record:

- Episode/channel, visual profile reference, storyboard revision/hash and exact requested scope.
- Required scene IDs and selected file for each, or explicit missing/rejected state.
- Actual reference files/hashes and roles (style, identity, location, historical detail); link acceptance/provenance instead of copying a stale summary.
- State/permissions needed by the next stage and any pending sample checkpoint.
- Representative early-check IDs/findings when applicable, plus the actual selected-file sequence sheet, covered IDs/versions, observed repetition/hierarchy findings and resolved or open corrections. Link the existing log; no parallel acceptance register is needed.

For each selected asset record:

| Field | Meaning |
|---|---|
| Scene ID, version, path, SHA-256 | These exact bytes; different versions with the same scene ID are not interchangeable |
| Requested generation target | Requested aspect, pixel dimensions and quality; exact prompt and any explicitly applied tool controls, with unsupported/unknown values identified |
| Native dimensions, format/mode, alpha | Measured file properties; delivery size/upscaling recorded separately |
| Delivery geometry and fit | Link the accepted brief/export contract; record target canvas, proportional scaling/crop and relevant zoom envelope separately from the generation request and native PNG size |
| Dependencies | Applicable storyboard beat/revision, narrative job/visual finding, assigned scene lettering and carrier, references, before/after object state; link the visual bible |
| Source/prompt | Reused/generated/edited source, exact prompt/log, actually supplied reference paths/hashes and roles distinguished from required references, known tool/parameters |
| Recurring-character findings | Planned and observed presence/role, including the presenter’s visible action if assigned by the storyboard; separate observed rendering-style, identity and costume findings against the accepted anchors, with limits for uninspected details |
| Environment and integration | Observed environment/prop rendering against the channel profile, separately from character fidelity; lighting, perspective, occlusions and contact |
| Operation and text context | Generate/edit, actual edit target and preserved elements where applicable; language and required wording of significant carriers tied to place/date/institution |
| Historical visual anchors | Inspected source pages/files, identity/date/version, construction features and unknown views, credit/usage conditions and reference roles; distinguish archival source from generated reconstruction |
| Acceptance | Who accepted what/when, with a source; user approval, author review and independent review separately |
| QA evidence | Full-file/detail views, actual framing/reduction checks, findings and limits, each tied to version/hash |
| Handoff | Ready/missing/rejected/needs recheck; planned frame fit/text areas; downstream checks affected by replacement |

Do not invent a review to complete a field. For legacy accepted assets keep the original acceptance source; absent detail/crop evidence stays unknown. This does not erase user acceptance or prove compliance with a new check. For new production close applicable blockers before import. A previous rejection remains in provenance when the replacement passes.

Source-image QA, framed-image QA, caption-composite QA, saved-timeline QA and final-film QA are distinct observations. Record coverage without collapsing them into one `PASS`. If bytes differ from the reviewed SHA, resolve the actual selection before forwarding it.

Changed dependencies require reassessment of affected assets: costume changes affect recurring scenes; moved objects affect scenes after the event; crops affect anatomy and caption fit. A title-only change does not regenerate scenes. A new storyboard revision with an unchanged scene may carry forward acceptance after verifying its dependencies are unchanged.

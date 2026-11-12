# Systemic renderer settings/provenance fix — 2026-11-04

Implemented locally, no YouTube mutation or episode re-render.

## Changes
- Full render requires an explicit READY_TO_RENDER export passport. The same actual final-command builder serves settings-only preparation and execution. Mismatches stop before scene encoding.
- Settings checks cover accepted mix binding, timeline, command mapping, supported video controls and AAC encode/copy contracts; unsupported required fields/controls fail explicitly.
- New delivery-v2 receipts bind frozen command/passport/code snapshots and FFmpeg version to exact media identity. Current working-tree engine changes no longer invalidate a completed output. Accepted source/edit/profile/evidence freshness and exact-file user acceptance remain checked.
- Historical saved-command audit writes a scoped report without encoding; explicit binding creates a new receipt and preserves old receipt, media and existing acceptance. It does not fabricate missing engine sources or AV review.
- Export/QA/production/state/lifecycle documentation and renderer instructions aligned. Existing unrelated working-tree edits preserved.

## Verification
- 37 montage/delivery tests passed, including actual renders for both channels/formats, PCM stereo AAC encoding, settings-only execution, failure before scene encoding, snapshot tampering, source changes, acceptance and historical rebinding.
- 17 uploader tests passed with synthetic network fixtures; no external API mutation.
- Current-process checker: 99 documents, no obsolete montage routes.
- git diff --check and Python compilation passed.
- Real saved-command audit of episode 038: v01 UNRESOLVED due to AAC 192k below stereo requirement; v02 SETTINGS_PASS under its original contract. Reports are adjacent. These are settings verdicts only, not AV QA or user acceptance.

## Boundaries
Other episodes have not been audited. No mass rerender or correction of published files occurred. Old receipts without provenance require the explicit saved-command audit, not an automatic rerender. User acceptance of Guy Fawkes v02 remains pending; no v03 is needed solely because this tool was updated.

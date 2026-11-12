# Paper one-line subtitle boundary review v01

- Episode: Paper Detour 045 — The Last Voyage of the Edmund Fitzgerald
- Narration/transcript: English v02; unchanged during this review.
- Voice and word map: exact v02 mix SHA-256 `5709d7740516f33f152f9106258cccb85e0208464031bcd48bbe7378250f5c2f`.
- Renderer geometry: Chalkboard SE TTC index 2, 84 px, maximum visible subtitle envelope 1344 px, which leaves 1298 px for glyphs after the 20 px horizontal padding and 3 px outline on each side.
- Evidence: `Work/subtitles_prep_en_v02/caption_groups.json`, `Source/Production/EXTRA_HIGH_SUBTITLE_GROUPING_v01.md`.

## Decision

Use the width-safe automatic groups from `Work/subtitles_prep_en_v02`; no manually forced phrase list changes the transcript. The sequence has 11 forced or ambiguous syntax boundaries. These are explicit, bounded caption compromises for the review export, not a claim that the grouping is ideal or an upload-ready signoff.

The Extra High reviewer recommended moving boundary 3 to `located the wreck / at a depth of about 160 meters.`. Raw Chalkboard glyph width for the second line is 1337.6 px, exceeding the actual 1298 px glyph safe width. The suggested joining of `while the stern was upside down.` measures 1348 px and also does not fit. A temporary `keep_together` experiment moved the number away from its unit and was discarded; the current manifest remains v02. Preserve the automatic lines to keep quantities and punctuation intact.

The suggested repairs for boundary 6 ended on `that` and `been`, and boundary 8 ended on `been`; these are syntactic hooks under the grouping rule. Boundary 7's alternate `that were not / sufficiently watertight.` ends on `not`; boundary 11's alternate `that has never been / fully reconstructed.` ends on `been`. The alternatives do not remove all hooks and are not an improvement under the channel rule. Keep the measured automatic groups and carry all warnings into the review export.

## Open checks

- Word highlight timing against the actual spoken recording: UNVERIFIED.
- Audio naturalness, pronunciation, mix balance/listening: UNVERIFIED.
- Caption pixel placement and protected-object clearance on real scene frames: UNVERIFIED pending the exported implementation sample.
- Full-track audible synchronization: UNVERIFIED.

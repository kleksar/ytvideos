# Release preflight — Guy Fawkes 038

Date: 2026-11-04. User instruction received: “пукша. заливай на ютуб в открытый”. Intended destination: Nuviko History, channel ID `UCbyLx6Rf3iWww4bPZJ2oo2A`; requested access: Public. This is an authorization to proceed with the requested release, not evidence that technical media checks have passed.

## Fresh channel and playlist read

Read-only YouTube Data API preflight through the verified destination profile returned the exact Nuviko History channel ID and title. The currently owned, fully paginated playlist inventory contains:

- `History Shorts` — private; 3 videos; not a fit for this long film.
- `History Documentaries` — public; 3 videos; appropriate long-form history collection. ID: `PLCtiNAU_98r0`.

Current members of `History Documentaries` are:
- `How the Black Death Spread Across Medieval Europe`
- `Marseille 1720: Life Inside a City Cut Off by Plague`
- `Pompeii Wasn’t Buried by Lava. What Actually Destroyed It?`

This is a dated read-only snapshot, not proof of a future membership write. If upload proceeds, add this video once to `PLCtiNAU_98r0` while it is Private, then confirm read-back before Public.

## Blocking media receipt fields

The current delivery receipt records:
- `semantic_grouping`: `PASS`
- `audible_sync`: `UNVERIFIED`
- `visual_placement`: `UNVERIFIED`
- user acceptance: not recorded in the receipt

The project upload adapter runs the delivery gate before contacting YouTube. It requires all three subtitle checks to be `PASS`, evidence records for each, and acceptance bound to the exact MP4 hash. The Public adapter separately requires a confirmed serving manual English SRT track, a processed owned Private upload, and exactly one membership in the selected owned playlist. These requirements have not been bypassed.

## Current external state

No upload, thumbnail write, playlist change, caption upload, metadata update, Public change, or native A/B test was performed in this preflight. Current intended base package remains the fixed description plus title/thumbnail experiment A/B/C from `PACKAGING_PLAN_v01.md`. Test status is `not started`.

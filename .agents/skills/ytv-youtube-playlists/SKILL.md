---
name: ytv-youtube-playlists
description: Select and organize YouTube playlists for a new video or a full channel catalog; produce a complete, evidence-based assignment and order plan for release, then reconcile saved memberships.
---

# YouTube playlists

Own playlist architecture, inclusion criteria, editorial order and catalog coverage. Read the active project's entry instructions and channel playlist registry first. For Paper Detour read [its profile](references/paper-detour.md). Other channels supply their own identity, language, topics, visibility policy and registry; do not inherit Paper settings.

## Choose the scope

- **Single release:** before upload, inspect a fresh, fully paginated inventory of the target channel’s existing playlists and select any appropriate existing playlist by stable ID based on the accepted film, its topic and the playlist’s actual promise/content. Return the assignment and rationale keyed to the episode before a video ID exists; resolve the actual ID at release. In the authorized upload flow, hand off the addition for the upload/organization step and verify membership after a video ID exists. Do not change playlist visibility or video privacy merely to add membership.
- **Catalog audit:** obtain a fresh, fully paginated inventory of owned uploads, playlists and members through the release/uploader route. Include public, unlisted and private states in the accounting; distinguish editorial releases from technical streams, tests, removed items and other exclusions. Read relevant episode context; a slug or title is insufficient evidence of topic or factual status.

Apply the project's research and evidence rules; an unavailable optional consultation does not prevent independent editorial work. A snapshot is dated evidence, not live state. Resolve a registry/API discrepancy before a dependent write; retain earlier receipts as history.

## Build the viewer's route

Reuse a matching playlist by stable ID. Its promise, description and actual videos must agree. Separate documented events, folklore, personal accounts and reported estimates when grouping them would imply a false evidentiary promise. Membership does not independently verify a story.

Each proposed addition needs a content-based reason. Overlap is useful when it offers a distinct viewer route; do not add every video everywhere. Related Shorts and their parent film are one story cluster when assessing the need for a new theme. Choose an intelligible sequence and preserve an accepted existing order unless there is a reason to change it; setting Manual is not arranging items.

Create a new playlist only when existing ones cannot honestly serve a useful route with available videos. If a new playlist would be better, tell the user directly and propose a specific name and concise rationale; record the proposal and its decision separately. Do not create it without the necessary authorization. A pending proposal or unavailable inventory does not by itself block the authorized upload: record `new_proposed`, `unassigned` or `unverified` with reason, continue within existing permissions, and resume the playlist action only when its requirements are met. Do not imply membership was saved until read-back confirms it. Avoid empty future categories and near-duplicate names. Channel size thresholds are editorial preferences, not YouTube requirements; record a justified exception rather than disguising a bad fit. A remaining unassigned video must be explicit and explained, never silently omitted. Write concise names/descriptions in the channel language; keyword or hashtag stuffing is not the organizing method. Do not promise algorithmic promotion or watch-time gains.

## Hand off and finish

Return a versioned plan containing:

- channel identity, mode, source snapshot/time and relevant accepted content;
- `playlist_architecture`: stable IDs (or temporary keys for proposed creations), names, descriptions, inclusion boundaries and visibility intent;
- `video_assignments`: every scoped video ID, target playlists and reasons, or an explicit excluded/unassigned status;
- `playlist_order`: intended ordered video IDs and the ordering reason;
- `release_handoff`: minimal create/add/remove/reorder/playlist-metadata delta, protected state and the applicable user authorization;
- `coverage`: total inventoried, editorial, assigned, unassigned and excluded counts; distinguish `proposal_only`, `applied_unverified` and `saved_verified`.

When external organization is authorized, continue through the project's release procedure and the available `youtube-upload` skill; do not stop at the proposal. They own API-first, OAuth, mutations and reconciliation, not this skill. Re-read the exact target before a write, apply only the remaining delta, preserve concurrent unrelated edits, and verify through that route. Unknown write outcomes require read-only reconciliation before any new write.

Compare the final complete membership/order with the plan, including duplicate video IDs within a playlist, missing additions, unintended removals and excluded items. Record item IDs and read-back receipts. A playlist's visibility and a video's privacy are independent: do not change either merely to make membership visible. A missing language or sorting-mode field is unverified, not inferred from English text or returned positions. API membership verification is not a Studio sorting-mode check.

Verify the required sorting mode before a position-bearing write if it has not been checked. For `manualSortRequired`, use the global uploader's reconciliation and Studio-only setting procedure; do not silently abandon the accepted sequence.

Update the channel registry and affected episode pointers from the verified result. Preserve exact IDs and actual access; do not turn this task's authorization into blanket permission for future publication. Return concrete changed counts, final coverage and material limitations.

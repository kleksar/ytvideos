# Paper Detour 040 — end screen plan v01

- Channel / episode: Paper Detour / 040 Berlin Wall.
- Applicability: `REQUIRED_NEW_LONG`.
- Basis: current new-long-film Paper standard; user authorized full production 2026-11-03.
- Product language: English. Narrative completes before the end-screen section; no spoken CTA or subtitles in silence.
- Accepted narration: `Source/Script/narration_en_v01.md`; last spoken line: “By midnight, the people of Berlin had answered him.” Exact end time awaits scene alignment against the generated voice.
- Canvas: 2560×1440, 30 fps.
- Background: two different complete static paper-diorama scenes, 5 seconds each, direct cut. Same calm paper world and palette; a small folded crossing pass and a paper bridge/threshold continue the story's documents-to-crossing motif. Keep all high-detail objects and human figures out of native UI reservations.
- No baked-in YouTube controls, card frames, thumbnails, avatar, button shapes, titles, or promised click targets. No speech, caption, or new audio in the tail.
- Initial geometric reserves (fractions of 16:9 frame; verify against actual Studio native preview before final acceptance): Subscribe center `(0.25, 0.52)`, clear circle diameter `0.16 × frame width`; upper video `x=0.57,y=0.12,w=0.34,h=0.34`; lower video `x=0.57,y=0.54,w=0.34,h=0.34`. Preserve extra margin for hover/labels. Zones stay clear in both backgrounds.
- Native labels, if consistent with channel standard: `KEEP EXPLORING` and `SUBSCRIBE` are platform-side elements, not text burned into backgrounds.

| Element | Planned target | Rationale | Verification | Timing / position |
|---|---|---|---|---|
| Subscribe | Paper Detour channel ID — resolve during packaging | Own channel | Pending Studio channel check | Full 10-second tail, left |
| Video 1 | `UNRESOLVED` until accepted catalog candidates are selected | Related long film | Pending content and status check | Full 10-second tail, upper right |
| Video 2 | `UNRESOLVED` until accepted catalog candidates are selected | Distinct second long film | Pending content and status check | Full 10-second tail, lower right |

- Background scene A: planned static bridge/threshold composition, 5 seconds; PNG/hash/frame interval pending storyboard and image creation.
- Background scene B: related static paper-document detail/alternate bridge angle, 5 seconds; PNG/hash/frame interval pending storyboard and image creation.
- Actual tail frames/end frame exclusive: pending final voice/edit timing.
- Tail sound: pending authorized mix; preserve the last narration intact and do not add audio for the end screen.
- `background_qa=PLANNED` — compositions, geometry, cut, and actual timing are not created or checked.
- `native_end_screen=NOT_CONFIGURED` — configure only after final edit and candidate selection.
- API/Studio configuration, saved read-back, public render/links, final MP4 hash, edit version: pending.

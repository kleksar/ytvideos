# Upload inventory and cleanup — 2026-11-03

Fresh Data API channel inventory before deletions in `api_snapshot.json`, 22 owned uploads: 17 public, four private and one unlisted. User approved plan to delete the old private duplicate and technical stream, then compare remaining pairs without new editing.

Deleted `HTDvGrDsvcA` (superseded private version without current built-in captions), retaining public `UkwqGIqvink`; deleted `QqMudxBNZgo` (unlisted zero-duration technical stream). Both absent on immediate API read-back; receipts `deleted_<id>.json`, before-state `before_deletions.json`. No other video was changed.

Radio Short 01: public `85dwIXy_lZs` has 458 views at pre-delete snapshot and a Related Video to film `0RaC4t7yn5o`; private `FMSPuyZvPXE` is an earlier accepted v03 redesign without current full narration subtitles; exact source hash `7bfbb706e14ebb66bfef5d25e99ca80eebc454ae2d2711e9f79f8ef989f281b3`. It removes 11 book-page SFX, adjusts accents, replaces one scene and applies motion. Later full subtitle review `Work/short01_subtitles_20261102_v02/previews/short01_subtitles_full_v04_group_v02_review.mp4`, SHA-256 `2046934add0e8647d35228d7d9d702e23e4cc9ff05a3fa4504ce85e52f7885a4`, is local only and has incomplete audible sync QA. The user explicitly does not want new montage; choosing an existing file and its release is a separate decision. Public and private uploads remain intact.


User chose the existing last subtitle preview for radio Short 01. Published `lotfSkfgvuM`, removed old `85dwIXy_lZs` and `FMSPuyZvPXE`, verified; [release receipt](../../videos/001_radio_game/Shorts/01_radio_signal/Packaging/Metadata/release_subtitles_20261103/RECEIPT.md).

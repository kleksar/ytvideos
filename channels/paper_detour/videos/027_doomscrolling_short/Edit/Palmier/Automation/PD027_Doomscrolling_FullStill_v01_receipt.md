# ARCHIVE — PD027 Doomscrolling full-still Palmier receipt

**Date:** 1 November 2026  
**State:** rejected: wrong story. This is the visual-only doomscrolling timeline; the current 027 is Minnie Freeman. Preserve for history and do not continue or render it.

## Project and timeline

- Project: `Paper Detour 027 Doomscrolling 20261031` (`09BFC4E5`).
- Timeline: `PD027 Doomscrolling full stills v01 20261101` (`CA999461`).
- Format: 1080×1920, 30 fps, 861 frames / 28.70 seconds, Rec.709.
- The new timeline is selected and visible in Palmier at frame 0. The existing `Timeline 1` (`41B11E0F`) was left unchanged.
- All project edits were made through Palmier operations. The `.palmier` package was not edited manually.

## Tracks and intervals

`Main` — track `62278A71`, index 1. The intervals are half-open `[start, end)`:

| Scene | Frames | Media | Media ref | Clip ID |
|---|---:|---|---|---|
| 01 Opening | [0,172) | `scene01_opening.png` | `2AEBA5B7` | `F24336FE` |
| 02 Endless stream | [172,313) | `scene02_endless_stream.png` | `8FFF61D6` | `9EFA5DE2` |
| 03 Family learning | [313,464) | `scene03_family_learning.png` | `BD45D72D` | `5657C84C` |
| 04 Other lives | [464,569) | `scene04_other_lives.png` | `AB03C4BC` | `329CC084` |
| 05 Looking away | [569,656) | `scene05_looking_away.png` | `940C7359` | `F837F052` |
| 06 Family evening | [656,768) | `scene06_family_evening.png` | `EB18BD24` | `057B2F18` |
| 07 Opening repeat | [768,861) | same `scene01_opening.png` | `2AEBA5B7` | `9077550B` |

`Grain` — track `53E695A8`, index 0, using the existing 8-second ProRes 4444 alpha source `film_grain_8s_prores4444.mov` (`9EE2ED3D`). Palmier's `full` / `fill` layout centers and cover-crops the landscape source for the vertical frame (0.342 crop on both horizontal edges). Four adjacent source segments cover the whole timeline at 50% opacity:

| Frames | Clip ID |
|---:|---|
| [0,240) | `9C5EEC08` |
| [240,480) | `C67F7EA0` |
| [480,720) | `1E007DF9` |
| [720,861) | `1AC813F6` |

The grain is a global texture overlay. It is not a separate scene plane and does not animate characters or props.

## Review performed

Palmier `get_timeline` confirmed the 861-frame duration, the two-track structure, the seven still intervals, the repeated opening media ref, and the four continuous grain segments. Palmier `inspect_timeline` composites were visually sampled at frames 1, 173, 314, 465, 570, 657, 769, and 860. Exact cut-boundary clip IDs were checked at 171/172, 312/313, 463/464, 568/569, 655/656, and 767/768; the loop uses the same image media ref at frame 0 and the final range. These diagnostic frames contain Palmier's coordinate grid and frame burn-in; they are not clean master frames.

Full 1× playback, voice synchronization, and audio checks remain pending. No voice, music, SFX, text, subtitles, or export were created. This timeline is a reviewable visual draft, not a finished release.

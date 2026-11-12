# Paper Detour 041 — Dune origin, storyboard v02

Status: production timing update against the actual user-approved EN v04 recording. Story and spoken wording remain locked. No fact-check or narrative edits were performed.

- Product: English Short, 9:16.
- Project canvas: 1440×2560, 30 fps.
- Source scene request: Nano Banana Pro 2K portrait. Actual accepted stills: 1536×2752 JPEG; generated pixels and dimensions are verified in Palmier. Slight cover-fit crop to project canvas must be checked on the actual composite.
- Construction: one complete still image per shot; direct cuts; no separate layer animation. Short-form holds vary with narration; scene timings follow the measured voice rather than the preliminary storyboard estimates.
- Speech: 52.88 s by `ffprobe`; alignment JSON is character-level. Boundary times below use the actual starts of the following sentence, rounded to the nearest 30 fps frame. Final end boundary is 1587 frames / 52.9 s, subject to final encoded-audio inspection.
- Subtitles and the three approved semantic accents remain separate screen overlays.

| Scene | Locked narration coverage | Timeline interval | Composition / light | Cut and continuity | Separate accent | Motion |
|---|---|---:|---|---|---|---|
| S01 | “Sand dunes kept blocking a highway in Oregon.” | 0–98f · 0–3.27s | High three-quarter Oregon road crossing layered pale dunes; asphalt visibly obstructed by sand; dark conifers, cool coastal light. | Opening conflict; cut to grass as the Forest Service response begins. | None | Whole-image right pan 0.7%; protect road bend and drift. |
| S02 | “The U.S. Forest Service fought back with grass.” | 98–202f · 3.27–6.73s | Low close view of beachgrass and anonymous paper hands planting it, pale dunes, cool soft light. | Scale shift from dune-wide to planted grass; then cut below the surface. | `GRASS` | Whole-image left pan 0.6%; keep hands and planted tuft visible. |
| S03 | “A journalist named Frank Herbert came to investigate. Beachgrass roots held the sand in place.” | 202–389f · 6.73–12.97s | Warm 3/4 view of blank field notebook and dimensional dune cross-section with visible roots. No portrait. | Planting to what holds the sand; cut wide to dune ridges. | None | Whole-image zoom 1.04→1.05; keep notebook and roots visible. |
| S04 | “But Herbert was struck by something larger: these dunes moved almost like ocean waves, only far more slowly.” | 389–608f · 12.97–20.27s | Broad layered ridges echoing the curve of ocean waves; dunes remain clearly sand; cool raking light. | Root detail to large landform; flow into study materials. | None | Whole-image right pan 0.8%; preserve several ridge lines. |
| S05 | “He began studying how deserts worked, and how people survived in them.” | 608–732f · 20.27–24.4s | Half-overhead warm desk, nonverbal wind/sand diagrams and small paper desert model with human silhouettes. | Dune pattern becomes the object of study; cut on paper forms. | None | Whole-image left pan 0.5%; keep model centered. |
| S06 | “His notes grew beyond any newspaper article. Eventually, he imagined” | 732–826f · 24.4–27.53s | Close view of blank manuscript pages in a spiral beginning to form a planet, golden side light. | Circular paper form sets up the full planet; continuous speech across cut. | None | Whole-image zoom 1.04→1.05. |
| S07 | “an entire planet shaped by its desert, where controlling the environment could change a civilization.” | 826–1055f · 27.53–35.17s | Full paper desert planet and miniature settlements/barriers against deep blue; globe fully visible, warm side light. | The imagined world opens into the name/rejection passage. | None | Whole-image right pan 0.6%; keep globe complete through full path. |
| S08 | “He called it Arrakis. Publishers turned down his novel again and again.” | 1055–1219f · 35.17–40.63s | Blank manuscript and glowing paper planet among anonymous envelopes receding into cool shadow. | Name/world to rejection; cut to a lit manuscript and symbolic press. | `ARRAKIS` | Whole-image left pan 0.6%; leave its exact overlay placement unobstructed. |
| S09 | “Then Chilton took a chance on it.” | 1219–1289f · 40.63–42.97s | Centered blank manuscript leading toward an old symbolic printing press under warm light. | Envelopes to a clear path and lit manuscript; cut to automotive material. | None | Whole-image zoom 1.04→1.05. |
| S10 | “Chilton was famous not for science fiction, but for car-repair manuals.” | 1289–1423f · 42.97–47.43s | Paper engine cutaway, wrench and anonymous repair folders; warm workshop light. | Sharp change to automotive context; cut to the desert-planet title reveal. | None | Whole-image right pan 0.6%; keep engine in frame. |
| S11 | “The book was Dune.” | 1423–1482f · 47.43–49.4s | Amber layered paper planet in deep blue atmosphere, strong side light. | Title reveal; cut from the imagined planet back to Earth. | `DUNE` | Whole-image zoom 1.04→1.05; keep the exact overlay clear. |
| S12 | “And before there was a desert planet, there was a problem on Earth:” | 1482–1587f · 49.4–52.9s | Reuse the exact accepted S01 Oregon road still, with the same held whole-image framing. | Exact same image at S12 and S01 makes the end-to-start visual loop continuous; spoken text remains a separate layer. | None | Hold the S01 still at the same 1.04 scale and centered position as the opening. |

## Timing and loop

- The spoken file is 52.88 s; 1587 project frames is a 52.9 s image timeline. Confirm encoder padding and final word on the exported audio.
- Sentence-boundary cuts preserve intact clauses. Some holds are shorter/longer than v01's 4–6 s estimate; this is required by the measured speech and does not change the story.
- The voice ends on “Earth:” and image S12 returns directly to S01, where the opening identifies the problem. No new narration or transition is added.
- Preliminary motion is permitted only as a subtle transform of the whole still; if full-path inspection shows crop or accent conflict, reduce/omit that motion without changing the still.


## v03 correction — exact image loop

The exported preflight candidate v01 did not visually match the opening road at the final cut. S12 now reuses accepted image S01 (mediaRef `E19BE26D`) with the same static transform. Narration, caption content, scene duration and cut timing are unchanged. This replaces the v02 note that the two separate road scenes only matched approximately.

# Paper Detour 043 — hashtag review v02

- Date: 2026-11-03 (Europe/Belgrade)
- Channel/video: Paper Detour, EN Short `LQRdFHkgEPg`; accepted MP4 v04 and narration EN v02 checked.
- Scope: description hashtags only. The approved title is unchanged and has no hashtags. The separate YouTube Tags field is not a hashtag field and remains unchanged.
- Live baseline read through YouTube Data API immediately before the edit: title `Pompeii: Run Through Falling Stones or Stay Inside?`; description text followed by `#Pompeii #MountVesuvius #VolcanicEruption #Pumice #History #Shorts #PaperDetour`. All seven existing hashtags are retained.
- Consultation: ChatGPT project `YT Видео`, visible model label **Очень высокий** immediately before the request; [completed consultation](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6aea44ee-092c-83ed-b392-7f12e3eddc30). Its full proposed set was 21 relevant tags; the review accepts that complete set under the project's maximum-coverage rule.

## Candidate coverage

| Direction | Accepted hashtags | Basis |
|---|---|---|
| Place and volcano | `#Pompeii`, `#MountVesuvius` | Exact city and volcano in the narration. |
| Event and date | `#VesuviusEruption`, `#AD79` | The specific eruption and year are central. |
| Historical setting | `#AncientRome`, `#RomanEmpire`, `#RomanHistory`, `#AncientHistory`, `#History` | The city and residents belong to the Roman world; tags span the specific setting and broad history topic. |
| Natural process and material | `#Volcano`, `#VolcanicEruption`, `#Pumice`, `#PumiceFall`, `#VolcanicHazards`, `#NaturalDisaster` | The eruption and sustained falling pumice create the danger. |
| Consequence and choice | `#RoofCollapse`, `#BuildingCollapse`, `#EscapeOrShelter` | The narration describes collapsing roofs/walls and the residents' choice between flight and shelter. These describe the story, not survival advice. |
| Format and channel | `#HistoryShorts`, `#Shorts`, `#PaperDetour` | Historical Short format and optional channel navigation. Paper profile requires `#Shorts` for a confirmed Short. |

## Full description block and change

Before: 7 tags — `#Pompeii #MountVesuvius #VolcanicEruption #Pumice #History #Shorts #PaperDetour`.

Added (14): `#VesuviusEruption #AD79 #AncientRome #RomanEmpire #RomanHistory #AncientHistory #Volcano #PumiceFall #VolcanicHazards #RoofCollapse #BuildingCollapse #EscapeOrShelter #NaturalDisaster #HistoryShorts`.

Removed: none. Reordered: no existing tags moved; all were retained in their prior order and the 14 additions were inserted between the specific subject tags and the broad/format/brand tail.

Final `description_hashtags` (21 tags, complete block):

`#Pompeii #MountVesuvius #VesuviusEruption #AD79 #AncientRome #RomanEmpire #RomanHistory #AncientHistory #Volcano #VolcanicEruption #Pumice #PumiceFall #VolcanicHazards #RoofCollapse #BuildingCollapse #EscapeOrShelter #NaturalDisaster #History #HistoryShorts #Shorts #PaperDetour`

Rejected alternatives: `#Vesuvius` duplicates the more specific `#MountVesuvius`; `#PompeiiEruption` could suggest the eruption was located in the city rather than at Vesuvius; `#Escape`, `#Danger`, and `#Survival` are less specific and could imply generic advice. Archaeology/excavations, lava, pyroclastic flows, volcanic ash, Plinian classification, Herculaneum, Pliny the Younger, and present-day Italy are not discussed. Do not infer these subjects from the premise.

## Exact-use and demand check

- Searches performed 2026-11-03 for English-language exact hashtags on YouTube-indexed pages included `site:youtube.com/watch "#Pompeii" "#MountVesuvius" "#History"`, `site:youtube.com/watch "#VolcanicEruption" "#Pumice"`, `site:youtube.com/watch "#RomanHistory" "#AncientRome" "#Pompeii"`, `site:youtube.com/watch "#Vesuvius79" OR "#79AD" OR "#EruptionOfVesuvius"`, plus focused searches for the proposed event, collapse, dilemma, history-format, and hazard tags. Search results surfaced descriptions containing `#Pompeii`, `#MountVesuvius`, `#AncientRome`, `#RomanHistory`, `#RomanEmpire`, `#AncientHistory`, `#HistoryShorts`, and `#Shorts`: [YouTube example 1](https://www.youtube.com/watch?v=Tqc_ByTKujo), [YouTube example 2](https://www.youtube.com/watch?v=L4XgurMjVV8), [YouTube example 3](https://www.youtube.com/watch?v=3A6nrm67IuU).
- Exact-use observation: the checked results did **not** surface every searched tag. In particular, the new exact forms `#VesuviusEruption`, `#AD79`, `#PumiceFall`, `#VolcanicHazards`, `#RoofCollapse`, `#BuildingCollapse`, `#EscapeOrShelter`, and `#NaturalDisaster` were not surfaced in those result pages. This does not prove that they are unused. Existing `#VolcanicEruption`, `#Pumice`, and `#PaperDetour` were also not surfaced in the queried results; none is removed for that reason.
- Demand, trend, and hashtag-search volume: **not checked / unknown**. Search visibility is not evidence of popularity or a trend. YouTube's [hashtag guidance](https://support.google.com/youtube/answer/6390658?hl=en) says hashtags have no spaces, up to three may appear by a title, and more than 60 causes all of them to be ignored; 21 is below that threshold, not a quality target.
- Search scope: search-engine results indexed from YouTube, not a complete count of YouTube results or Studio Trends. The number of exact matches and market demand remain unknown.

## Application

The approved block is for the description only. Full updated description is in `release_metadata_v02.json`; local validation and the API write/read-back are recorded in `HASHTAG_UPDATE_RECEIPT_v02.md`.

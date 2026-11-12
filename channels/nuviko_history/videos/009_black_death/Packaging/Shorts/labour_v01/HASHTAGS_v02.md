# Nuviko History Short — hashtag pass v02

**Target:** `5v6exl0iQJE`, `Why England Tried to Hold Down Wages After the Plague`; English Short. Current YouTube state was freshly read from the authorized Data API on 2026-11-03. Source material: accepted transcript `Source/Shorts/05_labour/retained_transcript_v01.txt` (SHA-256 `63cb6f381de7f000f47647a629387ac541d14e85f7c8539ba35e859d90d3b270`).

## Complete description block

`#BlackDeath #MedievalHistory #MedievalEngland #LabourHistory #LabourShortage #WageControls #OrdinanceOfLabourers #StatuteOfLabourers #Shorts`

Nine distinct, directly relevant labels. The complete set is used in the description; the YouTube rule that up to three may display by a title is not a three-tag cap. Hashtags stay separate from `snippet.tags`. No hashtags were requested in the title.

## Coverage

| Dimension | Hashtag | Basis |
|---|---|---|
| Event | `#BlackDeath` | Central event named in the narration. |
| Era | `#MedievalHistory` | Medieval setting. |
| Place + era | `#MedievalEngland` | Work, government and laws are explicitly England-wide. |
| Field | `#LabourHistory` | Central struggle over wages and control of work. |
| Cause | `#LabourShortage` | The text says labour supply had fallen after mass deaths. |
| Policy | `#WageControls` | The government tried to hold wages down. |
| Named 1349 instrument | `#OrdinanceOfLabourers` | The ordinance is separately described from the 1351 statute; source records call it the Ordinance of Labourers. |
| Named 1351 instrument | `#StatuteOfLabourers` | The statute is explicitly named. |
| Format | `#Shorts` | Confirmed vertical Short. |

## Delta

- **Retained (5):** `#BlackDeath`, `#MedievalHistory`, `#LabourHistory`, `#StatuteOfLabourers`, `#Shorts`. Their spellings and relative order are retained.
- **Added (4):** `#MedievalEngland` (precise geography and era), `#LabourShortage` (the cause stated in narration), `#WageControls` (the government's response), `#OrdinanceOfLabourers` (distinct 1349 instrument).
- **Removed (0).**
- **Flagged/excluded:** `#LondonHistory` (event is England-wide), `#PlagueHistory` (adds little beside `#BlackDeath`), `#WorkersRights` (can imply the modern legal concept and is not the story's framing), `#PeasantsRevolt` (not mentioned), `#MedievalEconomy` (broad where direct subject labels are available), `#EnglandHistory` (less precise than `#MedievalEngland`), `#Wages` (very broad and less informative), `#WorkHistory` (broad and less specific than `#LabourHistory`).

## Use and demand checks

Read-only YouTube Data API v3 `search.list` candidate searches were run 2026-11-03. Search query region and language were not constrained. For each new hashtag, the first five returned videos' titles/descriptions were checked for the exact literal tag with `videos.list`: `#MedievalEngland` appeared literally in 1/5; `#LabourShortage`, `#WageControls`, and `#OrdinanceOfLabourers` appeared in 0/5. The searches surfaced relevant labour/medieval material, but exact usage is limited evidence. Search results do not establish demand; all four tags' popularity/trend status remains **unknown**. Semantic relevance is the reason to include them.

Existing channel use of `#BlackDeath`, `#MedievalHistory` and `#Shorts` was observed in Nuviko descriptions; the other retained tags already appeared in the prior accepted package/current description.

## Current platform rules checked

YouTube's current help says hashtags have no spaces, must be directly relevant, over-tagging harms relevance and more than 60 means all hashtags on that video are ignored. It says up to three description hashtags may appear by the title; that is display behavior, not the limit on the complete block. This block has nine, no exact duplicates and no spaces. Reference: https://support.google.com/youtube/answer/6390658?hl=en

The current official Data API update reference says `videos.update` with `part=snippet` replaces mutable properties in that part and requires `snippet.title` and `snippet.categoryId`; therefore those and the accepted separate Tags/language values are preserved in the scoped description update. Reference: https://developers.google.com/youtube/data/reference/rest/v3/videos/update

Historical naming check: The National Archives describes the 1351 statute as supplementing an earlier 1349 ordinance; recent legal-history scholarship uses “Ordinance of Labourers” for the 1349 measure. Internal source check: https://www.nationalarchives.gov.uk/explore-the-collection/explore-by-time-period/early-modern/plague/ ; https://onlinelibrary.wiley.com/doi/10.1111/ehr.13355

**Result:** `applied_verified`. YouTube API read-back returned the exact new description. Full current text is in `DESCRIPTION_EN_v02.txt`; write/read-back evidence is in `DESCRIPTION_CHANGE_RECEIPT_v02.json`.

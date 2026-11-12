# Paper Detour 042 — hashtag review v02

- Date: 2026-11-03.
- Material: accepted English Short, narration EN v02, claim audit v01; title B remains unchanged.
- Editorial status: `applied_verified`; full coverage decision and consultation are saved in `CONSULTATION_HASHTAGS_EXTRA_HIGH_v02.md`.
- Before revision, fresh API read-back showed six tags — `#Shorts #BirdMigration #WhiteStork #Pfeilstorch #History #PaperDetour`.
- Complete new block (24 unique tags): `#Shorts #History #PaperDetour #Birds #AnimalMigration #BirdMigration #BirdMigrationHistory #Ornithology #NaturalHistory #HistoryOfScience #WhiteStork #Storks #Swallows #Pfeilstorch #CharlesMorton #BirdMigrationTheories #Moon #17thCentury #1822 #Kluetz #CentralAfrica #Rostock #UniversityOfRostock #MigrationEvidence`.
- Kept: all six current tags. Added 18: `#Birds`, `#AnimalMigration`, `#BirdMigrationHistory`, `#Ornithology`, `#NaturalHistory`, `#HistoryOfScience`, `#Storks`, `#Swallows`, `#CharlesMorton`, `#BirdMigrationTheories`, `#Moon`, `#17thCentury`, `#1822`, `#Kluetz`, `#CentralAfrica`, `#Rostock`, `#UniversityOfRostock`, `#MigrationEvidence`. Removed: none.
- Title hashtags: `not_requested`; title stays exact. Separate YouTube Tags: `[]`.
- Usage of exact hashtags and current demand/trend: `not_checked` / `unknown`. Targeted search and direct hashtag-page attempts were made; results were irrelevant, throttled, or stale and are recorded in the consultation file.
- External result: the new full block is saved on video `UqWIwpbTMik`, confirmed by `YOUTUBE_API_READBACK_v02.json` and `YOUTUBE_METADATA_UPDATE_RECEIPT_v02.md`.
- During reconciliation, `snippet.defaultAudioLanguage` changed from `en` in the before-read to `en-US` in the later fresh read. This field was outside the requested change and its origin is unknown; it was not overwritten. All requested metadata checks passed.

## Coverage decisions

| Direction | Tags | Decision and factual basis |
|---|---|---|
| Format, brand, history | `#Shorts`, `#PaperDetour`, `#History` | Keep: correct format, navigation label and historical content. |
| Named person and theory | `#CharlesMorton`, `#BirdMigrationTheories`, `#Moon` | Add: Morton and the lunar wintering hypothesis are stated in the narration; no claim that birds actually travelled to the Moon. |
| Birds/specimen | `#Birds`, `#WhiteStork`, `#Storks`, `#Swallows`, `#Pfeilstorch` | Keep/add: species/groups named and the arrow stork is the central historical specimen. |
| Migration and field context | `#AnimalMigration`, `#BirdMigration`, `#BirdMigrationHistory`, `#Ornithology`, `#NaturalHistory`, `#HistoryOfScience` | Keep/add: the episode contrasts a past hypothesis with physical evidence and the development of knowledge about migration. |
| Time | `#17thCentury`, `#1822` | Add: both periods are explicit in the story. |
| Place and custody | `#Kluetz`, `#CentralAfrica`, `#Rostock`, `#UniversityOfRostock` | Add: find location, arrow origin, and present-day collection are stated; none asserts an exact bird route. |
| Evidence/outcome | `#MigrationEvidence` | Add: the arrow stork became the first physical evidence of long-distance migration among European birds, within the claim audit's wording. |

## Current YouTube guidance and checks

- Official Help was read on 2026-11-03: hashtags must directly relate to the content; excessive unrelated tagging can reduce relevance; more than 60 causes all hashtags to be ignored. The limit is not a goal: https://support.google.com/youtube/answer/6390658?hl=en .
- The description contains 24 unique hashtag tokens, no spaces inside tokens and no repeated/case-insensitive duplicates. No hashtag is appended to the title. No popularity or performance claim is made.
- `DESCRIPTION_EN_v02.txt` preserves the accepted narrative exactly; the only intended diff against `DESCRIPTION_EN_v01.txt` is the complete hashtag block.
- Description validator: `valid=true`; exact narrative block occurred once, and diff changed only the hashtag line.

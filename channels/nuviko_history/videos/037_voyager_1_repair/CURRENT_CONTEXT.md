# Nuviko History 037 — Voyager 1 repair

## Release state
- Exact accepted v06 MP4 is Public: https://youtu.be/-dTi-_jQPgg (video ID `-dTi-_jQPgg`, channel `UCbyLx6Rf3iWww4bPZJ2oo2A`). SHA-256: `e97e2cddfb5429817a81aa7a17bac18c890dcf4a1a1cd7dcd78771ae33d44483`. YouTube processing succeeded.
- Title A, description A with chapters/hashtags, cover A and `History Documentaries` membership (`PLCtiNAU_98r0`) were verified. The English manual SRT is `serving`; caption ID `AUieDab7FFixWIc6oHsSdh56VEi39iBnxEEgpySK_2t8VsmgjN16RFw8`.
- The approved native title+thumbnail experiment is active. Studio report displays all three approved title/cover pairs A/B/C, status “Идет проверка…”, metric “Доля во времени просмотра”, and an estimate of 13 days 23 hours remaining. Outcome is pending; no monitoring was requested.
- User approved this exact film and all three package variants; the user also confirmed the sound is good. Evidence: `Packaging/v06/USER_ACCEPTANCE_20261105.md` and `Packaging/v06/USER_AV_CONFIRMATION_20261105.md`.

## Local lifecycle
- `storage_state=PARTIAL_TEXT_ARCHIVE`. The release cleanup permanently removed 11,409 exact owned media files (3,448,183,540 logical bytes) and 37 empty episode directories. The exact hash/stat plan and per-file execution receipt are `Edit/MediaLifecycle/TEXT_ONLY_PLAN_V06.json` and `Edit/MediaLifecycle/TEXT_ONLY_EXECUTION_V06.ndjson`. Trash staging is empty. Physical APFS space reclaimed is unknown.
- Retained dependency hold: 44 v03 scene PNGs, `Source/Audio/en_v02/mix_en_v02.wav`, and the text montage plan `Edit/Production/v03/montage_en_v03.json`. The sibling `channels/nuviko_history/videos/037_voyager_1-voyager/subtitle_prepare/` still references these inputs. Release this exact hold only after that consumer is retired.
- YouTube release, caption and A/B records: `Packaging/v06/YOUTUBE_RELEASE_V06.json`.

## Current production source
- Source/edit assets for v06 were retired after publication; only the documented active v03 sibling dependencies remain. The film is recoverable from YouTube, but the previous local MP4 and generated images were permanently removed.
- Nuviko History remains frozen by default. This episode is the user-authorized exception.

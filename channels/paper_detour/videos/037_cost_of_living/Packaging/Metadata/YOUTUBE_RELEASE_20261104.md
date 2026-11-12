# YouTube release receipt — Paper Detour 037

- Video: https://www.youtube.com/watch?v=NR5YBHYPHA8 ; video ID `NR5YBHYPHA8`; channel `UCMVfdfaNxV3ZkI3_J3Eejzw`, Paper Detour, verified via authenticated API.
- Approved source: `Deliverables/037_EN_review_20261104.mp4`; SHA-256 `08148e7ed48c7928cf5a913919a8f7dfa51e5972c0aa83dedfc5ade2cf301bc4`.
- User explicitly accepted known subtitle overlap in S16 and S66 and requested upload as-is; see `USER_ACCEPTS_VISUAL_OVERLAP_20261104.md`. Visual placement FAIL remains recorded; scoped exception-aware preflight checked all other delivery requirements and used project uploader without falsifying the receipt.
- YouTube actual read-back: privacy `private`, upload status `processed`, processing `succeeded`, no reported processing/upload failure. This is not Public or Unlisted.
- Title: `Could One Wage Cover a Family's Basic Needs?`; English metadata/audio language, self-declared made-for-kids false. Full description including chapters/hashtags is in `UPLOAD_METADATA_20261104.json` and was read back from API. Chapter times were formed from audio alignment and formally validated; chapter player rendering/playback not independently verified.
- Thumbnail: previously selected `Packaging/Thumbnails/Upload/037_thumbnail_v05_07.jpg`, `WHAT COMES FIRST?`. API set accepted and thumbnail read-back matched; actual device preview not independently checked.
- Playlist: `Real Stories & Discoveries`, ID `PLEIDCTZ8y2k8`, item `UExFSURDVFo4eTJrOC41QUZGQTY5OTE4QTREQUU4`, position 24 (zero-based), membership count 1 after insertion, playlist count 25. Existing 24 items were not intentionally changed. Playlist public; video remains private.
- A/B: not launched; three prepared options in `../Experiments/AB_20261104/CONCEPTS.md`. No public release or schedule was requested or executed.

## Public и A/B — 2026-11-04 04:38 CET

- Пользователь прямо поручил открыть видео и запустить A/B. API записи и последующее чтение подтвердили `public`, `processed`, `succeeded`; playlist membership проверена до записи. [Квитанция](PUBLIC_20261104.json). Исходный MP4 и явно принятые пользователем перекрытия не менялись.
- Studio: нативное совместное тестирование трёх названий и обложек; после сохранения и публикации обновлённая форма показала «Тестирование…», отчёт — «Идёт проверка», ожидается 13 дней 23 часа, результаты отсутствуют. Варианты и hashes — `../Experiments/AB_20261104/CONCEPTS.md`, снимок — `../Experiments/AB_20261104/studio_active.png`. Первый вариант — резервный при отсутствии ясного победителя.
- Список 26 video uploads канала прочитан по API перед немедленной публикацией; публикации постов и отдельная полная очередь не проверены. Время выхода определено прямой командой пользователя, а не утверждением о свободном слоте.
- Отдельный SRT не запрашивался: субтитры встроены в MP4. Статус хранения `PARTIAL_TEXT_ARCHIVE`: файлы не удалены, pending точный inventory и проверка допустимого способа очистки.

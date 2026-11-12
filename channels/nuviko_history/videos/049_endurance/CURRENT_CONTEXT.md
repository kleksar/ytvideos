# Endurance — текущий контекст

- Nuviko History, 049, английский полный фильм. Принятый MP4 v04: `Deliverables/Endurance_en_review_v04.mp4`, SHA-256 `5cb856cda02053b40f0309a95617253a41aae457cf8d607b01eb8fbd724dc059`; приёмка и техническая проверка в `Edit/QA`.
- Опубликован Public: https://www.youtube.com/watch?v=4-LLLu-LWfY; channel `UCbyLx6Rf3iWww4bPZJ2oo2A`. API подтвердил обработку, Studio — SD/HD и доступ для всех. Плейлист History Documentaries; английская ручная дорожка `serving`.
- Стартовый комплект B; нативный парный A/B с B/A/C сохранён. Отчёт Studio показывает «Идёт проверка…»; результата ещё нет. Квитанция: [RELEASE_RECEIPT_EN_v01.md](Packaging/Metadata/RELEASE_RECEIPT_EN_v01.md).
- `PARTIAL_TEXT_ARCHIVE`: медиа остаются локально (около 5.4 GiB); проверка процессов ограничена средой, точный план и очистка не завершены. Следующее действие — безопасная адресная инвентаризация и очистка по media-lifecycle, с сохранением текстовых свидетельств и учётом других consumers.

## Cleanup 2026-11-10

User approved deletion of 1 superseded/test MP4 files (1419869551 logical bytes); exact identities and SHA-256: `Edit/MediaLifecycle/cleanup-user-approved-20261110.json`. Current published master was retained. Storage remains PARTIAL_TEXT_ARCHIVE; other work and dependencies remain.

- Cleanup 2026-11-10 (additional): nine old subtitle, hook and opening test MP4s deleted (279,746,721 logical bytes); exact identities, hashes and limitations in `Edit/MediaLifecycle/cleanup-probes-20261110.json`. Reports and commands retained; state remains PARTIAL_TEXT_ARCHIVE.

# 032 — Galveston, 1900: Raising a City

Адаптация англоязычного длинного фильма `017_galveston_1900` для канала **Paper Detour**. Пользователь выбрал существующую запись Odom и поручил переработать визуальный ряд и создать бумажные акцентные титры.

## Принятый источник

- Сценарий: `channels/nuviko_history/videos/017_galveston_1900/Source/Scripts/film_en.txt`.
- Озвучка: `channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en_105.wav` (1.05× уже применено; в новом монтаже использовать на 100%).
- Связанные alignment, SRT и QA лежат рядом с WAV в источнике. Текст совпадает с alignment; локальные тайминги и произношение ещё не проверены на слух.
- Исторические оговорки и ссылки: `channels/nuviko_history/videos/017_galveston_1900/Source/Scripts/fact_check.md` и `archive/legacy_stories/research/2026-10-29-galveston-fact-dossier.md`.

## Текущий final — Private YouTube, 2 ноября 2026

Готовый полный EN фильм **Galveston: The City That Raised Its Ground** загружен на Paper Detour: **https://www.youtube.com/watch?v=EP0a0bX4eFo**, ID `EP0a0bX4eFo`, канал `UCMVfdfaNxV3ZkI3_J3Eejzw`. API подтверждает **Private**, processing `succeeded`; Studio подтверждает закрытый доступ и завершённые SD/HD; свежий YouTube fileDetails подтверждает2560×1440/30fps/H.264/stereoAAC и точный размер файла. Доступ Public/Unlisted и расписание не устанавливались.

Актуальная выдача: [MP4](Deliverables/032_galveston_en_final_v02.mp4), 574.433 с, 17233 кадра, 2560×1440/30 CFR, SHA-256 `a43d6f6b7d77440ed949280a9cd5ce263f7e16e2a6ed6fafead9c2ab9a52960a`; [EN SRT](Deliverables/032_galveston_en_v02.srt),179cues/1514слов,SHA `7d2058c3325166b2e42db602db3659c301c6f02c69988e11e352a8332644316b`. Точные pointers — Deliverables/current.json.

Новая раскадровка v02:129 цельных бумажных сцен, каждый план4–6с, прямые склейки, 16анимированных смысловых акцентов. Церковный блок: действительный архивный снимок CH01, общий подъём CH02, макро домкрата CH03, согласованная работа людей CH04, целая церковь CH05. Все сцены получили разрешённые движения камеры/depth parallax и G08. Canonical run `19fd8c3ec5f28ece170b` COMPLETE, project `25533909`, final timeline `02A15052`; still baseline `9A5FE055` сохранена. Native job `DBEDD6B8-56E7-4984-8495-407E1C16B0D1` completed. Прежний AAC скопирован без перекодирования, Odom-запись сохранена, новый звук не создавался.

Требуемый offline QA **PASS**: полный decode17233кадра, технический контракт/свежесть, все129сцен/16акцентов/179SRTcues по1373фактически просмотренным контрольным кадрам;267дополнительных roof-ROI кадров исправленных CH02/CH05 просмотрены целиком по интервалам. v03 был отклонён из-за верхушек башни, v04 дефект закрывает. Проверка движения всех129сцен, R028 отдельный recheck. Это выборочная проверка полных кадров, не непрерывный просмотр. [QA](Edit/QA/full-v04/REPORT.md),[receipt](Edit/QA/full-v04/reviewer_receipt.json). Субъективное прослушивание/слуховой sync **UNVERIFIED**, независимый reviewer **NOT_PERFORMED**, playback **NOT_REQUIRED** канальным профилем.

Упаковка: принятая обложка `Packaging/Thumbnails/032_galveston_cover_upload_v01.jpg` (WHERE’S THE GROUND?) записана API и проверена в обновлённой Studio. Итоговые title/description/10hashtags/12Tags/языки/category27/made-for-kidsfalse сверены API. False synthetic не возвращён API; в Studio radio «Нет» checked, без повторной mutation. 10глав **machine-checked** по ASR фактического finalMP4 и кадрам всех границ; отображение глав плеером отдельно **UNVERIFIED**. Дорожка EN manual serving; скачана API, все179текстов и таймингов совпали (delta0). Real Stories & Discoveries `PLEIDCTZ8y2k8`: добавлен девятым(position8), прежние8членств и порядок сохранены, плейлистPublic. [Release receipt](Packaging/Metadata/release_api_verification_v02.json). Старый motion-review MP4 сохранён как источник принятого AAC/сравнение, он больше не current.

## Источники постановки и историческое состояние

Актуальная раскадровка: `Storyboard/storyboard_v02.md`/`.json`. Принятый план доработки по эталону030: `Edit/EditorialReview_030_20261102/REVIEW_AND_REVISION_BRIEF_v01.md`; разрешение продолжать032безExtraHigh записано в CURRENT_CONTEXT. Ранние128сцен/14титров/no-grain версии являются историческими и не определяют текущий финал.

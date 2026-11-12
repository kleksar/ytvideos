# Paper Detour — распределение плейлистов

Завершено 2 ноября 2026 (Europe/Belgrade). Финальная API-сверка: **2026-11-01 23:57:06 UTC**. Канал `UCMVfdfaNxV3ZkI3_J3Eejzw`, владение проверено через `channels.list(mine=true)`; использован существующий management scope без новой OAuth-авторизации. Основание внешних изменений — прямое поручение пользователя создать навык и распределить все ролики Paper Detour.

## Сохранённый результат

| Подборка | Доступ | Видео в фактическом порядке |
|---|---|---|
| [Real Stories & Discoveries](https://www.youtube.com/playlist?list=PLEIDCTZ8y2k8) | Public | `0RaC4t7yn5o`, `85dwIXy_lZs`, `7DygREwtxfY`, `r71aCn4p88A`, `orQiLIvOL-8` |
| [Legends & Personal Stories](https://www.youtube.com/playlist?list=PLa2eDoWjSKkA) | Public | `pdSgHe6ScTI`, `WQw7ny9svrk`, `sA-PYrDl5H8` |
| [Digital Life & Attention](https://www.youtube.com/playlist?list=PLCAXo3w7Gths) | Public | `-KW8jgSoEz0`, `WQw7ny9svrk` |
| [Reported IQ Estimates](https://studio.youtube.com/playlist/PLOSBLM3rTTl0/edit) | Private | `xYS2XBeR_Jc` |

**10 из 10 сюжетных видео распределены**, 11 членств: Joshua/Jessica имеет два осмысленных маршрута. Нулевая техническая unlisted-трансляция `QqMudxBNZgo` учтена и исключена. Добавлены два членства, удалений и перестановок прежних элементов нет. В каждой подборке дубликатов нет. Создана одна заполненная IQ-подборка; её Private не меняет Public самого видео. Новая подборка не публиковалась, доступ трёх прежних сохранён.

Расширено только описание Digital Life: теперь оно включает AI companions и digital relationships, что делает новое членство Joshua/Jessica понятным. IQ-подборка сохраняет статус разнородных опубликованных оценок; одноэлементный старт — явное редакционное исключение из прежнего ориентира двух выпусков. У радио сохранён единый кластер «фильм + два поддерживающих Short», без искусственной новой рубрики из трёх версий одной истории.

## Доказательства и восстановление

- [BEFORE.json](BEFORE.json), [AFTER.json](AFTER.json): все страницы uploads, playlists, memberships и метаданные видео. [PLAN.json](PLAN.json): назначения каждого ID, причины, порядок и минимальные изменения. [VALIDATION.json](VALIDATION.json): итоговая сверка.
- [Описание Digital](digital_metadata_receipt.json): единственный API PUT, описание и `defaultLanguage=en` подтверждены чтением. Членство Joshua: первоначальный [HTTP 400 manualSortRequired](digital_add_receipt.json) разрешён через [снимок без нового членства](AFTER_REJECTED_POSITION.json), затем [проверку и сохранение Manual в Studio](STUDIO_SORTING.md); отдельный [API insert после исправления](digital_add_manual_receipt.json) подтверждён.
- [Создание IQ](iq_create_receipt.json): один POST. Первый by-ID GET ещё не вернул ресурс; [полный read-only inventory](AFTER_CREATE_RECONCILIATION.json) подтвердил единственный новый ID, точное название/описание/English/Private. Повторного создания не было. [Добавление IQ Gallery](iq_add_receipt.json): один POST, фактическое членство/позиция подтверждены.
- Studio отдельно показала Manual для всех четырёх и итоговые количества **5 / 3 / 2 / 1**, три Public и одну Private: [скриншот итоговой таблицы](PLAYLISTS_AFTER_STUDIO.png). Прямые страницы открывались по известным IDs; сохранение default sorting mode выполнено через UI, поскольку поле отсутствует в API-схеме.

Тексты/главы/метки и отдельные Tags видео, категория, языки, `status` и `contentDetails` совпали before/after; для `snippet` сравнивались исходные поля, производный `localized` исключён. `videos.update` не вызывался. Все десять редакционных видео остались public, техническая трансляция unlisted. Проверка не включает локализации, полный просмотр/прослушивание, AV QA или независимый фактчек. Была самопроверка координатора; отдельного reviewer не было.

API `defaultLanguage=en` подтверждён для всех четырёх. Только у Digital Studio English был явно выбран и сохранён; у остальных трёх chooser показывал «Выбрать», несмотря на API `en`. Это расхождение сигналов записано, соответствующие формы не менялись. Полная сверка членств и порядка от этого не зависит.

## Навык и автоматический маршрут

Создан переносимый [ytv-youtube-playlists](../../../.agents/skills/ytv-youtube-playlists/SKILL.md) и [профиль Paper](../../../.agents/skills/ytv-youtube-playlists/references/paper-detour.md). Навык владеет архитектурой, критериями, последовательностью, полной сверкой каталога и контрактом передачи. IDs/состояние остаются в [реестре](../../docs/YOUTUBE_PLAYLISTS.md), generic API mechanics — у глобального [youtube-upload](/Users/diplomat/.codex/skills/youtube-upload/SKILL.md). В нём закреплена процедура `manualSortRequired`; рабочая справка API указывает точную границу Studio.

Bootstrap, каталог, карта владельцев, Paper AGENTS, production/runbook/handoffs и release теперь вызывают нового владельца. Для одного нового фильма выбор плейлиста и позиции готовится автоматически вместе с упаковкой. При порученном релизе video ID разрешается и членство доводится до read-back без нового вопроса; при локальной выдаче сохраняется план без внешней записи. Старое требование private для уже опубликованных трёх подборок удалено из release. Публичность будущих подборок/видео не наследует разрешение этого прохода.

Skill создан по системному skill-creator и прошёл quick_validate. Entry-point installer проверил **47 входов**, без новых ссылок/router-файлов. Native `skills/list` в доступном наборе tools отсутствует: фактический будущий выбор навыка моделью не объявляется протестированным. [Процедурная консультация](../../../.agent/consultations/paper_playlist_procedure_20261102.md) и [консультация распределения](CONSULTATION.md) прочитаны координатором в Chrome Extra High; консультация не заменяет первоисточники или пользовательскую приёмку нового названия.

Технический исполнитель [apply_scoped_change.py](apply_scoped_change.py) привязан только к принятому плану этого аудита и сохраняет receipts; это не универсальная команда для новых выпусков. Повторный запуск уже выполненной операции блокируется наличием квитанции. Первичная проверка создания остановилась на временно пустом GET; код теперь допускает ограниченные read-only ожидания, а текущий результат подтверждён отдельной сверкой без повтора POST.

Механика сверена с первичными источниками: [playlist resource](https://developers.google.com/youtube/data/reference/rest/v3/playlists), [playlist insert](https://developers.google.com/youtube/data/reference/rest/v3/playlists/insert), [playlist update](https://developers.google.com/youtube/data/reference/rest/v3/playlists/update), [item insert](https://developers.google.com/youtube/data/reference/rest/v3/playlistItems/insert) и [item update](https://developers.google.com/youtube/data/reference/rest/v3/playlistItems/update). Эти документы подтверждают API-возможности; причинный рост просмотров от распределения не измерялся и не обещается.

Следующий этап принятого плана: переносимые владельцы названий и описаний, затем изображения/обложки, A/B/аналитика и полный пилот. Текущий проход не запускает эти отдельные производства и не меняет упаковку видео.

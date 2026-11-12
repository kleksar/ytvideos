# Пункт 3 — распределение и описания плейлистов

- Дата: 2026-11-02; Paper Detour `UCMVfdfaNxV3ZkI3_J3Eejzw`.
- Статус: **DONE / saved_verified / public visual verified**. После подготовки пользователь явно ответил «Открыть и добавить на главную»; Science & What If теперь **Public**, Home-секция добавлена и проверена.
- Поручение: продолжить улучшения канала по пунктам, текущий пункт — распределить два неназначенных ролика и исправить старое `handmade` в описаниях. Extra High временно отменён прямым указанием пользователя. Делегирования не было.
- Процедуры: root/channel preflight, `ytv-youtube-playlists` с Paper-профилем, `ytv-youtube-release`, `youtube-upload`, API README и текущие официальные схемы playlists.insert/update и playlistItems.insert.

## Сохранённые изменения

1. Real Stories & Discoveries `PLEIDCTZ8y2k8`: из описания удалено только слово `handmade`; английская локализация синхронизирована. Рак-богомол `Bfgcq4rxQT8` добавлен последним, API position11. Все прежние 11 membership IDs и их порядок сохранены.
2. Legends & Personal Stories `PLa2eDoWjSKkA`: из описания удалено только `handmade`; английская локализация синхронизирована. Четыре прежних членства сохранены. Обе подборки остались Public.
3. Создан **Science & What If**, `PLebMpVlzs-vY`, [ссылка](https://www.youtube.com/playlist?list=PLebMpVlzs-vY), English, **Private**. Последовательно добавлены только существующие публичные финальные версии:
   - `Bfgcq4rxQT8` — Mantis Shrimp Evolution: Spear or Hammer?
   - `UkwqGIqvink` — They Shared a Burrow for 250 Million Years.
   - `YRnIpr9P3iE` — What If Time Stopped for 5 Seconds? #Shorts.

Описание новой подборки:

> Surprising stories from evolution and prehistoric life, alongside imaginative what-if questions about physics. Explore natural history and thought experiments through paper-diorama worlds.

Эволюция и палеонтология дают тематический научный маршрут; условный эксперимент явно отделён названием и описанием от реальных событий. Для Real Stories остановка времени исключена. Два научных сюжета осмысленно пересекаются с более широкой подборкой открытий. Решение основано на текущих материалах 033/035/036 и свежих API-описаниях, а не на slug. Пустых будущих рубрик и альтернативных private-версий не добавлялось.

## Проверка

- [Полный before](before.json): 25 uploads/videos, 17 Public, 4 исходных плейлиста и полные участники, все секции Home. Фактическая OAuth-авторизация проверена по единственному channel ID, существующий scope `youtube.force-ssl`; расширения доступа не было.
- [План](plan.json), отдельные request/receipt/read-back каждой операции. Два PUT описаний, один POST создания, четыре POST членств; каждый выполнен один раз. Все семь операций получили успешный ответ и точную проверку API перед зависимым шагом. При временном старом read-back повторялись только чтения.
- [After до решения о публичности](after-preapproval.json), [формальная проверка](validation-preapproval.json): все 13 проверок PASS. Все video snippet/status/contentDetails совпали с before; исходные channel поля и Home-секции сохранены. Исходные playlist IDs, имена, доступ, языки и прежние участники/порядок сохранены; отличия описаний и добавлений точно соответствуют плану. Дубликатов внутри подборок нет.
- Покрытие: 17/17 Public видео имеют хотя бы одну подборку, неназначенных 0. В публичных подборках пока 15/17: time stop находится в новом Private Science, IQ — в прежнем Private IQ. Это разница между назначением и публичной навигацией, не изменение доступа самих видео.
- Insert-запросы не содержали `snippet.position`; текущий полный API-порядок проверен. Studio sorting-mode в этом ходе не проверялся, Manual не заявлен как подтверждённый.
- Исправленные оба описания прочитаны на публичной Home: [DOM](public-home-dom-preapproval.txt), [снимок](public-descriptions.jpg). Новая закрытая подборка подтверждена API; публичный preview для неё ещё неприменим.

## Последнее решение

Полностью подготовленная новая подборка сначала создана Private по действующему Paper-профилю: «For a genuinely new collection without an explicit access decision use Private». Затем пользователь явно ответил **«Открыть и добавить на главную»**. [Точный вопрос и ответ](public-authorization.json).

Выполнены и read-back проверены один `playlists.update` с Public и сохранением title/description/defaultLanguage/podcastStatus и один `channelSections.insert`: section ID `UCMVfdfaNxV3ZkI3_J3Eejzw.aqsRo9JYx5M`, позиция4, сразу после Real Stories. Все остальные секции сохранили относительный порядок; всего10 секций API. [Текущее состояние подборки](science-current.json), квитанции `publish-science-receipt.json` и `home-science-receipt.json`. Доступ самих видео не менялся.

Финальная сверка: [after.json](after.json), [validation.json](validation.json). Метаданные плейлистов, полные membership IDs/позиции/состав и Home точно совпали с согласованным результатом; channel поля и video metadata/status/contentDetails сохранились. Буквальное сравнение всех полей видео/playlist items отмечено false из-за **45 изменений query-параметров ссылок на private-превью** (`sqp`/`rs`): scheme/host/path, размеры и все остальные поля совпали. [Полный diff](preserved-fields-differences.json). Пиксели этих private-превью не сравнивались; thumbnail mutations не выполнялись. Эти расхождения не затирались и не исправлялись повторной записью.

Публичная проверка из браузерного аккаунта, не являющегося владельцем Paper: новая подборка открывается, видны три правильных видео в заданном порядке, название и описание; [снимок](science-public.jpg), [DOM подборки](science-public-dom.txt). На свежей Home виден порядок Real Stories → Science & What If → Legends → Digital; [DOM Home](public-home-dom.txt).

Окончательное покрытие: 17/17 Public видео назначены хотя бы в один плейлист, неназначенных0. Через Public-подборки доступны16/17; IQ `xYS2XBeR_Jc` остаётся только в прежней Private IQ-подборке по сохранённой политике. Непубличные альтернативы, техническая трансляция и их доступ этим действием не менялись.

Следующий общий пункт после завершения этого решения — проверить handle Paper Detour и подготовить точный вариант; не переименовывать наугад и не менять страну CY.

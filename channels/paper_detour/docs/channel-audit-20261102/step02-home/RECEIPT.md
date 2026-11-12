# Пункт 2 — главная Paper Detour

- Дата: 2026-11-02. Канал `UCMVfdfaNxV3ZkI3_J3Eejzw`, [публичная главная](https://www.youtube.com/channel/UCMVfdfaNxV3ZkI3_J3Eejzw).
- Статус: **DONE / saved_verified / public visual verified**.
- Поручение: пользователь одобрил улучшения по пунктам, затем «поехали» после плана, начинающегося с главной страницы. Прямое указание временно не использовать Extra High сохраняется; консультации в этом проходе не вызывались. Страну пользователь поручил оставить без изменений.
- Процедуры: root/channel preflight, `ytv-youtube-playlists` с Paper-профилем, `ytv-youtube-release`, глобальный `youtube-upload`, README API-адаптера. Делегирования не было.

## Что сделано

Через `channelSections.insert(part=snippet,contentDetails)` добавлены три секции `singlePlaylist` сразу после существующего блока последних длинных видео:

| Позиция API, с нуля | Подборка | Playlist ID | Section ID |
|---|---|---|---|
| 3 | Real Stories & Discoveries | `PLEIDCTZ8y2k8` | `UCMVfdfaNxV3ZkI3_J3Eejzw.iJLXf_7B368` |
| 4 | Legends & Personal Stories | `PLa2eDoWjSKkA` | `UCMVfdfaNxV3ZkI3_J3Eejzw.UgY69lf0UCE` |
| 5 | Digital Life & Attention | `PLCAXo3w7Gths` | `UCMVfdfaNxV3ZkI3_J3Eejzw.ebKlgRwnpFY` |

Существующие шесть секций сохранены, их относительный порядок и содержимое сохранены. Последующие позиции сместились вниз на три. API сообщает тип `channelsectiontypeundefined` для пяти существующих современных блоков; их типы не угадывались и не переписывались.

Публично проверенный порядок: Для вас → Shorts → Видео → Real Stories & Discoveries → Legends & Personal Stories → Digital Life & Attention → Записи. Пустые блоки могут не отображаться зрителю.

## Подтверждения

- [Исходное состояние](before.json): проверена фактическая OAuth-авторизация ровно целевого канала; existing scope `youtube.force-ssl`. Дополнительные права не выдавались. Получены все 4 подборки и полные списки участников; три целевые принадлежат каналу и Public.
- [План](plan.json), три отдельных `insert-N-request.json`, `insert-N-receipt.json` и read-back. Каждый POST выполнен один раз, каждый вернул HTTP 200, каждая секция проверена чтением до следующей mutation. Дубликатов не создано.
- [Финальное состояние](after.json), [проверки](validation.json): точный набор и порядок всех 9 API-секций; исходные channel snippet/branding/status; метаданные, доступ, количество, item IDs и порядок всех плейлистов совпали с before. Закрытая IQ-подборка не выведена.
- Публичная страница сначала показывала старую структуру; после ограниченных read-only проверок и reload показала все три секции с правильными playlist-ссылками. Повторных записей из-за кеша не было. [DOM](public-home-dom.txt), [вид секций](public-home.jpg), [полная страница](public-home-full.jpg).
- Попытка read-only Studio по точному channel ID показала отсутствие доступа у текущего браузерного аккаунта. Ссылка выбора открыла служебную страницу; аккаунты/роли/доступы не менялись. Studio write не требовался: операция полностью поддерживается официальным Data API и завершена через него.
- Справка метода: https://developers.google.com/youtube/data/reference/rest/v3/channelSections/insert ; схема/позиции: https://developers.google.com/youtube/data/reference/rest/v3/channelSections .

Видео, доступ видео, публикации, A/B, описания плейлистов и внутреннее членство не изменялись этим шагом. Проверка отдельных текущих video statuses не входила в этот проход.

## Следующий пункт

Распределить mantis shrimp и time stop по содержанию. При проверке навигации обнаружено, что исходные описания Real Stories и Legends всё ещё используют `handmade paper-diorama films`; это не было изменено в узком Home-шаге. При следующем проходе описаний заменить двусмысленную производственную формулировку на описание визуального стиля, сохранив документальные/легендарные границы подборок.

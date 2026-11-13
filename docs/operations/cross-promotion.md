# Cross-promotion — проверяемые действия после выпуска

Этот документ описывает **выполнение**, не заменяет владельца требований [release](../standards/release.md).
Shorts → Long, Community Posts, End Screens и плейлисты не запускаются от одного предположения или наличия draft.
Права, связанный исходный run и ограничения канала сохраняются по действующему workflow.

## Подготовка

1. После выхода и подтверждения фактического Public получить актуальный снимок YouTube/Studio по **точному** channel ID и video ID. В нём должны быть `channel_id`, `source` (`api_readback`/`studio_readback`), offset-aware `observed_at`, `videos` (`id`, `channel_id`, `privacy`, проверенный `format`) и `playlists` (`id`, `channel_id`, `privacy`). Для плейлиста при проверке членства нужны `members_complete=true` и полный `video_ids`. Для лонгового target у Shorts формат `long` должен быть проверен по фактической поверхности; одного значения duration недостаточно.
2. Неизвестный видео-ID, чужой канал, не-public/unlisted destination, непроверенный плейлист → **blocker**, а не автоматически выбранная замена. Отбирать семантически близкую цель редакционно. Не создавать/раскрывать private long ради ссылки.
3. Выполнить read-only предварительную проверку:

```bash
uv run ytv cross-promotion-plan --release-spec /path/to/release.json \
  --inventory /path/to/youtube-inventory.json --video-id EXACT_VIDEO_ID
```

План содержит `release_sha256`, timestamp inventory, точные targets, blockers и `ready_for_host` / `already_present`. Это **не** reservation, execution, permission, API result или подтверждение живого YouTube. Сохранить план как supporting artifact, привязать к run и video ID.

## Провайдер и read-back

| Действие | Платформа | Проверка результата |
|---|---|---|
| Shorts → Long | Studio `Related video`: точный Short и тематический long этого канала; destination Public/Unlisted; нужна функция advanced features | Перечитать конкретное поле **Related video** у Short, сверить ID |
| Community Post | Поддерживаемый Studio UI adapter; отдельный оригинальный текст, приложенный собственный video ID, только после verified Public | Перечитать фактический post ID, текст, вложенное видео и privacy/visibility |
| End Screen | Studio editor; long ≥25 c, элемент внутри последних 5–20 c, не Made for Kids; фактические целевые ID | Перечитать все native elements/target IDs; нарисованный фон не заменяет кликабельные элементы |
| Плейлист | Data API `playlistItems.list/insert`, только проверенный owner; только нужное membership | До insert прочитать **все страницы**; после операции прочитать membership и item ID; UNKNOWN не повторять вслепую |

Все мутации выполняет доверенный host с реальной авторизацией и reserve → dispatch → read-back. Helper `automation/youtube/add_to_playlist.py` поддерживает точную ожидаемую privacy: `private` по умолчанию для release и явную `--expected-privacy public` для опубликованного ролика. Сам helper не обходит authorization/approval workflow.

Community Post подготавливается как `ReleaseSpec.community_post = {"text": "..."}` (необязательное поле); после verified schedule core сохраняет `community_post` deferred action с зависимостью `verify_public` и точным video ID. Это не работающий dispatcher и не повод утверждать, что пост появился. Не использовать неофициальные/выдуманные endpoint YouTube Data API для создания posts, Studio end screens или Shorts related videos.

## Выбор и частота

Применять только содержательно нужные связи: Short должен быть самостоятельным, long — раскрывать дополнительный материал; Community Post — отдельная причина посмотреть, а не дублирование title; End Screen — логичное продолжение истории; playlist — тематически точная подборка. Не добавлять обязательный пост для **каждого** видео и не считать post/image-only работу подтверждением роста просмотров. Календарь постов и Shorts сверять с занятыми слотами, не вводить универсальный интервал.

Записывать исходные/новые public metrics и источники трафика в одинаковые окна. Рост long нельзя целиком приписывать Short без доказательств переходов. Если capability отсутствует — оставить задание с доказанным blocker, не замещать простым URL в описании и не объявлять его полноценной Studio-связью.

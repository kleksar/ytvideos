# Cross-promotion — проверяемые действия после выпуска

Этот документ описывает **выполнение**, не заменяет владельца требований [release](../standards/release.md).
Related video у Shorts, Community Posts, End Screens и плейлисты не запускаются от одного предположения или наличия draft.
Права, связанный исходный run и ограничения канала сохраняются по действующему workflow.

## Подготовка

1. После выхода и подтверждения фактического Public получить актуальный снимок YouTube/Studio по **точному** channel ID и video ID. В нём должны быть `channel_id`, `source` (`api_readback`/`studio_readback`), offset-aware `observed_at`, `videos` (`id`, `channel_id`, `privacy`, проверенный `format`) и `playlists` (`id`, `channel_id`, `privacy`). Для плейлиста при проверке членства нужны `members_complete=true` и полный `video_ids`. Для Related video у Shorts формат цели `short` или `long` должен быть проверен по фактической поверхности; одного значения duration недостаточно. Неизвестный формат и `live` этим helper не поддерживаются.
2. Неизвестный видео-ID, чужой канал, не-public/unlisted destination, непроверенный плейлист → **blocker**, а не автоматически выбранная замена. Отбирать семантически близкую цель редакционно. Не создавать/раскрывать private видео ради ссылки.
3. Выполнить read-only предварительную проверку:

```bash
uv run ytv cross-promotion-plan --release-spec /path/to/release.json \
  --inventory /path/to/youtube-inventory.json --video-id EXACT_VIDEO_ID
```

План содержит `release_sha256`, timestamp inventory, точные targets, blockers и `ready_for_host` / `already_present`. Это **не** reservation, execution, permission, API result или подтверждение живого YouTube. Сохранить план как supporting artifact, привязать к run и video ID.

Контракт `ytv-cross-promotion-plan-v1` сохраняет существующий long action `shorts_to_long` с payload `{short_id, long_id}`. Для подтверждённой short-цели добавлен `shorts_to_short` с `{short_id, target_short_id}`; `ReleaseSpec.related_video_id` остаётся общим входом. Сохранённые планы не переименовывать и не превращать в разрешение на новую цель. Host должен явно поддерживать новый action перед исполнением; неизвестный action — blocker, не fallback к long-маршруту. Для новой цели получить свежий inventory и новый план; перед любой мутацией всё равно необходим read-back.

## Провайдер и read-back

| Действие | Платформа | Проверка результата |
|---|---|---|
| Shorts → Short/Long | Studio [Related video](https://support.google.com/youtube/answer/14075157?hl=en): точный Short и тематический Short или long этого канала; destination Public/Unlisted; нужна функция advanced features | Перечитать конкретное поле **Related video** у Short, сверить ID |
| Community Post | Поддерживаемый Studio UI adapter; отдельный оригинальный текст, приложенный собственный video ID, только после verified Public | Перечитать фактический post ID, текст, вложенное видео и privacy/visibility |
| End Screen | Studio editor; long ≥25 c, элемент внутри последних 5–20 c, не Made for Kids; фактические целевые ID | Перечитать все native elements/target IDs; нарисованный фон не заменяет кликабельные элементы |
| Плейлист | Data API `playlistItems.list/insert`, только проверенный owner; только нужное membership | До insert прочитать **все страницы**; после операции прочитать membership и item ID; UNKNOWN не повторять вслепую |

Все мутации выполняет доверенный host с реальной авторизацией и reserve → dispatch → read-back. Helper `automation/youtube/add_to_playlist.py` поддерживает точную ожидаемую privacy: `private` по умолчанию для release и явную `--expected-privacy public` для опубликованного ролика. Сам helper не обходит authorization/approval workflow.

Community Post подготавливается как `ReleaseSpec.community_post = {"text": "..."}` (необязательное поле); после verified schedule core сохраняет `community_post` deferred action с зависимостью `verify_public` и точным video ID. Это не работающий dispatcher и не повод утверждать, что пост появился. Не использовать неофициальные/выдуманные endpoint YouTube Data API для создания posts, Studio end screens или Shorts related videos.

## Выбор и частота

Применять только содержательно нужные связи: исходный Short должен быть самостоятельным, целевой Short или long — раскрывать дополнительный материал или другой угол темы. Целевой Short также даёт собственную отдачу; ссылка не заменяет финал исходного ролика. Community Post — отдельная причина посмотреть, а не дублирование title; End Screen — логичное продолжение истории; playlist — тематически точная подборка. [Сюжетный мост](../standards/editorial.md#сюжетный-переход-к-следующему-видео) планируется для каждого нового видео с адаптацией формата, но не требует отдельного поста, нового Short или нерелевантной обязательной цепочки. Не считать post/image-only работу подтверждением роста просмотров. Календарь постов и Shorts сверять с занятыми слотами, не вводить универсальный интервал.

Записывать исходные/новые public metrics и источники трафика в одинаковые окна. Рост целевого видео нельзя целиком приписывать исходному Short без доказательств переходов. Если capability отсутствует — оставить задание с доказанным blocker, не замещать простым URL в описании и не объявлять его полноценной Studio-связью.

# YouTube adapters

Для новых runs использовать guarded application path из `src/ytvideos`, который проверяет exact MP4 approval, channel/scope/revision, lease и unique operation key. Здесь сохранены технические средства YouTube Data API; прямой legacy CLI не является альтернативным lifecycle или способом обойти guard.

Редакционная полнота/полномочия/два gates — [release standard](../../docs/standards/release.md). После MP4 approval полный производственный запрос включает завершение оформления и schedule по канальной политике; обычный промежуточный Unlisted review не требуется.

## Авторизация и capabilities

Проверить OAuth пользователя для точного channel ID, необходимые scopes и собственные tokens каждого канала. Credentials хранить вне Git/модельного context. Service accounts и Studio delegation не считать подтверждением API owner access. Смена аккаунта требует новой проверки фактического канала, не догадки по названию.

Google Cloud/API configuration, quota и возможность публикации проверяются для действительного проекта. Не выводить их из названия connector или успешной локальной валидации. Default upload privacy не использовать: передать Private явно. Историческое forced-private ограничение unverified проектов не является текущей защитой.

| Операция | Средство / проверка |
|---|---|
| OAuth, private upload, status, thumbnail | `upload.py`; exact channel и resumable state |
| Manual captions | `upload_caption.py` / `upload_caption_language.py`; exact SRT, язык, serving/not draft |
| Schedule read/set | `schedule.py`; Private, never-published applicability, future time, ETag/read-back |
| Playlist membership | `add_to_playlist.py`; проверить существующий item и ограничения helper |
| Исторические узкие privacy/public действия | `prepare_unlisted.py`, `publish_public.py`; только свой явно разрешённый scope |
| Нативные end screen/related video/A/B | Capability-driven Studio adapter, если public API нужное действие не предоставляет |
| Analytics | Отдельные scopes/API или Studio read-only; counters не заменяют retention report |

Точный синтаксис текущей команды получить через `--help`. Не выдавать отсутствие метода в этом helper за отсутствие функции платформы; и не придумывать endpoint, которого нет в поддержанном интерфейсе.

## Upload и recovery

До отправки подтвердить exact media SHA-256, delivery receipt, authorization и уникальную operation запись. `upload.py` сохраняет resumable session/offset/video ID и использует bounded retry. Сохранённый state file и его flock защищают этот путь; общая уникальность между хостами принадлежит transactional application store.

При restart использовать тот же operation/handle и проверенный файл. Timeout после отправки последнего chunk означает UNKNOWN до reconciliation. Не создавать вторую загрузку в другом каталоге/сессии. Не удалять state, чтобы заставить helper начать заново. Read-back фиксирует channel, video ID, privacy, processing и полученную версию.

Старый `--stage-private` разрешал ограниченный staging до отдельных checks; новые guarded runs не используют его для обхода пользовательского MP4 gate. Исторические receipt formats проверяются на import; отсутствие frozen provenance не восстанавливается из текущего Git HEAD.

## Оформление

После processing succeeded можно ставить custom thumbnail Shorts. Проверить реальный file/result; обложка не является декодированным кадром MP4 по умолчанию. Сохранять exact assets и read-back.

Metadata update выполняет read → merge нужных полей изменяемого part → schema/ETag → write → read-back. Непереданное поле внутри заменяемого part может быть очищено. Tags сравнивать по документированным нормализациям без скрытия потерянных значений. Не менять privacy ради доступности отдельного helper.

Субтитры: upload manual track, прочитать статус/language/ID/draft; failed или draft не проходит completion. Playlist: проверить владельца, доступ, sorting и уже существующее membership. При неизвестном insert outcome сначала читать состав. `manualSortRequired` не оправдывает слепой повтор; режим Studio проверяется отдельно.

## Schedule и post-publication

Перед `set` перечитать календарь/слоты, privacy и applicability конкретного video ID. Передать future RFC3339/timezone; дата в прошлом запрещена, поскольку не означает безопасную отложенную публикацию. Использовать исходный upload receipt/caption evidence, не произвольную новую сводку.

После mutation перечитать сохранённые значения. Локальный `plan` helper не назначает даты в YouTube и не является универсальным календарём каналов. Фактический Public и A/B — последующие задачи; в private/scheduled нативный A/B не запускается. Pending task без доступного executor не является действующим фоновым мониторингом.

## Проверка

`python3 -m unittest discover -s automation/youtube -p 'test_*.py'` проверяет локальные контракты/mock cases. Live upload/schedule тестируются только на разрешённом control episode с реальными credentials/policy, отдельно от MR unit suite.

Текущие первичные сведения о полях, quotas, thumbnails, resumable и release restrictions перечислены в [release standard](../../docs/standards/release.md#актуальность-платформы). При изменении контракта adapter сверить их заново.

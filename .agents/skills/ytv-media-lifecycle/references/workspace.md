# Workspace CLI

Этот CLI описывает обычную рабочую очистку. Отклонённый MP4 и архивирование завершённого выпуска выполняются по [действующему lifecycle](../SKILL.md); [TEXT_ONLY](text-only-archive.md) имеет отдельный exact plan и не добавляет несуществующую CLI-команду.

Python 3.10+, stdlib, POSIX file lock. Из root:

```sh
python3 .agents/skills/ytv-media-lifecycle/scripts/workspace.py --episode /absolute/episode init
python3 .agents/skills/ytv-media-lifecycle/scripts/workspace.py --episode /absolute/episode start --run render-v02 --owner actual-owner
```

`init` создаёт только отсутствующие layout directories и `Edit/MediaLifecycle/layout.json`, не переносит существующие файлы. Новый run создаётся эксклюзивно: `Work/<run>/manifest.json`, `scratch`, `previews`. Owner должен совпадать во всех последующих вызовах. Запись metadata защищена lock; наличие lock не доказывает отсутствие сторонних writers. Контролируемый writer держит run active до действительного окончания, включая завершение subprocess/background jobs.

## Роли и состояния

```sh
python3 .agents/skills/ytv-media-lifecycle/scripts/workspace.py --episode /absolute/episode register \
  --run render-v02 --owner actual-owner --path Work/render-v02/scratch/native.h264 \
  --role scratch --rebuild-from Work/render-v02/previews/native.mp4 --evidence Edit/QA/stream-proof.json
python3 .agents/skills/ytv-media-lifecycle/scripts/workspace.py --episode /absolute/episode finish \
  --run render-v02 --owner actual-owner --status complete --writer-finished
```

`register` сохраняет exact path, role, stat/hash и fingerprints reconstruction inputs/evidence. Пути confined episode, symlinks/escape запрещены. `scratch` требует существующие rebuild/evidence; их наличие не доказывает правильность рецепта — её проверяет координатор. `dependency` размещается в Assets/Generated, `evidence` в Edit, `preview` в previews своего run. Повторная регистрация не перезаписывает entry. Для новых версий использовать другой путь/run.

Состояния: active → complete/failed/abandoned. `--writer-finished` фиксирует выполненную проверку, не завершает процессы сам. Complete не означает QA/приёмку. Failed/abandoned сохраняются для разбора.

Preview по умолчанию pending и не удаляется clean. Если он явно отклонён, передать `register --role preview --disposition rejected --evidence Edit/decision.json`; первый evidence — JSON с `file` (абсолютный путь), `sha256`, `decision: rejected` и реальным основанием решения. Receipt не должен выдумывать одобрение/отклонение пользователя. Для уже зарегистрированного pending preview после фактического review использовать `reject --run ID --owner OWNER --path Work/ID/previews/file.mp4 --decision Edit/decision.json`. Команда проверяет complete writer, exact file/hash/decision receipt, сохраняет disposition и evidence; сама файл не удаляет. Затем clean по-прежнему защищает imports/pins/current/active scopes. CLI не угадывает редакционное решение.

## Очистка

Для пакетных QA-кадров использовать [managed QA и finalize-qa](qa-finalization.md): автоматическая регистрация, сохранение evidence, адресная очистка после фактического review, журнал и повтор после сбоя. `register-qa --legacy` — первоначальная регистрация точного старого frame map; он не разрешает удаление без review.

```sh
python3 .agents/skills/ytv-media-lifecycle/scripts/workspace.py --episode /absolute/episode clean \
  --run render-v02 --owner actual-owner --root . \
  --policy /absolute/episode/Edit/MediaLifecycle/policy.json
```

Это dry-run. `--execute` выполняет только точный набор зарегистрированных scratch или rejected-preview entries complete run. Команда заново читает live discovery и доступные project metadata через bounded auditor, защищает imports/snapshots/pins/current/active scopes, отказывается при scan error, изменении candidate/rebuild/evidence или hardlinks. Перед каждым unlink проверяет metadata inputs и file identity повторно. Каталоги целиком, sources, generated dependencies и shared store не удаляются. Pending/pinned comparisons сохраняются. Недоступные внешние проекты и динамические потребители перечисляются аудитом; координатор обязан разобрать применимость этих ограничений к своему scope перед execute. Fresh scan не является доказательством отсутствия всех возможных внешних потребителей.

Prepared/complete events записываются append-only в `Edit/MediaLifecycle/locations.jsonl`. При сбое после prepared сверить фактические файлы и журнал, не повторять mutation вслепую. Manifest отмечает фактически удалённые entries, повтор успешной очистки не удаляет новые файлы. Physical reclaimed bytes не обещаются.

## Legacy migration

`adopt --run ID --owner OWNER --path Edit/old/review.mp4 --role preview --root ROOT --policy POLICY` показывает точный перенос; `--execute` выполняет copy → hash/stat/dependency recheck → unlink прежней directory entry. Destination: `Work/ID/previews/legacy/Edit/old/review.mp4`; для scratch аналогично. `--keep-alias` только для сохраняемых preview оставляет относительную symlink по старому пути, чтобы исторические receipts продолжали открываться. Pin переносится в policy на фактический destination; import/current/active protections не обходятся. Новые outputs не писать через aliases. Для scratch alias не создаётся.

Imported files не переносятся этим helper: обновить явные пути зависимых монтажных планов либо сохранить зависимость на стабильном пути. После переноса зарегистрировать фактический destination. Исторические receipts не редактировать, journal хранит old/new/hash/role. После изменения расположения обновить policy/current context и dependency index; старый audit становится историческим.

## Актуальная выдача

```sh
python3 .agents/skills/ytv-media-lifecycle/scripts/workspace.py --episode /absolute/episode promote \
  --source Work/render-v02/previews/final.mp4 --name FILM_EN_v02.mp4 \
  --key full_en_1080p_mp4 --qa Edit/QA/report.json
```

QA JSON должен содержать `file` и `sha256` именно этого source. Проверка identity не является проверкой всех полей QA и не повышает субъективные/редакторские статусы. Staging на томе Deliverables → hash → эксклюзивная публикация файла → атомарный current.json. Existing destination не заменяется. При promotion уже находящегося в Deliverables файла обновляется только pointer после проверки identity. Старые выдачи сохраняются, получают отдельное рассмотрение по root §9; единственный local final автоматически не удаляется. Ключ различает язык/продукт/формат; MP4 и SRT — разные entries, готовность комплекта сверяет QA. Upload не вызывается.

`current.json` и manifest — эксплуатационные указатели, не второй редакционный реестр; принятые решения/IDs/ограничения остаются в CURRENT_CONTEXT и QA receipts. Exit 2 означает отказ; source не считать перемещённым/удалённым без complete event и проверки результата.

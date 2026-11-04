# Read-only audit/plan: CLI и policy v1

Этот CLI описывает обычную рабочую очистку. Отклонённый MP4 и архивирование завершённого выпуска выполняются по [действующему lifecycle](../SKILL.md); [TEXT_ONLY](text-only-archive.md) имеет отдельный exact plan и не добавляет несуществующую CLI-команду.

Этот контракт относится к `media_lifecycle.py`. Создание layout/owned runs, перенос, promotion и адресная очистка реализованы отдельно в [workspace.py](../scripts/workspace.py), см. [workspace contract](workspace.md).

Helper пишет только **новую** папку отчёта. Существующий output, symlink в его пути, `Source/Assets/Storyboard/Research/Packaging` и содержимое `.palmier` как output запрещены. Исходники/проекты не изменяются. Exit 0 означает, что отчёт построен; blockers/coverage errors остаются в нём. Exit 2 — некорректный вход/ошибка создания отчёта. Поддержаны только `audit` и `plan`.

Из корня `.`, с фактическим canonical-путём и новым именем запуска:

```sh
python3 .agents/skills/ytv-media-lifecycle/scripts/media_lifecycle.py audit \
  --root . \
  --episode /absolute/episode \
  --policy /absolute/episode/Edit/MediaLifecycle/policy.json \
  --output-dir /absolute/episode/Edit/MediaLifecycle/audit-run01

python3 .agents/skills/ytv-media-lifecycle/scripts/media_lifecycle.py plan \
  --audit /absolute/episode/Edit/MediaLifecycle/audit-run01/audit.json \
  --output-dir /absolute/episode/Edit/MediaLifecycle/plan-run01
```

Если кандидаты связаны с сохранёнными сторонними монтажными пакетами, аудитор поддерживает `--palmier-project /absolute/package.palmier`; `--live-palmier` запрашивает сведения работающего редактора. Эти параметры защищают существующие зависимости и не входят в FFmpeg-производство. Покрытие сканирования сохранять как ограничение очистки.

## Policy

Относительные пути вычисляются от episode; `..`, абсолютные candidate/pin/current/active пути и symlink-компоненты запрещены. Candidates задаются **точными файлами**, без wildcard. `pins/current/active_work` применяются к точному файлу либо всему подкаталогу с границей пути. У pins/current/active_work можно указать `evidence` (список относительных путей к ownership/QA/решениям); они включаются в проверку свежести inputs. Policy находится в служебном `Edit/MediaLifecycle`, не становится постоянным импортируемым медиа.

```json
{
  "version": 1,
  "current": [{"path": "Deliverables/current_en.mp4", "reason": "current checked EN film; see actual QA receipt"}],
  "pins": [{"path": "Edit/comparison/test.mp4", "reason": "pending comparison; actual decision record"}],
  "active_work": [{"path": "Edit/render-v02", "reason": "active owner from actual ownership record"}],
  "candidates": [{
    "path": "Edit/QA/native_video.h264",
    "role": "scratch",
    "status": "review",
    "reason": "stream extraction for completed hash comparison",
    "evidence": ["Edit/QA/report.json"],
    "rebuild_from": ["Edit/native_export.mp4"]
  }]
}
```

Roles кандидатов: `scratch`, `superseded_export`, `rejected_preview`. Status: `review`, `superseded`, `rejected`; прочие сохраняются с blocker. Наличие declaration не отменяет source/import/pin/current/active protection. `evidence` и `rebuild_from` должны быть существующими файлами; наличие файлов не доказывает правильность рецепта восстановления, выполненную QA или одобрение пользователя. У `superseded_export` отдельно проверить QA замены того же языка/формата; helper не принимает редакционное решение по filename.

## Отчёты и границы

`audit.json` содержит все обычные файлы episode, размеры, stat identity, classifications, найденные project references, text mentions кандидатов, hashes кандидатов, scope/errors и входные fingerprints. `.agents`, `.venv`, `.git`, node_modules, __pycache__, служебные `MediaLifecycle`/`audits` и symlink не обходятся. Package alias, чей canonical path уже независимо найден, отмечается в `covered_package_aliases` без повторного обхода; остальные symlinks остаются непроверенными. Пакеты внутри episode учитываются в объёмах; disk-поиск пакетов и текстовых ссылок по root пропускает их содержимое и читает метаданные отдельно.

Project scope: `media.json`, `project.json` и прямые `snapshots/*.json` всех найденных/указанных пакетов. Все внешние imports защищены, не только используемые видимым timeline. Это консервативная проверка текущей библиотеки и доступных snapshots, не полное восстановление истории, embedded binary форматов или неизвестных потребителей. Все найденные refs на кандидата являются hold. Ошибки чтения/неизвестные структуры показываются явно. Metadata с диска не заменяют live target перед будущей mutation.

Text scope: bounded поиск полного абсолютного/episode-relative пути и разрешаемых JSON-строк в текстовых файлах root до 8 MiB. Это эвристика для review, не граф исполнения; динамические пути и внешние scripts могут отсутствовать. Self-generated audit reports и policy не создают ложной зависимости на каждый перечисленный файл. Исторический output mention не считать доказанным input автоматически.

`plan.json` повторно проверяет device/inode/size/mtime_ns/ctime_ns/nlink и SHA-256 кандидатов без следования symlinks, а также stat сохранённых dependency inputs. Устаревшие входы дают `STALE_AUDIT_INPUTS`, смена кандидата — `STALE_FILE_IDENTITY`. Новый потребитель после audit может отсутствовать в сохранённых inputs: перед будущим удалением всё равно нужен новый dependency scan. Нет writer absence proof, deletion authorization или executable manifest.

Статусы: `PROTECTED` — источник/доказательство/проект/импорт/pin/current/active; `UNKNOWN` — нет достаточной декларации; `BLOCKED` — объявленный кандидат с blocker; `REVIEW_CANDIDATE` — объявленный кандидат без найденного локального blocker, всё ещё требующий решения и свежих проверок. План всегда `executable: false` и `deletion_implemented: false`.

Logical bytes, filesystem-reported allocated bytes и суммы по уникальным device/inode показываются отдельно. `physical_reclaimable_bytes: null`: APFS-клоны и snapshots не дают обещать освобождение по сумме размеров. Ничего не удаляется даже при нулевых blockers.

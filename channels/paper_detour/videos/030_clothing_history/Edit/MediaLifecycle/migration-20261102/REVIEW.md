# 030 — новая структура хранения внедрена

Поручение пользователя: разделить временные файлы, монтажные зависимости и актуальные выдачи; начать с030, существующие медиа разрешено перемещать/удалять. Это заменяет ограничение «только audit/plan, ничего не удалять» предыдущей задачи. Изменения ограничены хранением и flow, новый звук/фильм не создавались, внешних mutations не было.

## Фактический результат

- Созданы `Assets/Generated`, `Work` и [layout](../layout.json). Новые производные для импорта получают постоянный путь в Assets; новые scratch/previews — конкретный owned run в Work.
- Восемь сравнительных/native MP4 v07–v10, **2 044 846 206 bytes (~1,90GiB)**, физически перенесены в [Work/legacy-storage-20261102/previews](../../../Work/legacy-storage-20261102/previews). Они сохранены с pins; старые пути являются относительными compatibility symlinks, bytes/hash совпадают. Это не новые дубли медиа. [Карта](move-map.json), [журнал перемещений/очистки](../locations.jsonl).
- Семь H.264/PCM перенесены в scratch собственного run и после свежей проверки **удалены: 1 107 532 472 bytes = 1,031GiB logical**. [Квитанция](cleanup-receipt.json). Physical reclaim APFS неизвестен.
- Для каждого удалённого потока сохранён точный способ восстановления из остающихся MP4/микса через pipe, bytes/SHA256. Для v08 PCM прежний native MP4 оказался неверным предположением: фактическое совпадение установлено с принятым миксом. Ошибка и подтверждённая замена источника сохранены в [evidence](rebuild-evidence-verified.json).
- [Текущая выдача](../../../Deliverables/current.json) содержит точные MP4/SRT v13 с SHA256 и ссылками на реальные QA/identity receipts. Файлы выдачи не перекодировались и не менялись; current pointer не повышает их редакционные или AV-статусы.
- [Карта зависимостей](../dependencies.json) учитывает **196локальных +43shared =239** проверенных файлов. Все hashes/размеры совпали после миграции; **72локальные зависимости в Edit** оставлены на прежних путях как legacy dependencies, другие находятся в Source. Shared cache также остаётся на стабильных путях.

## Проверки и границы

[Verification](verification.json): live project **B1BA2D18**, timeline **82684371** побайтно совпал с get_timeline до миграции; все239source/dependency hashes, восемь сравнительных MP4/aliases и финальная пара совпали. `.palmier` вручную не редактировался, API mutations не вызывались. Imported файлы не переносились: текущий tools/list не даёт общей операции relink external source, а сохранённые timelines/snapshots должны продолжать работать.

[Audit после миграции](after/audit.md), [машинный audit](after/audit.json), [plan](after-plan/plan.md): ошибок чтения0, отсутствующих declared candidates0. Snapshot **2026-11-02 05:08:28 UTC /06:08:28 Belgrade**: выпуск **4,885GiB logical** без service reports. Из них Source0,774, Work1,904, Deliverables0,237, Edit1,919GiB. Это снимок, не неизменный текущий размер.

Параллельно другой разрешённый QA-проход добавил около **0,822GiB** в Edit/ComplianceAudit_20261102 и менялись другие рабочие материалы; поэтому разницу общего before/after размера нельзя выдавать за эффект нашей очистки. Точный удалённый набор и его1,031GiB подтверждены отдельно. Активные compliance/зерновые тесты и текущий final защищены; их медиа не перемещались/не удалялись. Глобальное покрытие ограничено доступными project packages/metadata; недоступные внешние проекты и динамические потребители остаются ограничением.

## Создание следующих видео

Процедура принадлежит [ytv-media-lifecycle](../../../../../../../.agents/skills/ytv-media-lifecycle/SKILL.md), CLI — [workspace contract](../../../../../../../.agents/skills/ytv-media-lifecycle/references/workspace.md).

- `init_episode.py` сразу создаёт layout и правильные directories. Это проверено в изолированном новом выпуске, реестр и чужие медиа не меняет.
- Captions managed CLI `--episode --run-id`: cue/mask PNG +manifest в Assets/Generated, все примерки в Work/run/previews. Run автоматически отмечается complete/failed после writer; приёмку PNG это не заменяет.
- Motion сохраняет готовые зависимости по прежним shared cache keys, raw/partial направляет в Work/image-motion-run/scratch. Маршрутизация не меняет cache keys или параметры движения. Реальные motion renders этой задачей не запускались.
- QA `--output-dir Edit/QA/run --frames-dir Work/run/previews/qa` разделяет отчёты и объёмные кадры. Выбранные доказательства/контакт-листы сохраняются в Edit, рабочие выборки удерживаются до завершения review. Уже активный QA030 не мигрируется из-под reviewer.
- `promote` проверяет exact source/QA hash и staging, атомарно обновляет current.json, сохраняет предыдущую выдачу до отдельного разбора. `clean` по умолчанию dry-run, с execute удаляет только точные disposable entries complete owned run после нового dependency scan и повторных проверок. Pending/pinned comparisons, источники, imported assets, failed/active runs и shared store автоматически не очищаются.

Проверки реализации: storage34, captions15, initializer4, motion8, QA11 — **72успешных теста**; quick_validate skill PASS; native discovery root/030 PASS, missing/duplicates/errors0. Это тесты и авторская проверка, отдельного независимого code review не было. Общие актуальные правила обновлены у одного владельца и связаны с production/audio/QA/release, исторические receipts сохранены.

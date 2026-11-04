---
name: ytv-media-lifecycle
description: Manage episode media, remove rejected renders promptly, clean owned temporary runs and archive verified completed releases as compact text-only records, preserving shared and active dependencies.
---

# Хранение, очистка и текстовый архив

Вход: [bootstrap](../../../.agent/CHANNEL_BOOTSTRAP.md), реестр, актуальное состояние и scope поручения. Этот skill владеет операционной процедурой хранения; постоянные разрешения — [root §9](../../../AGENTS.md#9-deliverables-и-очистка).

## Рабочая структура

| Содержимое | Путь | Жизненный цикл |
|---|---|---|
| Оригиналы/выбранные исходники | Source/ | Рабочие входы до архивирования завершённого выпуска |
| Импортируемые производные/cue PNG | Assets/Generated/<version>/ | Зависимости действующего монтажа |
| Сохранённый motion store прежних проектов | Shared/Image_Motion/Cache/ | Общий store; episode-owned entries учитываются по consumers |
| Временные попытки | Work/<run>/scratch/ | Очистка завершённых проверенных runs |
| MP4 на просмотр/сравнения | Work/<run>/previews/ | Текущий pending сохраняется; отклонённый render удаляется сразу |
| Конфиги/receipts/provenance | Edit/ | Компактные текстовые записи сохраняются |
| Принятый комплект | Deliverables/ + current.json | Один актуальный комплект до TEXT_ONLY |

Новый выпуск создаёт [init_episode.py](../../../channels/paper_detour/automation/init_episode.py); для существующего `workspace init` создаёт отсутствующий layout. Уже импортированные пути сохраняются в рабочем режиме. Разные языки/форматы имеют отдельные current entries.

## Обычная очистка

До генерации создать owned run и назначить роли выходам. После фактического завершения writer сохранить статусы и точные inputs/hash/evidence. Перед тяжёлым render, при handoff, после upload очищать ненужные выходы завершённых попыток, сохраняя рабочие зависимости и актуальный комплект.

- [Read-only auditor](references/cli-contract.md) строит свежий audit/plan; неизвестный consumer остаётся UNKNOWN.
- [Workspace CLI](references/workspace.md) управляет layout/run/roles/current. `clean --execute` удаляет exact registered scratch/rejected-preview entries complete run; обычный clean сохраняет imports/current/pins и shared assets.
- Назначенный кадровый QA использует [finalize-qa](references/qa-finalization.md); обычная MP4-приёмка сохраняет компактные технические замеры и текстовое решение пользователя.

Перед unlink перечитать identity и проверить writers/imports/pins/consumer scope. Failed/abandoned сначала получить фактический disposition. Неизвестный исход mutation сверить по файлам/журналу. Протокол и retained evidence сохраняются в текстовом виде. Один и тот же run не создаёт новые сравнения при повторе команды.

## Отклонённый MP4

При замечаниях пользователя сразу зафиксировать точный file/hash и `CHANGES_REQUESTED/REJECTED`, завершить writer и удалить отклонённый render. Принятую замену ждать не требуется. Рабочие картинки, озвучка, монтаж и необходимые производные сохраняются для исправлений.

Для managed preview выполнить `reject` с реальным decision receipt, затем `clean --execute` по workspace contract. Если отклонённый файл указан как current/pinned, актуализировать только его указатель/hold по сохранённому решению. Для legacy render составить exact path/hash/stat plan и удалить этот файл стандартной файловой операцией после свежей проверки зависимостей. Чужой активный consumer сохраняет свой hold. Сохранить текстовую квитанцию фактического удаления и размер; новая версия получает отдельный путь/hash и приёмку.

## Завершённый выпуск — TEXT_ONLY

После проверенного Public и статуса согласованного A/B для длинного фильма либо после проверки расписания и обработки выполнить [архивирование](references/text-only-archive.md). При расписании сохранить или передать все согласованные названия и обложки для будущего теста до очистки; документировать их доступность. Shorts — без A/B. Безвозвратное удаление требует всех обязательных подтверждений среды; проверяемо восстанавливаемое перемещение рассматривается отдельно. При отдельном поручении оптимизации тот же режим применяется к завершённым Public/Unlisted, включая доступ, изменённый пользователем вне текущего чата. Свежие remote identity/processing/access и подтверждение завершённой принятой версии обязательны.

Результат: в episode остаются компактные тексты; его тяжёлые исходники, звук, renders, собственные кэши и завершённые пакеты очищены в разрешённом объёме. Согласованные обложки для будущего A/B при расписании сохраняются либо передаются пользователю с подтверждённой доступностью. Shared assets и действующие consumers других работ сохраняются. Рабочая защита собственных зависимостей снимается только для записанного retirement scope; точная процедура и ограничения существующих helpers — в архивном контракте.

## Проверка результата

Обновить CURRENT_CONTEXT, current/location/dependency records: реальные оставшиеся пути, remote video/channel IDs/URL, состояние review/release, удалённые entries и статус хранения. Измерить остаточный logical/allocated size; physical APFS reclaim отмечать по фактическому измерению либо unknown. Частичную очистку записать как PARTIAL с конкретными holds. TEXT_ONLY присваивается после проверки результата. Возможности восстановления media описываются честно: генеративный PNG не воспроизводится побайтово по одному prompt.

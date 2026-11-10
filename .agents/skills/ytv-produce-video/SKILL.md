---
name: ytv-produce-video
description: "Produce an approved ytvideos script through storyboard, independent scene images, audio, subtitles and render. Use only the assigned task context and preserve exact accepted inputs."
---

# Произвести принятый текст

CLI и точные outputs/receipts: [task contract](../../../docs/operations/task-contract.md).

Выполнять только выданный task: `storyboard`, `scene_image`, `audio`, `subtitles` или `render`. Проверить actual script approval, inputs и lease. Читать стандарт, нужный этому task, а не весь производственный архив.

| Task | Нужные требования | Выход |
|---|---|---|
| storyboard | [visual](../../../docs/standards/visual.md) + художественный профиль | Сценовые IDs/revisions, смысл, композиция, references, камера и независимые задания |
| scene_image | [visual](../../../docs/standards/visual.md) + exact scene packet | Реальный файл/hash, provider handle, actual controls и review сцены |
| audio | [audio](../../../docs/standards/audio.md) | Точный полный mix, речь, скорость, права, timing/provenance и проверки |
| subtitles | [audio](../../../docs/standards/audio.md) + канальная типографика | Проверенная word map, смысловые группы, SRT и subtitle contract |
| render | [delivery](../../../docs/standards/delivery.md) | MP4/hash, frozen inputs, commands и технический receipt |

1. Проверить доступные tools и нужные assets. Использовать профиль, не менять голос/шрифт/стиль ради доступного default. Недостающий provider блокирует только свои задачи.
2. Claim задачу, выполнить её штатным adapter/tool и сохранить фактический outcome. Не помечать результат PASS без нужного просмотра/прослушивания или измерения.
3. Независимые сценовые задания отдавать пулу свежих сессий. Принимать готовые результаты по одному, освобождать slot и отправлять следующую сцену. Число сессий определяет [адаптивная очередь](../../../docs/architecture/adaptive-workers.md), а не число сцен или каналов.
4. В каждой новой сценовой сессии передать самодостаточный packet: точная сцена, стиль, references и output schema. Повторное использование slot не означает наследование контекста предыдущей картинки. Не превышать фактические caps/бюджет.
5. UNKNOWN после отправки сохранить и reconcile; не повторять запрос из другого чата. Stale result не применять к новой revision.
6. Завершить task через контракт, взять `next` и продолжать до готового MP4. Упаковку можно готовить параллельно. Готовый MP4 передать review, без дополнительного согласования промежуточных картинок/музыки/монтажа.

Для локального исправления сохранить остальные принятые artifacts/cache. Изменение смысла текста вернуть к script gate; технический ремонт выполнять автономно. Генераторы и existing helpers не получают право обходить guards, обязательные для новой run.

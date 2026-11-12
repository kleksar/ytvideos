---
name: ytv-produce-video
description: "Produce an approved ytvideos script through AI-generated images and thumbnails, audio, subtitles and render; preserve exact inputs and the Shorts loop while packaging runs in parallel."
---

# Произвести принятый текст

CLI и точные outputs/receipts: [task contract](../../../docs/operations/task-contract.md).

Выполнять только выданный task: `storyboard`, `scene_image`, `audio`, `subtitles` или `render`. Проверить actual script approval, inputs и lease. Прочитать выбранные `reference_documents`: общий стандарт, профиль и относящийся к формату канальный рецепт. Они передаются с содержимым и hash; каталог ссылок не заменяет требования.

| Task | Нужные требования | Выход |
|---|---|---|
| storyboard | [visual](../../../docs/standards/visual.md) + художественный профиль | Сценовые IDs/revisions, смысл, композиция, references, камера и независимые задания |
| scene_image | [visual](../../../docs/standards/visual.md) + exact packet; при `purpose: thumbnail` также [thumbnails](../../../docs/standards/thumbnails.md) | Реальный image или licensed clip, hashes, provider evidence и review |
| audio | [audio](../../../docs/standards/audio.md) | Точный полный mix, речь, скорость, права, timing/provenance и проверки |
| subtitles | [audio](../../../docs/standards/audio.md) + канальная типографика | Проверенная word map, смысловые группы, SRT и subtitle contract |
| render | [delivery](../../../docs/standards/delivery.md) | MP4/hash, frozen inputs, commands и технический receipt |

Для Short в storyboard/audio/render прочитать [editorial](../../../docs/standards/editorial.md) и точный loop plan принятого текста. Связать последний и первый планы, речь, музыку и субтитры; проверить начало на фактической озвучке. Не добавлять заставку/прощание, скрывать отдачу или менять текст ради стыка. Ошибка смысловой петли возвращает текст на script gate; техническая склейка исправляется без нового обычного gate. Финальная проверка — [delivery](../../../docs/standards/delivery.md).

1. Проверить доступные tools и нужные assets. Все создаваемые изображения/обложки делать через AI по [visual](../../../docs/standards/visual.md); дефекты исправлять prompt/AI-edit/регенерацией. Использовать профиль, не менять голос/шрифт/стиль ради доступного default. Для licensed clips зарегистрировать source/rights через `attach-artifact` и связать pinned `source_clip` по task contract. Недостающий provider блокирует только свои задачи.
2. Claim задачу, выполнить её штатным adapter/tool и сохранить фактический outcome. TTS генерирует raw 1,0×; конечную канальную скорость применить один раз по audio standard. Не помечать результат PASS без нужного просмотра/прослушивания или измерения.
3. Независимые изображения и `thumbnail:*` отдавать общему пулу свежих сессий с наблюдёнными `runtime_key/max_sessions`. Packaging выполняется параллельно по `ytv-release-video`; после его завершения создавать thumbnail tasks. Они не блокируют render или передачу MP4 на review. Для обложки читать [thumbnail standard](../../../docs/standards/thumbnails.md) и переданный brief; не переносить правила рекламной карточки на обычные сцены. Licensed clips готовить доступным host tool; `execute-media` не реализует extraction. Принимать результаты по одному и сразу занимать освободившийся slot; число workers определяет [адаптивная очередь](../../../docs/architecture/adaptive-workers.md).
4. В каждой новой сценовой сессии передать самодостаточный packet: точная сцена, стиль, `reference_documents` и output schema. Повторное использование slot не означает наследование контекста предыдущей картинки. Не превышать фактические caps/бюджет.
5. UNKNOWN после отправки сохранить и reconcile; не повторять запрос из другого чата. Operation observation привязать к exact `attempt_id/task_input_hash`. Stale result не применять к новой revision.
6. Завершить task через контракт: core проверяет реальные media bytes; authored receipt не заменяет decode. Взять `next` и продолжать до MP4, затем передать review exact hash и actual probe. Упаковку готовить параллельно; дополнительное согласование промежуточных картинок/музыки/монтажа не требуется.

Для локального исправления сохранить остальные принятые artifacts/cache. Изменение смысла текста вернуть к script gate; технический ремонт выполнять автономно. Генераторы и existing helpers не получают право обходить guards, обязательные для новой run.

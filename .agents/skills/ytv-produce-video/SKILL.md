---
name: ytv-produce-video
description: "Produce an approved ytvideos script through AI-generated images and thumbnails, audio, subtitles and render; preserve exact inputs and the Shorts loop while packaging runs in parallel."
---

# Произвести принятый сценарий или монтажный план

До действий выполнить [обязательную процедуру](../ytv-start/references/task-execution.md): прочитать pinned skill/требования/точные входы и проверить описанный способ. Пробел или неразрешённый конфликт — blocker затронутого этапа; не подставлять свои defaults и не менять правила ради продолжения.

CLI и точные outputs/receipts: [task contract](../../../docs/operations/task-contract.md).

Для `storyboard`, `scene_image` с `purpose: scene`, `render` и `review` прочитать [общую процедуру видеоклипов](references/video-clips.md); применять её при работе с клипами, начиная до затрат. Для `audio`, `subtitles` и обложок она не нужна.

Генерация клипов применяется к Shorts. Если в контексте есть [рецепт Flow](../../../channels/paper_detour/docs/FLOW_PRODUCTION.md#выбор-движения), выбрать планы Ingredients по записи и карте слов. Для каждой точной партии до отправки получить [отдельное одобрение внешнего видео](../../../docs/workflow.md#отдельное-одобрение-внешнего-видео) по параметрам из рецепта.

Выполнять только выданный task: `storyboard`, `scene_image`, `audio`, `subtitles` или `render`. Роль, обязательное чтение и точные входы определяет [форма задания](../ytv-start/references/task-execution.md#до-действия); для run координатор проверяет actual script approval и текущий lease.

| Task | Нужные требования | Выход |
|---|---|---|
| storyboard | [visual](../../../docs/standards/visual.md) + художественный профиль | Сценовые IDs, постановка, камера, [листы и привязка видов](../../../docs/standards/visual.md#листы-персонажей-предметов-и-локаций) |
| scene_image | [visual](../../../docs/standards/visual.md) + exact packet; при `purpose: thumbnail` также [thumbnails](../../../docs/standards/thumbnails.md) и его [QA](../../../docs/standards/thumbnails.md#qa-файла-и-пары) до показа готовой обложки | Реальный image или licensed clip, hashes, provider evidence и review |
| audio | [audio](../../../docs/standards/audio.md) | Точный полный mix, речь, скорость, права, timing/provenance и проверки |
| subtitles | [audio](../../../docs/standards/audio.md) + канальная типографика | Применимые word map/группы/SRT или проверенное решение `no_speech` |
| render | [delivery](../../../docs/standards/delivery.md) | MP4/hash, frozen inputs, commands и технический receipt |

Для storyboard/scene_image/audio/render прочитать применимый раздел [производственных примеров](references/production-examples.md): выбор камеры для закреплённого static whole-frame recipe, звуковой акцент или адресная AI-правка. Примеры не меняют профиль, входы и разрешённый способ исполнения. Для Ingredients выполнить [проверку единого стиля выпуска](../../../channels/paper_detour/docs/FLOW_PRODUCTION.md#единый-стиль-выпуска) перед согласованием партии и сверить стиль клипов на склейках при монтаже.

Для `subtitles` и `render`, включая ручную правку, выполнить [стандарт экранных субтитров](../../../docs/standards/audio.md#экранные-субтитры): сохранить карту слов, измеренные группы и SRT; применить карту и проверить точный MP4.

При нарезке исходной речи, включая ручную правку, до рендера сохранить дословную монтажную расшифровку с исходными таймкодами по [редакционному стандарту](../../../docs/standards/editorial.md#монтаж-исходной-речи).

Для `licensed_clips` и `music_first` прочитать принятый typed edit-script и его speech mode по [task contract](../../../docs/operations/task-contract.md#outputs). `source`/`none` используют source audio mix; `none` завершает subtitles проверенным `no_speech` JSON. Не придумывать narration/SRT и не отправлять TTS для этих режимов; точные checks и output kind уже находятся в task context. Для `music_first` следовать `task_guide.music_edit` и [музыкальному рендеру](../../../docs/operations/task-contract.md#музыкальный-рендер): `mix` сохраняет непрерывный принятый отрывок, `music_render` связывает planner, footage/rights и применимые вокальные титры.

Для Short в storyboard/audio/render прочитать [editorial](../../../docs/standards/editorial.md) и применимый loop plan принятого сценария. Связать последний и первый планы, музыку, применимую речь и субтитры; проверить начало по фактическому звуку. Не добавлять заставку/прощание, скрывать отдачу или менять принятый текст ради стыка. Ошибка смысловой петли возвращает текст на script gate; техническая склейка исправляется без нового обычного gate. Финальная проверка — [delivery](../../../docs/standards/delivery.md).

1. Проверить доступные tools и нужные assets. Все создаваемые изображения/обложки делать через AI по [visual](../../../docs/standards/visual.md); дефекты исправлять prompt/AI-edit/регенерацией. Использовать профиль, не менять голос/шрифт/стиль ради доступного default. Для source clips зарегистрировать source/rights через `attach-artifact` и связать pinned `source_clip` по task contract. Недостающий provider блокирует только свои задачи.
2. Claim задачу, выполнить её штатным adapter/tool и сохранить фактический outcome. Когда рецепт требует narration, TTS генерирует raw 1,0× до слухового review. До complete прослушать точный полный микс по task contract; конечную канальную скорость применить один раз по audio standard. Не помечать результат PASS без нужного просмотра/прослушивания или измерения.
3. Независимые изображения и `thumbnail:*` отдавать общему пулу свежих сессий с наблюдёнными `runtime_key/max_sessions`. Packaging выполняется параллельно по `ytv-release-video`; после его завершения создавать thumbnail tasks. Они не блокируют render или передачу MP4 на review. Для обложки читать [thumbnail standard](../../../docs/standards/thumbnails.md) и переданный brief; не переносить правила рекламной карточки на обычные сцены. Licensed clips готовить host tool только по описанному для рецепта способу; `execute-media` не реализует extraction. Если способ extraction не определён, вернуть blocker, не составлять новый pipeline. Принимать результаты по одному и сразу занимать освободившийся slot; число workers определяет [адаптивная очередь](../../../docs/architecture/adaptive-workers.md).
4. Составить по visual standard ведомость сущностей, включая детали реквизита и фон. Проверить листы деталей, виды сборок и позы. Если сборка меняется между кадрами, приложить проекции одной геометрии к локальной AI-правке и проверить соединения на увеличении. Сохранить промпт сцены, назначенные панели и результат проверки рук, креплений, перекрытий и канального стиля. Не превышать фактические caps/бюджет.
5. UNKNOWN после отправки сохранить и reconcile; не повторять запрос из другого чата. Operation observation привязать к exact `attempt_id/task_input_hash`. Stale result не применять к новой revision.
6. Завершить task через контракт: core проверяет реальные media bytes; authored receipt не заменяет decode. Для render сохранить обязательный [delivery evidence](../../../docs/operations/task-contract.md#render-manifest-и-delivery-evidence), связывающий принятые входы, manifest, фактическую команду текущего claim и exact MP4. Взять `next` и продолжать до MP4, затем передать review exact hash и actual probe. Упаковку готовить параллельно; дополнительное согласование промежуточных картинок/музыки/монтажа не требуется.

Для локального исправления сохранить остальные принятые artifacts/cache. Изменение смысла текста вернуть к script gate; технический ремонт выполнять автономно только предусмотренным способом. Генераторы и existing helpers не получают право обходить guards, обязательные для новой run.

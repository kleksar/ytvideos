# CLI и контракт task result

Все команды возвращают JSON. Синтаксис текущей версии — `uv run python -m ytvideos --help`. Один workspace/store используют все связанные сессии. Ниже placeholders заменяются фактическими значениями из ответа CLI, не выдумываются.

Порядок чтения, выполнения и сообщения blocker принадлежит [общей процедуре skill](../../.agents/skills/ytv-start/references/task-execution.md); этот документ задаёт синтаксис, схемы и семантику runtime. Наличие CLI/tool не разрешает производственный способ, отсутствующий в инструкциях.

Разделы: [запуск](#новый-сценарный-run), [план](#план-выпуска), [контекст](#требования-в-контексте), [блокировка](#блокировка-и-разблокировка), [outputs](#outputs), [источники и обложки](#источники-и-обложки), [render evidence](#render-manifest-и-delivery-evidence), [media checks](#проверки-media-и-review), [receipt](#receipt), [approval/recovery](#approval-и-продолжение), [adapters и release](#media-изображения-release).

## Новый сценарный run

Для любого нового сюжета, сценария или ролика вызвать `start` до веб-исследования и написания текста. Это также вход для запроса только на полный сценарий:

```bash
uv run ytv start --channel CHANNEL_ID --format short --intent 'точный запрос пользователя'
```

Подставить явный канал или default `paper_detour`; для long изменить формат. `start` создаёт один обычный run тем же runtime, возвращает `plan_summary`, `doctor`, `next` и `read_next`. Каждый элемент `read_next` содержит `task_id`, `input_hash`, `task_file`/его SHA-256, `skill_file`, `requirement_files`, `task_guide` и инструкцию чтения. Открыть именно эти сохранённые файлы, сообщить краткий план и продолжить по `next_action`. Пакет материализован из pinned context без claim; команда не вызывает providers и не создаёт approval. Полученный run ID использовать во всех следующих действиях; для существующего run выполнять `status` → `resume`/`next` → `plan`, без повторного `start`.

`run_version` в ответе идентифицирует единый snapshot, из которого получены план, task contexts и сохранённые capability observations. Файлы reading packet записываются после чтения состояния. При повторе того же packet, в том числе конкурентном, runtime принимает уже существующий каталог только при точном совпадении bytes; изменённый пакет не перезаписывается. Если другой worker успел изменить run, последующий claim заново проверяет актуальные входы.

Конфигурацию каналов можно проверить отдельно без создания run, store или workspace:

```bash
uv run ytv profiles
uv run ytv profiles --channel paper_detour --format short
```

Ответ показывает status, требования/варианты формата и blockers. `live_readiness=unverified` означает, что команда не проверяет подключение providers, аккаунтов или наличие media.

```bash
uv run python -m ytvideos status --run RUN_ID
uv run python -m ytvideos plan --run RUN_ID
uv run python -m ytvideos doctor --run RUN_ID
```

Для полного присланного narration сохранить исходный UTF-8 файл и передать его при создании run. Для `licensed_clips` и `music_first` допустим exact JSON edit-script из раздела [outputs](#outputs):

```bash
uv run ytv start --channel paper_detour --format short --intent 'Сделай видео по присланному сценарию' --source-script /absolute/path/to/script.en.txt
```

`--source-script` сохраняет точные bytes в artifact store и hash в `pins.source_script`; `plan` и task `context` возвращают descriptor `source_script`. Исходный файл после этого не является рабочей зависимостью. При повторной доставке с тем же `request_id` нельзя убрать или заменить этот source. Для темы, синопсиса или черновика использовать обычный `--intent`: они требуют разработки полного текста по [workflow](../workflow.md#готовый-текст-и-набросок).

Research проверяет факты именно присланной истории; script проходит обязательные проверки и регистрирует exact narration без повторного выбора темы. Сохранение source не создаёт approval. Локальный координатор связывает реальное исходное поручение с зарегистрированным script/hash через `approve` ниже; содержательно изменённый текст требует принятия новой версии.

До claim сохранить реально наблюдённые capabilities. Например `{"web.search":true,"model.text":true}` допустимо только когда эти tools доступны текущему worker. Запись `capabilities --run RUN_ID --file capabilities.json --evidence 'actual observation reference'` сама не предоставляет tool. Для metered audio/image требуется положительная reservation, либо подтверждённый `billing:included`; max paid budget по умолчанию не разрешает платные запросы.

Фактическое превышение бюджета фиксируется без занижения стоимости и запрещает новые платные reservations. Независимые задачи с известной нулевой стоимостью остаются доступны; metered operation без положительной reservation по-прежнему запрещена.

Новый run не наследует каталог tools сессии автоматически. `capability_checks` в `next` и provider checks в `doctor` различают `unobserved` / `available: null`, подтверждённые `available: true` и `unavailable: false`. При `unobserved` выполнить `next_action: inspect_runtime_tools`: проверить фактически доступные tools, включая deferred discovery текущего host, прочитать task context, записать наблюдение и повторить `next`. Это не blocker среды. При подтверждённой недоступности исправлять её по evidence и продолжать независимые задачи. Ссылка на реально полученный search result или наблюдение доступного text runtime — evidence, которое worker вправе сохранить без отдельного user approval. Не копировать пример evidence как факт и не заявлять доступ к чужому аккаунту по наличию имени connector.

```bash
uv run python -m ytvideos next --run RUN_ID
uv run python -m ytvideos context --run RUN_ID --task research --output context.json
uv run python -m ytvideos claim --run RUN_ID --task research --worker WORKER_ID
```

`context` разрешён до claim, в том числе при `dispatchable: false`; его чтение не тратит attempt или reservation. CLI `claim` атомарно возвращает `token`, `worker`, `input_hash`, `expires_at`, `estimated_units`, `claimed_at` и `context` текущей задачи. Сохранить JSON-ответ и брать точные token/input_hash из него программно, не перепечатывать идентификаторы вручную; использовать stable реальную идентичность исполнителя. Прочитать возвращённый пакет до исполнения. При `stale or missing task lease` сначала сверить task/status и точное значение с текущим claim: опечатка не означает истёкшую lease. Долгую задачу продлевать `heartbeat --run RUN_ID --task TASK_ID --token TOKEN`; lease не даёт право изменить scope.

### Доступ к независимому reviewer

Task `script` требует capability `sessions.independent`; порядок её обнаружения также выдаётся в `task_guide.independent_review` и `capability_checks.discovery`. Проверить **прямые инструменты текущего host и deferred registry**. Доступный `collaboration.spawn_agent` или `spawn_agent` позволяет создать свежую независимую сессию: он не обязан называться `reviewer` или присутствовать в `ALL_TOOLS`. Отсутствие такого имени в одном registry не подтверждает недоступность review.

Создать reviewer с новым контекстом, передать точный artifact без авторского вердикта и сохранить фактически полученный результат/session evidence с script hash. Не выдумывать reviewer ID и не заменять отдельную проверку авторской сменой роли. Если все session slots временно заняты, дождаться завершения активной работы либо освободить принадлежащий этой задаче завершённый slot поддерживаемым способом и повторить попытку; это ограничение расписания, а не отсутствие capability. `unavailable` записывать только по фактической ошибке поддерживаемого host или проверенной полной инвентаризации доступных инструментов. До этого продолжать обнаружение и доступную работу в пределах бюджета.

## План выпуска

`start` — агентский вход с компактным `plan_summary`, диагностикой и materialized reading packet. Низкоуровневый `create` сохраняется для программной совместимости и возвращает `run_id`, `pins`, `next`, `plan`, без автоматической подготовки reading packet. Оба используют один граф и один контракт. Для сохранённого выпуска `plan --run RUN_ID` строит read-only представление из состояния run; не вызывает providers, не запускает генерацию и не сохраняет ещё один plan artifact.

| Поле | Назначение |
|---|---|
| `channel`, `format`, `intent`, `revision`, `pins` | Точный продукт и закреплённые версии |
| `source_script` | Descriptor точного присланного narration, если он передан при `create` |
| `production_requirements` | Канальные требования к выбранному формату/рецепту из pinned profile |
| `accepted`, `steps`, `release_steps` | Принятые gates, статусы этапов, цели, skill, зависимости, выходы и checks |
| `next` | Готовые задачи, `context_command`, `capability_checks`, конкретный `next_action`, gates и blockers |
| `capability_gaps` | Отсутствующие положительные наблюдения и затронутые задачи |
| `runtime.code_matches_pin`, `commands` | Совместимость checkout и следующие команды в том же workspace/store |

План сообщает сохранённые наблюдения, а `doctor` проверяет фактическое окружение. `audio.listen` для audio/review означает доступный способ реального прослушивания с evidence; FFmpeg-анализ не предоставляет слух. До генерации кратко изложить план человеку по [workflow](../workflow.md#первый-ответ), затем продолжить разрешённую работу без нового approval.

## Инструкции для узкой задачи

```bash
uv run ytv instructions --channel CHANNEL_ID --stage packaging --format long
```

Без `run`, БД, providers и нового согласования. Для разработки/пересмотра обложки — `packaging`; для исполнения выбранного brief — `thumbnail`; для read-only анализа опубликованного Short — `retention --format short`; остальные значения stage совпадают с task context. Команда требует настоящий `channels/<id>/PROFILE.md`, возвращает полный skill и `reference_documents` с SHA-256, `read_next`, channel/status, фактический `channel_configuration` (JSON-профиль либо `null` для ручного канала) и scope `instructions_only`. Для production stages применяется тот же selector/`context_references`, что для нового run. `retention` выбирает `ytv-operate`, общую процедуру, editorial, retention reference, профиль и подходящие context references без ограничения по stage; это не production stage и не новый маршрут snapshot. Ручной канал не получает выдуманный ChannelSpec или автоматическое разрешение выпуска. Missing/blank/unreadable обязательный документ/skill, неизвестный канал или неоднозначный skill дают ошибку, не частичный успешный packet.

`instructions_only` доказывает наличие выбранных текстов, не чтение/понимание моделью, не полноту реальных media и не QA. Все выданные файлы прочитать целиком, затем выполнить [сверку входов](../../.agents/skills/ytv-start/references/task-execution.md#проверить-полноту-до-исполнения). Для уже существующего run использовать только его pinned `context`; новый helper не мигрирует правила.

## Требования в контексте

`context.references` — выбранные repo-relative пути; `reference_documents` — соответствующие `{path,sha256,text}`. `task_guide` даёт цель, skill, зависимости/gates, output kind, обязательные checks и следующие задачи. Его `execution_reference` указывает на закреплённую общую процедуру среди `reference_documents`; её шаги и правила blocker не копируются в каждую task card. `production_requirements` содержит закреплённый машинный контракт канала. Применение пакета — [preflight skill](../../.agents/skills/ytv-start/references/task-execution.md#до-действия).

`inputs` содержит прямые outputs зависимостей, `supporting_inputs` — descriptors принятых транзитивных outputs: например script/audio/storyboard для review, script для subtitles и research для packaging. `artifact_root` указывает хранилище actual артефактов; descriptor не содержит сам текст или медиа. Прикреплённые отдельно supporting notes не становятся входами автоматически.

`source_script` передаёт сохранённый исходный narration, если run создан с ним. Отличать его от проверенного `script` output и состояния approval; это три разных сущности.

Общие стандарты выбирает `src/ytvideos/context.py`, канальные документы — `ChannelSpec.context_references`. Общий `task-execution.md` входит в каждый маршрут нового snapshot, включая scene/thumbnail worker, с теми же text/hash проверками; runtime не может доказать само чтение текста или полноту его смысла. Фильтры `stages`, `formats`, `purposes` объединяются через AND; отсутствие фильтра означает все значения. `purposes` применим к `scene_image` (`scene` или `thumbnail`), на остальных этапах purpose отсутствует.

Пример записи в ChannelSpec:

```json
{
  "path": "channels/scenes_on_repeat/docs/EDIT_NOTES.md",
  "stages": ["storyboard", "audio", "subtitles", "render", "review"],
  "formats": ["short"]
}
```

Путь относительно корня репозитория, без `..`, абсолютного пути и выхода через symlink. Явно объявленный документ обязателен: отсутствующий файл останавливает создание нового run с конкретной ошибкой. `PROFILE.md` добавляется при наличии; активные профили объявляют его явно, чтобы отсутствие не прошло незамеченным. Один документ можно указать с разными фильтрами; в packet он попадает один раз. Изображения-эталоны передаются как actual assets отдельно: Markdown с описанием не заменяет файл.

При `create` один `reference_snapshot` сохраняет маршруты и тексты документов; его digest входит в `pins.references`. Task получает только нужную часть snapshot с `reference_source=pinned`. Изменение или удаление recipe в checkout не меняет закреплённые требования нового snapshot-run. Смена правил существующего выпуска требует [migration](../migration.md).

Старый run без snapshot использует проверенный исходный code pin и `reference_source=legacy_checkout`; это не утверждение о сохранённом историческом тексте. Не переписывать его pin ради запуска в новой версии.

`start.read_next` и native image worker получают материализованный packet с `materialization_version: 2`. В его `TASK.json` skill представлен descriptor с исходным `path`, `sha256` и `local_path: requirements/<repo path>`; сам текст хранится только по этому локальному пути. `reference_manifest` также содержит `path`, `sha256`, `local_path`, без повторных `reference_documents`. `start.read_next` возвращает `task_file`, `skill_file` и все `requirement_files`; native packet дополнительно содержит список `requirements`. Canonical `context`/успешный `claim` сохраняют полные pinned тексты и hashes. Прежний native packet с корневым `SKILL.md` остаётся читаемым; существующие entry packets не перезаписываются новой формой.

Image pool передаёт тот же manifest. Native host проверяет пути, полноту и hashes до создания файлов; sandbox не расширяется. Обычная сцена не получает thumbnail-only playbook, а обложка получает стандарт обложек. Для Shorts storyboard/audio/render также получают editorial loop standard.


## Блокировка и разблокировка

Точный отчёт о пробеле инструкции и условия продолжения задаёт [skill](../../.agents/skills/ytv-start/references/task-execution.md#блокер-и-продолжение). `fail` доступен координатору с действующим claim; он сохраняет reason в task и событии:

```bash
uv run ytv fail --run RUN_ID --task TASK_ID --token CURRENT_CLAIM_TOKEN --reason 'Фактический blocker с путями правил и evidence'
```

Без recorded external dispatch task становится `blocked`, claim снимается, reservation освобождается. При возможном внешнем dispatch task становится `unknown`; существующая операция требует reconciliation. Необязательный `--known-not-sent` допустим только при подтверждённом отсутствии отправки и отвергается при противоречащей записи dispatch. Он не служит обходом UNKNOWN.

До claim нет token для `fail`: сообщение blocker не означает, что task уже записан как `blocked`. Изолированный worker возвращает blocker host в своей разрешённой форме результата; право пользоваться workflow CLI из этого контракта не возникает.

```bash
uv run ytv unblock --run RUN_ID --task TASK_ID --reason 'Проверенное устранение причины и ссылка на resolution evidence'
uv run ytv next --run RUN_ID
```

`unblock` принимает только `blocked` task и непустое resolution evidence; возвращает его в `pending`, сохраняя событие. Команда не проверяет смысл исправления, не подтверждает QA и не заменяет [migration](../migration.md) при смене pinned правил. UNKNOWN разблокируется предусмотренной reconciliation, а не `unblock`. `resume` восстанавливает leases и не устраняет отсутствующую инструкцию.

## Outputs

`research` output — JSON:

```json
{
  "selected_topic": {
    "title": "Конкретная выбранная история",
    "angle": "Подтверждённый угол",
    "viewer_value": "Что зритель сможет понять благодаря событиям"
  },
  "sources": [
    {"url": "https://actual-primary-source.example/page", "claim": "Подтверждаемое утверждение", "location": "Проверенное место"}
  ]
}
```

Пример показывает форму, не источник: заменить URL/claim/location фактически прочитанными материалами. Дополнительно сохранить uncertainty, overlap/отвергнутые варианты, аудиторию и заметку о визуальном обещании и его раскрытии в сценарии. Для `illustrated` `script` output — UTF-8 файл полного narration без процедурных инструкций. Минимальная длина машинной проверки не является критерием качества: должен быть закончен сценарий, который пользователь просил.

Для `licensed_clips` можно сохранить plain narration либо strict edit-script JSON; `music_first` использует только этот JSON. Он описывает законченный монтаж без выдуманного дикторского текста:

```json
{
  "schema": "ytv-edit-script-v1",
  "production_variant": "scene",
  "intent": "Полный редакционный замысел и наблюдаемый исход",
  "speech": {"mode": "none", "text": ""},
  "segments": [{"id": "S001", "description": "Полное действие выбранного фрагмента и его функция", "spoken_text": ""}]
}
```

Вариант должен быть зарегистрирован в профиле; segments имеют уникальные IDs и монтажный порядок. `speech.mode` — `narration` для авторской речи, `source` для реально звучащих source-реплик либо `none` при их отсутствии. Объединение `segments[].spoken_text` сохраняет все слова `speech.text` по порядку; при `none` обе формы текста пусты. Approval связывает exact JSON целиком; TTS при `narration` читает только `speech.text`. Storyboard, audio, render и packaging сохраняют выбранный вариант и speech mode, не выводят их заново из caller flag. Отсутствие речи не отменяет реальный soundtrack, права и прослушивание.

Для `music_first` выбрать `production_variant: vocal` и `speech.mode: source` с точными словами песни либо `production_variant: instrumental` и `speech.mode: none` с пустым текстом. Поля JSON — ровно `schema`, `production_variant`, `intent`, `speech`, `segments`. Plain narration и `speech.mode: narration` отвергаются. Входной план сохраняет принятые слова и ordered segments; музыкальный маршрут и final AV review описаны в [музыкальном рендере](#музыкальный-рендер). Проверка дикторской `narrative_loop` к этому рецепту неприменима.

После принятия `none` task `subtitles` имеет `output_kind: no_speech`, отложенную perceptual capability `audio.listen` по [production before listening](#audio-production-before-listening) и результат **ровно** `{"schema":"ytv-no-speech-v1","script_sha256":"EXACT_EDIT_SCRIPT_SHA256","audio_sha256":"EXACT_ACCEPTED_MIX_SHA256","has_speech":false}`. SRT и слова не придумываются. Обязательный check `no_speech` у audio/subtitles связывает `artifact_sha256` принятого audio, реального reviewer, notes, coverage всего микса и evidence `{path,sha256}` по форме review ниже. В final review этот check относится к exact MP4. Для `source` остаются настоящие alignment/SRT и `exact_text`.

`storyboard` output — JSON `{"scenes":[{"id":"S001","prompt":"Самодостаточное задание","visual_intent":"Смысл кадра"}]}` с необходимыми реальными timing/references/continuity. Если `production_requirements.available_variants` непуст, добавить верхнеуровневый `production_variant` из этого списка: он выбирает канальный рецепт и закрепляется в render manifest. Scene IDs уникальны; приложение создаёт `image:<scene-id>` tasks. Остальные типы — actual media/SRT/QA/release-spec/remote receipts по task context. Файл с удобным расширением не доказывает реальный медиаформат.

`packaging` output — strict `ReleaseSpec` по `src/ytvideos/release.py`, без полей brief/plan/notes. `run_id`, `channel_id`, `revision` и `format` должны совпасть с текущим run; несоответствие отклоняется до создания зависимых обложек. На раннем этапе неизвестные optional `media_sha256`, `thumbnail_sha256` и `ab_variants` опустить, а не заполнять `null` или примерными значениями. Структура обязательного `thumbnail_plan`, проверки концептов и exact metadata — [контракт обложки](thumbnail-contract.md#план-концептов). После получения файлов финальный spec связывается через `prepare-release`, без повторного завершения packaging.

## Источники и обложки

Зарегистрировать фактически доступные source/reference/rights bytes:

```bash
uv run python -m ytvideos attach-artifact --run RUN_ID --file source.mp4 --kind source_video --source SOURCE_REFERENCE --expected-sha256 EXPECTED_SHA256
uv run python -m ytvideos attach-artifact --run RUN_ID --file license.pdf --kind rights_evidence --source RIGHTS_REFERENCE
```

`--expected-sha256` необязателен; при его наличии bytes должны совпасть. Сохранить возвращённые opaque artifact IDs. Регистрация файла не подтверждает права на его использование.

Для `licensed_clips` и `music_first` сцена содержит `source_clip` с полями `source_artifact_id`, `rights_artifact_id`, `start_seconds`, `end_seconds`, `authority`. Оба artifacts должны быть зарегистрированы, authority — конкретный источник полномочий. Выход scene task — реальный video extract либо JSON `{"clip_artifact_id":"EXISTING_ARTIFACT_ID","source_clip":{...}}` с тем же pinned source. Проверка связывает bytes, source duration и extraction bounds; editorial rights review остаётся обязательным. Для музыкальных переходов исходный интервал включает полную видимость плана по правилу ниже.

Создание thumbnail tasks, exact brief/concept binding и независимый review определены в [контракте обложки](thumbnail-contract.md), который входит в packaging и thumbnail packets.

Briefs, план сравнения и последующие наблюдения сохранять отдельными supporting artifacts. Например, после заполнения реальных файлов по [thumbnail experiments](thumbnail-experiments.md#план-сравнения-и-ручная-фиксация):

```bash
uv run python -m ytvideos attach-artifact --run RUN_ID --file thumbnail-brief.json --kind thumbnail_brief --source BRIEF_REFERENCE
uv run python -m ytvideos attach-artifact --run RUN_ID --file thumbnail-plan.json --kind thumbnail_experiment_plan --source PLAN_REFERENCE
uv run python -m ytvideos attach-artifact --run RUN_ID --file thumbnail-observation.json --kind thumbnail_experiment_observation --source OBSERVATION_REFERENCE
```

Последняя команда применима после фактического наблюдения; пустой план не является результатом. Сохранить возвращённые IDs и hashes, новые наблюдения добавлять отдельными файлами. `attach-artifact` сохраняет bytes/provenance, но не валидирует семантику этих JSON и не включает файл автоматически в `context.inputs` или `supporting_inputs`. Отдельную research note передать по artifact ID/path явно; запись внутри принятого research output доступна packaging через `supporting_inputs`. Не менять завершённый research ради добавления поздних результатов A/B.

## Render manifest и delivery evidence

Перед claim production-task проверить `production_requirements.configured` и `unresolved`. Значения получаются из pinned `channel.json`, формата и выбранного `production_variant`; произвольные defaults и неподходящий рецепт не заполняют пробелы. Для render/review обязательны точные canvas/FPS/video/audio codecs, SAR/цвет, motion/transitions/frame policy, captions/font, музыка и применимый end screen. Неполная policy блокирует production до reservation/provider dispatch, оставляя research/script доступными.

Необязательные `production.audio.channels` и `sample_rate` задают положительные целые значения для конкретного формата; при отсутствии сохраняется общая политика исходного звука. Все Shorts Scenes используют stereo/48000 Hz по своим recipes. Приёмка сравнивает эти параметры с actual audio stream и проверяет, что обе границы обязательной звуковой дорожки и длительность контейнера совпадают с video timeline с допуском кадра/AAC-пакета: отвергаются и недостающий звук, и лишний звуковой хвост после последнего кадра. Более длинная длительность контейнера не доказывает полноту audio stream; намеренная тишина остаётся частью полного микса.

Сохранить единый production manifest. Поля, нужные `complete`, не заменяют дополнительные параметры канонического renderer:

| Поле | Контракт |
|---|---|
| `purpose`, `channel`, `format`, `production_variant` | `production`, ID канала, формат и выбранный вариант; без вариантов поле omit/null |
| `canvas`, `fps`, `audio` | Закреплённые размеры/FPS и путь к точному принятому audio output |
| `scenes` | Принятые сценовые файлы по порядку и с тем же количеством; непрерывные `start_frame` / exclusive `end_frame` от нуля |
| `scenes[].image` / `scenes[].clip` | Actual image для illustrated или clip для licensed_clips/music_first; JSON receipt клипа не является самим видео |
| `scenes[].direction`, `zoom` | При `whole_frame` разрешённые horizontal direction/zoom; у каждой обычной сцены есть движение; renderer задаёт его плавную траекторию |
| `transitions`, `overlays` | Канальный режим; каждый overlay имеет `role`, `path`, `sha256`, frame interval. Decorative frame берётся только из exact approved asset, когда policy его допускает |
| `has_speech`, `subtitles`, `srt` | Boolean совпадает с принятым speech mode; для word captions `subtitles.mode: words`, для музыкального вокала — `lyrics`; путь к принятому manual SRT, когда требуется. Для `none`: `has_speech: false`, `subtitles.mode: none`, без SRT. Отсутствие речи не отменяет обязательный audio stream |
| `scenes[].role: end_screen` | Только последний интервал и точная канальная длительность, когда end screen требуется |
| `music` | Явное решение по схеме ниже |

Если музыка присутствует, `music.status: present`, `tracks` содержит реальные `{path,sha256,start_frame,end_frame}`, `mix_evidence` — `{path,sha256}` отчёта фактического сведения. Он содержит `audio_sha256` принятого микса, `track_sha256` всех использованных tracks, actual `argv` и `returncode: 0`. При обязательной музыке tracks и намеренные паузы `silences: [{start_frame,end_frame,reason}]` покрывают весь timeline. Для optional music без подложки записать `status: not_used` и содержательный `reason`.

В верхний уровень render receipt добавить `delivery_evidence: {path,sha256}` отдельного JSON:

```json
{
  "schema": "ytv-production-delivery-v1",
  "media_sha256": "EXACT_MP4_SHA256",
  "requirements_sha256": "SHA256_FROM_PRODUCTION_REQUIREMENTS",
  "manifest": {"path": "/absolute/path/to/manifest.json", "sha256": "ACTUAL_SHA256"},
  "execution": {"path": "/absolute/path/to/execution.json", "sha256": "ACTUAL_SHA256"},
  "renderer_receipt": {"path": "/absolute/path/to/render-receipt.json", "sha256": "ACTUAL_SHA256"}
}
```

`execution` фиксирует фактический запуск: `run_id`, `task_id`, `claim_token`, `input_hash` текущего claim, `kind` (`montage`, `music_render` или `host_render`), `state: completed`, `returncode: 0`, actual `argv`, `outputs`, `output_artifacts: [{path,sha256}]` и `inputs: [{path,sha256}]`. Inputs включают manifest, exact принятые audio/scenes/SRT, overlays, music tracks и mix evidence; перечислять только реально использованные bytes. Пути execution — абсолютные, относительные media paths manifest разрешаются от каталога manifest. Core сверяет ordered scene hashes, число кадров, duration, policy и MP4 bytes; сохраняет связанные evidence в store.

Для illustrated `word_highlight` обязателен canonical montage и `renderer_receipt`, проверяемый `automation/ffmpeg_montage/delivery.py`: он связывает word map, exact script/audio, actual font face/index/hash, профили, export contract и замороженный код renderer. Переименованный файл другого шрифта или ручные группы по три слова не заменяют эту подготовку. Для `music_first` обязателен отдельный canonical `music_render` и его sidecar по разделу ниже. `execute-media` сохраняет execution/evidence, но его успех не заменяет `complete` и независимый final review. Для другого поддержанного host render поле `renderer_receipt` опускается; остальные привязки сохраняются. Still-image montage не монтирует source clips.

### Полные исходные интервалы персонажного эдита

При `production_requirements.visual.source_interval_review: true` (Scenes `character_edit`) каждый элемент `scenes` дополнительно фиксирует:

| Поле | Контракт |
|---|---|
| `id`, `clip_sha256` | ID принятого storyboard segment и hash фактического принятого extract |
| `source` | Ровно `{path,sha256,start_seconds,end_seconds}`: абсолютный путь исходника и полный использованный source interval, включая нахлёсты |
| `visible_start_frame`, `visible_end_frame` | Полная видимость данного плана на финальном timeline, exclusive end; охватывает его обычный `start_frame` / `end_frame` и оба нахлёста |
| `crop` | `{interpolation,keyframes:[{frame,box}]}`: точный способ интерполяции и фактические ключи кадрирования, где `box` — `[left,top,right,bottom]` в пикселях исходника. Ключи возрастают и включают первый и последний видимый кадр; для неизменного crop эти два box совпадают |

В существующем `visual_review.observed.evidence` сохранить JSON `ytv-source-fragment-review-v1` с `artifact_sha256` точного финального MP4, тем же `reviewer` и ordered `fragments` — по одной записи на каждый принятый фрагмент. Каждая запись содержит:

- `id`, `clip_sha256`, `source`, `crop` точно из manifest; `timeline` с его `start_frame`, `end_frame`, `visible_start_frame`, `visible_end_frame`.
- `method` фактического полного просмотра исходного движения, движения в MP4 и проверки стыков; `source_coverage: [{start_seconds,end_seconds}]` покрывает весь использованный исходный интервал, а не только три отдельные картинки. `final_coverage` той же формы покрывает весь видимый интервал фрагмента в секундах финального MP4, включая перекрытия переходов. `source_inspection` и `final_inspection` содержат ровно `mode` (`video_playback` либо `av_playback`), фактический непустой `tool` и `playback_speed: 1`; описание листов кадров в `method` не заменяет воспроизведение.
- `source_anchors_seconds: [first,middle,last]` — реальные PTS первого использованного кадра, кадра ближайшего к середине source interval и последнего до exclusive end, относительно начала контейнера. Получить их можно через `ytvideos.media_checks.source_frame_anchors(source_path,start_seconds,end_seconds)`: helper читает только ограниченный исходный интервал, учитывает исходный start time, фильтрует кадры до входа после seek и поддерживает VFR. FPS финального ролика не заменяет PTS исходника; при входе между кадрами первый anchor может быть позже source in. `final_anchors_frames` — `[visible_start_frame, floor((visible_start_frame + visible_end_frame - 1)/2), visible_end_frame - 1]`.
- `checked_transition_frames` — уникальный возрастающий список из `visible_start_frame`, `start_frame`, `end_frame-1`, `visible_end_frame-1`: оба конца и полная видимость переходов. Эти опоры сопровождают просмотр переходов в движении.
- `checks` с пятью объектами `source_motion`, `crop`, `internal_cuts`, `final_motion`, `transitions`; каждый содержит `status: PASS | FAIL | UNVERIFIED` и конкретные непустые `notes`.

Probe учитывает задержку B-frames в исходных кадрах, включая низкий FPS. При отсутствии `stream.duration` конец контейнера не подтверждает конец видеопотока: покрытие границы проверяется по PTS и длительности декодированных видеокадров, чтобы длинный аудиохвост не расширял исходный видеоинтервал.

`complete review` требует все пять `PASS` у каждого фрагмента, совпадение source hash/interval с принятым storyboard, clip hash, crop, полной видимости и MP4 hash. Пропущенный фрагмент, неполное source coverage, `FAIL`, `UNVERIFIED` или данные предыдущего crop/монтажа отвергаются даже при общем `visual_review.status: pass`. Исходники из отчёта сохраняются и сверяются по hash. Автоматический detector, контакт-лист или decode сами не создают эти наблюдения; критерии реального просмотра остаются в [EDIT_NOTES](../../channels/scenes_on_repeat/docs/EDIT_NOTES.md#проверка-каждого-фрагмента-персонажного-эдита).

`--technical-probe` предназначен для изолированных инструментальных fixtures. Его output нельзя завершить или выпустить как production MP4.

### Локальная монтажная проба

`automation/montage_trial.py` собирает существующие изображения и видеоклипы в отдельный немой preview. Это локальная операция без provider calls. Процедура принадлежит [video-clips](../../.agents/skills/ytv-produce-video/references/video-clips.md#локальная-монтажная-проба); production contracts и gates сохраняются.

```bash
uv run python automation/montage_trial.py --manifest trial.json --output /absolute/path/to/new-trial.mp4
```

Manifest имеет `schema: ytv.montage_trial.v1`, `purpose: montage_trial`, `provenance: {run_id, script:{path,sha256}, storyboard:{path,sha256}}`, явные `canvas:[width,height]`, целый `fps`, `audio_policy: mute`, непустой `timing_basis` и `scenes`. Относительные пути разрешаются от manifest. Canvas/FPS выбираются из закреплённых требований выпуска; сам standalone helper не удостоверяет run identity. Hashes script/storyboard и источников проверяются по реальным bytes.

Каждая сцена содержит уникальный `id`, `type: image | video`, `source`, `source_sha256` и непрерывные полуоткрытые `start_frame`/`end_frame`. Для `image` обязательны `direction` и `zoom`, необязательный `camera` использует canonical image-motion контракт: `start/end: {center:[x,y],scale}`, `focus:[x,y]`, `subject`, `reason`. Разрешённый канальным планом hold задаётся явно через `none` и одинаковые camera endpoints. Для `video` обязательны `source_in_seconds`, `used_duration_frames`, равное длине timeline window, и явные `direction: none`, `zoom: none`; camera и дополнительное движение для видео отвергаются. Недостаточный видеоинтервал не дополняется повтором последнего кадра. Неизвестные поля, audio/overlays и изменение скорости этим helper не поддерживаются.

Код использует реальные преобразования SDR цвета, proportional cover crop, square pixels, заданный FPS и H.264/yuv420p с Fast Start. Цветовые свойства видео должны быть известны и поддержаны; RGB PNG интерпретируется как sRGB full-range, это записывается как предположение. Неизвестный цвет видео не получает выдуманные input tags. Параметры кодирования и наблюдаемые свойства сохраняются; metadata не доказывают зрительную оценку цвета.

Sidecar `MP4.montage_trial.json` связывает exact manifest/input/document/code hashes, actual argv, исходные свойства, использованные интервалы и фактический output probe/hash. Он содержит `production_acceptance:false`, `review:UNVERIFIED`. Существующие output/receipt не перезаписываются. Регистрация `attach-artifact --kind montage_trial` добавляет preview к тому же run; она не создаёт render output, QA или approval.

Для звуковой пробы `python automation/montage_trial_sound.py --manifest sound.json --output NEW.mp4` добавляет дорожки без перекодирования видео. Схема `ytv.montage_trial_sound.v1`: `picture` и `picture_receipt` содержат `path` и `sha256`; `required_roles` и `layers` задаются явно. Слой: `role` (narration/music/clip/ambience/foley), `path`, `sha256`, `at`, `source_in`, `duration`, `gain_db`, `fade_in`, `fade_out`. Время в секундах; для clip указать `scene`, совпадающую с источником и интервалом картинки. Обязательный clip должен покрыть все видео в пробе; обязательная music — весь монтаж. Сохраняются технический receipt, манифест и результаты прослушивания или честный UNVERIFIED. Проба с временным голосом не закрывает production audio/render.

### Музыкальный рендер

`music_first` исполняется по принятому typed edit-script. Audio task требует `audio.mix`; прослушивание учитывается по [production before listening](#audio-production-before-listening); `vocal` также использует `subtitle.align`, а `instrumental` завершает subtitles через `no_speech`. Читать точные checks и output kind из task context и `task_guide.music_edit`. Регистрация исходников и `rights_evidence` сохраняет bytes; право использования подтверждается отдельной проверкой.

Подготовить source audio через `execute-media` с `kind: mix` и [общим manifest](#media-изображения-release) `ytv-source-audio-v1`. Для музыки segments имеют IDs и порядок принятого плана, идут непрерывно из одной зарегистрированной записи с `gain: 1`. Native executor возвращает `mix_evidence: {path,sha256}`: JSON `ytv-source-mix-evidence-v1` связывает `audio_sha256`, список `track_sha256`, actual `argv`, `returncode: 0`, `execution` и `source_plan` records. В `audio` receipt включить этот record в `checks.source_identity.observed.mix_evidence`; прослушивание и применимый `no_speech` сохраняются отдельными checks.

Для выбранного музыкального конца source plan может содержать необязательный `fade_out_seconds`: конечное число от 0 до полной длительности микса включительно, без boolean. При 0 или отсутствии поля сохраняется исходный естественный хвост; положительное значение выполняет один линейный fade в конце уже соединённой дорожки. Параметр выбирает монтажёр по [музыкальному концу](../standards/audio.md#музыкальный-конец), фиксируя выбранную границу, метод и прослушивание; одинаковый fade всем трекам автоматически не назначается. Операция не меняет скорость, source offset, музыкальную фазу или длину timeline; исходная запись и `gain: 1` остаются обязательными. `source_plan`/execution hashes связывают точный fade, а `fragment_contract.ending` сохраняет `source_end_seconds` и `fade_out_seconds`. Незавершённую фразу сначала закончить выбором/перемонтажом интервала, затем подобрать спад; технический fade не подтверждает естественность на слух.

Для render передать такой request, заменив пути реальными абсолютными путями текущего claim:

```json
{
  "kind": "music_render",
  "args": ["/absolute/music-manifest.json", "--output", "/absolute/workspace/runs/RUN_ID/attempts/TOKEN/final.mp4"],
  "prepared_inputs": ["/absolute/music-manifest.json"],
  "outputs": ["/absolute/workspace/runs/RUN_ID/attempts/TOKEN/final.mp4"]
}
```

Runtime сам добавляет `--work-dir` и `--requirements` из pinned profile и принятого script; caller не переопределяет их. Manifest имеет `schema: ytv-music-render-v1`, общие `purpose/channel/format/production_variant/canvas/fps/has_speech`, пути к принятым `script` и `audio`, а также поля ниже. Каждый record `{path,sha256}` использует существующий canonical absolute path и фактический hash.

| Поле | Требование музыкального renderer |
|---|---|
| `scenes` | Не менее двух планов, каждый не короче четырёх кадров. IDs/порядок и clips совпадают с принятым storyboard и script segments; timeline непрерывен. |
| `scenes[].direction/zoom/scale/easing` | `direction: none`, `zoom: in` либо `out`, `scale` из pinned `music_edit.zoom` в выбранном направлении, `easing: smoothstep`. |
| `scenes[].source` | Оригинальные `path`, `sha256`, `start_seconds`, `end_seconds`, `rights_evidence` record и необязательный `source_page`. Один original footage SHA используется только одним планом. Исходный интервал включает видимость перехода: входящий план с `cut−1`, исходящий до exclusive `cut+2`; начало/конец ограничены timeline. Эти диапазоны и права совпадают с accepted `source_clip`. |
| `planner` | `input` и `output` records canonical `music_montage.py`. Вход использует exact accepted audio, 30 fps и полную длительность; renderer пересчитывает output, порядок/акценты/исходные интервалы и отвергает ручную замену результата. `approved_accents`, если нужны, содержат `reason` и bound `evidence`. |
| `color`, `transition` | Color равен pinned `music_edit.color`; transition сохраняет все pinned поля `music_edit.transition` и выбранные для этого монтажа `0 < blur_sigma_px <= 100`, `0 < brightness <= 1`. Каждый стык включает все три компонента. Цвет преобразуется в BT.709 limited YUV при рендере. |
| `music` | `status: present`, один `tracks` element с оригинальными `path/sha256`, `source_in_seconds`, `start_frame: 0`, `end_frame` полного timeline; возвращённый `mix_evidence` и зарегистрированный `rights_evidence` record. Отрывок непрерывен, паузы или подменённый mix не допускаются. |
| `subtitles` для `vocal` | `mode: lyrics`, `words` record, `font: {path,sha256,index}`, `settings` точно из pinned `music_edit.lyrics`; верхнеуровневый `srt` указывает на принятый SRT. Фактическая family/style шрифта соответствует профилю; переименованный substitute не проходит проверку. |
| `subtitles.beats` | Необязательный `{path,sha256}` record карты дополнительных акцентов из `music_beats.py` на exact accepted mix. JSON карты содержит `sha256` аудио, `fps: 30`, `frames` полного timeline, `source_start_seconds: 0`, точную `duration_seconds`, `candidates: [{frame,...}]` с уникальными возрастающими целыми кадрами от `0` до exclusive `frames`. Native renderer передаёт файл через `--beats`, связывает его bytes с execution/CAS и проверяет union beats + cuts с приоритетом cut при vocal snapping. Без карты сохраняется cuts-only маршрут; неизвестные поля `subtitles` отвергаются. |
| `subtitles` для `instrumental` | `{"mode":"none"}`, `has_speech: false`, без SRT; принятое отсутствие речи уже связано с exact audio. |

Vocal `words` JSON содержит `audio_sha256`, `transcript_sha256` точного `speech.text` в UTF-8 и `words: [{text,start_seconds,end_seconds}]`. Слова сохраняются полностью и по порядку; нормализация NFC удаляет пунктуацию, сохраняя буквы и цифры. Начала возрастают, каждый интервал лежит внутри финального музыкального отрывка. Канонический lyric compositor использует принятые settings и воспроизводимый `motion-seed: 17`.

Renderer создаёт `final.mp4.delivery.json` со schema `ytv-music-render-receipt-v1`: exact command, engine/input hashes, lyric mask/plan/cuts при вокале, `technical_review`, `fragment_contract`, `fragment_index` и `fragments`. Журнал связывает оригинальные футажи, исходную музыкальную запись с отступом, финальный MP4 и hash встроенных audio packets. `execute-media` возвращает общий `delivery_evidence`, ссылающийся на manifest, execution и этот sidecar. `complete` повторно проверяет связи, команду, timeline, шрифт и слова и сохраняет records в CAS. Sidecar оставляет `review_status: UNVERIFIED`: технический контракт и журнал не подтверждают качество монтажа, права или прослушивание. До gate точного MP4 нужен полный независимый review, включая применимый аудиовизуальный loop.

## Проверки media и review

`complete` самостоятельно проверяет audio/video через actual ffprobe и полное FFmpeg decode с timeout 300 секунд; render требует настоящего MP4, допустимого codec/tag и ожидаемых streams. Pillow проверяет image bytes/размеры, canonical SRT parser — структуру и cue bounds по фактическому аудио. Измерения сохраняются в task `media_validation`. Decode выполняется вне DB transaction; перед commit повторяются claim/input/artifact проверки. Эти измерения не подтверждают смысл, произношение или визуальную приёмку.

Review output — QA JSON с обязательными `reviewed_sha256` и `probe`. Первое поле равно hash текущего render, второе получается вызовом `ytvideos.media_checks.probe_media` на том же файле. Например, получить фактический summary можно так:

```bash
uv run python -c 'import json,sys; from ytvideos.media_checks import probe_media; print(json.dumps(probe_media(sys.argv[1])))' /absolute/path/to/final.mp4
```

Вставить полученный объект в `probe`, сохранить findings и отдельный receipt со всеми текущими `context.required_checks`. Выдуманная duration или summary другого файла отвергается. Помимо базовых проверок канальная policy добавляет motion/music/captions/frame/end-screen/Shorts AV loop там, где они применимы.

Каждый review check требует `status: pass`, actual `method` и `observed` с полями:

```json
{
  "artifact_sha256": "EXACT_RENDERED_MP4_SHA256",
  "reviewer": "ACTUAL_INDEPENDENT_REVIEWER",
  "notes": "Конкретные наблюдения выполненной проверки",
  "inspection": {"mode": "av_playback", "tool": "ACTUAL_PLAYER_AND_SESSION_REFERENCE", "playback_speed": 1},
  "coverage": [{"start_seconds": 0, "end_seconds": 43.2}],
  "evidence": {"path": "/absolute/path/to/review-evidence.json", "sha256": "ACTUAL_SHA256"}
}
```

Длительность 43.2 здесь иллюстрирует форму: подставить измеренные intervals этого файла. Coverage `visual_review`, `listening`, `subtitles`, `music`, `motion`, `captions` должен покрывать весь MP4; прочие checks указывают фактически проверенные интервалы. Reviewer и worker final review отличаются от render producer. Evidence bytes проверяются и сохраняются. Если обязательная проверка не выполнена, сохранить findings как `UNVERIFIED` вне успешного completion; не ставить `pass` для обхода gate. Пропуск применимого check нельзя объяснить отсутствием capability: это конкретный blocker его завершения. Отсутствие речи, рамки или optional music проверяется как фактическое соответствие policy, без утверждения о прослушивании несуществующей дорожки.

`observed.inspection` обязателен и описывает реально выполненный метод. Playback-режимы `video_playback`, `audio_listening`, `av_playback` содержат ровно `mode`, непустой `tool` и положительную конечную `playback_speed`; приёмка `motion` требует скорости 1×, замедленный разбор дополняет её. `motion`, `subtitles`, `captions` требуют видео или AV; `listening`, `music`, `no_speech` — аудио или AV. `av_loop` требует совместного `av_playback` на скорости 1×; раздельные картинки и звук не подтверждают аудиовизуальный стык. `media_probe` и `document_inspection` содержат только `mode`/`tool` и не закрывают перцептивные проверки.

`frame_inspection` содержит ровно `mode`, `tool`, `sampling` (`all_frames` или `sampled_frames`), числовой `source_fps`, целый `frame_count`, `inspected_frames` (возрастающие уникальные индексы от 0), `display_size` (фактические ширина/высота отображения кадра). FPS и число кадров сверяются с actual probe точного файла. Coverage описывает просмотренные кадры, а не полный промежуток между редкими выборками. Для `visual_review` нужны все кадры; даже полный лист кадров не закрывает движение, звук и синхронизацию. Свободный `method` поясняет проверку, но не заменяет эти поля. Валидатор проверяет соответствие объявленных данных: он не доказывает, что человек или агент действительно смотрел/слушал.

Новый контракт применяется с соответствующей версией кода и инструкций. Для существующего pinned run требуется штатная [миграция](../migration.md); историческим receipts нельзя дописывать несуществующий просмотр ради прохождения нового check.

## Receipt

Каждый `complete` получает отдельный JSON, привязанный к exact claim и output bytes:

```json
{
  "run_id": "RUN_ID",
  "task_id": "research",
  "input_hash": "EXACT_VALUE_FROM_CLAIM",
  "output_sha256": "SHA256_OF_EXACT_OUTPUT_BYTES",
  "worker": "EXACT_WORKER_FROM_CLAIM",
  "checks": [
    {
      "name": "sources",
      "status": "pass",
      "method": "actual method used",
      "observed": {"evidence": "actual observation and source reference"}
    }
  ]
}
```

Это структурный образец. Нельзя скопировать PASS или слова `actual observation` вместо выполненной проверки. Заполнить **все** имена из `context.required_checks`, каждое один раз, с непустым структурированным observed и реальным method. Отсутствующий/неуспешный обязательный check блокирует complete; сохранять черновик и конкретный blocker, не превращать UNVERIFIED в pass.

Для `script` обязательны factual_support, first_listener, viewer_value и independent_review. В `independent_review.observed` записать реального отличного от автора `reviewer`, `artifact_sha256` точного текста и `evidence: {path,sha256}` **одного фактического ответа reviewer**. Core читает JSON-объект ответа, сверяет исходный материал и сохраняет оба файла в CAS. JSON-строка с сериализованным объектом, произвольный текст, авторский пересказ и одно имя reviewer не являются review result. Если независимый reviewer недоступен, текст можно сохранить, но ready script gate не подтверждён.

Для narrative Short с `production_requirements.narrative_loop: required` добавляется обязательный `narrative_loop`. Long и рецепты с `not_applicable` не получают narrator check; аудиовизуальная петля Short всё равно проверяется на exact MP4. Отсутствующая policy Short — unresolved, не автоматическое исключение.

Подготовить exact reading input через канонический helper. `seam.json` содержит только `opening` и `ending`: точные неперекрывающиеся prefix/suffix сценария после обрезки краевых пробелов, с контекстом крайних реплик. Не делить слово. Для narrative Short:

```bash
uv run python -m ytvideos.script_review --script script.en.txt --seam seam.json --output reader-input.json
```

Для Long или non-narrative edit-plan опустить `--seam`. Helper создаёт input `ytv-script-review-input-v1` с точным исходным текстом/hash, инструкцией reviewer и **`output_contract` — полной JSON Schema ответа**. Имена required fields и enums общие с валидатором; контракт не содержит заранее выбранного PASS или выдуманных identity/hash. При петле input добавляет точный стык и `two_cycles = script_text + "\n\n" + script_text`; ответ содержит соответствующий `narrative_loop`, иначе `null`. Helper возвращает path/hash и `review_performed: false`: подготовка материала не выполняет review. Уже существующий output не перезаписывается. Не заменять два полных цикла одним стыком или авторским утверждением «прочитал два раза».

Передать **весь input**, включая `output_contract`, свежей независимой сессии без авторского диагноза/вердикта; попросить читать по процедуре [editorial](../standards/editorial.md#ограниченный-review) и **самостоятельно записать итоговый JSON по выданной схеме**. Host передаёт descriptor input из stdout helper и фактические tool/session IDs; если ID известен только после создания сессии, передаёт его follow-up. Reviewer использует этот descriptor в `input`, свой реальный ID в `reviewer` и `source.session_id`, фактический инструмент вызова в `source.tool`. Input hash можно вычислить по bytes файла; это не hash сценария. При недостающих metadata запросить их у host, не выдумывать. Опциональный `response_id` добавлять только когда runtime действительно его вернул. Сохранить ответ reviewer без переформулирования, дописывания пропущенных проверок или смены решения. IDs/hash обеспечивают проверяемую ссылку на trace, но не являются криптографическим подтверждением происхождения или доказательством чтения.

Проверить структуру и точные bindings ответа до попытки `complete`:

```bash
uv run python -m ytvideos.script_review --script script.en.txt --seam seam.json --check-response reader-response.json --author ACTUAL_SCRIPT_WORKER_ID
```

Для неприменимой narrator-петли опустить `--seam`. Корректные `revise` и `unverified` дают exit 0 с `structurally_valid: true`, своим исходным `decision` и `pass_consistent: false`: это валидное отрицательное evidence, а не успешная приёмка. Команда не меняет response, run или approval и возвращает `review_performed: false`, `script_accepted: false`. Неверная структура/hash вызывает ошибку; попросить **того же reviewer** самостоятельно исправить форму без смены его решения. Автор не переписывает review. Runtime `complete` по-прежнему требует согласованный PASS без blocking findings и с PASS применимой петли.

Один response object `ytv-script-review-v1` служит evidence для `independent_review` и, когда требуется, для `narrative_loop`:

```json
{
  "schema": "ytv-script-review-v1",
  "script_sha256": "EXACT_SCRIPT_SHA256",
  "reviewer": "ACTUAL_INDEPENDENT_REVIEWER",
  "source": {
    "tool": "ACTUAL_HOST_TOOL",
    "session_id": "ACTUAL_INDEPENDENT_REVIEWER"
  },
  "input": {"path": "/absolute/path/reader-input.json", "sha256": "EXACT_READER_INPUT_SHA256"},
  "decision": "unverified",
  "first_listener": {
    "understood": "Что reviewer понял при первом чтении",
    "attention": "Стал бы продолжать; где и почему остановился бы",
    "quotes": ["Точная подтверждающая цитата из сценария"]
  },
  "findings": [],
  "narrative_loop": {
    "opening": "Точный начальный фрагмент",
    "ending": "Точный конечный фрагмент",
    "joined_excerpt": "Точный конечный фрагмент\nТочный начальный фрагмент",
    "decision": "unverified",
    "observations": {
      "continuation": "Конкретная смысловая или грамматическая связь крайних фраз",
      "cold_open": "Почему начало понятно отдельно",
      "payoff_quote": "Точная цитата отдачи из этого сценария",
      "payoff_before_repeat": "Что уже разрешено до повтора",
      "two_cycle_read": "Собственное наблюдение reviewer при чтении двух полных циклов",
      "restart_test": "Почему это продолжение, либо где слышится новый старт или только повтор темы"
    }
  }
}
```

Это форма для фактического ответа, не готовый PASS. Reviewer выбирает `pass`, `revise` или `unverified`; каждый finding содержит `severity: blocking|non_blocking`, точную `quote` и `finding`. Незавершённый `blocking` конфликтует с общим PASS. Для неприменимой narrator-петли поле `narrative_loop` равно `null`; придумывать речевое кольцо edit-plan не требуется.

`narrative_loop.observed` сохраняет `artifact_sha256`, `reviewer`, `opening`, `ending`, `joined_excerpt` и **тот же evidence record**, что `independent_review.observed`. `joined_excerpt` строго равен `ending + "\n" + opening`. Core проверяет точные bytes/hash, literal материал двух циклов, совпадение reviewer/стыка, обязательные наблюдения и непротиворечивые решения. Счётчики реплик и классификация `continuous_narration` не заменяют фактический ответ reader. Код не распознаёт смысл, интонацию, честность наблюдений или художественное качество. При изменении текста сформировать новый input и получить ответ на точную новую версию.

При дефекте уже принятого `source_script` сохранить точный исходник и незавершённую проверку; предложить исправленную пару/версию отдельно по [workflow](../workflow.md#готовый-текст-и-набросок). Не переписывать присланный текст незаметно и не готовить подробный storyboard/сюжетный PR до проверки текста. Ответ reviewer только о фактах/атрибуции не разрешает автору приписать ему успешную проверку петли.

SHA-256 считать по actual bytes после окончательного сохранения, например `python3 -c 'import hashlib,pathlib; print(hashlib.sha256(pathlib.Path("output.json").read_bytes()).hexdigest())'`.

```bash
uv run python -m ytvideos complete --run RUN_ID --task research --token TOKEN --output output.json --receipt receipt.json --actual-units 0
uv run python -m ytvideos next --run RUN_ID
```

`--actual-units 0` использовать только при действительно известной нулевой цене; при неизвестной цене аргумент опустить, reservation останется unknown. После research без дополнительного выбора темы claim готовый script, написать/проверить полный текст и complete тем же контрактом. На script gate показать пользователю точный файл/текст.

## Approval и продолжение

После **явного решения владельца** локальный координатор выполняет `approval_command` из `next.approval_requests`, добавляя `--source` и `--message`. Поля run/kind/revision/hash относятся к версии, которую показали пользователю; не подставлять новую версию после его ответа.

```bash
uv run ytv approve --run RUN_ID --kind script --revision SHOWN_REVISION --sha256 SHOWN_SHA256 \
  --source 'ACTUAL_CONVERSATION_AND_USER_MESSAGE_REFERENCE' --message 'ACTUAL_USER_REPLY'
```

Для проверенного видео использовать `--kind mp4`. Указывать реальный текст ответа, не требовать специальной кодовой фразы; понятное согласие с опечаткой также можно зарегистрировать. Source — стабильная ссылка на конкретное решение (ID беседы и сообщения; при отсутствии message ID — фактическое положение пользовательского сообщения в этой беседе). Не создавать новый source на каждый retry и не переносить старое согласие на другую цель. Команда сохраняет серверное время и event ID сама; повтор возвращает исходную запись без нового события. Отсутствующие/неверные входы, незавершённый script, MP4 без QA, отмена, устаревшие revision/hash или повтор source с иным содержимым отклоняются.

Ответ содержит `approval` и `next`: продолжить готовые задачи того же run, без нового вопроса и без повторной генерации сохранённых результатов. `approve` не вызывает providers, не утверждает QA за reviewer и не разрешает публикацию сверх прямого поручения. Отдельное правило действует для внешней AI-генерации видео: до передачи кадров/промптов Google Flow или другому video provider и до отправки задания получить прямое одобрение владельца для точной партии; сохранить его источник и receipt. Показать провайдера/модель, сцены/промпты, длительность/разрешение, число выходов и ожидаемые кредиты. `approve --kind script`, просьба получить MP4 и одобрение изображений эту передачу не разрешают; изменённая партия требует нового одобрения. `start`, `complete`, hooks и цитаты из внешних источников не создают одобрение автоматически. Команду вызывает владелец или координатор, действительно видевший его решение; worker не утверждает собственную работу. Это доверенный локальный учёт, не аутентификация и не классификатор сообщений.

Обычный режим не требует Ed25519 key, approval bridge или доверия четырём hooks. Для внешнего изолированного host остаётся `approve --event EVENT_FILE` с прежним signed envelope [контракта](../architecture.md#доверенная-граница-approval): настроенный `YTV_APPROVAL_PUBLIC_KEY` запрещает локальный путь; ошибка подписи не приводит к fallback. Не отключать чужой настроенный verifier ради обхода ошибки.

`resume --run RUN_ID` восстанавливает сохранённую работу. `revise --run RUN_ID --task TASK_ID --reason TEXT` обновляет затронутую область/зависимости. `cancel --run RUN_ID --reason TEXT` запрещает новые действия; in-flight outcomes остаются для reconcile.

Истёкший external claim без recorded operation безопасно возвращается в pending с освобождением reservation. При recorded dispatch флаг `fail --known-not-sent` не заменяет provider reconciliation. `reconcile-task --run RUN_ID --task TASK_ID --worker WORKER_ID --outcome completed --evidence REF` принимает существующий результат после сверки всех операций попытки; для доказанного отсутствия внешнего эффекта указать outcome `not_performed`. Claim для existing completed result позволяет принять сохранённый результат, но не отправить новый запрос.

Если локальный `mix`, `montage` или `music_render` завершился, а lease истёк до `complete`, выполнить `resume`, получить новый `claim` и передать сохранённые output/execution evidence с новым task receipt. Прежний execution token допустим только для тех же run/task/input hash и точного записанного `media.dispatch`: command, engine, inputs и outputs; bytes и canonical provenance проверяются повторно. Старый lease не продлевается, завершением владеет текущий claim. Исходный producer сохраняется по `task.claimed`; ни он, ни исполнитель восстановления не могут быть final reviewer. Этот путь не повторяет provider call и не принимает paid либо неподтверждённый host execution.

Для частично выполненного `configure_release` после сверки всех отправленных операций использовать `reconcile-task --run RUN_ID --task configure_release --worker WORKER_ID --outcome continue --evidence REF`. Все исходы должны быть `confirmed` или `not_performed`; `unknown` и `dispatched` блокируют продолжение. Новый claim сохраняет confirmed действия и budget reservation: разрешены ещё не отправленные действия и новый attempt доказанно `not_performed` действия. Каждый такой повтор расходует общий `max_task_attempts`; первые разные действия не считаются повторами. Позднее observation старого attempt отклоняется. Outcome `completed` по-прежнему разрешает только принять существующий результат.

Для cancelled run после terminal observations использовать `settle-cancelled --run RUN_ID --task TASK_ID --evidence REF [--actual-units N]`. Task остаётся cancelled; UNKNOWN запрещает settlement. При confirmed вызове с неизвестной ценой reservation переходит в `unknown_reserved`, а не считается нулевой.

## Media, изображения, release

`execute-media --run RUN_ID --task TASK_ID --token TOKEN --request request.json` вызывает guarded adapter. Для TTS request `{"kind":"tts"}`: exact narration text и pinned voice выводятся из run; provider получает raw `generation_speed: 1.0`. Канальная конечная скорость применяется один раз при подготовке audio output — см. [audio](../standards/audio.md). При typed edit-script `source`/`none` TTS отвергается; audio task требует `audio.mix`; прослушивание учитывается по [production before listening](#audio-production-before-listening), checks определяются его context. Для srt/montage/inspect нужны argv, output paths внутри owned attempt и prepared_inputs по контракту `MediaExecutor`. Subprocess receipt не заменяет content QA или task complete.

Для `source`/`none` request `mix` содержит `args: [ABSOLUTE_MANIFEST, "--output", OWNED_ATTEMPT_WAV]`, `outputs: [OWNED_ATTEMPT_WAV]`, `prepared_inputs: [ABSOLUTE_MANIFEST]`. Manifest содержит `schema: ytv-source-audio-v1`, `segments: [{id,path,sha256,start_seconds,end_seconds,gain}]` и необязательный `fade_out_seconds`, других полей нет. IDs/порядок совпадают с принятым edit-script, source bytes предварительно зарегистрированы через `attach-artifact`, интервалы находятся внутри фактического audio stream, gain в диапазоне 0–4. Adapter извлекает/соединяет звук FFmpeg в WAV без изменения скорости, применяет только явно выбранный terminal fade и проверяет фактическую длительность результата против суммы интервалов. Длительность video/container не заменяет audio duration; если демультиплексор не сообщает её, проверка длины полученного WAV остаётся обязательной. Сохраняются inputs/execution; это подготовка source audio, не генерация речи и не подтверждение listening. Путь WAV должен находиться в `workspace/runs/RUN_ID/attempts/TOKEN/`; existing output сохраняется для reconcile, не перезаписывается.

Image queue использует `pool initialize|enqueue|tick|pending|claim|submitted|result|accept|reconcile|recover|status|cancel --run RUN_ID --payload FILE`. Сначала фактическая `sessions.independent` capability с `available`, `runtime_key`, `max_sessions`; initialize обязан использовать точно тот же runtime key/cap и evidence. Native submit — только после committed `pool claim` grant. `pool-candidates --runtime KEY` возвращает порядок ready dispatch. Exact payloads/семантика — [adaptive workers](../architecture/adaptive-workers.md).

Для release `prepare-release --run RUN_ID --spec SPEC --asset FILE` (повторить для каждого asset) сохраняет bytes/hashes. `operation-payload --run RUN_ID --task TASK_ID --action ACTION` даёт canonical description; `begin-operation` обязан получить совпадающий payload и current claim. Permit не означает результат; сохранить provider outcome/read-back через `observe-operation` и stage receipt.

Operation observation имеет **ровно** поля `operation_key`, `attempt_id`, `task_input_hash`, `status`, `provider_evidence`. Записать `operation_key = returned_operation.key`; `attempt_id` и `task_input_hash` копировать из той же operation без переименования. `status` — `confirmed`, `not_performed` или `unknown`; `provider_evidence` содержит ровно `method`, конкретный `observation_id` и непустой объект `observed`. Допустимые methods: `api_readback`, `studio_readback`, `adapter_execution`, `provider_job_readback`. Для confirmed upload `observed` обязан связать `channel_id`, `video_id`, `media_sha256`, `privacy: private` с настоящим provider result.

```bash
uv run python -m ytvideos observe-operation --run RUN_ID --key OPERATION_KEY --status confirmed --receipt observation.json --event-id OBSERVATION_EVENT_ID
uv run python -m ytvideos deferred-actions --run RUN_ID
```

Старый `attempt_id` не подтверждает новую попытку. `deferred-actions` возвращает сохранённые pending `verify_public` и применимый `ab_test`; автоматический dispatcher этой командой не запускается — см. [runtime](runtime.md#развёртывание).

## Audio: production before listening

Production (`audio`, and no-speech `subtitles`) may proceed without `audio.listen`.
Generation still requires its observed provider/mixer capability, approval, lease,
budget and exact media/provenance checks. Missing listening does not stop alignment
or a reviewable render, but does not establish audio quality.

Keep the required `listening` (and applicable `no_speech`) check. If listening is
unavailable, use `status: unverified`, a truthful `method`, and exactly
`observed: {"artifact_sha256": "EXACT_AUDIO_SHA256", "reason": "Concrete reason listening was not performed"}`.
For no-speech subtitles the hash is the accepted audio, not the JSON output.
Only these production perceptual checks accept this status; rights, text, identity,
speed, decoding and every other check remain mandatory PASS. Do not use this form
to disguise a failed listening check or claim a missing capability is available.

The completed production task and its immutable receipt retain `unverified_checks`;
subsequent packets expose `unverified_production_checks`. Deliver the resulting MP4
as a preview with the missing audio QA explicitly stated. Final review still needs
actual listening evidence; it does not accept UNVERIFIED and still blocks MP4
approval/upload. Production completion is not a quality approval.

Save provider handles and raw bytes normally. Never regenerate TTS merely to resume
QA. Existing runs must migrate from their original snapshot using `migrate-runtime`;
pins, approvals and budgets must not be edited directly.

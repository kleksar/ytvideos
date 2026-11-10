# CLI и контракт task result

Все команды возвращают JSON. Синтаксис текущей версии — `uv run python -m ytvideos --help`. Один workspace/store используют все связанные сессии. Ниже placeholders заменяются фактическими значениями из ответа CLI, не выдумываются.

Разделы: [запуск](#новый-сценарный-run), [outputs](#outputs), [источники и обложки](#источники-и-обложки), [media checks](#проверки-media-и-review), [receipt](#receipt), [approval/recovery](#approval-и-продолжение), [adapters и release](#media-изображения-release).

## Новый сценарный run

```bash
uv run python -m ytvideos create --channel paper_detour --format short --intent 'Нужен сюжет для канала Paper Detour'
uv run python -m ytvideos status --run RUN_ID
uv run python -m ytvideos doctor --run RUN_ID
```

До claim сохранить реально наблюдённые capabilities. Например `{"web.search":true,"model.text":true}` допустимо только когда эти tools доступны текущему worker. Запись `capabilities --run RUN_ID --file capabilities.json --evidence 'actual observation reference'` сама не предоставляет tool. Для metered audio/image требуется положительная reservation, либо подтверждённый `billing:included`; max paid budget по умолчанию не разрешает платные запросы.

```bash
uv run python -m ytvideos next --run RUN_ID
uv run python -m ytvideos context --run RUN_ID --task research --output context.json
uv run python -m ytvideos claim --run RUN_ID --task research --worker WORKER_ID
```

Claim возвращает `token`, `worker`, `input_hash`, `expires_at`, `estimated_units`, `claimed_at`. Копировать точные token/input_hash, использовать stable реальную идентичность исполнителя. Долгую задачу продлевать `heartbeat --run RUN_ID --task TASK_ID --token TOKEN`; lease не даёт право изменить scope.

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

Пример показывает форму, не источник: заменить URL/claim/location фактически прочитанными материалами. Дополнительно сохранить uncertainty, overlap/отвергнутые варианты и аудиторию. `script` output — UTF-8 файл полного narration без процедурных инструкций. Минимальная длина машинной проверки не является критерием качества: должен быть закончен сценарий, который пользователь просил.

`storyboard` output — JSON `{"scenes":[{"id":"S001","prompt":"Самодостаточное задание","visual_intent":"Смысл кадра"}]}` с необходимыми реальными timing/references/continuity. Scene IDs уникальны; приложение создаёт `image:<scene-id>` tasks. Остальные типы — actual media/SRT/QA/release-spec/remote receipts по task context. Файл с удобным расширением не доказывает реальный медиаформат.

## Источники и обложки

Зарегистрировать фактически доступные source/reference/rights bytes:

```bash
uv run python -m ytvideos attach-artifact --run RUN_ID --file source.mp4 --kind source_video --source SOURCE_REFERENCE --expected-sha256 EXPECTED_SHA256
uv run python -m ytvideos attach-artifact --run RUN_ID --file license.pdf --kind rights_evidence --source RIGHTS_REFERENCE
```

`--expected-sha256` необязателен; при его наличии bytes должны совпасть. Сохранить возвращённые opaque artifact IDs. Регистрация файла не подтверждает права на его использование.

Для `licensed_clips` сцена содержит `source_clip` с полями `source_artifact_id`, `rights_artifact_id`, `start_seconds`, `end_seconds`, `authority`. Оба artifacts должны быть зарегистрированы, authority — конкретный источник полномочий. Выход scene task — реальный video extract либо JSON `{"clip_artifact_id":"EXISTING_ARTIFACT_ID","source_clip":{...}}` с тем же pinned source. Проверка связывает bytes, source duration и extraction bounds; editorial rights review остаётся обязательным.

После script approval и завершения packaging создать brief обложки `{"id":"main","prompt":"...","visual_intent":"..."}` и вызвать:

```bash
uv run python -m ytvideos add-thumbnail-task --run RUN_ID --brief thumbnail-brief.json
```

Приложение создаёт `thumbnail:main` со stage `scene_image` и `purpose: thumbnail`. Этот task идёт в общий image pool, зависит от packaging и не ждёт storyboard/render. Созданные обложки становятся зависимостями upload; точный принятый hash затем входит в release spec. Добавлять их до начала upload.

## Проверки media и review

`complete` самостоятельно проверяет audio/video через actual ffprobe и полное FFmpeg decode с timeout 300 секунд; render требует настоящего MP4, допустимого codec/tag и ожидаемых streams. Pillow проверяет image bytes/размеры, canonical SRT parser — структуру и cue bounds по фактическому аудио. Измерения сохраняются в task `media_validation`. Decode выполняется вне DB transaction; перед commit повторяются claim/input/artifact проверки. Эти измерения не подтверждают смысл, произношение или визуальную приёмку.

Review output — QA JSON с обязательными `reviewed_sha256` и `probe`. Первое поле равно hash текущего render, второе получается вызовом `ytvideos.media_checks.probe_media` на том же файле. Например, получить фактический summary можно так:

```bash
uv run python -c 'import json,sys; from ytvideos.media_checks import probe_media; print(json.dumps(probe_media(sys.argv[1])))' /absolute/path/to/final.mp4
```

Вставить полученный объект в `probe`, сохранить findings и отдельный receipt со всеми review checks. Выдуманная duration или summary другого файла отвергается.

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

Для `script` обязательны factual_support, first_listener, viewer_value и independent_review. В `independent_review.observed` записать реального отличного от автора `reviewer` и `artifact_sha256` точного текста, плюс findings/coverage/evidence. Если независимый reviewer недоступен, текст можно сохранить, но ready script gate не подтверждён. При изменении текста обновить binding и затронутый review.

SHA-256 считать по actual bytes после окончательного сохранения, например `python3 -c 'import hashlib,pathlib; print(hashlib.sha256(pathlib.Path("output.json").read_bytes()).hexdigest())'`.

```bash
uv run python -m ytvideos complete --run RUN_ID --task research --token TOKEN --output output.json --receipt receipt.json --actual-units 0
uv run python -m ytvideos next --run RUN_ID
```

`--actual-units 0` использовать только при действительно известной нулевой цене; при неизвестной цене аргумент опустить, reservation останется unknown. После research без дополнительного выбора темы claim готовый script, написать/проверить полный текст и complete тем же контрактом. На script gate показать пользователю точный файл/текст.

## Approval и продолжение

`approve --event EVENT_FILE` принимает подлинный подписанный envelope [trusted host](../architecture.md#доверенная-граница-approval). Агент не генерирует private signing key или событие пользователя. После настоящего решения host фиксирует event; `next` возвращает следующие задачи.

`resume --run RUN_ID` восстанавливает сохранённую работу. `revise --run RUN_ID --task TASK_ID --reason TEXT` обновляет затронутую область/зависимости. `cancel --run RUN_ID --reason TEXT` запрещает новые действия; in-flight outcomes остаются для reconcile.

Истёкший external claim без recorded operation безопасно возвращается в pending с освобождением reservation. При recorded dispatch флаг `fail --known-not-sent` не заменяет provider reconciliation. `reconcile-task --run RUN_ID --task TASK_ID --worker WORKER_ID --outcome completed --evidence REF` принимает существующий результат после сверки всех операций попытки; для доказанного отсутствия внешнего эффекта указать outcome `not_performed`. Claim для existing completed result позволяет принять сохранённый результат, но не отправить новый запрос.

Для cancelled run после terminal observations использовать `settle-cancelled --run RUN_ID --task TASK_ID --evidence REF [--actual-units N]`. Task остаётся cancelled; UNKNOWN запрещает settlement. При confirmed вызове с неизвестной ценой reservation переходит в `unknown_reserved`, а не считается нулевой.

## Media, изображения, release

`execute-media --run RUN_ID --task TASK_ID --token TOKEN --request request.json` вызывает guarded adapter. Для TTS request `{"kind":"tts"}`: exact text и pinned voice выводятся из run; provider получает raw `generation_speed: 1.0`. Канальная конечная скорость применяется один раз при подготовке audio output — см. [audio](../standards/audio.md). Для srt/montage/inspect нужны argv, output paths внутри owned attempt и prepared_inputs по контракту `MediaExecutor`. Subprocess receipt не заменяет content QA или task complete.

Image queue использует `pool initialize|enqueue|tick|pending|claim|submitted|result|accept|reconcile|recover|status|cancel --run RUN_ID --payload FILE`. Сначала фактическая `sessions.independent` capability с `available`, `runtime_key`, `max_sessions`; initialize обязан использовать точно тот же runtime key/cap и evidence. Native submit — только после committed `pool claim` grant. `pool-candidates --runtime KEY` возвращает порядок ready dispatch. Exact payloads/семантика — [adaptive workers](../architecture/adaptive-workers.md).

Для release `prepare-release --run RUN_ID --spec SPEC --asset FILE` (повторить для каждого asset) сохраняет bytes/hashes. `operation-payload --run RUN_ID --task TASK_ID --action ACTION` даёт canonical description; `begin-operation` обязан получить совпадающий payload и current claim. Permit не означает результат; сохранить provider outcome/read-back через `observe-operation` и stage receipt.

Operation observation имеет **ровно** поля `operation_key`, `attempt_id`, `task_input_hash`, `status`, `provider_evidence`. Записать `operation_key = returned_operation.key`; `attempt_id` и `task_input_hash` копировать из той же operation без переименования. `status` — `confirmed`, `not_performed` или `unknown`; `provider_evidence` содержит ровно `method`, конкретный `observation_id` и непустой объект `observed`. Допустимые methods: `api_readback`, `studio_readback`, `adapter_execution`, `provider_job_readback`. Для confirmed upload `observed` обязан связать `channel_id`, `video_id`, `media_sha256`, `privacy: private` с настоящим provider result.

```bash
uv run python -m ytvideos observe-operation --run RUN_ID --key OPERATION_KEY --status confirmed --receipt observation.json --event-id OBSERVATION_EVENT_ID
uv run python -m ytvideos deferred-actions --run RUN_ID
```

Старый `attempt_id` не подтверждает новую попытку. `deferred-actions` возвращает сохранённые pending `verify_public` и применимый `ab_test`; автоматический dispatcher этой командой не запускается — см. [runtime](runtime.md#развёртывание).

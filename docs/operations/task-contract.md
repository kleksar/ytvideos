# CLI и контракт task result

Все команды возвращают JSON. Синтаксис текущей версии — `uv run python -m ytvideos --help`. Один workspace/store используют все связанные сессии. Ниже placeholders заменяются фактическими значениями из ответа CLI, не выдумываются.

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

Если failed operation гарантированно не отправлена, указать доказанное `fail --known-not-sent`. Иначе outcome UNKNOWN. `reconcile-task --outcome completed|not_performed --evidence REF` используется только после фактической сверки.

## Media, изображения, release

`execute-media --run RUN_ID --task TASK_ID --token TOKEN --request request.json` вызывает guarded adapter. Для TTS request `{"kind":"tts"}`: channel/text arguments выводятся из принятого script, не задаются произвольно. Для srt/montage/inspect нужны argv, output paths внутри owned attempt и prepared_inputs по контракту `MediaExecutor`. Subprocess receipt не заменяет content QA или task complete.

Image queue использует `pool initialize|enqueue|tick|pending|claim|submitted|result|accept|reconcile|recover|status|cancel --run RUN_ID --payload FILE`. Сначала фактическая sessions.independent capability и stable runtime_key/max_sessions/evidence; native submit только после committed `pool claim` grant. `pool-candidates --runtime KEY` возвращает порядок ready dispatch. Exact payloads/семантика — [adaptive workers](../architecture/adaptive-workers.md).

Для release `prepare-release --run RUN_ID --spec SPEC --asset FILE` (повторить для каждого asset) сохраняет bytes/hashes. `operation-payload --run RUN_ID --task TASK_ID --action ACTION` даёт canonical description; `begin-operation` обязан получить совпадающий payload и current claim. Permit не означает результат; сохранить provider outcome/read-back через `observe-operation` и stage receipt.

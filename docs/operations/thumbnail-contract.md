# Контракт обложки

Этот документ владеет структурой концептов, brief и review. Он передаётся в packaging и thumbnail packets, в том числе через `instructions` для узкой работы. Творческие требования — [thumbnail standard](../standards/thumbnails.md), процедура — [release skill](../../.agents/skills/ytv-release-video/SKILL.md), общие outputs/claims — [task contract](task-contract.md). Новых tasks, approval, сервера или настроек этот контракт не добавляет.

## План концептов

`thumbnail_plan` — обязательное имя в `receipt.checks`, рядом с `promise_matches_script` и `metadata`. Его `observed` — `{"schema":"ytv-thumbnail-plan-v1","script_sha256":"EXACT_ACCEPTED_SCRIPT_SHA256","selected_id":"main","concepts":[...]}`. Каждый concept содержит уникальный `id`, непустые `title`, `description`, `prompt`, `visual_intent`, `promise`, `first_confirmation`, `payoff`, `false_reading`, а также строки `overlay_text` (точный задуманный текст; пусто только при намеренном отсутствии надписи) и `intro_connection` (конкретная связь с интро либо пусто для других концептов). Long требует минимум три концепта и хотя бы одну непустую `intro_connection`; Short — минимум один, не фиктивный A/B. Основные title/description совпадают с ReleaseSpec дословно; повторяющиеся IDs/нормализованные promise и stale script hash отклоняются. Семантическую разницу и фактические основания runtime автоматически не оценивает.

## Brief и генерация

После script approval и завершения packaging создать brief обложки со стабильным `id`, точным выбранным `title`, полными `prompt` и `visual_intent`, а также `references` — списком зарегистрированных artifact IDs либо объектов `{"artifact_id":"ACTUAL_ID"}`. Если художественных refs действительно нет, сохранить пустой список и конкретный `reference_na_reason`; не выдумывать asset ради формы. ID/title должны совпасть с сохранённым `thumbnail_plan`; runtime добавляет выбранный `concept` в payload и передаёт его image worker. Prompt можно уточнить для технического исправления в рамках того же концепта; подмена смысла или metadata требует переработки packaging. Title нужен для пары «название + изображение» и не равен автоматически надписи `concept.overlay_text`. Пример формы:

```json
{
  "id": "main",
  "title": "Точное название из выбранного концепта",
  "prompt": "Полное задание на изображение по канальному профилю",
  "visual_intent": "Конкретный объект и смысловая связь",
  "references": ["ACTUAL_REGISTERED_REFERENCE_ID"]
}
```

После заполнения фактических значений вызвать:

```bash
uv run python -m ytvideos add-thumbnail-task --run RUN_ID --brief thumbnail-brief.json
```

Приложение создаёт `thumbnail:main` со stage `scene_image` и `purpose: thumbnail`. Этот task идёт в общий image pool, зависит от packaging и не ждёт storyboard/render. Созданные обложки становятся зависимостями upload; точный принятый hash затем входит в release spec. Добавлять их до начала upload.

## Review точной обложки

До `complete` thumbnail reviewer сохраняет **свой** JSON `ytv-thumbnail-review-result-v1`. Поля: `decision` (`pass`, `fail` или `unverified`), `source` с фактическими `tool`/`session_id`, `artifact_sha256`, `reviewer`, `title`, `concept_id`, `artwork_text`, `preview_manifest`, `phone_preview`, `crop_preview`, `observations`, `references` и при отсутствии refs `reference_na_reason`. Последние поля совпадают с observation ниже; `artwork_text` — фактически проверенная надпись, совпадающая с `concept.overlay_text` (пустой фон вместо ожидаемого текста не проходит). В `thumbnail_review.observed.evidence` передать path/hash этого exact файла. Runtime принимает только `decision: pass` и совпадающие поля; запись автором другого verdict поверх исходного review запрещена. Source — аудит, не криптографическое доказательство независимости или просмотра.

Для приёмки thumbnail создать `card.json` с точными `title` из brief и `channel` из `plan.channel.name`, затем canonical previews. Для Short:

```bash
uv run python automation/helpers/youtube-thumbnails/scripts/thumbnail_previews.py thumbnail.png --out thumbnail-qa --widths 320 --crops 2:3 --card-json card.json --theme both
```

Для Long передать `--crops` без значения: helper сохранит полный preview без дополнительных кропов. В обоих случаях обязательны просмотр artwork, уменьшения и карточки. Helper не подтверждает читаемость, не проверяет надпись автоматически и не моделирует CTR; actual YouTube surface проверяется отдельно.

Thumbnail task требует check `thumbnail_review` с `method` фактической проверки и `observed` следующей формы:

| Поле `observed` | Содержимое |
|---|---|
| `schema` | `ytv-thumbnail-review-v1` |
| `artifact_sha256`, `title`, `reviewer` | Exact artwork hash, exact brief title и реальный независимый reviewer, отличный от generator worker |
| `concept_id`, `artwork_text` | ID сохранённого концепта и фактически проверенный точный текст на artwork; сравниваются с `concept.id`/`concept.overlay_text` |
| `preview_manifest` | `{path, sha256}` canonical `thumbnail-qa/manifest.json` |
| `phone_preview`, `crop_preview` | `{path, sha256}` файлов из manifest: полный preview и central 2:3 для Short, для Long оба могут указывать на полный preview; ширина каждого 180–360 px |
| `observations` | Ровно пять непустых наблюдений: `focal_point`, `story_relation`, `title_pair`, `phone_size`, `crop` |
| `references` | По каждому выбранному ref `{artifact_id, sha256, comparison}`; при пустом списке повторить exact `reference_na_reason` из brief |
| `evidence` | `{path, sha256}` неизменённого reviewer JSON `ytv-thumbnail-review-result-v1`, не произвольного файла или авторского пересказа |

Core проверяет actual derivative bytes/geometry, карточку с exact title/channel, hashes и полноту сравнений; сохраняет evidence в artifact store. Само создание preview, фраза о бумажной фактуре или обычный `visual_review` не заменяют этот check. Структура evidence не доказывает восприятие автора отчёта или привлекательность картинки: содержательный просмотр выполняется по [thumbnail standard](../standards/thumbnails.md#qa-файла-и-пары).

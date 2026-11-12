# Text archive consultation

Task `text-archive-20261106`; GPT-5.6 Sol, Extra High. https://chatgpt.com/c/6aedc7dd-302c-83eb-a2e8-e2d8ab754a9a
Controlled lock acquired; exact prompt saved in companion file, posted message confirmed, composer empty and VERIFIED. Full answer captured from visible UI and code blocks.

## Prompt

For a Git repository that will preserve accepted video scripts and compact historical episode metadata but excludes media, suggest a minimal archival manifest that distinguishes accepted text from unknown or draft material, preserves source provenance, and warns against false claims of production readiness. No personal information.

## Answer

Минимальный вариант — хранить **статус текста отдельно от производственной готовности**. `accepted` должен означать только «этот текст принят как архивная версия», а не «факты проверены / ролик готов к производству».

```yaml
schema_version: 1

episode_id: "pd-001"
title: "Episode title"

script:
  path: "script.md"
  status: "accepted"        # accepted | draft | unknown
  sha256: "<hash>"
  accepted_revision: "git:<commit-sha>"   # only when status=accepted
  acceptance_scope: "text_only"

historical:
  period: "1919"
  places:
    - "Boston, Massachusetts"
  subjects:
    - "Great Molasses Flood"

sources:
  - id: "src-01"
    kind: "primary"         # primary | secondary | reference
    citation: "Bibliographic citation or stable URL"
    supports:
      - "Brief description of the claim/event supported"

production:
  readiness: "not_asserted" # not_asserted | reviewed | ready
  media_in_repository: false
```

К manifest стоит добавить четыре жёстких правила:

- `accepted` фиксирует **только принятую редакцию текста**; для неё обязателен hash и Git commit.
- `draft` и `unknown` нельзя автоматически повышать до `accepted` по наличию файла, имени каталога или истории Git.
- `sources` сохраняют происхождение фактов; отсутствие источника нельзя интерпретировать как подтверждение утверждения.
- `production.readiness: not_asserted` — безопасный дефолт. Наличие принятого script, metadata, source list или даже завершённого research **не является доказательством production readiness**.

Если нужен ещё более консервативный вариант, я бы вообще не использовал `ready` в архивном manifest, а оставил единственное поле:

```yaml
production_readiness: "outside_archive_scope"
```

Это почти полностью исключает ложный вывод «accepted script = готовый выпуск».

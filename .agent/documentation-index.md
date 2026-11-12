# Владельцы требований

| Правило | Единственный owner |
|---|---|
| Вход, scope, два approvals, общий lifecycle | [workflow](../docs/workflow.md) |
| Тема, факты, ценность, первый слушатель, внутренние sources | [editorial](../docs/standards/editorial.md) |
| Постановка, actual references, кадры, цельное движение | [visual](../docs/standards/visual.md) |
| Речь/voice/speed, mix, музыка, word map/SRT/caption semantics | [audio](../docs/standards/audio.md) |
| Рендер/геометрия/время/codec/QA exact MP4 | [delivery](../docs/standards/delivery.md) |
| Концепции обложек, QA пары, дизайн эксперимента и выводы | [thumbnails](../docs/standards/thumbnails.md) |
| Metadata, полный YouTube release, календарь, provider A/B и read-back | [release](../docs/standards/release.md) |
| Artifacts/cache/retention/cleanup/TEXT_ONLY | [storage](../docs/standards/storage.md) |
| State/leases/revisions/approval authority | [architecture](../docs/architecture.md) |
| Session backend, capabilities и actual executor | [runtime](../docs/operations/runtime.md) |
| Адаптивная image queue | [adaptive workers](../docs/architecture/adaptive-workers.md) |
| Переход старых работ и policy mapping | [migration](../docs/migration.md) |
| Ветка/MR/tests/evals | [development](../docs/development.md) |
| Channel style/identity/recipe | `channels/<id>/channel.json` + канальный PROFILE |
| Выбор skill по task | [manifest](skill-catalog.json) и [каталог](skill-catalog.md) |

Code/schema — источник машинной валидации. Документ не превращает неподдержанную capability в действующий tool. Фактические архивы и receipts сохраняют историю, но не являются вторыми инструкциями для новых runs.

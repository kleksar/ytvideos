# Владельцы требований

| Правило | Единственный owner |
|---|---|
| Вход, scope, два approvals, общий lifecycle | [workflow](../docs/workflow.md) |
| Тема, факты, драматургия всех каналов, переработка исходника, первый слушатель | [editorial](../docs/standards/editorial.md) |
| Естественная дикторская речь, устная редактура и EN/RU-подача | [narration](../docs/standards/narration.md) |
| Постановка, actual references, кадры, цельное движение | [visual](../docs/standards/visual.md) |
| Речь/voice/speed, mix, музыка, word map/SRT/caption semantics | [audio](../docs/standards/audio.md) |
| Рендер/геометрия/время/codec/QA exact MP4 | [delivery](../docs/standards/delivery.md) |
| Приёмы обложек, AI-черновики, карточка/начало/payoff и QA | [thumbnails](../docs/standards/thumbnails.md) |
| План/наблюдение A/B, интерпретация метрик, следующий тест | [thumbnail experiments](../docs/operations/thumbnail-experiments.md) |
| Metadata, полный YouTube release, календарь, provider A/B и read-back | [release](../docs/standards/release.md) |
| Artifacts/cache/retention/cleanup/TEXT_ONLY | [storage](../docs/standards/storage.md) |
| State/leases/revisions/approval authority | [architecture](../docs/architecture.md) |
| Session backend, capabilities и actual executor | [runtime](../docs/operations/runtime.md) |
| Общий межсессионный бюджет vidIQ | [vidIQ credits](../docs/operations/vidiq-credits.md) |
| Адаптивная image queue | [adaptive workers](../docs/architecture/adaptive-workers.md) |
| Переход старых работ и policy mapping | [migration](../docs/migration.md) |
| Ветка/MR/tests/evals | [development](../docs/development.md) |
| Channel style/identity/recipe | `channels/<id>/channel.json` + канальный PROFILE |
| Канальные документы в task, pinned snapshot, manifest worker | [task contract](../docs/operations/task-contract.md#требования-в-контексте), `src/ytvideos/context.py` и ChannelSpec |
| Выбор skill по task | [manifest](skill-catalog.json) и [каталог](skill-catalog.md) |

Skill и навык обозначают одно: короткую процедуру конкретного этапа. `AGENTS.md` выбирает вход; standard задаёт общие требования; профиль задаёт продуктовые различия; code/schema проверяет переходы и результаты. `plan` и `task_guide` — представления сохранённого runtime state, не отдельные владельцы правил.

Документ не превращает неподдержанную capability в действующий tool. Действующие инструкции описывают актуальное поведение. Архивные receipts/консультации и решения отдельного выпуска остаются evidence вне обычного production reading path; actual reference assets с provenance сохраняют своё художественное назначение.

Основания для thumbnail standard: [научные и платформенные источники](../docs/research/thumbnail-evidence.md), [опыт практика с таймкодами](../docs/research/thumbnail-practitioner-notes.md). Разборы практики помогают выбрать рабочий приём до накопления собственных результатов.

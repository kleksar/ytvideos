# Владельцы требований

| Правило | Единственный owner |
|---|---|
| Scope, два approvals, общий lifecycle | [workflow](../docs/workflow.md) |
| Обязательное чтение, preflight, выполнение, blocker и продолжение каждого task | [task-execution skill reference](../.agents/skills/ytv-start/references/task-execution.md) |
| Тема, факты, драматургия всех каналов, переработка исходника, первый слушатель | [editorial](../docs/standards/editorial.md) |
| Естественная дикторская речь, устная редактура и EN/RU-подача | [narration](../docs/standards/narration.md) |
| Постановка, actual references, кадры, цельное движение | [visual](../docs/standards/visual.md) |
| Речь/voice/speed, mix, музыка, word map/SRT/caption semantics | [audio](../docs/standards/audio.md) |
| Рендер/геометрия/время/codec/QA exact MP4 | [delivery](../docs/standards/delivery.md) |
| Подготовка платной видеопартии, приёмка и повторное использование клипов | [video-clips skill reference](../.agents/skills/ytv-produce-video/references/video-clips.md) |
| Приёмы обложек, AI-черновики, карточка/начало/payoff и QA | [thumbnails](../docs/standards/thumbnails.md) |
| Структура thumbnail_plan, brief и exact reviewer result | [thumbnail contract](../docs/operations/thumbnail-contract.md) |
| План/наблюдение A/B, интерпретация метрик, следующий тест | [thumbnail experiments](../docs/operations/thumbnail-experiments.md) |
| Получение и разбор удержания Short, передача вывода следующему сценарию | [retention skill reference](../.agents/skills/ytv-operate/references/shorts-retention.md) |
| Metadata, полный YouTube release, календарь, provider A/B и read-back | [release](../docs/standards/release.md) |
| Artifacts/cache/retention/cleanup/TEXT_ONLY | [storage](../docs/standards/storage.md) |
| State/leases/revisions/approval authority | [architecture](../docs/architecture.md) |
| Session backend, capabilities и actual executor | [runtime](../docs/operations/runtime.md) |
| Общий межсессионный бюджет vidIQ | [vidIQ credits](../docs/operations/vidiq-credits.md) |
| Текстовый production-пакет сюжетного MR, identity/coverage и source import | [preproduction contract](../docs/operations/preproduction-contract.md) |
| Адаптивная image queue | [adaptive workers](../docs/architecture/adaptive-workers.md) |
| Переход старых работ и policy mapping | [migration](../docs/migration.md) |
| Ветка/MR/tests/evals | [development](../docs/development.md) |
| Channel style/identity/recipe | `channels/<id>/channel.json` + канальный PROFILE |
| Канальные документы в task, pinned snapshot, manifest worker | [task contract](../docs/operations/task-contract.md#требования-в-контексте), `src/ytvideos/context.py` и ChannelSpec |
| Выбор skill по task | [manifest](skill-catalog.json) и [каталог](skill-catalog.md) |

Skill и навык обозначают одно: исполняемую процедуру конкретного этапа с обязательными references. `AGENTS.md` выбирает вход и закрепляет общий запрет самовольных методов; skill определяет, что прочитать и как выполнить действие. Docs владеют lifecycle/полномочиями, требованиями к результату, схемами/синтаксисом и обоснованиями; профиль — параметрами и разрешёнными вариантами канала; code/schema — проверками и переходами. `plan` и `task_guide` представляют эти правила и сохранённое состояние, не создают новые полномочия.

Пошаговую инструкцию «прочитать → проверить → выполнить → сохранить → продолжить» держать в skill/reference, а при переносе удалять её вторую действующую копию из docs. Порог качества, формат поля и ограничение результата оставлять у standard/schema owner и ссылаться на него. Общий task-execution reference обязателен для всех skills и включён в pinned task packet; длинные канальные требования не копировать в каждый skill. Без описанного метода/параметра нельзя выводить правило из примера или соседнего канала.

Документ не превращает неподдержанную capability в действующий tool. Действующие инструкции описывают актуальное поведение. Архивные receipts/консультации и решения отдельного выпуска остаются evidence вне обычного production reading path; actual reference assets с provenance сохраняют своё художественное назначение.

Основания для thumbnail standard: [научные и платформенные источники](../docs/research/thumbnail-evidence.md), [опыт практика с таймкодами](../docs/research/thumbnail-practitioner-notes.md). Разборы практики помогают выбрать рабочий приём до накопления собственных результатов.

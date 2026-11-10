# Разработка и проверка

## Рабочий цикл

1. Прочитать root и canonical owner изменения. Проверить `git status`, текущий main и чужие изменения. Исправление ошибки начать с воспроизведения и причины.
2. Работать в одной feature branch с небольшими тематическими commits. Для общей архитектуры допустима `work/architecture/<scope>`. Этот рефакторинг собирается в один MR; этапы реализации могут идти отдельными заданиями/сессиями.
3. Детерминированные проверки и переходы реализовать кодом. Параметры канала держать в ChannelSpec; не добавлять hardcoded перечень имён в workflow.
4. Синхронно переписать действующую документацию и ссылки, удалив отменённый путь. Архивные факты и evidence не переписывать как правила.
5. Запустить адресные tests и обязательный общий gate. Прочитать diff. В MR описать проблему, изменение поведения, реальные проверки и оставшиеся runtime/migration ограничения.
6. Публиковать свою ветку и MR; merge выполняется после review. Не менять production infrastructure/каналы ради подтверждения unit tests.

## Локальный вход

```bash
uv sync
uv run python -m ytvideos --help
uv run python -m unittest discover -s tests -p 'test_*.py'
```

[Task contract](operations/task-contract.md) содержит копируемые команды и точную форму outputs/receipts. Справка CLI — источник точного синтаксиса. `create`, `status`, `next`, `context`, `complete`, `approve`, `resume`, `cancel`, `doctor` и `import-legacy` обслуживают сохранённое состояние. `approve --event FILE` принимает только envelope trusted host; не создавать production approvals вручную из слов модели.

SQLite использовать для изолированных tests/local runs. Для production PostgreSQL integration проверить транзакции/конкуренцию и actual driver; skipped database tests не считать PASS реального Postgres. Missing native fonts/provider credentials не подменять фиктивным live output.

## Что проверять

Обязательные регрессии: новый сюжет без bundle; generic profiles; ровно два бизнес-gates; packaging не ждёт MP4; stale artifact/approval/worker; unknown upload; повтор user event; lease conflict; частичная invalidation; scene-pool backpressure/fairness; cancel с in-flight operation; complete без обязательного evidence; wrong channel; schedule в прошлом; Shorts thumbnail до обработки.

Для сложных skills — свежая GPT-6 Luna с обычным заданием без ожидаемого маршрута в prompt. Проверять сохранённый output и реальные вызовы/trace, не только самоотчёт. Отдельная сценарная проба должна пройти исследование, самостоятельный выбор темы, полный текст и остановку на script gate. Не отправлять реальные публикации и не тратить production budget ради тестов MR.

Измерять active time отдельно от user waiting, tokens/tools/cost, retries, долю reuse/resume, реальные interventions и ошибки wrong-skill/wrong-channel/stale-input. Цели ускорения устанавливать после baseline; число сессий и размер prompt сами не доказывают выигрыш.

## Skills и документация

`.agent/skill-catalog.json` содержит canonical names/paths/stages/intents; Markdown-каталог — его читаемое представление. Skill описывает триггер, необходимые входы, короткую процедуру и результат. Содержание стандарта не копировать в каждый skill. Python helpers находятся в `automation/helpers/`, а не внутри инструкций.

Проверять frontmatter, соответствие stage mapping, относительные ссылки, отсутствие отменённых entrypoints и обязательные missing-input cases. Независимый reviewer получает артефакт/задачу без диагноза автора. Новая модельная сессия не должна зависеть от предыдущего рассказа координатора.

## Secrets и артефакты

Ключи/OAuth tokens/private approval key и media не входят в Git. Public verifier key передаётся конфигурацией host. Не печатать credentials при doctor/errors. Большие cache/output складывать в runtime workspace, не source checkout. Реальный файл, подвергнутый QA, связывать с хешем и provenance.

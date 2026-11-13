---
name: ytv-maintain
description: "Change ytvideos code, profiles, documentation or project skills with bounded scope, contract tests and migration safeguards. Use for repository maintenance and onboarding a verified channel."
---

# Изменить проект

1. Прочитать [development](../../../docs/development.md) и [владельца затронутого правила](../../../.agent/documentation-index.md). [Architecture](../../../docs/architecture.md) нужна при изменении runtime/state/границ компонентов. Определить дефект, минимальное изменение и критерий проверки. До исправления ошибки воспроизвести её.
2. Проверить branch/status и активные изменения. Править только свою область; не перезаписывать чужую работу. Новая архитектура не мигрирует текущие выпуски автоматически: [migration](../../../docs/migration.md).
3. Повторяемое решение поместить в одного владельца: code/schema для детерминированного поведения, channel profile для параметров, standard для требований, короткий skill для процедуры. Не расширять root длинными domain-checklists.
4. При смене процесса заменить отменённый маршрут во всех действующих docs/skills/examples. Фактические журналы и принятые художественные reference packs сохранить. При изменении skill синхронизировать frontmatter с `.agent/skill-catalog.json`; читаемое представление генерировать командой из development.
5. Проверить контракт/отказной случай, из-за которого менялся код, затем нужные regression checks. Сложный skill проверить в новой сессии Luna на обычном запросе без подсказки правильного маршрута; сохранить trace/output/evidence. Самоотчёта «прочитал skill» недостаточно.
6. Для нового канала создать проверенный ChannelSpec/профиль и recipe, не добавлять имя канала в workflow-ветвления. Замороженные и архивные identities не переопределять. Проверить doctor, voice/fonts/rights/calendar/provider доступ до производства.
7. Сохранить проверенные небольшие commits по [общему Git-порядку](../../../docs/development.md#git-и-совместная-работа): основа — main, для отдельной ветки сразу открыть PR в main. В PR указать проблему, поведение, выполненные проверки, migration и реальную оставшуюся границу исполнения. Не сообщать, что live pipeline проверен, по fake backend tests.

Репозиторные skills являются частью code/rules version и хранятся в Git проекта; это не установка персональных навыков приложения. В новую сессию передавать конкретную задачу и canonical packet, не весь предыдущий разговор.

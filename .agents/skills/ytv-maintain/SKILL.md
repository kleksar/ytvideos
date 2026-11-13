---
name: ytv-maintain
description: "Change ytvideos code, profiles, documentation or project skills with bounded scope, contract tests and migration safeguards. Use for repository maintenance and onboarding a verified channel."
---

# Изменить проект

Прочитать [процедуру исполнения](../ytv-start/references/task-execution.md) и границы production blocker. Прямое поручение изменить код/правила разрешает разработать недостающую процедуру в указанном scope; production worker не получает это право ради завершения своего task. Исправить владельца правила, связанные checks/ссылки и проверить изменение до использования. Для существующего pinned run применять migration, не подменять snapshot.

1. Прочитать [development](../../../docs/development.md) и [владельца затронутого правила](../../../.agent/documentation-index.md). [Architecture](../../../docs/architecture.md) нужна при изменении runtime/state/границ компонентов. Определить дефект, минимальное изменение и критерий проверки. До исправления ошибки воспроизвести её.
2. Проверить branch/status и активные изменения. Править только свою область; не перезаписывать чужую работу. Новая архитектура не мигрирует текущие выпуски автоматически: [migration](../../../docs/migration.md).
3. Повторяемое решение поместить в одного владельца: code/schema для детерминированного поведения, channel profile для параметров, standard для требований, skill и его обязательный reference для процедуры. Пошаговый алгоритм переносить из docs в skill без второй действующей копии; docs сохраняют lifecycle/invariants, схемы, синтаксис и обоснования. Общая процедура исполнения принадлежит reference выше и передаётся каждому task packet. Не расширять root длинными domain-checklists.
4. Переписать затронутые docs/skills/examples в актуальном состоянии и удалить отменённый маршрут. Историю изменения хранит Git; task-specific разрешения и очереди принадлежат run/evidence, а не общему профилю. Фактические журналы и принятые художественные reference packs сохранять вне обычного reading path. При изменении skill синхронизировать frontmatter с `.agent/skill-catalog.json`; читаемое представление генерировать командой из development.
5. Проверить контракт/отказной случай, из-за которого менялся код, затем нужные regression checks. Сложный skill проверить в новой сессии Luna на обычном запросе без подсказки правильного маршрута; сохранить trace/output/evidence. Самоотчёта «прочитал skill» недостаточно.
6. Для нового канала создать проверенный ChannelSpec/профиль и recipe, не добавлять имя канала в workflow-ветвления. Замороженные и архивные identities не переопределять. Проверить doctor, voice/fonts/rights/calendar/provider доступ до производства.
7. Сохранить проверенные небольшие commits по [общему Git-порядку](../../../docs/development.md#git-и-совместная-работа): основа — main, для отдельной ветки сразу открыть PR в main. В PR указать проблему, поведение, выполненные проверки, migration и реальную оставшуюся границу исполнения. Не сообщать, что live pipeline проверен, по fake backend tests.

Репозиторные skills являются частью code/rules version и хранятся в Git проекта; это не установка персональных навыков приложения. В новую сессию передавать конкретную задачу и canonical packet, не весь предыдущий разговор.

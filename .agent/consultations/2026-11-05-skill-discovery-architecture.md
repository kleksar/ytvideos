# Skill discovery architecture consultation

- Date: 2026-11-05. Chrome, [ChatGPT consultation](https://chatgpt.com/c/6aec9929-e290-83ed-b9ec-761d6cff2c36). Visible model GPT-6, reasoning Extra High.
- Task: `skill-discovery-architecture-20261105`. [Exact prompt](2026-11-05-skill-discovery-architecture-prompt.txt). Exact posted text and empty composer confirmed before controlled lock release. Completed answer read from the visible reply via Copy.
- Scope: advisory. No production routes modified in this pass.
- Coordinator decision: recommend a single entry for all storyboards, a separate history verification task, and retiring the Paper production entry after moving its unique channel references and updating callers. Migrate active references directly. Preserve historical records as evidence rather than creating a second discoverable route.

## Completed answer

Рекомендация: сократить discovery на два навыка — `ytv-paper-storyboard` и `ytv-paper-production`. `ytv-history-story` сохранить самостоятельным, но переименовать в `ytv-history-verification`.

Это убирает дублирующиеся точки входа, не теряя специализированные процедуры.

## 1. Решение по навыкам

| Навык                  | Решение                                               | Основание                                                                                                                                        |
| ---------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ytv-history-story`    | Сохранить, переименовать в `ytv-history-verification` | Самостоятельный запрос и результат: проверенные источники, хронология, противоречия, неопределённость. Не пишет историю и не создаёт storyboard. |
| `ytv-paper-storyboard` | Сделать reference внутри `ytv-video-production`       | Специфика бумажной постановки важна, но владельцем создания и приёмки storyboard уже является production coordinator.                            |
| `ytv-paper-production` | Убрать из discovery после миграции маршрутов          | Это wrapper без собственного производственного результата: фильмы делегирует production, карусели — posts playbook.                              |

Важно: превращение Paper Storyboard в reference не означает удаление его содержания. Сохраняются правила постановки, бумажных объектов, интегрированной типографики и визуального языка.

## 2. Минимальная discovery-поверхность

`ytv-topic-research`

Выбор и оценка тем

`ytv-history-verification`

Проверенная фактическая основа

`ytv-storycraft`

Написание и редактура сценария

`ytv-video-production`

Координация после готового сценария, storyboard, монтаж, MP4 и разрешённый release

References:

`visual-storyboarding.md` — общие правила

`paper-storyboarding.md` — бумажная постановка

`ytv-scene-images`

Генерация, проверка и правка PNG

Это пять основных selectable skills. Схема показывает функциональные связи, а не обязательную последовательность вызовов: каждый владелец принимает самостоятельные задачи.

Самостоятельные карусели должны иметь прямой маршрут к существующему posts playbook. Если сейчас единственная discoverable точка входа для них — wrapper, удалять его до появления отдельного маршрута нельзя.

## 3. Три примера маршрутизации

| Запрос                                                                                        | Единственный основной владелец                              |
| --------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| «Проверь источники, даты и спорные версии по исторической теме. Сценарий не пиши».            | `ytv-history-verification`                                  |
| «Сделай только Paper Detour storyboard по утверждённому сценарию, без генерации изображений». | `ytv-video-production`, storyboard-only, с двумя references |
| «Исправь композицию и надписи в уже созданном PNG».                                           | `ytv-scene-images`                                          |

Ошибка Nuviko устраняется именно разделением фактического исследования и производственной раскадровки, а не удалением History Story.

## 4. Порядок миграции

1. Зафиксировать таблицу маршрутов и инвентаризировать callers: skill metadata, role configs, docs, flow YAML/JSON, stage dependencies. Добавить проверку, что Nuviko storyboard принадлежит `ytv-video-production`, а не History.
2. Переименовать History Story без поломки ссылок: обновить callers на `ytv-history-verification`; прежнее имя временно поддерживать как недоступный для discovery alias. В description явно исключить написание сценариев и storyboard.
3. Перенести Paper Storyboard в reference production. Сохранить весь содержательный playbook. Paper storyboard stage должен вызывать coordinator, который использует общий storyboard reference и Paper-specific reference. Убрать второй selectable entrypoint только после обновления ссылок.
4. Развязать wrapper: Paper film → `ytv-video-production`; standalone carousel → posts playbook. После проверки всех потребителей исключить wrapper из discovery и убрать устаревшие ссылки.
5. Прогнать routing regression tests на трёх примерах выше, отдельно проверить Paper/Nuviko flow и отсутствие dangling skill references.

## 5. Границы ответственности

`ytv-video-production` остаётся единственным координатором storyboard и последующего производства, но запрос только на storyboard не разрешает автоматически переходить к PNG, MP4 или публикации. Существующие permission gates для производственных действий сохраняются, release — только при явной авторизации.

`ytv-scene-images` отвечает за файлы изображений, не принимает storyboard как финальный результат фильма. `ytv-history-verification` не получает права менять утверждённый сценарий или производственную последовательность.

Итог: целевое состояние — пять основных discoverable skills плюс самостоятельный posts route при необходимости. Два redundant entrypoints исключаются, специализированные знания остаются, а существующие callers мигрируют до удаления старых имён.

---
name: ytv-resolve
description: "Assemble, mix, subtitle, animate, render and hand off future ytvideos episodes in DaVinci Resolve across channels; preserve editable sources and verify the exact export and authorized YouTube delivery."
---

# DaVinci Resolve — общий монтажный маршрут

Для **всех новых каналов и будущих видео** Resolve — приложение по умолчанию для сборки, звука, экранных субтитров, монтажного движения, рендера и delivery. Это общий способ работы, не новый художественный профиль и не миграция готовых выпусков. Сценарий, ImageGen, ElevenLabs и подготовка исходников остаются у своих providers. FFmpeg/ffprobe допустимы для подготовки carrier media и независимой проверки, не как молчаливая замена Resolve-монтажа.

Выполнить [task execution](../ytv-start/references/task-execution.md). Сохранить exact approved inputs, channel identity/voice/typography/pixel policy и existing run pins. Конфликт нового app default с закреплённым старым renderer решать по [migration](../../../docs/migration.md), не переписывать старый рецепт. Skill не устанавливает Resolve, не добавляет backend в `execute-media` и не доказывает доступность приложения: если нет пригодного native host route, назвать конкретный blocker, продолжать независимую подготовку.

- Для создания/переработки раскадровки, включая исправления по меткам Resolve, выполнить [storyboard-процедуру с назначением Astra](../ytv-produce-video/references/storyboard.md). Монтажник реализует проверенное решение, не заменяет этого исполнителя.

- Для монтажа/audio/subtitles/render читать [timeline](references/timeline.md). Сборка должна остаться редактируемой, не превращать всё в один готовый MP4.
- Когда у речевых клипов разные пустые края или паузы, выполнить [нормализацию пауз по слышимой речи](references/voice-spacing.md). Обрабатывать исходные фразы раздельно, не ускорять голоса.
- Для export/upload/configure/read-back читать [delivery](references/delivery.md). Поручение собрать проект без рендера не разрешает render queue, upload или замену уже опубликованного видео.
- Для порученного обучения и нового native метода читать [private lab](references/lab.md); отделять live proof от reference-only упражнения.
- Перед выбором метода сверить [проверенные возможности и границы](references/evidence.md). Не выдавать видимое UI-поле за успешную интеграцию/API или готовую публикацию.

Разрешённые действия с одним Resolve instance выполнять **последовательно**. Независимую подготовку изображений, речи, SFX, metadata и QA можно распараллеливать. Не захватывать мышь/клавиатуру и не переключать пользовательский текущий проект ради фоновой работы; если native route требует конфликтующего переключения, остановить именно мутацию и согласовать безопасное окно. Не закрывать чужие проекты/задачи.

На Mac использовать существующий `/Users/diplomat/ytvideos`, материалы выпуска внутри `channels/<id>/videos/<episode>/Work/`. Не создавать соседние clones/worktrees/каталоги проекта. В иных средах использовать их фактический repo root; Mac-путь не переносить буквально. Сохранять проект/export manifest, пути/hash исходников и QA рядом с выпуском, тяжёлые media и credentials не коммитить.

## Future-video native editability (owner clarification, 2026-11-19)

For ALL future videos and channels, keep creative editing native and editable in Resolve: source gameplay/facecam crops and transforms, still/meme graphics, text/captions, speech, music and SFX as separate appropriate clips/tracks/nodes. Discovery tools supply source windows, timing and editable handoffs. FFmpeg may prepare/conform/validate technical inputs, but must not silently bake framing, captions or the finished creative edit as a substitute for native assembly. Existing baked carriers are a migration gap, not proof of native editability; preserve accepted outputs and pins and migrate only within authorized scope. This requirement does not change artistic profiles, approval gates or upload visibility.

## Control route preference

Prefer an available, verified MCP capability for the requested operation; otherwise use the officially supported Resolve scripting/API route. A preference does not establish that an MCP server, method or permission exists: inspect actual tools and documented API support, and preserve honest capability blockers. Use desktop UI only for gaps, visual QA or the requested native YouTube preset when needed and available. Coordinate foreground interaction with the owner and other workers; keep the existing single-instance serialization and prior-project preservation requirements. Do not simulate unsupported scripting operations or silently take over the active desktop.

# Независимый review MR: Shorts retention, MP4 opening/tempo, Short → Short

**Существенных подтверждённых дефектов, требующих исправления до merge, не найдено.** Вывод относится к прочитанному diff и выполненным offline checks. Он не подтверждает работу с реальным YouTube Studio, просмотр MP4 или улучшение audience retention.

## Область проверки

- Baseline: `f8e9c582fa2e7f2b94473c884e77e0d31d6946d7`, исходники из `/workspace/scratch/98a321085278/mr-source/baseline`.
- Candidate: `/workspace/scratch/98a321085278/mr-source/work`; проверены все 13 путей из `changed-paths.json`.
- Прочитаны `AGENTS.md`, `ytv-maintain`, обязательная `task-execution`, `docs/development.md`, владельцы затронутых правил и связанные контракты.
- Отдельная узкая проверка охватила `cross_promotion.py`, `ReleaseSpec`, CLI и связанные release consumers.
- Candidate не изменялся. Live каналы, платные providers, публикации и Studio mutations не использовались. Публичная справка YouTube прочитана без доступа к аккаунтам.

## Findings

Список существенных findings пуст. Основания вывода:

1. `.agents/skills/ytv-operate/references/shorts-retention.md:7` — анализ начинается с точного channel/video identity и версии. Процедура сохраняет фильтры, временные окна, определения метрик и отсутствующие значения; запрещает восстанавливать кривую из APV или просмотров. Отсутствие отчёта и отсутствие точного MP4 имеют раздельные, ограниченные последствия: доступная часть остаётся выполнимой, содержание участка и причина ухода не выдумываются.
2. `.agents/skills/ytv-operate/references/shorts-retention.md:14` — наблюдение, гипотеза и будущий опыт разделены. Нет универсального порога удержания, автоматического winner или причинного вывода по одиночной метрике. `.agents/skills/ytv-operate/references/shorts-retention.md:24` использует существующий `attach-artifact`; текст прямо предупреждает, что прикрепление не валидирует смысл и не включает заметку автоматически в task inputs. Явная передача по ID/path согласуется с `docs/operations/task-contract.md:204` и новым чтением наблюдений в `.agents/skills/ytv-write-script/SKILL.md:18`.
3. `docs/standards/delivery.md:50` — mute-проверка касается читаемости изображения/ситуации; для `music_first` задано применимое исключение без требования диктора. `docs/standards/delivery.md:52` связывает замечание к темпу с фактическим playback и интервалом, разрешает отсутствие найденного дефекта, отделяет мнение reviewer от audience retention и сохраняет `UNVERIFIED` при отсутствии просмотра. Новое требование не разрешает менять принятый текст или автоматически ускорять звук.
4. `src/ytvideos/cross_promotion.py:108` — подтверждённая цель `short` получает `shorts_to_short` с `{short_id, target_short_id}`; для `long` сохранены `shorts_to_long`, `{short_id, long_id}` и `ytv-cross-promotion-plan-v1`. Проверки same-channel, Public/Unlisted, source Public/format, отсутствующей цели и самоссылки сохранены. Неизвестный или неподдерживаемый формат блокируется. Вызов проверки End Screen сохранил прежнюю семантику.
5. `src/ytvideos/cli.py:293` — planner остаётся read-only и не создаёт state DB. `docs/operations/cross-promotion.md:20` явно требует поддержки нового action host-адаптером, запрещает fallback к long и не выдаёт план за исполненную операцию. Новый dispatcher этим изменением не заявлен.

## Выполненные offline checks

Из candidate выполнены:

```bash
PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 python -m unittest test_context test_instruction_packet test_repository_check
# Ran 48 tests — OK
```

В независимой узкой проверке того же candidate выполнены:

```bash
PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 python -m unittest test_cross_promotion
# Ran 12 tests — OK

PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 python -m unittest test_release
# Ran 18 tests — OK
```

Итого: **78 tests OK**. Это адресные существующие unit checks, не полный CI и не production integration.

## Проверка публичных оснований

13.11.2026 прочитаны первичные документы:

- [YouTube Help: content performance](https://support.google.com/youtube/answer/12220281?hl=en) — определения engaged views, stayed to watch, AVD/APV согласуются с новым reference.
- [YouTube Help: audience retention](https://support.google.com/youtube/answer/9314415?hl=en) — путь к отчёту на уровне видео, типичная задержка 1–2 дня и неоднозначность пиков согласуются с процедурой. Срок не превращён в обязательную гарантию доступности.
- [YouTube Help: Related video](https://support.google.com/youtube/answer/14075157?hl=en) — возможность связать Short с другим Short своего канала при Public/Unlisted и advanced feature access подтверждена. Helper явно оставляет Live за пределами своего поддерживаемого scope.

## Ограничения review

- Исходники представлены source-only snapshot, а не полным git checkout. Remote HEAD, актуальность ветки, staged state, push и CI этим review не проверены.
- Не проводилась свежая поведенческая проба production worker на реальном отчёте/MP4. Процедурные требования прочитаны и сопоставлены с контрактами; их соблюдение конкретной моделью не доказано unit tests.
- Не проверялись доступ к аналитике конкретного аккаунта, сохранение Related video в Studio, advanced features и исполнение нового action конкретным host.
- Не оценивалась фактическая история зрителей или рост retention. Получение таких доказательств остаётся отдельной авторизованной работой.

## SHA-256 проверенного candidate

```text
d055fe3cd685b46bd7e91f4bc84a78de6e9bfee87ecbc2e5679edfbb0eaa8086  .agent/documentation-index.md
c9dc6dd58a45dcd1fb232e5cdf0fb9b78ae3c50525f3a07e401009e9d3560653  .agent/skill-catalog.json
cca3044269514b07a617487dbdfed64983433caa72f17360305c16e61ef97918  .agent/skill-catalog.md
6c5306cde2882003ba6f86a4348927c44a75894b67af1f6bc1ed90d214d29abc  .agents/skills/ytv-operate/SKILL.md
c9ded405edc03785a002b11b1027bc9709b0e6599e790cdd600008bb041306a8  .agents/skills/ytv-operate/references/shorts-retention.md
1a3e5bcefc7e7df36e1d0a932c589e8865479f498345294417b23545b08177ad  .agents/skills/ytv-review-video/SKILL.md
2eb22f1f6d4eb3636198f84ef7a3e36d5d071ee5f922607224f4cb2629072ca6  .agents/skills/ytv-write-script/SKILL.md
b2febe0aa32b8ebeebf0a9d4dcc994a452c04e629e294014c1d64ffd542cceba  AGENTS.md
b98f95bc914706ec6eb76d002e536bda83610a4f40a5ce1b81f9cbd1dc67b782  docs/operations/cross-promotion.md
c5ffb5eaf948edef459a263f069c98994cfd4c3982ca692476efdf17fbde4a46  docs/standards/delivery.md
eb34b70eda4ac14644de2170dd553cf2dc59c693cec7fade9bef09bd90bf5fe5  docs/standards/release.md
e2e5416f95dae3817d0daa0f41fb7edc4e2bfeb7560fe01e58249469874fbfe7  src/ytvideos/cross_promotion.py
30f12d35afc310b47244356fbc6e340bfc6bc1d553721f9ffaa9eccd19a45858  tests/test_cross_promotion.py
```

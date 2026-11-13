# Дополнение к независимому review: instructions-only retention route

**Существенных подтверждённых дефектов в routing fix не найдено.** Это адресный review реализации, документации и offline-проверок. Он не подтверждает успешное поведение production worker; повторная fresh Luna-проба в этот review не входит.

## Область

Проверены изменения относительно baseline `f8e9c582fa2e7f2b94473c884e77e0d31d6946d7` в `/workspace/scratch/98a321085278/mr-source/work`:

- `src/ytvideos/context.py`;
- `src/ytvideos/cli.py`;
- `scripts/check_repository.py`;
- `tests/test_instruction_packet.py`;
- `AGENTS.md`;
- `.agents/skills/ytv-operate/SKILL.md`;
- `.agents/skills/ytv-start/references/task-execution.md`;
- `docs/operations/task-contract.md`.

Прочитаны также уже рассмотренный retention reference и действующие контракты. Первый отчёт `reviewer-result.md` сохранён без изменений; настоящий addendum относится к перечисленным новым правкам. Candidate не изменялся. Временные fixtures создавались вне candidate и удалены. Live/providers не использовались.

## Findings и основания

Список существенных findings пуст.

1. **Production маршруты сохранены.** `src/ytvideos/context.py:43` объявляет отдельный `INSTRUCTION_OPERATIONS`; `STAGE_REFERENCES`, создание snapshot и whitelist production stages в `_entries()` не расширены. `retention` не создаёт production task или новый маршрут pinned snapshot. Для существующих stages прежняя выборка skill сохраняется в `src/ytvideos/context.py:204`.
2. **Выбран полный специальный packet.** `src/ytvideos/context.py:186` проверяет допустимый формат; `retention + long` отклоняется. Выбор `ytv-operate` требует ровно одного совпадения. References проходят прежние path/current-text/blank проверки, включают общую процедуру, настоящий профиль, editorial и retention reference; возвращаются exact text/SHA-256 и `read_next` (`src/ytvideos/context.py:209`).
3. **Семантика channel references подтверждена исполнением.** `task_references()` сохраняет AND-фильтры. В retention включаются declarations без `stages`, если подходят остальные фильтры. Declarations с `research` либо полным набором production stages исключаются; `formats: [long]` и `purposes: [scene]` также исключаются. Отсутствующие файлы этих неприменимых scopes не блокируют packet. Совпавшие повторные пути дедуплицируются.
4. **Команда не создаёт состояние.** `src/ytvideos/cli.py:29` добавляет choice, не меняя раннюю instructions-ветку `main()`. Самостоятельно проверены успешный retention CLI и отказ для long с mock-запретом на создание `Store` и `Production`: оба пути обходят эти классы, не создают БД/workspace.
5. **Документация согласована.** `AGENTS.md:19`, `.agents/skills/ytv-operate/SKILL.md:12`, `.agents/skills/ytv-start/references/task-execution.md:7` и `docs/operations/task-contract.md:88` задают один instructions-only вход. Контракт прямо отделяет retention от production stage/snapshot и объясняет обработку references без stage-фильтра. Разбор предоставленных материалов не требует нового run/claim/provider; операции с существующим run по-прежнему сохраняют pins.
6. **Новый reference учитывается offline checker.** `scripts/check_repository.py:110` добавляет instruction-operation references к current runtime documents. Новый процедурный файл не выпадает из проверки актуальности из-за отсутствия в production stages.

## Выполненные проверки

Самостоятельно выполнено:

```bash
PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 python -m unittest test_instruction_packet test_context test_repository_check test_cross_promotion
# Ran 63 tests — OK
```

Дополнительно выполнены адресные проверки на временном fixture, без добавления тестов в candidate:

| Проверка | Результат |
|---|---|
| Registered frozen channel с unscoped и short-only references | Обе declarations включены, channel/status/config сохранены |
| Research-only и all-production references с отсутствующими файлами | Исключены; успешный retention packet |
| Long-only и scene-purpose references с отсутствующими файлами | Исключены; успешный retention packet |
| Повторный применимый путь | Включён один раз |
| Полнота manifest и соответствие bytes/hash | Совпадают со всеми выбранными файлами |
| CLI retention/short с запрещёнными Store и Production | Exit 0, состояние не создано |
| CLI retention/long с запрещёнными Store и Production | Exit 2, состояние не создано |

Узкий независимый reviewer дополнительно прочитал согласованность AGENTS/skills/task-contract/context; существенных findings не сообщил. Его проверка была статической, без повторного запуска tests.

## Ограничения

По сообщению координатора первая поведенческая проба не прочитала нужную процедуру. Этот review проверяет добавленный маршрут и его границы, но не объявляет этот поведенческий риск устранённым: для этого требуется результат повторной свежей пробы с проверяемым read/call evidence. Само наличие полного packet не доказывает, что worker прочитал и выполнил его.

Не проверялись live Studio, фактические retention reports, playback MP4, remote state и полный CI. Прямой repository gate в этом повторном review не запускался; выполнены его существующие unit tests. Source-only ограничения первого отчёта сохраняются.

## SHA-256 проверенных файлов

```text
ace98d94fe39113a56b24ba2f964ccee8cfd46f84a8f10ee81070f0c31c3e864  src/ytvideos/context.py
10474b25019250fa302c3db4fe94934b35408519e4a33b075acd1272b2de73b0  src/ytvideos/cli.py
8f70a71d00772245dae9e5cc6cbc416435f544ca9154a341b1e17ac299db799f  scripts/check_repository.py
dc40b6dfb53b739c3fd15680483c67eddc98069dbc799b42e34ad22831979971  tests/test_instruction_packet.py
7b35fe05658264275c86977ff8fba354e2d333316f5b283fca74a1a336647d69  AGENTS.md
a6566121d28b821b477ec10ac76b43455c71d0681461226e94e27038b9625a36  .agents/skills/ytv-operate/SKILL.md
0bd8b658ea0a001c77ba55c692bc9faebf32afa4f606a8f5a24f02b74d32410d  .agents/skills/ytv-start/references/task-execution.md
4be13baa05361244443095cbaa49e45a23c10390225c053c851526aeb357b2f0  docs/operations/task-contract.md
```

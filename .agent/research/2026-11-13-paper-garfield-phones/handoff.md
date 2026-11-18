## 2026-11-18 updated handoff: three variants
**EDITORIAL_CANDIDATE_UNREGISTERED**; no local ytv checkout, no actual run, no independent session/receipt, no exact owner approval. The previous handoff is kept below as historical evidence.

- 02m: [EN](variants/02m/script.en.txt) SHA-256 03619fac6e367a984fa63ed41c95389fbe4fd46a5f21b7e62144989dc232e504; [RU](variants/02m/script.ru.txt) SHA-256 4ef991280facce9041e2954d8bf04a12b6ba80f20b30b2c60bcc9e35c0e05296.
- 05m: [EN](variants/05m/script.en.txt) SHA-256 ecb542776693eb0464b2b708d1bae25285b50ae647ffe28a40f53149011f5230; [RU](variants/05m/script.ru.txt) SHA-256 130bb6334c8804eea62f5ce3c9b7871d848ce3fcdeaaf67b7b395519c05e602d.
- 10m: [EN](variants/10m/script.en.txt) SHA-256 d63490b478db0dd7669fc7e45e3c5ee252e94ddcb41ac9efc12c230553b01e0c; [RU](variants/10m/script.ru.txt) SHA-256 f7e38a25e845cc4c431725f36079434a516dde451345d2ccdb575cbbf1faaebc.

Recommended editorial 05m Long, NOT approved master. All three scripts are new proposals; unchanged root source and original 14-scene storyboard are archive. Both Short and Long formats exist in current Paper ChannelSpec, but stage completion/production not claimed.

Next local transfer: owner selects exact EN version; register a genuine `uv run ytv start --channel paper_detour --format long|short --intent 'Garfield phones selected exact variant from PR #30'`, read real pinned `plan_summary`/`read_next`, attach variant scripts and story-review by official CLI, obtain independent first-listener and applicable bilingual/Short-loop assessment, then actual script approval. No fabricated run IDs/receipts, old pins unchanged. Never interpret PR review as production order.

---
## Original handoff (2026-11-13) preserved

EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate

# Handoff — Paper Detour editorial hypothesis, NOT registered run
- Канал: `paper_detour` (проверено по `channels/paper_detour/channel.json`, status `active`), format `short`, language narration English, русский только полный перевод для владельца.
- Папка источника: `.agent/research/2026-11-13-paper-garfield-phones/`. Entry: `.agent/research/2026-11-13-paper-garfield-phones/README.md`; полный EN `.agent/research/2026-11-13-paper-garfield-phones/script.en.txt`; полный RU `.agent/research/2026-11-13-paper-garfield-phones/script.ru.txt`; `research.md`, `story-review.md`, `storyboard.md`, `packaging-brief.md`. Текущий текст EN и RU — v1, только editorial hypothesis.
- Установленный remote main на момент кандидата: `96c8fa1573c02e8e7987e272a569bf34f037691e`; HEAD целевой ветки / PR — смотреть удалённый GitHub после получения, не подменять SHA base.
- Нет настоящих `run_id`, `task_id`, `input_hash`, `research/script task receipts`, `ytv-script-review-v1` или independent reviewer. Не генерировать произвольные ID. Нет `awaiting_script_approval`. В этом host нет checkout с `pyproject.toml` для `uv run ytv start`; `sessions.independent` не представлен среди доступных tools.
- Исследовательская provenance: документы через GitHub remote main, внешние report/court sources с URL и датами в `research.md`. Дата редакционной версии: 2026-11-13. Получить actual media reference bytes/хеши отдельно.

## Точный переносимый вход локальному агенту (не выполнить без explicit owner production approval)
1. В свежем клоне `main` изучить текущие `AGENTS.md`, `docs/workflow.md`, task contract, workflow и актуальный канал; забрать текстовую папку из Draft PR как **редакционную гипотезу**, не как готовый run или accepted source script.
2. Создать **новый** официальный run командой: `uv run ytv start --channel paper_detour --format short --intent 'Проверить и зарегистрировать редакционную гипотезу о телефонах Garfield на побережье Бретани; текстовый источник .agent/research/2026-11-13-paper-garfield-phones; без production до одобрения владельца'`. Прочитать реальный `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`; не придумывать `read_next` по этому Markdown.
3. В точные research/script tasks перенести проверенные источники и полный EN narration, сверить против актуальных требований; сохранить настоящие receipts, hashes, входы и исходные пути через CLI. Само наличие EN не означает owner approval.
4. В fresh host independent session вызвать оригинальный `ytv-script-review-v1` с **хешем exact EN** и буквальным двойным полным прочтением Short + end→start, получить подлинный review и reviewer receipt. Сначала передать начало/полный текст/стык без beat map; источники и сильнейшую альтернативу — лишь после первого чтения. Если review `FAIL`, вернуться к отбору или исправить точечно.
5. Только после действительного завершения script task и независимого review подвести run к `awaiting_script_approval` и получить **новое явное решение владельца для точной версии**; PR/merge/автоматизация не разрешают production. До этого TTS/image/render/upload запрещены. После разрешения проверять media refs, первичный physical paper style, actual audio timing, whole-frame loop и subtitles по штатному workflow.
6. `python scripts/check_repository.py` и адресный `tests/test_context.py` плюс CI запустить в реальном checkout; в этой connector-only среде не выполнялись.

Никакие общие docs/skills или `channel.json` не изменены. Не делайте самостоятельную публикацию, merge или approve от имени владельца.

EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Atari E.T. landfill, Paper Detour

**Source:** актуальный проверенный remote `main` SHA `131ef24068d75967b1e43aa88e5f1370f6775054`. `#124` **merged** на момент чтения; действующие canonical `docs/standards/editorial.md` blob SHA `cd8ed20c697af001df887853772971a81176b7e1`, writer skill `fb45362fbc2ac5d0ae9d5178c2c98536637061df`. Историческая proposed policy `7d6bdf7702a2a241a33a21677fce29f26ada9b72` не является отдельной текущей pin. Записи о source и hashes не заменяют pinned reference_documents конкретного будущего run.

**Git branch:** `work/story-drafts/paper-atari-et-landfill-20261122`, основана прямо на source main. Все изменения ограничены `.agent/research/2026-11-22-paper-atari-et-landfill/`. PR должен быть Draft в main; не merge и не переводить существующие runs на новую политику. Не открывать очередной PR на эту же историю.

## Готовые редакционные входы

- Один фактический research: `research.md`; проверенные источники / сигналы / альтернативы, все сомнения сохранены.
- Шесть полных рассказов в `variants/{02m,05m,10m}/script.{en,ru}.txt`, hashes в `story-review.md`.
- `05m` предложена как Long master; точный EN SHA-256 `28b7da58638846e1603f59a34d9bf4ad430fc4f2a720de00e44595965a1c7225`.
- `story-review.md` содержит только self-review. Не существует reviewer-authored schema result, claims о подготовленном source не означают approvals.
- `packaging-brief.md`: честные title/thumbnail/first-proof/payoff; **не** содержит готовых картинок, bytes, SRT/AV timings или scene prompts.

## Конкретные blockers

1. **Official runtime:** `uv run ytv start --channel paper_detour --format short --intent ...` был реально попытан в доступном окружении и не запустился: `Failed to spawn: ytv ... No such file or directory (os error 2)`. Нет локального repo/runtime workspace, `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, run ID, lease, receipt, result или script approval. Git-only исключение прямо разрешено владельцем исключительно для редакционного пакета.
2. **Independent reviewer:** недоступна отдельная новая сессия с правом самостоятельного оригинального `ytv-script-review-v1` результата на точных bytes; отмечено `UNVERIFIED`. Первый reader должен увидеть только текст каждой версии (без этих оценок), за ним — sources и альтернативы; для 02m полный рассказ дважды + literal spoken seam и RU equivalence. При существенном замечании исправить текст и провести новый review на **новом hash**, не придумывать ответ самому.
3. **Production approval/format:** выбранный 05m текст — Long предложение, не выбран владельцем. Перед официальным стартом проверить ChannelSpec, текущие capabilities и pins. Не делать исходный Short run местом подмены Long master; при необходимости нужен разрешённый Long route и применимая миграция.
4. **Evidence:** свежий сопоставимый спрос на YouTube, baseline авторов, YouTube comments, analytics Paper, хронометраж Lawrence 1.10x, actual rights на footage/game art, relevant Public next-video intro, actual storyboard references, AV seam **UNVERIFIED**.
5. **Media:** ничего не отправлялось внешним API. Нет TTS, imagegen, mp4, Flow, upload, publishing; любое внешнее видео требует своего согласования по workflow. Не делать preproduction.json из неподтверждённых references/hash.

## Путь переноса на рабочем локальном host

После явного выбора владельцем конкретного варианта и совместимого format:

```bash
# Команда пример-процедура. Выполнять на host с repo, uv, runtime и корректным общим workspace.
uv run ytv start --channel paper_detour --format long \
  --intent 'owner chose Atari E.T. landfill 05m source' \
  --source-script .agent/research/2026-11-22-paper-atari-et-landfill/variants/05m/script.en.txt
uv run ytv plan --run ACTUAL_RUN_ID
```

Для ещё не принятого нового текста сначала выполнить обычный pinned research / reviewer / script gate; **не** применять `source_script` import без реального владельческого поручения на exact source (он предназначен для уже принятого неизменённого сценария). Проверить `plan_summary`, `read_next`, `task_guide`, pinned docs и actual ChannelSpec. Точные SHA/runs/approval взять только из runtime. Ветка редакционной очереди не должна менять `main`, schedule или production state.

Дальнейшее: fresh independent reviewer → факты / слова / петля (если выбран 02m Short) → корректный runtime Long → единственный exact script gate → только по принятому тексту подробный storyboard/scene prompts с variant/hash → исходные Paper reference bytes и rights → audio/meters → approved MP4. Это не поручение выполнять последующие этапы сейчас.

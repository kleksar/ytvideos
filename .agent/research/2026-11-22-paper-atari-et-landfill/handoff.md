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


## 10m r2 — редакционная запись (2026-11-22)

Baseline PR HEAD `aa3603609f727341234ffcacbff19e6c0c0f0edb`; исходные 10m blobs EN `3ac01abffb5a0f5bad84bc096aa2d283227d0319`, RU `5cb08a0af6c46843a4bf0b2d8d3d4722007b5257`. Новый 10m SHA-256 EN `fdefa420b2205420bc50b3261346ef6d13baa0e8449c5e10796d1e968f6c795c` / RU `47829261ec1808482eb82ebaa0bf922445ac84b047b5e0a8fb2ea7ff6485a128`. Был повторный объяснительный хвост после находки успешных игр; теперь ведёт цепь ограниченный поиск → E.T. → другие хиты → конкретное объяснение логистики Хеллером → документированная музейная атрибуция по Робарджу. Источники S1/S3/S4/S6, неопределённость высшего заказчика сохранена. 02m/05m unchanged и 05m recommended, не approval. Новая 10m r2 нуждается в independent reviewer и в новой раскадровке после выбора exact hash. Runtime / TTS / AV / upload не выполнялись.


## 02m r3 — новая короткая редакция (2026-11-22)

Baseline `cfacdcb0f3b2b4449dd531c65907d7eaa9202dad`, прежние Git blobs EN `595ef99250aa32f243f5481ff402f9fd493fc09e`, RU `ec6afef35945c55359aa255476a48f1471137419`. New SHA-256 EN `7a6ec816c5b3f74dbb42cdd1e3ac6f7546d8fea14fe37c43d4ba54f0ee043103`, RU `ba9b6b4c524ffce666b7f789872b87a6b5de0e7e16ee57d271cd8f07031ef434`. Газетный вывоз → склад → открытие E.T. → Centipede/Missile Command → музей. Источники S1/S3/S6/S7 уже в research; 05m/10m без изменений, рекомендация 05m. EN/RU loop дважды автором по тексту; независимый reviewer и реальный AV UNVERIFIED. Пункты о runtime/pins/owner approval выше актуальны.

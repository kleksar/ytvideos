EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Tunnel 57 — exact local handoff

**Channel:** `nuviko_history` (active according to main ChannelSpec, NOT music channel `nuviko_videos`). **Format:** English illustrated Long 16:9, 2560×1440/30 fps, Nuviko photoreal historical reconstruction; RU is reading translation, not voice. **Current status:** text-only authorial editorial candidate; no official run, no production-ready state, no actual approval.

**Verified base main (2026-11-15):** `5d3222c8888c775d2195c8b2949949f2d992e98d`, root Git tree `e92a9c5b9ee656aa1448f34264b217ca1d0cbe98`. A new branch from this base must be rechecked before push and PR publication. Source research uses recorded URLs and limitations in `research.md`.

## Content, identity and provisional outputs

- `script.en.txt` EN Git blob SHA: `537ab0539c1e6048fa28486d32f1f8c8f8e588ef` (552 words, 42 paragraphs). English is future TTS/SRT candidate only.
- `script.ru.txt` RU Git blob SHA: `50471b35bf32a42df2469d1bc931c0414c32bb24` (42 equivalent paragraphs).
- `story-review.md` Git blob SHA: `9385bc3a1a0ad95687011e5cf07b46088dc339b8`. Eight authorial criteria; no independent reviewer.
- `storyboard.md` Git blob SHA: `d268727748c4c85d7cfe4fa9e27b930f0376cb1c`. Forty-two provisional exact EN/RU spans. 4–6-sec holds are creative estimates, not measured TTS timecodes. End screen concept needs actual generation and QA later.
- `research.md` Git blob SHA: `521eb3f4af3858684b749c2faa6de1251de9bce1`. Historical claim ledger + selection + cautious YouTube sampling, no confirmed same-author baseline.
- `packaging-brief.md` has three different title/thumbnail hypotheses, none generated.

## Runtime blocker observed

Real terminal attempt in this host: `uv run ytv start --channel nuviko_history --format short --intent 'Исследовать сильный исторический сюжет для Nuviko History; сценарий без производства'` ended `Failed to spawn: ytv (No such file or directory)` (exit 2). That was only a capability check; it did **not** create a run, and no Long start was attempted. No pinned `plan_summary`, `read_next`, `task_guide`, `reference_documents` or task/claim/lease receipt exists. Project checkout or executable ytv CLI is missing in this host. Tool discovery also found no actual `sessions.independent` / fresh spawn_agent reviewer capability; changing author role is not independent review.

## Transfer in an authorized local checkout

1. Do not treat this PR as a production run. First inspect existing runs, current branch, canonical docs and ChannelSpec; do not register a duplicate if this exact story was imported elsewhere.
2. In the **authorized local checkout containing the real runtime and persistent store**, use `uv run ytv start --channel nuviko_history --format long --intent 'Проверить редакционную заготовку Tunnel 57, 1964, по сохранённым research и exact EN/RU script; довести только до script gate'`. Capture actual run ID, `plan_summary`, `read_next`, `task_guide`, pinned skills and all referenced documents. If CLI/provider missing, stop dependent step, not silently replace it.
3. Treat the two scripts and research as **unapproved imported candidate inputs**. Check facts and EN↔RU against exact bytes and historical sources, calculate actual SHA-256 in local runtime, record current provisional storyboard as a non-production coverage suggestion. Do not claim the above Git SHA-1 equals SHA-256.
4. Obtain a genuinely fresh independent first-listener and bilingual reviewer via available host. Show cold open, then exact full EN text without author score, then the full narration again (Long loop not mandatory). Provide sources and strongest Thai cave alternative **after** blind first reading. Require original `ytv-script-review-v1`, exact EN SHA-256 and observed findings. If the story is rejected/revised, update both scripts, dependent spans, hashes and review.
5. Only then present **entire** exact EN+RU for the owner's **explicit script approval**; await real `awaiting_script_approval` state, do not create fake approval IDs. This recurring Draft PR task grants **no** permission to make images, TTS, media, render, upload, schedule, publish or merge.
6. After actual separate production authorization, use channel pinned references and verify real identity PNG files and source rights; no claimed actual source bytes in this editorial packet.

**Measured results / external operations:** no live TTS/audio, no images, no MP4, no imported model reviews, no upload, no publication. vidIQ current available balance 0, no paid queries. Known blockers are runtime and independent review access; source and evidence search can continue free of charge.


## 2026-11-16 — существующий PR #101, новые альтернативы без master подмены

Сохраняется original (EN blob `537ab0539c1e6048fa28486d32f1f8c8f8e588ef`, RU blob `50471b35bf32a42df2469d1bc931c0414c32bb24`) и storyboard 42 original spans. Baseline ветки `42764d9b21373d3f2741272a689975c67406a6e4`. Созданы 3 раздельные редакции: `02m` EN SHA-256 `9a433fc78bd1924d94147bdbf22d02e69691f67dbbbcbb0aab650c8f0284fbf7`, RU SHA-256 `7df1698f79d0105b952a26299301c0f239cc49da321e9254c05bc8e2076bc3e3`; `05m` EN SHA-256 `81a672086161f55adf71ffd0975f42c92ebc420a0b7e55a29c0c3cc1169f5a09`, RU SHA-256 `a535667853490bdaf3aa3faa18903fde638b1ee0dc492c520912833f1c82515d`; `10m` EN SHA-256 `2e8f65aaf1cc93abbfc93d8effa653ff90dec3597318222601967a5920e62b37`, RU SHA-256 `5646819832c9fc23cfe6e8354a7ed0f82953ff3f5683e986ba42cffbcbe7b386`. Таблица путей и сравнение — [README](README.md) и [story-review](story-review.md). Рекомендация — 05m, **не** owner's selection.

Новый редакционный стандарт использован как прямое поручение владельца по предложенному [#124](https://github.com/kleksar/ytvideos/pull/124) `7d6bdf7702a2a241a33a21677fce29f26ada9b72`; #124 остаётся Draft и не объявляется main. New variants only supporting files: **EDITORIAL_CANDIDATE_UNREGISTERED**. В авторизованном runtime проверить действующие pins/context, зарегистрировать три пары через существующий `attach-artifact --kind script_variant` и сравнение как `story_review` с реальным `--source`, затем получить независимую проверку exact bytes и предъявить владельцу одну выбранную версию в обычном script gate. Никаких созданных IDs/run, повторных согласований или подтверждённых approvals здесь нет.

Источник на принятом PR не подменять. `storyboard.md`, `packaging-brief.md` исходно соответствовали original EN, а **не** новым версиям; пересобрать spans/visual intent/тайминги и metadata для выбранной версии после независимого review и владельческого выбора. Реальный TTS, смонтированный MP4, звуковой seam, удержание и превью обложки UNVERIFIED. No media generation, no schedule, no publication.

## 2026-11-19 — новая 05m редакция; перенос только exact bytes

Переработаны только `variants/05m/script.en.txt` / `script.ru.txt`. **Текущие** SHA-256: EN `73dfa51d9d17cfa65bb9802061811809204a0e9d27a8c9679f8bc328ea7384cb` (755 слов, Git blob `c8a45d137ff3532911f45a83caee1d5b728651a3`); RU `79f465d101c1351a2eb71e49360387753996ae5645ccab29cff162ff7768339d` (Git blob `fb587e83c777a0a6ec0ffc1fd5d8e6c133d378a1`). Старые 05m hashes из записи 2026-11-16 **исторические и непригодны для review/production**. 02m, 10m, original master, storyboard и старые pins не менялись. Актуальный canonical editorial стандарт находится в `main`: #124 merged 2026-11-16, не Draft.

`EDITORIAL_CANDIDATE_UNREGISTERED`: runtime `ytv` CLI и независимая reviewer-сессия не доступны в текущей GitHub-only среде; не выдумывать регистрацию, отзыв или receipt. При возможном дальнейшем импорте открыть локальный pinned context, перенести три exact пары как supporting artifacts, получить подлинный blind reviewer на новом 05m hash и отдельное решение владельца по одному master. Затем перестроить storyboard/visual spans по выбранному тексту; не наследовать 42 сцены старого master. No MP4, TTS, image generation, upload, release or merge.

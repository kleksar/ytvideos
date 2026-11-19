# McDonald's Monopoly — точный handoff после новой редакции

EDITORIAL_CANDIDATE_UNREGISTERED. English Long `paper_detour`. Новый текст: [EN](script.en.txt) **901 слово / 34 блока**, [RU](script.ru.txt) **34 блока**. Старый PR HEAD `c266ca02c6e40552f1dfb5c1d5d85ab39eadbc55` — архив исходника; его оценки, storyboard 38 spans и хронометраж НЕ относятся к текущей версии.

Перед официальным `uv run ytv start --channel paper_detour --format long --intent 'Review McDonald Monopoly editorial story for owner approval'` в авторизованном runtime проверить существующие active runs, pinned requirements и доступ к independent reviewer; не создавать дубликат. Наличие текстовых файлов в GitHub не доказывает `ytv-script-review-v1` или `awaiting_script_approval`.

Для документального Long вводные вопросы до погружения и основного hook (прямое требование владельца от 15 ноября, отражено в Draft PR #117). На точном EN/RU тексте выполнить новый blind first-listener и независимую историческую / bilingual сверку; не использовать старый hash или «PASS». Старый `storyboard.md` помечен OBSOLETE, только исторический снимок, без генераций; после принятой озвучки заново построить spans по фактическому таймингу.

В данном GitHub-only окружении локального CLI/хранилища и `sessions.independent` не подтверждено. Никаких TTS, картинок, MP4, upload, publish или merge без разрешения.

---

## Handoff: редакционные 02m / 05m / 10m от 2026-11-16

Доступны три полных EN/RU пары: [02m RU](variants/02m/script.ru.txt) / [EN](variants/02m/script.en.txt), [05m RU](variants/05m/script.ru.txt) / [EN](variants/05m/script.en.txt), [10m RU](variants/10m/script.ru.txt) / [EN](variants/10m/script.en.txt). Редакторская рекомендация — **05m**, но владелец master ещё не выбрал. Исходные `script.en.txt`/`script.ru.txt` остаются неизменными и дословно представлены в 05m; старый storyboard унаследован **ни одним** вариантом. SHA-256 и оценки точных версий — [story-review](story-review.md).

До production: проверить существующий сохранённый run, свой pinned контекст и права на канал; получить **реальный** blind independent first-listener отдельно для выбранного EN (при необходимости двуязычную сверку), сохранить собственный ответ reviewer без правок от автора; зарегистрировать `script_variant` и `story_review` через supported runtime, если он доступен; получить от владельца exact script approval. **Без** придуманного run ID/approval и без переноса старой раскадровки. Счётчики слов и целевые минуты — оценка, voice Lawrence 1.10× не менять. Статус до этого: `EDITORIAL_CANDIDATE_UNREGISTERED` / `UNVERIFIED`. Никакого TTS, Google Flow, MP4, upload или schedule.

## Обновление handoff 19.11.2026

Изменена только 10m пара, EN 1591 слов / 37 EN+RU смысловых абзацев. Baseline b393fe7aa67ed0f64c9e5dfd803ac09f0b0ff2c4; новые hashes в [story-review](story-review.md). **02m, 05m и root master сохранены.** Corporate giveaway на $10m — объявленный 21.08.2001 новый розыгрыш, не доказательство фактических компенсаций. Имена призовых заявителей приведены как allegation DOJ, не как приговоры. Предпочтительна 05m за темп до финала. Независимый first listener, factual/bilingual review, реальный TTS, owner approval, регистрация variants/review в runtime, построение новых storyboard spans и release — UNVERIFIED/NOT_DONE. Для переноса проверить existing run/pins, зарегистрировать шесть exact texts с hashes как supporting variants, выбрать один мастер и получить новое approval. Git-only status EDITORIAL_CANDIDATE_UNREGISTERED. Параметры канала/production не менять.

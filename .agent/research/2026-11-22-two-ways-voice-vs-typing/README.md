EDITORIAL_CANDIDATE_UNREGISTERED

# Two Ways Lab — Voice typing or thumbs: which message is ready first?

**Логлайн:** я должен отправить одно и то же 60-словное сообщение. Диктовка создаёт черновик втрое быстрее, но проверка способна поменять победителя. Это **расчётная модель**, а не эксперимент на реальном телефоне.

| Редакция | Production EN (полный текст) | Русский (полный перевод) | Авторская классификация |
|---|---|---|---|
| 2 минуты | [script.en.txt](variants/02m/script.en.txt) | [script.ru.txt](variants/02m/script.ru.txt) | **STRONG_CANDIDATE — рекомендована**, Short editorial |
| 5 минут | [script.en.txt](variants/05m/script.en.txt) | [script.ru.txt](variants/05m/script.ru.txt) | STRONG_CANDIDATE, Long production blocker |
| 10 минут | [script.en.txt](variants/10m/script.en.txt) | [script.ru.txt](variants/10m/script.ru.txt) | REWORK, Long production blocker |

**Выбор — 2 минуты.** За один короткий рассказ зритель узнаёт не только победителя при двух условиях, но и точную границу смены победителя: 48 секунд на проверку диктовки для 60 слов. Пятиминутная версия добавляет влияние длины текста и способ реального тестирования. Десятиминутная вводит чувствительность к дополнительной проверке и скорости ввода, но риск превращения истории в длинную лекцию значительно выше.

[Общее исследование, честные YouTube-контрсигналы и модель](research.md) · [Индивидуальные оценки, SHA-256 и сравнение](story-review.md) · [Упаковка](packaging-brief.md) · [Handoff](handoff.md).

**Границы:** исходный remote main `131ef24068d75967b1e43aa88e5f1370f6775054`; #124 merged, canonical документы main. `uv run ytv start --channel two_ways_lab --format short` в текущей среде дал `Failed to spawn: ytv / No such file or directory`. Нет run, independent reviewer, TTS timings, AV seam, production approval. Формат Long канала не настроен. Исправление — локальный checkout с установленным project runtime → настоящий `ytv start` и pinned packet → регистрация шести текстов с exact hash → independent review → один master и approvals. Никаких TTS, imagegen, MP4, upload, изменений расписания.

## Revision progress — 2026-11-23 · PR #353

**Before → after:** prior exact PR HEAD `6f3b974c3e57a6bab0b6ea497219fd10ea0d8197`; revised 10m EN/RU are complete new oral scripts with the actual SHA-256 values below. No alteration to preferred 02m or 05m. The previous ten-minute draft had 1705 EN words and a long explanatory afterword after the main reveal; current 10m has 1239 EN words and a distinct long-message sensitivity reversal, then returns to the Send-ready payoff.

| Same 60-word message and variants | Full RU | Full EN | Authorial status |
|---|---|---|---|
| 02m · Short | [RU](variants/02m/script.ru.txt) · [EN](variants/02m/script.en.txt) | Strong original preserved; 299 EN words; author-only seam; AV UNVERIFIED | 
| 05m · Long | [RU](variants/05m/script.ru.txt) · [EN](variants/05m/script.en.txt) | Original preserved; 788 EN words; Long production BLOCKED |
| 10m · Long | [RU](variants/10m/script.ru.txt) · [EN](variants/10m/script.en.txt) | Full new causal revision; 1239 EN words; potential UNDERLENGTH; Long production BLOCKED |

**New 10m SHA-256:** EN `983bdaee9c0251594acea79a2909235731546cc589c18dd056e731211ba9e56a`; RU `f695d55d2e08d27c9da67f9debac0cee709c17875fe5f3bd967fa9e1cc38fdea`. Existing 02m/05m SHA-256 and packaging unchanged. The new length remains **REWORK_UNDERLENGTH**, not confirmed as 10 minutes. **Recommendation is still 02m**, not approval. Hypothetical model E110 for 120 words now reveals B=158 > A=144; source of model and limits: [research](research.md#2026-11-23-revision-specific-sensitivity-case-10m-only). Author-only eight criteria and separate gates: [review](story-review.md#2026-11-23-substantive-review--10m-exact-revision-supersedes-earlier-10m-author-judgement).

**Unregistered:** no actual ytv local runtime, pinned task packets, independent reviewer response, owner approval, voice measurement, scene assets, AV Short seam or final rights checks. Two Ways Lab Long production configuration missing; this Git-only variant is not a permission to configure it. PR-head CI/remote diff must be checked after push. No media, merge or publication.

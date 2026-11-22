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

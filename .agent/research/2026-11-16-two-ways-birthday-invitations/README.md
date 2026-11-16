EDITORIAL_CANDIDATE_UNREGISTERED — Git-only editorial candidate; no verified `uv run ytv start`, pinned context, independent reviewer, script gate, approval, or production.

# Two Ways Lab — Eight birthday invitations: first finished vs all finished

**Логлайн:** я делаю восемь приглашений двумя способами. A выдаёт первый готовый конверт за **30 секунд**, а B — лишь за **2:22**. Но все восемь B заканчивает за **2:50** против **4:35** у A. Неочевидный ответ: «что именно должно быть готово первым?» Это **условная модель**, а не реальный хронометраж работы человека.

## Одна история — три законченные редакции

| Версия | Полный русский текст | Полный английский narration master | EN words | Авторский статус / производственная граница |
|---|---|---|---:|---|
| **02m (рекомендуется)** | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | 267 | **STRONG_CANDIDATE**; поддерживаемый Short 9:16, фактический seam UNVERIFIED |
| 05m | [RU](variants/05m/script.ru.txt) | [EN](variants/05m/script.en.txt) | 717 | STRONG_CANDIDATE editorial; **Long production BLOCKED** |
| 10m | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | 1,609 | REWORK, complete editorial Long; **Long production BLOCKED** |

Оценка хронометража **до озвучки**: 02m ~1:45–2:10 при 135–160 английских словах/минуту с паузами; 05m ~4:35–5:20 при 140–165; 10m ~9:35–11:30 при 145–170. Это ориентиры, не измеренный TTS. Русский — полный смысловой эквивалент, не второй production voice.

**Почему 02m:** полный двойной payoff — ранний выигрыш A и поздний выигрыш B — без длинного расчёта в речи. 05m объясняет смену критерия и цену setup, но требует неподключённого Long. 10m добавляет тесты чувствительности и ограничения, однако после уже понятного результата становится слишком объяснительным. Не создавать три production run.

[Общее исследование, аналоги, YouTube и воспроизводимый расчёт](research.md) · [SHA-256, восьмикритериальные оценки каждой версии и сравнение](story-review.md) · [Упаковка рекомендованной версии](packaging-brief.md) · [Границы исполнения и передача](handoff.md).

**Ограничения:** подтверждённый спрос, прямой просмотр и комментарии YouTube, собственная аналитика, внешний первый слушатель, реальная озвучка, AV seam, права на будущие изображения и approval — UNVERIFIED. Модельная арифметика проверена автором; она не является эмпирическими данными. Назначать победителя без явного определения метрики нельзя. Существующие видео Gemba Academy о таком же типе конвертов показывают **противоположный** итог в другой постановке — это честный контрсигнал, а не источник наших 5-секундных setup.

**Provenance:** branch created from exact remote main `b1be73fbcd2a87dafe34ad65c479d337a26ebd80`. Правило 2/5/10 — прямое поручение владельца по [PR #124](https://github.com/kleksar/ytvideos/pull/124), **proposed** revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` (не main и не merged на момент создания). Код, общие skills/docs, профили и чужие PR не менялись.

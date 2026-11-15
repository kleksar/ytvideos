EDITORIAL_CANDIDATE_UNREGISTERED — Git-only editorial draft, **not** an official `ytv start` run, script approval or production order.

# Nuviko History — Entebbe, 1976: the rescue that needed a black Mercedes

**RU логлайн.** Военные прилетели за тысячи километров, чтобы освободить заложников в аэропорту Уганды. Они выгрузили «Мерседес» для маскировки под кортеж диктатора, но план нарушила стрельба у терминала. Спасли 102 человека; не все вернулись домой. Суть истории — сочетание переговоров, разведданных, топлива и штурма, а не чудо одного автомобиля.

| Готовая редакция одной истории | Полный RU | Полный EN master | EN words | Рабочий формат | Авторский статус |
|---|---|---|---:|---|---|
| 02m | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | 301 | Short 9:16 | STRONG_CANDIDATE |
| **05m — рекомендована** | [RU](variants/05m/script.ru.txt) | [EN](variants/05m/script.en.txt) | 725 | Long 16:9 | **STRONG_CANDIDATE** |
| 10m | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | 1430 | Long 16:9 | REWORK — лишняя плотность военного/дипломатического объяснения |

Каждый текст автономен и закончен. RU — полная смысловая редакция EN, не отдельный TTS master. Ориентировочные устные длительности при **допущении** 145–170 EN wpm с паузами: 02m ≈1:50–2:20; 05m ≈4:30–5:30; 10m ≈9:00–11:00. Профиль задаёт скорость 1.10× ровно один раз, **реальная длительность UNVERIFIED** до TTS. Для Long отдельный 10-секундный end screen после рассказа.

**Выбор 05m:** показаны дополнительные проверенные препятствия (освобождённые пассажиры → план здания → спор о переговорах → обратный маршрут → маскировка, которая не выдержала → реальные потери), а не повтор хука. 02m более компактна и подходит для Short. В 10m после основного результата расширенная институциональная линия повышает цену внимания — её нельзя выбирать только за хронометраж.

[Research: факты/конкуренты/источники/YouTube](research.md) · [Story review: восемь критериев, hashes и сравнение](story-review.md) · [Brief для выбранной 05m](packaging-brief.md) · [Handoff и blockers](handoff.md).

**Критические границы:** независимый first listener / `sessions.independent`, реальный `ytv start`, реальные task packet/lease, TTS/AV loop, rights clearance, owner approval, собственные метрики и спрос — **UNVERIFIED**. Авторский review ≠ независимый reviewer. Никаких выдуманных receipt, user approval, сцен или медиа.

Исходная база — remote `main` **b1be73fbcd2a87dafe34ad65c479d337a26ebd80**. Требование 2/5/10 применяется по прямому поручению владельца из **proposed, не merged** [PR #124](https://github.com/kleksar/ytvideos/pull/124), revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72`. Общие docs/skills и ChannelSpec не изменены.

EDITORIAL_CANDIDATE_UNREGISTERED

# Paper Detour — The Lifeboats Were There. Time Was Gone.

**Логлайн:** 13 января 2012 года Costa Concordia налетела на скалы у Джильо. Пока пассажирам говорили о проблеме с электричеством, вода проникала в корпус. Приказ об эвакуации прозвучал больше чем через час; часть шлюпок уже не получалось спустить из-за крена. Судно осталось у острова ещё более двух лет. Не утверждаем, что один только поздний приказ объясняет все 32 смерти.

| Одна история, полный текст | EN production narration | Полный русский смысловой перевод | Авторский статус / предполагаемый формат |
| --- | --- | --- | --- |
| 02m | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | REWORK: Short, механический last→first, AV seam UNVERIFIED |
| **05m** | **[EN](variants/05m/script.en.txt)** | **[RU](variants/05m/script.ru.txt)** | **STRONG_CANDIDATE / Long 16:9 — редакционная рекомендация** |
| 10m | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | REWORK: Long 16:9, спасательная операция после кульминации замедляет середину |

**Почему 5m:** в отличие от 02m есть отдельное развитие через сообщение на берег, запаздывание эвакуации, механизм отказа спуска шлюпок и инженерную развязку; 10m добавляет подтверждённые подробности, но их стоимость для зрителя не столь высока. Длительность до TTS только оценочная, не измеренное время. Эта рекомендация НЕ является approval выпуска.

- [Research и зрительские сигналы](research.md)
- [Оценки шести exact текстов, SHA-256, сравнение 2→5→10](story-review.md)
- [Упаковка: честный title / thumbnail / первое доказательство / payoff](packaging-brief.md)
- [Постановочная заготовка исключительно под 05m](variants/05m/scene-plan.md)
- [Передача в рабочий runtime, границы и blockers](handoff.md)

**Capability/blocker:** в доступной Git-only среде отсутствует запускаемый `ytv` из репозитория, поэтому не создан `uv run ytv start`, `plan_summary` и pinned packet. Независимый reviewer не запускался. Script gate, TTS, media, публикация и production approval **не выполнены**. Локальный перенос описан в [handoff](handoff.md).
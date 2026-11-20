EDITORIAL_CANDIDATE_UNREGISTERED — редакционная Git-очередь, не официальный `ytv start`, не script gate, не одобрение производства.

# Paper Detour — The Great Boston Molasses Flood (1919)

**Логлайн.** В 1919 году по жилым улицам Бостона пронеслась гигантская волна патоки, убив 21 человека. Резервуар протекал годами, но его красили, а не укрепляли. Вопрос: как медленная патока могла так быстро убивать и почему предупреждение проигнорировали?

| Одна история | Полный русский текст | English narration master | EN words | Формат / статус |
|---|---|---|---:|---|
| 2 минуты | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | 287 | Short 9:16 — STRONG_CANDIDATE |
| **5 минут** | [RU](variants/05m/script.ru.txt) | [EN](variants/05m/script.en.txt) | 731 | Long 16:9 — **рекомендована, STRONG_CANDIDATE** |
| 10 минут | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | 1571 | Long 16:9 — REWORK, закончена, но плотность слабее |

Тексты **самостоятельные и законченные**, не планы и не нарезки общего master. Пять минут также называют погибших детей и пожарного, раскрывая три действительно разные причины удержания — масштаб первой волны, охлаждение и сложность спасения, затем доказательства халатности. Две минуты дают полный ответ быстрее; длинный вариант расширяет судебный и общественный контекст, но часть добавочного времени менее насыщена.

Хронометраж **предположительный**: при 145–170 EN слов/мин с ориентиром дополнительных пауз ~5–12 сек: 2m ≈1:46–2:11, 5m ≈4:23–5:15, 10m ≈9:19–11:02. Фактический голос Lawrence, 1.10×, и паузы до озвучки **UNVERIFIED**. Для Long — отдельный 10-секундный end screen после narration. Нельзя менять скорость голоса ради заявленного числа минут.

- [Research: источники, первичный скрининг 10 историй, три финалиста, YouTube-сигналы и пределы](research.md)
- [Story review: восемь критериев каждой точной версии, SHA-256, сравнение и blockers](story-review.md)
- [Packaging для выбранной 05m](packaging-brief.md)
- [Handoff для локального runtime](handoff.md)

**Граница:** независимый первый слушатель, точный `ytv start` и pinned task packet, owner choice/approval, measured duration, TTS, AV loop, media rights — **UNVERIFIED/NOT_RUN**. Ни одна авторская оценка не выдаётся за retention/CTR.

Исходный remote `main`: `b1be73fbcd2a87dafe34ad65c479d337a26ebd80`. Прямое редакционное поручение о 2/5/10 принято из **proposed**, не merged [PR #124](https://github.com/kleksar/ytvideos/pull/124), exact revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72`. Общие docs/skills/channel status не менялись.

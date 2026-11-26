EDITORIAL_CANDIDATE_UNREGISTERED

# Two Ways Lab — The Highway AC Rule That Failed Its Own Test

**RU логлайн:** Я сравниваю открытые окна и кондиционер на одной машине при той же скорости и расстоянии. Испытания Ок-Риджской лаборатории ломают распространённое правило: даже на 70 милях в час открытые окна экономичнее кондиционера на максимуме в двух проверенных машинах; на 80 милях в час Corolla меняет победителя, Explorer — нет. Это анализ опубликованных измерений, **не снятый эксперимент**.

| Цель | Формат | Полный EN | Полный смысловой RU | Авторская редакционная оценка |
|---|---|---|---|---|
| 02m | Short candidate, longer than usual 35–50s | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | STRONG_CANDIDATE по содержанию; авторский loop textual candidate, independent/AV UNVERIFIED |
| **05m** | Editorial Long, production blocker | **[EN](variants/05m/script.en.txt)** | **[RU](variants/05m/script.ru.txt)** | **STRONG_CANDIDATE — рекомендуется как самая полезная редакция** |
| 10m | Editorial Long, production blocker | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | REWORK — после основного результата слишком много пояснительного материала |

**Рекомендована 05m редакция:** механизм сопротивления → 2009 Corolla/Explorer → противоположный исход на 80 mph → почему max AC не описывает обычный режим → практическая оговорка. Двухминутная успевает завершить сравнение, но частично теряет объяснение условий; десятиминутная добавляет независимые исследования и границы модели ценой замедления.

[Общее исследование и конкуренты](research.md) · [SHA-256, сюжетные карты, восемь оценок каждой редакции и hard checks](story-review.md) · [Упаковка](packaging-brief.md) · [Handoff](handoff.md).

**Границы:** тексты являются одной историей с тремя завершёнными редакциями, не тремя отдельными испытаниями. Общая фактическая основа — опубликованный ORNL 2013 и DOE/EPA FuelEconomy.gov; результаты не переносить на любую машину или «порог 50 mph». Данные реального viewer interest, свежего retention, CTR, независимого чтения и AV seam — UNVERIFIED. Редакционные баллы не performance forecast. Первое лицо описывает выбор, не притворное проведённое испытание.

**Runtime blocker:** `uv run --offline ytv start` в доступном контейнере завершился `Failed to spawn: ytv` / `No such file or directory (os error 2)`. Канонические `plan_summary/read_next/task_guide/pinned reference_documents` и независимый reviewer в этом окружении не получены. Это *исключение для Git-only редакционной очереди*, не script gate/lease/approval. Two Ways `long` recipe не определён; 05m/10m только текстовые editorial proposals, 02m не согласован в 35–50s. До производства требуется точный runtime import и независимый review hash выбранного текста, approval владельца.

Никаких TTS, изображений, MP4, загрузки, публикации, расписаний или изменения общих правил.

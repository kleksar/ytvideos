EDITORIAL_CANDIDATE_UNREGISTERED — не официальный script gate. Independent reviewer, run и approval: UNVERIFIED.

# Henry “Box” Brown: человек, доставленный в ящике

**Одна история, три законченные редакции.** В 1849 году Браун бежал из рабства как груз, пережил опасные перевороты ящика и позже публично рассказывал о своём побеге. У него оставалась невосполнимая потеря — проданные в рабство жена и дети; подтверждённого воссоединения нет.

| Цель | Полный русский текст | Full production EN | Words EN | Редакторский статус |
|---|---|---|---:|---|
| 02m | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | 264 | **содержательно уточнена 21.11; timing/AV/storyboard UNVERIFIED** |
| **05m** | **[RU](variants/05m/script.ru.txt)** | [EN](variants/05m/script.en.txt) | 653 | **рекомендована к independent review** |
| 10m | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | 1265 | завершена; слабее по темпу |

**Рекомендация 05m:** помогает понять механизм отправки, цену маскировки, реальную опасность при перегрузках и последствия публичности. В 10m появляются важные сведения из более позднего свидетельства 1851 года и отдельная театральная линия, но после спасения история теряет темп. 02m теперь завершает линию семьи и публичности, но риск переполненного темпа при 264 словах всё ещё нельзя подтвердить до TTS.

**Сохранённый baseline:** branch HEAD 021a9c8b651950030b29268404e71938dc3b2e70; неизменённые root [script.en.txt](script.en.txt) / [script.ru.txt](script.ru.txt) были буквально скопированы в variants/02m до 20.11; новая 02m пара отделена от исходных root masters. Предварительный [storyboard на 18 сцен](storyboard.md) и [packaging](packaging-brief.md) привязаны только к исходным root bytes; **не** к обновлённой 02m. Ни scene spans, ни timings нельзя переносить на какую-либо из трёх текущих variants. Под них пока нет раскадровки: число сцен должно следовать точной выбранной версии.

[Факты и источники](research.md) · [Точные SHA-256, story maps, оценки, blockers](story-review.md) · [Путь передачи локальному агенту](handoff.md).

Progress: baseline 021a9c8b → три полные пары 02/05/10 → переработка 02m 20.11 → более плотная 02m 21.11 (лишняя линия о последующем аресте перенесена только в неизменённые Long; новое причинное возвращение к предупреждению) → авторская проверка фактов/EN-RU/целого Short → 05m всё ещё предварительно рекомендована. Exact 02m SHA-256 EN `35efe297356a40fb02a45f724a7a54ff65a1d0e55f9730d3a29424c8ef2c2447`, RU `28cdaceb6b47c86e39d10a90a32b3607cdd0770902a21ac42dde41f4fee76f48`; 05m/10m и исходные root scripts не менялись. Independent first-listener, runtime registration, voice duration, AV loop, audience demand: **UNVERIFIED**. Никакие медиа, расписание, публикация, approvals или pins не изменялись.

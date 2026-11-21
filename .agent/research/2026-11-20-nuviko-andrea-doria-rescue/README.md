EDITORIAL_CANDIDATE_UNREGISTERED

# Nuviko History — Andrea Doria: The Lifeboats Nobody Could Reach

**Логлайн.** В 1956 году итальянский лайнер «Андреа Дориа» после столкновения с «Стокгольмом» накренился настолько сильно, что большая часть его шлюпок стала недоступна. Другим кораблям пришлось доставлять собственные лодки. Сам «Стокгольм» принимал спасённых, а французский «Иль-де-Франс» развернулся и вывез 753 человека.

**Рекомендация: пять минут, Long, STRONG_CANDIDATE (авторская, не approval).** Эта редакция не просто повторяет парадокс шлюпок, а раскрывает помощь сухогруза, повреждённого второго лайнера, прибытие военного транспорта и решение французского капитана. Полная развязка: 1660 выживших из 1706 человек на «Андреа Дориа» и 46 погибших на ней; ещё 5 погибли на «Стокгольме». Источники — в [research.md](research.md).

| Версия | Полная английская | Полная русская | Классификация | Формат |
|---|---|---|---|---|
| 2 минуты | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | STRONG_CANDIDATE, текстовая петля самопроверена; independent UNVERIFIED | Short, 9:16; timing estimate |
| **5 минут** | **[EN](variants/05m/script.en.txt)** | **[RU](variants/05m/script.ru.txt)** | **STRONG_CANDIDATE — рекомендована** | **Long, 16:9** |
| 10 минут | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | REVISED — добавлена подтверждённая линия семьи Боггс; независимое чтение и длительность UNVERIFIED | Long, 16:9 |

Это **одна история и шесть самостоятельных полных текстов**, а не единый master, обрезанный на три отрезка. EN — предлагаемый production master; RU — смысловой перевод для review. Точные UTF-8 SHA-256, восемь отдельных редакционных критериев на каждую языковую редакцию, главные недостатки и сравнение находятся в [story-review.md](story-review.md). [packaging-brief.md](packaging-brief.md) связывает заголовки, подтверждаемое обещание, первые действия и развязку. [handoff.md](handoff.md) фиксирует полномочия, pins и блокеры.

**Ни один production stage не пройден.** Команда `uv run ytv start` в доступной среде завершилась `Failed to spawn: ytv`; настоящего run/lease/receipt/approval нет. Независимый reviewer не вызван, TTS/MP4 не созданы, длительность и AV seam не измерялись. Это исключительно редакционная Git-очередь, не официальный script gate. PR #124 уже merged; читать действующий main, не выдавать proposed SHA за canonical. Никаких изменений общих docs, skills, channel status или media.


## Содержательная переработка 21 ноября 2026

**Было:** во всех шести текстах «Иль-де-Франс» ошибочно шёл *к* Нью-Йорку до SOS. По [MARAD](https://www.maritime.dot.gov/history/gallant-ship-award/ss-%C3%AEle-de-france) он шёл **из Нью-Йорка в Европу**, развернулся к месту аварии, вывез спасённых обратно в Нью-Йорк и затем продолжил путь в Европу. **Стало:** направление и причина разворота исправлены во всех трёх полных версиях EN/RU. В 10m вместо повторения выводов после гибели лайнера появилась подтверждённая свидетельством [семьи Боггс, 31 июля 1956 года](https://vineyardgazette.com/news/1956/07/31/desperate-hours-survivors-doria-italian-vessel-sounded-fog-horn-say-dr-and-mrs/) линия: разделение членов семьи → дым/крен → ожидание → два разных пути эвакуации → встреча на французском судне. Сведения не выдаются за показания всех пассажиров.

| Длительность | Полный EN | Полный RU | EN words | Предварительное решение |
|---|---|---|---:|---|
| 2m Short | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 295 | Завершён, авторский text seam, independent/AV UNVERIFIED |
| **5m Long** | **[EN](variants/05m/script.en.txt)** | **[RU](variants/05m/script.ru.txt)** | **747** | **Рекомендуется: более компактная причинная линия** |
| 10m Long | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1677 | Новая линия реальных очевидцев; риск перегруженного middle и длительности |

Новые SHA-256 и отдельно восемь оценок/жёсткие проверки для шести изменённых текстов — в [story-review.md](story-review.md). Все исходные production pins, master, approvals и media остались нетронутыми. Это **EDITORIAL_CANDIDATE_UNREGISTERED** (без невидимого символа в machine status: `EDITORIAL_CANDIDATE_UNREGISTERED`), independent review, TTS и owner approval **UNVERIFIED**. Для выбора исходника использовать конкретный Git commit SHA и hash, а не master/storyboard от другой версии.

# Story review — One Microwave, Four Lunches (exact variants)

Дата: 2026-11-23. Автор и единственный редактор: ChatGPT GPT-6 (самопроверка; независимый reviewer в этой среде отсутствует). Тексты находятся в `variants/`; оценки — редакционные мнения, **не** CTR, retention, прогноз просмотров или заключение владельца. Research и source model: [research.md](research.md). Git-only очередь, `EDITORIAL_CANDIDATE_UNREGISTERED`.

## Точная identity и оценочная длительность

SHA-256 вычислен из точных UTF-8 bytes с завершающим LF после **последней** смысловой редакции. Git blob SHA даны для дополнительной сверки read-back. EN — production narration; RU — полный смысловой перевод. Ссылка на каждый вариант относительна и останется стабильной внутри PR.

| Версия | EN narration: words, SHA-256, Git blob | RU: words, SHA-256, Git blob | Время/format (оценка, не TTS) |
|---|---|---|---|
| 02m | [302 EN words](variants/02m/script.en.txt), `b9495e8612ce19c610671bdb87c5a57880a35203e8c4767149e6faf331e750b3`, blob `4e4e18035066cc7c1855ea572b91d054df74fdb7` | [280 RU words](variants/02m/script.ru.txt), `53424826aea0101b316f8afa376866ad3b9ca730d27cb5ad8a31842fab129170`, blob `8c80d427da5736c17fc11dca04cdc9fae5009d44` | EN 1:57–2:10 при 145–155 wpm + паузы ≈2:02–2:20; intended illustrated Short 9:16, **длиннее канального ориентира 35–50s** |
| 05m | [790 EN words](variants/05m/script.en.txt), `30896252aed385fe4245e5f395d4ea94645da96e8d95ff9ee69053fa166b706c`, blob `2b13ef29c8b796b9bf86aaec9904c83873ab88a0` | [657 RU words](variants/05m/script.ru.txt), `910f45535938e8dd7bdcd9129517fa4b099dd044fecc146db6eca407c56b830c`, blob `a0f500fdbeee61db314f9528dc3e2aeecfa5a35a` | EN ~4:47–5:27 при 145–165 wpm + паузы; editorial Long **PRODUCTION_BLOCKER: Long recipe unset** |
| 10m | [1425 EN words](variants/10m/script.en.txt), `f98abbbe029e160c4e704e792e47aaf7f171fa5889cd39124d39f7fd7325eedc`, blob `de4fd2f7f5fb56a534300b0814f278a980769572` | [1159 RU words](variants/10m/script.ru.txt), `37fbdb60e69952a8cd3fd8eb91f63db56bfdc2b2db7c11c93593f84a9ab13727`, blob `86bcde1a166d622d9d8acc459f7da2edc6dbaae2` | EN ~8:54–9:50 at 145–160 wpm, plus pauses ≈9:05–10:10; **estimated**, not measured. Editorial Long; **PRODUCTION_BLOCKER: Long recipe unset** |

Реальная скорость voice ID `zfc8CJQpe8Kqyl0vvCzo`, паузы, измеренная длительность TTS/MP4 и права — UNVERIFIED; не менять закреплённую скорость 1.0. Математический эксперимент не снимался и не измерялся.

## Готовая редакция 02m: STRONG_CANDIDATE — recommended, confidence MEDIUM / demand LOW

Story map: cold question `Who should go first at the only microwave in my office?` → четыре одновременных прихода и два заранее объявленных порядка → метрика среднего времени до еды → A completion 10/12/14/15 → B completion 1/3/5/15 → победа 6:00 vs 12:45 → обладатель 10m обеда опаздывает при 11m deadline → конкретный условный выбор и петля. После хука **есть два новых исхода**, а не только повторы цифр.

| Критерий editorial | Авторская оценка и проверяемое основание |
|---|---|
| 1. Интерес/значимость | **8/10** — личная дилемма `Who should go first...` и реальная конфликтность очереди в Reddit; не все зрители разделят интерес к модели |
| 2. Начало | **8/10** — сразу один прибор, четыре обеда и вопрос, без неизвестного термина |
| 3. Развитие/причина остаться | **8/10** — `At minute five...` и смена результата между A и B, затем личная потеря владельца длинного контейнера |
| 4. Payoff | **9/10** — `The average with B is six minutes`, затем дедлайн `minute eleven`; выигрыша без учёта цели не обещает |
| 5. Свежесть угла | **7/10** — известная математическая идея, бытовая постановка без обнаруженного точного видео-двойника |
| 6. Визуальная выразительность | **8/10** — два ряда контейнеров, один счётчик, на t5 результат 0 vs3 и конфликт одного человека; **изображений ещё нет** |
| 7. Живость/ясность речи | **7/10** — фразы о человеке и обеде естественнее лекции, но ~302 EN words могут перегружать 2m Short |
| 8. Подтверждённость спроса | **UNVERIFIED** — Reddit вопросы/комментарии показывают обсуждение ситуации, сопоставимые YouTube — учебные, не Two Ways Shorts |

**Главный недостаток:** две минуты превышают привычные 35–50s ролика и рассчитаны на модельную информацию, а не реальные смешные действия. Не сокращать автоматически или ускорять голос ради привычного Short. Сильнейший смысловой payoff в конце есть; чисто техническая проверка loop не равно AV.

Literal EN Short seam: closing `Before anyone presses Start, I still have to ask:` → opening `Who should go first at the only microwave in my office?` (после ответа ещё раз ставит уже понятную задачу с новым контекстом дедлайна; настоящее естественное вопросное продолжение, не один повтор предмета). Literal RU seam: `мне всё равно нужно спросить:` → `Кого поставить первым к единственной микроволновке в офисе?`. Автор прочитал весь EN/RU два прохода и сравнил последнюю и первую реплики. **Independent double reading UNVERIFIED.** Полный payoff до seam; audio/video seam UNVERIFIED.

## Редакция 05m: STRONG_CANDIDATE as text, production BLOCKED, confidence MEDIUM

Story map: вопрос о справедливости → правила одновременного прихода и score → A/B на общих часах → неожиданное равенство 15m завершения → противоречие среднего и ущерба человеку с долгим обедом → его дедлайн → двухконтейнерный обмен 10+1 → границы реальной кухни → итог без новой неразрешённой интриги.

| Критерий | Авторская оценка и наблюдение |
|---|---|
| 1. Интерес/значимость | **8/10** — одновременно выигрыш группы и проигрыш отдельного человека; длиннее двухминутной версии |
| 2. Начало | **8/10** — `Which lunch should enter the office microwave first?` и `fair result` сразу обещают вопрос |
| 3. Развитие | **8/10** — от порядка к среднему, затем `I could pretend everybody benefits. That would be false`, потом отдельный критерий дедлайна |
| 4. Payoff | **8/10** — итог `B wins the average, A protects the earliest deadline`; все обещанные результаты названы |
| 5. Новизна угла | **7/10** — SPT известен в teaching, социальная дилемма добавляет угол |
| 6. Визуальность | **8/10** — два изометрических порядка, пара 10/1 и перевод счётчика; иллюстрации не созданы |
| 7. Естественность/ясность | **7/10** — сравнительно ясный разговорный EN/RU, но пара дополнительных расчётов может терять неспециалиста |
| 8. Аудиторный спрос | **UNVERIFIED** — ни одно видео не соответствует длительности, формату и аудитории одновременно |

**Главный недостаток:** в длинной версии заметно объяснение механизмов вместо действия, и нет production Long recipe у канала. Семантический Long ending завершён, Short loop N_A. Продукционный формат FAIL до появления документированного Long-профиля; редакционная полнота текста не обходит blocker.

## Редакция 10m: substantial revision of exact EN/RU, EDITORIAL_CANDIDATE; confidence MEDIUM on arithmetic / LOW on unmeasured audience

**Baseline:** old EN `d05d81d6b227d656d68a1604ca8b03eaeef89f3a9a56ca206eb92d9164847aa7`, old RU `24fe042ebe5d3e415cebc8b9c343365ffcc87e77d86964b77df1e73764fcd30b` (PR #385 initial head `bc2eab7f58e864a398e4e7fe17a2a0b3158fb834`). The original 10m has been **replaced in-place**, not lost: its bytes remain accessible at that immutable Git commit. 02m and 05m remain byte-identical. Current 10m hash identity is in the table above.

**Before → after:** old 10m spent the final stretch explaining pairwise scheduling, changing estimates, changing containers and fairness metrics after the main A/B result. New 10m uses the same inputs but **a new problem caused by the preceding result**: B gives 6:00 average but makes L miss t11. I then negotiate a specific trade, test [1,10,2,2], get 10:00 average **and** L ready at t11, establish optimality under that hard constraint, then tighten the deadline to t10 and show why only L-first can work. A late-arrival reset challenges what the rearrangement can promise. All are explicitly different model conditions, not claims about real food.

**Story map:** question about group win versus one person's lunch → hypothetical model and clear average-to-ready metric → A completion 10/12/14/15, B completion 1/3/5/15, group win at same appliance total15 → L's t11 deadline fails under B → compromise [1,10,2,2], completion 1/11/13/15, average10:00 while meeting deadline → prove only L-first or S-first-with-L-second can satisfy t11 → t10 change forces L-first, average12:15 → late arrivals t5 make earlier B physically unavailable, with separate arrival-based mean8:30 → qualified payoff and real-world consent.

| Критерий editorial | Авторский балл и конкретное основание/ограничение |
|---|---|
| 1. Интерес/значимость | **8/10** — после групповой победы появляется личная проблема: `one colleague miss lunch entirely`; гипотетичность снижает убедительность для части аудитории |
| 2. Начало/обещание | **8/10** — три первых абзаца ставят проверяемый вопрос о компромиссе, метрику и правила до чисел; относительно длинный setup |
| 3. Развитие/причина смотреть | **8/10** — новый шаг `can I give the short lunches a head start and still have the long meal ready` приводит к третьему рассчитанному состоянию и граничному t10, а не к лекционной вставке; доказательство допустимых перестановок ещё плотное |
| 4. Payoff | **8/10** — противопоставлены 6:00 без дедлайна, 10:00 с t11 и 12:15 с t10; итог не обещает, что все люди выигрывают |
| 5. Свежесть угла | **7/10** — задача с deadline-constrained queue в школьной/операционной математике известна; бытовая история и конкретный компромисс являются сценической интерпретацией, спрос на неё не доказан |
| 6. Визуальность | **8/10** — три реально различающихся временных состояния A/B/компромисс, отдельный one-minute deadline flip и поздний приход; actual artwork/scene continuity UNVERIFIED |
| 7. Естественность/ясность | **7/10** — действия `I put the one-minute meal in` и дедлайн конкретнее прежнего `sum of completion times`, но чисел всё ещё много; требуются независимое чтение/voice timing |
| 8. Подтверждённость зрительского спроса | **UNVERIFIED** — существующие Reddit-вопросы относятся к общей проблеме, не к этому десятиминутному сценарию; CTR/retention отсутствуют |

**Главный недостаток и confidence:** после `I want to check whether another order could reduce the average` техническое доказательство может временно ослабить зрительское действие, хотя теперь оно разрешает заявленное ограничение. Авторская уверенность **MEDIUM** в структуре и **HIGH** в арифметике условной модели, **LOW** в пользе 10m для конкретных зрителей без независимого feedback. Не производить Long: canvas/fps/recipe не заданы. Редакционный текст не становится production PASS.

## Сравнение трёх точных текстов и рекомендация

| Переход | Содержательное приобретение | Потенциальная потеря внимания |
|---|---|---|
| **02m → 05m** | Из сильного краткого сравнения A/B получается полный reset, индивидуальные времена, объяснение, почему appliance total не изменился, и парный обмен 10/1 | В 05m `Why does placing short meals first cut the average?` переводит сцену в объяснение после развязки |
| **05m → revised 10m** | После провала L в B появляется новая достижимая цель: `[1,10,2,2]` даёт 10:00 и дедлайн t11, меняющийся на t10; есть доказательство оптимальности и сценарий позднего прихода | Середина доказательства двух допустимых размещений L и поздние времена прибытия могут потребовать визуальной поддержки, которой пока нет |

**Рекомендация по содержанию остаётся 02m EN `b9495e8612ce19c610671bdb87c5a57880a35203e8c4767149e6faf331e750b3`** (02m RU `53424826aea0101b316f8afa376866ad3b9ca730d27cb5ad8a31842fab129170`): больше действия на минуту и два завершённых результата без математического блока. Переработанная 10m теперь имеет **самостоятельную добавочную ценность** (не только повтор) и является честным editorial candidate, но качество для зрителей и хронометраж **UNVERIFIED**, Long production **BLOCKED**; выбора владельца, approvals и запуска трёх медиа нет. 05m по-прежнему пригодна как редакционный текст, но её Long recipe также отсутствует.

## Матрица checks (только проверенное)

| Check | 02m | 05m | 10m | Метод и предел |
|---|---|---|---|---|
| Арифметика/условная модель | **PASS** | **PASS** | **PASS** | Авторский пересчёт двух порядков, суммы 51/24/40/49, среднее 12.75/6/10/12.25, поздний приход (10+6+8+10)/4=8.5; EN/RU данные сверены; нет реальных замеров |
| Фактологические утверждения о реальном мире | **PASS (limited)** | **PASS (limited)** | **PASS (limited)** | Narration не утверждает реальных результатов, теоретический принцип подтверждён open SPT explanation; источники в research, не в речи |
| Эквивалентность EN/RU ключевых действий | **PASS (author)** | **PASS (author)** | **PASS (author)** | Авторский параллельный просмотр двух полных версий; независимый двуязычный review UNVERIFIED |
| Редакционная завершённость payoff | **PASS (author)** | **PASS (author)** | **PASS (author), attention UNVERIFIED** | Точные концовки отдают объявленные ответы |
| Формат / ChannelSpec | **UNVERIFIED** | **FAIL production** | **FAIL production** | 2m script предложен для illustrated Short, существенно длиннее 35–50s; 5/10 Long canvas/fps = null |
| Short text loop | **PASS (author)** | N_A | N_A | EN и RU literal question seam, каждый текст прочитан дважды одним автором |
| Независимый reviewer | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | Отдельная model session/reviewer tool недоступны. Никакого `ytv-script-review-v1` не создано |
| Фактический AV seam, TTS, права/assets | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | Видео, аудио, изображения и права не проверялись и не создавались |
| Спрос / CTR / retention | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | Публичные lecture views + Reddit дискуссия не заменяют YouTube Studio |
| Official runtime script gate/approval | **FAIL / not registered** | **FAIL / not registered** | **FAIL / not registered** | `ytv start` ENOENT, no run/lease; approval not requested or inferred |

Авторские проходы: исходный review 02m/05m сохранён; отдельная 10m переработка на новом hash привязала сюжет к найденному дедлайн-компромиссу, повторно проверила все показанные расчёты и смысловой перевод. Число авторских правок не равно independent review. Для любого изменённого hash требуется свежая независимая проверка; до неё текст лишь EDITORIAL_CANDIDATE_UNREGISTERED. Речевой Long loop N_A; actual TTS, voice speed, AV и права UNVERIFIED.

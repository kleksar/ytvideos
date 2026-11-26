# Story-review — six exact versions, eight editorial criteria

**Status:** EDITORIAL_CANDIDATE_UNREGISTERED. **Автор:** GPT-6, редакционный анализ 2026-11-17; уверенность в вычислениях высокая (при допущениях модели), в художественной оценке средняя, в спросе низкая. Независимый reviewer не запускался, второй самостоятельной сессии не было; `ytv-script-review-v1` и `ytv start` отсутствуют. Цифровые оценки ниже — мнение автора, не измеренная вероятность удержания/CTR. Независимый reviewer вправе отклонить даже 02m.

## Inventory: exact remote UTF-8, SHA-256 and estimated lengths

| Exact edition | Full EN SHA-256 / count | Full RU SHA-256 / count | Целевое время и фактическая оценка |
|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) — `cfd506c42e7f8c3fc2db1e0c8d1e7a2eaf55e22387ff5d7c82f0227d0c4114ad` **292 words** | [RU](variants/02m/script.ru.txt) — `f4ef1888ad8717ccc72400f76c173c8df4bd07ef4441d4b827361ec077692d9a` **243 words** | @140–165 EN wpm 1:46–2:05 без пауз; с паузами может превысить 2m |
| 05m | [EN](variants/05m/script.en.txt) — `261ea8a3e4a740b3c532e25acb81ac54ab9dbdef8d7f2f73d6c0effe44d0de26` **893 words** | [RU](variants/05m/script.ru.txt) — `6fb5a177be51dfaff743b3a9f044ade556b0187f14fe661f389baff9db9a0908` **708 words** | @140–165 EN wpm 5:25–6:23 без пауз: требует сокращения под строго 5m |
| 10m | [EN](variants/10m/script.en.txt) — `6ebc8a51b21b0384bad327f1551b15fd00e5ee2fc8f1611e10bcb3356e301eb7` **1852 words** | [RU](variants/10m/script.ru.txt) — `6c866c6b95795aa5c32748d26eca76b5f63c1de056b9ae8da43e7ecedc87f7f6` **1508 words** | @140–165 EN wpm 11:13–13:14 без пауз: REWORK для 10m |

RU оценивается ориентировочно @120–145 words/min, зависит от числа длинных слов и пауз. **Реального TTS и измеренного времени нет**. Время на выбор A/B и финальное действие добавит паузы; не ускорять утверждённый voice ради укладывания. Все пары — полные самостоятельные истории, не сокращённые синопсисы, но хронометраж версий 05m/10m **не выдерживает строгую целевую минутность**.

## Eight criteria, six separate exact texts

`I` интерес/значимость; `O` начало; `D` развитие; `P` payoff; `F` свежесть угла; `V` визуальная выразительность; `S` естественность и понятность произнесения; `M` подтверждённый спрос. Все значения 1–10 — только авторская оценка; `M=UNVERIFIED` во всех шести строках. Индивидуальная confidence medium, математические числа отдельно проверены.

| Exact text | I | O | D | P | F | V | S | M | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 02m EN | 8 | 8 | 8 | 9 | 8 | 8 | 8 | UNVERIFIED | **STRONG_CANDIDATE** / recommended editorial |
| 02m RU | 8 | 8 | 8 | 9 | 8 | 8 | 8 | UNVERIFIED | **STRONG_CANDIDATE** / editor translation |
| 05m EN | 8 | 8 | 9 | 9 | 8 | 8 | 8 | UNVERIFIED | **STRONG_CANDIDATE** (content; timing REWORK) |
| 05m RU | 8 | 8 | 9 | 9 | 8 | 8 | 8 | UNVERIFIED | **STRONG_CANDIDATE** (content; timing REWORK) |
| 10m EN | 8 | 8 | 7 | 8 | 7 | 8 | 7 | UNVERIFIED | **REWORK** |
| 10m RU | 8 | 8 | 7 | 8 | 7 | 8 | 7 | UNVERIFIED | **REWORK** |

**Обоснования по каждой точной языковой редакции**, включая недостаток, а не общая оценка темы:

- **02m EN:** I=8: узнаваемое “three messy rooms”; O=8: сразу “Do I finish one room… or do the same job”; D=8: A/B 14→4 switches, затем отдельный deadline; P=9: “twenty-two minutes sixteen seconds” vs “eighteen minutes twenty seconds”, плюс flip on five seconds; F=8: считать transitions, а не только шаги; V=8: пять полос задач и три двери; S=8: обычные “clear / dust / wipe / vacuum / mop” и короткая развязка; M=UNVERIFIED, Reddit не подтверждает спрос. **Недостаток:** два численных поворота могут звучать как формулы без наглядной графики, слабый literal seam.
- **02m RU:** I=8: «три неубранные комнаты» без контекста; O=8: прямой выбор «Выбирай A или B»; D=8: «четырнадцать раз меняю занятие» против четырёх, гость меняет метрику; P=9: «на восемнадцать минут двадцать секунд» и «через семь минут» дают два завершённых ответа; F=8: неочевидная стоимость переключения; V=8: тот же коридор с чистыми состояниями; S=8: разговорные глаголы без ложных опытов; M=UNVERIFIED. **Недостаток:** числовую плотность перевод сохраняет, а spoken timing не измерен.
- **05m EN:** I=8: весь дом против одной готовой комнаты; O=8: “one gets the whole place ready nearly four minutes earlier” — явное обещание; D=9: прозрачное повторение **того же** объёма работ и обход в обратном направлении до suspense over early guest; P=9: полностью посчитаны two finish criteria and 6.4s threshold; F=8: изменение цели, а не постфактум победителя; V=8: траектория тележки читается по маршрутам; S=8: “Nothing got cleaned faster” просто отделяет work и overhead; M=UNVERIFIED. **Недостаток:** середина перегружена объяснениями и 893 слова часто больше пяти минут.
- **05m RU:** I=8: спор о начале/конце уборки; O=8: «какой» сохраняет интригу без ложной ставки; D=9: “одна тележка” / «четырнадцать» / «четыре» → подробный честный расчёт → «гость»; P=9: «первый полезный результат раньше» и порог 6.4s выполняют обещание; F=8: не банальная рекомендация; V=8: в обратных проходах естественная последовательность; S=8: «Саму уборку я не ускорял» ясная бытовая речь; M=UNVERIFIED. **Недостаток:** долгая арифметика и неподключённый Long делают это только редакционной редакцией.
- **10m EN:** I=8: три вопроса в начале; O=8: обещает method, bottleneck, guest; D=7: после основного payoff длинные эпизоды про 80m corridor and four rooms слабо повышают ставки; P=8: “The answer decides the method” возвращает к задаче; F=7: повторяет уже объяснённый механизм на новых параметрах; V=8: смена геометрии и этажности пригодна для original visuals; S=7: слишком много spoken arithmetic and caveats; M=UNVERIFIED. **Недостаток:** ~11–13 минут без пауз, пояснительный хвост снижает интерес.
- **10m RU:** I=8: «что важнее — короткий маршрут или меньше переключений»; O=8: три тематических вопроса; D=7: «Если комнат четыре…» не меняет центральную цель; P=8: возвращение к двум итоговым метрикам; F=7: общее правило повторяется; V=8: карта коридора и последовательные изменения; S=7: многословная инструкция по проверке реального опыта после уже состоявшейся развязки; M=UNVERIFIED. **Недостаток:** нуждается в крупном сокращении, иначе название 10m нечестно.

Для обеих STRONG_CANDIDATE по художественному содержанию **I/D/P ≥8** с основаниями выше, но это **не** PASS format/reviewer/loop. Ни среднее восьми, ни название версии не прячут отклонение времени.

## Story maps and exact openings / payoff / endings

| Version | Hook/first event | Development/changed expectation | Climax + completed answer | Closure / weakness |
|---|---|---|---|---|
| 02m EN/RU | “I have three messy rooms to clean” / «Передо мной три неубранные комнаты»; выбрать A/B | От 16m ходьбы к 80m, цена switching меняет победителя | Total A 22:16, B 18:20; 8m guest A 7:00, B 16:04; 5s switching A 16:26 vs B 16:40 | “Next Saturday, I open that same door again” / «В следующую субботу я опять открываю ту же дверь» → новая итерация уборки; **это пока может звучать как новый старт, не доказанная смысловая петля** |
| 05m EN/RU | “I need to clean three rooms” / «Мне надо убрать три комнаты» + какая схема быстрее? | Смена оборудования vs путь и обратные проходы, ранняя комната, отдельная стоимость смены | Total B wins, first room A wins, threshold 6.4s | Чёткое условное решение, без обязательной Long-петли; середина может затянуться |
| 10m EN/RU | Три вопроса обещают весь дом и одну раннюю комнату | Метод подробно разбирает 14/4 переключения, контрфакт 5s, geometry 80m, four-room scaling | Центральный ответ до дополнительных проверок; итог повторяет цель vs overhead | Пояснения и предложенный protocol после кульминации — лишний справочный хвост |

**02m cold start:** первая строка сама объясняет задачу; кульминация/практический вывод даны до возврата двери. **Seam EN literal:** “Next Saturday, I open that same door again. I have three messy rooms to clean.” **Seam RU literal:** «В следующую субботу я опять открываю ту же дверь. Передо мной три неубранные комнаты». Авторский отрицательный тест: новая суббота и повторение сцены дают смысловую связь, но это *скорее новый эпизод, чем непрерывное предложение*; проверка full two cycles настоящим независимым читателем **UNVERIFIED**. Ни точный AV seam, ни скорость озвучки не известны. Не переносить эту авторскую идею как обязательный literal PASS. Long `narrative_loop=N_A`.

**Owner policy long opening:** 05m содержит короткое открывающее обещание и один вопрос, затем погружение и расчёт; это редакционная форма, требующая independent first-listener check, а не заранее утверждённый script gate. 10m содержит явные три вопроса. **EN/RU:** семантическая пара сохраняет количества комнат, метры, switching, оба результата и существенные оговорки; авторская текстовая сверка, independent UNVERIFIED.

## Checks / review state for each edition

| Check | 02m | 05m | 10m |
|---|---|---|---|
| Model arithmetic (author recomputation + transparent reproducible equations in research) | PASS for **toy only** | PASS for **toy only** | PASS for **toy only**, additional scenarios |
| Research / empirical universality | UNVERIFIED: switching costs assumed | UNVERIFIED: no empirical measurements | UNVERIFIED: no empirical measurements |
| EN/RU meaning pair | PASS author text inspection; independent UNVERIFIED | PASS author text inspection; independent UNVERIFIED | PASS author text inspection; independent UNVERIFIED |
| Format / target duration | **FAIL production**: 35–50s Short target exceeded; actual TTS UNVERIFIED | **FAIL production**: no Long recipe, text likely 5m+ | **FAIL production**: no Long recipe, 10m target missed |
| Literal Short narrative loop | **UNVERIFIED**, plausible thematic reset but risk of restart | N_A Long | N_A Long |
| Media/third-party rights | UNVERIFIED, original images not yet produced | UNVERIFIED | UNVERIFIED |
| Independent reviewer | **UNVERIFIED**, no session | **UNVERIFIED** | **UNVERIFIED** |
| Demand, CTR, retention | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** |

No official `uv run ytv start`, `plan_summary`, `read_next`, pinned `task_guide`, `ytv-script-review-v1`, claim/lease, receipt, approved script or measured TTS/MP4. Self-review **does not count** as independent. **Author revisions:** first original composition plus one author-only verification pass (math and EN/RU); no fabricated reviewer iteration.

## Comparison and recommendation

| Gain | Concrete new understanding | Where attention is at risk |
|---|---|---|
| 2 → 5 | Sequence of fourteen changes shown instead of asserted, same-first-room timing explained, 6.4s crossing derived rather than just reported | Over-explaining switching before the final payoff, 893 EN words too long |
| 5 → 10 | Very long hallway scenario and four-room variant demonstrate limits of generalization, plus reproducible design of hypothetical real test | Audience already knows winner and mechanism; 80m corridor is contrived; 1852 EN words beyond ten-minute target |

**Recommendation: 02m editorial only** — clearest complete question and conditional payoff, smaller dilution of stakes. **Substantial objections:** 02m still doesn't fit active Short profile; its prose seam looks like a restart, not independently verified; central effect is model-selected. Reviewer could reject whole concept, and that is acceptable. Five and ten minutes remain self-contained alternatives, not automations of an unsupported Long production. Detailed storyboard/prompts MUST NOT proceed until exact chosen hash is independently reviewed and allowed; don't invent reference images.

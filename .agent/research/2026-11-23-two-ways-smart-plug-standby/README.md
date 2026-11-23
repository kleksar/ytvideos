EDITORIAL_CANDIDATE_UNREGISTERED

# Two Ways Lab — Can a Smart Plug Waste More Power Than It Saves?

**RU логлайн.** Я хочу уменьшить расход электричества и ставлю умную розетку перед телевизором. Но она сама тратит энергию: в честной условной модели телевизор в ожидании расходует **6 Вт·ч** за день, а розетка — **17,6 Вт·ч**, увеличивая расход на **11,6 Вт·ч**. Когда я заранее заменяю прибор на старый ресивер с другим расходом в ожидании, победитель меняется: розетка экономит **142,4 Вт·ч/день**. **Это прозрачная модель, не измерение реальной квартиры.**

| Самостоятельный вариант | Полный RU | Full English production narration | Редакционный статус |
|---|---|---|---|
| **2m / Short editorial** | **[RU](variants/02m/script.ru.txt)** | **[EN](variants/02m/script.en.txt)** | **STRONG_CANDIDATE — рекомендована**, но ~2m не совпадает с обычным 35–50s Short |
| 5m / proposed Long | [RU](variants/05m/script.ru.txt) | [EN](variants/05m/script.en.txt) | STRONG_CANDIDATE, **Long production BLOCKED** |
| 10m / proposed Long | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | REWORK — перегрузка после развязки, **Long production BLOCKED** |

**Почему 2m:** зритель успевает выбрать A/B, увидеть полный обратный эффект, честное изменение победителя и практический критерий — реальный расход прибора в ожидании против собственных затрат контроллера. В 5m добавляются обоснование границы **0,88 W** и экономическая цена решения. В 10m есть новые расчёты времени работы и мощности самой розетки, но плотность и время не окупают их для массового зрителя. Не удлинять/ускорять ради квоты. Ни один вариант не получает официального производства автоматически.

Supporting artifacts: [research.md](research.md) (12 screened directions, three finalists, demand/source limits and fixed model), [story-review.md](story-review.md) (eight criteria per exact edition, six hashes, author-only QA), [packaging-brief.md](packaging-brief.md) (honest titles/thumbnail/first action/payoff), [handoff.md](handoff.md) (main SHA, runtime blockade, approved migration route).

**Current blockers:** no genuine `uv run ytv start` (executable `ytv` absent), no independent reviewer or approval; Short ~2m exceeds channel's ordinary 35–50s target; ChannelSpec Long canvas/fps unresolved; TTS, exact media/reference bytes, actual voice duration, rights and AV loop **UNVERIFIED**. Neither README nor passing CI is a script gate. No TTS, image generation, MP4, upload/publication, scheduling, changing general docs/skills or merging authorized.
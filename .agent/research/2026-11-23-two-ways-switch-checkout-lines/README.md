EDITORIAL_CANDIDATE_UNREGISTERED

# Two Ways Lab — The Other Checkout Line Moved First. Should I Switch?

**RU логлайн.** Я стою у кассы за двумя покупателями, у соседней — четыре, но там уже обслужили первого, а моя очередь ещё не двинулась. Перехожу ли я? В одной объявленной математической модели переход задерживает меня на десять секунд (**3:25 против 3:15**); если заранее добавить отдельную 25-секундную проверку цены, переход выигрывает пятнадцать (**3:25 против 3:40**). Это две воспроизводимые условные ситуации, **не замеры в магазине и не универсальное правило**.

| Самостоятельная редакция | Полный русский | Full English production narration | Авторский статус |
|---|---|---|---|
| **02m / Short editorial** | **[RU](variants/02m/script.ru.txt)** | **[EN](variants/02m/script.en.txt)** | **STRONG_CANDIDATE — рекомендована редакционно**; Short 35–50s target mismatch, independent review UNVERIFIED |
| 05m / proposed Long | [RU](variants/05m/script.ru.txt) | [EN](variants/05m/script.en.txt) | STRONG_CANDIDATE, **Long production BLOCKED** |
| 10m / proposed Long | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | REWORK: complex probability/arrival sensitivity; **Long production BLOCKED** |

**Почему 02m:** в ней уже полностью раскрыты выбор, неожиданный исход, явная смена победителя при изменении одного условия и вывод о *оставшейся работе* вместо того, кто первым закончил. 05m добавляет реальную ценность: пересечение времени ходьбы с ожиданием, порог ничьей 10 секунд и более ясный контроль условий. 10m добавляет расчёт вымышленной вероятности, дедлайн и нового покупателя, но ослабляет темп. Не удлинять сценарий ради производственной квоты. Production format отдельно от длительности.

| Supporting evidence | What it covers |
|---|---|
| [research.md](research.md) | 12 направлений, три финалиста, реальные источники зрительских вопросов/сопоставимых YouTube-видео и ограниченные данные; точные правила, все входы и арифметика модели |
| [story-review.md](story-review.md) | По восемь отдельных оценок автора на каждый exact текст, главный недостаток, сравнение 2/5/10, SHA-256 шести EN/RU, self QA и UNVERIFIED независимый review |
| [packaging-brief.md](packaging-brief.md) | Честные заголовки, первый кадр и вопрос A/B, payoff, концепт обложки и ограничения перехода к релевантному видео |
| [handoff.md](handoff.md) | Source main, merged status #124, original/revised text identity, доступные capabilities, blockers и локальный путь продолжения |

**Actual environment:** `uv run ytv start` returned `Failed to spawn: ytv — No such file or directory (os error 2)`. No active ytv run, approved script, independent reviewer, first-listener receipt, voice, hero visual reference bytes, media, rendered MP4 or publisher action. Git-only editorial exception is not an official script gate. Short 2m exceeds the current 35–50s target; ChannelSpec Long is unresolved.

The text is a self-contained original model, not derived from a YouTube transcription. Public video pages were **not watched or listened to**. Demand/CTR/retention, actual spoken durations and the visual/audio loop are **UNVERIFIED**.

**Never merge on an author's evaluation alone.** Keep this Draft until exact one-version owner choice, runtime registration/import, independent review and format feasibility; no changes to other PRs, shared rules, provider assets or channel schedules.

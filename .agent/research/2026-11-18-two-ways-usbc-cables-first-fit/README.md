EDITORIAL_CANDIDATE_UNREGISTERED

# Two Ways Lab — Four cables. The monitor still stayed black.

**Логлайн:** я раздаю четыре разных USB-C кабеля четырём устройствам. Если первым подключить телефон и каждый раз брать первый подходящий провод, монитор останется без видео — работают только три устройства. Если начать с самого ограниченного устройства, заработают все четыре. Но стоит перевернуть порядок кабелей на столе, и оба способа дают четыре из четырёх. **Это воспроизводимая условная модель, не физический эксперимент или измерение скорости.**

| Цель | Полный RU | Full EN (future voice master) | Авторский статус / формат |
|---|---|---|---|
| **2 минуты** | [script.ru.txt](variants/02m/script.ru.txt) | [script.en.txt](variants/02m/script.en.txt) | **STRONG_CANDIDATE**, но 313 EN слов несовместимы с текущим ориентиром Short 35–50s |
| **5 минут** | **[script.ru.txt](variants/05m/script.ru.txt)** | **[script.en.txt](variants/05m/script.en.txt)** | **STRONG_CANDIDATE — рекомендована редакционно**; Long-рецепт в ChannelSpec не определён |
| **10 минут** | [script.ru.txt](variants/10m/script.ru.txt) | [script.en.txt](variants/10m/script.en.txt) | **REWORK**: полный текст, но поздняя часть учебная и затянута, Long не поддерживается |

**Почему пять минут:** в короткой версии есть тёмный экран, два честных прогона и полный результат, но почти нет времени на возражения. В пяти минутах дополнительно раскрыто, что A можно исправить перестановкой после оценки, затем изменён *порядок кабелей*, и A также получает 4/4; отсутствующий видеокабель не может заменить ни один алгоритм. Десять минут добавляют объяснения портов и границ стратегии, но после основного payoff появляется длинный справочный хвост. Качество этого выбора — **суждение автора**, а не measured retention.

- [Shared research: десять разных кандидатов, три финалиста, честные альтернативы, открытые фактические источники и YouTube metadata](research.md).
- [Story review: восемь отдельных критериев каждой из трёх законченных редакций, шесть SHA-256, точные результаты модели, сравнение, blockers](story-review.md).
- [Packaging brief: заголовок, первый кадр, A/B выбор, честная отдача, правила будущего визуального производства](packaging-brief.md).
- [Handoff: исходный remote main, pin policy, миграция и точные оставшиеся зависимости](handoff.md).

**Публичные сигналы:** объяснения USB-C у x-kom (2026-06-23) и Les Tests de Cyril (2026-06-30) подтверждают, что тему объясняют разные авторы; *не* подтверждают спрос на именно нашу A/B-схему. Native comments, creator baselines, CTR, retention, актуальный темп просмотров и собственная аналитика **UNVERIFIED**. Авторский review не является независимым.

**Ограничения исполнения:** Git-only editorial candidate. В доступном GitHub окружении отсутствуют подключённые локальные `uv run ytv start`, сохранённый `plan_summary/read_next/task_guide/pinned reference_documents` и отдельная независимая reviewer session (`sessions.independent`). Не создан run/lease, нет script-gate receipt или owner approval. Точный перенос описан в handoff. Не делали detailed storyboard/prompts, TTS, image/video generation, MP4, release, scheduling или merge. Общие docs/skills/channel profiles не менялись.

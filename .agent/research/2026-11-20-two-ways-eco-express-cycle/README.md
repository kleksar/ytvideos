EDITORIAL_CANDIDATE_UNREGISTERED

# Two Ways Lab — the one-hour cycle that uses more electricity

**RU логлайн:** я выбираю между часовой и 3:35-часовой программами одной посудомойки. В опубликованной таблице для этой Bosch быстрый цикл расходует вдвое больше электричества. Но если чистые тарелки нужны через час, победитель по практической задаче меняется. Это сравнение данных, **не** снятый физический эксперимент.

| Одна история | Full English | Полный русский | Редакционная классификация |
|---|---|---|---|
| **02m — рекомендована** | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | **STRONG_CANDIDATE**, Short editorial; фактический хронометраж и AV loop UNVERIFIED |
| 05m | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | STRONG_CANDIDATE, Long production blocker |
| 10m | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | REWORK: избыточные объяснения, Long production blocker |

**Рекомендация — 2 минуты**, не потому что у длинных текстов меньше слов, а потому что за эту редакцию зритель уже узнаёт две разные цены быстрого режима: электричество и время; цифры привязаны к конкретной модели, качество мытья не выдумано. Длительность оценена по словам, не измерена TTS. Конкретная Short-петля в тексте — только авторская проверка, независимое чтение и AV стык **UNVERIFIED**.

**Что в пакете:** [единое исследование, первоисточники, реальные вопросы и сравнение финалистов](research.md), [индивидуальные восемь оценок каждой редакции, SHA-256 и блокеры](story-review.md), [упаковка](packaging-brief.md), [handoff](handoff.md). Все шесть файлов — самостоятельные законченные narration, а не планы или обрезки.

**Непосредственный blocker:** нет исполняемого `ytv` в текущей среде (`uv run ytv start` → `Failed to spawn: ytv / No such file or directory`); независимая сессия reviewer с `sessions.independent` не обнаружена. Это разрешённая **редакционная Git-only очередь**, а не официальный run, script gate или production approval. Для двухминутного Short отдельная неопределённость: профиль канала ориентирован на 35–50 секунд. Для 05m/10m Long-рецепт отсутствует. Не создавать ложный Long run, не менять профиль.

**Git baseline:** новый сюжет от remote `main` `ea314fc36a798ded8d8ec684085e5a4c3aca80aa` (before-write recheck documented in handoff if changed); #124 merged and canonical editorial policy is main. No shared docs/skills/channel status edits. No paid providers, TTS, images, MP4, upload or publication.

**Continue locally:** In an actual repository checkout with CLI and independent reviewer, use `uv run ytv start --channel two_ways_lab --format short --intent 'Evaluate editorial candidate: Eco vs Express on one Bosch dishwasher'`; read `plan_summary`, `read_next`, `task_guide` and pinned documents; transfer exact six texts/research/review with hashes, arrange independent cold EN and RU reading and (for Short) two full cycles, then owner chooses one exact script. Later stages only by runtime permissions. Nothing here constitutes approval.

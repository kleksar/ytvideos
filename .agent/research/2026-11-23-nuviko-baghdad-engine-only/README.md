EDITORIAL_CANDIDATE_UNREGISTERED

# Nuviko History — The Missile Took Every Flight Control. They Still Landed.

**Логлайн:** В ноябре 2003 года ракета вывела из строя управление Airbus A300 над Багдадом. Экипаж из трёх человек научился менять высоту и направление одной лишь тягой двух двигателей, перенёс заход на соседнюю полосу и выжил после выката на песок.

| Длительность | Полный English production script | Полный русский смысловой перевод | Редакторский результат |
|---|---|---|---|
| 2 минуты | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | REWORK — spoken seam |
| **5 минут** | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | **STRONG_CANDIDATE — рекомендована** |
| 10 минут | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | REWORK — narration density |

**Рекомендация: 5 минут**, illustrated Long 16:9. Новые причинные решения (тяга вместо рулей, топливо, шасси, соседняя полоса, финальная коррекция) оправдывают более полное повествование. Десятиминутная редакция добавляет реальные детали, но сильнее рискует задержать зрителя техническим разбором. Двухминутная даёт весь результат, однако требует исправления речевой петли.

[Research](research.md) · [Exact SHA-256 and separate eight-criterion reviews](story-review.md) · [Packaging](packaging-brief.md) · [Handoff](handoff.md).

**Runtime blocked:** exact `uv run ytv start --channel nuviko_history --format short --intent 'Editorial scenario: 2003 Baghdad DHL A300 missile damage and thrust-only landing'` attempted here; result: `Failed to spawn: ytv; No such file or directory (os error 2)`. This is a permitted **Git-only editorial candidate**, not a registered run, lease, reviewer receipt or official script gate. No TTS, image generation, MP4, upload, release or merge. Reviewer independent reading and script owner approval: UNVERIFIED.

**Local transfer:** in an authorized repository/runtime run `uv sync --locked` then `uv run ytv start --channel nuviko_history --format long --intent 'Use proposed 05m editorial candidate after owner selection'`; read `plan_summary`, `read_next`, pinned `task_guide` and `reference_documents`, then attach the six exact files and `story-review.md` with canonical `attach-artifact` commands. If the owner explicitly accepts one full source for production, use `start --source-script variants/05m/script.en.txt` plus the genuine source-import/approval event described in workflow, without pretending prior review. Any changed master requires new hash/review. No old pins may be substituted.

Other blockers: independent fresh reader not available; exact voice timing, visual reference PNG bytes and rights, source video and end-screen target not verified. All figures/date/crew claims grounded in source map; visual footage not obtained.

EDITORIAL_CANDIDATE_UNREGISTERED

# Two Ways Lab — One Microwave. Four Lunches. Who Goes First?

**Логлайн (RU):** у меня одна микроволновка и четыре обеда. Пропускать короткие разогревы вперёд сокращает среднее время до еды с **12:45 до 6:00**, но обладатель долгого обеда может опоздать на собственный перерыв. Одни и те же 15 минут работы, разные человеческие последствия. Это **модель с условными входами**, а не реальный эксперимент.

| Редакция одной истории | Полный русский | Full English (narration) | Редакторский статус / формат |
|---|---|---|---|
| **2 минуты** | [02m RU](variants/02m/script.ru.txt) | [02m EN](variants/02m/script.en.txt) | **STRONG_CANDIDATE — recommended**; intended 9:16 Short, превышает обычный канальный ориентир 35–50s |
| 5 минут | [05m RU](variants/05m/script.ru.txt) | [05m EN](variants/05m/script.en.txt) | STRONG_CANDIDATE как текст, но **Long production BLOCKED** |
| 10 минут | [10m RU](variants/10m/script.ru.txt) | [10m EN](variants/10m/script.en.txt) | **REVISED_CANDIDATE**: новый t11 компромисс и t10 порог; **Long production BLOCKED** |

В каждой папке самостоятельный **полный** сценарий, не обрезок одной master-версии. [Research](research.md): 11 направлений, три финалиста, открытые Reddit-обсуждения общей микроволновки, YouTube-контрсигналы, модель и воспроизводимая арифметика. [Story review](story-review.md): отдельные 8 критериев для каждой версии, SHA-256 всех шести текстов и точные ограничения. [Packaging brief](packaging-brief.md): обещание/первый кадр/развязка без придуманных медиа. [Handoff](handoff.md): перенос, source revision, блокеры.

**Почему 2 минуты:** в одном сценарии есть самостоятельная развязка, правильный расчёт и человеческая оговорка. На 5m добавлен механизм двух переставленных обедов; переработанная 10m теперь проверяет новый рассчитанный компромисс **1,10,2,2 → average 10:00 при дедлайне L=t11** и изменение ответа при t10. Плотность расчётов всё ещё выше, поэтому 02m пока сильнее как рекомендация; независимое чтение UNVERIFIED. Подробный storyboard не готовился до независимого review (UNVERIFIED).

**Строгие границы:** `uv run ytv start` из этой среды ENOENT (`ytv` executable absent), официальный saved run и script gate не существуют. Независимого reviewer/его реального ответа нет. Спрос на именно этот формат, actual TTS/AV loop, права и производственный формат Short 2m — UNVERIFIED. Для Long у канала отсутствует определённый recipe/canvas/fps; редакционный текст не создаёт Long-разрешение. Никаких production/media/image/TTS/публикаций/merge; Draft PR не означает approval.

**10m rework:** initial baseline EN `d05d81d6b227d656d68a1604ca8b03eaeef89f3a9a56ca206eb92d9164847aa7` / RU `24fe042ebe5d3e415cebc8b9c343365ffcc87e77d86964b77df1e73764fcd30b` (Git `bc2eab7`) → revised EN `f98abbbe029e160c4e704e792e47aaf7f171fa5889cd39124d39f7fd7325eedc` (1425 words) / RU `37fbdb60e69952a8cd3fd8eb91f63db56bfdc2b2db7c11c93593f84a9ab13727` (1159 words). Original 02m/05m are unchanged. Arithmetic, status and variant-specific evidence in [story-review.md](story-review.md); no storyboard was transferred to the new text.

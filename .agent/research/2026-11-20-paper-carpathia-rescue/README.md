EDITORIAL_CANDIDATE_UNREGISTERED

# Paper Detour — Carpathia: The Rescue Began Before the Ship Arrived

**RU логлайн:** Когда «Титаник» уже тонул, капитан «Карпатии» развернул собственный пароход к опасным льдам. Пока он спешил к месту бедствия, команда готовила врачей, горячую еду, трапы и приспособления для подъёма детей. Лайнер к их прибытию уже затонул, но более семисот человек ещё оставались в шлюпках.

| Версия одной истории | Полный русский review | Full English production narration | Редакционный статус |
|---|---|---|---|
| 2 минуты / Short | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | REWORK — неоднозначный повтор вопроса в loop |
| **5 минут / Long** | **[RU](variants/05m/script.ru.txt)** | **[EN](variants/05m/script.en.txt)** | **STRONG_CANDIDATE — рекомендуется** |
| 10 минут / Long | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | REWORK — лишний второй кульминационный эпизод |

**Почему 05m:** 2m завершён по сюжету, но возвращает уже раскрытый вопрос в последней реплике. 05m даёт новое развитие: как большой пароход готовился принять людей из качающихся шлюпок, чего стоило добраться среди льда, и что пришлось делать после спасения. 10m добавляет подтверждённую судьбу «Карпатии» в 1918 году, но теряет цельность и темп после спасения. Рекомендация редакционная, **не выбор владельца/approval**.

[Общее исследование и сравнение 11 кандидатов](research.md) · [Точные отдельные оценки EN/RU и SHA-256](story-review.md) · [Обложка/первые события/payoff](packaging-brief.md) · [Handoff и blockers](handoff.md).

**Сильнейшая альтернатива:** Lake Peigneur (1980), когда озеро обрушилось в соляную шахту — мощнее визуально, но причина обвала оспаривалась, а зрительская ценность длинной версии менее подтверждена.

**Контрсигнал:** почти все знают «Титаник» и истории его спасения, многие документальные видео конкурируют за тот же поисковый запрос. Доступны только индексированные YouTube-карточки, не просмотры/транскрипты/комментарии. Текущий сопоставимый спрос, CTR, retention и baseline аналогичных небольших каналов — `UNVERIFIED`.

**Почему не зарегистрирован:** команда `uv run ytv start --channel paper_detour --format long --intent 'New candidate: Carpathia Titanic rescue, editorial only'` не смогла запустить `ytv` (`Failed to spawn: ytv; No such file or directory`) в доступном исполнении. Независимый reviewer также не запускался. Это Git-only редакционная очередь, не официальный script gate.

Source remote `main` `450f005793e94ad6ca889e0090befe7fcf4d75b1`; PR #124 уже merged и **документы main canonical**, proposed revision не импортирована. Только новая папка; не менять общие docs/skills, статус канала или старые pinned runs. Ни TTS, ни media, ни MP4, ни upload/publication, ни merge не выполнялись.

**Путь переноса:** в полном рабочем checkout выполнить реальный `uv run ytv start`, прочитать `plan_summary`/`read_next`/`task_guide`/`reference_documents` из зарегистрированного run; перенести через предусмотренные `attach-artifact --kind script_variant` (каждая редакция и перевод) и `--kind story_review` с exact `--source`, сохранить IDs/hashes; создать реальный независимый reading-input review **05m EN SHA-256 `0c89028a...`** до создания storyboard/производства; выбрать и утвердить только один master. Pins чужих runs не заменять.

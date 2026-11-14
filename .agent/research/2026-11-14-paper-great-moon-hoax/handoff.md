EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Handoff — Paper Detour · Great Moon Hoax (1835)

- Канал: `paper_detour`, ChannelSpec `active`, recipe `illustrated`, English narrative Short, 9:16, полный RU перевод отдельно.
- Стартовое состояние: remote main `cd749ac2559170bdbd761cb447683e1e88260556` (фактически перепроверенный перед записью; новый main после этого не подменяет provenance); текстовая кандидатская ветка от exact main commit.
- Источники, claims, uncertainty: `research.md`. Первичная история: 1835 газета, воспроизведённая в 1859 перепечатке Project Gutenberg. Историческая реконструкция событий 1835 и вымышленные утверждения самой The Sun явно разделены.
- Revision: одна авторская версия `script.en.txt` и однозначный смысловой `script.ru.txt`. Exact script source будущего TTS/SRT — EN. Продолжать работу после изменения source только с новым review и синхронизированным storyboard; нет предыдущего accepted narration или measured timings для переноса.
- Storyboard: `storyboard.md`, 15 предварительных бумажных диорам, exact сценовые spans, 4–6 секунд только ориентир. Real image refs, реальные pixels эталонов Paper и plane, TTS, actual word timestamps, music, CI, AV seam — не подтверждены.
- Scope этой заготовки: текстовые материалы и Draft PR. Нет разрешений на merge, imagegen, TTS, rendering, upload, publishing, смену статуса канала.

## Точный локальный путь перехода в официальный workflow

1. На действительно исполняемом локальном host проверить свежий `origin/main`, открыть этот Draft PR и прочитать полный EN/RU, research и diff; без автоматического merge.
2. До открытия нового production run: `uv run ytv start --channel paper_detour --format short --intent 'Разработать сценарий по редакционному кандидату Great Moon Hoax (1835); без производства и публикации'`. Получить реальный `plan_summary`, `read_next`, `task_guide` и каждый pinned `reference_documents`; сохранить реальные IDs, если host их выдаст. Никаких IDs в этом PR не присваивается.
3. Пронести именно эти файлы как research/script inputs через выданный штатный task output и сохранить exact EN SHA256. Не превращать эту ветку в источник authorization/approved script.
4. Доступный настоящий `sessions.independent` или разрешённый независимый host: оригинальный `ytv-script-review-v1` на exact EN hash после двух полных чтений, без авторского вердикта в входном пакете; сложные замечания исправлять лишь с новой версией и новым reviewer result.
5. Только после реального script gate `awaiting_script_approval` показать точный EN текст и RU перевод владельцу; данное поручение **не** разрешает ни одобрение сценария от имени пользователя, ни медиа.

## Блокирующие capabilities в этой среде

- Нет подключённого исполняемого repo checkout/локального `uv run ytv` (локальная network Git clone невозможна; GitHub connector позволяет Git data, но не запуск команд и сохранение run).
- Native независимая новая сессия reviewer `sessions.independent` / `spawn_agent` / `collaboration.spawn_agent` не обнаружена среди доступных инструментов; author self review не заменяет независимость.
- Не разрешена генерация или проверка реального MP4. Script gate, independent attention, AI assets и AV seam = **UNVERIFIED**.

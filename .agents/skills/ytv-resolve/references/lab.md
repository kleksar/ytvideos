# Private Resolve lab: проверять, затем переносить

Читать при порученном обучении/прототипировании Fusion, Color, Fairlight или новом native методе. Lab — отдельный **never-publish** project/timeline, не канонический выпуск, не approval новых кадров/звука. Не ставить его в upload queue. Сохранить IDs, исходный project/timeline/page/playhead и вернуть прежний вид после разрешённого эксперимента, не закрывая чужую работу. Все mutations одного instance последовательны; prep вне приложения можно распараллеливать. Папка — существующий episode `Work`, без соседних Mac clones. [Общие ограничения](../SKILL.md) сохраняются.

## Перед первым узлом

- Проверить сценарную причинность, единую **master room layout**, масштаб/перспективу реквизита и места соединений. Нужны geometry-matched clean plate и alpha того же canvas, отмеченные относительный anchor, ground plane и contact shadow. Проверить alpha/premultiplication и перекрытия на фактических пикселях. Ошибку статичной картинки не исправляют camera move или grade; вернуть её в разрешённую подготовку assets, не маскировать движением.
- Проверять установленный официальный SDK/README и точные методы. Resolve timeline API и Fusion comp API — разные поверхности; наличие GUI-функции не доказывает setter. Не изобретать методы Color/Fairlight; недоступность отметить или использовать разрешённый UI в безопасное окно, без захвата мыши в фоне.
- Whole-shot editorial motion по [timeline](timeline.md)/visual: fit-relative crop, линейные реальные endpoints, static и tighter channel caps. Событие предмета может иметь собственную фазу/паузу; это не разрешение ease для монтажной камеры.

## Минимальный цикл доказательства

1. Записать одну гипотезу, исходники/hash, точный тестовый диапазон и критерий результата. Не менять approved master/mix глобально.
2. Выполнить изменение только в lab, снять read-back graph/keys/clip properties/markers, SaveProject и проверить сохранность повторным чтением, при разрешённом reopen — после reopen. При modal/ошибке остановить повторные мутации, сохранить наблюдение; не принимать `True` от API за готовую картинку.
3. Проверить начало/середину/конец и особые события, непрерывное воспроизведение, при порученном test export — exact bytes по [delivery QA](delivery.md). Listen обязателен для звукового результата. Graph/параметры доказывают редактируемость, не финальное качество.
4. Сохранить маленький recipe/manifest с prerequisites, фактическими API/версией, результатом и ограничениями. Переносить только проверенную часть; lab approval не разрешает публикацию или замену production timeline. Отменённую пробу не записывать как работающую автоматизацию.

## Подтверждённый опыт, не универсальные настройки

Ниже — отчёт выполнявшего Mac lab worker от 2026-11-19, не самостоятельный live-тест автора docs. Числа относятся к конкретному private Fix Anything lab.

| Область | Что подтверждено | Чего это не доказывает |
|---|---|---|
| Edit | 8 blue timeline chapter markers и 13 настоящих editable music keys | Автоперенос глав на YouTube или готовность финального mix |
| Fusion | Сохранён graph: background MediaIn + portable alpha EXR → Transform → Merge → MediaOut; 7 position checkpoints предмета, genuine Merge на frame 47 и alpha до frame 73 отдельно read back; editable graph сохранён. Старый V2 overlay отключён **только в sandbox**, чтобы не было двойного предмета | Проверенный planar tracking, все export frames или универсальная правка исходного арта |
| Loader recovery | Первая live PNG Loader-проба открыла modal; EXR pass с `comp.Lock()` прошёл | PNG всегда неисправен или Lock гарантированно лечит любой modal. Проверять методы lock/unlock текущего SDK, освобождать lock при завершении/ошибке и проверять сохранённый comp |
| Fairlight | Один отдельный FX20 cue сохранил gain −1.5 dB и pan −6 на своём точном времени | Готовые ducking/EQ/финальный mix; эти значения не defaults других SFX |
| Subtitles | `ImportMedia` принял approved SRT в Media Pool. Generic Append в populated timeline не соблюдал желаемую позицию; проба +178 s сдвинула все cues и была отменена | Native editable subtitle track automation **не завершена**; не повторять глобальный offset как исправление. Требование native track из timeline reference остаётся целью, пока не выполнены фактический placement/read-back/SRT round-trip |
| Color | Пока нет live proof | Не заявлять проверенный grade/group pipeline |

## Reference-only упражнения

Это варианты следующих **порученных** тестов, не выполненные рецепты и не обязательные эффекты каждого канала:

- [Fusion](https://www.blackmagicdesign.com/products/davinciresolve/fusion): planar tracker/corner pin для вставки на плоскость, 2D tracking или foreground mask. Сверять дрейф углов и окклюзию, сохранять editable graph. Сначала простая геометрия, не всё видео.
- [Color](https://www.blackmagicdesign.com/products/davinciresolve/color): Original/Test versions нескольких plates, group pre/post balance или shared nodes, scopes и визуальная сверка. Не менять единственную approved версию; shared node меняет все клипы, использующие этот shared node; group pre/post меняет участников Color Group.
- [Fairlight](https://www.blackmagicdesign.com/products/davinciresolve/fairlight): отдельные voice/music/Foley, clip gain/fade/keys; при проверке Ducker явно назначить dialogue source. Сравнивать bypass/test и слушать recovery, не нормализовать утверждённый mix автоматически.

Официальные страницы подтверждают продуктовые возможности, не доступность scripting API и не успешный тест в этой установке. Численные допуски конкретного эксперимента записывать как выбранные test targets, не требования Blackmagic.

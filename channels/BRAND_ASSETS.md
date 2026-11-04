# Канальные бренд-материалы в клоне

Этот перечень описывает, что новый клон получает автоматически и что требуется передать отдельным пакетом. Исторические материалы выпусков, экспортированные видео и монтажные сессии не подразумеваются доступными только потому, что есть их текстовые ссылки.

## Nuviko History

Включены два утверждённых пользователя персонажных референса в [`brand/References`](nuviko_history/brand/References/README.md): лист внешности/костюма и коллаж мимики v03. Их хеши и факт приёмки находятся в receipt рядом. Правила внешности — [`VISUAL_PROFILE.md`](nuviko_history/brand/VISUAL_PROFILE.md); монтажные размеры и цвета — [`nuviko.json`](../automation/ffmpeg_montage/profiles/nuviko.json), [`nuviko_short.json`](../automation/ffmpeg_montage/profiles/nuviko_short.json) и [`long.json`](../automation/ffmpeg_montage/profiles/long.json). Передавайте оба принятых PNG каждой генерации/правке с героем. Image generation не гарантирует одинаковые пиксели; для сохранения личности используйте одни и те же PNG и сверяйте результат вручную.

## Paper Detour

Включены текстовые стандарты типографики и обложек: [`TYPOGRAPHY_STANDARD.md`](paper_detour/brand/TYPOGRAPHY_STANDARD.md) и [`THUMBNAIL_PLAYBOOK.md`](paper_detour/brand/THUMBNAIL_PLAYBOOK.md), плюс [`FILM_REFERENCE_030.md`](paper_detour/brand/FILM_REFERENCE_030.md) с описанием принятого визуального примера и ссылкой на публичный выпуск. Профиль монтажа и титров — [`paper.json`](../automation/ffmpeg_montage/profiles/paper.json). Старые локальные примерные PNG из прошлых выпусков не включены; используйте текстовые стандарты и публичный пример, если он доступен.

## Шрифты и перенос между компьютерами

Файлы системных шрифтов в Git не распространяются. Профили монтажа сейчас ссылаются на шрифты macOS (`ChalkboardSE.ttc`, `Georgia Bold.ttf`); на Mac рендер ожидает эти системные шрифты. Их лицензия/наличие определяется ОС, а не этим репозиторием. На Windows/Linux абсолютные пути профилей не подходят: до монтажа потребуется установить и разрешённо использовать совместимый шрифт и локально настроить путь в профиле или renderer. Замена гарнитуры может изменить ширину и перенос текста.

## Третий канал «Нувико»

Для русскоязычного канала жизненных историй коллеги пока не задан отдельный visual profile и нет принятых brand references. Не переносите на него изображения Nuviko History, `channels/nuviko_history/`, Paper Detour или legacy `channels/nuviko_stories/` автоматически. Создайте отдельный профиль после получения его бренд-решений.

# Экспорт и YouTube delivery

## Локальный экспорт

Использовать native Deliver queue в существующем проекте только при порученном рендере. Сверить exact timeline/job, range, video/audio codec, geometry/fps, bitrate/channel/sample rate с [delivery](../../../../docs/standards/delivery.md) и профилем. Проверенная комбинация H.264/AAC не отменяет канальные параметры. Не рендерить другой открытый проект; дождаться job completion, не считать enqueue успехом.

Probe + полный decode итогового файла, длительность/число кадров, первый/средний/последний кадры планов и склейки, прослушивание sync/mix, alpha/captions/font/safe area. Screenshots viewer, track counts и отсутствие ошибок API не заменяют проверки exact MP4. Сохранить SHA-256, render settings, job result, sources/rights и QA. Передать exact export по обычному delivery workflow; не удалять единственные исходники.

## Resolve YouTube — пока проверяемая опция

Настройки **Internet Accounts** и YouTube Deliver существуют, но native upload end-to-end ещё не подтверждён. Первый тест разрешён только в scope порученного upload, на проверенный канал, с согласованной Private/Unlisted видимостью и read-back; не делать отдельный пробный дубль без поручения. Если авторизация/метод недоступны, использовать допустимый Studio handoff для того же файла, сначала reconcile попытку. Не обещать выигрыш скорости и не считать локальный render доказательством upload.

На пользовательском screenshot Deliver видны `Title`, `Description`, `Chapters from Markers` с выбором цвета, `Upload Thumbnail` с путём, `Privacy`, `Category`, vertical toggle. Это **UI evidence**, не подтверждение scripting setters, сохранения полей или capability конкретного аккаунта. Private в одном screenshot — состояние того экрана, не универсальная настройка. Прочитать текущий UI/settings, заполнить только известные поля и сверить, что thumbnail/media пути существуют. Chapters строить по фактическому монтажу, выбранному marker color и платформенным требованиям, не по раннему сценарию.

Применить [release standard](../../../../docs/standards/release.md) и [release skill](../../ytv-release-video/SKILL.md): exact MP4 approval и upload scope, identity канала, видимость и отсутствие дубликата обязательны. Перед повтором UNKNOWN проверить queue/YouTube по результату и ID. Не переключать/добавлять accounts, не менять ограничения канала ради обхода.

## Обязательный Studio read-back

После upload получить настоящий video ID/URL и проверить тот же канал, privacy, обработку/ограничения, metadata и фактическое отображение. Довести порученный release через Studio там, где Resolve не позволяет установить или проверить playlist, язык, audience, CC/SRT, tags, rights/restrictions, end screen либо Related video. Не объявлять эти поля готовыми по наличию общего YouTube preset.

Для Short Related video нужен доступ к advanced features, а цель должна быть доступным public/unlisted видео **этого канала**. Для long подготовить релевантный end screen в разрешённом scope и проверить его сохранение. Настоящий clickable end screen/Related video не заменяется рисунком или титром в MP4. Custom thumbnail также зависит от account eligibility; Resolve не обходит проверку YouTube. При блокировке сохранить точную причину/остаток работы, не заливать дубль и не изменять account. Статус «uploaded», «configured», «public» различать по фактическому read-back.

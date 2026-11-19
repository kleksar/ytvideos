# Экспорт и YouTube delivery

## Preferred native YouTube route (owner clarification, 2026-11-19)

For future videos across channels, prefer Deliver's built-in YouTube preset and Upload directly when the exact destination channel, visibility and required metadata can be verified. A preset is a starting point: retain the approved geometry/fps/audio contract and do not silently renormalize the mix. This preference is not upload authorization or evidence of successful native upload. The global initial Private visibility remains unchanged unless the owner explicitly authorizes another visibility for the named scope; [Vice Wreckroom](../../../../channels/vice_wreckroom/PROFILE.md) has its own narrow Unlisted requirement.

If the native route cannot verify destination, visibility, mandatory fields or completion, stop that upload, preserve job state and report the concrete blocker. Do not silently redirect to another account/tool or duplicate an UNKNOWN upload. Preserve all existing exact-file approval, rights, review and Studio read-back requirements below. Existing baked projects require scoped migration rather than a false claim of native reconstruction.


## Локальный экспорт

Использовать native Deliver queue в существующем проекте только при порученном рендере. Сверить exact timeline/job, range, video/audio codec, geometry/fps, bitrate/channel/sample rate с [delivery](../../../../docs/standards/delivery.md) и профилем. Проверенная комбинация H.264/AAC не отменяет канальные параметры. Не рендерить другой открытый проект; дождаться job completion, не считать enqueue успехом.

Если brief требует музыку с титульного начала, прослушать exact export с 0:00: музыка должна быть намеренно слышна, наличие waveform не является проверкой.

Probe + полный decode итогового файла, длительность/число кадров, первый/средний/последний кадры планов и склейки, прослушивание sync/mix, alpha/captions/font/safe area. Screenshots viewer, track counts и отсутствие ошибок API не заменяют проверки exact MP4. Сохранить SHA-256, render settings, job result, sources/rights и QA. Передать exact export по обычному delivery workflow; не удалять единственные исходники.

Для проверенного Short-пресета: **1080×1920, 30 fps, H.264/AAC**; остальные параметры взять из утверждённого выпуска/профиля и сверить read-back. Утверждённый mix **не нормализовать автоматически** и не включать новую loudness processing ради preset: любое изменение должно относиться к порученной правке и пройти повторное прослушивание. Это не перенос Short-пресета на Long или каналы с другой pixel policy.

## Цветные полосы и другие кратковременные дефекты

Успешный полный **software decode не доказывает визуальную чистоту**: декодер может корректно прочитать уже испорченные пиксели. Перед выдачей/upload проверить actual decoded frames и воспроизведение всего экспорта, включая короткие вставки, overlays, склейки и участки вне first/middle/last выборки. При замеченных полосах не объявлять причиной codec, GPU, YouTube или исходник без сравнения.

1. Зафиксировать exact local file/hash, соответствующий video ID (если уже загружен), таймкод/номер кадра, fps, разрешение и условия воспроизведения. Сравнить **тот же момент** в сохранённом timeline, локальном native master и доступной YouTube-версии после обработки; учесть смещение начала/частоту кадров, проверить соседние кадры. Screenshot одного плеера не устанавливает, где появился дефект.
2. Проверить соседние декодированные кадры по всей длительности, не только редкую выборку. При доступном анализе кадров искать кандидатов: кратковременные горизонтальные цветовые полосы, резкий chroma-сдвиг в узкой области строки относительно соседних строк и кадров. Это сигнал для визуальной проверки, не автоматический диагноз или универсальный порог: субтитры, границы панели, художественные вспышки и склейки могут дать ложное срабатывание. Проверить candidate frame плюс соседние кадры и отличить авторское событие от артефакта. Без такого анализа не заявлять, что автоматический детектор выполнен; один clean sample не исключает однокадровый дефект.
3. Сохранить утверждённый timeline/исходники. Сначала установить, чист ли **native master**. Если он чист, исследовать доставку/декодирование/платформенную версию, не пересобирать монтаж наугад. Если дефект в master, остановить выдачу этого export и локализовать источник/слой/рендер, сохранив evidence. До delivery-only encode проверить native intermediate на том же проблемном диапазоне и затем весь результат; не переносить дефект исходного render в новую упаковку. Чистый альтернативный export/транскод допустим только в порученном repair scope, после проверки его источника и всего результата; перекодирование грязного master не восстанавливает повреждённые пиксели. Не подменять Resolve-монтаж другим renderer молча.
4. Записать PASS/FAIL/UNVERIFIED и покрытие сравнения по каждому уровню. Недоступный timeline или YouTube read-back — конкретная граница проверки, не доказательство чистоты. **Не делать повторный upload лишь для теста**: сначала reconcile существующий ID/попытку, затем действовать только в разрешённом release/замене scope.

## Resolve YouTube — пока проверяемая опция

Настройки **Internet Accounts** и YouTube Deliver существуют, но native upload end-to-end ещё не подтверждён. Первый тест разрешён только в scope порученного upload, на проверенный канал, с согласованной Private/Unlisted видимостью и read-back; не делать отдельный пробный дубль без поручения. Если авторизация/метод недоступны, использовать допустимый Studio handoff для того же файла, сначала reconcile попытку. Не обещать выигрыш скорости и не считать локальный render доказательством upload.

На пользовательском screenshot Deliver видны `Title`, `Description`, `Chapters from Markers` с выбором цвета, `Upload Thumbnail` с путём, `Privacy`, `Category`, vertical toggle. Это **UI evidence**, не подтверждение scripting setters, сохранения полей или capability конкретного аккаунта. Private в одном screenshot — состояние того экрана, не универсальная настройка. Прочитать текущий UI/settings, заполнить только известные поля и сверить, что thumbnail/media пути существуют. Chapters строить по фактическому монтажу, выбранному marker color и платформенным требованиям, не по раннему сценарию.

Для порученного **Unlisted Short** явно выбрать и проверить Unlisted, не оставлять видимый Private по инерции. В этом Short-пресете `Chapters from Markers` выключен; chapter workflow длинного ролика не переносится автоматически на Short. Если нужное поле отсутствует или его значение нельзя прочитать, не имитировать успешную настройку: сохранить blocker и выполнить допустимый Studio follow-up для того же видео. Thumbnail path в Resolve не доказывает принятие обложки YouTube: проверить файл, eligibility и фактический thumbnail в Studio данного канала.

Применить [release standard](../../../../docs/standards/release.md) и [release skill](../../ytv-release-video/SKILL.md): exact MP4 approval и upload scope, identity канала, видимость и отсутствие дубликата обязательны. Перед повтором UNKNOWN проверить queue/YouTube по результату и ID. Не переключать/добавлять accounts, не менять ограничения канала ради обхода.

## Selectable captions и главы

Native subtitle track, burned text и selectable YouTube CC — разные результаты. Обычный MP4 и direct upload **не считаются передачей selectable captions** без проверки. Сохранить финальный timed EN SRT, а при порученном release загрузить его в язык субтитров соответствующего видео через Studio с режимом `With timing`, если автоматический перенос не подтверждён. Проверить сохранение/публикацию track и выбор языка/CC в плеере, сверить начало, середину и конец. Auto transcript не заменяет проверенный SRT; не запускать повторную TTS ради CC. Для явного иного языка использовать его track. Если уже есть burned captions, не включать второй видимый слой в самом MP4.

Для применимого Long использовать `Chapters from Markers` и exact chapter color только когда поле фактически доступно и прочитано в Deliver UI; не выдумывать API setter. После direct upload всё равно проверить результат в Studio/реальной полосе прогресса. Если перенос глав не подтверждён, вставить сохранённый список timestamp + title в description того же видео: начало **0:00**, минимум **3** возрастающих позиции, каждая глава минимум **10 s**, включая последнюю до конца. Проверить соответствие фактическому export и доступность функции каналу; не создавать искусственные главы в слишком коротком материале. Сохранённое описание ещё не доказывает появление глав в плеере. Shorts: chapter toggle off, без принудительного Long-шаблона. Это настройка текущего разрешённого выпуска, не изменение account defaults.

## Обязательный Studio read-back

После upload получить настоящий video ID/URL и проверить тот же канал, privacy, обработку/ограничения, metadata и фактическое отображение. Довести порученный release через Studio там, где Resolve не позволяет установить или проверить playlist, язык, audience, CC/SRT, tags, rights/restrictions, end screen либо Related video. Не объявлять эти поля готовыми по наличию общего YouTube preset.

Для Short Related video нужен доступ к advanced features, а цель должна быть доступным public/unlisted видео **этого канала**. Для long подготовить релевантный end screen в разрешённом scope и проверить его сохранение. Настоящий clickable end screen/Related video не заменяется рисунком или титром в MP4. Custom thumbnail также зависит от account eligibility; Resolve не обходит проверку YouTube. При блокировке сохранить точную причину/остаток работы, не заливать дубль и не изменять account. Статус «uploaded», «configured», «public» различать по фактическому read-back.

## Delegated channel access is not native/API proof

YouTube channel-permissions Manager access supports creating/uploading/publishing content in Studio, but invited channel-permission users do not gain YouTube API access through that delegation. Verify the current [official channel-permissions help](https://support.google.com/youtube/answer/9481328) and actual account/role. Do not conflate this with a different Brand Account role or generalize it to all owners.

A working Studio account switch or successful Studio upload does not establish which channel Resolve's connected YouTube account will use. Before native upload, verify the exact channel ID and visibility through that route; if unavailable, report the blocker without guessing, silently changing account permissions or redirecting upload. A role label does not authorize a new account connection or broaden the user's release scope.

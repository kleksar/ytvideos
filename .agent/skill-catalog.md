# Каталог проектных навыков

До применения любого навыка прочитать [канальный bootstrap](CHANNEL_BOOTSTRAP.md). Наличие skills в каталоге не загружает автоматически правила всех каналов. Канонические файлы одни; ссылки в папках каналов/выпусков обеспечивают discovery без Git.

Каждый skill содержит trigger, входы, процедуру, результат и ссылки. Открывать только навыки для текущей задачи. `AGENTS.md` задаёт обязательные ограничения независимо от того, выбрал ли runtime skill автоматически. Имена `ytv-*` уникальны в каталоге.

| Задача / владелец процедуры | Проектный skill | Основные входы и результат |
|---|---|---|
| Личный проход через Chrome ChatGPT | [ytv-chatgpt-extra-high](../.agents/skills/ytv-chatgpt-extra-high/SKILL.md) | Узкая задача → завершённый ответ, маркировка, URL, принятая версия |
| Единый flow Paper Detour и Nuviko | [ytv-video-production](../.agents/skills/ytv-video-production/SKILL.md) | Принятый сценарий → автономный готовый MP4 на просмотр → упаковка → одобренный Unlisted; профиль задаёт стиль/героя |
| Совместимый вход Paper / карусель | [ytv-paper-production](../.agents/skills/ytv-paper-production/SKILL.md) | Видео направляется в общий flow; карусель — в Posts Playbook |
| Постановка цельных сцен Paper | [ytv-paper-storyboard](../.agents/skills/ytv-paper-storyboard/SKILL.md) | Принятый текст → исполнимая партитура цельных кадров |
| Финал и конечная заставка нового длинного Paper | [ytv-paper-production / end screens](../.agents/skills/ytv-paper-production/references/end-screens.md) | План/бумажный фон → приёмка монтажа → нативные Subscribe и рекомендации через порученный release; Shorts исключены. Новый отдельный skill не требуется |
| Сценовые изображения: создание, правка и приёмка | [ytv-scene-images](../.agents/skills/ytv-scene-images/SKILL.md) | Прямой запрос и этап полного ролика: принятая постановка/реальные эталоны + обязательный [профиль Paper](../.agents/skills/ytv-scene-images/references/paper-detour.md) с запросом качества/4K → точные PNG, фактические размеры, continuity и доказательства проверок; старый ytv-paper-images — совместимый вход |
| Сценарий сюжетного Shorts всех каналов | [ytv-shorts-story](../.agents/skills/ytv-shorts-story/SKILL.md) | История и профиль → полный текст, проверка и решение о переходе; без подмены принятого сюжета |
| Естественный переход Shorts для всех каналов | [ytv-shorts-loop](../.agents/skills/ytv-shorts-loop/SKILL.md) | Оценить возможный стык; применить его, только если сохраняются ясность и полная развязка; иначе закончить без петли |
| Экранные субтитры Paper Detour | [ytv-paper-subtitles](../.agents/skills/ytv-paper-subtitles/SKILL.md) | Дословные субтитры и пословная подсветка; для Shorts принята одна строка до трёх слов и Chalkboard SE Bold |
| Отдельные субтитры SRT | [ytv-srt](../.agents/skills/ytv-srt/SKILL.md) | Фактическая речь и монтаж → отдельный SRT на языке аудио для каждого применимого нового выпуска, точные версии и раздельные QA; [профиль Paper](../.agents/skills/ytv-srt/references/paper-detour.md) |
| Названия YouTube: выпуск или аудит каталога | [ytv-youtube-video-titles](../.agents/skills/ytv-youtube-video-titles/SKILL.md) | Фактический фильм/обложка/эксперименты → точное название, решение keep/revise/defer и отдельные проверки; [профиль Paper](../.agents/skills/ytv-youtube-video-titles/references/paper-detour.md), старый ytv-paper-video-titles сохранён как адаптер |
| Обложка Shorts/длинного видео | [ytv-youtube-thumbnails](../.agents/skills/ytv-youtube-thumbnails/SKILL.md) | Одобренный MP4/название/эталоны + профиль → сгенерированная обложка с обязательной надписью, мастер/загрузочная копия и фактические проверки; Paper-вход совместим |
| Описания YouTube: выпуск или аудит каталога | [ytv-youtube-descriptions](../.agents/skills/ytv-youtube-descriptions/SKILL.md) | Фактический фильм/оговорки/принятые блоки → полное описание, diff и раздельные статусы; [профиль Paper](../.agents/skills/ytv-youtube-descriptions/references/paper-detour.md), старый Paper-вход совместим |
| Хэштеги YouTube для выпуска или каталога | [ytv-youtube-hashtags](../.agents/skills/ytv-youtube-hashtags/SKILL.md) | Материал/профиль/текущие метки → точный набор, основания и статусы проверки; запись выполняет release/upload |
| Главы и тайм-коды YouTube | [ytv-youtube-chapters](../.agents/skills/ytv-youtube-chapters/SKILL.md) | Финальный MP4/профиль → главы со свидетельствами и методом проверки; запись через release/upload |
| Подборки YouTube и аудит распределения каталога | [ytv-youtube-playlists](../.agents/skills/ytv-youtube-playlists/SKILL.md) | Фильм/полный каталог/реестр → назначения, порядок и минимальный план; release/upload исполняет порученные изменения |
| A/B названий и обложек | [ytv-youtube-ab-testing](../.agents/skills/ytv-youtube-ab-testing/SKILL.md) | Одобренный MP4 → три карточки → попарная проверка смысла до генерации и выдачи → готовый пакет на отдельное одобрение; доступность/текущий тест → контракт, наблюдение и отдельный исход; [профиль Paper](../.agents/skills/ytv-youtube-ab-testing/references/paper-detour.md) |
| Аналитика выпуска и канала | [ytv-youtube-analytics](../.agents/skills/ytv-youtube-analytics/SKILL.md) | Источник/период/формат/фильтры/журнал изменений → воспроизводимый baseline, ограничения и следующая проверка; [профиль Paper](../.agents/skills/ytv-youtube-analytics/references/paper-detour.md) |
| Упаковка других каналов и маршрутизация Paper | [ytv-video-packaging](../.agents/skills/ytv-video-packaging/SKILL.md) | Зафиксированный сюжет → заголовок/обложка; для Paper — переход к отдельным владельцам |
| Движения картинки и их сочетания | [ytv-image-motion](../.agents/skills/ytv-image-motion/SKILL.md) | Плавное движение целой картинки и сочетания направлений через FFmpeg |
| Монтаж Paper и Nuviko | [ytv-video-production](../.agents/skills/ytv-video-production/SKILL.md) | FFmpeg; канал задаёт стиль, текст и звук |
| Хранение медиа перед рендером и после QA/upload | [ytv-media-lifecycle](../.agents/skills/ytv-media-lifecycle/SKILL.md) | Роли/зависимости/owned runs → layout, audit/plan, current pointer и адресная очистка disposable файлов |
| Аудио, полный микс и аудиопараметры доставки | [ytv-audio-delivery](../.agents/skills/ytv-audio-delivery/SKILL.md) | Разрешения, существующие записи и монтаж → полный разрешённый микс и audio contract |
| Настройки и технический паспорт до рендера | [ytv-video-export](../.agents/skills/ytv-video-export/SKILL.md) | Saved edit / профиль / полный микс → единый export contract, фактические возможности движка и порученный экспорт → тот же контракт в QA |
| Финальная проверка видео/звука и адресный аудит | [ytv-video-qa](../.agents/skills/ytv-video-qa/SKILL.md) | Точный файл/edit/cues/motion → фактические проверки, покрытие, дефекты и перепроверка; [профиль Paper](../.agents/skills/ytv-video-qa/references/paper-detour.md) |
| Межканальный динамический календарь, выпуск и посты; исполнение плана подборок | [ytv-youtube-release](../.agents/skills/ytv-youtube-release/SKILL.md) | Отдельный календарь по channel ID, канальная политика/готовые материалы/поручение → план и проверенный внешний результат; [общая процедура](../.agents/skills/ytv-youtube-release/references/dynamic-scheduling.md) |
| Разработка исторического сюжета для нужного канала | [ytv-history-story](../.agents/skills/ytv-history-story/SKILL.md) | Источники и фактические ограничения → общий процесс сюжета → полный текст для пользовательского решения; канал выбирается по реестру |
| RU/EN личные истории, титры и VPN | [ytv-stories-shorts](../.agents/skills/ytv-stories-shorts/SKILL.md) | Текст/речь/библиотека → конкретный артефакт Stories |

Для создания/продолжения видео Paper и Nuviko использовать ytv-video-production. Профиль канала задаёт внешний вид и настройки, общий flow — последовательность и точки контроля. Готовый пользовательский текст сразу поступает в озвучку по root §5. Явная узкая задача сохраняет свою границу.

## Совместимые Paper-входы

- [ytv-paper-images](../.agents/skills/ytv-paper-images/SKILL.md) → общий `ytv-scene-images`.
- [ytv-paper-video-titles](../.agents/skills/ytv-paper-video-titles/SKILL.md) → общий `ytv-youtube-video-titles`.
- [ytv-paper-thumbnails](../.agents/skills/ytv-paper-thumbnails/SKILL.md) → общий `ytv-youtube-thumbnails`.
- [ytv-paper-descriptions](../.agents/skills/ytv-paper-descriptions/SKILL.md) → общий `ytv-youtube-descriptions`.

Эти входы подключают профиль Paper и не являются независимыми копиями общих процедур.

## Внешние зависимости и совместимость

- Системный `$imagegen` задаёт технический способ генерации/редактирования изображений; `ytv-scene-images` — производство и приёмку сцен с профилем канала. Paper-вход подключает профиль, не копирует процедуру. Не копировать инструкции системного инструмента.
- Глобальный `youtube-upload` (внешний навык; только если доступен в текущем Codex runtime) владеет механикой API-first, проверкой записи и условиями перехода к Studio; `ytv-youtube-release` направляет к [API-адаптеру](../automation/youtube/README.md) и добавляет проектные каналы/плейлисты/релизы. Не создавать локальный одноимённый upload skill.
- `paper-detour-director` и `paper-detour-film-crew` направляют соответственно в `ytv-paper-storyboard` и `ytv-paper-production`.

`.codex/agents` отвечает за обязанности исполнителей, skills — за workflow. Ни наличие роли, ни этот каталог сами по себе не запускают субагентов. При допустимом делегировании использовать реальные возможности текущего runtime; независимый обзор нельзя подменять сменой имени роли у автора.

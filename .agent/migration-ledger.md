# Миграция инструкций и skills — 1 ноября 2026

Последующий аудит по запросу пользователя подтвердил discovery и устранил отсутствие skills при входе из папок каналов/выпусков: [41 native-проверка и канальный bootstrap](discovery-checks-20261101/REPORT.md). Числа root/проверок ниже относятся к первоначальной миграции; GUI picker и свободный implicit-selection e2e не объявляются проверенными.

По просьбе пользователя структура разработана последовательными консультациями в Chrome ChatGPT Extra High. Видимая маркировка — **5.6 Extra High**. [Консультации](consultations/20261101-skills/README.md), [машинная карта переноса](migration-map.json), [архив и SHA-256](archive/before-skills-20261101/manifest.json).

## Что стало владельцем

- Корневой AGENTS.md: обязательные общие ограничения и маршрутизация, без длинной ленты статусов; 7787 байт вместо 126559.
- Канальные `channels/paper_detour/AGENTS.md` и `channels/nuviko_history/AGENTS.md`: визуальная идентичность, формат и предохранители канала.
- Десять уникальных `ytv-*` в `.agents/skills`: повторяемые процедуры с triggers, входами и результатами. [Каталог](skill-catalog.md).
- `.agent`: явные индексы, реестр идентичности, шаблоны и доказательства; эта папка не загружается автоматически.
- Пятнадцать TOML `.codex/agents`: обязанности исполнителей, ссылки на skills, без самостоятельного разрешения spawning и без model/permissions overrides.
- README и журналы выпусков: текущие разрешения, версии, ID и проверки. Перенесённые снимки — история, не свежая проверка.

## Карта всех разделов прежнего AGENTS.md

Исходник сохранён целиком (126559 байт). Строки 1–4 — заголовок/вводная, заменены краткой вводной нового root. Все остальные исходные строки учтены ниже; таблица показывает действующего владельца или локальный снимок, а точные старые формулировки остаются в архиве.

| Строки исходника | Раздел | Назначение |
|---|---|---|
| 5–13 | Чаты и источники ChatGPT в Chrome | [.agents/skills/ytv-chatgpt-extra-high/SKILL.md](../.agents/skills/ytv-chatgpt-extra-high/SKILL.md) |
| 14–49 | Каналы и монтаж | [.agent/documentation-index.md](documentation-index.md) |
| 50–56 | Итоговые файлы и очистка версий | [.agents/skills/ytv-audio-delivery/SKILL.md](../.agents/skills/ytv-audio-delivery/SKILL.md) |
| 57–62 | Стандарт звука для всех финальных рендеров | [.agents/skills/ytv-audio-delivery/references/delivery-checks.md](../.agents/skills/ytv-audio-delivery/references/delivery-checks.md) |
| 63–72 | Загрузка на YouTube | [.agents/skills/ytv-youtube-release/SKILL.md](../.agents/skills/ytv-youtube-release/SKILL.md) |
| 73–82 | Текущий выпуск 002 — Pompeii | [channels/nuviko_history/videos/002_pompeii/AGENTS_STATUS_20261101.md](../channels/nuviko_history/videos/002_pompeii/AGENTS_STATUS_20261101.md) |
| 83–86 | Текущий выпуск 004 — Pompeii Shorts | [channels/nuviko_history/videos/004_pompeii_short/AGENTS_STATUS_20261101.md](../channels/nuviko_history/videos/004_pompeii_short/AGENTS_STATUS_20261101.md) |
| 87–90 | Выпуск 010 — перелёты птиц | [.agent/episode-status/010_pfeilstorch.md](episode-status/010_pfeilstorch.md) |
| 91–97 | Историческая серия: фильм и поддерживающие Shorts | [.agents/skills/ytv-history-story/SKILL.md](../.agents/skills/ytv-history-story/SKILL.md) |
| 98–101 | Выпуск 001 — бывшая брата и лучшая подруга | [channels/nuviko_stories/videos/001_brother_ex_best_friend/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/001_brother_ex_best_friend/AGENTS_STATUS_20261101.md) |
| 102–107 | Выпуск 011 — свидания с другом | [channels/nuviko_stories/videos/011_парень_приводил_друга_на_каждое_свидание/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/011_парень_приводил_друга_на_каждое_свидание/AGENTS_STATUS_20261101.md) |
| 108–112 | Выпуск 012 — семейная реликвия | [channels/nuviko_stories/videos/012_дорогой_подарок_оказался_семейной_реликвией/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/012_дорогой_подарок_оказался_семейной_реликвией/AGENTS_STATUS_20261101.md) |
| 113–117 | Выпуск 013 — сестра на помолвке | [channels/nuviko_stories/videos/013_сестра_пришла_на_помолвку_в_свадебном_платье/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/013_сестра_пришла_на_помолвку_в_свадебном_платье/AGENTS_STATUS_20261101.md) |
| 118–124 | Выпуск 014 — книги Толкина и незнакомец | [channels/nuviko_stories/videos/014_подарок_парню_и_незнакомец_с_книгами_толкина/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/014_подарок_парню_и_незнакомец_с_книгами_толкина/AGENTS_STATUS_20261101.md) |
| 125–130 | Выпуск 015 — девушка брата и LEGO | [channels/nuviko_stories/videos/015_девушка_моего_брата_приревновала_его_ко_мне/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/015_девушка_моего_брата_приревновала_его_ко_мне/AGENTS_STATUS_20261101.md) |
| 131–136 | Выпуск 018 — соседский мальчик назвал меня папой | [channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/AGENTS_STATUS_20261101.md) |
| 137–141 | Выпуск 019 — торт с чужим именем | [channels/nuviko_stories/videos/019_торт_с_чужим_именем/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/019_торт_с_чужим_именем/AGENTS_STATUS_20261101.md) |
| 142–146 | Выпуск 021 — семейный ужин-сюрприз | [channels/nuviko_stories/videos/021_семейный_ужин_сюрприз/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/021_семейный_ужин_сюрприз/AGENTS_STATUS_20261101.md) |
| 147–151 | Выпуск 022 — свадьба сестры в подарок | [channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/AGENTS_STATUS_20261101.md](../channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/AGENTS_STATUS_20261101.md) |
| 152–183 | Выпуск 020 — Rarovista: программа в радиоэфире | [channels/paper_detour/videos/001_radio_game/AGENTS_STATUS_20261101.md](../channels/paper_detour/videos/001_radio_game/AGENTS_STATUS_20261101.md) |
| 184–192 | Paper Detour 002 — Margorie McCall | [channels/paper_detour/videos/002_margorie_mccall/AGENTS_STATUS_20261101.md](../channels/paper_detour/videos/002_margorie_mccall/AGENTS_STATUS_20261101.md) |
| 193–200 | Выпуск 025 — IQ Gallery, минутный Shorts | [channels/paper_detour/videos/003_iq_gallery/AGENTS_STATUS_20261101.md](../channels/paper_detour/videos/003_iq_gallery/AGENTS_STATUS_20261101.md) |
| 201–216 | Paper Detour 004 — Last Video | [channels/paper_detour/videos/004_last_video/AGENTS_STATUS_20261101.md](../channels/paper_detour/videos/004_last_video/AGENTS_STATUS_20261101.md) |
| 217–224 | Paper Detour 007 — Joshua and Jessica | [channels/paper_detour/videos/007_joshua_jessica/AGENTS_STATUS_20261101.md](../channels/paper_detour/videos/007_joshua_jessica/AGENTS_STATUS_20261101.md) |
| 225–229 | Paper Detour 009 — Knorozov and Asya | [channels/paper_detour/videos/009_knorozov_asya/AGENTS_STATUS_20261101.md](../channels/paper_detour/videos/009_knorozov_asya/AGENTS_STATUS_20261101.md) |

## Дополнительные переносы и исправления

Внутри прежних общих правил строка 22 содержала идентичность Минни 027: она дополнительно сохранена рядом с выпуском. Указания 46–48 радио 001 остаются в его журнале координации и снимке. Образ/эталон 004 вынесен в Paper AGENTS; голоса и скорости — в канальные правила и справку доставки. Это не новые проверки медиа.

Три больших руководства Paper превращены в короткие совместимые указатели; прежние заголовки оставлены для входящих anchors, полные тексты сохранены в архиве. Два старых глобальных Paper skills стали тонкими routers к уникальным локальным навыкам. Глобальные `youtube-upload` и `make-story-shorts` не изменялись. Общий checklist загрузки принадлежит первому, проектная организация релиза — `ytv-youtube-release`.

Исправлены устаревший README ролей (runtime сейчас предоставляет `agent_type`, но его наличие нужно проверять), входной индекс Paper со слоевым примером и ссылка README Pompeii на прежний root-статус. Для двух навигационных файлов preimage восстановлен обратным применением точной внесённой замены; это отмечено в manifest.

Исследования, подробные captions/VPN/History guides, типографические примеры, playlist registry и конкретные списки ресурсов оставлены справочной предметной базой. Каждый такой документ не нуждается в собственном skill. Устаревшая слойная схема не возобновляется через архивную ссылку.

## Границы и неизвестное

- Реестр содержит 36 физических каталогов и их canonical links, четыре канала помечены UNVERIFIED: назначение не выведено из slug. Алиасы-симлинки не размножают выпуски.
- Прежний `archive/legacy_stories/videos/010_pfeilstorch` не найден. Его текст сохранён в `.agent/episode-status`, каталог и активы не выдумывались.
- Импорт/фактический picker skills и custom roles в новой сессии клиента не тестировались. Проверена файловая структура по официальным правилам discovery; `.agent` не объявлена специальным runtime-каталогом.
- Независимый production review не выполнялся; консультация ChatGPT — проверка архитектуры, не просмотр роликов.
- Медиа, проекты Palmier, внешние публикации, настройки Codex, permissions и модели не менялись; Git не инициализировался.

## Воспроизводимая проверка

Из корня: `python3.11 .agent/scripts/validate-governance.py`. Это read-only проверка структуры, ссылок, TOML, архива, покрытия исходных строк и реестра. Frontmatter skills дополнительно проверяется системным `quick_validate.py`. Результаты и ограничения — в [отчёте](validation-report-20261101.md).

# Полный ролик и отдельные навыки: проверка продолжения

2026-11-01. Основания: прямое уточнение пользователя «сюжет = весь ролик» и предложение отдельных модулей; личные завершённые консультации координатора [о зависимостях](../../../consultations/20261101-paper-detour-full-video-dependencies.md) и [о helper титров](../../../consultations/20261101-paper-detour-caption-helper.md). Это проверка документации и помощников, не выполненный новый фильм.

## Действующий контракт

[Production](../../../../.agents/skills/ytv-paper-production/SKILL.md) → [полный runbook](../../../../.agents/skills/ytv-paper-production/references/production-runbook.md): контекст и полномочия → исследование, история, полный EN script и две проверки → постановка всей длины → параллельная подготовка сцен, разрешённой речи и упаковки → проверенная фактическая речь, alignment и точный timing → PNG титров и preflight всех назначенных пар → один writer Palmier → полный микс → MP4 и нужный SRT → реальный полный просмотр/прослушивание 1× и технический QA → локальная выдача.

Стадия не создаёт пользовательского approval. Явные узкие поручения сохраняются; новый звук имеет конкретный scope, загрузка и публикация поручаются отдельно.

Созданы четыре модуля: captions, thumbnails, video-titles, descriptions. Images и release → глобальный youtube-upload переиспользованы. У cue procedure один владелец captions, старый storyboard reference перенаправляет к нему. Typography владеет глифами и геометрией, edit — движением. Routing docs и прямые ссылки согласованы. В Shorts strategy устранён остаточный обязательный кульминационный хук/loop: это жанровый приём, не общая формула.

## Проверки

- [quick_validate](skill-validation.json): **14 из 14 skills PASS**.
- [Native skills/list](../../../discovery-checks-20261101/after.json): **44 из 44 зарегистрированных входов PASS**; 14 enabled skills на каждом, missing 0, duplicates 0, errors 0. Hash всех 14 SKILL совпали после probe. Только initialize + skills/list, без thread/start, turn/start или model generation. Discovery не доказывает будущий выбор модели.
- Независимый read-only walkthrough четырёх запросов: полный 90-секундный EN ролик с прямым разрешением всего звука; только EN script/обсуждение; только размер существующих акцентов; упаковка и Private upload. Маршруты, границы, ownership, permissions и QA согласованы. Это чтение и симуляция маршрута, не исполнение медиа или операций Chrome/Studio.
- Проверены 358 Markdown targets по маршрутам и отдельно новые helper links. Четыре отсутствующих legacy README Pompeii 005–008 находятся в adapter README других каналов. Paper owner/runbook/caption/release targets доступны. Вне Paper не исправлялись.
- [Caption helper](../../../../.agents/skills/ytv-paper-captions/scripts/render_paper_captions.py), версия **1.0.1**: 14 meaningful unittest PASS у исполнителя; первоначальные 12 независимо повторены reviewer. Только synthetic assets во временных каталогах. Существующие PNG или explicit fontTexture, общий пропорциональный fit, half-open face/alpha bounds, все назначенные пары и anchors, неизменяемые входы, новая выдача и provenance. Нет timeline, audio, network или SRT.
- Независимый review выявил реальную коллизию cue/scene IDs по регистру на case-insensitive FS: short/SHORT затирали output. Исправлено через casefold uniqueness без переименования IDs. Два новых теста воспроизвели FAIL до исправления, затем PASS до создания output. Reviewer независимо подтвердил отказ short/SHORT и s1/S1 до output и сохранение допустимого mixed-case ID. **Дефект закрыт.**
- Старый [normalizer](../../../../new_channel/automation/normalize_paper_accent_cues.py:133): устранён двойной +1 в NumPy-ветке. Четыре regression-теста сначала FAIL, после PASS; NumPy/Pillow возвращают одинаковые half-open bounds. Root повторил всю automation suite: **17 tests OK**. AST Python 3.11 двух изменённых файлов PASS у исполнителя.
- Governance validator проверяет уникальные имена и равенство текущему canonical catalog вместо фиксированных 10 skills; **14/14 совпадают**. Остальные проверки не отключались.

## Ограничения

Font backend не принят как фирменный font/atlas; нет автоматического fallback на SFNSRounded. Технический PASS относится к статичной геометрии выбранных anchors. Написание на existing PNG, стиль, глифы, фактура, смысловые коллизии, интерфейсные safe zones, движение и sync требуют реальной визуальной проверки/playback и остаются UNVERIFIED в машинном отчёте. Реальные титры выпуска здесь не принимались.

[Полный governance validator](governance-validation.json) остаётся **FAIL**. Сообщения включают исторические assumptions: history не учитывается в inventory, директории проверяются как файлы, относительные канальные routers, regex запретов параллакса; также сравнение живого global upload с архивом и root budget. У свежего 030 нет history field в registry. Этот срез не подменяет FAIL зелёным статусом и не меняет параллельную миграцию выпусков. Discovery и изменённые Paper-процедуры имеют отдельные результаты выше.

Пользовательский пилот пока на стадии предложения темы: [Гейб и публичный пароль](../../../../new_channel/research/2026-11-01-feed-pilot/SELECTION.md). Полный EN script, сцены, новый звук, монтаж, экспорт и upload не запускались. Процесс предстоит проверить настоящим полным циклом; готовность helper не является готовностью ролика.

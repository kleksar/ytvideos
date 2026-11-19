# Vice Wreckroom — GTA VI Shorts

## Identity и границы

YouTube channel ID: `UCcZWXzkL_K1mD5dr8MZBYrQ` ([канал](https://www.youtube.com/channel/UCcZWXzkL_K1mD5dr8MZBYrQ)). Имя **Vice Wreckroom**, прежнее имя **OddlyDrawn**. Последний наблюдавшийся handle — `@OddlyDrawnBtw`; новое имя не доказывает смену handle. Не переименовывать аккаунт и не переносить эту identity на Scenes on Repeat / You But Weird.

This is a documented manual workflow, NOT an activated ChannelSpec, executable recipe or automatic publication. Saved Studio description was independently read back on 2026-11-19, with Publish disabled and no edits:

> The funniest GTA VI stream moments, cut so the joke still lands if you missed the stream. Bad plans, weird glitches, and reactions worth replaying. Original streams are credited in each description. Story spoilers are marked up front.

The description is a verbatim identity snapshot, not permission to bypass the spoiler/source-rights gates below. Dated observations: [evidence](../../docs/references/vice-wreckroom-discovery.md).

Контент: короткие самостоятельные смешные эпизоды из реальных GTA VI стримов. Показать понятную завязку, действие и завершённую реакцию/развязку. Не выдавать trailer reaction, меню, чужой пересказ или синтез за реальный gameplay. Имя стримера/подпись должны соответствовать источнику. Не заполнять квоту слабыми эпизодами.

## Candidate handoff before production

The owner chooses the story/moment from the discovery shortlist. Send each nomination with the exact VOD link, a review start BEFORE the peak, the peak timestamp, proposed end/duration, and the observed chat signal with its limits (window, message/user counts where known, laughter vs general activity, baseline/coverage and missing evidence). Label these as candidates, not approved funny Shorts. Do not invent metrics, anonymous author IDs, a verified laugh or a finished payoff.

Do not hold this initial shortlist until Dot completes a full audiovisual/editorial review of every candidate. Wait for the owner's choice and instructions before creating the editable Resolve project or production edits, then iterate on the selected moment. This changes the candidate handoff order, not source rights or final quality gates. The manual STOP/STAY/PAYOFF, complete audiovisual boundaries and release checks below apply to selected production material before it is called ready; unknown observations stay explicit in the initial handoff. No automatic quota filling, assembly or upload from a scout score.

## Отбор и монтаж

- Канальные входы: exact VOD/creator, доступный законный исходник, source offset, проверенные условия использования и короткий edit plan. Оригинальный NoCodeHack — [gta6-clipper](https://github.com/nocodehack/gta6-clipper); локальный исходный clone `Work/gta6-clipper` не заменять аддоном `Work/gta6-clipper-discovery-v2`. Эти относительные локаторы не гарантируют наличие файлов в другом checkout.
- Три независимых сигнала: **stock scout** (громкость/популярность/клипы), **chat laughter** (текстовые признаки смеха с проверенными IDs/авторами), **audio laughter** (временная классификация звука или ручная проверка). Громкая волна, большое число сообщений, `W`/`OMG` не доказывают смех; смех в игре/донате не доказывает смех стримера. Сохранять происхождение, окно и ограничения каждого сигнала; не складывать коррелированные scores как независимую вероятность качества.
- Любой сигнал только выдвигает кандидата. Требуется независимая ручная аудиовизуальная проверка **STOP / STAY / PAYOFF**: понятен ли первый кадр, зачем смотреть дальше, есть ли завершённая смешная развязка. Проверять не только транскрипт или контактный лист, но действие и речь в самом исходнике. Chat-only, audio-only и stock-only кандидаты не становятся одобрением автоматически.
- Контекст поиска одного момента — **не более 600 секунд**. Для монтажа допустимы несколько непересекающихся фрагментов этого контекста с явными ролями setup/action/payoff, при необходимости reaction. Записать точные границы и соответствие локальных таймкодов VOD. Не переставлять фразы так, чтобы выдумать причинность. Полнота слов и действий важнее фиксированного числа секунд.
- Субтитры — по реально произнесённой речи, с проверкой имён, шутки и тайминга на слух. Ошибку ASR не превращать в надпись. Цитата чата явно помечается как чат, а не речь стримера. Кадрирование сохраняет видимыми и действие игры, и нужную реакцию; детектор лица может принять игрового персонажа за webcam.
- Главные сюжетные спойлеры, нагота, меню и дубликаты — veto. Незначительный спойлер допускается лишь при отдельном явном разрешении, допустимости по правилам источника и проверенном предупреждении. Одно предупреждение не снимает запрет источника.

Монтажный default — [Resolve](../../.agents/skills/ytv-resolve/SKILL.md): редактируемые исходные clips/audio/captions, а не единый запечённый MP4 вместо проекта. JSON cut list/CMX3600 video-only EDL аддона не доказывает готовый native проект, conform звука или проверенный импорт. Сверять актуальное evidence приложения. Целевой Short — 1080×1920 / 30 fps, H.264/AAC; увеличение 720p-источника не восстанавливает детали. Сохранить исходную речь/реакцию, слышимость и синхронность; не применять новую нормализацию к принятому mix без соответствующего scope и проверки.

## Native editability: explicit channel requirement

The owner requires ALL creative editing for Vice Wreckroom to remain native in Resolve: separately editable gameplay/facecam crops and transforms; still/meme graphics; text/captions; original speech, music and SFX on their appropriate individual clips/tracks/nodes. Clipper detects candidate windows and exports source clips, exact timing and an editable handoff only. FFmpeg is allowed for technical preparation/conform/validation, not baking framing, captions or the creative finish before import. Importing one finished MP4 does not satisfy this requirement.

Existing project #7 contains some baked carriers: this is a known migration gap, NOT proof of fully native reconstruction. For a newly authorized affected edit, recover separate elements from verified sources, preserve the previous project until verification, and check editability of each role and the exact export. Migration is not claimed complete; this rule does not silently rewrite other completed projects or other channels.

## Права и источник

Для каждого эпизода сохранить creator/VOD URL, конкретное разрешение или условия кампании, дату проверки, разрешённые платформы/монетизацию/монтаж, обязательные credit/hashtags, запреты и доступность исходника. Reach/Content Rewards campaign, доступный VOD и разрешение стримера — разные факты; не выводить одно из другого. Проверить также права на игру, музыку, вставки и иных правообладателей; не утверждать, что согласие стримера отменяет их. Использовать обычный публичный или авторизованный доступ, без обхода ограничений.

Перед релизом сверить актуальные первичные правила: [Rockstar](https://support.rockstargames.com/articles/7bNaeoMFTV0iUDGhStTXvz/policy-on-posting-copyrighted-rockstar-games-material), [YouTube reused content](https://support.google.com/youtube/answer/1311392). Разрешение на использование не гарантирует монетизацию YouTube; монтаж/субтитры сами по себе не дают такой гарантии. При пробеле остановить только затронутый release.

## Плейлисты

Последний проверенный Studio read-back: все три **Unlisted**, пустые на дату наблюдения. Перед добавлением видео повторно сверить точный ID и видимость, не создавать дубликат по одному имени.

| Название | ID |
|---|---|
| GTA VI — NPC Chaos | `PLUAzjjS5i4z8` |
| GTA VI — Physics & Fails | `PLMjOhnNApdxc` |
| GTA VI — Chat Made Me Do It | `PLHtdNiRjdumM` |

Legacy playlist **Body Myths, Explained** не относится к новому пакету. Удаление/очистка старого контента — отдельная явно разрешённая владельцем операция, не часть этого документа и не следствие переименования. Её завершение здесь не утверждается.

## Канальный delivery contract

Общие [release gates](../../docs/standards/release.md) и [Resolve delivery/read-back](../../.agents/skills/ytv-resolve/references/delivery.md) сохраняются. По прямому поручению владельца для **Vice Wreckroom** выбран маршрут **Resolve Deliver → Upload directly → YouTube Unlisted**, категория **Gaming**. Это узкое канальное исключение из общего начального Private, не новый default остальных каналов. Оно не разрешает Public, schedule, перенос/удаление старого видео или публикацию непроверенного кандидата; exact media и scope upload остаются обязательными.

До dispatch требуются точный channel ID в подключённом аккаунте, approved exact timeline/export, complete source/rights/QA, title/description/tags/playlist, реальное audience/disclosure решение и явно выбранная Unlisted visibility. Если native UI не даёт проверить канал/видимость/обязательное поле, upload блокируется до устранения пробела; не предполагать безопасный default и не обходить молча другим каналом/методом. Chapters для Short выключены; thumbnail выбирается только доступным поддержанным способом, не считать его загрузку проверенной по наличию локального файла.

Проверка render job не равна проверке upload. Нужны returned video ID и Studio read-back: именно этот канал и файл/длительность, Unlisted, Gaming, точные metadata/playlist, завершение обработки и применимые проверки/ограничения. Проверить воспроизведение, звук/субтитры и доступное качество после обработки. UNKNOWN сначала сверить с существующими видео/job receipts, не отправлять повторно. Native direct-upload **не подтверждён как успешно выполненный** в текущем evidence; выбранный пользователем маршрут не является результатом теста.

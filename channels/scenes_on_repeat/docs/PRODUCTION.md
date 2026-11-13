# Производственный рецепт киноформатов

Общий запуск/создание ID/state и два approvals задаёт [workflow](../../../docs/workflow.md). Здесь только выбор и подготовка материалов `licensed_clips`.

## Исходники и отбор

Для принятого фильма установить точную версию, длительность, язык/каналы звука, English subtitle source, права и actual file hashes. Найденный файл/доступность в интернете сами по себе не доказывают разрешение. Не переносить media в Git. Сначала изучить субтитры и необходимые окна кадров/звука, затем выбрать конкретные сцены; описание по памяти не заменяет просмотр.

Каждый кандидат имеет понятное начало, изменение ситуации и результат/реакцию. Указать исходные timecodes, номера кадров, сохранённые целые реплики, нужный контекст первого зрителя, spoiler scope и отличие от соседних кандидатов. Вырезать проходное, не потеряв причину события. Не создавать обязательный пакет из фиксированного числа сцен.

Полный сценарий для `licensed_clips` включает авторскую narration, если она нужна, и точный edit/story plan исходных сцен. Для монтажа из source-реплик или без речи использовать typed `ytv-edit-script-v1` с явным `speech.mode` по [task contract](../../../docs/operations/task-contract.md#outputs). Не добавлять выдуманный narration ради прохождения текстового gate. Одобрение относится к exact содержанию полного текста/JSON. При обычном запросе нового сюжета сначала представить законченную редакционную основу, не просить пользователя самостоятельно отбирать все clips.

## Сборка

Сценовые Shorts собираются по [EDIT_NOTES](EDIT_NOTES.md), long по [LONG_COMPILATIONS](LONG_COMPILATIONS.md), мемы по [MEME_SHORTS](MEME_SHORTS.md). Для мини-трейлера просмотреть фильм целиком, выбрать узнаваемые сцены из разных частей и не раскрывать ключевые спойлеры. Мини-трейлер сохраняет связное зрительское обещание, фактический порядок выбранных source shots и оригинальный разрешённый звук; montage decisions, cue maps и subtitles фиксируются по exact source/final frames.

Перепроверить crop, чистые cuts, целые реплики, звуки действия, карту слов и полный музыкальный план. Написать reproducible edit plan. Sources/extracts и сборку выполнять фактически доступным host tool с наблюдёнными capabilities; `execute-media` не содержит clip extraction, а still-image montage не принимает `licensed_clips`. Существующие helpers из `automation/pipeline/` использовать по их `--help`, сохраняя production manifest и claimed `host_render` execution по [task contract](../../../docs/operations/task-contract.md#render-manifest-и-delivery-evidence). Batch renderer Shorts сам не строит длинную подборку.

Принятый `source`/`none` использует audio `mix` из точных зарегистрированных фрагментов, без TTS. При `source` подготовить фактические слова и SRT; при `none` выполнить listening всего soundtrack и сохранить typed `no_speech` decision вместо фиктивного SRT. `has_speech` в render/release совпадает с принятым сценарием. Поля и commands принадлежат [task contract](../../../docs/operations/task-contract.md#media-изображения-release).

Для общей очереди media может оставаться по прежнему стабильному адресу; store ссылается на artifact URI/hash. Не создавать вручную ещё один mutable EPISODE/RELEASE_STATE для новой run. Исторические записи сохраняются для import и provenance.

## Проверка и release

Сохранить frozen inputs/commands и проверить фактический MP4. Показать пользователю готовый результат; упаковку выполнять параллельно. После MP4 approval и прямого поручения на выпуск выполнить Private upload, claims/processing/subtitles/metadata и разрешённое расписание по [release](../../../docs/standards/release.md). Политика прав/звуков — [PROFILE](../PROFILE.md).

Если live checks выявили дефект, исправить в минимальной области. Новые bytes имеют новый hash и требуют соответствующего MP4 approval; это исправление конкретного выпуска, не отдельное штатное Unlisted согласование. Повторные upload attempts учитываются в лимите и operation journal; удаление video не считать возвратом quota.

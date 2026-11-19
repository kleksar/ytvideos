# Vice Wreckroom — bounded evidence, 2026-11-19

Текущие параметры и release scope принадлежат [профилю](../../channels/vice_wreckroom/PROFILE.md). Этот документ — датированное свидетельство, не production approval и не установка аддона.

## Канал и Studio

Independent Studio read-back on 2026-11-19: channel `UCcZWXzkL_K1mD5dr8MZBYrQ`, Vice Wreckroom, handle `@OddlyDrawnBtw`; Publish was disabled, no edits. Exact saved description:

> The funniest GTA VI stream moments, cut so the joke still lands if you missed the stream. Bad plans, weird glitches, and reactions worth replaying. Original streams are credited in each description. Story spoilers are marked up front.

The three full playlist names/IDs/Unlisted status in the profile were verified (0 videos at that snapshot). Later read-back confirmed legacy cleanup complete under its separate owner authorization; one public GTA Short and the three GTA playlists remain. This is observed state, not a deletion instruction.

Публичный Short `mfT2wnPdLeQ` («KreekCraft Was Just Standing There… | GTA 6») загружен владельцем вручную. Это не доказательство agent/native Resolve upload. Текущий документ не меняет channel settings и не разрешает удалять legacy Body Myths.

## Исходный инструмент и отдельное исследование

Upstream: [nocodehack/gta6-clipper](https://github.com/nocodehack/gta6-clipper), локальный оригинальный clone `Work/gta6-clipper`. Аддитивная локальная работа: `Work/gta6-clipper-discovery-v2`, проверенный HEAD `c6d68a5` (предыдущие `26c25f4`, `1a02f20`). Это **локальные коммиты аддона**, не upstream PR, не commits ytvideos и не гарантия remote backup. Не коммитить raw media, credentials или персональные chat exports в ytvideos.

Позднейшее подтверждение координатора 2026-11-19: интеграция в отдельном `Work/gta6-clipper-integrated`, commit `6097ca3`, локальный merge `3721b6e` в локальную ветку `kleksar/main`; 40 tests и stock self-test прошли. Remote fork не найден, push не выполнен, оригинальный clone не изменён. Локальная интеграция не является remote merge или новым доказательством качества. Последующий локальный commit `bcb9509` в `kleksar/main` добавляет optional `chat.py activity`: симметричный configurable radius, абсолютные 10-секундные bins, раздельные counts/users и laughter, ≥80% покрытия каждой стороны с before/after local background. Координатор сообщил 47 tests и unchanged stock self-test PASS; remote push по-прежнему отсутствует. Wider-window benchmark ещё не выполнен, доступна лишь ±40s диагностика: это не доказательство улучшенного отбора.

Read-only inspected: `README.md`, `DEVELOPMENT_CHECK.md`, `comparison-hybrid-development.json`, `baseline-comparison.json`. Первоначальный README тезис «synthetic only» исторический: более поздний DEVELOPMENT_CHECK фиксирует ограниченные real-window проверки, не независимую валидацию. Для переноса нужны exact addon/input версии и hashes, а не только эти локаторы.

## Что реально измерено

10 convenience windows, четыре GTA VI VOD одного дня (Kai, Clix, Lacy, Kreek). Восемь положительных labels — прежний выбор editorial workers; два weak labels — редакторская оценка. Это **не персональные approvals/rejections владельца**, не held-out set, не просмотры/удержание и не общая точность.

Hit означает пересечение номинированного окна с заранее отмеченным событием, **не** самостоятельный смешной Short.

| Вход / scout | Hits из 8 provisional positive windows | Nominations из 2 weak windows |
|---|---:|---:|
| Redaction-heavy input (4,778 messages), stock | 6/8 | 1/2 |
| Тот же input, strict chat laughter | 4/8 | 1/2 |
| Тот же input, additive union | 7/8 | 2/2 |
| Sensitivity input (4,808 messages), stock | 6/8 | 1/2 |
| Sensitivity input, strict chat laughter | 6/8 | 0/2 |

У sensitivity input сохранены reaction templates; два повторно полученных окна немного изменились. Это существенное отличие preprocessing/input, не чистое доказательство превосходства модели. Union расширил охват и одновременно номинировал оба weak окна. **6/8 + один weak nominee не означают шесть готовых удачных роликов.** Два negatives недостаточны для оценки false-positive rate. Предыдущая отклонённая десятка была вручную собрана несколькими workers, а не получена единым алгоритмом; технический PASS её файлов не является editorial acceptance.

`comparison-hybrid-development.json` сохраняет input SHA-256 `0157b5d8362794780c6d7f7f2938a91ef0c70e14d7be586858f6b8895e0b7c5a`. `baseline-comparison.json` отдельно помечен SYNTHETIC; не смешивать его с real-window результатами.

## Audio laughter: wiring, не доказанный классификатор юмора

Локальный report: Apple SoundAnalysis дал 32 окна confidence ≥0.30 на CC0 sample [Laughter(s)](https://commons.wikimedia.org/wiki/File:Laughter(s).ogg), девять ≥0.80, max 0.908. На десяти прежних mixed exports и четырёх Kai raw excerpts не было ≥0.80. Это sanity check подключения, **не precision/recall**; отсутствие detections не доказывает отсутствие смеха. Classifier confidence не является вероятностью, что Short смешной, и не устанавливает личность смеющегося.

Chat laughter OR подтверждённый streamer audio laugh может номинировать; оба сигнала имеют приоритет для просмотра, не автоматический approval. Stock-only путь сохраняет собственную метку и требует самостоятельного аудиовизуального подтверждения юмора. Результаты не обосновывают замену stock scout, обучение модели или обещание качества на масштабе.

Следующая содержательная проверка: одинаковые frozen исходные окна, независимые холодные оценки завязки/действия/развязки и причин отказа, отдельные chat/audio timestamps; continuous и multi-cut варианты из одних raw media в слепом порядке. Нужны результаты, а не только существование плана. Импорт video-only EDL аддона в Resolve и audio re-conform пока **UNVERIFIED**; успешное создание EDL не считается native import test.

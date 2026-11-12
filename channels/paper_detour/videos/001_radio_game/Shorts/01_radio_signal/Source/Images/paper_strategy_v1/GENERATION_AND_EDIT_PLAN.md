# Short 01 — новые слои и монтажный план

30 октября 2026. Материалы для отдельного 9:16 Shorts. Основной фильм в другой сессии: его таймлайн и импортированные источники не изменять. Сцены и тайминги ниже — исходный план; фактическое состояние монтажа приведено в разделе «Текущее состояние редактора». До использования в Palmier оценить масштаб, перспективу, границы альфы и соответствие свету на реальных композициях. Режим возврата к редактору должен учитывать параллельную сессию.

## Голос и субтитры

- Новый текст: `../../Voice/strategy_v1/narration_en.txt`, взят из Short A стратегии; источник фактов — `../../../../../Research/FACT_CHECK.md`.
- ElevenLabs Roger `CwhRBWXzGAHq8TQ4Fs17`, `eleven_v4`; тот же голос, что в фильме. Запись `../../Voice/strategy_v1/generated/voice_en.mp3`, mono MP3 44,1 кГц, около 29,44 с, без изменения скорости.
- Рядом `voice_en.alignment.json`, `voice_en.words.json` и `voice_en.draft.srt`. Тайминги предоставлены TTS: последние могут выходить за фактическую длину файла. SRT черновой, проверка произношения, слуховая синхронизация, при необходимости корректировка обязательны. Название Clip Informática проверить на слух особенно внимательно. Не включать непрерывные субтитры как акцентный текст.

## Исходники и запросы imagegen

Использовалась встроенная генерация image_gen. Общий ориентир: `channels/paper_detour/videos/001_radio_game/Source/Images/composition_fix/radio_desk_master.png`; тёплая бумажная диорама, янтарный свет, темно-бирюзовая комната, без дырок гофрокартона. Разные планы должны восприниматься как одна история и общая материальная стилистика.

- `study_bg.png`: вертикальная пустая комната с рабочим столом для отдельных предметов; окно, полки, растения.
- `radio_fg.png`: изолированный 1980s радиомагнитофон как прозрачный слой, перспективный вид спереди; бутафорские условные обозначения без бренда.
- `cassette_fg.png`: изолированная кассета с прозрачностью, вид сверху в три четверти; без текста.
- `computer_fg.png`: изолированный винтажный компьютер и клавиатура на прозрачном фоне, зелёный экран с абстрактными данными.
- `tape_deck_close_bg.png`: крупный план открытого кассетного механизма. Из-за формы и перспективы кассеты отдельно проверить реальную совместимость с ним; использовать как отдельный план, если вставка не выглядит естественно.
- `computer_close_bg.png`: отдельный крупный план монитора с абстрактным сигналом, видимая глубина резкости и бумажные материалы.
- `station_bg.png`: нейтральная бумажная радиостанция на закате, не документальная реконструкция конкретного здания.
- `wave_fg.png`: отдельная бумажная волна на прозрачном фоне для объясняющей анимации.
- `software_text_fg.png` и `data_text_fg.png`: объёмные бумажные слова на прозрачном фоне, отдельно от картинки. Их нужно разместить не перекрывая смысловые объекты и мобильный интерфейс; плавно проявлять при свободном появлении.

Выше файлы сгенерированы как отдельные активы; прозрачность присутствует, но ореолы и масштаб требуется проверить именно в композите на вертикальном холсте. Угол изолированных предметов не гарантированно совпадает с каждым фоном. Не оставлять эффект парящих предметов; при необходимости пересоздать целостную композицию и совместимые слои. Исходники не перемещать после импорта; экспортов и публикаций нет.

## Монтажный план по сырой озвучке (30 fps; секунды — приближённый alignment)

| Время | Смысл / визуальный план | Анимация и звук |
|---|---|---|
| 0–4,6 | Крупная кассета: «больше, чем музыка… компьютерная программа». Показать объект сразу, избегая длинной заставки. | Небольшой мягкий наезд или короткая статика; бумажный акцент `SOFTWARE` в такт «program», без перекрытия предмета. |
| 5,1–11,7 | Бразильская радиостанция → радиосигнал; название передачи означает исторический пример. | Смена масштаба и ракурса. Схематическая волна из отдельного слоя; по возможности тихий собственный иллюстративный сигнал с пометкой реконструкции. |
| 12–15,8 | Приёмник → запись звука на кассету. | Короткая смена на крупную деталь; механический звук только при реально видимом действии и в точном синхроне. Не использовать отбракованный щелчок из основного фильма. |
| 16,1–20,6 | Лента → совместимый компьютер → DATA. | Отдельные слои сцены; слово `DATA` с появлением на слове «data» и слышимым бумажным акцентом, либо спокойное проявление без эффекта. |
| 21–27,3 | Позднее исследование старой записи: что обнаружили в шуме? | Другой план с данными/записью, без выдуманного человека и без утверждения успешного запуска игры. |
| 27,4–29,44 | «The full story is in the linked video». | Разборчивый CTA, без стрелки к фиксированному месту интерфейса. Связанный фильм добавить только при реальной загрузке после проверки версии и доступа. |

Для сборки скопированы независимые кандидаты `../../Audio/strategy_v1/music_bed_56s_synth_stereo.wav`, `sfx_tape_motor_synth_5s.wav`, `sfx_radio_search_synth_1_8s.wav` из проектных синтетических заготовок; они не являются проверенным миксом. Музыка: выбрать подходящую синтетическую дорожку проекта, сохранять непрерывность и низкий уровень относительно голоса; проверять баланс на слух. Изображения и звук реконструкции не выдавать за оригинальную архивную запись. Не считать график точным до проигрывания. Отдельные слова или группы, появляющиеся по очереди, должны иметь согласованные звуковые атаки; если используется один общий звук, анимация должна читаться как единый жест.

## Текущее состояние редактора

31 октября: собран и сохранён отдельный проект `/Users/diplomat/Documents/Palmier Pro/Paper Detour 001 Short 01.palmier`, 1080×1920/30 fps, таймлайн `7178D5B6`, 885 кадров (29,5 с). Основной фильм не изменялся. Шесть планов: кассета на столе, радиостанция, крупная дека, крупный компьютер, компьютер в комнате, радиостанция. Волна и компьютер — отдельные слои; слова SOFTWARE и DATA проявляются и исчезают с fade. Зерно 0,5, непрерывная музыка, голос 1,0×, отдельный бумажный звук на жест волны. Звук механизма убран: видимого движения деки нет. В конце голос содержит CTA; отдельная текстовая CTA-плашка пока не сделана.

Для устранения географической ошибки и парящей кассеты добавлены `study_bg_saopaulo_v2.png` (нейтральный городской вид; сцена условная) и цельная композиция `cassette_desk_hero_v2.png`. `station_bg.png` также условный образ, а не фотография станции. В нескольких выбранных кадрах и по обе стороны стыков монтажной нарезки чёрных кадров не видно; проверка всех кадров, плавности на воспроизведении, звучания и точной синхронизации на слух ещё не выполнена. DATA на выбранном кадре не перекрывает монитор, а компьютер стоит на столе; мобильные безопасные зоны нужно проверить в движении. Ориентиры речи — черновой ASR, а не слуховая проверка; `voice_en.asr_draft.srt` не является финальными субтитрами. Контактный лист выбранных кадров: `../../../Edit/preview_contact_v2.jpg`; в нём отображается вспомогательная сетка инспектора. Рендер и публикация не выполнялись.

## Промпты генерации

Общий референс: `Source/Images/composition_fix/radio_desk_master.png` основного выпуска; встроенный `image_gen`, исходник только читался. Запросы сокращены до финальных требований генерации:

1. `study_bg.png`: «Vertical 9:16 warm Brazilian 1980s study at sunset, same constructed paper diorama, paper fibres, layered dark teal walls, plants, wooden desk and sunset window. Empty desk for composited objects; no radio, cassette, computer, characters, words, borders or corrugated cardboard.»
2. `radio_fg.png`: «One complete 1980s radio cassette boombox, matching the reference, dark copper and black, three-quarter front view, warm upper-left light, isolated on true transparent alpha; no words or border.»
3. `cassette_fg.png`: «One complete 1980s cassette, handmade dimensional paper, ivory labels and black/brown housing, two reels, three-quarter top-down view, warm upper-left light, true transparent alpha, no text or other items.»
4. `computer_fg.png`: «One complete 1980s beige computer with CRT and keyboard, paper-diorama, warm upper-left light, three-quarter front view, dark green screen with abstract data dots, true transparent alpha, no text or brand.»
5. `tape_deck_close_bg.png`: «Vertical extreme close-up of an empty open cassette player mechanism on a wooden desk in the same warm Brazilian paper-diorama room, spindles visible, empty space for separately composited cassette, no text, people, corrugation or blur.»
6. `computer_close_bg.png`: «Vertical extreme close-up of warm paper CRT computer, softly luminous green screen with abstract dots and bars, no words or logos, same teal-and-amber room, handmade depth.»
7. `station_bg.png`: «Vertical exterior of modest 1980s Brazilian radio studio, paper miniature, glowing windows and transmitter mast, dusk, distant era-neutral low-rise buildings. No bridges, famous landmarks, modern skyline, people, text or corrugation; room above for animation.»
8. `wave_fg.png`: «One isolated segmented sound-wave strip of cream and orange paper, bold clear silhouette, texture and subtle edge shadows, centered, true transparent background, no words or objects.»
9. `software_text_fg.png`, `data_text_fg.png`: «Exact word SOFTWARE / DATA, dimensional cream cut-paper letters, warm orange edges, soft physical shadows, reference diorama style, clear readable single line, true transparent background; no other text, objects or borders.»

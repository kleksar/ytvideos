# Harrison — EPISODE (работа в research)

Редакция v01; Nuviko History, Short, product_language=en. 8 ноября 2026 пользователь принял сюжет и поручил полное производство. Эпизод не зарегистрирован; bundle и номер не назначены. Принятая история и точная производственная речь v01 находятся в [исходной записи](2026-11-08-harrison-short-story-v01.md); они не переписываются.

## Narration N001, EN v01

How could a clock tell sailors where they were in the ocean?

In the 1700s, ships far from land struggled to work out how far east or west they had sailed. One answer was time.

When the sun reached its highest point, sailors knew it was noon on the ship. If a clock still showed the time back home, they could compare the two and calculate their position east or west.

But a clock had to stay accurate through a long, rolling voyage. English clockmaker John Harrison spent years working on one that could.

In 1761, his son took Harrison's watch, known as H4, on a voyage to Jamaica. It kept time accurately enough to prove that the method could work at sea.

The ship could use the time back home to help find its place on the ocean.

## Визуальная постановка

[Предварительная постановка сцен](2026-11-08-harrison-visual-development.md); время не привязано, исторические опоры конкретных предметов не проверены. Пилот в [журнале](harrison-visual-pilot/README.md), не принят в монтаж.

## Звук M001

ElevenLabs web, голос `5vsgZsi667xMyGinrNIM`, Odom, Eleven v4, stability 1, similarity 0. Исходный [MP3](harrison-audio/voice-en-v01-raw.mp3): SHA-256 `ba8bb9719ca7983da006eed9442c02e86f7dbb09cb184f3c1978736dab2e1a6a`. [Ускоренный WAV](harrison-audio/voice-en-v01-110.wav): atempo 1.10 ровно один раз; 47.310313 с, SHA-256 `8826aef0daeba08dfcf8f1a54ccfcb832e19a0aa3858ac234fa36bf48530dd4b`. Машинная [карта слов](harrison-audio/alignment-mix-v01.json) содержит 139 слов, механическая последовательность и conform проверены. Прослушивание речи и синхронизации UNVERIFIED.

[Микс](harrison-audio/mix-preview-v01.wav), SHA-256 `d4052da67cad6eb45a5e08ed19b973f5d8d47d71e79034a24c937851edae40db`, 48 kHz mono, включает Thinking Music — Kevin MacLeod, CC BY 4.0, [источник](https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1600060). Для публичного описания необходима атрибуция. Слуховая оценка микса UNVERIFIED.

## Монтаж и проверка

[Версия v02 для просмотра](harrison-review-v02.mp4), SHA-256 `eda2cd33730e1e1c11ea0bf4b68890da9bf3c8f6a24dd91e05e95641ff6b6d4f`; [план](harrison-edit-v02.json), [паспорт](harrison-export-contract-v03.json), [отчёт проверки](harrison-qa-v02/REPORT.md). Видеофайл полностью декодирован без ошибок; проверены кадровая выборка каждой сцены, выбранные смены слов, непрерывность и полнота карты. Два вынужденных смысловых переноса оценены в контексте. Прослушивание и непрерывный просмотр UNVERIFIED; независимая проверка и пользовательская приёмка не выполнялись. Независимое машинное распознавание восстановило 139 слов по порядку, но не заменяет слуховую оценку. Предыдущая v01 хранится как рабочая версия, не актуальная выдача.

В сценах 07–08 исходный референс заменён на фото Jordiferrer с Wikimedia Commons по CC BY-SA 4.0: [происхождение](harrison-visual-pilot/h4-provenance-v02.md). Перед публикацией обеспечить атрибуцию и проверить применимые условия share-alike. Для музыки требуется атрибуция CC BY 4.0. [Черновик упаковки](harrison-packaging-draft-v01.md) не опубликован и не одобрен.

## Следующий шаг

Версия v02 передана пользователю для обычного согласования после повторной проверки точного файла 9 ноября. Для пользовательской приёмки нужен просмотр со звуком. Статус условий CC BY-SA для визуального референса H4 перед выпуском остаётся открытым.

## Повторная проверка перед передачей · 9 ноября

Координатор сверил SHA-256 с замороженным контрактом и полностью декодировал оба потока без ошибок. Параметры: 47,333 с, 1 420 кадров, 1440×2560, 30 кадр/с. Все девять интервалов по монтажному плану 4,83–5,67 с. Осмотрена последовательность с выборкой примерно раз в секунду. В первом кадре одновременно видны часы в руках, палуба и открытое море, вопрос начинается с первой группы субтитров. Далее сопоставляются полдень, часы, работа мастера и испытание. Сохраняется принятый текст и прежняя версия MP4. Эта проверка дополняет [техническую квитанцию](harrison-qa-v02/REPORT.md). Слуховая оценка, непрерывное воспроизведение и независимая проверка UNVERIFIED.

## SRT и обложка

[Английский SRT v03](harrison-en-v03.srt), SHA-256 `8491216ee11e7b865742068a74831372f975a9ad319a324f326bf9ac32f08104`: 12 реплик, 139 слов; структура, буквальное покрытие и границы по карте слов проверены. Воспроизведение и слуховая синхронизация UNVERIFIED.

[Обложка v03](harrison-packaging/cover-v03.jpg), SHA-256 `fd4b5d53ea66356e308ec812c1d790a5fb6c5f1d207832bd37d20a43b958a1b9`, 941×1672; [локальная проверка](harrison-packaging/cover-v03-review.md) включает полноформатный кадр и уменьшенный crop 2:3. Показывает обобщённые часы, а не реконструкцию конкретного H4. В интерфейсе YouTube не проверялась.

## Дополнительная техническая проверка

[Запись проверки звука и источников](harrison-qa-v02/rights-and-audio-v01.md): проверены все hash-привязки рендера и соответствие декодированного звука исходному миксу; проверены публичные условия CC BY-SA и их неопределённая применимость к конкретным сгенерированным сценам. Прослушивание и окончательное лицензионное заключение не выполнялись.

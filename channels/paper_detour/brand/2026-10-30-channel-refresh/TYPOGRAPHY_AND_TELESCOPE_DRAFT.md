# Paper Detour: единая типографика и телескоп — предложение

Этот документ сохраняет историю эксперимента. Актуальные правила для новых материалов — в [едином стандарте типографики](../TYPOGRAPHY_STANDARD.md).

30 октября 2026. Пользователь попросил привести телескоп на баннере к аватарке и согласовать надписи со шрифтом из «видос сессия 1». Таймлайн этой сессии занят; монтаж в рамках этой работы не менялся.

## Что проверено

- В сессии 1 для акцентов используется не подтверждённая шрифтовая гарнитура, а изображения букв и слов, в том числе `../../videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png` и `MATCH.png`. Формы широкие, скруглённые, слегка неровные и без засечек; лицевая бумага светлая, с тёплым нижним слоем и тенями. Полный алфавит и установленный шрифт не подтверждены.
- Эталон телескопа для аватара: `avatar-paper-telescope-v01.png`. Опубликованный `banner-depth-youtube-2560x1440-v01.jpg` содержит другой телескоп и буквы с засечками.
- Исследование и обсуждение изображений в ChatGPT Extra High: https://chatgpt.com/c/6ae4ebe3-819c-83eb-9b6b-a3bf2c5325ea. ChatGPT предложил бумажную типографику, проверку небольшого размера и отдельный эталон телескопа; его утверждение о размерах загруженного в чат JPEG не совпадает с фактической локальной проверкой 2560×1440, возможно из-за обработки изображения при передаче.

## Визуальное направление

Для названия, обложек и коротких видеоакцентов взять один характер букв: крупные округлые и слегка неровные формы без засечек, поверхность бумаги, аккуратная толщина и тени. Цвет букв на баннере одинаковый, как просил пользователь; жёлтый и терракотовый не обязательны для бренда. Проверять надписи в уменьшенном размере. Цвет, регистр и конкретные очертания остаются предметом визуального согласования. Это визуальная система, а не название существующего шрифта или готовый набор букв.

Для действительно идентичного телескопа необходимо сохранить пиксели исходного объекта и использовать единый прозрачный слой; при наложении проверить края, освещение, тень, посадку на поверхность и читабельность перекрытых букв. Генерация по референсу не гарантирует точную копию.

## Эксперименты

- `banner-unified-typography-experiment-v01.png` — баннер с буквами, приближенными к фильму, и телескопом по образцу аватара. Телескоп перерисован генератором и не подтверждён как идентичный. Пользователь одобрил баннер; увеличенная копия `banner-unified-typography-2560x1440-v01.jpg` опубликована. Подробности о текущем аватаре и водяном знаке — в журнале генерации.
- `telescope-avatar-transparent-experiment-v01.png` — генеративное удаление фона; сохранение всех пикселей исходного телескопа не подтверждено, пока не считать эталонным точным вырезом.

Генерация встроенным image_gen; модель не указана. Запрос на баннер:

```text
Use case: compositing. Input image 1: existing YouTube channel banner to EDIT. Input image 2: the AUTHORITATIVE approved paper telescope avatar; use this exact telescope design for the telescope in the scene. Input image 3: actual paper lettering from the film, the authoritative letter-shape and tactile material reference. Primary request: reconcile brand art. Keep image 1's panoramic handmade miniature radio studio, observatory, nighttime sky, lighting, and composition. Replace the central telescope with the same exact telescope from image 2, maintaining its key silhouette, orientation, cream paper body, dark navy rings, coral accents, one large round adjustment knob, and its distinctive short cream-footed tripod; fit it naturally into the paper world and have it sit in front of and gently overlap the paper title, as in the iPhone wallpaper depth effect. Replace the banner's serif title with exactly 'PAPER DETOUR' in uppercase, large rounded chunky slightly hand-cut sans-serif letters whose shapes resemble image 3, with dimensional layered paper, all letters identical light cream color. Do not copy the orange-red thick outline from the film if it fights the banner: lettering must be monochrome, subtle shadows. Text must remain perfectly readable, never obscure multiple letters. Central words and telescope stay near the center and compact enough to fit the middle horizontal strip for a mobile banner. Retain 16:9 framing, no additional text. Restrict changes to title and telescope, no extra stars or fictional symbols, no colored letter in the title, no cardboard corrugation. Natural lighting and contact shadows; no mockup.
```

Запрос на удаление фона:

```text
Use case: background-extraction. Input is the authoritative approved avatar telescope. Remove only the navy background. Keep the exact original telescope intact, matching every pixel, geometry, colors, lens details, orientation, tripod and paper texture. Isolate the whole telescope on a genuinely transparent background. Do not redraw, restyle, modify, crop or add anything; include all tripod feet. No text, no white matte.
```

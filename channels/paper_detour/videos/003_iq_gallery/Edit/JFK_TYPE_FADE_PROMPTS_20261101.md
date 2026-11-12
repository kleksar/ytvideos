# JFK IQ Gallery: текст и fade, запросы и результат

Дата: 1 ноября 2026. Канал: Paper Detour. Это локальный визуальный тест на основе существующей карточки, не полная новая версия ролика.

## ChatGPT.com Extra High

Проектный чат в Google Chrome: [«Драматургический каркас Shorts»](https://chatgpt.com/g/g-p-6ae147d3975777d0-yt-video/c/6ae74b79-d8d0-83eb-8e7f-7d2ab9ea2de0). Перед каждым содержательным запросом видимая маркировка режима была `Extra High`.

### Запрос: типографика

> Ты — консультант в уже открытом ChatGPT Extra High. Не открывай другой ChatGPT.
>
> Одна узкая задача: предложи один точный макет типографики для карточки John F. Kennedy / IQ 119, чтобы исправить именно текст в существующем пилоте. Не создавай ImageGen-промпт и не проектируй анимацию в этом ответе.
>
> Фактические стилевые референсы канала: слова A MESSAGE и MATCH — крупные широкие округлые заглавные буквы, выглядят как вручную вырезанная плотная бумага: светло-кремовая лицевая часть, тёплая оранжевая подложка/толщина и естественная тёмная тень. Официальный канал-референс — бумажная диорама 004 с ночным синим интерьером, мягким янтарным светом, настоящими контактными тенями и видимыми бумажными краями. В текущем JFK-пилоте портрет и индиго-янтарная сцена в целом неплохи, но имя и IQ набраны тонкой кремовой/оранжевой serif-типографикой и выглядят чужеродно.
>
> Дай одно конкретное решение: регистр, разбиение имени по строкам (если нужно), взаимный размер имени и IQ, интервалы, привязка блока к нижней части кадра и обработка букв, чтобы текст был плотным, читаемым на телефоне и визуально родственен A MESSAGE / MATCH. Сохрани сами имя и значение без изменений, не закрывай лицо и не предлагай плакатную плашку. Без вариантов и без общих рассуждений.

Ответ задал три строки `JOHN F.` / `KENNEDY` / `IQ 119`, округлые широкие uppercase sans, кремовую лицевую часть `#F1E3C9`, торец `#C47D45`, мягкую тёмно-синюю контактную тень и отсутствие плашки. В собранном макете строки имеют высоты 82/82/92 px: IQ на 12% выше имени.

### Запрос: fade

> Ты — консультант в уже открытом ChatGPT Extra High. Не открывай другой ChatGPT.
>
> Одна узкая задача: задай простой тайминг появления текста на одной 5-секундной карточке IQ Gallery. Текущая картинка остаётся полностью неподвижной; пользователь просит только fade in / fade out. Текстовый блок состоит из трёх строк JOHN F. / KENNEDY / IQ 119 и должен проявляться и исчезать как единая группа, все строки синхронно и с одинаковой скоростью. Не добавляй сдвиги, масштаб, наклон, покадровую анимацию букв или движение камеры. Дай одно конкретное решение с длительностью fade-in, удержанием, fade-out и характером кривой, чтобы вход/уход были мягкими, но не медленными. Учитывай 30 fps. Никаких других этапов.

Ответ: 5 секунд при 30 fps / 150 кадров; fade-in 0.00–0.30 с (кадры 0–8), удержание 0.30–4.60 с (9–137), fade-out 4.60–5.00 с (138–149); smoothstep/ease-in-out, без overshoot. Три строки используют общий opacity; фон остаётся неподвижным и непрозрачным.

### Запрос: восстановление фона для нового текста

> Ты — консультант в уже открытом ChatGPT Extra High. Не открывай другой ChatGPT.
>
> Одна узкая задача: напиши один короткий английский ImageGen edit prompt для подготовки фона существующего JFK IQ Gallery пилота к новому титру. Работай с приложенным референсом: удалить только две текущие строки тонкого serif-текста, оставить тёмно-индиговую волнистую поверхность под ними цельной и естественно восстановить её бумажную фактуру по соседним участкам. Сохранить в остальном пиксельно как можно ближе портрет, свет, композицию, фон и полный кадр; никаких новых объектов, надписей или замены дизайна. Результат — та же законченная вертикальная 9:16 бумажная картинка, без текста. Верни только один английский prompt, никаких пояснений.

Промпт, переданный ImageGen:

```text
Edit the existing JFK IQ Gallery image. Remove ONLY the two lines of thin serif text (“John F. Kennedy” and “IQ 119”). Seamlessly reconstruct the dark-indigo wavy paper surface beneath them, matching the surrounding paper texture, grain, curves, lighting, and natural shadows. Preserve the JFK portrait, facial features, clothing, composition, colors, lighting, background, and all four edges as close to pixel-identical as possible. Do not redesign, reposition, or modify anything else. Add no objects, lettering, symbols, or decorations. Output the same complete, full-bleed vertical 9:16 handmade paper diorama, entirely text-free.
```

Из очищенного full-frame результата использована только локальная область нижней ленты под старым текстом; портрет в итоговой карточке взят из исходного v02.

### Запрос: прозрачный бумажный титр

> Ты — консультант в уже открытом ChatGPT Extra High. Не открывай другой ChatGPT.
>
> Одна узкая задача: составь один английский ImageGen prompt для отдельного прозрачного PNG с бумажной типографикой JFK IQ Gallery. Это только типографический блок для наложения opacity в короткой анимации; не фон и не сцена.
>
> Три точные строки, строго по центру одна под другой: JOHN F. / KENNEDY / IQ 119. Все три строки — крупные широкие округлые uppercase sans-serif буквы, как в фирменных вырезанных бумажных словах A MESSAGE и MATCH. Лицевая часть одинаковая тёплая кремовая бумага #F1E3C9, заметный оранжево-терракотовый бумажный торец #C47D45 с лёгким смещением вниз-вправо и мягкая тёмно-синяя контактная тень. Физические матовые бумажные буквы с волокнами, слегка неровными краями и одинаковой толщиной. Не serif. IQ 119 всего на 12% выше по буквам, чем строки имени. Не добавлять плашку, фон, рамку, дополнительные слова/цифры или декор. Снаружи букв — настоящая прозрачность. Спеллинг критичен.
>
> Ответь только самим prompt на английском языке, без пояснений.

Промпт, переданный ImageGen:

```text
Create a standalone high-resolution PNG containing ONLY a handcrafted 3D cut-paper typography block on a fully transparent background (true alpha channel).

Render exactly THREE lines of text, horizontally centered on the same vertical axis, stacked with consistent, compact spacing:
JOHN F.
KENNEDY
IQ 119

Spelling, capitalization, punctuation, numbers, and line breaks must be EXACTLY as written.

All three lines must use the same bold, wide, rounded uppercase sans-serif lettering, matching the signature handmade Paper Detour cut-paper typography seen in “A MESSAGE” and “MATCH”. Absolutely NO serif fonts, thin strokes, or conventional digital typography.

Every letter is a physical piece of thick matte cardstock with:
- Warm cream-colored front surface: #F1E3C9.
- Clearly visible orange-terracotta paper thickness and edges: #C47D45, subtly offset downward and to the right.
- Soft, natural dark-navy contact shadows following each letter's physical shape.
- Delicate paper fibers, gently irregular hand-cut edges, realistic material depth, and consistent thickness.
- Warm, subtle directional lighting with no glow or artificial outlines.

The first two lines, “JOHN F.” and “KENNEDY”, must have IDENTICAL visible capital-letter heights. The third line, “IQ 119”, must have a visible capital-letter height exactly 12% larger. Maintain the same font family, weight, material treatment, lighting, and paper thickness throughout.

Center all three lines precisely, with balanced letter spacing and clean, readable gaps between lines. Keep the composition compact, cohesive, visually substantial, and instantly legible on a mobile screen. Preserve the complete visible silhouette, paper edges, and shadows of every letter without cropping.

CRITICAL TRANSPARENCY: Everything outside the physical letters and their subtle shadows must be genuinely transparent (alpha = 0). No solid background, colored background, paper surface, checkerboard pattern, gradient, plaque, banner, frame, scenery, decorative elements, or opaque canvas.

This is a single isolated typography asset intended for synchronized opacity fade-in and fade-out over an existing Paper Detour image.

Output one clean transparent PNG containing ONLY the three exact text lines.
```

## Сборка и проверка

- Исходная карточка: `Source/Images/iq_gallery_flat_card_redesign_20261101/JFK_IQ119_pilot_v02.png`.
- Переходные файлы и готовые выходы: `Source/Images/iq_gallery_type_fade_20261101/`.
- Повторяемая сборка: [`compose_jfk_iq_fade.py`](compose_jfk_iq_fade.py). В отдельном прозрачном PNG хранятся бумажные буквы для вычисления покадровой прозрачности; финальный PNG статичен, а MP4 содержит только один сведённый видеопоток без титровой дорожки.
- Проверка: PNG 1080×1920 просмотрен целиком и в масштабе 360×640. MP4 — H.264, 1080×1920, 30 fps, 150 кадров, 5.000 с; полное декодирование прошло, аудиодорожки нет. В измеренной области текста средняя разница с фоном растёт от 1.7 на кадре 0 до 48.2 при полном появлении, держится на кадрах 9–137 и возвращается к 1.7 на кадре 149.
- Проверены уменьшенные кадры в начале, на полной яркости, в удержании и на выходе. Портрет/фон неподвижны. Это только дизайн-тест: в Palmier не импортировался, в проектной монтажке не собирался и на YouTube не загружался.

## Историческая сцена JFK в открытой машине

После просмотра типографики пользователь попросил заменить абстрактный фон на более живой президентский контекст, предложив машину и исторические кадры. Перед отдельным постановочным запросом в проектном чате Chrome видимая маркировка режима была `Extra High`.

### Запрос ChatGPT Extra High

> Одна узкая задача: предложи одну конкретную композицию для новой цельной карточки John F. Kennedy / IQ 119. Поменять только сцену: нынешний абстрактный фон мне не нравится, хочу более живую президентскую картинку — например, JFK в машине, в историческом контексте. Сделай один ясный постановочный план для неподвижной полноформатной картинки 9:16 в handmade paper/card diorama стиле Paper Detour, сверяя выразительность и бумажную фактуру с точным эталоном 004, 38.08. Сохрани узнаваемость JFK и оставь внизу чистое спокойное место под уже готовый встроенный бумажный титр JOHN F. / KENNEDY / IQ 119. Не предлагай слои, параллакс, движение частей или отдельную титровую дорожку. Избегай сцены убийства, выстрелов, ранения и насилия; не придумывай читаемые надписи или эмблемы. Ответ дай как одно конкретное решение: исторический момент/обстановка, ракурс, расположение персонажа и автомобиля, фон, свет и композиция нижней зоны. Не создавай ImageGen-промпт и не генерируй изображение.

Ответ предложил визит Кеннеди в Западный Берлин 26 июня 1963 года: открытая машина, приветствующая толпа, городская улица; машина по диагонали, JFK крупно и узнаваемо, низ оставить свободным под титр.

### Проверка исторического контекста

- [Bundesarchiv: John F. Kennedys Staatsbesuch in West-Berlin](https://www.bundesarchiv.de/themen-entdecken/online-entdecken/themenbeitraege/john-f-kennedys-staatsbesuch-in-west-berlin/) датирует визит 26 июня 1963 года, описывает поездку Кеннеди с Аденауэром и Вилли Брандтом в открытой машине по Западному Берлину и показывает архивное фото их отъезда из Тегеля.
- [The JFK Library Archives: Digitized Photographs from President John F. Kennedy’s Trip to Germany](https://jfk.blogs.archives.gov/2022/03/01/digitized-photographs-from-president-john-f-kennedys-trip-to-germany/) описывает официальную поездку и каталог White House photos, включая моторкад с Вилли Брандтом и Конрадом Аденауэром и фотографии берлинских толп.

В созданную карточку не вставлялась архивная фотография; это AI-генерированная бумажная реконструкция на основе документированного эпизода.

### ImageGen-промпт для новой сцены

Референсы: `Source/Images/iq_gallery_flat_card_redesign_20261101/JFK_IQ119_pilot_v02.png` только для лица/возраста JFK и `channels/paper_detour/videos/004_last_video/Storyboard/user_reference_parallax_20261101.png` для материала и постановки цельной диорамы.

```text
Create one new complete vertical 9:16 still for the Paper Detour IQ Gallery. Use reference 1 ONLY to preserve John F. Kennedy’s recognizable face, age, hair, and 1960s suit; discard its abstract paper-wave background, pose, framing, and all existing typography. Use reference 2 as the exact material and craft reference for a handmade paper/card diorama: visible cut-paper thickness, matte fibers, hand-cut edges, layered physical depth, natural contact shadows, and richly composed miniature detail. Reconstruct a documented public presidential motorcade in West Berlin on June 26, 1963. Show JFK standing in the rear of an open-top dark official touring car, prominent in the upper center, smiling and raising one hand to greet people. Frame the car diagonally in a three-quarter front view, moving from lower left toward center-right; keep JFK’s full face unobstructed and recognizable. Include two restrained secondary dignitaries in the car, and small but lively groups of welcoming Berliners along both sidewalks. Use period-appropriate 1960s West Berlin street façades in the distance, without identifiable signs or text. Make the scene feel active through the car’s angle, crowd gestures, strong depth, and warm June daylight, while the final image itself remains a single static complete illustration. Color palette: deep indigo paper shadows, cream paper, warm amber daylight, restrained terracotta accents. Leave the lower band from roughly 63% to 79% of image height as quiet, uninterrupted dark-indigo paper roadway/foreground for the existing three-line title to be composited as part of the finished still; keep all people, car parts, and busy details above that band. Full bleed to all four edges. No captions, lettering, numbers, logos, emblems, readable signs, flags, plaques, or borders. No assassination imagery, weapons, injury, blood, or violence. Do not create separate layers or an isolated cutout; return one complete clean text-free 9:16 diorama scene.
```

Результат ImageGen: `Source/Images/iq_gallery_type_fade_20261101/JFK_WestBerlin_motorcade_scene_raw_v01.png`, 941×1672. При сведении в 1080×1920 текст перенесён вниз на 80 px относительно прежней карточки, чтобы не пересекать нижний край автомобиля. Титр использует ранее созданный paper cutout PNG; итоговая still-карточка и MP4 сплющены.

Новые выходы: `JFK_IQ119_Berlin_motorcade_card_v02.png` и `JFK_IQ119_Berlin_motorcade_fade_preview_v02.mp4`; сборка — [`compose_jfk_berlin_card.py`](compose_jfk_berlin_card.py). Полный 5-секундный экспорт декодирован: H.264 1080×1920/30, 150 кадров, без аудио. В Palmier не импортирован; YouTube не менялся.

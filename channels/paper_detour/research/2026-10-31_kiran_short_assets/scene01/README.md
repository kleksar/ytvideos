# Scene 01 — paper newspaper concept

Статус: поисковый мастер DRAFT, 31 октября 2026. Это одна плоская генерация, не готовые монтажные слои и не подтверждение параллакса; на картинке условное пространство, не документальное изображение редакции, статьи, квартиры или места событий. Надписи не создавались. Изображение не импортировано в Palmier и не является итоговым кадром выпуска.

- Результат: `newspaper_master_concept_v1.png`, 940 × 1672 px, SHA-256 `5f0ba4256bb13d597bb3428362865ba34cf5b38441fbf3effdfa8ab917aea4b0`.
- Создано встроенным `image_gen.imagegen` по стилистическому референсу `new_channel/brand/paper_world_reference/paper_diorama_approved.png`, референс просмотрен до создания. Инструмент сгенерировал отдельное новое изображение; PNG скопирован в эту папку без перезаписи.
- Исполнитель: `/root/artist_assets`; прочитаны `.codex/agents/paper_artist.toml`, корневой `AGENTS.md`, `new_channel/RAROVISTA_PRODUCTION_GUIDE.md`, `imagegen/SKILL.md` и черновая партитура `new_channel/research/2026-10-31_young_workers_ai_short_development.md`.

## Полный prompt

> Use case: illustration-story. Asset: one NEW 9:16 portrait concept master for the opening of a Paper Detour video. The input image is solely a visual style reference: a richly tactile handcrafted paper-and-cardboard miniature diorama, photographed like a premium stop-motion set, warm amber lamplight contrasted with cool blue shadows, believable material texture, spatial depth, delicate contact shadows. Do not copy its person, radio, computer or room. Subject and meaning: a neutral folded blank newspaper and a few plain paper pages on an abstract wooden desktop, representing a journalist's reassuring advice. This is a metaphor, not an image of an actual article or place. Composition: foreground lower edge of an entirely blank folded paper, its clean uninterrupted top edge strongly defined for future occlusion; behind it a clearly empty mid-frame area where separate paper letters will later rise; middle plane is the newspaper on the desktop, back plane is soft, simple, softly lit blue paper wall and vague miniature city shapes. Three clearly separable depth planes and plausible shadows; no person or hands. Modern, timeless setting, visually uncluttered, physically plausible material. Strict constraints: no text, lettering, lines resembling print, numbers, illustrations, headlines, logos, labels, symbols, signage or watermark anywhere in the image. Don't pre-render any typographic title. Vertical composition.

## Фактическая проверка

Визуально проверена одна исходная картинка: видны стопка/сложенный бумажный лист, стол, подсвеченная лампа, дальний фон и свободная зона по центру; читаемых заголовков, логотипов и символов не замечено, людей и рук нет. Сложенная чистая стопка может восприниматься как книга или пачка листов, а не однозначно как газета. Силуэт дальнего города и тропическая пальма напоминают стилистический референс: это условная декорация, не место из биографии героини. Проверки соответствия месту и времени не заявляются.

Для возможной постановки требуется отдельно изготовить чистый фон под закрытыми областями, средний слой стола/газеты с контактной тенью и прозрачный передний край для выхода букв из-за него; проверить перспективу, свет, позиции, чистоту маски, реальное перекрытие и перемещение на всём движении. Пока этих вырезок, букв, прозрачных слоёв, озвучки и видео нет; координатное совпадение слоёв и анимация не проверены. Использование в монтаже требует утверждения режиссуры и проверки пригодности в мобильном формате.

## Вариант v2 после замечаний QA

`newspaper_master_concept_v2.png` — новый поисковый мастер, отдельно от v1, 941 × 1672 px, SHA-256 `2b2b11fd6b24b0b773bb19af39e746575e40b22c3dfe2112a4c6ebf0d73f133c`. Создан встроенным `image_gen.imagegen` по тому же просмотренному стилистическому референсу. Это условный бумажный новостной лист, не воспроизведение статьи; отдельные вырезки, подложка и монтаж не подготовлены.

Prompt:

> Create ONE entirely NEW vertical 9:16 conceptual master frame for Paper Detour. Input image is exclusively a reference for physical craftsmanship and lighting: tactile layered cut-paper and cardboard miniature, fine paper fibers, premium stop-motion set photography with warm amber and cool deep blue shadows. Do not copy its room, people, objects, window, city or geographic landscape. Composition: on a simple paper-covered tabletop, a single recognizable newspaper-like news page with an unbroken clean front/top paper edge across the lower-middle frame, positioned so an independent word may later rise visibly from behind it. The page contains only sparse subtle abstract gray horizontal bars resembling columns of print, with deliberately NO letters, numbers, coherent words, logotypes, symbols, pictures, mastheads or fabricated headlines. Visible border and a vertical fold distinguish it from a thick book or stack. The upper half is an unmarked softly shaded paper backdrop with generous clear space for later paper typography. One slightly defocused foreground table edge gives depth; all shadows touch their paper surfaces naturally, consistent soft light from top left. This is a metaphor, not a real publication or documentary image. No people or hands. Absolutely no windows, city, landscape, plants, geographical landmarks, signs, screens, visible text, letters, logos or watermark.

Визуальная проверка одного кадра: газета распознаётся по трём колонкам из абстрактных серых полос, читаемых букв, цифр и логотипов не видно; окна и географические ориентиры отсутствуют; на бумажном фоне достаточно пустого места. Чёткая верхняя кромка листа потенциально подходит для маски, но пока это единое сплющенное изображение. Газета всё ещё выглядит сложенной в несколько листов; качество отделения края, чистый фон за ним, непрерывность контакта с поверхностью, читаемость будущего текста, движение и аудиосинхронизация не проверены. Пропорция близка к 9:16, но файл 941 × 1672 не является 1080 × 1920; окончательное кадрирование согласовывается с монтажом и будущими слоями. Версия не импортирована в Palmier. Независимое QA ожидается.

## Кандидаты слоёв — 31 октября 2026

Исполнитель `/root/artist_assets` просмотрел `newspaper_master_concept_v2.png` и выполнил три встроенных вызова `image_gen.imagegen` по этому файлу. Получены кандидаты, **не прошедшие проверку совместимости с оригиналом**:

- `newspaper_cutout_candidate_v1.png`: прозрачная газета, 941 × 1672, alpha-канал есть, SHA-256 `5834b1e4e7a9c9f4526e884b11675edaff09593f9c362a430ec60da181959d8e`.
- `newspaper_cutout_candidate_v2.png`: повторная попытка с требованием нейтрального края, 941 × **1671**, alpha-канал есть, SHA-256 `604466f5d28048f5d474bf5aca6f825b47d3358391e725ea0d2a98a85da702de`; высота на 1 пиксель отличается от мастер-кадра, поэтому точная регистрация не подтверждена.
- `newspaper_clean_plate_candidate_v1.png`: стол без газеты, 941 × 1672, без alpha, SHA-256 `37f56a1c08e06321c5163d584e4c2c37494516f04e922d00a3c31eb986e4f0a5`.

Визуально газета в двух вырезках находится примерно на месте исходника, а фон сохраняет общую композицию и освещение. Это не доказывает совпадение краёв, рисунка, цвета и положения попиксельно: объекты сгенерированы заново. На прозрачных превью видны жёлтые следы вдоль края; выборочная read-only проверка v2 показала там жёлтый RGB с alpha 1/255 (пример `x=815,y=859`), то есть очень слабую непрозрачность, а не полностью непрозрачную окантовку. Реальный эффект на композите не проверен. Тень газеты удалена, поэтому для естественного контакта нужна отдельная совместимая тень. Вырезки, наложение, чистота прозрачности по всему периметру, регистр и параллакс не проверены в композите или Palmier. Состояние точного соответствия и монтажа — **UNVERIFIED**, а несоответствие высоты v2 — **FAIL** относительно исходного размера. Повторная генерация не устранила видимые в превью цветные точки.

Prompt вырезки v1:

> Extract only the folded newspaper from the provided master image as a transparent PNG foreground layer for compositing. Preserve the exact original newspaper silhouette, size, perspective, location in the full 9:16 canvas, newspaper paper texture, all existing gray bars, fold, lighting and sharp top edge. Keep the original framing and retain the full image canvas; do not zoom, shift, crop, straighten, redraw or embellish the object. Delete the wall, table, background and cast shadow. All non-newspaper pixels must have genuine alpha zero, including the entire upper portion and table. No added text, hands, or logos.

Prompt чистого фона:

> In the provided master frame, remove only the folded newspaper and its cast shadow. Fill the previously obscured area with a natural seamless continuation of the same tabletop texture and light. Preserve EXACTLY the remaining image's canvas dimensions, framing, camera, perspective, table geometry, backdrop, lighting, color and all pixels outside the smallest necessary removal area. This is a clean plate for compositing the original newspaper back at its same coordinates. Do not add any objects, words, symbols, hands, lettering, additional table edges or horizon; preserve the image's upper wall and lower foreground as-is.

Prompt вырезки v2:

> Precise object extraction only: use the attached 941×1672 vertical image as the source. Isolate the original folded newspaper, preserving its existing original shape, exact perspective, printed gray stripe pattern, size, color, positions, edges and full canvas registration. Remove the entire table and wall so all surrounding space is truly transparent. No crop, no zoom, no rotation, no shift, no recreation or sharpening, no recoloring. Transparent background must have clean neutral edge pixels matching the actual newspaper: no yellow, green, white, neon, black outlines, no background remnants or glow. Preserve the original unmodified tabletop-free cutout without shadow. Exact original canvas size and exact position are essential.

## Мастер v3 и новые кандидаты — 31 октября 2026

По замечанию независимого QA создан новый мастер `newspaper_master_concept_v3.png`: вся газета видна внутри кадра; по визуальной оценке боковые поля около 6–9% ширины, точный допустимый диапазон движения не проверен. Видимых букв, логотипов, людей и географических ориентиров нет. Размер 941 × 1672, SHA-256 `262b35f221f6bad0bdd12ef678fa6043f40e6ea2e9ace41f2a4b3ae6978abff1`. Генератор просили разместить газету в центральных 55% ширины, но фактически она занимает существенно больше; поэтому большой запас не подтверждён.

По этому мастеру встроенным `image_gen.imagegen` созданы кандидаты, каждый 941 × 1672:

- `newspaper_v3_cutout_candidate.png` (alpha), SHA-256 `b104fc41e135b9ca0438f1f52d0479a5bd5d913b3c852e91fc062e02d26477c2`;
- `newspaper_v3_clean_candidate.png` (непрозрачный), SHA-256 `4df4834ecdea994289977261a0b3ee69e699d1c38a9dff443c2857ea0aa54851`;
- `newspaper_v3_shadow_candidate.png` (alpha), SHA-256 `a508c1ec2117c0865f0e07c2249add5191df08df6892420918d6b830773389e0`;
- `newspaper_v3_matte_candidate.png` (alpha), SHA-256 `677229aac7ee63ddf5d86dc80639befd985f479738bf54f72a76902ad9ae90de`.

**Проверка — FAIL для заявленной полной непрозрачности.** `sips` подтвердил размеры/наличие alpha; read-only проверка ImageMagick в точке `x=500,y=1000` дала вырезке alpha 253/255 и матту 254/255, в `x=0,y=0` оба alpha 0. Это лишь две выборочные точки, не полная проверка маски. Белая маска на просмотре имеет неровные белые вылезания за края газеты; отдельная тень похожа на широкую размытую форму с вертикальным выступом справа и не проверена на соответствие оригинальному контакту. Размеры совпадают, но точное попиксельное совмещение, качество композита, реальное перекрытие текста и непрерывное движение не проверены. Материалы не импортированы в Palmier. До независимой повторной проверки нельзя считать их готовыми для монтажа.

Prompt мастера v3:

> Create a NEW vertical 9:16 Paper Detour concept master. Input image is only a reference for tactile warm paper-diorama and practical stop-motion lighting, not its scenery. A single recognizably folded newspaper lies on a simple tactile paper desk. The entire newspaper, including all four corners and folded edges, is COMPLETELY INSIDE the frame, occupying only the CENTER 55 percent of image width, with broad clean tabletop margin on BOTH left and right, and clear empty tabletop around every side of it so it can move in parallax without leaving the frame. Place it in lower half below a large empty softly shaded background. Top edge of newspaper clearly visible for future physical text occlusion. Newspaper page shows only anonymous gray horizontal rectangular bars suggesting columns, NO letters, numbers, headings, logos, symbols or images. Three depth planes: clean empty blue paper wall behind, paper table with newspaper in middle, simple foreground table edge. Warm light from upper left and natural contact shadow under newspaper. Do not include any windows, city, landscapes, geographical indicators, identifiable people, hands, screens or real publication. Ensure no part of newspaper touches frame edges, and composition provides substantial margins. No text, no watermark.

Prompt вырезки:

> Precisely extract the original folded newspaper ONLY from this exact master as a transparent PNG layer, with full image canvas and exact original pixel positions. Preserve identical size, orientation, geometry, folds, gray bars, lighting, edge and paper texture. Fully opaque alpha 255 throughout the solid newspaper interior; natural antialiased edge; completely alpha 0 elsewhere. Remove table, wall and cast shadow. Do not crop, shift, rescale, regenerate, stylize or add anything. Canvas should exactly match input dimensions.

Prompt подложки:

> Edit the original frame in place: remove the newspaper and its cast shadow only, fill that region with natural continuation of the existing paper tabletop. Keep the rest of the image unchanged, including exact canvas size, framing, table/wall horizon, camera, lighting and colors. No new items or text. This is a clean plate for an exact foreground overlay.

Prompt тени:

> For the exact newspaper in the given master image create only its original soft contact shadow as a transparent PNG layer registered on the same FULL canvas, in the same position and perspective. Exclude the newspaper, table and backdrop entirely; invisible pixels transparent, shadow softly black/brown semitransparent where it touches table. No outline, no text. Preserve original canvas size, no crop, zoom, rescale or reposition. This is a contact shadow layer for a compositing pipeline.

Prompt матта:

> Create a precise opaque occlusion matte for the newspaper in the attached full-canvas master. Entire canvas transparent except a solid opaque white silhouette in exactly the newspaper's original shape, full size and original pixel coordinates. Inside silhouette alpha must be exactly 255; outside alpha exactly 0 except antialiased boundary. No shadows, no table, no newspaper gray bars, no extra marks; no shift, crop, resize or rotation. Keep original canvas dimensions.

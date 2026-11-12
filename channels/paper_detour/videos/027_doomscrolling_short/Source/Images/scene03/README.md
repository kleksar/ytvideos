# Сцена 03 — печатная мастерская, Paper Detour 027

## Статус: DRAFT / слои НЕ прошли приёмку

Задача: условная бумажная реконструкция мастерской Лондона около 1710 года, не достоверный портрет или документальное изображение издания. Мастер и пробные слои созданы встроенным OpenAI image generation, не CLI. Стилевой референс: извлечённый кадр `channels/paper_detour/legacy/027_doomscrolling_short/Edit/PaperDetour_reference/margorie_12s.png` из фильма Paper Detour 002. Сценарная основа — `Storyboard/LAYER_STORYBOARD_v01.md` текущего выпуска. Последующая полноценная историческая и независимая визуальная проверка не выполнена.

Все PNG имеют 941×1672 px, меньше целевых 1080×1920; при увеличении необходимо проверить резкость. Мастер и фоны RGB, отдельные вырезки RGBA с фактическим альфа-каналом диапазона 0–255. Фоны не содержат повторного станка или человека по выборочному визуальному осмотру. Никакие файлы не импортированы в Palmier.

- `master_1710_workshop_v01.png` — единый мастер, бумажный рабочий рядом с деревянным прессом; руки не видны, количество пальцев не проверяется. Детали силуэта города за окном условны, их историчность неизвестна. Табличек и читаемого текста нет; мелкие штрихи на листе не являются достоверной первой полосой.
- `background_clean_v01.png` — заполненный фон без рабочего и пресса, но с передним столом и балкой.
- `background_empty_v02.png` — вариант без этих передних предметов; заполнение дорисовано генератором, соотнесение света, перспективы и деталей со всем композитом не проверено.
- `foreground_cutout_check_v01.png` — отдельный передний стол с принадлежностями и балкой; требуется сравнить с мастер-кадром и проверить края.
- `press_cutout_reposition_REQUIRED_v01.png`, `press_cutout_adjust_reposition_v02.png` — отдельно вырезанные станки; генератор существенно изменил масштаб и координаты, заново дорисовал детали, несмотря на указание сохранить их. Нужна подгонка и сравнение с мастером, опорой на пол и передним столом. Ни одна версия не считается принятой.
- `worker_cutout_reposition_REQUIRED_v01.png` — отдельный рабочий, генератор сильно увеличил и сместил его, а также дорисовал скрытую часть ног. Нужна подгонка и проверка закрытия передним столом и места опоры; пока не принят.

При попытке более точно выделить человека система imagegen отклонила созданный результат на стадии `output`, категория `other`, ID запроса `3752179b-ac3b-4f64-8c33-bf749b15fcc2`; более подробной причины сервис не сообщил. Новую попытку обхода не делали; ранее возвращённый кандидат сохранён выше. Сборка кадра, проверка крайних положений параллакса, масок, контактов и действия по всей траектории не проводились. В композиции со словами окклюдер и читаемую область ещё нужно проверить. Никакого звука не создавали и не рендерили.

## Исторические ориентиры

- Smithsonian, [Wooden Hand Presses](https://www.si.edu/spotlight/printing-presses/wooden-presses): деревянная рама, винт и длинный рычаг характерны для ранних ручных прессов; направляющие на станине использовались на ранних устройствах. Конкретная геометрия сгенерированного станка как действующая конструкция не проверена.
- Smithsonian, [Franklin common press](https://www.si.edu/object/nmah_882271): английский пресс датирован примерно 1720 годом, то есть это близкий, но более поздний ориентир и не фотография устройства из сюжета 1710 года.

## Точные запросы imagegen

Мастер:

> Create an ORIGINAL vertical 9:16 master composition for the Paper Detour animated short, using the input image ONLY as a reference for its handcrafted paper diorama, dimensional layered cut-paper characters, textures, lighting and coherent scene depth. Scene: a plausible London printing workshop around 1710, before dawn; a full wooden early-English common hand printing press with vertical frame, screw, horizontal lever and guided sliding bed, standing directly on the floor. One period-dressed print worker stands beside it, not touching or gripping anything; a broad wooden worktable with a single plain printed sheet beside the press. Wooden wall, window, shelves of modest supplies behind. A foreground dark wooden beam partly frames the left edge without covering the main subject. Make a single coherent wide composition with clear physically plausible proportions, contact points, matching perspective and directional warm window light. Leave a clean upper area for later separately layered typography. Everything including people and machinery is textured matte cut paper/cardboard with visible layered edges; NOT photorealistic. The sheet is a stylized prop, not a facsimile: no letters, no printed text, no logo or watermark, no photographic pictures, no modern equipment. The setting is an illustrative historical reconstruction, not a documentary photo.

Фон v1:

> Edit this exact master as a production clean background plate. Remove ONLY the standing worker and the large wooden printing press including its handle and base. Reconstruct the hidden wall, empty floor, window, shelves and warm light seamlessly behind them; retain the foreground worktable and left dark beam. Preserve canvas dimensions, scene geometry, position, colors, paper material and camera viewpoint of all remaining elements exactly; no new objects, no text. Historical reconstruction of 1710 London printing workshop. Do not crop. Return full scene without transparency.

Станок v1:

> Extract ONLY the large wooden printing press, including the long handle and the feet/base, from this precise image. Transparent background, full original canvas and exact original location, scale, perspective and lighting. Keep all details of the press precisely unchanged. Remove the person, all room, table, floor, everything else. Do not add anything. Return an actual RGBA transparent canvas; not a checkerboard.

Рабочий v1:

> Extract ONLY the standing male printer with his clothing, hair and full visible body from this precise image. Transparent background, full original canvas and exact original location, scale, perspective and lighting. Preserve his pose exactly, without redraw or moving. Remove all machinery and room and foreground furniture. If part of him is hidden, do not invent or extend it. Return an actual RGBA transparent canvas; not a checkerboard.

Станок v2:

> Isolate exactly the printing press from the supplied source image, preserving all visible pixels of that object without redesign. Output a 941 by 1672 portrait canvas with transparent background. CRITICAL placement: press top roughly x=520, y=607 pixels; press bottom x=850, y=1445; full object including lever occupies x=375 through x=930, y=607 through y=1445. Keep original apparent size and position, do not center or enlarge object. Delete all other objects and room. Real RGBA transparent canvas, no checkerboard.

Передний план:

> Isolate the original left dark vertical wooden frame and the wooden foreground desk from the source image on a full transparent canvas, leaving their exact location, edges and lighting as they appear in the source. Preserve empty gaps transparent, and keep the paper pile, dark pen pot and blank sheet sitting on the table. Do not add text or draw new objects, do not crop or center or enlarge. Real RGBA transparency, no checkerboard.

Фон v2:

> Edit this clean workshop background plate: remove the wooden foreground table, paper pile, pen pot, and dark foreground beam at the far left; extend the matching wooden wall, floor and left part of the window behind them. Keep the existing empty room geometry and all other details precisely in place; do not add any people, press, foreground furniture, text or marks. Preserve full dimensions, camera and directional light.

## Тест совмещения, не приёмка

По прямому запросу координатора созданы два одноразовых статических контрольных композита FFmpeg без обращения к Palmier и без звука. В `test_composite_v01.png` пресс уменьшен до 762×1354 и сдвинут на (212,139), рабочий — до 337×599 и сдвинут на (153,663), затем сверху наложен передний слой. В результате ноги человека визуально оказались на поверхности переднего стола — **FAIL**.

В `test_composite_v02.png` пресс оставлен с теми же параметрами, рабочий увеличен до 385×685 и сдвинут на (145,660), чтобы передний стол скрыл ноги. На выбранном статическом кадре положение головы и корпуса и порядок перекрытия приблизились к мастеру, ноги больше не стоят поверх стола. При этом полная геометрия не идентична мастер-кадру: рукоятка пресса касается правого края и частично обрезается; контактная тень пресса на полу не восстановлена; рабочий и пресс перерисованы генератором, не являются точной пиксельной вырезкой. Фон и передний слой в статике визуально похожи на единую комнату, но крайние положения, мобильный кроп, буквы и работающая механика пресса не проверены. **Комплект остаётся DRAFT, не передавать как готовый к монтажу без исправления и независимой проверки.**

## Новая постановка без человека — v02

После независимой проверки, выявившей недостатки первой композиции и возможную путаницу печатника с героем сатиры, по запросу координатора создана отдельная постановка: `master_no_person_v02.png`. Из неё получены `background_no_person_v02.png`, `press_no_person_cutout_v02.png`, `foreground_no_person_v02.png`. Станок и передний слой — реальные RGBA с alpha 0–255; фон RGB. Все файлы 941×1672. На мастере и пробном композите нет человека, рычаг целиком в кадре, фон без дублирующего станка; бумага без читаемых надписей.

Для статической проверки `composite_no_person_v02.png` пресс уменьшен до 678×1204 и помещён на (192,314), поскольку генератор сдвинул и увеличил вырезку; передний слой наложен без преобразования. Композиция приближается к мастеру, но детали перерисованы генератором. Опоры и тени на поверхности пола, точные края и параллакс не проверены в движении; отдельно проверить теневую подложку, край рычага, буквы, полную механику пресса и исторические особенности. Это DRAFT и не подтверждение приёмки. Файл композита RGB, прозрачной последней колонки нет. Никакого звука или изменений Palmier.

Точные запросы встроенного imagegen:

Мастер:

> Create a NEW original paper diorama 9:16 master shot in the same Paper Detour material and colors as the input reference. Scene: a London workshop around 1710, as an illustrative reconstruction. There is NO person, NO human figure, no hands anywhere. Focus on a single complete wooden early English screw-driven letterpress resting on a wooden floor, large enough to read clearly: wooden upright frame, vertical screw and bed with a small plain inked sheet; full handle visible inside frame. Modest timber room, a window with subtle early morning light, old plain stacks of paper, and one foreground beam at the left edge. Press, floor and shadow share consistent scale, viewpoint and light. Maintain clear separation between background room, press and foreground beam for subsequent depth layers. Leave clean upper wall space for a future separate paper number. Do not show readable text, lettering, logos or watermarks; no modern machinery, no bright white borders, no model of a famous person. All objects appear constructed of textured matte paper and card, visible cut layers, soft cinematic paper shadows.

Фон:

> Edit this exact image as a clean background plate. Remove the printing press, its handle, the near table and the dark wood beam at the far left, and fill behind them with the existing wooden floor, wall, shelves and window. Keep remaining architecture, window, skyline, lighting and camera position unchanged. No people or new objects or text. Preserve the entire 941x1672 canvas.

Пресс:

> Extract ONLY the wooden letterpress from this image to a real transparent RGBA canvas of original 941x1672 size. Keep the scale, position, perspective, handle and geometry matching the master exactly. Include the complete base and the paper on the press bed as a single contact group; remove everything else. Do not crop, invent an extra press, center or enlarge. No checkerboard, no text.

Передний план:

> Extract ONLY the dark wooden beam on left foreground and the foreground table with its paper stack, inkwell and blank sheet from the image. Transparent RGBA full 941x1672 canvas, same original position, shape, proportion and lighting. Remove press and background. Do not crop or enlarge, do not add writing.

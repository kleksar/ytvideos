# Сцена 07 — финал / DRAFT

Встроенный OpenAI imagegen; 941×1672 px. Ориентиры персонажа и комнаты — `../scene01/master_v01.png` и `../scene06/master_v01.png`, визуально просмотрены. Мастер `master_v01.png`: тот же герой в зелёном свитере, сидит за столом и смотрит на рассвет, телефон и блокнот на столе. Волосы, одежда, окно и городская гора согласованы по общему облику; этот кадр с нового более широкого ракурса. Способ удержания лица рукой не идентичен предыдущей позе, что соответствует изменению действия. Пальцы обеих рук частично скрыты, точное количество не подтверждено; глаз и лица в движении не проверены.

`background_clean_v01.png` — заполненный фон без героя и стола; `subject_desk_group_v01.png` — RGBA с героем, стулом, столом, телефоном, блокнотом и растением на столе; `foreground_plant_v01.png` — отдельное RGBA растение и предмет справа. Реальная прозрачность PNG подтверждена: alpha от 0 до 255. Генератор подвинул и увеличил группу относительно мастера и заново дорисовал элементы, точного попиксельного совпадения нет. В стыках свет согласован визуально приблизительно. Группа содержит телефон и блокнот, они не движутся независимо; при необходимости отдельной анимации нужны дополнительные маски. Применять параллакс только с учётом привязки человека и предметов к столу и полу.

`composite_test_v03.png`: статический QA-композит из трёх PNG, группа масштабирована до 847×1505 и помещена на (100,110) относительно полного холста, фон и FG — в исходном положении. Ракурс близок к мастеру, следов второго героя/стола на фоне не видно, предметы располагаются на столе, стол/стул/герой находятся в одной контактной группе. Однако ноги и стул отделены от восстановленного пола без специально рассчитанной контактной тени, а растению не хватает запаса за краями на движение. Проведён просмотр только статического кадра, не анимации; крайние положения, маска слов, мобильный интерфейс, соответствие прочим сценам в движении и реальный звук не проверены. Нужно независимо оценить композицию, устранить соскальзывание и тени; DRAFT, не принят как готовый план. Источник 941 пиксель по ширине потребует увеличения для 1080×1920 и проверки резкости.

`composite_test_v01.png` — ранний технический тест с прозрачной последней колонкой, не использовать. `composite_test_v02.png` — RGB-тест без подгонки размеров группы. `composite_test_v03.png` является статическим тестом, не финальным кадром видеомонтажа; последний композит имеет RGB без прозрачного края. Звук и Palmier не менялись.

## Полные запросы

Мастер:

> Create a new 9:16 master composition for the final shot of the same Paper Detour short. Both reference images show the SAME fictional young man and room; preserve his exact recognizable dark wavy hair, facial features, teal green knit sweater, navy trousers and the same bedroom/desk, window on right, warm lamp, plant on left, recognizable skyline silhouette. One coherent hand-cut paper-and-cardboard diorama, precisely matching the supplied paper material style and color rendering. New intentionally WIDER camera view, not a crop or slight zoom of either reference: the young man sits at the desk in side or three-quarter view and has stopped writing, gazes away from his phone towards the brightening window, hopeful but subtle; one blank notebook and his black phone rest on the desk. Show his body, chair, the full table front, floor and planted foreground leaves for layered depth. His limbs and body must be anatomically coherent with five fingers per hand, his hands are relaxed on the desk. Early morning sunlight through the right window, gentle warm color continuity, dimensional cut paper edges and contact shadows. Include clean open wall area for separately animated lettering. No visible letters, typography, captions, signs or logos. Stable overall composition, accurate support for seated person, notebook and phone; unobstructed narrative objects.

Фон:

> Edit this exact paper diorama master into a clean background plate for later animation. Remove the young man, his chair, the entire desk and all objects on the desk, and foreground plants/furniture on the left and bottom right; fill in behind them naturally with the existing bedroom, bed and floor. Preserve the geometry, angle, position, style and details of the window, sky, city, lamp ambience, wall, shelves and bed; don't add a second person, furniture, text, logo or phone. Same full 941x1672 vertical frame. No transparent background.

Контактная группа:

> Isolate the full contact group from this exact master: the young man, his chair, the desk with its legs and all objects touching the desk including notebook, phone, small potted plant and lamp. Transparent RGBA background. Preserve the exact pose, exact proportions, exact position relative to the original 941x1672 canvas; do NOT center or enlarge the group. Keep all contact points and occlusions correct, do not add anything. No text or checkerboard.

Передний план:

> Extract only the near-left potted plant with all leaves and pot, plus the near-right out-of-focus furniture edge from the original paper diorama image, keeping their exact original canvas positions and original 941x1672 size. Everything else genuinely transparent RGBA. Preserve their paper texture, illumination, proportions and shape without moving, centering or enlarging. Do not add characters, text, watermark or other objects.

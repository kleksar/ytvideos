# Проверка сгенерированных изображений v01 — выпуск 035

2026-11-02 · Nuviko History · 16:9.

**Средство:** встроенный `image_gen` по навыку `imagegen`. Созданы три отдельных черновых кадра; результат осмотрен визуально после генерации. Выбранные файлы скопированы из стандартной папки генератора в `Source/Images/`. Все три — PNG 1672×941 (соотношение 16:9). Это авторский первичный осмотр, не независимая проверка и не финальная приёмка визуалов в фильме.

## IMG-02 — натюрморт основных нужд

**Файл:** [IMG-02_necessities_still_life_v01.png](../Source/Images/IMG-02_necessities_still_life_v01.png) · сцены S01, S05, S24.

- Крупно читаются хлеб, топливо, мыло, вода и свеча; справа есть спокойное свободное поле под графику. Свет/ориентацию можно повторно использовать в финале.
- Генератор добавил миску и ткань, свечной держатель. Они не мешают распознаванию категорий; ткань может рифмоваться со строкой linen в последующем наборе, но на этом кадре всё остаётся недатированным натюрмортом.
- **Статус:** пригодный черновой мастер-кадр. Не точная реконструкция товара/корзины конкретного века. До монтажа проверить кропы S01/S24 и убедиться, что свободная зона справа не пересекает субтитры.

**Исполненный prompt:** IT-01 в [IMAGE_TASKS_v01.md](IMAGE_TASKS_v01.md).

## IMG-05 — Tudor London, общий панорамный фон

**Файл:** [IMG-05_tudor_london_panorama_v01.png](../Source/Images/IMG-05_tudor_london_panorama_v01.png) · опциональная врезка S13.

- Содержит широкую реку, плотный низкий городской силуэт, крыши и множество шпилей; передний план мал и не перетягивает внимание. Современных предметов, текста и явной стройки нет.
- Панорама стилизована в сторону плотного средневекового городского силуэта и не совпадает с конкретным подлинным видом/ракурсом 1540-х. Использовать только как атмосферную авторскую реконструкцию, не как точную картографию, документальный план или свидетельство стройки. Именованные здания не обозначены.
- **Статус:** кандидат для короткой малой врезки за графикой; можно заменить native-design картой, если при детальном просмотре захочется меньше архитектурной конкретики. Не добавлять поверх кадра утверждение о конкретной стройке.

**Исполненный prompt:** IT-02 в [IMAGE_TASKS_v01.md](IMAGE_TASKS_v01.md).

## IMG-07 — строительная площадка позднего XIX века

**Файл:** [IMG-07_victorian_worksite_v02.png](../Source/Images/IMG-07_victorian_worksite_v02.png) · S20.

- Широкий рабочий план, люди небольшие, видны деревянные конструкции, камень и речной фон. Нет текста, сигнальной символики или узнаваемого Crystal Palace. Кадр поддерживает переход к позднему сравнению, но не объясняет его причин.
- Первую версию с крупным куполом не включал в пакет выпускных ассетов. Выбранная v02 заменяет его на невыразительный дальний силуэт; эта точечная правка визуально не разрушила основную композицию.
- **Статус:** пригодный постановочный черновик. Конкретную одежду, подъёмные устройства, леса и стройматериалы надо сравнить с архивными записями перед включением в монтаж. Это не настоящая архивная фотография и не конкретная площадка зарплатной серии.

**Исполненные prompts:** IT-03 в [IMAGE_TASKS_v01.md](IMAGE_TASKS_v01.md); корректировка v02 убирает только купол из skyline.

## Не создавались

- IMG-03 / до Чёрной смерти: сохранена условная схема-карта IT-04; реалистичную рабочую группу не генерировал из-за пробела в предметных референсах.
- Карточки статута, числа, полосы 333/250/176/216/116, множители x2.22/x2.78 и остальные диаграммы: это native-design, не генеративные изображения.
- Ведущий не перегенерировался; использовать существующий референс персонажа 004.

## Пределы проверки

Проверены наличие требуемых объектов, композиция, 16:9, отсутствие текста/логотипов и основные запреты prompt. Не выполнены независимая историческая экспертиза каждого костюма/инструмента, проверка в фактическом монтаже, cold-viewer review или аудит читаемости после наложения субтитров/графики. До решения об использовании кадры остаются черновыми.

## Журнал prompts

Изображения созданы без внешних image inputs; музейные/архивные материалы были текстовыми опорами, их файлы не копировались и не передавались генератору.

**IT-01 — exact prompt:**

> Use case: photorealistic-natural. Asset type: reusable 16:9 landscape still-life image for a historical explainer film, no period claim. Scene/backdrop: a quiet plain room with a sturdy unadorned wooden tabletop, soft natural side light, muted warm earth tones. Subject: four separate everyday necessities, clearly spaced: one simple loaf of bread, a modest piece of household fuel, an unbranded piece of washing soap beside a little water, and one plain candle. Style/medium: original photorealistic cinematic still life, restrained natural materials and believable surface texture. Composition/framing: low three-quarter view of the tabletop; objects sit mostly left and center with generous clean negative space on the right for separately added graphics; 16:9 landscape. Lighting/mood: soft side daylight, calm and understated. Constraints: the objects communicate categories only, not a shopping basket or complete annual budget. No people. Avoid: visible prices, packaging, basket, coins, modern branding, labels, letters, numbers, watermarks, text, logos, decorative clutter, dramatic flames. No copy or imitation of a specific historical artifact.

**IT-02 — exact prompt:**

> Use case: historical-scene. Asset type: optional establishing visual for a Nuviko History film, 16:9 landscape. Primary request: an original photorealistic environmental reconstruction of London in the mid-1540s, based on the broad silhouette in the surviving 1540s London panorama, not a replica. Scene/backdrop: view across the Thames toward a dense low-rise city, layered rooflines and a scattered skyline of church spires, pale overcast daylight. Subject: the cityscape only; at most two tiny anonymous human silhouettes on the near riverbank, indistinct clothing, no visible job or tools. Style/medium: restrained photorealistic historical reconstruction, natural materials, documentary realism, not an old photograph, not fantasy concept art. Composition/framing: wide landscape, river as a horizontal depth cue, city occupies the middle distance, no named landmark framed as a hero subject. Lighting/mood: neutral soft daylight. Color palette: subdued stone, timber, muted roof tones, grey-blue river. Constraints: original composition; generic atmospheric view, not exact street geography; no presenter; no readable text, no signage, no labels, no watermark. Avoid: modern skyline, modern bridges, railway, smokestacks, huge fantasy towers, invented flags, dramatic battle, recognizable named landmark, precise bridge design, construction activity, detailed faces, modern objects.

**IT-03 — exact prompt (first pass):**

> Use case: historical-scene. Asset type: optional 16:9 landscape establishing reconstruction for an English historical explainer, later nineteenth-century London. Primary request: an original photorealistic Victorian-era urban construction site, generic and not a replica of a named location. Scene/backdrop: broad riverside work area with timber staging, stacked beams and masonry, a few small anonymous workers at ordinary manual tasks; hazy London riverfront in the distance. Subject: the scale and texture of a large worksite, with workers present but not individually featured. Style/medium: restrained photorealistic historical reconstruction, documentary composition, not a modern photograph. Composition/framing: human eye-level wide view, believable depth and scale, worksite fills the foreground and middle distance, no hero worker, unidentifiable faces. Lighting/mood: neutral overcast daylight, sober atmosphere. Color palette: muted brown timber, grey stone, soft river and sky tones. Materials/textures: rough timber, worn stone, earth, period clothing kept simple and subdued. Constraints: evoke London construction work between 1850 and 1899 without identifying this as a specific wage-series worksite. No text, signs, labels, presenter, copied faces, logos, watermark, modern equipment, hard hats, factory smokestacks, spectacular steam, named landmarks. Avoid precise replication of Crystal Palace or Victoria Embankment; do not add a dramatic tower or prominent bridge.

**IT-03 — exact edit prompt for selected v02:**

> Use case: precise-object-edit. Edit target: the supplied Victorian London construction-site image. Change only the far-background skyline: remove the large recognizable domed cathedral near the center and replace it with a low, indistinct nineteenth-century urban roofline, preserving the soft haze and overall density. Keep the foreground workers, faces, clothing, timber staging, stacked stone, lifting gear, river, vessels, lighting, color, framing, and all other pixels as close to the source image as possible. Do not add a new landmark, bridge, tower, text, labels, or modern equipment. Preserve the original wide landscape composition.

# Scene 05 — недоступная ступень

Статус: **поисковый мастер DRAFT**, не готовый многослойный кадр и не утверждённый монтаж. Исполнитель `/root/art_story`, 31 октября 2026. Прочитаны профиль `.codex/agents/paper_artist.toml`, корневой `AGENTS.md`, производственное руководство, сценарный пакет и навык imagegen; просмотрен утверждённый стилистический референс `new_channel/brand/paper_world_reference/paper_diorama_approved.png`.

## Файл и происхождение

- `ladder_master_concept_v2.png`: 941×1672 px, RGB PNG, SHA-256 `ac3803132111a4c1f6be0c01dcf705a4f72781f56ac73a2bff007130bbfbca62`.
- Построено встроенным imagegen на основе визуального референса канала, а затем отредактировано встроенным imagegen. Первая генерация оставила досягаемую ступень и персонажа, похожего на эталон; она отвергнута. v2 исправляет оба замечания. Исходная генерация хранится во внутреннем каталоге генератора, в проект не импортировалась.

## Исходный prompt

```text
Use case: illustration-story. Asset: one NEW vertical 9:16 exploratory master composition for a Paper Detour short film; not a portrait or a documentary reconstruction. The supplied image is ONLY a material, craftsmanship and cinematic lighting reference; do not reproduce its character, furniture, room, city, radio, palms, mountains, posters or geographic cues. Build a neutral, abstract theatrical tabletop world from tactile, hand-cut fibrous paper and cardstock. A small anonymous young adult paper figure seen entirely FROM BEHIND stands on a broad flat paper platform and faces a tall freestanding cardboard career ladder in the middle distance; the bottom rung is visibly well above their reach, an intentionally symbolic metaphor. The person's arms are lowered and both hands hidden, face entirely unseen, no identifiable likeness. A simple modern dark thin computer monitor sits to the side, physically anchored to the same platform on its own stand, screen blank, no code or symbols. Clearly separated foreground dark tabletop edge, midground figure/ladder/monitor with proper grounded contact shadows, and a deep softly blurred neutral paper wall background. Leave a generous clear upper area of plain background around the ladder for separately animated words later, with unobstructed silhouette outlines to enable future layered work. Intimate cinematic miniature-set photography, warm amber light from upper left, subtle deep blue-violet ambient shadow, premium handcrafted layered paper; perspective and relative scale internally coherent, no recognizable cityscape, no location cues, no logos, no text, no letters, no watermark. This is a single flattened concept, do not draw compositing guides.
```

## Prompt редакции v2

```text
Edit this existing portrait paper-diorama composition. Preserve exact composition, camera, lighting, blank screen, backdrop, platform, ladder side rails, positions and shadows. Make the visual metaphor unambiguous: remove every ladder rung below the top three rungs, so the lowest remaining rung is well ABOVE the top of the standing person's head and above their full reach; the two vertical ladder rails still touch the floor and are stable. Keep the anonymous person the same small scale and back-facing pose but simplify the head to a completely featureless neutral dark paper silhouette with smooth shoulder-length hair, so it is NOT the recognizable person from any previous reference. No visible face or hands, no text, logos, symbols, labels, landmarks, cityscape, or watermark. This is an anonymous symbolic figure, not a depiction of any real person. Keep the same physical tactile cardstock and warm-left/cool-right light.
```

## Фактическая визуальная проверка

На v2 нижняя ступень существенно выше головы фигуры; фон абстрактный, узнаваемой географии не видно. Фигура со спины без лица; это условный персонаж, не портрет Kiran Maya Sheikh и не её подтверждённая одежда. Экран пуст, видимых надписей и логотипов не обнаружено. Пятки фигуры, опоры лестницы и подставка экрана соприкасаются с поверхностью; общая светотеневая схема визуально согласована. Руки примыкают к телу и индивидуальные пальцы не читаются; в этом разрешении нельзя подтвердить их анатомию для крупного плана. Лестница и персонаж — метафора, её нельзя интерпретировать как доказательство отсутствия стартовых работ повсюду.

**Ограничения:** PNG плоский: раздельных прозрачных переднего плана, лестницы, экрана, фигуры и заполненного скрытого фона, отдельных масок, движения и зерна нет. Слои, границы вырезок, параллакс, крупноплановые пальцы и непрерывность со смежными кадрами не проверены. Предполагаемый порядок — абстрактная стена → лестница/фигура/экран → будущие бумажные слова → маска края соответствующего предмета → край стола; позиции и тени надо отдельно согласовать при подготовке настоящих слоёв. Файл ещё не импортирован в Palmier и не является финальным ассетом.

## Пробное разделение на слои — 31 октября 2026

Исходник `ladder_master_concept_v2.png` повторно просмотрен перед обработкой. Все три файла созданы встроенным imagegen; мастера и чужие файлы не изменялись. Это **кандидаты, не принятые как совместимые монтажные слои**.

- `figure_ladder_alpha_candidate_v1.png`: 941×1672, RGBA, SHA-256 `afed0aaa922ee36dcb3c0e0e07986788f3fd64bd7a1126ba7d03936953e9401c`. Прозрачность подтверждена проверкой альфа-канала (`0..255`; 1 110 601 полностью прозрачных пикселей). Визуально изображение сильно увеличено и сдвинуто по сравнению с мастером; края имеют заметные цветные остатки. **FAIL** для совмещения без новой обработки.
- `figure_ladder_alpha_candidate_v2.png`: 941×1672, RGBA, SHA-256 `9950d484d195292629bbfeb6548a19092dd3e2188582696d8774eae2b2f51062`. Прозрачность подтверждена (`0..255`; 1 351 244 полностью прозрачных пикселя). Визуально положение фигуры ближе к мастеру, но лестница и ступени имеют смещение/изменение масштаба и формы; по краям видны красные и жёлтые остатки. Ненулевая альфа распространена почти по всей рамке: bbox `(74, 19, 927, 1640)`, что указывает на возможные изолированные остатки; все они отдельно не исследованы. Точное наложение на мастер **FAIL/не гарантировано**, альфа-края требуют исправления.
- `clean_plate_candidate_v1.png`: 941×1672, RGB, SHA-256 `d78419537aee38f9ea5da6473ee84e55e19dd369966a42eece49027376e23b37`. Визуально фигура, лестница и их тени удалены, поверхность и фон заполнены, монитор и его опора сохранены примерно в исходном положении. **UNVERIFIED:** точная пиксельная идентичность оставшейся сцены и незаметность заполнения в движении не проверены.

Контактные тени фигуры и лестницы в альфа-слое отсутствуют; при оживлении необходимы отдельные совместимые тени или иное проверенное решение. Данные слои не импортированы в Palmier. Тестовый композит и параллакс не выполнялись: край, физический контакт, дрожание и цвет в движении не подтверждены. Одинаковое разрешение само по себе не гарантирует совпадения.

### Prompt вырезки v1

```text
Background-extraction edit of the exact input image for a vertical film composite. Isolate ONLY the existing entire cardboard ladder (both side rails, exactly three high rungs, its feet) AND the existing small rear-view paper figure (body, hair, clothes, shoes) together as ONE image layer. Preserve their exact appearance, posture, proportions, perspective, scale and original pixel positions relative to the full 941×1672 portrait canvas; do not crop, resize, redesign, add or move anything. Remove the wall, floor, monitor, table edge and all cast shadows; all removed areas, every gap in the ladder and all empty space between objects MUST have genuine fully transparent alpha, not a checkerboard or colored fill. Preserve natural clean anti-aliased edges and warm lighting. Do not add text or symbols. This is a precision cutout, not a new illustration.
```

### Prompt вырезки v2

```text
Make an exact-position transparent-background extraction from this input portrait frame. Preserve the full 941x1672 canvas, DO NOT zoom or enlarge the subject, DO NOT crop margins. Pixel positioning is essential: the small person should remain at approximately x=138..311, y=836..1364; the ladder should remain approximately x=313..663, y=224..1292. Preserve scale, position, pose, silhouette and original texture of the combined person and all parts of the ladder including the three rungs. These two objects together fill only the central left region of the full canvas; maintain wide transparent margins at the top, both sides and bottom. Remove all other pixels (wall, floor, screen, shadows, tabletop) to actual alpha transparency, including the empty spaces inside the ladder, and leave no colored outline, residual pixels or checkerboard. No redesign, no text, no extra objects. Precision isolated layer, not a new composition.
```

### Prompt clean plate

```text
Precise clean-plate edit of the exact provided 941×1672 vertical paper diorama frame. Remove ONLY the entire central cardboard ladder and the person standing at lower left, including their cast and contact shadows. Fill the exposed spaces invisibly with a seamless continuation of the existing softly textured neutral purple-blue background wall and warm amber paper floor, consistent with adjacent areas and the original light from upper left. Preserve the existing monitor at the right, its stand and its own original shadow exactly in position, size, design and color; preserve the floor horizon, foreground dark tabletop edge, camera, lighting, texture, aspect ratio and every part of the original scene not occupied by the removed ladder/person. Keep full original framing and canvas, no crop or scale. No replacement objects, no people, no ladder, no text, logos, arrows or patterns; produce a clean background plate for a later movable foreground.
```

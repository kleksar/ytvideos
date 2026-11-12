# Paper Detour033 — S05/S06/S07/S09

Дата: 2026-11-01. Исполнитель: paper_artist /root/time_stop_metaphor_images.

Входы: [принятая раскадровка](../../Storyboard/STORYBOARD_v01.json), [визуальная библия](VISUAL_BIBLE_v01.md), пользовательски принятый [S01_v01.png](../Images/paper_v01/S01_v01.png). Указание продолжать13сцен и действующее исключение Extra High для этой адаптации прочитаны; новый сюжет/наррация не разрабатывались.

Встроенный image_gen, отдельный вызов на каждый asset, transparent_background=false. Все генераторные оригиналы сохранены, в Source/Images — точные копии без изменения пикселей. Локальные scenePNG не импортировались в Palmier.

Все4фактических canonicalPNG открыты целиком через view_image после копирования, и отдельно ранее осмотрен S01. Это авторская проверка, не independent review. Руки/лица/обувь/частицы и основания рассматривались в полном нативном изображении; отдельное увеличение/zoom деталей и phone-size composite с акцентами в этом проходе не выполнены. До разрешения импорта требуется закрыть эти проверки у координатора/reviewer; пользовательской приёмкой новых4файлов не объявляются.

## S05

- Файл: [S05_v01.png](../Images/paper_v01/S05_v01.png), 941×1672 RGB opaque PNG, ~9:16 с нативным округлением.
- SHA-256: `793f83bff15f0ca33ea10071c50b0de113df9392d43786be07aca247d7751da9`.
- Generator source: `/Users/diplomat/.codex/generated_images/01a19945-d9c3-72c0-b88d-75c12fcedb7a/exec-ee52607a-b03d-40cc-aac1-6c38d4ab6b3d.png`.
- Image references: S01_v01.png.
- Авторская оценка: **ACCEPTED_FULL_FRAME_CANDIDATE / DETAIL_ZOOM_AND_CUE_QA_UNVERIFIED**. Нерегулярные бумажные круги на заднике с основанием; три короткие дуги слева не пересекают модель. Видимых связей/кристалла нет, фактура и контакт основания читаются.

### Exact prompt

```text
Use case: illustration-story. Asset: one complete static full-bleed opaque vertical 9:16 Paper Detour scene PNG, no panel borders.
Input image 1 is the USER-APPROVED MATERIAL, COLOUR AND DIORAMA STYLE reference S01. Match its tactile cut/folded cardstock, layered paper edges, visible fibres, deep navy shadows and amber practical light, dimensional handmade miniature photography. This is a new shot in exactly that crafted world. No live-action person, smooth CGI, vector cartoon, lettering, symbols, numerals, labels, watermark, UI or captions. Keep a quiet upper area for a later separate paper title; don't render that title.
Primary request: a close macro view of a handmade explanatory model of motionless air, not a literal crystal. A deep-navy textured paper backing mounted on a low paper plinth fills the image. In the lower two thirds, small cream and blue-grey layered paper circles are placed in a deliberately irregular, uneven, non-grid scatter, supported invisibly against the backing at varied shallow depths. On the left only, three short nested amber paper wave arcs on the same backing stop before the field of circles; no arcs crossing the model. The circles have NO rods, bonds, connectors, lines or lattice between them. No ice, glass chamber, cage, scientific apparatus, clouds, human figure or street shown in this abstract explanatory insert. Warm amber side-light catches cut edges and casts tiny natural shadows on navy backing, matching the reference craft and lighting. The model is plainly supported on its plinth, not free-floating random debris. Full image is a single finished still.
```

## S06

- Файл: [S06_v01.png](../Images/paper_v01/S06_v01.png), 941×1672 RGB opaque PNG, ~9:16 с нативным округлением.
- SHA-256: `d8d964678dade5baafbb89da93916c121c1ee0bee9092d9cd7d3f5376c499805`.
- Generator source: `/Users/diplomat/.codex/generated_images/01a19945-d9c3-72c0-b88d-75c12fcedb7a/exec-c7e58aad-a878-4630-b7da-aa3a4c6e56a2.png`.
- Image references: S01_v01.png + S05_v01.png (только форма частиц).
- Авторская оценка: **ACCEPTED_FULL_FRAME_CANDIDATE / DETAIL_ZOOM_AND_CUE_QA_UNVERIFIED**. Герой/поза/волосы/поднятая правая ладонь/опущенная левая/обе стопы сохраняют S01. Два человека, велосипедист слева, лампа/фасад/сток справа и главная капля у носа на месте. Частицы — условные бумажные диски, видимых связей/клетки нет. Камера получилась близка S01, хотя prompt просил немного шире; отдельная композиция определяется появлением модели воздуха.

### Exact prompt

```text
Use case: illustration-story. Asset: one complete static full-bleed opaque portrait 9:16 Paper Detour film still, no borders.
Input image 1 = exact USER-APPROVED HERO, STREET, FROZEN BODY POSE AND CRAFT STYLE. Input image 2 = explanatory air-particle model reference only; borrow its irregular cream/blue paper disks, not its plinth or wave symbol.
Create S06, the air-is-the-trap revelation. Same young dark layered-paper-haired man in ochre hooded jacket over dark shirt, dark trousers and cream paper sneakers. Precisely retain his standing foot placement, open right palm lifted near face/shoulder and left arm down as in image1; face points SCREEN-RIGHT. No walking or touching. Frame a slightly wider full-body three-quarter view from the SAME side of the street, never mirror him. Keep main raindrop in front of nose on right, about20cm away at nose height. Keep blue-grey helmeted cyclist with dark backpack on dark bicycle behind him at left, facing right; exactly TWO people.
Same deep-navy evening street: right brick facade, big warm lamp upper-right, curb/drain bottom-right, right plant rooted in its pot, left houses/tree, amber windows and distant blue city silhouettes. The character, cyclist and suspended droplets remain in their original physical positions.
Now reveal a VISUAL EXPLANATORY MODEL of invisible air: numerous small flat handmade cream/blue-grey layered-paper disks, irregularly and closely scattered in the SPACE AROUND the hero, including in front of his shoes and open palm. They sit at varied shallow depths on a concealed dark backing. They surround his silhouette without covering face/hand identity. No bonds, lattice, rods, bars, chains, crystal, glass cage or force-field. It is a paper visualization, not a new object trapping him. Maintain visible card fibres, folded jacket and cut hair, macro-diorama depth. Cooler dim navy light yet readable, sparse amber edge light matching reference. Quiet dark upper area for later separate accent; NO text, labels, numbers, logos, watermark or UI. One coherent finished paper diorama, no separated layers or panels.
```

## S07

- Файл: [S07_v01.png](../Images/paper_v01/S07_v01.png), 941×1672 RGB opaque PNG, ~9:16 с нативным округлением.
- SHA-256: `dba338bac4a9c1c12a34a4d6dd3a98d88fed56d3877bc61d83606138d98a82e8`.
- Generator source: `/Users/diplomat/.codex/generated_images/01a19945-d9c3-72c0-b88d-75c12fcedb7a/exec-d973a1c8-0b48-4968-9fa1-a8bb99681afe.png`.
- Image references: S01_v01.png + S05_v01.png (только форма частиц).
- Авторская оценка: **ACCEPTED_FULL_FRAME_CANDIDATE / DETAIL_ZOOM_AND_CUE_QA_UNVERIFIED**. Два кремовых кроссовка, оба стоят на брусчатке без поднятого носка/пятки; ближний левее, дальний впереди справа, как в S01. Сток/бордюр справа, тёплая лампа/синий фон и бумажные брюки совпадают по миру. Частицы перед носками не раздвинуты. Самая задняя часть ближней обуви уходит за левую границу close-up; оба носка и контакты подошв видны.

### Exact prompt

```text
Use case: illustration-story. Asset: one complete static full-bleed opaque portrait 9:16 Paper Detour film still.
Input image1 = exact USER-APPROVED HERO SHOES, STREET, FROZEN BODY POSE AND CRAFT STYLE. Input image2 = explanatory paper air-particle model reference only.
S07 low macro close-up of the same man's lower dark paper trouser legs and BOTH cream handmade paper sneakers, both soles firmly planted on the SAME wet cobblestones. Preserve the relative stance from image1: near left shoe slightly closer to camera, far right shoe farther forward pointing screen-right. This is only a closer camera, not a foot movement. Do not lift heel/toe, take a step or turn the body. Sneakers' layered cream card, laces, sole edges and trouser fibres match image1. Natural sole contact shadow and tiny wet reflection under each shoe.
The same wet navy/amber cobbled street and right-side curb with black drain visible in depth, same warm windows and right brick facade softly blurred above. In the empty air immediately in front of the toe tips, irregular small cream and blue-grey layered paper disks like image2, closely spaced but not in a grid, supported against hidden backing at different shallow depths. They illustrate locked-in-place air; none move aside. No connectors, crystals, ice, chains, cuffs, cage, new props or visible support rods. No extra feet. Keep a quiet upper navy background area, shoes fill the lower half to two thirds with both shoes fully readable. Full image physical handmade paper miniature photography with navy shadows, warm amber edge light and visible fibres, no smooth CGI/live action/vector. No lettering, numerals, symbols, captions, logo or watermark. A single finished still.
```

## S09

- Файл: [S09_v01.png](../Images/paper_v01/S09_v01.png), 941×1672 RGB opaque PNG, ~9:16 с нативным округлением.
- SHA-256: `e05cee51ce263bd9bf30a58ff08ab8854be754de5ddff782a3adfb8d9bdfb97a`.
- Generator source: `/Users/diplomat/.codex/generated_images/01a19945-d9c3-72c0-b88d-75c12fcedb7a/exec-7ed55628-1580-44d4-867d-eb87b69f6eda.png`.
- Image references: S01_v01.png.
- Авторская оценка: **ACCEPTED_FULL_FRAME_CANDIDATE / DETAIL_ZOOM_AND_CUE_QA_UNVERIFIED**. Один бумажный жук внутри медово-янтарных слоёв, шесть ног и два усика читаются в полном просмотре. Есть основание/контактная тень, видимые края/волокна, нет человека/смолы/стекла/текста. Глубина переднего полупрозрачного слоя тонкая; не выдаётся за научную реконструкцию янтаря.

### Exact prompt

```text
Use case: illustration-story. Asset: one complete static full-bleed opaque vertical 9:16 Paper Detour scene PNG, no panel borders.
Input image 1 is the USER-APPROVED MATERIAL, COLOUR AND DIORAMA STYLE reference S01. Match its tactile cut/folded cardstock, layered paper edges, visible fibres, deep navy shadows and amber practical light, dimensional handmade miniature photography. This is a new shot in exactly that crafted world. No live-action person, smooth CGI, vector cartoon, lettering, symbols, numerals, labels, watermark, UI or captions. Keep a quiet upper area for a later separate paper title; don't render that title.
Primary request: a close macro explanatory SIMILE of one small paper insect embedded inside a honey-amber layered translucent-paper volume resting securely on a low navy paper base. An irregular warm amber rounded chunk built from many visibly hand-cut translucent tissue-paper sheets; its edges reveal fine layered fibres. In its central interior is ONE small dark paper beetle, anatomically simple with six thin paper legs and two short antennae, visible THROUGH the translucent honey sheets. The insect must read as inside the volume, not sitting on its front surface. This is a handcrafted amber metaphor, not a real resin photograph or polished glass ornament. No human or trapped man. No street, labels or symbols. Navy textured paper background and warm amber edge light, supported base and natural contact shadow, quiet upper third. One coherent completed static diorama with the same cut-paper material finish as the reference.
```


# S03/S04/S08/S10 — built-in image_gen

## Фактический результат и self-review

2026-11-01. Пять встроенных image_gen вызовов: четыре исходных кадра и одна адресная правка S04. Все PNG скопированы без обработки из generator output в canonical Source/Images/paper_v01; оригиналы оставлены на месте. Все941×1672, RGB, непрозрачные, полноформатные; это нативные PNG, не экспорт1080×1920. Ресайз/кроп/растягивание не выполнялись.

| Кадр | Выбранный PNG | Статус self-review | SHA256 |
|---|---|---|---|
| S03 | [S03_v01.png](../Images/paper_v01/S03_v01.png) | ACCEPTED_FOR_INDEPENDENT_REVIEW | `0889abab4189c4b767b86dbcf2df445dc1cc4b66f11462d96c554a3bdca6a45d` |
| S04 | [S04_v02.png](../Images/paper_v01/S04_v02.png) | ACCEPTED_FOR_INDEPENDENT_REVIEW | `06b4e747c2bd64ecb566008cd622f2fa70be17b67b162c26ff13b53365b18c83` |
| S08 | [S08_v01.png](../Images/paper_v01/S08_v01.png) | ACCEPTED_FOR_INDEPENDENT_REVIEW | `51f37f7e7e447351814f9ea19a75b2be2eb18ac9226e742b347e95b3eed7ec06` |
| S10 | [S10_v01.png](../Images/paper_v01/S10_v01.png) | ACCEPTED_FOR_INDEPENDENT_REVIEW | `0fb6b766069a15d40bf1ea96adc694812a6abff2f7b77cd21440b031d59bbbab` |

S04_v01 сохранён как источник предыдущей версии; REJECTED_CURRENT_SELECTION из-за плохо различимого велосипедного звонка. SHA256 `4d674afb465cb13e0ff970e05632f90efbff90bb5f48b3a170af799bb5eede87`. В v02 добавлен маленький серебристо-серый звонок с основанием на существующем руле; остальная композиция при повторном просмотре сохранена.

Просмотр: S01 реальным view_image перед генерацией; затем каждый из пяти canonical PNG отдельно через view_image целиком. Лицо/волосы/ухо занимают значительную часть крупного плана, видны бумажные волокна и слои. Дополнительное увеличение/отдельные detail crops не выполнялись. Не заявляю их выполненными. Рассмотрены следующие фактические области:

- S03: открытый матовый чёрный глаз без отражения, профиль вправо, ухо/шея прикреплены, тёмно-синее фактурное пространство перед лицом. Нет лучей/фотонов/надписей. Тёплая окантовка — зрительская внешняя постановка. Фактический план — крупный профиль головы/глаза, не изолированный глаз.
- S04: ухо на голове, шея/капюшон/плечо соединены; та же бумажная причёска и юный профиль вправо. Велосипедист один, на заднем левом плане направо, звонок в v02 различим маленьким куполом на руле. Его мелкий рычажок и точные велосипедные контакты отдельно не увеличены. Ладонь героя у правого края естественно обрезана, точный счёт всех пальцев из этого кадра не заявлен.
- S08: рот слегка открыт, чёткий зазор до бумажных сине-серых дисков воздуха. Диски нерегулярны, без соединений/решётки; ни один не входит в рот/ноздрю. Капюшон, лицевая бумага, волосы и часть исходной поднятой ладони сохранены; нет удушающих рук/разреза тела/смерти. Частицы — объясняющая метафора, не предметы новой физической сцены.
- S10: один главный стекловидный дождевой объект перед носом справа, заметный зазор, масштаб относительно головы сопоставим с S01. Не касается героя; нет пальца/трещины/камня. В глубине кирпичный фасад справа, янтарные окна и синяя мокрая улица. Герой не состарен.

Во всех выбранных картинках видны материальные бумажные края/фактура; текстов, пустых страниц/экранов и посторонних аксессуаров нет. Одежда/лицо соответствуют принятому S01. Наложенных акцентов пока нет: phone-size cue fit, точная caption safe area, звук/AV sync и монтаж не проверялись. Это self-review автора четырёх картинок, НЕ независимая проверка и НЕ пользовательское принятие этих четырёх версий.

## Источники tool output

Все находятся в `/Users/diplomat/.codex/generated_images/01a19945-ad14-75a2-ad37-0a26332a9075/`:

- S03_v01 — `exec-d880f0aa-0a2d-448a-950f-1479a779a2c6.png`.
- S04_v01 — `exec-990bed99-b070-4fcc-be49-36ef70b0993f.png`.
- S04_v02 — `exec-d48058bb-799b-4501-9ae1-12285fd4dc04.png`.
- S08_v01 — `exec-514cfeb3-771c-4c85-b51a-190fb871b814.png`.
- S10_v01 — `exec-87990cf4-c29f-4bd8-80fc-83aabd597c00.png`.

## S04 v02 targeted edit prompt

Причина: в v01 звонок у руля велосипеда в глубине плохо различим рядом с рукой. Только конкретная правка звонка, без изменения героя/географии.

```text
Use case: precise-object-edit.
Image 1 is the edit target S04. Image 2 is the accepted S01 identity/style reference only.
Change ONLY one very small detail in image1: on the existing background cyclist's bicycle handlebar at the left background, add a clearly recognisable small domed silver-grey PAPER bicycle bell physically attached beside his right hand. It must remain appropriately tiny for the distant bike, with a small base and lever, readable as a bell rather than an extra hand. No magnified insert, no giant bell, no additional objects.
Preserve EVERY other part of image1: same exact portrait canvas, paper character face/ear/hair/clothes, raised hand position at right crop, frozen cyclist and bicycle position heading right, rain, buildings, navy and amber colours, lighting, focal depth, texture, composition, no text.
Keep a single complete opaque full-bleed portrait9:16 PNG. Do not recompose or change the hero, do not add symbols or typography.
```

## S08 prompt

```text
Use case: illustration-story.
Asset type: one finished static portrait 9:16 full-bleed opaque PNG for Paper Detour 033.
Input image 1 is the USER-ACCEPTED reference for exact hero identity, handmade paper material, rainy street geography, and lighting vocabulary. Build a new camera composition from that same physical paper diorama, not a new character or location.
Hero: same young adult man, clean youthful face, small plain black paper eye, short dark layered paper hair, ochre brown paper hooded jacket over dark shirt. Preserve actual facial proportions and hair silhouette of image1. He faces screen-right. His body has not moved during the freeze; his right open palm remains raised near shoulder/face and other arm down, only crop hides it where necessary.
Medium: richly tactile handmade cut and folded paper/card miniature, visible fibres, layered torn cut edges, dimensional paper face/hair/clothing, physically grounded shadows and shallow miniature depth. Same navy blue and warm amber vocabulary as reference, cooler dim external explanatory lighting during stopped time. Viewer sees the external paper model; this is not the man's literal vision.
No text, letters, numbers, subtitles, logos, watermark, border, collage, split panel, transparent bands. No smooth CGI, real person photography, flat vector drawing. Do not add phones, watches, glasses, jewellery, extra people, light rays or magic symbols. Leave calm upper area for later separate editorial accent.
Scene S08: close side profile from the same man's nose to upper chest, facing RIGHT, exact youthful paper face and ochre hood from reference. His mouth is very slightly parted, his expression alert and puzzled rather than choking or dying. Only the camera moves: his original raised open right palm may appear near right edge at the original shoulder/face level, not moved to his throat or mouth. Outside his nose and mouth is a quiet, irregularly spaced field of small layered blue-grey round PAPER DISCS: an explicitly explanatory miniature model of frozen air. These are attached to an invisible dark backing, with no visible stands or connecting bonds. All particles stay OUTSIDE the body with clear space from lips/nostril; no particles enter the mouth or nose, no inhalation arrows or stream. Irregular placement, not a crystal or ice lattice. Dim navy rainy street depth and warm paper rim recall the same reference street. The image means air cannot be drawn in. No cutaway anatomy, lung diagram, hands choking, collapse, gas cloud, dust spray or death. Full complete diorama, room above for later separate text.
```

## S10 prompt

```text
Use case: illustration-story.
Asset type: one finished static portrait 9:16 full-bleed opaque PNG for Paper Detour 033.
Input image 1 is the USER-ACCEPTED reference for exact hero identity, handmade paper material, rainy street geography, and lighting vocabulary. Build a new camera composition from that same physical paper diorama, not a new character or location.
Hero: same young adult man, clean youthful face, small plain black paper eye, short dark layered paper hair, ochre brown paper hooded jacket over dark shirt. Preserve actual facial proportions and hair silhouette of image1. He faces screen-right. His body has not moved during the freeze; his right open palm remains raised near shoulder/face and other arm down, only crop hides it where necessary.
Medium: richly tactile handmade cut and folded paper/card miniature, visible fibres, layered torn cut edges, dimensional paper face/hair/clothing, physically grounded shadows and shallow miniature depth. Same navy blue and warm amber vocabulary as reference, cooler dim external explanatory lighting during stopped time. Viewer sees the external paper model; this is not the man's literal vision.
No text, letters, numbers, subtitles, logos, watermark, border, collage, split panel, transparent bands. No smooth CGI, real person photography, flat vector drawing. Do not add phones, watches, glasses, jewellery, extra people, light rays or magic symbols. Leave calm upper area for later separate editorial accent.
Scene S10: extreme close SIDE view of the same man's face looking RIGHT on the left part of the image, with the SAME single suspended glass-like raindrop separated from his nose toward screen-right at nose height. Preserve the reference drop's scale relative to his head: a SMALL teardrop about one tenth of his visible head height, with a gap of roughly 20cm in the represented miniature world (about one head-width). Do NOT make it gigantic or touching his face. The drop has the same accepted clear blue/amber reflective finish as image1; hidden suspension, no visible string. It is the focus of the open space directly in front of his nose, not a different stone, metal or ice object. Same layered dark paper hair, youthful profile and ochre hood partially visible at bottom-left. The dim depth contains the SAME right-side brick facade/amber window and blue rainy paper street, no new location. Tight crop hides his raised hand naturally; no finger touches or pushes the drop, no fracture, no motion blur. Upper part calm for a future separate accent, NO text in this PNG.
```

Входы: принятая раскадровка и VISUAL_BIBLE_v01.md; основной image reference во всех вызовах — `Source/Images/paper_v01/S01_v01.png`, SHA256 `700b11da5d3c4c0bc1032eb1f48b3bdb7373378865b94cdf33184e9921b048f0`. Пользователь принял S01 и поручил остальные13. Исполнитель /root/time_stop_closeup_images. Новые картинки не являются пользовательски принятыми.

## S03 prompt

```text
Use case: illustration-story.
Asset type: one finished static portrait 9:16 full-bleed opaque PNG for Paper Detour 033.
Input image 1 is the USER-ACCEPTED reference for exact hero identity, handmade paper material, rainy street geography, and lighting vocabulary. Build a new camera composition from that same physical paper diorama, not a new character or location.
Hero: same young adult man, clean youthful face, small plain black paper eye, short dark layered paper hair, ochre brown paper hooded jacket over dark shirt. Preserve actual facial proportions and hair silhouette of image1. He faces screen-right. His body has not moved during the freeze; his right open palm remains raised near shoulder/face and other arm down, only crop hides it where necessary.
Medium: richly tactile handmade cut and folded paper/card miniature, visible fibres, layered torn cut edges, dimensional paper face/hair/clothing, physically grounded shadows and shallow miniature depth. Same navy blue and warm amber vocabulary as reference, cooler dim external explanatory lighting during stopped time. Viewer sees the external paper model; this is not the man's literal vision.
No text, letters, numbers, subtitles, logos, watermark, border, collage, split panel, transparent bands. No smooth CGI, real person photography, flat vector drawing. Do not add phones, watches, glasses, jewellery, extra people, light rays or magic symbols. Leave calm upper area for later separate editorial accent.
Scene S03: very close side profile of the same eye and nose, face looking RIGHT. Place the open eye/profile in the lower two-thirds, the dimensional dark layered paper hair attached above/behind it. Eye is a simple dark matte paper shape with NO street reflection or light reflection, not a realistic wet eyeball. The space directly before the face toward screen-right is deep black/navy matte fibrous paper, a readable void. Gentle soft external rim only makes the paper edges readable for the viewer. His face is still intact and attached, not a detached eye. The meaning is that no outside light can reach his eyes. Do not show lamps illuminating his retina, visible photons, lasers or a literal black-screen POV. Frame tightly enough to privilege eye/profile, calm top black area, still a full complete crafted scene.
```

## S04 prompt

```text
Use case: illustration-story.
Asset type: one finished static portrait 9:16 full-bleed opaque PNG for Paper Detour 033.
Input image 1 is the USER-ACCEPTED reference for exact hero identity, handmade paper material, rainy street geography, and lighting vocabulary. Build a new camera composition from that same physical paper diorama, not a new character or location.
Hero: same young adult man, clean youthful face, small plain black paper eye, short dark layered paper hair, ochre brown paper hooded jacket over dark shirt. Preserve actual facial proportions and hair silhouette of image1. He faces screen-right. His body has not moved during the freeze; his right open palm remains raised near shoulder/face and other arm down, only crop hides it where necessary.
Medium: richly tactile handmade cut and folded paper/card miniature, visible fibres, layered torn cut edges, dimensional paper face/hair/clothing, physically grounded shadows and shallow miniature depth. Same navy blue and warm amber vocabulary as reference, cooler dim external explanatory lighting during stopped time. Viewer sees the external paper model; this is not the man's literal vision.
No text, letters, numbers, subtitles, logos, watermark, border, collage, split panel, transparent bands. No smooth CGI, real person photography, flat vector drawing. Do not add phones, watches, glasses, jewellery, extra people, light rays or magic symbols. Leave calm upper area for later separate editorial accent.
Scene S04: close side profile of the SAME man's ear, rear part of head, neck and ochre hooded shoulder, all attached anatomically to the figure. The head still faces RIGHT; ear and the layered dark paper hair are the visual focus in the lower-middle foreground, with enough nose/profile at screen-right to establish orientation. The frozen rainy street remains in shallow depth behind, navy paper buildings, dim amber windows. In the LEFT background the SAME blue-grey helmeted cyclist with dark backpack and dark bicycle remains behind him, heading RIGHT; show a small recognisable bicycle bell physically attached to that bicycle's handlebar. Keep it naturally small and in depth, not a giant floating bell or an inserted illustration. Only the original man and original cyclist, no additional figures, no detached ear. Retain the same street axis and right-side brick facade vocabulary, cooler outside explanatory light. The image means no sound from the outside world, not total physiological deafness; no waves, no symbols, no cross-out signs.
```

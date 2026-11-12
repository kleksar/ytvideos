# ImageGen — набор промптов и референсов

Встроенный imagegen, 31 октября 2026. Файлы проекта — `Source/Images/paper_v1/` и `Source/Graphics/`. Значения в фигурных скобках подставлялись по таблице.

## Персонажи

Референс 1 — фотография конкретного человека из `channels/paper_detour/legacy/025_iq_gallery/Source/Images/`; референс 2 — утверждённый `channels/paper_detour/brand/paper_world_reference/paper_diorama_approved.png`. Запрос прозрачного фона.

> Use case: stylized-concept. Produce one separate, transparent-background paper-cutout character for a Paper Detour vertical short. Image 1 is the facial identity and pose reference: portray {person} recognizably as a real person, inspired by the identity in Image 1. Image 2 is the art-direction reference, not a character to copy: closely match its handcrafted dimensional cut paper, hand-cut layered matte paper and cardboard face, sculptural silhouette, visible paper edges, tactile textured fibres, appealing simplified face, detailed hair, warm amber light, contact shadows, subtle blue shadows, photographic physical miniature. Three-quarter body, full intact head and hands, standing upright on a tiny paper plinth, {prop} in foreground as an integral part of the paper puppet. The whole figure must fit fully inside image, with transparent empty margins on all sides. No background, no environment, no image frame, no text, no letters, no numbers, no watermark. All surfaces are layered cut paper, never a flat photographic collage or flat vector.

| Файл | Person | Prop |
|---|---|---|
| haha.png | Haha, South Korean TV host and performer | a handheld microphone |
| kasparov.png | Garry Kasparov, chess grandmaster | a black chess rook |
| feynman.png | Richard Feynman, physicist | a chalkboard and chalk |
| logan_paul.png | Logan Paul, video creator and wrestler | a vintage movie camera |
| nolan_gould.png | Nolan Gould, actor known for Modern Family | a film clapper |
| kate_beckinsale.png | Kate Beckinsale, British actress | a small film reel |
| tarantino.png | Quentin Tarantino, film director | a vintage movie camera |

`haha_clean.png`: нейросетевая правка созданного Haha: «Replace ONLY the large white sports numerals on his shirt with plain dark navy paper fabric, keeping the two white shoulder stripes. Remove all letters and numbers from clothing. Preserve the exact person, face, sunglasses, hair, pose, microphone, hands, lighting, paper texture, pedestal, positioning, alpha transparency, and every other element. Do not add any text or new objects.»

`marilyn_photo_ref.png`: референс 1 — опубликованный фотопортрет, источник указан в README; референс 2 — стиль канала. Запрос: «Create one separate transparent-background paper cutout character representing Marilyn vos Savant, the American writer and puzzle columnist. Image 1 is a real published photograph of her: preserve her recognisable facial structure, hairline, long swept-back dark hair, warm smile, fair skin, round white earrings and pale grey blazer; no glasses or bangs. Image 2 is the style reference: create a dimensional handmade paper-and-card puppet with paper-cut layered face, sculptural silhouette, tactile fibres, warm amber light and subtle cool shadows; keep her identity recognisable. Show her three-quarter body with a small stack of paper books, standing on a tiny paper plinth. Whole character fully visible with transparent margins. No background, typography, logo, numbers or watermark.» Более ранняя стилизация по неподтверждённой иллюстрации в монтаже не использована.

## Фон и передний план

Референс — утверждённый бумажный мир.

Фон: «Create a vertical 9:16 clean BACKGROUND PLATE for an editorial paper diorama inspired by reference image. An empty handmade miniature theatre gallery: deep layered midnight-blue paper walls, ochre folded-paper side curtains, shelves and a warm wood-and-cardboard stage deck near the lower edge, small paper cut-out spotlights casting warm amber pools, intimate tactile scene, cinematic depth, realistic miniature macro photography. No people, no figures, no signs, no letters, no numerals, no picture frames. Leave a wide clear dark central area for a character to be composited. Strong multi-plane depth and consistent lighting from upper left. Crop with generous side margins.»

Передний план: «Create ONE separate transparent-background foreground layer for a paper diorama animation. A low horizontal vintage theatre stage ledge, crafted of red-brown matte cut paper and layered cardboard with warm amber rim lighting and crisp fibers, spanning the entire width, viewed straight on, small curved upper edge. Fill only the bottom third with the ledge, leave the upper two thirds completely transparent; no people, letters, numbers, signs, logo, no text, no vignette, no backdrop. Match the handmade dimensional paper world of the reference image.»

## Цифры и имена

Для цифр 2, 3, 5, 6, 7, 9 и + референс — `accent_typography_v2/0.png`; 0 и 1 скопированы из исходных PNG канала. Запрос: «Create exactly one large isolated paper-cut glyph {symbol} on transparent background. Match Image 1's lettering with exceptionally close visual fidelity: thick rounded off-white matte fibrous paper face, red-orange thick paper backing, slightly irregular handcrafted edges, warm soft light and dimensional edge, no additional symbols or text. Whole glyph centered with transparent margins. Front view. No border or watermark.»

Для каждого имени отдельно референс — `accent_typography_v2/A_MESSAGE.png`: «Produce a single horizontal cut-paper title that reads exactly {name} in large uppercase letters, spelled precisely, with the words separated by a small gap; one single line. Match the reference's lettering as closely as possible: thick rounded off-white lightly fibrous paper cutouts mounted individually on red-orange paper backing, tactile depth and shadows, no surrounding objects. Transparent background with ample margin, word entirely visible and no clipping. No other text, symbols, lines or watermark.» Имена: HAHA, GARRY KASPAROV, RICHARD FEYNMAN, LOGAN PAUL, NOLAN GOULD, KATE BECKINSALE, QUENTIN TARANTINO, MARILYN VOS SAVANT.

Таблички с текстами `ILLUSTRATION / HISTORICAL CHILDHOOD SCORE` и `REPORTED IQ SCORES` созданы по эталону бумажного мира на прозрачном фоне с заданием напечатать точный текст на рваном кремовом бумажном ярлыке; фактическое написание проверено визуально.

## Минутное расширение, 31 октября 2026

Встроенным imagegen созданы семь дополнительных прозрачных фигур по тому же промпту и стилю, что выше, с референсами из `Research/` и `paper_diorama_approved.png`. Персонажи и предметы: Filip Pavlović — микрофон; Kim Hee-sun — кинохлопушка; Cathy Kelley — микрофон; RM (Kim Nam-joon) — микрофон; Frank Lampard — футбольный мяч; Sharon Stone — киноплёнка; Park Kyung — микрофон. Тот же промпт создания имени и эталон A_MESSAGE использованы для буквальных надписей FILIP PAVLOVIC, KIM HEE-SUN, CATHY KELLEY, RM, FRANK LAMPARD, SHARON STONE, PARK KYUNG. Файлы — соответственно `Source/Images/paper_v1/` и `Source/Graphics/names/`.

Глифы 4 и 8: тот же промпт цифры и образец `accent_typography_v2/0.png`, `Source/Graphics/digit_4_generated.png`, `digit_8_generated.png`. Отдельная надпись IQ создана по образцу `A_MESSAGE.png`: «Create exactly the two uppercase letters 'IQ' together as a single isolated transparent cutout for a paper-diorama video. Image 1 is the style reference: match its chunky rounded cream paper letters, rust red-orange thick paper backing, tactile handmade cut edges, lighting and proportions. Exact text: 'IQ'. No other text, digits, border, icons, or shadow beyond the letters. Tight but legible spacing between the two letters, both on one horizontal baseline, entire asset within transparent margins». Результат: `Source/Graphics/iq_letters_generated.png`.

## Замена на более известных персонажей

Встроенный image_gen, референсы из `Research/new_reference_credits.json`, `paper_diorama_approved.png` и `A_MESSAGE.png`. По тому же промпту прозрачной бумажной фигуры, что в разделах выше, сгенерированы Kanye West (микрофон), Lee Byung-hun (кинохлопушка), John F. Kennedy (микрофон на столе), Sunny Deol (кинохлопушка). Использован тот же промпт бумажных имён с точными строками KANYE WEST, LEE BYUNG-HUN, JOHN F KENNEDY, SUNNY DEOL. Прозрачные исходники фигур — `Source/Images/paper_v1/`, имён — `Source/Graphics/names/`. Права на фотоснимки-референсы — в каталоге исследования; фотографии не вставляются в ролик.

Имя `JOHN F KENNEDY` перегенерировано отдельной версией `Source/Graphics/names/john_f_kennedy_v2.png` по тому же образцу A_MESSAGE с требованием отдельных букв без полосы, тумана или свечения между ними; первая версия сохранена. Визуальная проверка второй версии выполняется независимо.

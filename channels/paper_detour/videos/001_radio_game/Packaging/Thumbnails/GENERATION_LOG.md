# Обложки Rarovista 001 — протокол генерации

30 октября 2026. Статус: **draft**, на YouTube не загружены и A/B-тест не запущен. Это три концепции для одного видео, а не изолированный тест эмоции. Инструмент: встроенный image_gen; точный ID модели интерфейс не сообщил. Все изображения — художественные реконструкции.

## Референсы

- `../../../../brand/2026-10-30-channel-research/radio-character-reference-portrait.png` — присланный пользователем ориентир внешности персонажа.
- `../../../../brand/2026-10-30-channel-research/radio-character-reference-scene.png` — присланный пользователем ориентир внешности и стиля сцены.
- Общие действующие правила: `../../../../RAROVISTA_PRODUCTION_GUIDE.md`. Конкретную сцену не следует превращать в образ обязательного маскота канала.

## Варианты

| ID | Исходник | Подготовленный JPEG | Вопрос для сравнения | Статус |
|---|---|---|---|---|
| A | `Concepts/radio-code-on-radio-v01.png` | `Upload/radio-code-on-radio-v01.jpg` | Достаточно ли неожиданной связи радио и кода? | draft |
| B | `Concepts/radio-press-record-v01.png` | `Upload/radio-press-record-v01.jpg` | Помогает ли действие и реакция героя? | draft; пользовательскую оценку сходства ещё не получали |
| C | `Concepts/radio-software-on-air-v01.png` | `Upload/radio-software-on-air-v01.jpg` | Понятен ли механизм радио → звук → компьютер? | draft |

JPEG — технические производные PNG через macOS `sips`, 1280×720, JPEG quality 90; PNG остаются нетронутыми. Это кандидаты к загрузке, а не подтверждение доступности функций или запущенного теста. Проверить выбранные варианты на телефоне, нижний правый значок длительности и соответствие окончательному монтажу. Образы кассеты и компьютера — иллюстрация; подтверждённого запуска игры не показывают. Герой B показан в радиостудии и нажимает запись; надпись без заголовка сама по себе не объясняет передачу программ.

## Промпты, отправленные в image_gen

### A

```text
Use case: ads-marketing. Make ONE finished cinematic YouTube thumbnail, wide horizontal 16:9, for a true story about a 1980s Brazilian radio show transmitting computer software as sounds that people can record. References: input image 2 is the definitive cinematic layered cut-paper look, warm amber lighting and deep navy; do not copy its scene. Composition: dramatically large recognizable retro FM radio receiver, a single visibly readable audio cassette next to it; a single beautiful ribbon of sound in amber light emerges from the radio and resolves into a few simple data blocks near the cassette, suggesting the unexpected connection. A rich handmade layered-paper diorama with smooth paper edges, real depth, expressive shadows; no exposed corrugated cardboard or cardboard holes. Strong silhouette and clear focal hierarchy, visually striking even on a phone. Integrate exactly the large short English headline 'CODE ON RADIO?' in bold legible cream uppercase, high contrast and generous clear margin. Preserve title legibility, no additional words, logos, UI, gibberish or watermark. Do not depict a working computer game or imply a proven game launch. No person in this version. Leave lower-right corner uncomplicated for YouTube duration.
```

### B

```text
Use case: ads-marketing. Create ONE finished widescreen 16:9 YouTube thumbnail for a true story of 1980s radio broadcasting computer software as sound. Input image 1 is the exact CHARACTER IDENTITY reference and input image 2 is the exact CHARACTER AND WORLD STYLE reference. Reproduce the same young male character with the same facial proportions, natural warm complexion, thick distinct dark brown curls, brows and brown eyes, blue hoodie, white T-shirt with yellow, red and blue horizontal stripes; keep his identity recognizably faithful, no redesign, no different haircut or outfit. In a dynamic medium close-up he is actually pressing RECORD on a vintage cassette radio, gazing at it with a natural subtle engaged smile, and an amber wave of signal travels toward the cassette. Radio and cassette and the pressing hand must be clear and plausible, no extra fingers. Cinematic handmade layered cut-paper world like reference, rich depth and smooth edges with no exposed corrugated cardboard holes, deep navy and warm amber, strong visual hierarchy on mobile. Add only the exact huge, legible cream headline 'PRESS RECORD' in a clear open area, with generous margin. No other text, logo, or watermark. No screen showing an allegedly running game, no exaggerated shocked mouth, no replacement of hero by another person. Leave bottom right clean for YouTube duration.
```

### C

```text
Use case: ads-marketing. Generate ONE finished 16:9 widescreen YouTube thumbnail, an intriguing single scene for an educational story about computer software being broadcast as sound on Brazilian radio in the 1980s. Reference image 2 ONLY for the cinematic smooth layered-paper diorama style, rich depth, amber light and deep navy, no exposed corrugated cardboard. An oversized unmistakable vintage FM radio on the left emits one flowing sound-wave ribbon that gradually resolves into simple luminous ordered data blocks leading to a vintage home computer on the right; a recognizable compact cassette can be secondary but must not clutter. Three large readable forms with separation, strong cinematic perspective, coherent spatial depth and crisp silhouette. Across the upper clear space place exact text 'SOFTWARE ON AIR?' in very large bold cream uppercase, spelled precisely, high contrast; no other words, logos, watermark, tiny diagram labels or extraneous code. No face in this version. Do not show a computer game being played or suggest proven successful game launch. Reserve lower right free for duration overlay.
```

Все три генерации технически получили оба референса; промпт уточняет, какой именно использовать в каждом варианте. Промпт — запрос, а не гарантия точного совпадения.

## SHA-256 файлов

```text
f7afd4e72bdd2755a241dc55b0a104e9d84890b87013f68baa35274fd3c89a3e  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Concepts/radio-code-on-radio-v01.png
8aaf32cb17f815e2392dc63397e441e27c34f1e96a4b35e3e982ff016f1acd1a  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Concepts/radio-press-record-v01.png
6a14a5d52c7cd3b72ac76f5fe143d2736d468d3593079cef7595f48cafa1976d  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Concepts/radio-software-on-air-v01.png
dce3bb02064a4589ca70de05a2d18034be8b63e20cdb1252857cb4ac1d37146e  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Upload/radio-code-on-radio-v01.jpg
eafc0144cf8b0d316a521f8b853ef0fec76f5ca43702027c689f6a7f2c53d03d  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Upload/radio-press-record-v01.jpg
fa1adf9cbb9dba0b9abcde607055ad5e4830ce47938f2d0af4dcb911a39ccfaa  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Upload/radio-software-on-air-v01.jpg
7b5e8c1e1110b77d5e6e92d064d2664cadba5daf9dcd3bf832d1f3ab8dcfc2ab  channels/paper_detour/brand/2026-10-30-channel-research/radio-character-reference-portrait.png
e31d485c94b680dbb6e82d65368212546da236f7adafc7f78e0169a99625dddc  channels/paper_detour/brand/2026-10-30-channel-research/radio-character-reference-scene.png

```

## Второй проход — более сильная интрига

30 октября 2026. Пользователь отметил, что первые варианты недостаточно интригуют, особенно `PRESS RECORD`. Новые варианты — **draft**, не тестировались и не загружались. Модель встроенного image_gen интерфейс не сообщил. Исследование и идеи с [ChatGPT Pro](https://chatgpt.com/c/6ae4c568-2834-83eb-8cb8-b4778b787c87); фактические ограничения — в `Research/FACT_CHECK.md`. JPEG — производные через `sips`, 1280×720, quality 90.

| Концепция | Исходник | JPEG | Гипотеза |
|---|---|---|---|
| NOT MUSIC | `Concepts/radio-not-music-v02.png` | `Upload/radio-not-music-v02.jpg` | Странный звук из радио — что это, если не музыка? |
| THAT’S CODE? | `Concepts/radio-thats-code-v02.png` | `Upload/radio-thats-code-v02.jpg` | Герой слышит шум и реагирует на неожиданное назначение; сходство с референсом пользователь ещё не оценил |
| DOWNLOADED? | `Concepts/radio-downloaded-v02.png` | `Upload/radio-downloaded-v02.jpg` | Противоречие: загрузка данных и магнитофон 1980-х |

Все идеи — гипотезы для сравнения. На первой обложке «NOT MUSIC» относится к конкретному программному звуку, а не ко всей радиопередаче. Третий образ представляет запись радиозвука на кассету, а не современную беспроводную передачу файлов. Сверить финальный смысл с готовым монтажом и выбрать подходящий title/thumbnail комплект.

### Prompt — NOT MUSIC

```text
Use case ads-marketing. Create ONE outstanding 16:9 widescreen YouTube thumbnail for a surprising true-story science documentary, not a textbook diagram. The visual twist: what comes out of a vintage radio sounds like an ordinary noise, but is actually a computer program. Close cinematic macro view: large tactile 1980s FM radio, one giant unmistakable round speaker and glowing tuner; immediately next to the speaker a cassette recorder with one clearly visible tape, both large and recognizable; a vivid waveform made of three or four coarse paper layers comes out of the speaker, one short portion subtly changes from jagged sound wave to blocky program data. Make the audience ask 'If it wasn't music, what was that sound?' Very clear at small mobile thumbnail scale, tightly cropped, one dramatic focal moment; scene is a warm retro Brazilian night studio suggested subtly in defocused background. No diagram arrows or floating complex numbers, no person. Use the provided scene solely as the exact style reference: elegant, mature, cinematic layered smooth cut-paper world, sculpted paper, deep shadows, restrained orange light against deep navy, no corrugated cardboard holes. Place a large bold premium hand-set style uppercase headline, EXACTLY 'NOT MUSIC' in white/cream high contrast, with ample margins, correct spelling. No other text, logos, watermarks, buttons, English gibberish, misinformation, game screen, or modern internet imagery. Keep lower right area unobstructed for YouTube duration. Treat sound graphics as metaphor, no assertion an actual computer directly receives digital files wirelessly.
```

Вход: `brand/2026-10-30-channel-research/radio-character-reference-scene.png` как ориентир стиля.

### Prompt — THAT’S CODE?

```text
Use case ads-marketing. ONE finished landscape 16:9 YouTube thumbnail for a true surprising story of a 1980s Brazilian radio broadcast containing computer programs as sound. Deliver a brilliant visual hook, not a descriptive infographic. The subject is the exact young paper-diorama character from BOTH reference images, with faithfully matching face and dark brown curly layered-paper hair, dark-blue hoodie, and white shirt with horizontal yellow, red and blue stripes; do not redesign him. Tight close crop: he leans his ear toward a big recognizable retro tabletop FM radio, eyebrows slightly raised in real puzzlement, one hand lightly cups ear, intent on a loud strange audio signal; his face occupies one third of frame and radio speaker nearly another third, readable on a phone. A visually striking paper speech bubble emerging FROM RADIO contains only chunky jagged sound squiggles; beneath/next to it, a physical cassette with unlabelled black and gold reels offers a hint. Text integrated clearly in a separate bold white area: exact words 'THAT’S CODE?' (curly apostrophe or straight acceptable), huge cream uppercase, no other lettering. Cinematic layered smooth cut paper style of image 2, warm amber vs navy, minimal clutter, mature clever tone. No extra people, no cartoon comics style, no exposed corrugated holes, no fabricated logos, no game or running software, no modern devices. Leave bottom right unobstructed for the duration.
```

Входы: `brand/2026-10-30-channel-research/radio-character-reference-portrait.png` и `radio-character-reference-scene.png` — внешность и стиль.

### Prompt — DOWNLOADED?

```text
Use case ads-marketing. ONE premium 16:9 widescreen YouTube thumbnail with an immediately obvious, unexpected 1980s DOWNLOAD paradox for a true story: computer software could be transmitted as sound via a radio show and recorded to cassette. Construct a cinematic tactile paper miniature: a vintage radio and a transparent audio cassette exceptionally large in the foreground, with a hand pushing an old cassette into a retro recorder; above the cassette an unmistakable DOWNWARD ARROW symbol and '1980s' as a single visually readable chunky cut-paper icon, not a flowchart. The radio emits an intriguing jagged audio signal towards cassette, suggest radio sound being recorded; no computer directly receiving wireless files, no download interfaces, no modern phones, no gameplay. Exact primary headline 'DOWNLOADED?' in very large bold cream capital letters, include a separate small but readable '1980s' element, no other text. Deep navy darkness with vivid amber and a touch of warm red, strongly lit physical layered paper with depth as in the second supplied image; no visible cardboard corrugation. Close dramatic perspective and bold negative space, visually intelligible at 320 pixels; leave lower right corner clear of text for timestamp. No people faces, no brand names or watermark.
```

Входы: тот же портрет и сцена (стиль по сцене); промпт — запрос, а не свидетельство точного воспроизведения всех требований.

Проверка: просмотрены уменьшенные копии 320×180, три английские надписи читаются; просмотр в YouTube Studio и тест на реальных зрителях не выполнялись.

### SHA-256 файлов второго прохода

```text
9344aa0e45c71567287812fd5b8d70b046025912667e9288ab168fcd5e328237  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Concepts/radio-downloaded-v02.png
ef148d0e7fd701dfc04bec2b24ed9745dda846c715528a8955a8341919c814e7  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Concepts/radio-not-music-v02.png
fc4b24175711e394fa805421fc71f3eef4ad98c7b4035a0c2ffe9e730cb792cb  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Concepts/radio-thats-code-v02.png
5aa8f2d153da936584b22d8e7af85bc4be394c5d536cbb33e76c6328f1f954ed  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Upload/radio-downloaded-v02.jpg
a397c59570d8f5d4688f9c0068a5201ba4fcdf493e6204c4e8d9be38d6e79721  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Upload/radio-not-music-v02.jpg
b0b77c9245d72e78643ea6cf246f0a80b329574e2d5365fab04d0b4e79706aca  channels/paper_detour/videos/001_radio_game/Packaging/Thumbnails/Upload/radio-thats-code-v02.jpg

```

### Дополнительная проба — NOT FOR YOU

`Concepts/radio-not-for-you-experiment-v02.png`, статус **не выбран**: перечёркнутое ухо может восприниматься как запрет/тема потери слуха, вместо неожиданного получателя радиосигнала. Исходник оставлен как история эксперимента, не подготовлен к загрузке. Использован built-in image_gen и тот же референс сцены.

```text
Use case ads-marketing. Create ONE cinematic horizontal 16:9 YouTube thumbnail as a clever visual puzzle for a true story about a radio program that deliberately broadcast computer software as audio in the 1980s. A large expressive anthropomorphic visual contrast without anthropomorphizing the machine: left side, a large 1980s vintage radio with its glowing dial and speaker; right side, a large recognizable period-appropriate cassette and home computer, both as tactile paper miniatures. The radio emits a bold hand-cut, jagged sound waveform towards the recorder, suggesting a sound a computer could later decode via cassette, NOT direct wireless transfer. Create immediate intrigue that the eerie sound is not intended as music for people. Graphic treatment features a giant simple cut-paper ear symbol and a clear red slash through that ear symbol next to the sound, making 'not for human ears' instantly visible. Short monumental bold cream title lettering, spell exactly 'NOT FOR YOU' in 3 words, high contrast, spacious margins, no other lettering or logos; placement away from bottom right YouTube duration. Strong story-focused visual hierarchy, close-up rather than busy educational diagram. Use supplied scene as style reference only: cinematic mature layered smooth paper-diorama with subtle geometric paper texture, amber practical lighting against deep navy, dimensional depth and rich contrast, no corrugated holes. No character faces, no alien, no hazard sign, no faked conspiracy, no glowing game screenshot, no watermark. The slash is only a graphic creative metaphor, not an explicit prohibition.
```

## Третий проход — неожиданный слушатель и запись сигнала (30 октября 2026)

Созданы встроенным image_gen по двум референсам: `brand/2026-10-30-channel-research/radio-character-reference-portrait.png` и `radio-character-reference-scene.png`. Точная модель не сообщена инструментом. PNG в `Concepts/`, JPEG 1280×720 в `Upload/`. Кандидаты, а не результаты теста. Уменьшенные копии 320×180 просмотрены: основные объекты и надписи читаются; с реальными зрителями и в Studio не проверялись. Компьютер в наушниках — визуальная метафора, не реконструкция приёма радио. На версии с героем намерение нажать красную кнопку видно, портрет похож на референс, но сходство пользователь ещё не оценил.

### FOR MACHINES — фактический запрос

```text
Use case: ads-marketing. Make ONE polished 16:9 YouTube thumbnail for a surprising factual history documentary. Core visual gag: in the 1980s this radio signal was not just for people to listen to, it carried computer programs in sound. Create a cinematic paper diorama featuring a giant classic 1980s beige home computer wearing comically oversized realistic-looking vintage headphones, with the headphones clearly over the top corners of its monitor; monitor dark without face, no eyes and no game. Beside it a much smaller but recognizable vintage FM radio with illuminated tuning dial and antenna and a compact cassette recorder with visible tape; these give radio context and reveal an old-fashioned recording step. A single short stylized jagged sound squiggle beside the radio suggests strange sound, NOT wirelessly connecting radio to computer. This is a deliberately obvious and playful visual metaphor; no imaginary person, no logos, no actual audio cable implied. Huge strong cream headline 'FOR MACHINES' in two words, exact spelling, highly legible at phone size, clear of timestamp area. Use supplied second image as style reference ONLY: mature, richly layered smooth cut-paper miniature, saturated warm amber light against deep midnight blue, dramatic yet realistic paper shadows; bold close composition, uncluttered scene, no corrugated holes. No additional text, no watermark, no game screen, no computer success indicator, no robots/AI. No unnecessary arrows or diagram.
```

### NOT STATIC — фактический запрос

```text
Use case: ads-marketing. Generate ONE strong 16:9 YouTube thumbnail for a true story: an unusual radio signal that sounds like static was intentionally transmitted as computer software, which listeners could record onto cassette. Image: exactly the same character as both supplied references: same face, dark wavy curls, expressive brown eyes, blue hoodie, white shirt with narrow yellow red navy stripes. A tight cinematic medium close-up of him reacting with curious disbelief to a large recognizably 1980s radio cassette deck; his right index finger is clearly poised just over the prominent red RECORD button, a transparent cassette clearly visible in its deck. Show a short sharp jagged sound burst as a cut-paper shape in front of the radio speaker, making it clear what he hears. Strong emotional curiosity rather than fear, no huge gaping mouth, no misdrawn hands. Add exactly 'NOT STATIC' in very large cream uppercase, in a clean area at upper right, high contrast; no other words or logos. The contradiction is 'why record something that sounds like interference?' Use the exact tactile layered smooth-paper diorama material, warm amber highlights and deep blue shadow, cinematography of provided second reference, preserving mature charm and the distinct character. Only one person, no game screen, no fantasy sparks or danger, no cardboard corrugation, no watermark, lower-right free for duration.
```

### SHA-256

```text
5e2043c5c3a53372a68a41ef87cd552313b7854b454b3dc93af347b522ea5163  Concepts/radio-for-machines-v03.png
e0da771290433e8f1306ba9c6a71952369fe9330fbfaedfd78db26badde8f3e9  Concepts/radio-not-static-v03.png
f2f09d6a75e5d10b2d69e883c475a0e57827f419287bee840179cd772b2ea49a  Upload/radio-for-machines-v03.jpg
a24110d00e329541f868204df60eba170baacf31f3343c5955517810a8ceb100  Upload/radio-not-static-v03.jpg
```

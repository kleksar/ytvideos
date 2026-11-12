# 008 — журнал генерации обложек

## 1 November 2026 — option 1, draft candidate v01

- **User selection:** “My Boyfriend Brought Matt to Every Date”; cover wording “EVERY DATE?”.
- **Destination:** [`Concepts/short008_every_date_v01_20261101.png`](Concepts/short008_every_date_v01_20261101.png).
- **Tool:** `image_gen.imagegen`; model/version was not exposed by the tool.
- **Canvas:** 941 × 1672 px (portrait 9:16).
- **Input reference for edit:** first generated draft at `/Users/diplomat/.codex/generated_images/01a19467-e9f7-78f0-9aed-5afbd2ac3994/exec-9ac0b241-ebb2-4ef0-931c-af3a58dd4ddb.png` (SHA-256 `42678646a4a513e76f68f4dd51022b17e7f66aff66ed1aa5a37818825eaa34c8`). The first pass had the right composition and wording but looked too much like a smooth 3D cartoon, so it was used only as an edit reference.
- **Status:** superseded after user feedback that the characters differed from the finished video. Retained for provenance; not uploaded or published.

### Exact generation prompt

> Create one finished YouTube Shorts thumbnail for Paper Detour, portrait 9:16. Composition: a handmade paper-and-card diorama showing a young woman on the left and her boyfriend on the right seated at a small date table, both turned toward each other; an unexpected male friend, Matt, sits prominently in the exact middle between them. Tight medium shot, large expressive paper-cut faces and upper bodies, clear silhouette and readable relationship even at phone size. The woman has a mildly confused, questioning expression; boyfriend is casually unaware; Matt is friendly and non-threatening. Simple restrained date setting, no distracting props. Handmade cut-paper/card construction must be unmistakable: tactile fibrous paper grain, clean but visible cut edges, layered card thickness, subtle dimensional paper shadows, warm studio light, crafted miniature diorama, visually coherent and elegant. Not photorealistic, no ordinary digital 3D render, no anime. Use muted cream, warm red, dusty blue and charcoal, high contrast focal faces. Add only the exact words “EVERY DATE?” in large, bold, simple cut-paper letters, integrated in clear negative space near the top, fully legible and spelled exactly, no other text or lettering. Keep all essential faces and the entire phrase inside the central 2:3 safe crop of the 9:16 canvas. Full-frame composition, no borders, no watermark, no logos. Preserve the story mystery: do not show a fiancée, family, reveal, wedding, or villainous framing.

### Exact edit prompt

> Revise this exact Paper Detour thumbnail composition while keeping the same three-person date setup and story meaning. Convert the visual style from sculpted 3D characters into a clearly handmade paper-cut diorama: figures built from flat, layered cut-paper shapes, visible crisp cut edges and card thickness, tactile fibrous paper surfaces, simple graphic facial features cut from paper, shallow real-paper shadows. Avoid rounded clay sculpture, plush forms, smooth CGI, or photorealism. Keep the woman on the left mildly confused, Matt seated in the middle and friendly, boyfriend on the right. Retain the simple table and restrained background. Preserve only the exact lettering “EVERY DATE?” in cut paper, but reduce it slightly and move it down so the top of every letter lies at least 9% below the canvas top; keep all letters fully legible, with comfortable spacing from the figures. Maintain generous negative space. Keep every face and all of the phrase inside the central 2:3 crop. Portrait 9:16 full frame, no borders, no watermark, no extra text. Keep the warm cream, red, dusty blue and charcoal palette, but make the construction unmistakably flat layered paper rather than a digital 3D render.

### Review and checks

- Compared the full image against the Paper Detour cover examples in Shorts 007 and 002. The final candidate has tactile paper grain, layered hair and clothing, visible paper edges, and soft miniature-scene shadows. The first pass was rejected as too smooth and sculptural.
- Inspected the full frame and a temporary central 2:3 crop (`941 × 1412`, crop origin `x=0, y=130`). “EVERY DATE?” and all three faces remain legible and inside the crop. The crop preview was only for review; the saved image is the uncropped full frame.
- Phone-size readability: the large two-line cover words and three distinct faces read clearly at the reviewed scale.
- No other text, logos, or unsupported story reveal is visible.
- No channel-card simulation or YouTube upload was performed. Keep title as a selected candidate until its real card display is reviewed.

### Output integrity

- Candidate SHA-256: `6fb9af31e5c1fc6454d0a0b589d20872bb1c1e4f0d55824889aa8c30134e67c6`.
- Source first-pass SHA-256: `42678646a4a513e76f68f4dd51022b17e7f66aff66ed1aa5a37818825eaa34c8`.
- Edited generation source: `/Users/diplomat/.codex/generated_images/01a19467-e9f7-78f0-9aed-5afbd2ac3994/exec-34112702-0827-417e-9d0b-6c8ea6ea1b2b.png`.

## 1 November 2026 — cast correction, draft candidate v02

- **User feedback:** “герои отличаются. в видео другие”.
- **Consultation:** Google Chrome, project `YT Видео`; visible mode **Extra High** immediately before the request. [Prompt for cover](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae79fa3-0f78-83eb-84c6-d6d28bffac81).
- **Exact consultation prompt:**

> Ты — консультант в уже открытом ChatGPT Extra High; обязательная проверка режима выполнена координатором непосредственно перед этим запросом. Ответь здесь, не открывай рекурсивно другой ChatGPT. Одна узкая задача: дай точные визуальные инструкции для исправления уже выбранной обложки Paper Detour Short 008 «My Boyfriend Brought Matt to Every Date», чтобы герои совпадали с готовым v06 видео. Композицию сохраняем: три крупных героя за столом свидания, рассказчица слева, Мэтт неожиданно в центре, парень справа, текст «EVERY DATE?»; раскрытие сюжета не добавлять. На текущей обложке внешность и одежда неверны. Канон, сверенный по кадрам готового v06 и материалам сцены: рассказчица N — женщина с коротким тёмным волнистым каре, ржаво-оранжевой рубашкой поверх кремовой футболки и тёмными брюками; парень B — мужчина с тёмными волнистыми волосами, тёмно-синей рубашкой поверх кремовой футболки и тёмными брюками; Matt — мужчина с взъерошенными медно-рыжими волосами, коралловой рубашкой поверх кремовой футболки и светлыми брюками. Сохрани узнаваемую фактуру handmade paper/card диорамы и безопасную центральную область 2:3. Верни один короткий английский image-edit prompt, который прямо фиксирует N/B/M и запрещает менять композицию, надпись и число людей. Не генерируй изображение и не добавляй новых деталей сюжета.

- **Exact Extra High response:**

> Edit the existing cover, correcting only the characters’ appearances to match the v06 video: N (left) — woman with a short dark wavy bob, rust-orange overshirt over a cream T-shirt, dark trousers. Matt (center) — man with tousled copper-red hair, coral shirt over a cream T-shirt, light trousers. B (right) — man with dark wavy hair, dark navy shirt over a cream T-shirt, dark trousers. Preserve the exact existing composition: three large characters seated at the date table, same positions, poses, proportions, framing and background. Keep the exact text “EVERY DATE?”, unchanged in wording, typography and placement. Do not add, remove, duplicate or replace any people. Do not introduce new story elements or plot reveals. Preserve the handmade paper/card diorama aesthetic, crisp cut-paper edges, layered depth, tactile paper texture and soft shadows. Keep all three characters and the text within the central 2:3 safe area of the 9:16 canvas. Change character identity and clothing only; do not redesign the cover.

- **ImageGen inputs:** v01 cover as composition/text source only; finished v06 frame [`export_f0225.png`](../../Edit/Palmier/VisualChecks/title_size_v06_20261101/export_f0225.png) as the actual-video identity check; `character_lineup_v01.png` as supporting clothing/identity reference (the lineup README marks it DRAFT). Both cast references were used only for appearance and outfit, not as composition or scene-background sources.
- **Tool:** `image_gen.imagegen`; model/version was not exposed. Source output: `/Users/diplomat/.codex/generated_images/01a19467-e9f7-78f0-9aed-5afbd2ac3994/exec-e7c70884-44d8-410d-b4ea-6615b2b1a8ea.png`.
- **Destination:** [`Concepts/short008_every_date_v02_20261101.png`](Concepts/short008_every_date_v02_20261101.png).
- **Canvas:** 941 × 1670 px, approximately portrait 9:16.
- **Exact image-edit prompt:**

> Edit the first image. It is the composition and lettering source only. Images 2 and 3 are the character identity references: image 2 is a real frame from the finished v06 video; image 3 is a character lineup. Use them only to match the three characters' faces, hair and clothing. Do not borrow image 2's park, background, poses or lettering; do not rearrange the first image.
>
> Correct only the three characters in the first cover so they match the video cast: N on the left is a woman with a short dark wavy bob, rust-orange overshirt over a cream T-shirt, dark trousers. Matt in the center is a man with tousled copper-red hair, coral overshirt over a cream T-shirt, light trousers. B, the boyfriend, is on the right, a man with dark wavy hair, dark navy overshirt over a cream T-shirt, dark trousers. Keep their positions, seated date-table poses, relative sizes, expressions, camera framing and background from image 1. Keep exactly these three people, with Matt visibly between the couple. Keep the exact words “EVERY DATE?” in the same lettering style and placement; do not change, add or remove text.
>
> Preserve the handmade Paper Detour paper/card diorama material: layered fibrous paper, visible cut edges, tactile surfaces, soft object shadows and warm miniature-set lighting. Keep all three faces and the complete phrase within the central 2:3 safe crop of the portrait 9:16 image. Change character identity and clothing only; no new story elements, no extra people, no logos, no watermark.

### Review and checks

- Compared v02 with the actual finished v06 frame and supporting lineup. N now has the short dark wavy bob and rust-orange overshirt; Matt has copper-red hair, coral overshirt and light trousers; B has dark wavy hair and navy overshirt. The selected left / center / right cover arrangement remains N / Matt / B.
- Inspected the whole image and the central 2:3 crop (`941 × 1412`, origin `x=0, y=129`). All three faces and the full phrase remain visible in the safe crop. A 160 × 240 px phone-size preview kept the wording and three-character conflict readable.
- Text remains exactly “EVERY DATE?”; no additional person or plot reveal appeared.
- Title’s actual channel-card preview remains unchecked. v02 is a draft candidate, not an uploaded or published asset. Visual review was performed by the coordinator; no independent review was requested or claimed.

### Output integrity

- v02 SHA-256: `86535c99dca2de442b9a8b9e0107c5ef50b5eb252e13f116aa3d4e84f2069a23`.
- v01 SHA-256 (superseded): `6fb9af31e5c1fc6454d0a0b589d20872bb1c1e4f0d55824889aa8c30134e67c6`.
- v06 frame reference SHA-256: `ba697b8d5850bd42c1bc548bcd9025a40022b28e896f4686185d415f328ee123`.
- Supporting lineup SHA-256: `e91bc54266f351a0f3246648db52bc0812d35f670c7dccc61c480741feddf3ec`.

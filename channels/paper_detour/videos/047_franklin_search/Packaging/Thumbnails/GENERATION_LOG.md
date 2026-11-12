# 047 — журнал генерации обложек

Каждая запись: дата, концепция, назначение, точный запрос, инструмент и модель
(если известна), входные референсы и их роль, исходник, производные файлы,
статус, проверки, ограничения и необходимые SHA-256. Фиксировать подтверждение
пользователя и результаты теста только после фактического получения.

## 2026-11-05 — Franklin long A/B/C

Built-in imagegen; model and native generation controls unknown. Requested 3840×2160 maximum quality, actual each selected master 1672×941 RGB. Style reference inspected/supplied: `channels/paper_detour/brand/References/bold_visual_hooks_20261105_v01/05.png` (paper depth, rounded headline, visual hierarchy); story reference inspected/supplied: `Source/Images/scene_006_v04.png` (Arctic episode environment). Three concepts and pre-generation distinction in `../Metadata/CONCEPTS_v01.md`.

- A master `A_master_v01.png`, SHA-256 `469e6a152e25bcf672191444d7678218576240c10f6307a0256543b27408c6c9`; exact words `BOTH FOUND`. Initial generation: two 1840s wooden ships under Arctic ice, one lit, one distant; paper headline, strong hierarchy; requested no fabricated disaster or outer frame. Edit target original generated A: separate ships into distinct paper windows to avoid implying one wreck site, preserve exact headline and no added words.
- B master `B_master_v01.png`, SHA-256 `3dda4daf6a1cb5439e472fc5e12b6b53c22973153d79e21e77b6d693b0f228ab`; exact words `SHIPWRECK CLUE`. Initial generation: glove finds rusty ship fitting on Arctic shore with distant modern sonar boat, large `ONE SMALL CLUE` lettering. First edit removed two period ships erroneously shown in the same era as modern boat. Second edit replaced headline with `SHIPWRECK CLUE` so image has independent context, preserving the scene.
- C master `C_master_v02.png`, SHA-256 `ec67a14844c8174d8c1b07f779c4483618555adecf5f32dc9369d2d5f0a2cf48`; exact words `THEY CHANGED COURSE`. Initial generation: overhead tactile Arctic map, modern vessel turning toward a piece of wood in sea ice, arrow as an editorial route. Edit corrected arrow to reach and point at object; no change of text or other content requested.

Each request required full-bleed 16:9 paper/card diorama with paper lettering embedded by imagegen, high contrast, meaningful visual hierarchy, no decorative outer border and no invented disaster. The exact edit requests are preserved in this conversation's imagegen calls. Selected masters were visually examined individually and reduced to `contact_320_v02.jpg` for self-review. JPEG conversions are upload copies, not newly generated artwork. Standalone interpretation, differences, limits and linked titles in `../Metadata/PACKAGE_REVIEW_v01.md`. No actual YouTube test or display verification. User acceptance of the video is not thumbnail selection.

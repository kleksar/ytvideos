# Jascon-4 — camera plan v13, Extra High consultation

- Date: 2026-11-02. Coordinator personally used Google Chrome; visible model label immediately before request: «Очень высокий».
- URL: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae7efbd-75a4-83ed-ae0c-d762127296eb
- Input: user requires camera animation AND depth parallax on every scene, all four modes, same visible horizontal direction. Baseline still timeline v11 `1BD3395C`, project `8BE390BC`, exact images from v12 source manifest.
- Narrow request: assign one of push-in, pull-out, pan-left, pan-right to each of S01–S16, with short purpose. Full scene list: diver in corridor; close hand contact; diver left/Okene right; sinking tug; inverted wreck/diver upper-left; diver entering hull; isolated Okene right; Okene left watching beam right; Okene right reaching left; close Okene looking upper-left; wide air pocket; rescue support; transit toward bell right; decompression chamber/technicians; face at chamber window; final surface/seabed section. Explained that pan names mean visible image travel, not physical camera direction; same-direction parallax; fixed timing, captions/audio. Standard camera center travel 4.5% and zoom 1.048↔1.093. Asked only for the 16-row map, no other parameters.
- Completed substantive response, read in full:

| Scene | Camera | Purpose |
|---|---|---|
| S01 | push-in | К источнику света в глубине коридора |
| S02 | push-in | Акцент на контакте рук |
| S03 | pan-left | Okene справа ближе к центру |
| S04 | push-in | Опасность накренившегося буксира |
| S05 | pan-right | Водолаз слева ближе к центру |
| S06 | pan-left | Вход в корпус справа ближе к центру |
| S07 | push-in | Изоляция Okene |
| S08 | pan-left | Луч справа ближе к центру |
| S09 | pan-right | Луч слева ближе к центру |
| S10 | pan-right | Лицо вправо, пространство по взгляду слева |
| S11 | push-in | К герою в глубине воздушного кармана |
| S12 | pull-out | Раскрыть поддержку водолаза и героя |
| S13 | pan-left | Колокол справа ближе к центру |
| S14 | pull-out | Камера и техническая команда |
| S15 | push-in | Лицо за иллюминатором |
| S16 | pull-out | Масштаб спасательной операции |

The consultant also stated: full-image depth map on all scenes; pan-left parallax travels left and pan-right travels right; no independent part animation. Its additional suggestion to tie zoom depth to scale is not adopted: the existing renderer uses its documented alternating lateral parallax for zoom scenes. The accepted map above uses all four modes, with 6 push-ins, 3 pull-outs, 4 left pans, 3 right pans. These are coordinator decisions following the explicit user instruction, not new user acceptance of a rendered result.

Sources/config: `Edit/ImageMotion/sources_v13.json`, `motion_v13.json`. Do not process the baked v12 videos again: render/apply from still baseline v11, reusing valid depth/video cache.

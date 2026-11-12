# 027 — журнал обложек Shorts

## 2026-11-01 — user-selected scene, text lowered to 2:3 safe area (v05)

- Назначение: финальная локальная версия выбранной пользователем обложки Minnie Freeman с полностью видимой надписью `FROM ONE BOY` в центральном crop.
- Статус: предшествующая попытка загрузить файл через Studio не изменила обложку. 1 ноября 2026 YouTube Data API установил этот v05 для Shorts `r71aCn4p88A`; API принял запись, `readback: matched`.
- Источник: [`shorts_9x16_v02_20261101/01_from_one_boy_v02.png`](shorts_9x16_v02_20261101/01_from_one_boy_v02.png), выбран пользователем; правка ограничена положением/размером существующего заголовка.
- Результат: [`minnie_freeman_thumbnail_v05_from_one_boy_safe_20261101.png`](minnie_freeman_thumbnail_v05_from_one_boy_safe_20261101.png), PNG, 941×1672, портрет 9:16.
- Проверка: полный кадр и центральный crop просмотрены; обе строки `FROM ONE BOY` целиком видимы в crop. Это локальная проверка макета, не проверка показа после загрузки.
- v05 заменяет v04 как текущую локальную версию для дальнейшей работы; более ранние варианты сохранены как provenance.

## 2026-11-01 — text-safe revision v03

- Назначение: новый локальный кандидат Minnie Freeman, чтобы надпись `TIED THROUGH / THE BLIZZARD` целиком помещалась в центральный 2:3 crop.
- Статус: кандидат показан пользователю; не загружался и не устанавливался в YouTube Studio. Существующая/загруженная обложка не менялась.
- Инструмент: встроенный `image_gen.imagegen`; модель не указана.
- Вход и роль: [`minnie_freeman_thumbnail_v01_20261101.png`](minnie_freeman_thumbnail_v01_20261101.png) — edit target. Сохранены бумажная сцена спасения, герои, группа, верёвка, ферма, свет и фактура.
- Результат: [`minnie_freeman_thumbnail_v03_safe_area_20261101.png`](minnie_freeman_thumbnail_v03_safe_area_20261101.png), PNG/RGB, 941×1672; SHA-256 `4d92e0f40f23da5933cfd7ff71cd97f3f7bd5a60fb259cc7bee75bbd818d620b`.
- Проверка: полный кадр и центральный crop 941×1412 с верхним смещением 130 px просмотрены; оба ряда headline целы и читаемы. Проверка относится к локальному crop, не подтверждает реальный показ в Studio.
- Prompt:

```text
Use case: text-localization / precise thumbnail edit
Asset type: Paper Detour Shorts cover, portrait 9:16
Input images: Image 1 is the exact edit target. Preserve its existing paper-diorama artwork.
Primary request: Change only the position and scale of the existing headline so it stays completely visible in the centered 2:3 crop of this 9:16 cover. Keep the same miniature rescue scene, exact characters, colors, lighting, twine and all other visual details.
Style/medium: preserve the existing tactile handmade paper/card diorama, cut-paper letter texture, fibers, edge shadows and miniature depth exactly.
Composition/framing: preserve the full portrait 9:16 master. Reflow the headline as two centered lines in the upper-middle of the 2:3 safe area, with generous left/right margins. Keep every letter at least a small visible margin inside the centered 2:3 crop; on a 1080×1920 canvas that crop excludes the top and bottom 150 px. Keep text clear of Minnie's face, the pupils, twine and farmhouse. Slightly reduce the headline only if needed to keep it fully visible at phone size.
Text (verbatim): line 1 “TIED THROUGH”; line 2 “THE BLIZZARD”. Spell every letter exactly; add no other lettering.
Constraints: edit only the existing headline placement/size. Preserve all artwork and story details. One complete full-bleed portrait image, no border, no UI, no watermark, no added objects, no new scene, no extra text.
```

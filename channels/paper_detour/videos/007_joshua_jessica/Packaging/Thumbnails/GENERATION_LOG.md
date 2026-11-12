# 007 — журнал генерации обложек

Каждая запись: дата, концепция, назначение, точный запрос, инструмент и модель
(если известна), входные референсы и их роль, исходник, производные файлы,
статус, проверки, ограничения и необходимые SHA-256. Фиксировать подтверждение
пользователя и результаты теста только после фактического получения.

## 2026-11-01 — text-safe revision v03

- Назначение: новый локальный кандидат, где `HE STILL CRIED` остаётся целиком видимым после центрального 2:3 crop.
- Статус: локальный v03 установлен 1 ноября 2026 через YouTube Data API для Shorts `WQw7ny9svrk`; API принял запись, `readback: matched`. Видеопубликация не менялась.
- Инструмент: встроенный `image_gen.imagegen`; модель не указана.
- Вход и роль: `Source/Images/YOUTUBE_THUMBNAIL_v01_20261101.png` — исходный edit target; сохранены выражение и поза Joshua, ноутбук с `55% REMAINING`, цвета и свет.
- Результат: [`joshua_chatbot_thumbnail_v03_safe_area_20261101.png`](joshua_chatbot_thumbnail_v03_safe_area_20261101.png), PNG/RGB, 941×1672; SHA-256 `c3d8d6f1203bf168b809a80682d1e9c625b648b5c66f123ff68f79ef14ed983f`.
- Проверка: полный кадр и центральный crop 941×1412 с верхним смещением 130 px просмотрены; кремовая плашка и вся строка находятся внутри crop, текст читаем, линия не перекрывает волосы. Промежуточная v02 после просмотра заменена v03.
- Первый prompt:

```text
Use case: text-localization / precise thumbnail edit
Asset type: Paper Detour Shorts cover, portrait 9:16
Input images: Image 1 is the exact edit target. Preserve its existing paper-diorama artwork.
Primary request: Move and slightly scale the existing cream headline banner so the words are completely visible after a centered 2:3 crop of the 9:16 image.
Style/medium: retain the existing tactile paper diorama, dark-blue background, sculpted Joshua, laptop, warm desk light, and torn cream paper banner with black cut-paper letters.
Composition/framing: keep the full portrait master. Set “HE STILL CRIED” on one line, horizontally centered in the open dark-blue band just above Joshua's hair. On this 941×1672 source, keep the banner top around 150 px (the 2:3 center crop begins at 130 px) and the banner bottom before the hair begins. Reduce banner width/height enough to fit that space while keeping the words large, clear, and unwrapped.
Text (verbatim): “HE STILL CRIED”. Spell exactly; no other lettering.
Constraints: change only the headline banner's size and position. Preserve Joshua's expression, pose, hair, hands, laptop, “55% REMAINING” display, room, lighting, shadows, and all other scene details. No added objects, new narrative, interface, logo, border, watermark, or extra text.
```

- One-change refinement after checking the crop:

```text
Use case: precise-object-edit
Asset type: Paper Detour Shorts cover, portrait 9:16
Input image: Image 1 is the current candidate. Preserve it as the edit target.
Primary request: Move the existing cream “HE STILL CRIED” banner farther down into the centered 2:3 safe area and make it slightly smaller, so its full torn-paper top edge and every letter have clear breathing room after the crop.
Composition: the 2:3 crop begins 130 px from the top on this 941×1672 image. Set the banner top about 35 px below that boundary and keep its bottom above Joshua’s hair; scale it to fit in the open band. Keep the phrase on one centered line.
Constraints: change only the banner and its text size/position. Preserve exact wording “HE STILL CRIED”, spelling and letter style. Do not alter the face, hair, pose, hands, laptop, “55% REMAINING” display, room, lighting, or any other pixels. No added text, objects, border, interface, or watermark.
```

# 027 — бумажные акценты v01/v02

Статус: подготовленные изображения для дальнейшей проверки в монтажном композите, не анимация и не утверждённый готовый шрифт. Исполнитель `/root/artist_typography`, встроенный инструмент imagegen, 31 октября 2026. Стиль сверялся с исходниками выпуска 001 `channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png` и `MATCH.png`: широкие скруглённые буквы, светлое бумажное лицо и тёплая объёмная подложка. Совпадение отдельных глифов не подтверждено.

- `1_MINUTE_v01.png` — визуально читается 1 MINUTE, RGBA 2142×734.
- `20_MINUTES_v01.png` — визуально читается 20 MINUTES, но пробел между числом и словом узок; сохранён для истории.
- `20_MINUTES_v02.png` — визуально читается 20 MINUTES, промежуток увеличен; RGBA 2172×724.
- `1710_v01.png` — визуально читается 1710, RGBA 1842×854.
- `THE_TATLER_v01.png` — визуально читается THE TATLER, RGBA 2141×734.
- `SATIRE_v01.png` — визуально читается SATIRE, RGBA 2107×746.
- `ONE_QUESTION_v01.png` — визуально читается ONE QUESTION, RGBA 2172×724. Надпись длинная, её читаемость в вертикальном кадре и на экране телефона ещё не проверена.
- `YOUR_LIFE_v01.png` — визуально читается YOUR LIFE, RGBA 2146×733.

Все изображения визуально проверены на написание. Режим RGBA, полный диапазон альфы и прозрачность четырёх углов проверены через Pillow; фон фактически прозрачный. Это не полная проверка альфа-края на каждом фоне: возможно цветное свечение и мелкие дефекты краёв; требуется проверка на светлом и тёмном композите. Каждая фраза — единый PNG, индивидуально анимировать отдельные буквы из этих файлов без дополнительного разделения нельзя. Окклюзия и выход из-за объекта, геометрия и движение в вертикальном кадре ещё не выполнены и не проверены.

## Точные запросы

Общие входные style references: указанные выше `A_MESSAGE.png` и `MATCH.png`. Для всех запросов — встроенная генерация, `transparent_background=true`.

Для `1_MINUTE_v01.png`:

```text
Use case: stylized-concept. Asset: a standalone animation-ready typography cutout for Paper Detour. The two input images are style references, not edit targets. Create precisely the single-line text “1 MINUTE”, spelled 1 M I N U T E, all capitals. Reproduce the references' wide rounded hand-cut paper character shapes, cream lightly textured paper face, warm rust-orange paper backing, subtly layered thickness and coherent soft dimensional shadow. Group the entire phrase and preserve clear space and clean margins around it. Real transparent background, without any backdrop, pattern, checkerboard or auxiliary object; no additional words, no punctuation, no clipping.
```

Для `20_MINUTES_v01.png` использован тот же запрос с формулировкой `“20 MINUTES”, spelled 2 0 M I N U T E S` вместо `“1 MINUTE”, spelled 1 M I N U T E`.

Для `20_MINUTES_v02.png`:

```text
Use case: stylized-concept. Asset: standalone transparent paper typography cutout for Paper Detour. The two reference images are STYLE references. Generate precisely the text '20 MINUTES' on one line, spelled 2 0 then a noticeable SPACE then M I N U T E S, all capitals. Keep a visibly wide transparent gap between 20 and MINUTES, about the width of half a letter, with no orange backing touching across that gap. Match the reference: wide rounded irregular handmade cut-paper letters, cream textured faces with rust-orange paper backing, subtle paper thickness and soft shadow. Transparent background and generous margins, no other text, no punctuation, no extra objects.
```

Для пяти оставшихся надписей использованы отдельные вызовы со следующим шаблоном; `{TEXT}` заменён соответственно на `1710`, `THE TATLER`, `SATIRE`, `ONE QUESTION`, `YOUR LIFE`:

```text
Use case: stylized-concept. Asset: standalone animation-ready cutout of a short paper text accent for Paper Detour. The two images are style references. Render precisely "{TEXT}" in capital letters as one horizontal phrase. Copy the references' wide rounded, slightly irregular hand-cut paper character shapes with cream paper faces, orange-rust paper backing, tactile paper texture, subtly layered thickness and soft shadow. Keep a clearly visible transparent space between words where applicable, with no backing joining across word gaps. Transparent background, ample clear margins, no other words, punctuation, objects or watermark.
```

## Дополнительные акценты

Созданы отдельные PNG `OLDER_v01.png`, `SCROLLING_v01.png`, `BEFORE_DAWN_v01.png`, `WHAT_HAPPENED_v01.png` (с вопросительным знаком в изображении), `NEVER_ENDS_v01.png`, `RELIABLE_SOURCE_v01.png`, `CHECK_AGAIN_v01.png`. Написание и пунктуация визуально сверены по каждому результату; все RGBA с альфой 0–255 и четырьмя прозрачными углами. Ограничения для предыдущего набора применимы и здесь; для длинных фраз особенно требуется мобильная проверка на фактическом фоне, а для знака вопроса — читаемость при уменьшении.

Для каждой фразы выполнен отдельный вызов встроенной генерации с указанными выше двумя PNG-референсами, `transparent_background=true` и этим точным шаблоном; `{TEXT}` заменён на точное содержимое, включая `?`:

```text
Use case: stylized-concept. Asset: standalone animation-ready cutout of a short paper text accent for Paper Detour. The two images are style references. Render precisely "{TEXT}" as one horizontal phrase, using all capitals. Copy the references' wide rounded, slightly irregular hand-cut paper character shapes with cream paper faces, orange-rust paper backing, tactile paper texture, subtly layered thickness and soft shadow. Keep a clearly visible transparent space between words where applicable, with no backing joining across word gaps. Transparent background, ample clear margins, no other words, objects or watermark. Preserve punctuation exactly when present.
```

## Замена неоднозначного CHECK AGAIN

Независимая проверка отметила, что `CHECK AGAIN` можно понять как призыв снова листать новости. Этот вариант сохранён как **отклонённый кандидат**; подготовлен `NEXT_CHECK_v01.png`. Визуальная проверка подтвердила написание NEXT CHECK и похожий бумажный характер; PNG 2172×724, RGBA, альфа 0–255, все четыре угла прозрачны. Совпадение с глифами эталона, читаемость на мобильном размере, композит по контуру и фактическая анимация ещё не проверены.

Встроенный imagegen, `transparent_background=true`, style references — `A_MESSAGE.png` и `MATCH.png` из 001. Точный запрос:

```text
Use case: stylized-concept. Asset: standalone animation-ready cutout of a short paper text accent for Paper Detour. The two images are style references. Render precisely "NEXT CHECK" as one horizontal phrase, using all capitals. Copy the references' wide rounded, slightly irregular hand-cut paper character shapes with cream paper faces, orange-rust paper backing, tactile paper texture, subtly layered thickness and soft shadow. Keep a clearly visible transparent space between words, with no backing joining across the gap. Transparent background, ample clear margins, no other words, objects, punctuation or watermark.
```

# Проверка края исторического листа / 027 сцена 02

**Результат: FAIL, не использовать кандидат в монтаже.** Пользователь запросил существующий стиль Paper Detour, а монтажу нужен прозрачный окклюдер, из-за которого акцент `OLDER` должен действительно выходить между слоями. Для `master_v02.png` была предпринята одна попытка встроенным OpenAI imagegen выделить верхний край старого печатного листа с сохранением координат и исходных деталей.

Результат `old_page_edge_candidate_v01.png`: RGBA, 941×1672, альфа 0–255; bbox пикселей с альфа >16 — `(0, 338, 700, 555)`. Отдельный [тест композита](occluder_test_candidate_v01.png) показывает, что генератор дорисовал и сдвинул край приблизительно на 60 px вниз: в сцене виден второй край листа, а накладка частично перекрывает телефон. Изображение листа и мелкие печатные штрихи отличны от мастера. Условие отсутствия двойников и точного совмещения не выполнено. Проверочный композит технический, не смонтированный кадр.

По указанию координатора детерминированную вырезку в обход imagegen не делать. Вместо неудавшегося листа можно **попробовать** существующие прозрачные `phone_v01.png` или `foreground_leaves_v01.png` как передний окклюдер для выхода `OLDER`. Эти отдельные слои просмотрены; возможность и читаемость именно такого выхода, контакт и корректное перекрытие текста не проверены в Palmier. Нужно проверить первый видимый кадр, середину и конец движения, фон и позицию слова относительно экрана/листьев в реальном монтаже, не выдавая простое плоское появление за перекрытие.

## Точный запрос и происхождение

Источник — `master_v02.png`. Использован встроенный OpenAI imagegen, `transparent_background=true`:

> Extract an occlusion mask asset from this exact 941x1672 paper-diorama composition. Preserve ONLY a narrow strip along the TOP edge of the old printed sheet, across the upper-left part of the old sheet, located approximately x=0 to 665 and y=275 to 470 in the ORIGINAL frame. Keep the ORIGINAL image pixels, diagonal edge, tiny printed marks, original scale, orientation, paper texture and lighting exactly as pictured. Remove the smartphone and ALL other scene objects and paper outside that strip. Everything else fully transparent, including region above the irregular top edge and through the rest of canvas. Do not enlarge, move, rotate, recreate or center the strip; do not add any illustrations or photos or legible writing. Output an actual transparent RGBA image of the SAME 941x1672 full-frame canvas.

Других вариантов не генерировалось; звук и Palmier не изменялись.

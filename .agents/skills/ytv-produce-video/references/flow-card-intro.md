# You But Weird: вступление с убираемой карточкой

Необязательный приём по одобренному опыту Desire, не требование к каждому фильму и не гарантия исполнения моделью. Выбор приёма не одобряет другую генерацию: внешняя партия требует отдельного решения по [процедуре клипов](video-clips.md), а конкретный полученный клип пользователь одобряет до вставки. Одобрение Desire не распространяется на новые Mind Reading intro, другие обложки или будущие генерации. Утверждённые финалы и pins существующих run не заменять.

## Постановка

В Google Flow Frames запросить 5 секунд, передав actual выбранную обложку как Frame A и actual первый кадр как Frame B. A — рисунок на непрозрачной физической карточке, изначально заполняющей экран без видимых краёв. Иллюстрированная рука/персонаж убирает её из-за кадра; B появляется только на освободившемся месте. Надпись, лица и фон A закреплены на карточке и уходят с ней, без превращения в B. Финал удерживает B. Не применять fade, cross-dissolve, прозрачное наложение, ghosting, double exposure, morph, cuts или вспышки; надписи A и B сохраняются без переписывания. Адаптировать действия и точные слова к actual A/B, не переносить сюжет Desire буквально.

Точный prompt одобренного опыта Desire (исторический образец, не универсальный prompt):

```text
Create a 5-second continuous illustrated shot using Frame A as the opening image and Frame B as the final composition.
Frame A is artwork printed on a solid, opaque card held very close to the camera. At first, the card fills the entire screen and its edges are not visible. Frame B is the scene behind the card, not an image to blend into it.
0.0–0.5 seconds: Hold Frame A clearly. Keep “THEY ALL WANT YOU” sharp and unchanged.
0.5–2.3 seconds: The woman in the blue blouse from Frame B physically lowers the card and moves it out of view to camera-right. The camera pulls back smoothly, revealing the card’s edge and the group behind it. Reveal the scene only where the opaque card has moved away. The printed faces, sofa, background and headline stay attached to the card and leave together as one solid object. They do not transform into the people or furniture behind it.
2.3–4.5 seconds: Continue the same uninterrupted shot. The woman sets the card aside and gestures toward the scarf-wearing protagonist. The surrounding adults lean slightly toward him with delighted smiles. He looks around, puzzled. Keep the movements small and fluid. Preserve the character designs, clothing, table and cup shown in Frame B. Smoothly settle into its framing and poses.
4.5–5.0 seconds: Hold Frame B steady. Keep “EVERYONE WANTS YOU?” readable and spelled exactly as shown.
The reveal is caused only by the physical movement of the opaque card and the camera. The two scenes never overlap transparently.
No fade, cross-dissolve, opacity animation, ghosting, double exposure, image blending, morphing, teleportation, wardrobe transformation, cuts or flashes. No added captions. Do not animate or rewrite either headline. No audio.
```

## Проверка и сборка

1. Открыть actual A и B, первый и последний кадры результата и весь клип в движении. Проверить читаемость обоих текстов, непрозрачность и непрерывное движение карточки, отсутствие fade/morph, стабильность и соответствие B; также проверить шов с основным видео. Небольшой redraw может отличаться от B попиксельно: оценивать видимые признаки и влияние на сцену, не объявлять пиксельную идентичность.
2. Проверить фактические duration, FPS, resolution и наличие/содержимое звука. Запрос 5 секунд и `No audio` не гарантируют этих свойств: исходный Desire Flow имел 4.958 с, 1280×720/24 fps и ненулевой AAC. Сохранить exact source и evidence; звук оценивать отдельно. Только после проверки нормализовать финальную сборку по профилю до 1080p30; для пятисекундного вступления это 150 кадров. Не скрывать недостаток source неподтверждённым freeze/loop.
3. Для такого пятисекундного вступления You But Weird начать narration в **t=3.000 s** финального timeline: две секунды overlap до конца intro в t=5. Согласовать первые реплики и кадры основного фильма с этим overlap по actual аудио; не вырезать содержание вслепую и не повторять стартовые реплики. Ранее собранная версия с началом речи после пяти секунд не является эталоном этого нового тайминга. Проверить звук, синхрон и стык на exact финальном MP4; отсутствие необходимого playback/listening остаётся UNVERIFIED.

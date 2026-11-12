# THE TRAVELER — персонаж v1

## Правило консистентности

Используй `reference/MASTER_SHEET.png` как **обязательный визуальный референс** и `reference/MASTER_FRONT.png` как канонический передний ракурс. При создании новых сцен лучше генерировать **фотореалистичный фон без персонажа**, а затем накладывать один из PNG из папок `turnarounds`, `poses` и `expressions`. Это сохраняет узнаваемость значительно надёжнее, чем независимая регенерация героя в каждой сцене.

## Неизменный дизайн

Молодой мультяшный мужчина, тёплая светлая кожа, взъерошенные каштановые волосы, большие круглые белые глаза и маленькие чёрные зрачки. Яркая горчично-жёлтая куртка с капюшоном, тёмно-коричневый внутренний слой, оливковые cargo-брюки, коричневые шнурованные ботинки, большой серо-оливковый походный рюкзак со свёрнутым ковриком. Толстая тёмная линия контура, чистые 2D-заливки и максимум две ступени теней. Никаких реалистичных текстур кожи, волос или одежды — аватар должен выглядеть нарочито чужеродным на фоне реалистичной истории.

Персонаж — современный путешественник по эпохам. **Не переодевать под викинга, римлянина или рыцаря; не менять постоянный костюм.** Можно дать в руки предмет (карту, пергамент, кубок) только когда это предусмотрено сценой и видно, что персонаж интерактивно присутствует в кадре.

## Промпт для дополнительной генерации позы

Use the attached MASTER_SHEET and MASTER_FRONT as exact identity references. Render ONLY the SAME 2D cartoon traveler, in [SPECIFIC POSE AND EXPRESSION]. Keep absolutely identical chestnut hair silhouette, giant round white eyes, tiny pupils, facial proportions, mustard-orange hooded jacket, dark brown inner shirt, olive cargo pants, brown lace-up boots and charcoal-olive backpack with rolled mat. Bold black outlines and flat cel colors. No photorealistic rendering on character. Isolated, transparent background, full body clearly visible, hands and boots not cropped, no words, no labels, no panels, no ground shadow, no other people. Match reference identity strictly, do not redesign.

## Промпт для исторического фона

Photorealistic cinematic historical reconstruction of [PERIOD, PLACE, YEAR, FACTUAL SCENE], 16:9, accurate material culture, period-appropriate clothes and architecture, natural lighting, suitable negative space for an animated host in the [LEFT/RIGHT] foreground. Absolutely no cartoon character, no modern objects, no lettering, no logos. Background only.

## Монтаж в Palmier Pro

1. Исторический фон 16:9 на базовой дорожке.
2. PNG из `poses` / `turnarounds` поверх, без рамки и без рендера фона вокруг персонажа.
3. Точки якоря фиксировать по ногам героя для полнофигурных поз; не деформировать пропорции.
4. Анимировать position/scale/rotation и небольшие body bob/talking cuts; для крупных планов использовать `expressions`.
5. Персонаж должен быть узнаваемым в обоих языковых версиях. Местоположение и эмоции могут меняться, одежда и лицо нет.

Важно: это слои PNG из генеративного concept sheet, а не 3D-риг или lip-sync персонаж. Для точной артикуляции придётся отдельно делать рот/слои или новые состояния.

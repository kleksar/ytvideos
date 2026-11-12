# Extra High consultation — editorial text overlays, Brest Fortress 039

- Date: 2026-11-04
- Model label observed immediately before the request: `Очень высокий`
- Chat: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6aeb4d00-a494-83ed-868d-6137738cf885
- Scope: visual treatment and timing for three approved overlay sets. No story or narration changes.

## Prompt

Ты — консультант в уже открытом ChatGPT Extra High. Требование внешнего координатора уже выполнено этим обращением; ответь здесь, не открывай другой ChatGPT. Одна узкая задача: предложи компактное оформление трёх редакционных текстовых оверлеев для 16:9 фильма Nuviko History о Брестской крепости. Не меняй narration, не исследуй историю. В фильме разрешены только точные строки: дата “23 July 1941”; отдельный факт-блок “453 killed or missing” / “668 wounded” с явной подписью “Brest-Litovsk fighting overall” (не только крепость); финальная реконструированная надпись “Я умираю, но не сдаюсь! Прощай, Родина” и дата “20 июля 1941 года”. Никаких других надписей в документе или на стене. Стиль: сдержанный, современный, исторический, читабельный на 2560×1440 и телефоне; не имитировать машинопись документа, не вклеивать текст как подлинный оригинал, не добавлять флаги/эмблемы/декор. Дай для каждого точные строки, иерархию/расположение и время появления по narration anchors, плюс 3 короткие проверки читаемости и фактической области. Не предлагай новые данные или сюжетные детали.

## Accepted decisions

### Shared overlay style

- Neutral modern sans-serif (Inter or Noto Sans), light text, no decorative elements. Add text in post-production as separate overlays, not inside generated images.
- Safe area: 150 px from side edges; top begins at 140 px. Keep the lower 280 px free for captions.

### 23 July 1941

- Exact text: `23 July 1941`.
- 94 px Medium, upper-left at X=160, Y=175, without a box or ornament; a soft shadow is allowed on a complex background.
- Starts on the spoken words “July 23, 1941” inside “Gavrilov’s biography gives July 23, 1941, as the date of his capture.” Remove by the end of shot 16.01, about 422.200–428.080 s.
- It refers only to Gavrilov’s capture, not the end of the fortress defense.

### German losses

- Exact lines: `453 killed or missing`; `668 wounded`; `Brest-Litovsk fighting overall`.
- Statistics: 88–96 px Medium, equal sizes. Scope label: 64 px Regular. Upper-right sector X≈1320–2390, Y≈170–570. A neutral translucent backing may be used; do not imitate the report.
- Begin on “the division lost 453 men killed or missing, with another 668 wounded.” The scope label appears with the first number. Reveal `668 wounded` when those words are spoken.
- Keep visible from shot 17.05a (about 503.648 s) through 17.06 (to 520.560 s), as the narration clarifies the geographical scope. Keep the label visible whenever either figure is shown.

### Final inscription

- Exact quote: `Я умираю, но не сдаюсь! Прощай, Родина`; exact date: `20 июля 1941 года`.
- Quote: 90–96 px Medium; a line break after the exclamation mark is allowed without changing punctuation. Date: 68–72 px Regular.
- Centered on the reconstructed wall, roughly X=300–2260, Y=330–780. Add as a flat editorial layer over the reconstructed wall; no handwriting, artificial aging, or claim to reproduce the original hand.
- Show the Russian quote from the English anchor “I am dying, but I will not surrender! Farewell, Motherland.” in shot 19.02a (about 565.137 s). Add the date in 19.03 after “July 20, 1941.” Keep the text present during narration about the unknown author. Cut directly to the report on “The German general left behind a report.” For the final repeated quote, return to the full inscription and date through 612.320 s. No hand-writing animation; the final wall holds still.

### Checks

- Review the final 2560×1440 frame at phone scale; all text must be readable without zoom, and captions must not overlap it.
- Keep `23 July 1941` attached only to Gavrilov; keep both casualty figures visibly paired with `Brest-Litovsk fighting overall` throughout their display.
- Keep the report non-legible and the wall free of extra text. Editorial text remains a separate layer, not a claim of original document lettering.

Timing guidance is anchor-derived. Exact word-level reveal frames must come from the current character alignment and be checked against the actual recording.

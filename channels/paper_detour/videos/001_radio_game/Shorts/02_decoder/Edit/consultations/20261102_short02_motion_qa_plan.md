# Short02 motion QA plan — 2026-11-02

External consultation was performed in the project ChatGPT workspace. The visible mode label immediately before submission was **«Очень высокий»**.

**Prompt:** «Ты консультант проекта „YT Видео“. Координатор лично проверил видимую маркировку режима непосредственно перед запросом: „Очень высокий“. Одна узкая задача: дай план targeted motion/framing QA для готового локального MP4 Paper Detour Short02. В ролике 1098 кадров, 30 fps, 7 сцен: [0,177), [177,330), [330,468), [468,606), [606,774), [774,924), [924,1098). Уже были фактически просмотрены 403 кадра для композиции/титров, но dedicated motion-extrema review не проводился. Движение целого изображения запечено в семи scene clips по отдельным finish receipts с линейными keyframes; титры screen-space. Составь минимальную конкретную выборку по каждой сцене (начало, 25%, 50%, 75%, последний кадр), предложи проверку видимого направления движения и реальных экстремумов через финальный MP4 и patch matching, критерии пустых границ, clipping, warping/jitter и безопасности титров. Не редактируй видео; отдели targeted PASS от общего QA, где слуховая синхронизация с речью остаётся UNVERIFIED. Максимум 220 слов.»

**Visible model label:** «Очень высокий».

**Result:** минимум 35 кадров, по пять на каждую из семи сцен, плюс фактические экстремумы, пропущенные сеткой. Sample IDs:

| Scene | Start | 25% | 50% | 75% | Last |
|---|---:|---:|---:|---:|---:|
| S01 | 0 | 44 | 88 | 132 | 176 |
| S02 | 177 | 215 | 253 | 291 | 329 |
| S03 | 330 | 364 | 399 | 433 | 467 |
| S04 | 468 | 502 | 537 | 571 | 605 |
| S05 | 606 | 648 | 690 | 732 | 773 |
| S06 | 774 | 811 | 849 | 886 | 923 |
| S07 | 924 | 967 | 1011 | 1054 | 1097 |

Use patch matching on static texture within each scene, excluding title overlays, to check visible direction, shift, and scale against the finish receipts. Establish actual displacement/scale extrema from final MP4 and add frames if a peak falls between the samples. Inspect borders/corners, unintended object clipping, depth/edge tearing, warping, jitter/reversals, and subtitle safe area at extrema. Record exact frame IDs and matching results. `MOTION_FRAMING_TARGETED` can pass only after this factual review; overall QA remains `UNVERIFIED` while spoken subtitle synchronization has not been checked by ear.

**Source conversation:** https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae8da79-7a90-83eb-b17b-34d93423204b

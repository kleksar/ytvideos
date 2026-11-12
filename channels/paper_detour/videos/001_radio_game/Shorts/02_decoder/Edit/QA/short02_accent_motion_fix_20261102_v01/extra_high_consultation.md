# Short02 accent-motion diagnosis — 2026-11-02

Project ChatGPT consultation performed before the implementation decision. The visible mode label immediately before the request was **«Очень высокий»**.

**Prompt:** «Ты консультант проекта „YT Видео“. Координатор лично проверил видимую маркировку непосредственно перед запросом: „Очень высокий“. Одна узкая техническая задача Paper Short02. Пользователь заметил в готовом review MP4, что верхние текстовые акценты неподвижны. Сверка с принятым монтажным правилом показывает: отдельные cream/orange PNG лежат на своих image tracks с fadeInFrames/fadeOutFrames, но без position/opacity keyframes; движение камеры сцены уже запечено в сценовых клипах. Принятый акцентный motion: вход снизу вверх с opacity 0→100%, остановка на принятом anchor, затем движение выше с opacity 100→0%; hold неподвижен. Что конкретно считать причиной и минимальным исправлением на canonical Palmier timeline? Сохраняются ли текст PNG, тайминг, положение hold и voice/A1, если добавить только принятые position/opacity keyframes к текущим cue clips и повторить локальный экспорт/QA? Не предлагай новые слова, звук или перестановку сцен. Ответ до 160 слов.»

**Visible model label:** «Очень высокий».

**Result:** причина — на текущих PNG-дорожках есть только fadeIn/fadeOut, но отсутствует самостоятельная анимация position; camera baked в scene clips не двигает независимые captions. Минимальное исправление: сохранить текущие cue clips и PNG, добавить к каждому cue `position`- и `opacity`-keyframes по принятому enter/hold/exit, сохранить границы/длительности и hold anchor, повторить локальный review export. Не менять слова, artwork, timing, scene order, voice/A1 и baked camera. После рендера проверить вход, hold и выход каждого cue, включая clipping и коллизии с subtitles. Motion PASS только после фактического просмотра; общий QA остаётся UNVERIFIED до слуховой проверки синхронизации.

**Source conversation:** https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae8da79-7a90-83eb-b17b-34d93423204b

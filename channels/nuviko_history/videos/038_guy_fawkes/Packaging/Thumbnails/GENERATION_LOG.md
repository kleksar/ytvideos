# 038 — журнал генерации обложек

Каждая запись: дата, концепция, назначение, точный запрос, инструмент и модель
(если известна), входные референсы и их роль, исходник, производные файлы,
статус, проверки, ограничения и необходимые SHA-256. Фиксировать подтверждение
пользователя и результаты теста только после фактического получения.

## v01 — three beta concepts (2026-11-04)

Tool: built-in image generation; three independent `ads-marketing` generations. Each generated 1672×941 PNG with integrated exact English lettering. The source PNG is retained; an upload derivative was made as 1280×720 JPEG at quality 90. No reference images used. The displayed results were reviewed for intended concept, lettering and broad phone-size contrast; no YouTube upload or performance test was made.

### A — leadership / famous face

Prompt: “Use case: ads-marketing. Asset type: 16:9 YouTube history thumbnail for Nuviko History, concept A, title ‘Guy Fawkes Is the Face of the Gunpowder Plot — But He Didn't Lead It’. Create a cinematic, high-contrast editorial split composition of two separate spaces. On the left, Guy Fawkes is discovered by lantern light in a stone undercroft near barrels, wary and caught. On the right, in a distinct separate chamber, Robert Catesby leads a small group in a plotting huddle, visibly the organizer. Do not make it look like one meeting; keep both faces large. Photorealistic historical reconstruction, tactile stone/wool/wood, candle and lantern light, sepia/charcoal/amber. Wide landscape 16:9, very large subjects, dark negative space for bold short phone-readable text across lower-left/lower-center. Exact lettering: ‘FAWKES CAUGHT. CATESBY LED.’ Uppercase, exact spelling and punctuation, heavy condensed cream letters with subtle dark shadow, no other words. No explosion, fireball, bodies, blood, modern objects, watermark or logo. Do not depict Fawkes as leader or show Fawkes and Catesby meeting.”

### B — warning / search

Prompt: “Use case: ads-marketing. Asset type: 16:9 YouTube history thumbnail for Nuviko History, concept B, title ‘How an Anonymous Letter Led to Guy Fawkes’ Arrest’. A large folded warning letter with indistinct unreadable writing dominates the foreground on a dark Jacobean table. In the background, out of focus but recognizable, royal searchers with lanterns begin searching a stone undercroft near powder barrels. No sender appears. Tell warning-to-search, not authorship. Photorealistic historical reconstruction, tactile paper/wax/wood/stone/wool, lantern light, amber/deep brown. Wide 16:9, close foreground letter on left, searchers and barrels on right, clear lower-band negative space. Exact lettering: ‘WARNING RECEIVED. SEARCH BEGINS.’ Uppercase, exact spelling/punctuation, heavy condensed cream with dark outline/shadow, no other words. No legible letter content, named sender, explosion, modern objects, watermark/logo, or clutter.”

### C — failure / later tradition

Prompt: “Use case: ads-marketing. Asset type: 16:9 YouTube history thumbnail for Nuviko History, concept C, title ‘How the Gunpowder Plot Led to Bonfire Night’. A later British November bonfire gathering at dusk, clearly a later tradition rather than 1605: a straw effigy of Guy Fawkes atop a controlled bonfire, distant townspeople watching, restrained fireworks in the sky. The effigy is recognizable by period clothing and a simple hat, not a real person. Evoke the long afterlife of a failed conspiracy as public custom. Photorealistic historical reconstruction, period clothing, warm firelight and cool blue twilight, cinematic amber/blue contrast. Wide 16:9; large effigy on right, small distant viewers, open darker sky/negative space upper left; short bold phone-readable text lower-left. Exact lettering: ‘FROM FAILURE TO TRADITION’, uppercase, exact spelling, heavy condensed cream with dark outline/shadow, no other words. Later custom; no blast, burning Parliament, bodies, modern signage, watermark/logo.”

| Pair | Source master | Upload copy | Master SHA-256 | Upload SHA-256 | Upload size |
|---|---|---|---|---|---|
| A | `Source/thumbnail_A_v01.png` (1672×941) | `Upload/thumbnail_A_v01.jpg` (1280×720) | `8468a1dd348105790ba4b4f83a4ba4d947512bd36c579e0462b7b376d548dece` | `5f43fb011c6aac570af43b215b2665acf64a03cb29492614b2bcce8ce9378de8` | 329 KB |
| B | `Source/thumbnail_B_v01.png` (1672×941) | `Upload/thumbnail_B_v01.jpg` (1280×720) | `412dac5ce67121bdf85603735fb7bd23c5fd5dda780621fc0cfaa8f07e0ef046` | `4f1d8bbc00f1f8f206fb3033e14e4f8511f90a00bd922c09707c8dcb559872f7` | 313 KB |
| C | `Source/thumbnail_C_v01.png` (1672×941) | `Upload/thumbnail_C_v01.jpg` (1280×720) | `704a7d3073c53ab4122bee31c1a2ecaaa38964f586ee2f2e6c0e8d22e4e46ae9` | `5c908194819cb9db0e6588274c4920382af3f69636bd5dde9c827ea43a49b62d` | 387 KB |

## Three new hooks v02 — 2026-11-04
Imagegen edits of corresponding A/B/C v01 masters. A: single cellar, THE KING WAS COMING. B: preserve letter and seal, separate editorial STAY AWAY. C: bonfire effigy, HE DIDN’T LEAD THE PLOT; corrected generated final period. Masters in Source; 1280×720 JPEGs in Upload. Mobile comparison in Review_v02/mobile_feed.html uses a simulated duration badge and an initial for the channel avatar. User selection pending.

## B v03
Imagegen produced first-person delivery of a sealed letter with editorial DON'T GO TO PARLIAMENT. Mobile comparison is Review_v02/mobile_feed_B_v03.html. User selection pending.

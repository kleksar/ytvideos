# Ragusa Short — three thumbnail options, v02

## Selection and application

The user selected option A, “SO CLOSE TO HOME”. Its uploaded 2160×3840 cover was saved on the existing Public Short in YouTube Studio on 2026-11-03. Studio displayed “Изменения сохранены.” and showed the selected cover preview. The title and Public access were unchanged. Options B and C remain unselected proposals; Shorts shelf propagation was not rechecked. Evidence: `../Metadata/SHORTS_THUMBNAIL_UPDATE_RECEIPT_v01.json`.

Target: Paper Detour `Y_TB6r4jI9I`, current title `Even Coming Home Meant 30 Days of Waiting`.
State: option A is applied in Studio; options B and C remain proposals. Studio confirmed the save. The current Shorts shelf was not rechecked after application. Native Shorts A/B testing is unavailable.

Visual references inspected: `channels/paper_detour/videos/038_47_ronin/Packaging/Thumbnails/Concept_A/Masters/PD038_A_for_one_man_v01.png` and `channels/paper_detour/brand/2026-10-30-channel-refresh/banner-unified-typography-2560x1440-v01.jpg`. The typography PNG paths named by `TYPOGRAPHY_STANDARD.md` were not present, so exact font-file compliance is not claimed.

## Files and bounded visual review

### A — SO CLOSE TO HOME
Return home: one traveler at the closed gate, rooftops visible through a narrow opening.
- master: `Masters/PD044_A_so_close_to_home_v03.png`; 981×1602; 3129891 bytes; SHA-256 `1e613a9fb23e0e38fb9b312e2260a8ab841863250deb433c456188b2f7eed2be`.
- export_9x16: `Exports/PD044_A_so_close_to_home_v03_9x16.png`; 900×1600; 2744315 bytes; SHA-256 `9dfd6437293a4fc46b84f3c0fa886523f7bbf3e314464a642a070efcdd2cf4f8`.
- QA: full 360×640 and central 360×540 / 180×270 previews at `QA_A_v03`; exact headline spelling and phone-size readability inspected. Live YouTube rendering and physical-device fit are not verified.

### B — 30 DAYS APART
The 30-day rule: two travelers wait at a schematic shore shelter, with a broad gap to the walled harbor.
- master: `Masters/PD044_B_30_days_apart_v01.png`; 941×1672; 3324517 bytes; SHA-256 `b557e8b43941fca60fa311d91a889bfc8bc0ccfd1b121e4ad5c35d9898688a9c`.
- export_9x16: `Exports/PD044_B_30_days_apart_v01_9x16.png`; 936×1664; 3054138 bytes; SHA-256 `039a8c0817b270b2197ff6641be3132508eb0c7f3f2b90f23648b4b616e37b1f`.
- QA: full 360×640 and central 360×540 / 180×270 previews at `QA_B_v01`; exact headline spelling and phone-size readability inspected. Live YouTube rendering and physical-device fit are not verified.

### C — 30 BECAME 40
The later change to forty days and the word quarantine: symbolic paper hourglass before the harbor.
- master: `Masters/PD044_C_30_became_40_v02.png`; 941×1671; 3107415 bytes; SHA-256 `b2520babfc3e548a9714905d132e84bddbe02068090846a779a44b7e60d5aea6`.
- export_9x16: `Exports/PD044_C_30_became_40_v02_9x16.png`; 936×1664; 2933854 bytes; SHA-256 `e40c474ef114b5b7e4101fef35429cbdbb57fea13cf0c0272cab9f40441f4234`.
- QA: full 360×640 and central 360×540 / 180×270 previews at `QA_C_v02`; exact headline spelling and phone-size readability inspected. Live YouTube rendering and physical-device fit are not verified.

## Image generation prompts

### Option A

```text
Create ONE finished image at an exact portrait 9:16 aspect ratio for a Paper Detour YouTube Shorts cover (target 941×1672 pixels). Emotional return-home angle, medieval Ragusa on the Adriatic in 1377. In a close three-quarter side view, one returning traveler with a small cloth bundle pauses before a massive closed stone-and-wood city gate. The traveler reaches toward the gate and looks through a narrow opening toward a few rooftops within the city: home is visibly near but still inaccessible. Keep the traveler’s face, hand and bundle in the lower-middle; let the gate rise along the right half and a glimpse of the warm city appear through the opening. This is a single clear action-led paper diorama, not a panoramic port view. Keep all lettering, face and meaningful props inside the central 2:3 safe area, with generous margins. Add exactly one headline, spelled exactly “SO CLOSE TO HOME”, on two lines in the upper-middle with clear breathing room above and below. The headline is large, broad rounded warm-cream paper cutout lettering, tactile fine fibers, subtle thickness, soft cast shadows, high contrast and readable at phone size. No other writing, signs, flags, logos, watermark, plague masks, medical symbols or extra numbers. Historically plausible 14th-century Adriatic architecture and clothing; do not identify a specific isolation site. Refined handmade layered paper/card miniature with carefully cut edges, believable stone and aged wood, soft contact shadows, nuanced late afternoon light, rich crafted material detail, not glossy CGI and not a flat illustration.
```

### Option B

```text
Create ONE finished portrait 9:16 YouTube Shorts cover for Paper Detour, as a distinctly different visual concept from a close traveler-at-the-gate scene. Story: in Ragusa in 1377, arrivals from plague-affected places had to wait separately for 30 days before entering; the exact historical isolation site is not specified. Show two small, clearly visible medieval travelers waiting beside a plain simple shore shelter in the near foreground. Between them and the fortified Adriatic harbor city lies a broad, quiet stretch of empty shoreline and water, making separation the main action; a few ships and the city walls sit far beyond. Use an elevated diagonal view that leads from the waiting figures toward the distant gate. Keep the shelter generic and schematic, not a named or distinctive historic quarantine building. No illness, masks, symbols, written signs, flags, or modern details. Add exactly this headline in two lines in the upper-middle: “30 DAYS / APART”. Use only these words and digits in the image. Lettering is large, crisp, rounded hand-cut paper, warm cream with visible fine fibers, slight thickness and soft contact shadow; verify exact readable spelling and spacing. Keep title, travelers and shelter inside the central 2:3 crop of the portrait with comfortable margins, especially above and below. Refined handmade layered-paper diorama with carefully cut edges, real paper/card texture, gentle contact shadows, natural restrained coastal daylight and expressive miniature depth. No other text, letters, numbers, labels, logos or watermark.
```

### Option C

```text
Create ONE finished portrait 9:16 YouTube Shorts cover for Paper Detour, a third concept clearly different from both a traveler at a gate and people waiting by a shore shelter. Accepted story: Ragusa required 30 days of separate waiting in 1377; a later forty-day period gave us the word quarantine. Show a tactile sculpted paper hourglass as a symbolic visual metaphor in the foreground (not a claimed historical Ragusan object). Around it, two large dimensional cut-paper numerals suggest a change in waiting time: place 30 slightly farther back and 40 closer to camera, connected by a subtle path of falling sand. Behind them, a small believable Adriatic walled harbor city and a distant ship anchor the scene in the story. Make the numeric change instantly readable, with elegant visual depth and one clear center of attention. Add exactly the English headline “30 BECAME 40” on two lines, with 30 and BECAME above 40; the numerals are part of this one exact headline. Do not include any other writing, dates, signs, labels or numbers. Keep headline, hourglass and both digits fully within the central 2:3 safe area of the portrait, with generous margins and readable at phone size. Paper Detour style: layered handmade paper/card miniature, visible fine fibers, crisp hand-cut edges, soft contact shadows, broad rounded warm-cream paper lettering with subtle thickness, restrained Adriatic daylight and warm stone; premium crafted miniature, not glossy CGI or flat infographic. No extra objects, logos or watermark.
```

C edit prompt (removed duplicate lower numerals and preserved one exact hook):

```text
Edit this Paper Detour Shorts cover. Preserve the medieval Adriatic harbor, city, ship, sculpted symbolic hourglass, layered paper materials, soft shadows and overall visual identity. Keep only one occurrence of the exact headline “30 BECAME 40”. Remove the extra large standalone 30 and 40 numerals from the lower half completely; do not replace them with any text or numbers. Restore the exposed stone quay and subtle falling-sand trail naturally as paper diorama scenery. Move the existing headline slightly downward and reduce it only a little if needed, so its top sits around 14–16% of the full portrait height and the entire phrase has comfortable margin inside the central 2:3 safe crop. Preserve the headline’s exact spelling, word order, cream paper lettering, legibility, and separate-line hierarchy. Keep the hourglass unobstructed and prominent. Add no dates, labels, signs, letters, numbers, logos, or watermark.
```


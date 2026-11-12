# Paper Detour clothing-film thumbnails — generation log

**Date:** 2026-11-01  
**Status:** The user selected A/B/C as this episode's packaging set. A remains untouched; selected replacements are B v06 and C v09. No upload or Studio A/B test has taken place.  
**Image tool:** built-in ImageGen.  
**Style reference inspected:** `/Users/diplomat/ytvideos/channels/paper_detour/brand/paper_world_reference/paper_diorama_approved.png`.

## Previous round — superseded after user feedback

| Variant | Title | Master PNG | Upload JPG | On-image text | Final generation |
|---|---|---|---|---|---|
| A | We Found Their Tools. Where Are Their Clothes? | `Concepts/a_tools_where_clothes_v02.png` | `Upload/a_tools_where_clothes_v02.jpg` | WHAT'S MISSING? | Second attempt; first looked too photographic |
| B | When Dresses Became Architecture | `Concepts/b_dresses_architecture_v02.png` | `Upload/b_dresses_architecture_v02.jpg` | A DRESS THIS WIDE? | Second attempt; first crowded the lower-right duration area |
| C | The River Stayed. The Silhouettes Didn’t. | `Concepts/c_river_silhouettes_v03.png` | `Upload/c_river_silhouettes_v03.jpg` | none | Third attempt; earlier silhouettes were too small and too similar to B |

These candidates were superseded after the user approved A and rejected B/C as weak. Their assets have been moved to `Archive/previous_round/`.

## Replaced candidate set — superseded after second style feedback

| Variant | Title | Master PNG | Upload JPG | On-image text | Status |
|---|---|---|---|---|---|
| A | We Found Their Tools. Where Are Their Clothes? | `Concepts/a_tools_where_clothes_v02.png` | `Upload/a_tools_where_clothes_v02.jpg` | WHAT'S MISSING? | Retained unchanged; user said A is good |
| B | Could a Dress Change Your Shape This Much? | `Concepts/b_shape_change_faceoff_v03.png` | `Upload/b_shape_change_faceoff_v03.jpg` | BOTH DRESSES? | Replacement candidate |
| C | How Did We Go From THIS to THAT? | `Concepts/c_four_eras_silhouette_sculpture_v06.png` | `Upload/c_four_eras_silhouette_sculpture_v06.jpg` | CENTURIES APART | Replacement candidate |

In this superseded set, masters were 1672×941 PNG and upload copies were same-resolution JPEG at quality 88. Those B/C files were checked full-size and at 320×180, then rejected by the user in the next feedback pass.

## Superseded concepts

- A first pass was too photographic; the final v02 emphasizes hand-cut paper strata and paper fibers.
- B first pass placed the skirt beneath the lower-right duration badge; the final v02 shifts the figure left and clears that corner.
- C v02 improved the paper construction but still made the crinoline the dominant, tiny-preview hook; it is in `Archive/previous_round/`. C v03 enlarged three period silhouettes, but the user still found the overall B/C round weak; it too is archived.
- The user later approved A and rejected the then-current B/C as weak. Those previous B/C images are archived; the replacement pair uses a direct crinoline-versus-1920s face-off and a bold four-era paper sculpture.

## Prompt A — final ImageGen request

```text
Use case: ads-marketing
Asset type: 16:9 landscape YouTube thumbnail concept A for Paper Detour
Primary request: A dramatically readable, curiosity-driven thumbnail for “We Found Their Tools. Where Are Their Clothes?” showing the contrast between durable stone tools and the absence of early clothing evidence.
Scene/backdrop: One handmade tabletop paper diorama of a prehistoric riverbank; layered ochre card terrain against a deep indigo paper sky.
Subject: A large, instantly recognizable prehistoric handaxe cut from angular, mottled grey paper. Nearby, a few delicate twisted paper-fiber strips are partly swallowed by the cut-paper sediment, suggesting the fragility of organic traces without depicting an actual garment or find.
Style/medium: Every visible surface is constructed from paper, cardstock, and cardboard: the axe is a faceted paper sculpture, the soil is stacked hand-cut card with clearly visible thin edges, fibers are rolled paper strips, water is folded blue paper. Handmade miniature craft, soft paper shadows, tactile but clearly illustrated, never photorealistic and never a conventional 3D stone render.
Composition/framing: Cinematic landscape 16:9. Large axe occupies left-center foreground; small paper river recedes at lower right; dark open negative space in upper-right supports headline. Strong visual hierarchy at 320×180: axe first, vanishing fibers second, headline third. No pedestal, no person.
Lighting/mood: Focused amber illumination on the axe and earthy card layers, deep blue shadow around the empty space; mysterious, bold, cinematic.
Text (verbatim): “WHAT’S MISSING?” large, heavy, rounded, cream-colored cut-paper uppercase letters in the upper-right negative space. Spell exactly with apostrophe and question mark; keep clear of the axe.
Constraints: Distinct cut edges, paper grain, physically grounded objects and contact shadows, one complete cohesive miniature scene. Lower-right duration-badge area unobstructed.
Avoid: Photographs, real rock texture, realistic soil, museum displays, empty pedestal, excavated clothing, clothing outline/imprint, any human figure, fake discovery or label, extra writing, tiny detail, logos, watermark, clutter, photorealism, conventional 3D render, separate layers, parallax, motion.
```

## Prompt B — superseded ImageGen request (v02)

```text
Use case: ads-marketing
Asset type: 16:9 landscape YouTube thumbnail concept B for Paper Detour
Primary request: Create a bold, immediately readable thumbnail paired with “When Dresses Became Architecture.” The visual hook is a historically plausible 1850s crinoline whose astonishing width changes the wearer’s silhouette.
Scene/backdrop: One restrained miniature paper stage, deep navy-blue background, a simple curved paper wall and one warm amber spotlight; no furniture or decorative props.
Subject: A single handcrafted paper woman in a mid-1850s crinoline gown. Her recognizable small upper body and head sit above an exceptionally broad, historically plausible domed skirt made from folded cream and terracotta cardstock.
Style/medium: Entirely handmade paper/card diorama: layered paper person, faceted paper features, folded cardstock skirt with visible cut edges, paper-stage background, soft physical contact shadows. Tactile and clearly crafted, not photographic and not smooth CGI.
Composition/framing: Wide 16:9. Put the woman and the massive skirt in the center-left, filling most of the left 70% with a clean readable silhouette. The skirt must end before the lower-right corner; keep the lower-right 18% as uninterrupted dark navy negative space so the duration badge cannot cover the dress. Keep upper-left clear enough for the headline while making sure it never overlaps the head. Strong mobile-sized focal hierarchy: skirt silhouette, small figure above it, short headline.
Lighting/mood: Warm amber spotlight only on the cut-paper dress, deep blue background and shadows; dramatic scale, playful surprise, no clutter.
Text (verbatim): “A DRESS THIS WIDE?” in large cream rounded hand-cut paper capitals, upper-left open space. Spell exactly and keep away from the figure and the dress outline, readable at 320×180.
Constraints: One coherent static scene, high contrast, plausible mid-19th-century crinoline proportions, lower-right duration-badge safe area empty.
Avoid: Extra figures, extra props, candles, furniture, wallpaper ornaments, big decor, fantasy balloon proportions, literal architecture/buildings, realism, real fabric photography, photoreal faces, digital 3D render, words other than the exact headline, logos, watermark, panels, separate layers, parallax, motion.
```

## Prompt C — superseded ImageGen request (v03)

```text
Use case: ads-marketing
Asset type: 16:9 landscape YouTube thumbnail concept C for Paper Detour
Primary request: A clear visual comparison for the title “The River Stayed. The Silhouettes Didn’t.” Make three sharply different human clothing silhouettes easy to read on a phone while one recurring fictional river links the eras.
Scene/backdrop: A single continuous, simple paper riverbank with a blue S-shaped paper river running behind the figures and a pale far-bank rock with one triangular notch. Invented symbolic European landscape; no specific city.
Subject: Three full-length handmade paper figures at similarly large scale, standing separately along the same near bank as a symbolic time comparison: left, a Roman-era traveler in tunic and draped cloak; center, a mid-19th-century woman in a broad crinoline dress; center-right, a contemporary 2020s pedestrian in casual trousers and jacket. Each figure is immediately recognizable by silhouette and occupies about half the image height. They represent separate centuries and are not meeting.
Style/medium: Handmade Paper Detour cut-paper/card diorama. Every figure, outfit, river, rock, bank, and distant hill is visibly made from flat, layered cardstock with crisp cut edges and folded paper depth; tactile paper texture, simple stylized faces, soft contact shadows, not photorealistic, not a conventional 3D scenic render.
Composition/framing: Wide 16:9 landscape. Arrange the three figures in the left two-thirds with enough separation to compare the silhouettes at 320×180. River curves behind them toward the notched rock. Keep the lower-right 20% as calm dark-blue paper water with no figure or key detail for the duration badge. No on-image text; the title carries the hook. One unified scene, no timeline panels.
Lighting/mood: Warm amber light on figures, blue river and background; vibrant but restrained, high-contrast silhouettes.
Constraints: Communicate “same recurring landscape, different moments” as visual metaphor. All figures firmly stand on the bank.
Avoid: Tiny distant figures, oversized foreground crinoline dominating the others, parasols, props, scenery clutter, detailed real cities, bridge, map or date labels, simultaneous gathering, split-screen, collage, photorealism, realistic skin or fabric, smooth CGI, text, logos, watermarks, separate layers, parallax, movement.
```

## Previous-round QA record — superseded

- Viewed each final image full-size and as a 320×180 preview after JPEG export.
- A: “WHAT'S MISSING?” is legible; the generic cut-paper stone tool and fading fibers read at small scale. Risk of implying a specific missing artifact is reduced by avoiding a plinth or garment outline.
- B: “A DRESS THIS WIDE?” is legible; the paper figure and broad crinoline read clearly; the lower-right duration-badge area is dark and unobstructed.
- C: no text; three different period silhouettes remain distinguishable in the small preview; the recurring river and notched rock read as a continuous symbolic landscape; lower-right area is open water.
- The three candidates use different visual hooks and compositions. They are thumbnail concepts, not accepted film frames. Their final promise-to-edit comparison remains pending until the user accepts the story and the film is cut.
- No upload, publication, or Studio A/B test was performed.

## Superseded prompt B — replacement v03

    Use case: ads-marketing
    Asset type: replacement YouTube thumbnail B, Paper Detour, landscape 16:9
    Primary request: A striking silhouette face-off paired with “Could a Dress Change Your Shape This Much?” Compare a huge mid-19th-century crinoline to a narrow late-1920s dress. The visual promise is the contrast itself, not why it happened.
    Scene/backdrop: A single continuous handmade miniature paper theatre stage, deep midnight-blue cardstock background, no real room or scene.
    Subject: Two historically plausible paper women, same head height, facing slightly toward one another as a symbolic comparison, not a historical meeting.
    - Left: mid-19th-century woman in an enormous bell-shaped ivory crinoline, the skirt dominating the left half.
    - Center-right: late-1920s woman in a streamlined coral-red straight dress with an era-appropriate hem, visibly narrow silhouette.
    Style/medium: Every visible element is handmade paper/card: dimensional miniature figures, folded-paper garments, tactile fibers, crisp cut edges, layered thickness, sculpted pleats, soft physical contact shadows. Premium Paper Detour paper diorama, visibly crafted, not fashion photography, not ordinary CGI.
    Composition/framing: Wide 16:9 landscape. Strong diagonal face-off and extreme width contrast. Keep both complete silhouettes unmistakable at 320×180. Put the figures within the left and center 78%; leave the lower-right 20% empty dark navy for YouTube duration badge. Keep upper-center negative space clear for a short headline without covering either head.
    Lighting/mood: Warm spotlight on the ivory and coral paper outfits, saturated deep-blue shadows; dramatic, high contrast, immediate phone readability.
    Text (verbatim): “BOTH DRESSES?” in large, bold, cream-colored hand-cut paper capitals across the upper-center negative space. Exact spelling; crisp and legible.
    Constraints: One unified full-frame still, no panels, the women represent different centuries and do not meet.
    Avoid: Generic single-gown fashion poster, women touching, implying a real encounter, claiming a cause for fashion change, fantasy proportions, extra people, furniture, candles, props, dates, logos, watermark, tiny text, photorealism, real fabric, split screen, collage, separate layers, parallax, motion.

## Superseded prompt C — replacement v06

    Use case: ads-marketing
    Asset type: replacement YouTube thumbnail C, Paper Detour, landscape 16:9
    Primary request: A spectacular paper-sculpture thumbnail paired with “How Did We Go From THIS to THAT?” Show four sharply different clothing silhouettes from different eras.
    Scene/backdrop: One continuous tabletop paper-diorama stage against deep midnight-blue cardstock.
    Subject: One fully clothed neutral paper mannequin just left of center, wearing a simple opaque ivory long-sleeved tunic and trousers from neck to ankles, with a smooth blank paper face and covered hands. Around it, four enormous dimensional cardstock clothing silhouettes fan outward like a single sculptural display:
    1) broad Roman Britain-inspired ochre draped tunic and cloak;
    2) structured late-16th-century Amsterdam merchant outfit in burgundy;
    3) narrow straight coral-red 1920s dress;
    4) oversized teal 2020s jacket and trousers.
    Each silhouette is recognizable from shape and color alone. Symbolic comparison across eras, not literal clothing worn simultaneously. No prehistoric garment.
    Style/medium: Premium handmade paper/card sculpture; crisp hand-cut edges, visibly thick cardstock, folded paper forms, tactile fibers, layered depth, warm directional light and soft contact shadows. Clearly crafted miniatures, not photography, not smooth CGI.
    Composition/framing: Wide 16:9. The silhouette fan fills the left and center 78% of the frame. All four forms remain large and distinct at 320×180. Place the teal 2020s jacket in the upper-right-middle; its lower edge ends above the lower-right corner. Reserve the lower-right 20% as a clean, continuous patch of dark navy stage with absolutely no garment, mannequin, shadowed object, lettering, or important detail, for the YouTube duration badge. The empty area is open stage, not a panel or card. Keep headline in upper-left clear space.
    Lighting/mood: Warm spotlight catches raised paper edges; deep-blue negative space between contours creates drama.
    Text (verbatim): “CENTURIES APART” in large cream hand-cut uppercase letters across the upper-left negative space; exact spelling and high contrast.
    Constraints: One cohesive static physical sculpture, no panels; safe lower-right corner truly empty.
    Avoid: Naked mannequin or visible anatomy, open lower-right corner clutter, garments touching bottom-right edge, tiny figures, collage, timeline arrows, dates, extra text, extra people, props, nudity, photorealism, real fabric, separate exported layers, parallax, movement, logos, watermark.

## Previous QA record — superseded after second style feedback

- A remains byte-for-byte unchanged in the thumbnail folders and is the user's preferred variant.
- B v03: viewed full-size and at 320×180 after JPEG conversion. “BOTH DRESSES?” is legible; the crinoline versus 1920s silhouette contrast reads immediately. The lower-right duration-badge area stays dark and open.
- C v06: viewed full-size and at 320×180 after JPEG conversion. “CENTURIES APART” is legible; four era shapes read separately; the neutral figure is fully clothed; the lower-right duration-badge area is empty dark stage.
- The story text is still a user-unapproved draft; final promise-to-cut review remains pending. No upload, publication, or Studio A/B test was performed.

## Current round — A-inspired cinematic packaging, 2026-11-01

The user said A is detailed, beautiful, intriguing, and has the right mainstream click appeal: one large bright ancient object, warm dramatic light, dark open field, and oversized headline. Earlier B/C were rejected as raw and too much like plain paper-fashion displays. This pass follows A's hierarchy and contrast while allowing richer textile detail and retaining tactile paper/earth cues where useful. A was not edited.

### Current title and thumbnail pairs

| Variant | Title | Master PNG | Upload JPG | On-image text | Status |
|---|---|---|---|---|---|
| A | We Found Their Tools. Where Are Their Clothes? | `Concepts/a_tools_where_clothes_v02.png` | `Upload/a_tools_where_clothes_v02.jpg` | WHAT'S MISSING? | Retained unchanged; user-approved |
| B | When Dresses Were Huge | `Concepts/b_crinoline_then_this_v06.png` | `Upload/b_crinoline_then_this_v06.jpg` | THEN / THIS? | Selected by user |
| C | Would You Wear This Today? | `Concepts/c_1559_fashion_v09.png` | `Upload/c_1559_fashion_v09.jpg` | FASHION / IN 1559? | Selected by user |

### Extra High packaging direction

- The approved image A uses a hero object in the foreground, amber light on ochre texture, deep navy negative space, and very large cream uppercase copy. The coordinator described these observed features in the consultation prompt.
- B sells one high-contrast silhouette jump: huge ivory crinoline versus a narrow crimson 1920s dress. The image text points from “THEN” to “THIS?”; the film's visual payoff is the crinoline-to-1920s comparison, without claiming to explain its causes.
- C sells the strangeness of a specific old silhouette: a close, richly detailed 1559 Amsterdam merchant doublet and bright white ruff, with the later 2020s contrast carried by the title and chronology. The modern silhouette was removed from the final image so the duration-badge corner stays clear.
- The consultant's final title recommendations were B “When Dresses Were Huge” with “THEN / THIS?” and C “Would You Wear This Today?” with “FASHION / IN 1559?”. The user selected the A/B/C package set; its fit against the final story remains to be checked.

### Final image-generation prompts and edits

**B v06 — base prompt:**

```text
Create one premium, cinematic 16:9 YouTube thumbnail, visually rich like a dramatic historical documentary and composed for instant phone-size readability. One complete unified scene, no collage, no panels.

A gigantic, historically plausible mid-19th-century ivory crinoline dress dominates the left foreground, filling nearly two-thirds of the frame. Its bell-shaped skirt is enormous, detailed with dense cream silk folds, delicate stitching, tiny wear marks, and sculptural shadows; the very narrow waist makes its astonishing width obvious. Directly to its right, a dramatically slim late-1920s straight coral-red dress creates a sharp silhouette contrast. Show just enough of each wearer to establish two different historical outfits; heads small and secondary, no fashion-catalog posing. The comparison is symbolic across eras, not an encounter.

Make the crinoline the bright hero object: warm amber light rakes across its folds and catches its edge; subtle ochre earth and tactile paper-cut strata recede beneath it. Deep midnight-navy shadows open on the upper-right for the text. Cinematic depth, intricate tactile surface detail, beautiful high-end finish; a restrained handmade paper / layered-card quality in the ground and edges, while fabric itself has convincing dimensional folds rather than flat cardboard. Bold warm-versus-cool color separation, unmistakable shape even at 320x180.

Place exactly “WHERE DID IT GO?” in huge, heavy, warm-cream uppercase lettering in the upper-right dark negative space. Spell perfectly, keep clear of the garments and readable on a phone. Leave the lower-right corner clear of garment and important detail for YouTube's duration badge. No other text, no logos, no watermarks, no decorative clutter.
```

**B headline edits:** The first minimal edit replaced `WHERE DID IT GO?` with `THEN THIS?`; a second headline-only edit enlarged it and stacked the exact words on two lines, `THEN` / `THIS?`, leaving the image unchanged.

**C v09 — base prompt:**

```text
Create one premium, cinematic 16:9 YouTube thumbnail with the visual richness and immediate curiosity of a major historical documentary. One complete unified scene, no collage, no panels.

A striking late-16th-century Western European merchant outfit inspired by Amsterdam around 1559 dominates the left and center foreground, shown in powerful close three-quarter view on a mostly shadowed human figure. The outfit is a dark burgundy velvet doublet with distinctive padded sleeves, a fitted waist, intricate period-appropriate seams and stitching, and a crisp, luminous white linen ruff collar. Make the enormous sculptural ruff the bright instantly recognizable focal element: each fine fold catches sharp warm amber light, with rich detailed velvet texture and deep sculptural shadows. The face remains largely in darkness and secondary. The outfit should feel unfamiliar and arresting to a modern viewer, yet grounded in a plausible late-16th-century silhouette.

At the far right, partially emerging from midnight-blue shadow, include only the restrained silhouette of a contemporary oversized jacket and trousers as a secondary comparison, not a second portrait or fashion lineup. Rough ochre ground and subtle layered paper-cut strata recede below the figure. Dramatic amber-on-navy lighting, deep atmosphere, premium film-still detail, tactile handmade edges only where they add richness. Avoid flat cardboard clothing and fashion-catalog posing.

Reserve upper-right navy negative space for the exact words “THIS WAS FASHION?” in huge, heavy, warm-cream uppercase lettering. Spell perfectly; make it exceptionally legible on a phone. Keep text away from the ruff and silhouette. Leave the lower-right corner clear for YouTube's duration badge. No other text, no logos, no watermarks, no extra decorative props.
```

**C headline and safe-corner edits:** The headline was changed to `FASHION IN 1559?`, in huge warm-cream uppercase. A final minimal edit removed the distant modern silhouette from the lower-right and filled that region with quiet dark riverfront. The new final master is C v09.

### Current QA

- Final B v06 and C v09 were reviewed full-size and from 320×180 JPEG previews. B's crinoline/1920s contrast reads immediately and `THEN / THIS?` is legible at phone size. C's ruff and burgundy doublet are the dominant object; `FASHION / IN 1559?` is legible and the bottom-right corner is open.
- Masters are 1672×940 (B) and 1672×941 (C); upload copies are same-resolution JPEG at quality 88. Both previews retain strong warm/cool contrast and large focal hierarchy.
- A was left untouched. Earlier B/C images and intermediate edits were moved to `Archive/previous_round/`.
- The plot remains an unapproved draft. Final promise-to-edit check must follow approval and final cut. No upload, publication, or Studio test was performed.


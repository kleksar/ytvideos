# Image prompt provenance v01

Exact outgoing prompts and supplied reference roles for images generated on 2026-11-05. Other files in `Source/Images/` were created earlier in this production run; their exact prompt payloads are not yet captured in this record and must be recovered or re-generated into a complete manifest before final image handoff. A reconstructed prompt summary is not represented as an exact original.

## Scene 026 — `scene_026_v01.png`

Exact prompt:

> Use case: photorealistic historical reconstruction for a Nuviko History long documentary, 16:9 landscape, detailed but natural. Scene 026: a Soviet Tu-95 Bear-A bomber cruising steadily high above the clouds, calm side view slightly from below, four distinctive contra-rotating propellers visibly turning, characteristic long swept wing and tall tail clearly legible; soft cold daylight, cloud horizon and open sky. The supplied source photo anchors the actual Bear-A silhouette, proportions and engine/propeller layout only; generate a new clean side-flight composition and do not copy the source framing or Soviet star insignia. No text, numbers, emblems, weapons, smoke, battle, or other aircraft. Documentary reconstruction, not archival footage. Leave modest open sky above for captions; keep full aircraft silhouette inside a 16:9 crop, ultraphotoreal materials and natural optics.

- Supplied reference: `Research/VisualReferences/tu95_bear_a_flight_1977_dod_publicdomain.jpeg`, SHA-256 `25b69c6013021907ac19a7737216cd1dbd3634ebc61b17444b5da7100b33210d`; aircraft identity and silhouette only.
- Output: 1672×941 PNG; SHA-256 `800de2e60515b5372f8692ef0d082e976c0d46eb1a315f819655d04d6bbde2a6`.
- Imagegen control values: no explicit size/quality controls available in the built-in tool call; actual size measured from returned file.

## Scene 035 — `scene_035_v01.png`

Exact prompt:

> Nuviko History documentary scene 035, 16:9 photorealistic explanatory model. High front-quarter view of a precise Tu-160 scale model on a clean industrial test table, with the variable-sweep wing panels fully extended in the broad low-sweep configuration. Soft, even workshop light; symmetrical fuselage, both full wingtips and landing gear visible; convey a broad, supportive wing suited to long subsonic cruise. The supplied Tu-160 reference anchors exterior proportions and silhouette only. Keep it unmistakably a physical explanatory model, not archival footage. No labels, numbers, text, logos, weapons or people. Natural materials, clean frame and upper subtitle-safe margin.

- Supplied reference: Tu-160 in-flight photo listed in `VisualReferences/README.md`; aircraft exterior only.
- Output: 1672×941 PNG; SHA-256 `dd6b8f69016c79ee5cf79a7ce79bae1a577e33e64490ce7dcacd7ab829fb4056`.
- Imagegen control values: no explicit size/quality controls available; actual size measured from returned file.

## Scene 036 — `scene_036_v02.png`

Exact prompt for v01:

> Nuviko History documentary scene 036, 16:9 photorealistic explanatory test. Side technical close-up of a physically plausible small Tu-160 aerodynamic model mounted in a real wind tunnel, broad wings in low-sweep position. Fine real smoke filaments flow smoothly over and behind the wing to make airflow legible; no glowing effects, digital arrows, labels, or fake measurements. Focus the crisp wing and translucent smoke against a dark tunnel, dramatic but restrained work lights. The supplied Tu-160 reference anchors the outside silhouette and wing arrangement only; hide any internal structures not supported by the reference. Clearly a present-day explanatory test, not a historical record. Keep model and smoke within crop with upper subtitle-safe margin.

It generated a red star on the tail and blue-yellow fuselage stripes, so v01 was rejected. Exact edit prompt for v02:

> Edit this exact image. Remove only the red star marking on the tail and the blue-and-yellow fuselage stripes. Keep the same model, smoke flow, wind tunnel, lighting, camera angle, support stand and overall composition unchanged. Preserve a clean unmarked white model surface. No new markings or text.

- Supplied reference: Tu-160 in-flight photo listed in `VisualReferences/README.md`; aircraft exterior only.
- Output v02: 1672×941 PNG; SHA-256 `b7ccfc870829fdb8fe45a88890cd3a9e6729ea412918d5b0c6db6719327b0397`.
- Imagegen control values: no explicit size/quality controls available; actual size measured from returned file. The v01 generated source remains in the Codex generated-images area; it was not added to `Source/Images/`.

## Scene 037 — `scene_037_v01.png`

Exact prompt:

> Nuviko History documentary scene 037, 16:9 photorealistic explanatory reconstruction. A tight diagonal view from the root toward the tip of a white Tu-160 wing section, seen against deep blue high-altitude sky. The sharply swept leading edge fills the frame; realistic rivet lines and smooth painted skin catch cold overhead sun, with no aircraft nose or other setting detail. The composition turns from the previous broad-wing view toward a new geometry. Supplied Tu-160 photo anchors wing proportions and exterior shape only. Do not add markings, text, logos, shock waves, or unsupported mechanisms. Full wing edges remain inside frame; keep motion-safe space along the diagonal.

- Supplied reference: Tu-160 in-flight photo in `VisualReferences/README.md`, exterior only.
- Output: 1672×941 PNG; SHA-256 `4a2bdbb132fd39fe617ee311dcbbed3b4111163b9a90b9c2e416379001fcdfbe`.

## Scene 038 — `scene_038_v01.png`

Exact prompt:

> Nuviko History documentary scene 038, 16:9 photorealistic explanatory model test. Inside a real dark wind tunnel, show a clean white swept-back wing model at a slightly overhead angle, strong visible sweep and a smooth trail of fine smoke lines passing over it. The wing angle and coherent airflow are the entire visual point: backlit filaments, crisp metal edges, dramatic restrained contrast. This is an explanatory physical experiment, not a recorded historical test. The supplied Tu-160 photo is a broad outer-wing identity reference only; don't invent shock waves, internal mechanisms, labels, measurements, markings, text or logos. Keep the model wing and trails within frame with enough dark space at top for captions.

- Supplied reference: Tu-160 in-flight photo, outer-wing identity only.
- Output: 1672×941 PNG; SHA-256 `399744fb200a0a8daadf63b6ee6daece1758fae5925136a2fd02609d305673b3`.

## Scene 039 — `scene_039_v01.png`

Exact prompt:

> Nuviko History documentary scene 039, 16:9 photorealistic explanatory physical model. Extremely low side view along a narrow test platform placed beside a runway surface; a small swept-back Tu-160 model sits on sturdy test gear, its rear-swept wings plainly visible. The long runway lines converge into distant haze, making the model's high-speed geometry feel sleek while the ground-level camera reminds us what this shape gives up for takeoff and cruising lift. Clear early-evening hard side light, no failure or crash, no smoke or motion blur. Supplied Tu-160 photo anchors outside form and variable-wing placement only. Keep tips, gear and nose all within the crop; no labels, markings, logos, text, weapons or people. Physical model, not a real historical event.

- Supplied reference: Tu-160 in-flight photo, aircraft silhouette only.
- Output: 1672×941 PNG; SHA-256 `e07e28663edf4095062fd179ef7848f2570970bb5de0c73a75ae06012229e7f6`.

## Scene 040 — `scene_040_v01.png`

Exact prompt:

> Nuviko History documentary scene 040, 16:9 wide: the recurring illustrated traveler stands waist-up at the left beside a very broad Tu-160 wing set in its extended configuration, looking along the leading edge as he explains the takeoff/cruise trade-off. His torso is turned three-quarter right; his left palm is held horizontal beneath the wing edge to echo its broad plane, and his right hand is half open near his chest. Expression focused and questioning. The traveler must remain a 2D drawing with dark outlines and soft colored shading on face, hair, body and ochre jacket; the aircraft, wing, display environment and all materials are ultraphotoreal, with realistic contact and light. Both traveler references anchor his identity, clothing and drawn rendering only; do not copy their pose. Tu-160 photo anchors wing and external silhouette only. Hard side light creates a crisp contrast across the wing. Keep the left hand, face and full visible leading edge clear and in frame; preserve caption-safe lower area. No additional people, text, logos, labels or markings.

- Supplied references: both traveler anchors and Tu-160 exterior photo; exact reference hashes and roles are in channel and episode records.
- Output: 1672×941 PNG; SHA-256 `c4ae769b53099430c21578fc0a871b158add993d5d67713a2dd211bcf015e90e`.

## Scene 041 — `scene_041_v01.png`

Exact prompt:

> Nuviko History documentary scene 041, 16:9 photorealistic explanatory close-up. Tight overhead macro on the Tu-160's movable outer wing panel meeting its fixed center section at the root. Show only the visible exterior panel seam, structural joint cover and pivot region that can be seen on the real aircraft; preserve realistic metal skin and attachment alignment, do not expose invented internal gears, bolts, pistons or hidden structure. A narrow workshop light picks out the axis and both panel edges against a quiet dark hangar floor. The attached real Tu-160 photo is the visual anchor for exterior placement and wing shape only; no source-photo markings should be copied. This is a present-day explanatory display/model view, not archival footage. No people, text, diagrams, labels, logos, weapons, or markings. Keep the whole visible joint and both adjoining surfaces within the frame.

- Supplied reference: Kubinka Tu-160 photograph, exterior wing root only; no internal pivot detail.
- Output: 1672×941 PNG; SHA-256 `43c1774677d742c795ab123e9dfe47cdb1712f04da0370e1a22478b53884f129`.

## Scene 042 — `scene_042_v01.png`

Exact prompt:

> Nuviko History documentary scene 042, 16:9 photorealistic reconstruction. Near-orthographic aerial view looking straight down on one complete Tu-160 in bright even daylight; aircraft centered on neutral concrete, all parts within frame. Make the fixed center wing structure and two fully extended movable outer panels visually distinct through natural panel seams and light, so the variable-sweep design reads without graphics. Preserve exact recognizable Tu-160 planform and proportions from the supplied real photograph. No new markings, text, numbers, labels, diagram overlays, weapons or people. This is a clean reconstruction, not archival footage. Keep nose, tail, both wing tips and four engines clearly inside the crop; subtle calm presentation.

- Supplied reference: Kubinka Tu-160 photograph, outside silhouette and wing configuration only.
- Output: 1672×941 PNG; SHA-256 `7b2d3d4eacf0b8eaeff1caeb6546c4e9e45e2b33c11a5d995eda7619af6eca56`.

## Scene 043 — `scene_043_v02.png`

Exact prompt for v01:

> Photorealistic Nuviko History reconstruction, scene 043, 16:9 landscape: a Tu-160 on a Soviet-era runway in takeoff configuration, wings fully extended, viewed from a high frontal three-quarter angle. Make the broad variable-sweep wings, nose and complex landing gear all legible; early morning clear light, full aircraft within the frame with enough runway around it to feel very large. The actual Tu-160 image anchors the aircraft's external silhouette and proportions; a physical model reference anchors the fully extended wing position only. Show a real aircraft, not a scale model. No labels, invented numbers or emblems, weapons, people or explosions. Caption-safe upper sky, realistic ground shadow and perspective; no distortion of span or aircraft proportions.

v01 contained blue-yellow invented fuselage stripes. It was rejected; exact edit prompt for v02:

> Edit this exact image and remove only the blue-and-yellow fuselage stripes. Preserve the Tu-160, runway, open wings, shadows, lighting, perspective and composition exactly. Replace the stripe area with natural white aircraft skin matching adjacent surfaces. Add no markings, text or other new details.

- Supplied references: Tu-160 exterior photo and scene 035 wing-extended model, respectively.
- Output v02: 1672×941 PNG; SHA-256 `bfde04655f957a698bb75077dfe8adae0a617051042b5206816a3db7498300f9`.

## Scene 044 — `scene_044_v02.png`

Initial v01 exact prompt:

> Nuviko History documentary scene 044, 16:9 photorealistic reconstruction. Tu-160 in flight above a high cloud deck from an upper three-quarter side angle, wings in a distinct intermediate sweep position: neither fully extended nor fully swept back. Let the wing panels and main fuselage read clearly, bright hard daylight with deeper cloud shadows, dynamic but steady flight. This frame continues the variable-wing explanation; the next will show maximum sweep. Actual Tu-160 reference anchors the aircraft silhouette; the extended-wing reference anchors the broad configuration and pivoted outer-panel placement. Show the real aircraft, no model. No contrails, sonic boom, invented markings, labels, text, weapons or people. Preserve the full silhouette and wing edges inside frame.

v01 repeated the open-wing state and invented blue-yellow nose stripes, so it was excluded. Exact v02 prompt:

> Nuviko History documentary scene 044, 16:9 photorealistic reconstruction. Show a Tu-160 from a high upper three-quarter side angle in flight above bright broken clouds, with both variable-sweep outer wing panels visibly at an intermediate angle: clearly narrower than the fully extended wings in the first supplied reference, but noticeably wider than the fully swept-back wings in the second. The aircraft is steady, not accelerating; clear hard daylight and rich cloud depth. This frame continues the variable-wing explanation; the next will show maximum sweep. The two references anchor the same Tu-160 and the two endpoint wing configurations; create the distinct middle state between them. No painted markings, text, numbers, logos, weapons, smoke, contrail or sonic-boom effect. Keep the entire aircraft and both wing edges inside the wide frame. This is a reconstruction, not archival footage.

- Supplied references: scene 042 extended configuration and scene 007 fully swept flight reconstruction. The latter uses a real Tu-160 reference in its own provenance.
- Output v02: 1672×941 PNG; SHA-256 `b23713adffe53399d121640015f1744926b308a229262dcda5bf8476a662ccc5`.

## Scene 045 — `scene_045_v01.png`

Exact prompt:

> Create scene 045 for a Nuviko History 16:9 documentary: a Tu-160 bomber in level flight over high cloud, seen from high above at a diagonal angle, with both movable wing panels fully swept back to their narrowest high-speed configuration. The wings must read clearly as strongly swept, close to the fuselage line, with no broad triangular spread. Use cool bright light and a dramatic blue-white cloud depth. This is a photorealistic reconstruction, not archival footage. The attached actual in-flight Tu-160 photo is the sole aircraft geometry reference; preserve its recognizable form and its swept-wing orientation. Keep entire aircraft silhouette in view. No labels, numbers, markings, logos, weapons, smoke, sonic boom or other aircraft.

- Supplied reference: Tu-160 in-flight photograph in `VisualReferences/README.md`, identity and maximum-sweep silhouette only.
- Output: 1672×941 PNG; SHA-256 `449e1e098010215f723d21b6bd74d1a0d2135e10f50d3e6804afdab246200fea`.

## Scene 046 — `scene_046_v02.png`

Exact prompt for v01:

> Nuviko History scene 046, 16:9 photorealistic historical reconstruction: a gigantic Tu-160 wing-root connection and adjoining fixed structure seen from very low inside a clean aircraft service hangar. The immense curved metal surfaces loom overhead; two distant anonymous technicians in neutral workshop clothing stand safely beside the aircraft for scale, small and secondary. Hard industrial light catches the joint cover and structural seams, with deep shadow under the wing. Use only external features visible in the supplied Tu-160 photo; do not expose hidden construction or invent load-bearing parts. The visual point is the huge scale of the joint, not a specific recorded repair event. No markings, text, logos, tools touching aircraft, dangerous action or weapons. Keep the visible joint in full frame.

The first output contained a small red circular detail on the skin, so it was replaced. Exact edit prompt for v02:

> Edit this exact image. Remove the small red circular detail on the aircraft skin near the upper center, replacing it with matching natural white painted metal. Preserve the hangar, aircraft geometry, lighting, technicians and composition exactly. Add no markings or text.

- Supplied reference: Kubinka Tu-160 photo, exterior form only; no internal structure revealed.
- Output v02: 1672×941 PNG; SHA-256 `82e8dd660794fb7e0cb90ea1f74ca5678f9307f5fbafc3cfc132bbf15e73cb8a`.

## Scene 047 — `scene_047_v02.png`

Initial v01 exact prompt:

> Nuviko History documentary scene 047, photorealistic reconstruction, 16:9. From ground level beneath a white Tu-160, look upward past the heavy main landing-gear group into the fuselage belly. Show two matching main bogies beneath the aircraft, each with four large wheels in a tandem arrangement, firmly grounded on concrete; the huge body looms above them. Use cold industrial daylight and a strong sense of mass, full gear support points visible with enough context to understand their relation to the fuselage. Actual photographs anchor Tu-160 exterior gear placement and nose gear form; the prior closeup composition is only a framing guide. Do not add markings, invented hardware, labels, text, weapons, people or damage. Reconstruction, not archival footage.

v01 placed large wheels on the lower caption band. Exact v02 prompt:

> Generate a wider revision of Tu-160 landing-gear scene 047 for Nuviko History, 16:9 photorealistic reconstruction. Ground-level long-lens view from under the fuselage, with the complete left and right main gear groups supporting the large body above. Each main bogie has four tires in tandem; both full gear groups remain clear and accurate. Reduce their scale enough to keep all tires and struts in the middle 70 percent of the frame, with a clean strip of runway in the bottom 18 percent reserved for on-screen subtitles. The enormous fuselage still dominates overhead, communicating 275-tonne scale. Actual Tu-160 references anchor exterior gear placement and strut/wheel configuration; do not copy markings. Natural overcast light, no invented details, labels, numbers, text, damage, weapons, people or fire. Keep all wheels inside the frame; do not crop their contact with the ground.

- Supplied references: Kubinka landing view and MAKS forward gear photo. The latter shows nose gear only; main bogie configuration is retained as unresolved final-source comparison.
- Output v02: 1672×941 PNG; SHA-256 `eb6826ca2ed2844d92ebbdc0dc46467ba2c4eb7b3bd4f21dfefd031536d359cf`.

## Scene 048 — `scene_048_v01.png`

Exact prompt:

> Nuviko History explanatory scene 048, 16:9 ultraphotorealistic physical model, not a real aircraft cutaway. A clean side section of a very large variable-sweep wing root shows two broad adjoining wing structures meeting around a thick central pivot area, held within a robust frame. Emphasize the scale and the need for a strong load path under airflow; show layered metal plates and large structural surfaces without specifying a real hinge design, exact component count or dimensions. Sharp angled camera, directed cool industrial light, rich metal texture, dark background. The Tu-160 photograph anchors only the external location and silhouette of the wing root. This representation is conceptual, not an exact Tu-160 engineering drawing. No labels, text, bolts arranged as exact schematic, exposed gears, measurements, logos or people. Keep all major connections in frame.

- Supplied reference: Kubinka Tu-160 photo, exterior silhouette only.
- Output: 1672×941 PNG; SHA-256 `1c227b4f5b05aebb3ac9edadd5c8ea2b6638eb0122a967140f9165c293b842fe`.

## Scene 027 — `scene_027_v01.png`

Exact prompt:

> Use case: photorealistic historical reconstruction for a Nuviko History long documentary video, 16:9 landscape, high detail. Scene 027: a Soviet Tu-22M Backfire bomber standing on a broad late-Soviet airfield, low diagonal nose-quarter view, its distinctive long fuselage and variable-sweep wings clearly different from a Tu-160. Strong, low hard daylight, restrained documentary color, aircraft fills the frame with enough surrounding runway to show scale. The attached reference is for aircraft identity and exterior shape only; do not copy its museum display setting, framing, or its markings. Keep the aircraft historically plausible and unmarked: no invented numbers, text, emblems, weapons, explosions, people, or battle. This is a static explanatory reconstruction, not archival footage. Compose wide with full nose, wing tips and tail inside crop, with quiet negative space at top for subtitles. Ultra-photoreal live-action appearance, natural materials and optics.

- Supplied reference: `Research/VisualReferences/tu22m_schleiffert_2014.jpg`, SHA-256 `74e5e41665394f36261b20659f8467f554e7f3840ed5555c168ce47a85cc6e1d`; aircraft exterior identity only.
- Output: 1672×941 PNG; SHA-256 `40cb89c60dee08de1a95fff29aedf86f79eff47e2de9ec9c2c7bd7e6109c3c18`.
- Imagegen control values: no explicit size/quality controls available in the built-in tool call; actual size measured from returned file.

## Scene 032 — `scene_032_v01.png`

Exact prompt:

> Use case: photorealistic explanatory physical model for a Nuviko History documentary, 16:9 wide. Scene 032: on a dark industrial design table, a realistic scale model of a Soviet Tu-95 Bear bomber sits beside a visibly over-stretched, too-heavy enlarged mock-up that preserves the old bomber's basic layout but looks structurally awkward and impractical. The viewer should understand why simply scaling an existing aircraft up is not the same as designing a new long-range supersonic machine. Dramatic close low tabletop angle, precise believable model materials, hands of anonymous engineers only at frame edge, shallow warm workshop lighting. The supplied actual Bear-A photo anchors the old aircraft's silhouette and four propeller layout only; do not copy its photo framing. Keep the oversized mock-up visibly an explanatory what-if model, not a claimed real prototype; no labels, readable technical drawings, numbers, logos, weapons, or text. Photoreal live-action workshop, no 2D illustration. Compose with both models distinct and fully visible, clean negative space above for subtitles.

- Supplied reference: same Tu-95 public-domain source as scene 026; identity/model shape only.
- Output: 1672×941 PNG; SHA-256 `cf96e4075abe3ab08f4b4abae144fd7dae883df5939045d417e8c8379b2a7952`.
- Imagegen control values: no explicit size/quality controls available in the built-in tool call; actual size measured from returned file.

## Scene 033 — `scene_033_v01.png`

Exact prompt:

> Use case: photorealistic explanatory reconstruction for Nuviko History, 16:9 wide. Scene 033: a clean, unmarked scale model of a Tupolev Tu-160 rests centered on a dark engineering work surface, seen directly from above, its variable-sweep wings extended and full swept-wing outline clearly recognizable. A warm narrow work light traces the geometry; the aircraft shape is the single focal idea, with subtle real drafting materials at the edge but no readable documents or technical text. The supplied Tu-160 flight reference anchors only the recognizable aircraft proportions and defining silhouette; it is not an archival depiction. No people, text, numbers, emblems, weapons, diagrams, or invented markings. Photoreal physical scale model and real tabletop, no illustration or glowing graphics. Keep full outline inside frame with balanced negative space and subtitle-safe upper margin.

- Supplied reference: `Research/VisualReferences/tu160_inflight_sergey_lysenko_2013.jpg`, SHA-256 recorded in `VisualReferences/README.md`; identity/proportions only.
- Output: 1672×941 PNG; SHA-256 `0916c930640682e8b5c98b04962bb3c89312aea00b22fc23c1feb88fc9140535`.
- Imagegen control values: no explicit size/quality controls available in the built-in tool call; actual size measured from returned file.

## Scene 034 — `scene_034_v01.png`

Exact prompt:

> Use case: Nuviko History long-film scene, 16:9 wide photorealistic real-world environment with the channel's recurring illustrated traveler. Scene 034: at the edge of a realistic aircraft display, a 40–45-year-old male traveler leans toward the root of a large Tu-160 variable-sweep wing model and studies the hinge geometry. Medium waist-up at frame right, torso turned three-quarter left, gaze fixed on the wing joint, right hand raised beside the shoulder with open palm angled to echo the wing's sweep, left arm relaxed down with open fingers. His illustrated face, hair, body and ochre jacket must retain drawn dark contours and soft colored shading; the hangar, aircraft model and all materials remain ultra-photoreal live action with physically integrated lighting and contact shadows. The two traveler references define identity/costume and facial consistency only; do not copy their pose. The Tu-160 reference anchors the aircraft model silhouette. Dramatic diagonal top light, clear wing root as focal point. Protect both visible hands, the face and wing joint, leave upper-left subtitle-safe space. No added text, labels, logos or people.

- Supplied references: channel traveler turnaround `channels/nuviko_history/brand/References/traveler_turnaround_20261104.png` and emotion sheet `traveler_emotions_20261104.png` (hashes in channel visual profile); Tu-160 flight photo in `VisualReferences/README.md`. Character references define identity/render style only; aircraft photo defines exterior silhouette only.
- Output: 1672×941 PNG; SHA-256 `71f8a488580c9bf99d8a482c9e155d72ea93390f4355c816c662277bffe0b475`.
- Imagegen control values: no explicit size/quality controls available in the built-in tool call; actual size measured from returned file.


## Scene 049 — `scene_049_v01.png`

Exact prompt:

> Create one photorealistic 16:9 cinematic still for a serious historical aviation documentary, a clearly explanatory reconstruction rather than a photograph of a specific recorded event. In a vast Soviet-era aircraft factory hangar, show a massive titanium-alloy load-bearing structural component resting on a heavy industrial jig, its scale conveyed by the hangar trusses and distant workers. The object should read as a broad, thick, engineered aircraft structural assembly with complex curves and machined metal surfaces, but do not present a recognizable exact internal Tu-160 layout, do not label it, do not add text, numbers, logos, flags, roundels, weapons, or identifiable aircraft. Natural industrial lighting, muted steel and amber tones, crisp detail, grounded documentary realism, wide composition with the component as the subject and clean darker lower margin for subtitles. Avoid dramatic sparks, futuristic styling, diagrams, exploded views, unsupported technical detail, and all insignia.

- No supplied image reference; generated as a clearly conceptual production-space reconstruction.
- Output: 1672×941 PNG; SHA-256 `501f5fadd41807660a979fdee283724481532324dd8630030e3c35560ef7d129`.

## Scene 050 — `scene_050_v01.png`

Exact prompt:

> Photorealistic cinematic 16:9 historical documentary still, a clearly illustrative reconstruction of heavy aircraft manufacturing in a Soviet-era industrial workshop, late 1970s / early 1980s atmosphere without readable signs or identifiable people. A very large precision machine tool works on an anonymous thick aircraft-grade metal component; show the part held securely on a heavy machine table, with the massive enclosure, gantry, tool head, chips and practical task lighting conveying scale and difficulty. The component must not resemble a specific identifiable Tu-160 internal part, no exact technical drawing or unsupported process detail. No sparks, no dramatic danger, no text, labels, numbers, logos, flags, roundels, weapons, or visible aircraft. Documentary realism, warm workshop light, steel-grey palette, composition with the machine and component clear, leave a darker unobstructed lower strip for subtitles. This is an explanatory reconstruction, not an archival photograph.

- No supplied image reference; generated as a generic workshop reconstruction, not evidence of a particular documented operation.
- Output: 1672×941 PNG; SHA-256 `a8d127b4d91e4bbab5d46b12cfa4261ab5fd0fa6ccf6f397bd4e569d6609925b`.

## Scene 051 — `scene_051_v01.png`

Exact prompt:

> Photorealistic 16:9 still for a serious aviation-history documentary. On a dark, uncluttered engineering table in a modest Soviet-era design bureau, place two accurate scale models of the same Tu-160 strategic bomber side-by-side, viewed from a high three-quarter angle: the left model has wings fully extended; the right model has wings fully swept back. Both models should have matching proportions, size, twin engine nacelles on each side, pointed nose, white paint with no national markings and no text. Their full silhouettes and wing positions must be unmistakably comparable, with no overlap. Restrained practical desk lighting, documentary realism, no people, no arrows, no diagrams, no labels, no flags, no invented weapons, no logos. Wide composition and clear darker lower margin reserved for subtitles. Models are illustrative, not archival photographs.

- No supplied image reference; two models are explanatory.
- Output: 1672×941 PNG; SHA-256 `742342908f93b29ad238ae6d5fac3cf9d53e17fd9d56e387871c884c42b3c17d`.

## Scene 052 — `scene_052_v01.png`

Exact prompt:

> A 16:9 photorealistic explanatory close-up for a Nuviko History aviation documentary. On a dark engineering table, show a conceptual physical demonstration model of a variable-sweep wing's heavy pivot/load-bearing joint: a large circular steel pivot form connects two thick metal wing-root plates held by a robust support frame. View from a low oblique macro angle; let the round metal form and layered load path catch cool hard light while the surrounding workshop falls into deep shadow. This is an illustrative model, explicitly not an exact Tu-160 internal mechanism or a historical photograph. Do not show gears, actuators, exact bolt patterns, dimensions, labels, arrows, text, logos, flags, aircraft insignia, weapons, or people. Carefully composed, tactile metal, visually clear but no speculative precision. Leave bottom 18% relatively dark for subtitles.

- No supplied image reference; generated as a conceptual mechanical model, not an actual Tu-160 internal assembly.
- Output: 1672×941 PNG; SHA-256 `444243da99a062d19d7890d14f5e7d97b080ed4a32789a4f15240da504adb69b`.


## Scene 053 — `scene_053_v01.png`

Exact prompt:

> Make a 16:9 ultraphotoreal documentary composite for Nuviko History. Use the two traveler reference images only to reproduce the exact recurring character as a clearly drawn 2D figure (same face, hair, clothes, proportions and line style), standing at the far right in half figure, in profile and leaning very slightly back as if taking in a large object. The traveler looks left toward the engine, right palm open toward it, left hand resting at the waist with relaxed slightly curled fingers. Use the NK-32 reference solely for the real external shape and cutaway form of one museum-display turbofan, placed large on a sturdy neutral demonstration stand in a dark modern aviation museum. The person remains unmistakably flat 2D illustration; engine and room remain photographic. Hard side light draws out metallic layers of the engine. Keep face and extended hand comfortably inside frame; leave a dark lower subtitle band. No labels, captions, logos, flags, extra people, flames, or aircraft markings.

- Supplied: accepted traveler turnaround and emotion sheet; NK-32 cutaway photo listed in `VisualReferences/README.md`. Roles: character identity/shape, and engine construction respectively.
- Output: 1672×941 PNG; SHA-256 `ee4b4c11b22373b31f6a6c55dc610103b5b5892a399bc65ecf4900110f7afb5d`.

## Scene 054 — `scene_054_v01.png`

Exact prompt:

> Create a photorealistic 16:9 aviation-history documentary still. In a restrained, large aircraft museum hangar, arrange four separate NK-32 turbofan engine units in two rows on sturdy low display stands. Each engine is clearly its own complete unit, and all four can be counted at a glance; use the supplied photograph only to anchor the real external and cutaway construction of an NK-32, without copying its exact museum framing or visible labels. Keep plausible scale, no Tu-160 aircraft in frame. Cool museum lighting with crisp metal detail, wide composition, lower 18 percent relatively dark and unobstructed for subtitles. No text, numbers, plaques, labels, logos, flags, people, flames, exhaust, weapons or diagrams. A clear explanatory museum display, not archival footage.

- Supplied: NK-32 cutaway photo in `VisualReferences/README.md`, used for engine form only.
- Output: 1672×941 PNG; SHA-256 `bb176eb619965584b3563eb0894590609c01deb36b888cf01b817ea66bbc92bb`.


## Scene 055 — `scene_055_v01.png`

Exact prompt:

> Photorealistic 16:9 cinematic documentary reconstruction, close rear-side view of one full-scale turbofan exhaust nozzle on an outdoor test stand at dusk, afterburner lit. The circular nozzle rim remains fully visible and sharp; beyond it, a long bright but controlled blue-white and amber hot plume streams straight behind into dark open test range, with heat distortion and subdued cool shadows on the surrounding metal. Use the supplied NK-32 image only to guide engine family appearance; do not pretend this is a documented historical Tu-160 engine test. Realistic materials and optics, grounded aviation documentary, no dramatic explosion, no fireball, no text, gauges, numbers, flags, emblems, aircraft, people or weapons. Leave a dark bottom strip for subtitles.

- Supplied: NK-32 cutaway in `VisualReferences/README.md`, engine family only.
- Output: 1672×941 PNG; SHA-256 `e7a31f052af0a14202568c9a1e2cd3307becf0e31d5a8e3d1d7f87fecf44110f`.

## Scene 056 — `scene_056_v01.png`

Exact prompt:

> Photorealistic 16:9 aviation-history documentary reconstruction of an unmarked white Tu-160 strategic bomber viewed low and directly from behind, centered and symmetrical on a quiet runway at blue-hour dusk. Show the complete rear fuselage and all four separate engine exhaust nozzles, clearly arranged as two close pairs beneath the wing roots; preserve correct aircraft silhouette and proportions from supplied external references, use them only for exterior aircraft identity and never copy their markings or framing. No afterburner flames. Cool metal edge light, subtle runway reflections, aircraft fully within frame, modest dark lower strip for subtitles. No text, numbers, flags, roundels, logos, weapons, smoke, people, damage or dramatic action. This is a clean explanatory reconstruction, not archival footage.

- Supplied: Tu-160 Kubinka landing and in-flight photographs listed in `VisualReferences/README.md`, exterior shape only.
- Output: 1672×941 PNG; SHA-256 `1315a3fdd6e7a13d3ecaf270abdfd81227e7fb218aae6724cf849a7f7f80c492`.

## Scene 057 — `scene_057_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction of a white Tu-160 in flight, viewed from below and slightly behind at a three-quarter angle. Show all four engine nacelles in two close pairs beneath the wing center, their intakes and outer shape clearly visible, and enough fuselage context to understand where the paired nacelles sit. The variable-sweep wings are in an intermediate/broad configuration. Use the supplied photograph only as an exterior silhouette and underside feature anchor; do not copy its markings or exact pose. Natural daylight above broken clouds, crisp but calm, aircraft fully inside the frame with dark cloud/open space at bottom for subtitles. No text, numbers, emblems, flags, weapons, contrails, battle, or extra aircraft. Clearly a reconstruction, not archival footage.

- Supplied: Tu-160 flight photo in `VisualReferences/README.md`, visible exterior and underside only.
- Output: 1672×941 PNG; SHA-256 `671604b0d2cd86d64976a60f6116fefbdde99891c617752bd1221dcaefe624d4`.

## Scene 058 — `scene_058_v01.png`

Exact prompt:

> Photorealistic 16:9 high-altitude documentary reconstruction of a white Tu-160 strategic bomber crossing a deep blue sky above a soft cloud layer, seen from a distant side profile, wings fully swept back. The aircraft is small enough within the wide frame to feel fast and high, but its complete unmistakable silhouette remains crisp: long pointed fuselage, swept wings, twin tail, four engine nacelles in two pairs. Use supplied photo only for the aircraft's true external silhouette and proportions; do not copy markings or pose. Natural cold upper-atmosphere light, restrained motion impression through cloud texture only, no streaks or contrails, no superheated effects, no text, numbers, emblems, flags, weapons, combat or other aircraft. Documentary reconstruction, not archival footage. Leave a calm darker area below for subtitles.

- Supplied: Tu-160 in-flight photo in `VisualReferences/README.md`, silhouette only.
- Output: 1672×941 PNG; SHA-256 `faf4fa8eda080a28effba2787af708648e7a5611ff200203178eaff4cccaa242`.


## Scene 059 — `scene_059_v03.png` (v01/v02 rejected)

Exact prompt for v01:

> Photorealistic 16:9 explanatory scale-model scene for an aviation-history documentary. On one flat, dark engineering table, place two realistic physical scale models at the exact same scale and nearly parallel on a common axis, viewed from directly overhead to avoid perspective distortion: a white Tu-160 and a dark gray B-1B Lancer. Both full silhouettes must be visible, with the Tu-160 clearly longer and broader, the nose directions aligned left-to-right, no overlap. The supplied Tu-160 and B-1B photos are identity and relative-shape references only; do not copy their backgrounds, lighting or aircraft markings. No labels, rulers, dimensions, flags, roundels, text, weapons, people or diagrams. Neutral even archival-study lighting, tangible model materials, clean dark lower margin for subtitles. They are comparative models, not a historical scene or side-by-side real aircraft.

- Supplied: Tu-160 exterior image and `b1b_inflight_commons.jpg`; identity and relative shape only.
- v01 was rejected: both models read too similarly and length difference was not clear. Output SHA-256 `f62add1cdc6818edfde5d1eb58f154972a07c10d4ed2df67947319f405caa0d4`.

Exact prompt for v02:

> Create a photorealistic 16:9 directly overhead comparison of TWO DISTINCT physical aircraft models on a neutral dark worktable, both pointing right and aligned on exactly the same scale. The upper model is a long white Tupolev Tu-160: very long slender fuselage, pointed nose, long swept variable wings, distinctive twin tail, four nacelles clustered beneath the wings. The lower model is a shorter dark gray Rockwell B-1B Lancer: visibly shorter fuselage and about 80 percent of the Tu-160's length at this same scale, broad blended wing-body planform, variable swept wings, smaller nose, four nacelles. Preserve these characteristic different silhouettes from the two supplied identity references. Both models must be separated by a wide gap, fully in frame, same nose direction, same physical scale; make the Tu-160 unmistakably longer by about one fifth. Clean tabletop only, no perspective distortion. Models are unmarked, no text, no rulers, numbers, flags, insignia, weapons or diagrams. Neutral studio/documentary light and a clean dark lower subtitle band. This is an explanatory side-by-side model comparison, not a co-located historical event.

- v02 was rejected because imagegen added explanatory lettering inside the frame. Output SHA-256 `bc6808810e8a5dfa0792a7918a0a16ff2d7559aa08c580eee0b1213c795144a4`.

Exact edit prompt for v03:

> Create a clean revision of this exact scene, preserving the aircraft's complete side-flight silhouette, angle, position, swept variable wings, scale, lighting and cloud background. Remove every marking from the aircraft: no red star, no text, no numbers, no colored stripes, no emblems or insignia anywhere. Keep a uniformly white and light-gray unmarked Tu-160. Do not add any new objects, labels, contrails, or visual effects. Keep the composition photorealistic and retain the clean lower cloud area for subtitles.

- The referenced-image text-removal prompt did not correspond to the actual v02 subject; v03 is retained only as a candidate pending the full contact sheet.
- v03 output: 1672×941 PNG; SHA-256 `9391aa9745e3f81ec0ec849bf7a6ff8f9d451daed7d6e39f9008652b40af9a31`.

## Scene 060 — `scene_060_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary composite in a quiet aviation museum. The exact recurring Nuviko traveler from the two reference images appears as a clearly drawn 2D figure, seated on a low bench at the left in a thoughtful pose: lean forward, right elbow on knee and right hand gently at chin, left palm on the opposite knee, head tilted and gaze raised toward the engine. Match the character's face, hair, clothes, proportions and line style faithfully; do not photorealize or alter the character. To the right, a single large NK-32 engine cutaway sits on a stand, with real external/cutaway appearance anchored by the supplied engine photo, no copied labels or framing. Engine and museum photographic, traveler unmistakably flat illustration. Medium side view, subdued warm practical light, composition gives character breathing room, lower dark strip for subtitles. No other people, text, plaques, logos, flags, aircraft markings, flames or weapons.

- Supplied: traveler turnaround and emotion sheet; NK-32 cutaway, roles limited to character and engine identity.
- Output: 1672×941 PNG; SHA-256 `f483fe244b711c3cd72578314bac80757e0e9dd3b08b70bc237b7308444de7e2`.

## Scene 061 — `scene_061_v01.png`

Exact prompt:

> Photorealistic 16:9 explanatory model for an aviation-history documentary, not a recorded historical event. On a dark workshop table, a short transparent demonstration section of a large aircraft fuel line with a few thick fittings runs from a simple unlabeled metal fuel reservoir toward a powerful turbofan engine in the background. Amber light catches a controlled stream of fuel-like liquid inside the clear section, communicating that high power consumes fuel quickly without showing any quantities, rates, instruments, diagrams or labels. Keep all connections visible and ordinary, no unsafe leaks or spills. Engine and model are illustrative, not an exact Tu-160 fuel-system layout. Documentary realism, cool metal and warm depth, lower 18 percent dark and clean for subtitles. No text, numbers, gauges, logos, flags, weapons, flames or people.

- No external image reference; generic conceptual demonstration, not an exact fuel-system layout.
- Output: 1672×941 PNG; SHA-256 `c81c36fc3f64250374f22f7d99563bb3d9952fd9a0320097155c4d266c760d98`.

## Scene 062 — `scene_062_v01.png`

Exact prompt:

> Photorealistic 16:9 overhead explanatory tabletop scene for an aviation-history documentary. On a plain, unlabeled physical relief map of the Northern Hemisphere, a small white Tu-160 scale model rests beside a simple transparent fuel-volume demonstration tank and a long curved, unmarked route thread that arcs across the map. The route represents distance only: no country names, borders, real bases, targets, arrows, symbols or numerical fuel calculation. Arrange objects so aircraft, route, and fuel reservoir are distinct and fully visible, showing that an all-supersonic journey would demand too much fuel without claiming an exact amount. Neutral workshop light, documentary realism, no text or labels; no military mission activity. This is a conceptual explanation, not an actual flight plan or historical scene. Keep bottom margin dark and free for subtitles.

- No external map reference; conceptual flight-distance model only.
- Output: 1672×941 PNG; SHA-256 `1ea2a1de402c22a419d23c25286491780d09f42e535428fbec74b50de081bf54`.

## Scene 063 — `scene_063_v02.png` (v01 rejected)

Exact prompt for v01:

> Photorealistic 16:9 historical documentary reconstruction of a Tu-160 cruising peacefully above a cloud sea in morning light, seen from a distant frontal-side angle with wings in a broad low-sweep configuration suited to long-distance cruise. Aircraft banks very gently with lots of open sky and cloud horizon ahead, complete silhouette visible and clearly readable. Use supplied photo only for true exterior silhouette and visible features; no copied markings. Soft warm dawn highlights, calm blue atmosphere, no streaks, flames, contrails, text, numbers, logos, flags, weapons, combat or other aircraft. Clearly a reconstruction, not archival footage. Preserve a clean dark cloud area at the bottom for subtitles.

- v01 was rejected because it added invented Russian markings, stripe, red star and tail number. Its SHA-256 was `3eeb516666defe9f309c538a11a117e196a2cf39938f7a497031f51cec95501e`.

Exact edit prompt for v02:

> Create a clean revision of this exact scene, preserving the aircraft's complete side-flight silhouette, angle, position, swept variable wings, scale, lighting and cloud background. Remove every marking from the aircraft: no red star, no text, no numbers, no colored stripes, no emblems or insignia anywhere. Keep a uniformly white and light-gray unmarked Tu-160. Do not add any new objects, labels, contrails, or visual effects. Keep the composition photorealistic and retain the clean lower cloud area for subtitles.

- Supplied: v01 image for composition edit and Tu-160 in-flight photo for exterior identity.
- v02 output: 1672×941 PNG; SHA-256 `765f4e571dd831a0848178767c32ebe6fe56d1ce6652423c52618ba4ac47229a`.

## Scene 064 — `scene_064_v01.png`

Exact prompt:

> Photorealistic 16:9 explanatory tabletop scene for an aviation-history documentary. Show two identical unmarked white Tu-160 physical scale models on one neutral work surface, same size and parallel axis, viewed from high directly overhead: left model has its variable-sweep wings fully extended for efficient cruise; right model has wings fully swept for faster flight. Make the two wing positions immediately distinct while the fuselage shape and scale match. Both aircraft fully visible with no overlap; actual Tu-160 reference anchors exterior silhouette and wing form only. No labels, text, numbers, arrows, flags, insignia, weapons, people, or diagram graphics. Natural neutral light, tidy dark table, clear lower subtitle-safe band. These are explanatory models, not a historical co-located scene.

- Supplied: Tu-160 exterior image in `VisualReferences/README.md`, silhouette and wing configuration only.
- Output: 1672×941 PNG; SHA-256 `df32ed0be00654cd1fbd20c6761eac5ec3578bfe43c3ac4966917351a722ba09`.


## Scene 065 — `scene_065_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction inside a vast aircraft hangar. Show an unmarked white Tu-160 bomber parked with all internal weapon bay doors closed, viewed from a low side-under angle along its smooth belly. The huge fuselage dominates while the two bay areas are only subtly legible as closed flush panel lines, not opened. Use supplied actual photo only for the aircraft's exterior silhouette and proportions, not its markings. Cool industrial daylight, wide quiet composition, clean darker lower area for subtitles. No missiles, no weapons, no people, no text, numbers, flags, emblems, logos, damage or dramatic action. This is an explanatory reconstruction, not archival footage.

- Supplied: Kubinka Tu-160 exterior photo, external shape only.
- Output: 1672×941 PNG; SHA-256 `ee9e511a71379c021c36f9db980926e3e05a956f2996642e943ffc57553dbf46`.

## Scene 066 — `scene_066_v01.png`

Exact prompt:

> Create a 16:9 photorealistic documentary composite in a quiet military aviation museum. Use both traveler references to render the exact recurring Nuviko character as a clearly flat 2D illustration on the right, quarter-turned left, gaze fixed on a static Kh-55 cruise missile displayed horizontally on a low museum stand. The traveler raises the right hand with an open palm toward the missile's nose; left hand relaxed near waist. Match face, hair, clothes, proportions and line style exactly; never make the person photographic. Use the supplied real Kh-55 photograph only to anchor the missile's exterior appearance and small folding wing/tail features; do not copy its markings or setting. Missile is inert display hardware with no launch context, no warhead view, no targets, no route or operational details. Photographic museum and missile; clearly drawn character. Strong clean composition, lower dark subtitle band. No text, labels, numbers, logos, flags, other people, weapons beyond the single static museum missile or dramatic action.

- Supplied: both traveler anchors and licensed Kh-55 photo; character identity and missile exterior only.
- Output: 1672×941 PNG; SHA-256 `2b5ab9de5bb9f363b1c2e33df470294bd6d3c114735a82c2a64b84f31eaed3f4`.

## Scene 067 — `scene_067_v01.png`

Exact prompt:

> Photorealistic 16:9 high-level historical documentary illustration of a Kh-55-type cruise missile as an inert explanatory object flying alone over a vast empty forest-and-mountain landscape in cold morning light. Show a clear side three-quarter silhouette at a safe distance, wings unfolded, no visible exhaust flame or payload detail. Use the supplied museum/display photo only for the missile's external shape; do not copy markings. The landscape is uninhabited, with no roads, settlements, borders, targets or military sites. This is a symbolic explanatory reconstruction of autonomous flight, not footage of a real operation. No explosion, impact, damage, people, text, labels, route graphics, flags, insignia or additional weapons.

- Supplied: Kh-55 photo, exterior shape only.
- Output: 1672×941 PNG; SHA-256 `f7f872a276594140ae4fd2b45d6eb504c5068347ea736c787f50df58c75fd8c4`.

## Scene 068 — `scene_068_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary explanatory still, close three-quarter side view of a museum-displayed Kh-55 cruise missile on a simple support stand, framed from nose to folded wing section with enough length visible to understand its narrow cylindrical body and compact proportions. Use the supplied real Kh-55 photo only for exterior shape and details; no copied markings, labels or display context. Inert static museum object, neutral dark background, cool directed light on the nose and body, clean cinematic composition with subtle depth. Do not expose or invent internal components, warhead, navigation hardware or mechanisms. No text, numbers, arrows, flags, logos, people, target, launch scene, damage or additional weapons. Lower strip dark and clear for subtitles; this is a technical display reconstruction, not archival footage.

- Supplied: licensed Kh-55 photo, exterior shape only.
- Output: 1672×941 PNG; SHA-256 `ae1023efc7453793105a0f01832cee25f245cd88ed8a2be686c20a7c20f0d2f4`.

## Scene 069 — `scene_069_v01.png`

Exact prompt:

> Photorealistic 16:9 high-level museum display for an aviation-history documentary. A single inert Kh-55 cruise missile exterior model lies horizontally on a neutral stand in a quiet museum, its smooth closed body intact and no internal structure exposed. On a separate small plinth nearby, place a generic unmarked navigation instrument box as an illustrative visual cue, not connected or arranged as a technical diagram. Use the supplied photograph only to anchor the missile's outer shape and small wings; no copied markings. Do not show, depict or imply the contents of a warhead, any nuclear material, fuze, wiring, route programming, guidance mechanism or exact internal arrangement. Restrained cool light, serious documentary tone, dark clean lower subtitle band. No text, numbers, labels, arrows, logos, flags, people, targets, launch or combat. This is a nontechnical museum explanation, not a working weapon or historical event.

- Supplied: licensed Kh-55 photo, exterior only.
- Output: 1672×941 PNG; SHA-256 `bfeffc0eb05aa383e7e3cde9c20502372bf4ebe87a7f717c6d077e685a76c526`.

## Scene 070 — `scene_070_v01.png`

Exact prompt:

> Photorealistic 16:9 high-level museum teaching display, an unarmed training bomb silhouette and a static Kh-55 cruise missile model rest separately on a dark table beside a plain unlabeled curved route map. Composition reads as a conceptual contrast between a freely falling object and a self-propelled missile traveling along a path, with no motion or operation shown. Use the supplied photo only as the cruise missile's exterior shape reference; no copied markings. Do not show release, launch, impact, targets, warhead, internal parts or technical instructions. The route map is abstract and has no borders, names, coordinates or destinations. Quiet documentary museum lighting, all objects fully visible, clean lower band for subtitles. No text, labels, arrows, numbers, flags, logos, people, damage or explosions. Educational conceptual display, not a real mission scene.

- Supplied: licensed Kh-55 photo, exterior only.
- Output: 1672×941 PNG; SHA-256 `3131e9018ffab401f20b429a761db9e230ea8dcc3a709553e3d879ca41cc2e80`.

## Scene 071 — `scene_071_v01.png`

Exact prompt:

> Photorealistic 16:9 explanatory physical model of the lower fuselage of a Tu-160 bomber, viewed from a high side-under angle in a dark industrial museum. Show a clean cutaway of the aircraft belly with TWO large separate internal bays arranged in sequence one behind the other along the fuselage. Both bays are empty, closed-looking rectangular cavities, clearly separated by structural space; do not show rotary launchers, missiles, weapons, payloads or mechanisms. Use the supplied aircraft photo only to anchor exterior fuselage proportions and underside silhouette. The cutaway is a simplified conceptual model, not an exact engineering drawing; avoid unsupported geometry, labels, measurement, text, logos or markings. Cool industrial light, full front and rear bay boundaries visible, clean lower strip for subtitles.

- Supplied: Kubinka Tu-160 photo, exterior form only.
- Output: 1672×941 PNG; SHA-256 `da563fa58cff5916f60c1036fc7e417a8ab9941811c7fd59a59d8d8fba3a03ef`.

## Scene 072 — no image (generation blocked)

The image generator rejected the requested static six-missile rotary-carrier explanatory model under its violence safety review. Do not retry or route around this block. Required next step: find a rights-cleared authentic source image of a Tu-160 rotary launcher or revise the visual plan in a permitted review; candidate image is intentionally absent.


## Scene 074 — `scene_074_v02.png` (v01 rejected)

Exact prompt for v01:

> Photorealistic documentary composite in a spacious modern aviation museum hangar. Under the smooth belly of a white Tu-160 display aircraft, the exact Nuviko traveler from the two references appears as a clearly drawn 2D figure, crouched at frame left in three-quarter view, looking upward toward the fuselage. Match face, hair, clothes and line style. Right index finger points up; left hand rests naturally on the traveler's own knee. The aircraft and hangar remain photographic; the traveler remains flat 2D. Use supplied Tu-160 photo only for exterior underside silhouette, no markings copied. Low camera, soft cool hangar daylight, large clean area around the pointing gesture, dark lower subtitle band. No weapons or open bays, no text, labels, logos, flags, extra people or dramatic effects.

- Supplied: channel traveler turnaround/emotion refs and Kubinka Tu-160 exterior photo.
- v01 rejected because generator opened the aircraft bays despite the prompt; rejected PNG SHA-256 `adadbd1a1adc5a17e288538e353bd52ce1f7c61bcda4193832190f81024dfab7`.

Exact edit prompt for v02:

> Revise this museum scene while preserving the exact framing, aircraft, drawn traveler, gesture, hangar and lighting. Change only the two large dark rectangular openings under the belly: replace each opening with smooth closed flush white/gray exterior bay doors that follow the fuselage skin, with subtle panel seams only. Nothing inside the aircraft is visible; no open cavities, no missiles, no stores, no weapons. Keep the traveler pointing up and keep the whole figure and aircraft silhouette. Do not add text, markings, logos, flags, or other objects. Maintain the lower subtitle band.

- v02 output: 1672×941 PNG; SHA-256 `cdd67d0701455382a14b3b43fe16b303d364566d9901ed517e99622180bc15e7`.

## Scene 075 — `scene_075_v01.png`

Exact prompt:

> Photorealistic 16:9 explanatory wind-tunnel demonstration, not a Tu-160 historical test. A clean white delta-like bomber-wing model is mounted inside a dark wind tunnel; beneath one wing is a single small smooth unmarked cylindrical dummy store, clearly a generic demonstration object and not a real Tu-160 configuration. Fine visible smoke filaments bend around the protruding shape and continue downstream to suggest added drag, with no arrows, graphics, numbers or measurements. Keep the store visually secondary to the airflow and wing. Cool technical light, realistic physical apparatus, clean lower band for subtitles. No missile fins, weapons markings, labels, text, logos, flags, people, explosions or launch.

- No exact-aircraft reference; generic aerodynamic illustration.
- Output: 1672×941 PNG; SHA-256 `428bdee5e9727c01c1f71bd50923f5bfc2807642f0cde6b0ffb6cbace666ec84`.

## Scene 076 — `scene_076_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction of an unmarked white Tu-160 in flight seen from a low front-under three-quarter angle, focusing on its smooth continuous underside and closed flush internal-bay doors. Preserve the true long fuselage, variable-sweep wing, twin tail and four nacelles using the supplied exterior image only as a shape anchor. No external stores or weapons. Bright cool daylight above a soft cloud layer, the fuselage contours fully inside frame and clear; calm sky and cloud at bottom for subtitles. No text, numbers, emblems, flags, flames, smoke, battle or extra aircraft. This is a reconstruction, not archival footage.

- Supplied: Tu-160 in-flight exterior photograph, shape only.
- Output: 1672×941 PNG; SHA-256 `0f5049c61a74358bbb1f5d4da39b1e8204b3a91742005e3dce38ecfa34889017`.

## Scene 078 — `scene_078_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction on a quiet aircraft apron beside a white Tu-160. Four anonymous aircrew members in plain, unmarked late-Soviet flight suits stand in a loose line near the large aircraft, seen at shoulder height with enough space between them for all four silhouettes to be counted. They are not portraits and have no identifiable faces, names, badges, insignia or weapons. The aircraft fills the background, its full nose and large fuselage helping convey the people-to-machine scale; use supplied exterior photo only for aircraft silhouette, no markings copied. Soft cold side light, restrained period atmosphere, clean dark lower area for subtitles. No action, no text, no flags, no logos, no extra crew, no dramatic gesture. Clearly a reconstruction, not archival footage.

- Supplied: Kubinka Tu-160 exterior photo, aircraft shape only.
- Output: 1672×941 PNG; SHA-256 `12a1fb32b362f09061c34e78ccb724d410be1bf4defa0265384030506371e985`.

## Scene 079 — `scene_079_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction of an unoccupied Tu-160 cockpit viewed from the rear through the center aisle toward the front, showing four distinct crew places across a wide cabin in a plausible forward-facing arrangement. Use the supplied real cockpit photo only to anchor the actual shape and style of visible front control panels, seats and cockpit windows; do not copy its camera angle, readable instrument settings or markings. Preserve a documentary 1980s atmosphere, subdued greenish instrument glow and practical overhead light. Keep all four seats countable, no people, no readable labels, screens, numbers or text. Do not invent recognizable secret controls or operational procedures; details remain general. No logos, flags or insignia. This is a careful interior reconstruction, not archival footage; leave lower edge clear for subtitles.

- Supplied: Tu-160 cockpit source photograph, cabin appearance only.
- Output: 1672×941 PNG; SHA-256 `afbc593b11c7ca37b27f4bd9e3e67957fe3250d0858f10d4eddc31c7e864da04`.

## Scene 080 — `scene_080_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary composite on a modern aircraft museum viewing platform in soft daylight. Place the nearly full Tu-160 aircraft on the left and center, large enough to show its whole nose, wings and tail; the exact Nuviko traveler from the two references stands in the foreground at right as a clearly flat 2D drawn figure. The traveler turns left toward the aircraft, left hand raised open at shoulder level, right arm extended low and forward to indicate the fuselage's length. Match the character's identity, clothing, proportions and line style exactly. Aircraft and platform photographic, traveler distinctly 2D. Use supplied aircraft photo for external shape only and do not copy markings. Pull-back perspective emphasizes how small one person is beside the machine. No other people, weapons, text, numbers, logos, flags, emblems, or dramatic effects. Keep both hands and full aircraft silhouette inside the frame; lower edge clear for subtitles.

- Supplied: accepted traveler references and Tu-160 exterior photograph.
- Output: 1672×941 PNG; SHA-256 `85f86368f11f9637e6a1d03bbd920bd8520872b5dc4931bb3d380f074af77691`.

## Scene 081 — `scene_081_v01.png`

Exact prompt:

> Photorealistic 16:9 explanatory museum cutaway model of a Tu-160 strategic bomber on a dark engineering table, seen from a high diagonal angle. Show a long aircraft fuselage section with a few broad, simplified, clearly separated conceptual zones: fuel volume as sealed translucent tanks, four engine nacelles externally visible, a robust wing-root section, and two empty internal bay cavities. This is a teaching model only, not an exact engineering drawing or internal layout. Do not add missiles, weapons, launchers, wiring, control systems, dimensions, labels, arrows or text. Use supplied aircraft photo only for exterior silhouette and proportions. Keep all aircraft and cutaway areas inside the frame; even technical studio light, realistic materials, clean lower subtitle band. Serious documentary visual, no people, insignia or flags.

- Supplied: Tu-160 exterior photo, outer silhouette only.
- Output: 1672×941 PNG; SHA-256 `af471aafb5857153b838e750b04489169defb490a47ac3f818b7e51ac55b9722`.

## Scene 086 — `scene_086_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction at a large cold-weather airfield in the late Soviet period. A white Tu-160 is parked on the apron in a wide low view along the fuselage; in the midground a maintenance vehicle and a small unmarked ground-support trolley are parked beside it, and deeper in frame a plain communications/workshop building with a single lit window suggests infrastructure. Two or three anonymous ground technicians in plain coats remain small secondary figures. Use supplied photo only for aircraft exterior form and proportions, no copied markings. Natural gray morning, wet concrete reflections, quiet operational readiness without a specific alert or event. No text, numbers, flags, insignia, weapons, missile vehicles, combat or dramatic action. Keep nose, wing and ground support visible; lower dark strip safe for subtitles. Clearly a reconstruction, not archive.

- Supplied: Tu-160 exterior photo, aircraft silhouette only.
- Output: 1672×941 PNG; SHA-256 `d9754d8352fd14e178a8fae6b38bf39869d0cda0e6cd9c5dae9f5b2b0b829e95`.

## Scene 088 — `scene_088_v01.png` (rejected)

Exact prompt:

> Photorealistic 16:9 documentary composite in a quiet modern archive room. On the left, the exact Nuviko traveler from the two references appears as a medium 2D illustration, body turned right, eyes on a large framed photograph of a Tu-160 in flight mounted on the wall. The traveler points toward the aircraft with the right index finger; left arm rests behind the back and stays hidden. Match the character's face, hair, clothes and line style faithfully; person is drawn, room and framed photograph photographic. Use the supplied actual Tu-160 flight photo as the content of the framed photograph, preserving its recognizable real aircraft image while cropping out no essential part; keep the image plane straight and clear. No copied extra markings beyond those already present in the supplied archival photograph. Soft side light, dark lower subtitle band, no added text, labels, logos, flags or extra people. The photograph is a real 2013 flight image shown in an archive setting, not a claim that the image depicts the 1980s.

- Supplied: both accepted traveler anchors and CC BY-SA 4.0 2013 Tu-160 flight photo.
- Rejected: imagegen altered the recognizable actual photo with invented Russian words, a made-up name and markings; output was moved to the workspace trash. Do not use it as a scene. The license and source remain documented in `VisualReferences/README.md`.

## Scene 089 — `scene_089_v01.png`

Exact prompt:

> Photorealistic 16:9 historical reconstruction of an early Tu-160 prototype inside a vast Soviet-era assembly or flight-test hangar around the early 1980s. Show the complete unmarked white strategic bomber from a high three-quarter angle with wings in a broad low-sweep position, surrounded by the deep perspective of the hangar. Use the supplied Tu-160 photo only for the basic external silhouette and proportions; do not copy markings or imply this is a known specific prototype number. Aircraft is assembled and intact, with no invented test outcome, no crew or weapons. Cold natural light from large hangar doors, documentary grain and restrained color, full nose, wingtips and tail inside frame. No text, labels, numbers, logos, flags, roundels, cranes crossing the aircraft or dramatic effects. Explicitly a reconstruction, not archival footage.

- Supplied: Tu-160 exterior photo, silhouette only.
- Output: 1672×941 PNG; SHA-256 `aad7c406d08f7478c33e5ef4aa0be361eed4136b606f616375425dc42fe141b2`.

## Scene 090 — no image (generation blocked)

Imagegen rejected the generic ground-component test-hangar reconstruction under its violence safety review. Do not retry or rephrase around the block. Candidate remains absent; use a separately rights-cleared source if one is found.

## Scene 091 — `scene_091_v01.png`

Exact prompt:

> Create a photorealistic 16:9 documentary reconstruction of this unmarked early Tu-160 prototype now standing intact on a quiet flight-test runway in winter daylight, viewed very low from the front with broad horizon and full wing visible. Preserve its external silhouette and unmarked white surface from the supplied reconstruction. The aircraft is stationary and ready for a test flight; no takeoff, no crew, no weapons, no vehicles, no smoke, no activity. Restrained cold early-1980s atmosphere, natural light, credible film grain, full nose and wings within frame, darker runway band below for subtitles. No text, numbers, emblems, flags, logos or other aircraft. This is a reconstruction and makes no claim to show the exact first-flight date.

- Supplied: scene 089 reconstruction, composition/identity only.
- Output: 1672×941 PNG; SHA-256 `522ad99744a9f46d7f3f9592ae1c7ee0439e0a90f23237034412344779ed0e59`.


## Scene 083 — `scene_083_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary composite on a dark neutral map-study table. At the far left stands the exact Nuviko traveler from the two references, full-height as a clearly flat 2D illustration, nearly frontal and looking at the viewer. The traveler's right hand is open in a calm negating gesture; left hand points down toward a single small white Tu-160 scale model on the table. Behind them, a broad, unmarked physical globe/map surface fills the frame to show strategic scale, but contains no borders, names, bases, targets or installations. Use aircraft photo only for the model's exterior shape; no copied markings. Keep the single aircraft small against the wide map, making clear it is one component rather than an entire national system. No weapons, text, labels, flags, logos, extra aircraft or dramatic effects. Serious documentary lighting, enough room around both hands and the model, lower subtitle-safe margin.

- Supplied: accepted traveler turn-around/emotion references and Tu-160 exterior photo.
- Output: 1672×941 PNG; SHA-256 `897d31887ad5d0250297d3382297348375cb9f0e5d27f6c0ad65b76845bb9849`.


## Scene 093 — `scene_093_v01.png`

Exact prompt:

> Photorealistic 16:9 careful reconstruction inside a Tu-160 cockpit during an early flight test. View from behind the pilot over one shoulder: a single anonymous test pilot in a plain period flight helmet and suit faces forward toward the instrument panel and windscreen; only back of head and shoulders are visible, with no identifiable face, name or insignia. Use the supplied authentic cockpit photograph only for the general panel, window and seat appearance; no copied readable indicators or markings. Restrained 1980s film tone, soft daylight through the cockpit glazing, instrument lights subdued, no dramatic maneuvers. No visible weapons, text, numbers, logos, flags or extra crew. Clearly a reconstruction, not an archival portrait; lower edge kept free for subtitles.

- Supplied: authentic Tu-160 cockpit reference, general appearance only.
- Output: 1672×941 PNG; SHA-256 `080e0f45347b85ce91e23ef60796817a97f8c11a934101fe2e025271cd98ed9c`.

## Scene 094 — `scene_094_v01.png`

Exact prompt:

> Photorealistic 16:9 historical documentary reconstruction of an unmarked early Tu-160 prototype in flight above a broad neutral landscape, viewed from a distant upper-side angle in clear daylight. Full aircraft silhouette visible against earth and sky, no dramatic maneuver or claimed test result. Use the supplied image only for aircraft exterior silhouette and proportions, not markings or exact composition. Restrained period film grain, natural color, aircraft appears as the sole subject. No text, numbers, logos, flags, weapons, contrails, battle, or other aircraft. Clearly a reconstruction, not archival footage. Keep a calm darker area near the bottom for subtitles.

- Supplied: Tu-160 flight image, external silhouette only.
- Output: 1672×941 PNG; SHA-256 `fd230bc0d24183269867a5f1d7173de6f27830dbe6f140d6ecb070a22d9755f7`.

## Scene 095 — `scene_095_v01.png`

Exact prompt:

> Photorealistic 16:9 historical reconstruction of a Soviet-era flight-test workspace around the early 1980s. Camera inside a modest technical room: foreground is a clean analog instrument desk with a few unlabelled dials and paper-free panels; through a large window, a Tu-160 test aircraft sits in soft focus on the airfield. Keep instruments generic and unreadable, with no invented data or specific test results. Use the supplied actual cockpit photo only as a general period reference for analog panel styling, not as a technical layout. Cool daylight, quiet investigative atmosphere, restrained film texture. No people, text, numbers, logos, flags, weapons or dramatic action. This is a generic reconstruction, not a documented specific test room or archival scene. Leave bottom edge clear for subtitles.

- Supplied: cockpit reference, broad period panel style only.
- Output: 1672×941 PNG; SHA-256 `369ed94e332b9fe9e8c66b875e5bc5fc023d0824d9111473148fb35c957ad5c8`.

## Scene 097 — `scene_097_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction in a large Soviet aircraft factory shop in the early 1980s. From workpiece height, look along the length of a massive unpainted aircraft-grade metal panel assembly secured on a heavy industrial cradle; the panel's size and complex curved edges dominate, while machine tools and two distant workers provide scale. No identifiable exact Tu-160 internal part or undocumented operation is implied; this is a generic large-component manufacturing reconstruction. Practical industrial lights, natural steel and warm amber tones, period workshop atmosphere. No sparks, labels, readable signs, logos, flags, text, numbers, aircraft weapons or drama. Keep the full component in view and a darker lower strip clear for subtitles.

- No external reference; generic production reconstruction.
- Output: 1672×941 PNG; SHA-256 `8215ce6155c6ff479d6b0635a732750517cceda154eefd7494d26a3648bd1267`.

## Scene 098 — `scene_098_v01.png`

Exact prompt:

> Photorealistic 16:9 very wide high-angle view from an industrial gallery into a huge Soviet-era aircraft assembly shop in the early 1980s. A large unpainted bomber airframe sits centrally in a long work bay while separate teams work in distinct distant zones on broad wing panels and fuselage sections; cranes, platforms and overhead lights convey scale and coordinated assembly. Do not show a recognizable exact internal layout, logos, signs or fictional supplier names. No sparks or dramatic action. Keep the entire assembly hall context and main airframe visible. Period documentary realism, even cool industrial lighting, restrained film grain, clean lower margin for subtitles. This is a generic reconstruction of large-aircraft production, not a verified photograph of the Kazan plant and not a claim about a particular recorded shop.

- No external reference; generic production reconstruction, not identified as Kazan.
- Output: 1672×941 PNG; SHA-256 `336f9a8f7414be16c16a06083b577f88e6c6bf99c5e258e448e77a7635d7e312`.

## Scene 100 — `scene_100_v01.png`

Exact prompt:

> Photorealistic 16:9 historical reconstruction of an early white Tu-160 parked at a Soviet long-range aviation airfield in the late 1980s, suggesting the aircraft entering service. Show a calm low side angle along the full fuselage and wide concrete apron; modest period buildings far in the background, no ceremony, no named base, no specific arrival event. Use supplied exterior image only to anchor the aircraft silhouette and landing gear; do not copy modern display setting or aircraft markings. Overcast daylight, restrained documentary colors, no people close to camera, no weapons, no text, numbers, flags, emblems, smoke or action. Clearly a reconstruction, not archival footage. Preserve nose, wings and tail fully inside frame, lower area clean for subtitles.

- Supplied: Kubinka Tu-160 exterior image, shape/gear only.
- Output: 1672×941 PNG; SHA-256 `d8af1d07b33aa603fa835ffc0981fedbaedd4eceaf0acced6ee2f8b085e90d20`.

## Scene 102 — `scene_102_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction close three-quarter front view of an unmarked white Tu-160 nose against an open blue sky. Elegant white skin and long pointed nose dominate; cockpit windows are visible but undistorted, clean highlights glide along the curved surface, with one wing root softly entering frame to imply the full aircraft. Use supplied Tu-160 photo only for true nose and cockpit exterior shape, not markings or exact framing. Calm daylight, restrained natural color, no text, flags, numbers, emblems, weapons, smoke, other aircraft or people. Clearly a reconstruction, not archival footage. Keep nose contour completely inside crop and a dark sky strip below for subtitles.

- Supplied: Tu-160 flight photo, nose/cockpit silhouette only.
- Output: 1672×941 PNG; SHA-256 `ee03dde608b97ec7c691bbe5e754b3942df570f932780fbaef38483b65281367`.

## Scene 103 — `scene_103_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction of a clean unmarked white Tu-160 in a front-side three-quarter view above a neutral cloud layer, camera moderately high and long-lens to keep the pointed nose undistorted. Show the long white fuselage, nose, swept wing, twin tail and four engine nacelles in one coherent recognizable silhouette. Soft side daylight glides along the skin, natural blue-gray air and calm clouds. Use supplied photo only for exact outside proportions and visible aircraft geometry; no copied markings. No text, numbers, flags, insignia, weapons, contrails, battle, or other aircraft. Full aircraft fits comfortably within frame; lower cloud band clean for subtitles. This is a reconstruction, not archival footage.

- Supplied: Tu-160 flight photo, external geometry only.
- Output: 1672×941 PNG; SHA-256 `5934ae36080000254b270ce936e5202ffcd028f0d513cd0f360d8401321c81ea`.

## Scene 104 — `scene_104_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction, wide high front-quarter view of an unmarked white Tu-160 parked on a quiet runway with wings fully extended in the broad forward-swept-out configuration. Show the full nose, both complete wing tips, tail, and strong wing shadow on the concrete to emphasize the ground span. Use supplied exterior reference only for aircraft silhouette and extended-wing geometry; no copied markings. Soft daylight, calm open airfield, no people, no weapons, no text, logos, flags, numbers or dramatic effects. Composition preserves full aircraft inside the frame with quiet darker runway band for subtitles. Clearly a reconstruction, not archival footage.

- Supplied: Kubinka Tu-160 exterior reference, silhouette and wing state only.
- Output: 1672×941 PNG; SHA-256 `a63b30bd6af951878aa46ba0c2cd738458296e4ee539294d8c80d8d372bd3886`.

## Scene 105 — v01 rejected; reuse 045 candidate considered

The newly generated v01 presented a distorted aircraft tail with two vertical fins, so it was rejected and moved to the workspace trash (SHA-256 `cf1502bbaedcb17223b5a35ec6711ca0c451ea443e901b05e14af21d4a285ea5`). Existing scene 045 is a closer match for the storyboard's fully swept Tu-160 flight silhouette and may be reused as a mapped plan image after full-sequence review.


## Scene 107 — `scene_107_v01.png`

Exact prompt:

> Photorealistic 16:9 explanatory documentary still: an unmarked Tu-160 stands alone on a vast empty concrete apron just after the Cold War, viewed wide from the side with the whole aircraft small against generous negative space. Low cold overcast light, quiet stillness, no people, no other planes, no weapons, no national symbols, no text or identifiable airbase. Use supplied photo only for external aircraft silhouette; no copied markings. The image should carry a pause and historical uncertainty without implying abandonment or damage. Calm cold gray palette, full aircraft inside frame, lower dark runway band for subtitles. A present-day reconstruction, not archival footage.

- Supplied: Kubinka Tu-160 exterior reference, shape only.
- Output: 1672×941 PNG; SHA-256 `cc3b8f3e68ca4733038ae04c0543cf5366c32846aec32a5f13f227fd5a9e3769`.

## Scene 109 — `scene_109_v01.png`

Exact prompt:

> Photorealistic 16:9 overhead tabletop explanatory model on a physical map centered on Eastern Europe, showing the recognizable outlines of Ukraine and Russia with a thin neutral border and no names or labels. Place two small identical white Tu-160 scale models: one over Ukraine, one far to the east over Russia, clearly in different territories and not at named airbases. Use simple subdued blue-gray land colors and natural paper-map texture, no flags, bases, routes, arrows, numbers or military symbols. The map is conceptual and only explains that aircraft were located in two newly independent countries; it does not show exact deployment or quantities. Documentary museum lighting, models fully visible, clean lower subtitle band. No text or invented words.

- No external map reference; conceptual location illustration only.
- Output: 1672×941 PNG; SHA-256 `47220d51d9ff636121eeef0fed37d9201da397b672675742cb21394b98368273`.

## Scene 111 — `scene_111_v01.png`

Exact prompt:

> Photorealistic 16:9 high-angle explanatory model, a physical unlabeled map of Eastern Europe and western Russia on a clean dark tabletop. Show the recognizable shape of Ukraine west of a much larger Russia. On the Russian side, arrange EXACTLY EIGHT small identical white Tu-160 scale models in two neat rows of four, each separated and fully visible for counting; show no models on the Ukraine side in this frame. This represents eight aircraft transferred to Russia, not a simultaneous flight or a route. Do not include arrows, lines, bases, flags, text, names, borders beyond a subtle national outline, numbers, weapons or combat details. The models are illustrative, no national markings. Neutral museum lighting, dark lower subtitle band, precise overhead view.

- No external map reference; exact eight-model count is the visual beat, no route implied.
- Output: 1672×941 PNG; SHA-256 `10aaeabe21e6e5a875895e8435607ca6325961ecc23a48fa027b066a1a717daf`.

## Scene 112 — `scene_112_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction of a quiet aircraft factory hangar in the early 1990s, after large-aircraft production had sharply slowed. Show a wide symmetrical industrial hall with unused heavy assembly jigs, empty platforms and a few incomplete metal fixtures under weak cold overhead light; no aircraft is present, and no signs or papers state that production ended entirely. The visual conveys lost momentum without implying a specific closure order or abandoned damage. No people, text, labels, logos, flags, weapons or dramatic ruin. Industrial documentary realism, dark negative space in the lower frame for subtitles.

- No specific plant reference; explanatory reconstruction of reduced activity, not a documented closure scene.
- Output: 1672×941 PNG; SHA-256 `56b974a0140b47cbf04b70477d82dfa5328c994ce9bad12e2b2acd081a040a82`.

## Scene 113 — `scene_113_v01.png`

Exact prompt:

> Photorealistic 16:9 present-day documentary reconstruction of a serviceable white Tu-160 at an active airfield in clear morning daylight. Medium-wide side view along the fuselage with the nose, wing, landing gear and tail visible; a plain modern hangar and distant apron activity suggest continued service without showing a specific sortie. Use supplied exterior photo only for aircraft shape, no copied markings. No weapons, people in foreground, text, numbers, flags, logos, emblems, smoke or dramatic action. Clean composition with natural cool light, lower dark runway band for subtitles. This is a reconstruction, not a photograph of a specific aircraft or event.

- Supplied: Kubinka Tu-160 exterior reference, silhouette only.
- Output: 1672×941 PNG; SHA-256 `d3167f07fd08a08f1d4021b565876c029e96e6f82d080c3e5641e925400a75d2`.

## Scene 114 — `scene_114_v01.png`

Exact prompt:

> Photorealistic 16:9 documentary reconstruction in a large modern aircraft factory hangar. In the foreground left, an existing white Tu-160 airframe is parked in a maintenance bay with a few unmarked service platforms beside it, suggesting modernization but no visible weapons or identifiable modification. Deeper in a separate work zone at right, new white fuselage and wing sections rest on clean assembly jigs, suggesting renewed production. Keep the zones visibly distinct; do not imply these exact aircraft or work happened simultaneously. Use supplied photo only for exterior Tu-160 silhouette. Neutral industrial light, realistic materials, no logos, flags, text, numbers, people close-up, weapons, technical schematics, or dramatic action. This is a conceptual reconstruction, not a photo of the Kazan plant or a verified event; leave a clean lower subtitle band.

- Supplied: Kubinka Tu-160 exterior reference, silhouette only.
- Output: 1672×941 PNG; SHA-256 `90bcc39a3aadaa9dd559580d2fcac0f7a2cd0741175f533d3cf242b49fb26cef`.

## Scene 119 — `scene_119_v01.png`

Exact prompt:

> Photorealistic 16:9 closing documentary reconstruction of a modern unmarked white Tu-160 in flight at calm natural late-afternoon light. Distant high three-quarter view with the nose pointing toward wide open space on the right, the whole aircraft silhouette centered slightly left and completely visible above a soft cloud sea. Its white fuselage, variable-sweep wings, four engines and twin tail remain recognizable; use reference only for exterior proportions, not markings. The mood is reflective and restrained, suggesting a long-lived machine beyond the country that created it. No weapons, contrails, text, numbers, flags, emblems, battle, or other aircraft. Natural blue and silver palette, no dramatic sunset glow. Reconstruction, not archival footage; preserve subtitle-safe dark cloud band below.

- Supplied: Tu-160 flight reference, exterior silhouette only.
- Output: 1672×941 PNG; SHA-256 `6d75a469930dd94ce10b5424c41f361de65b2f433fbf8e8b127663262cc9113c`.


## Scene 024 — `scene_024_v01.png`

Exact prompt:

> Nuviko History scene 024, documentary-quality photorealistic historical reconstruction, widescreen 16:9. At a remote United States air-defense radar station in the late 1970s, a large period-plausible white geodesic radome stands on a broad concrete base with a low service building and metal access structures. Frame from near ground level looking upward past the radome toward a cold dawn sky; a tiny distant interceptor silhouette is just visible far above, secondary and unarmed. The supplied historical U.S. Air Force AN/FPS-26 radar image anchors only the period radar technology and radome form; the new scene is a reconstruction and must not copy the source's interior composition. Serious, restrained documentary mood; sharp layered geometry, winter-blue ambient light with a thin amber horizon, realistic scale and optics. No text, logos, readable signs, flags, numbers, people, weapons, explosions or battle. Keep the full radome and horizon inside 16:9 with caption-safe space low in frame.

- Supplied reference: `Research/VisualReferences/an_fps26_radar_1950s_usaf.jpg`, radar technology/radome only; source page records a 1950s example, not a 1970s base.
- Output: 1672 × 941 PNG; SHA-256 `03d4faaa868adbb45cd5a92ea5acf291e17e84e50a5d5253fcc9d909ddafe916`.
- Imagegen controls: no explicit output-size/quality controls were available; actual dimensions measured from the file.

## Scene 025 — `scene_025_v01.png`

This is a corrected edit. The first generated version depicted a jet-powered bomber with a B-52-like engine arrangement and was rejected; it is preserved only in the rejected-image trash record.

Exact edit prompt:

> Edit the first referenced image, preserving its exact composition, camera, weather, light, radar structures, horizon, and framing. Replace only the distant aircraft in the upper right. The current jet-bomber shape is wrong. Make it an unmarked Soviet Tu-95 Bear long-range bomber, matching the supplied actual Tu-95 reference: four large turboprop nacelles along the wings with distinctive propeller disks, long swept wing, and tall tail. Keep it far away and small but clearly legible. Do not retain any underwing jet engines. No national markings, text, numbers, weapons, contrails, battle, or changes to the radar installation. This remains a photorealistic historical reconstruction, not an archival photograph.

- Supplied references: rejected v00 scene composition (edit target); `tu95_bear_a_flight_1977_dod_publicdomain.jpeg` (aircraft identity); radar reference only informs scene context.
- Output: 1672 × 941 PNG; SHA-256 `f1f9c6dc136b9c2f40a6fde65ef804ca49ae920057c37e4a2a99ff6527c03326`.
- Visual review: radar remains intact; aircraft has four propeller nacelles and no obvious jet pods. Candidate only; confirm silhouette legibility in the full sequence and motion-safe crop.
- Imagegen controls: no explicit output-size/quality controls were available; actual dimensions measured from the file.


## Scene 029 — `scene_029_v01.png`

Initial output v00 contained invented blue/gold aircraft striping and was rejected; moved to `/Users/diplomat/.Trash/040_tu160_rejected_images/scene_029_v00_invented_markings.png`. The following exact edit produced v01.

Initial exact prompt:

> Create Nuviko History scene 029, a 16:9 cinematic photorealistic museum-display scene with one deliberately illustrated recurring traveler. Composite rendering boundary: the man is a 2D illustrated traveler matching both supplied character reference sheets, with visible drawn ink contours and soft colored shading on face, curly brown hair with gray at temples, mustard hooded jacket, cream shirt, dark backpack and brown trousers; the display room, models and lighting are photorealistic. He stands full height on the RIGHT side, stepping toward the LEFT, looking at a white Tu-160 scale model beside a separate slim Kh-55 cruise-missile scale model on a neutral display platform. His RIGHT arm extends in a clear guiding gesture along the missile's direction; his LEFT hand holds his backpack strap. Keep the exact plane and missile forms anchored to the supplied aircraft and Kh-55 references; they are static inert display models, not armed or operational. Daylight side light, expressive grounded museum perspective, models separated and fully visible, lower caption-safe band. No text, labels, flags, numbers, insignia, launchers, actual weapons, warhead detail, firing, threat, explosion, or battle.

Exact edit prompt:

> Edit the exact first referenced image. Preserve the composition, camera, photorealistic museum room, lighting, traveler pose and identity, aircraft/missile model placement, display platform, and crop. Remove all blue and gold striping, all stars, roundels, logos, and any other markings from the large Tu-160 model so its visible surfaces are clean unmarked white and gray; match the actual aircraft's exterior proportions to the second reference without copying that reference's photo framing. Keep the Kh-55 model cleanly unmarked and unchanged. Preserve the traveler as a visibly illustrated 2D figure with drawn contours and soft colored shading; do not make him photorealistic. Do not change either model into an operational scene. Add no text or symbols.

- Supplied initial-generation references: traveler turnaround and emotion sheets (identity/rendering boundary); Tu-160 flight and Kh-55 museum photos (object forms). For edit: rejected v00 image as target plus both character references and both object references.
- Output v01: 1672 × 941 PNG; SHA-256 `53e23dd73ed34f66f3815835df7659d2e4069aa4fff53f64b819320d6e85d279`.
- Review: pose and left/right actions match the brief; figure remains visibly outlined/illustrated within a realistic room. Plane markings removed; candidate only, pending crop and sequence review.
- Imagegen controls: no explicit output-size/quality controls were available; actual dimensions measured from the file.

## Scene 030 — `scene_030_v01.png`

Exact prompt:

> Nuviko History scene 030, photorealistic historical reconstruction of a Soviet long-range-aircraft design bureau in the early 1970s, widescreen 16:9. A spacious but practical engineering room with long drawing tables, precise mechanical drafting tools, large pale blueprint sheets showing only faint non-readable technical lines, drafting lamps, rulers, dividers, and a few anonymous engineers in period-appropriate plain work clothes studying a clean aircraft side-profile sketch. The drawing is generic and unmarked, not a recognizable Tu-160 prototype; no exact design or recorded meeting is implied. Composition uses the rows of tables to lead toward a bright work surface, warm industrial window light with cool ambient shadows, documentary realism. All people are anonymous, natural poses, no identifiable faces. No text, letters, logos, flags, numbers, weapons, missile, or dramatic action. Leave a quiet dark caption-safe band along the lower edge and keep major hands/tools on the table within frame.

- No external reference was supplied; this is a generic conceptual reconstruction of a design workspace, not a documented meeting or actual design bureau interior.
- Output: 1672 × 941 PNG; SHA-256 `ccd7201b5b68daf3c2df56cb88d9fcbe2255af1cdbcc33b76a6f532100741b1b`.
- Imagegen controls: no explicit output-size/quality controls were available; actual dimensions measured from the file.


## Scene 084 — `scene_084_v01.png`

Exact prompt:

> Nuviko History scene 084, photorealistic educational museum diorama, 16:9 landscape. High diagonal view over one shared physical dark slate surface on which three distinct inert scale models are arranged with clear space between them: a white Tu-160 long-range aircraft, a generic upright silo-based intercontinental missile model displayed safely and without explosive detail, and a large submarine model partly revealed by a separate transparent water-section panel. All are presentation models only, not active systems; no launch, blast, targeting, or attack. Cool neutral museum light with controlled highlights, the aircraft gets slightly stronger directional light to lead from the previous scene, then the eye can travel across missile and submarine. Physical scale models only; no warhead internals, launch, targeting, blast, map arrows, or digital overlays. No people, text, names, flags, national marks, logos, numbers or digital overlays. Keep all three carriers fully visible and distinct, with subtitle-safe negative space along the lower edge. Documentary photorealism; no claim that these exact models were in one place together.

- No external references supplied; all objects are generic inert scale models.
- Output: 1672 × 941 PNG; SHA-256 `d410c01ae76fbcd5439b42ed5f090503da0fb35cc11dd071fe69777002753fbd`.

## Scene 087 — `scene_087_v01.png`

Exact prompt:

> Nuviko History scene 087, photorealistic explanatory museum model tableau in 16:9 landscape, distinct from an earlier evenly balanced triad. Elevated close diagonal view: a white Tu-160 scale model is the clear foreground focal object under a narrow cool spotlight, its full aircraft shape visible; behind it, smaller but distinct, a covered land-based missile silo model and a separate submarine model in a shallow glass water panel form a layered strategic display. This represents one additional type of delivery carrier joining forces already shown, not a coordinated attack or a unified launch. Physical scale models only; no warhead internals, launch, targeting, blast, map arrows, or digital overlays. Deep perspective, subtle museum reflections, directional light joins the three objects without obscuring any. No people, text, labels, names, flags, numbers, logos or national markings. Keep all objects in frame with dark clean lower caption space. Documentary photorealism.

- No external references supplied; all objects are generic inert scale models.
- Output: 1672 × 941 PNG; SHA-256 `32127a867898bdb2c0664f9f05b1c9d9bffc66df155cf0d4b4346bd7f6e73fb5`.


## Scene 019 — `scene_019_v01.png` (composite archive board)

A blank archival tabletop was generated, then the two genuine source photographs were placed unchanged inside the blank mounts by uniform resize-to-contain and direct paste. No source photograph was regenerated or cropped. This is a literal archival-photo composite, not a depiction of a documented shared event.

Exact background prompt:

> Create a cinematic 16:9 photorealistic archival-table scene for a documentary. Camera directly overhead, looking straight down at a dark walnut archive table under subdued warm desk-lamp light, with two large clean rectangular photo mounts laid horizontally side by side and aligned parallel to the frame. Each mount has a blank light-gray center, thin paper border, and subtle natural shadow, with clear empty space for photographs to be placed exactly on top in postproduction. Add a few neutral file folders at the outer edge only, no readable text or markings. The two photo areas must be broad landscape rectangles, flat and undistorted, fully visible with margins; the background grain and light should feel like a real archival work surface, not a graphic layout. No people, aircraft, missiles, military objects, flags, words, labels, numbers, dates, stamps, or logos.

- Background output: 1672 × 941 PNG from imagegen; supplied reference paths: none.
- Left photograph: `tu95_bear_a_flight_1977_dod_publicdomain.jpeg` (U.S. DoD/NARA 1977 Tu-95; PD-US). Right photograph: `rockwell_b1a_74_0159_inflight.jpg` (U.S. Air Force B-1A; PD-US).
- Composite process: original photo pixels uniformly scaled to fit the two flat mounts, centered with no crop or content retouch.
- Final output: 1672 × 941 PNG; SHA-256 `ebce8ca5871daa14aadf101b4d78f11da27acd74d62098872c64e249d971838c`.
- Full-frame review: both aircraft remain recognizable, photographed source content preserved; the layout matches the planned archival-table reveal. Candidate pending final motion and subtitle overlay checks.

## Archive scene assets 015 and 028

- Scene 015 `scene_015_v01.jpg` is the unaltered 1977 U.S. Department of Defense/National Archives Tu-95 Bear-A flight photograph; SHA-256 `25b69c6013021907ac19a7737216cd1dbd3634ebc61b17444b5da7100b33210d`. This is an actual 1977 aircraft image, not a reconstruction.
- Scene 028 `scene_028_v01.jpg` is the unaltered U.S. Air Force B-1A serial 74-0159 in-flight image; SHA-256 `b7c070149e0a8f56678ad997e279765656f8ed1ecb74a2c556d8726811bf1252`. The Commons page identifies it as a B-1A and public domain in the U.S.; exposure date is not established, so do not call it the 1974 first flight.
- Scene 110 `scene_110_v01.jpg` is the unaltered DTRA/National Archives Tu-160 dismantlement photo described in the preceding archive reference block.


## Scene 105 — `scene_105_v01.png` (reused image)

- Reuses the exact accepted candidate from `scene_045_v01.png`, SHA-256 `449e1e098010215f723d21b6bd74d1a0d2135e10f50d3e6804afdab246200fea`; no new image generation or pixel edit.
- The flight image clearly shows the Tu-160's wings swept back and creates a visual counterpoint to scene 104's parked, wider-wing configuration. It is a generic reconstruction, not a specific high-speed test.
- Scene 105 can use a short motivated push-in along the swept wing; adjacency/crop must be checked before acceptance.


## Approved archive-gap fallback candidates — scenes 031, 092, 096, 099, 108

These candidates follow the visible Extra High fallback consultation recorded in `Research/CONSULTATION_ARCHIVE_FALLBACKS_v01.md` and the scene-specific directions in `Storyboard/visual_score_v02.md`. They are contemporary explanatory constructions, not archival photographs.

### Scene 031 — `scene_031_v02.png`

Exact prompt:

> Nuviko History scene 031 v02, 16:9 photorealistic contemporary explanatory still life. Direct overhead camera over a clean, present-day charcoal-gray cutting mat on a neutral worktable. At the center is a carefully cut white cardstock silhouette of a large long-range aircraft with variable-sweep wings, made as an obvious physical paper model. Around it: a metal ruler, plain unprinted card pieces, a circle template and a few simple geometric construction pieces. Strong directional side light creates real contact shadows and reveals paper edges; restrained, focused documentary composition with generous negative space. This represents organised aircraft design in general, not the actual Tupolev bureau, a historical office, a real blueprint or a documented meeting. No people, historical papers, Soviet-era furniture, legible text, drawings that claim to be technical plans, logos, flags, numbers, tools cutting anything or military weapons. Leave the full cardstock aircraft form visible and keep a clean upper-left area for later subtitle overlay.

- Supplied reference paths: none. Generic cut-card model; not a historically specific aircraft document or workspace.
- Output: 1672 × 941 PNG; SHA-256 `41f9439f7be52bc4644147e5062415d1bd72a1009382ef928c4d93573b4334b7`.
- Full-frame review: paper edges, cutting mat, ruler and geometric pieces are clear; no dated marks, office, people or text. Candidate.

### Scene 092 — `scene_092_v02.png`

Base exact prompt:

> Nuviko History scene 092 v02, photorealistic contemporary explanatory display, 16:9 landscape. A precise small white physical Tu-160 silhouette model, accurately shaped from the supplied aircraft reference, is held above a neutral matte gray tabletop by an unmistakable transparent acrylic stand. A single thin curved strip of white paper rises and arcs behind it as an abstract trajectory. The static display is clearly a present-day schematic object, not a real aircraft photographed in flight and not an archival reconstruction. Quiet directional museum light, tactile paper and acrylic, sculptural negative space, restrained cinematic composition. Keep the complete aircraft model inside frame and leave clear upper-left negative space for a clean modern editorial caption added later. No people, runway, sky, clouds, archival film grain, text, numbers, logos, flags, military symbols, weaponry or simulated takeoff.

Exact edit prompt:

> Edit the exact first referenced image while preserving its aircraft model, acrylic stand, paper trajectory, camera, lighting, background, materials and crop. In the empty upper-left corner only, add a restrained contemporary editorial caption in clean uppercase sans-serif typography, aligned left, dark charcoal ink with ample spacing. The wording must be exact and spelled correctly on three lines: “FIRST FLIGHT” / “SCHEMATIC ILLUSTRATION” / “18 DECEMBER 1981”. Keep it clearly a modern caption placed over a physical schematic model; do not add archival styling, handwriting or any other text or marks.

- Supplied reference: Tu-160 flight photo `Research/VisualReferences/tu160_inflight_sergey_lysenko_2013.jpg`, aircraft form only; the photograph itself is not embedded in the candidate.
- Output: 1672 × 941 PNG; SHA-256 `da3b6b17f778be18b25d6a3f02969308bd1afb9198fe9e6c8b088e81c3262d13`.
- Full-frame review: exact words and date are legible; physical aircraft model, acrylic stand and curved paper ribbon make schematic status visually clear. Candidate only. Continue searching for a licensed image of the event; do not represent this model as a photograph of the actual flight.

### Scene 096 — `scene_096_v02.png`

Base exact prompt:

> Nuviko History scene 096 v02, photorealistic contemporary tabletop assembly schematic, 16:9 landscape. On a clean charcoal-gray studio surface under soft dimensional side light, show three separate white cardstock components of a long-range variable-sweep aircraft arranged along a clear assembly axis: nose/fuselage section, central body and wing assembly, then a more complete but still visibly handmade cardboard aircraft model at the far end. Include a simple abstract metal support frame and plain unprinted card spacers; one assembled section is the visual focal point. This is a present-day explanatory construction about aircraft manufacture in general, not a reconstruction of the Kazan factory, not a historical shop, and not a real documented build. Every piece should visibly be a model or teaching schematic. No people, factory interior, workers, machinery, signs, historical documents, logos, flags, text or labels. Leave a clean lower-left area for an editorial status caption added later. Keep all sections distinct and fully in frame.

Exact edit prompt:

> Edit the exact first referenced image without changing its paper aircraft sections, assembly frame, camera, lighting, shadows, background or crop. In the open lower-left corner of the dark tabletop, add a small clean modern uppercase sans-serif editorial caption, left-aligned, reading exactly “ASSEMBLY SCHEMATIC”. Keep it unobtrusive but readable. Do not add any other words, dates, labels, signage or historic details.

- Supplied reference: Tu-160 flight photo, exterior identity form only; no source photo embedded.
- Output: 1672 × 941 PNG; SHA-256 `96dc2a0a5eee53b851141f17365d08336c5b42b54acf036e13cffc7f8c9c55f0`.
- Full-frame review: sections are visibly cardstock models on a contemporary frame, no factory or claimed historical shop; exact caption legible. Candidate.

### Scene 099 — `scene_099_v02.png`

Base exact prompt:

> Nuviko History scene 099 v02, contemporary physical milestone display, photorealistic 16:9 macro scene. A raised, minimal paper timeline runs diagonally across a neutral charcoal-gray tabletop and stops at a prominent blank pale date card standing upright. Beside the card rests a small, clearly static aircraft-shaped schematic relief made of white cardstock on a low support, not an aircraft photograph. Strong controlled spotlight on the blank date card and model, gentle dimensional shadows, neutral modern materials and precise documentary composition. This is an editorial explanatory timeline, not a record or photograph of a 1984 flight test. No runway, sky, flying pose, workers, hangar, historical artifacts, printed marks, legible text or date. Leave broad empty space on the date card for exact type to be added later and a quiet area below for a short factual status caption. Keep the date card and silhouette fully in frame.

Exact model correction prompt:

> Edit the first referenced image, preserving the exact camera, timeline track, blank date card, neutral background, lighting, shadows and composition. Replace only the small white cardstock aircraft relief on the right. It currently has the wrong generic aircraft form. Make it a restrained, unmistakable Tu-160 schematic silhouette with a long pointed nose, variable-sweep wings shown in a moderate swept position, four paired engine nacelles and twin vertical tail, matching the supplied Tu-160 reference proportions. Keep it a static white physical card model on the same low display stand, not a photograph or real flying aircraft. Add no text, dates, markings, logos or new objects.

Exact caption edit prompt:

> Edit the exact first referenced image and preserve its composition, raised timeline track, model, blank standing card, lighting, materials and crop. Add legible, clean modern uppercase sans-serif type on the blank face of the standing card, centered with ample spacing, in three lines with the correct hierarchy: large “1984”; smaller “FIRST PRODUCTION AIRCRAFT TEST”; and smallest “EXPLANATORY TIMELINE — NOT HISTORICAL DOCUMENTATION”. Spell every word exactly as written. The card must read as a contemporary editorial display, not a historical document. Add no other text, dates or objects; keep the aircraft schematic small and stationary on its stand.

- Supplied references for aircraft correction: Tu-160 flight photo (object silhouette only); no source photo embedded.
- Final output: 1672 × 941 PNG; SHA-256 `d864f6bb353add56fa4db366e76960337dcf36487e7d4247982f784b1a5df164`.
- Full-frame review: Tu-160-like stationary model on a modern stand; exact year and captions legible; no runway or simulated flight. Candidate. Any image asserted to depict the actual 1984 test remains blocked until an authentic cleared source is available.

### Scene 108 — `scene_108_v02.png`

Base exact prompt:

> Nuviko History scene 108 v02, unmistakably contemporary physical metaphor, 16:9 photorealistic tabletop still life. On a clean neutral graphite-gray surface under restrained side lighting lies one single deep-red sheet of paper divided by a pronounced jagged fractured seam. Its two broad halves remain visibly connected along one edge and share the same fibers, proving they came from one sheet; they are gently separated by only a few centimeters. The split represents the end of a political structure in December 1991, not a literal map, flag, ceremony, attack, physical collapse or historical event. Modern tactile paper edges, subtle real shadows, stark quiet negative space at upper left for later clean editorial caption. No historical objects, archival borders, grain, documents, newspapers, flags, maps, people, text, emblems, numbers or fire. Calm documentary composition, no dramatic ruin.

Exact edit prompt:

> Edit the exact first referenced image, preserving its single red sheet, jagged torn seam, visible fibers, gray tabletop, camera, lighting and crop. In the empty upper-left gray space, add one clean contemporary editorial caption, uppercase charcoal sans-serif, left-aligned: “DECEMBER 1991”. Keep the caption legible and unobtrusive. Do not add any other text, flags, maps, documents, people, symbols, archival grain or historical details.

- Supplied reference paths: none.
- Output: 1672 × 941 PNG; SHA-256 `4fc03499cccb7a5a070e66d56dbf3752e7ecb4a2ba148d199ea2bea6f0dd3992`.
- Full-frame review: clear torn seam in one physical sheet; exact date caption readable; no implied ceremony, map or real archive. Candidate bounded metaphor.

## Scene 117 — `scene_117_v02.png` (new contemporary timeline)

Exact prompt:

> Create one 16:9 widescreen image for an English-language history documentary, a contemporary explanatory museum tabletop model about the forty-year span between the Tu-160 prototype's first flight in 1981 and the newly built Tu-160M first flight in 2022. A single clean timeline runs diagonally across a neutral pale stone table. At the left, a small white variable-sweep bomber scale model sits beside a simple raised card reading “1981”; at the right, a closely matching, subtly modernized white bomber model sits beside a raised card reading “2022”. A fine continuous brass line joins the two dates, with forty small etched tick marks subtly visible, suggesting elapsed time. Soft museum daylight, tactile paper and brushed metal, sophisticated restrained editorial installation, accurate general Tu-160 silhouette with long nose, swept wings and four engines, strong clear visual distinction between two dated models. Camera slightly elevated, models and dates all safely inside frame with generous margins, no people, no flags, no military action, no weapons shown, no logos, no other text, no archival-photo styling. Highly realistic studio photography.

- References supplied: none. This is a contemporary editorial display, not documentary photography and not a claim about the exact 1981 or 2022 airframes.
- Output: 1672 × 941 PNG; SHA-256 `ac10041434a6bd19b4c0412b3926dfcedd330daddb84eb271ac399d22554f9d2`.
- Full-frame review: both aircraft models and dates are legible, the linking timeline is visible, and all elements remain within the frame. Candidate only.

# Paper Detour 038 — scene selection and generation log v01

Updated 2026-11-03. **This file owns the current scene-image selection and its provenance.** Author review is not independent review or user approval.

## Inputs and profile

- Episode/channel: 038, Paper Detour, Russian long film.
- Storyboard: `Storyboard/SHOTLIST_v58.md` is current. S001–S003 used the unchanged v04 compositions. S004–S007 were generated from v05/v06 scene meanings; v07 records the actual accepted S005/S007 compositions. v08 records S008–S009 accepted compositions without changing narration or story function.
- Visual bible: `Source/Production/VISUAL_BIBLE_v01.md`.
- Profile: `.agents/skills/ytv-scene-images/references/paper-detour.md`.
- Delivery frame: 2560×1440, 16:9. No camera motion/parallax.
- Built-in `image_gen` generated all selected images. Each prompt requested maximum available quality and 4K UHD 3840×2160. The tool exposed no separate resolution control; actual returned images are 1672×941 RGB PNGs, opaque, 16:9. Fit to 2560×1440 is proportional scaling by approximately 1.531 with no crop. Upscaling adds no native detail.
- Channel style references: Paper 004 `channels/paper_detour/Shared/References/Paper/paper004_user_38.png`, SHA-256 `238bb11958c8e59224edcd006db060df0bddd0c9e100f795e44eeb537ebdc166`; Paper 033 `channels/paper_detour/videos/033_time_stop/Source/Images/paper_v01/S01_v01.png`, SHA-256 `700b11da5d3c4c0bc1032eb1f48b3bdb7373378865b94cdf33184e9921b048f0`. Both were used as paper/card style references only. No modern subject, setting, rain or wet street was reused.

## Current selection

| Scene | Selected file | SHA-256 | Status | Image review and open dependencies |
|---|---|---|---|---|
| S001 | `S001_v01.png` | `008db56fc4f3ad13c36c2bae0124ca0e71e1930b9ad616da542f840e1ac56c67` | **AUTHOR ACCEPTED — 2026-11-03** | Edo roofline, estate gate, small distant group approaching; bare branch and dark evergreen silhouettes fit the January date without adding snow/weather. Full frame, 640×360 phone reduction, 2560×1440 proportional upscale and gate/figure detail inspected. Upper-center and lower-center text reserves contain no key action/evidence. |
| S002 | `S002_v01.png` | `230b8ba0636ce34af2e755e4f85c155500925285b5de1dc21d3253c3048d57b1` | **AUTHOR ACCEPTED — 2026-11-03** | High oblique cutaway of the same gate, armed paper figures entering. No fight, guard count, injuries or added room plan. Full frame, phone reduction, proportional 2K upscale and gate/group detail inspected. Subtitle reserve is clear. The upper-center gate roof occupies the candidate accent region; if captions keep the tentative `47` accent, this scene needs a safe approved placement or a revised image before import. |
| S003 | `S003_v01.png` | `96c10628d540ff162d2d577efaaa2faba0065bf629b930a39d7363ec76ebcf08` | **AUTHOR ACCEPTED — 2026-11-03** | Close high-oblique corridor cutaway with open, empty spaces and a few searching figures. No target is shown, and no exact floor plan is claimed. Full frame, phone reduction, proportional upscale and search-detail crop inspected. Subtitle field crosses a dark foreground roof; readability and final overlay fit remain to be checked with real subtitles. Storyboard assigns no accent here. |
| S004 | `S004_v01.png` | `358e054bfa004eb3f16a463954c28b6b8785cfb7aabe4cffb945a71eca7fbadd` | **AUTHOR ACCEPTED — 2026-11-03** | Reverse wide view from inside the estate toward an empty passage; the approaching group is gathered at the threshold. No target or exact room is shown. Full frame, phone reduction, proportional upscale and gate/group detail inspected. Clear subtitle field. |
| S005 | `S005_v01.png` | `5398839741180409073e7e807d163f3bba2622d71735b29ccd8c5632ba5b44e5` | **AUTHOR ACCEPTED — 2026-11-03** | Side-on group and long shadows as a metaphor for willingness to risk their lives. The selected version stops the shadows above the subtitle field; full frame, phone reduction, proportional upscale and figures/shadow detail inspected. The first draft let shadows enter the bottom subtitle band and was not selected. |
| S006 | `S006_v01.png` | `94a9bb18cc55f25b2a89b43dcd701d413111f880f749213e470b092c1ba70340` | **AUTHOR ACCEPTED — 2026-11-03** | Neutral pre-attack scene: unarmed Kira faces Asano, whose short blade remains sheathed; distant gate is a separate time-link layer. Generic similar-age faces and no portrait likeness. Full frame, phone reduction, proportional upscale and character detail inspected. Lower subtitle field is clear. Two earlier drafts were not selected: one overemphasized Kira's age; another let figures enter the subtitle field. |
| S007 | `S007_v01.png` | `fc3085ea85154f4cd7acf188dbaed6d76097155373bae990f5841b2c27662e96` | **AUTHOR ACCEPTED — 2026-11-03** | Asano's short-blade attack, with Kira stepping back, empty-handed; no contact, injury or blood. Full frame, phone reduction, proportional upscale and blade/hand detail inspected. Action reads at phone size and stays above the subtitle reserve. |
| S008 | `S008_v01.png` | `3146f7aac40ce9e3ee61ec8837ae6724d1197a568a9e92cb21a0ee28622e541a` | **AUTHOR ACCEPTED — 2026-11-03** | Rōnin silhouettes at left; framed Asano–Kira corridor tableau at right; broad upper sky supports candidate “47”; lower foreground remains empty. Full frame, phone reduction, proportional 2560×1440 fit inspected. First draft was rejected because figures/frame entered subtitle reserve. |
| S009 | `S009_v01.png` | `03e71ecfe14b93d61784ac8077f72effc60c747322f4cf55822306b4bf0bd607` | **AUTHOR ACCEPTED — 2026-11-03** | Retainers face closed gate and blank open order on a stand; no writing, seal, or invented court scene. Full frame, phone reduction, proportional 2560×1440 fit inspected. Upper candidate accent area and lower subtitle reserve remain clear. |
| S010 | `S010_v01.png` | `c27f20c47613949e935094f3c5d298ee4e6481bae09c9d11708d60b8e737602b` | **AUTHOR ACCEPTED — 2026-11-03** | Wide bridge tableau: retainers in a left inset; Asano directs his short blade at Kira in the corridor with no contact or injury. Action reads at phone size; the upper sky is open for the planned accent and the lower subtitle band is clear. Full frame, phone reduction and proportional 2560×1440 fit inspected. |
| S011 | `S011_v01.png` | `876690d9ff87f5cce4adacc15f94543ea2b2c4724ea8b601582e5aa58016e818` | **AUTHOR ACCEPTED — 2026-11-03** | Generalized Edo residence reception hall being prepared with folded screens. Corrected to early spring greenery after first candidate retained winter-bare trees. Full frame, phone reduction, setup detail and proportional 2560×1440 fit inspected; upper accent area and bottom subtitle floor are clear. |
| S024 | `S024_v01.png` | `4d826f93ff8aa1a7068cc9210b69d479d93b82d2c66b5e3d66d7b98d11468f87` | **AUTHOR ACCEPTED — 2026-11-03** | Closed gate and tied blank order as a neutral sign of the same-day ruling; quiet upper sky preserves the planned accent. Full frame, 640×360 phone reduction, portrait center crop, and order detail inspected; native output 1672×941 RGB. |
| S025 | `S025_v01.png` | `2347fad4960197760b75017b7b7ee4495a03e4351bdf5c43266f3663f8c1a7c1` | **AUTHOR ACCEPTED — 2026-11-03** | Paired estate entrances show an unequal outcome: left gate shut with a blank order, right gate open and undisturbed. Full frame, phone-size, portrait center crop and gate contrast detail inspected; native output 1672×941 RGB. |
| S026 | `S026_v01.png` | `dbcb846dab09d556ee8056e629bca5a501204597696d2e2959ebff55381524c1` | **AUTHOR ACCEPTED — 2026-11-03** | Six generalized retainers stand outside the closed estate gate, separated by small gaps; no lord, arrest, action, or exact historical headcount is implied. Full frame, 640×360 phone reduction and people detail inspected; native output 1672×941 RGB. |
| S027 | `S027_v01.png` | `0238d31de4db466abbf8a06bfbd7d2a72de6e18393feb79837553f1f45c2a1f5` | **AUTHOR ACCEPTED — 2026-11-03** | High three-quarter view places the group outside the closed estate, separated from a distant empty passage; no specific crest or exact site layout is implied. Full frame, 640×360 phone reduction and group detail inspected; native output 1672×941 RGB. |
| S028 | `S028_v01.png` | `daba0d60f627d9bf6ffa495704c09e7d88518d3121a8c39ffe23ae8b9b39f34c` | **AUTHOR ACCEPTED — 2026-11-03** | Two retainers face the closed gate; hands are relaxed and blades remain sheathed. First composition was revised because figures entered the subtitle band; second was revised because the men faced one another. Final frame, phone-size and hands/sword detail inspected; native output 1672×941 RGB. |
| S029 | `S029_v01.png` | `f4b8b95bec6c1ef9cd75efc812bca0c57a0e1605dc90c5529a7e38b379afe5de` | **AUTHOR ACCEPTED — 2026-11-03** | Reverse high-angle view of the closed estate gate and empty approach; no eviction, poverty, or invented family details. Full frame, 640×360 phone reduction and gate detail inspected; native output 1672×941 RGB. |
| S030 | `S030_v01.png` | `e6825786ce7ec5a564fd7aefc13aedd4fbdfde8d6e2a953405f40844db06d762` | **AUTHOR ACCEPTED — 2026-11-03** | Quiet residential lane with indistinct silhouettes behind shoji; revised to remove an unneeded prominent castle/keep. Full frame, 640×360 phone reduction and household detail inspected; native output 1672×941 RGB. |
| S031 | `S031_v01.png` | `83afdd9fe2d38795b5429233ca06464018d6f5972f4a9dd1dd42f3764ac144e6` | **AUTHOR ACCEPTED — 2026-11-03** | Several separated, small former retainers on a residential lane; the image represents masterless status without asserting an exact headcount. Reframed to keep people and shadows above subtitle reserve. Full frame, phone-size and group detail inspected; native output 1671×941 RGB. |
| S032 | `S032_v01.png` | `752d18e417dd6357eb651e0a9b478a816b87503403bf811fb181a23406f026ab` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous retainers consider resistance or surrender around a paper gate model, blank sheet and fully sheathed sword. Reframed to remove the pot, sheath the entire blade and clear the subtitle floor. Full frame, phone-size and tabletop detail inspected; native output 1672×941 RGB. |
| S033 | `S033_v01.png` | `b65ac26ab4f13a3b3d394bf494c38511ea8571a418f8674a21a28aa8f8ac822a` | **AUTHOR ACCEPTED — 2026-11-03** | One anonymous retainer sits apart from an otherwise quiet council; empty tatami carries the unspoken choice. Reframed to place all figures above subtitle reserve; no ritual or bodily action. Full frame, phone-size and figure detail inspected; native output 1672×941 RGB. |
| S034 | `S034_v01.png` | `7226cc87a5a167fd688737dd580ca2908d3397f7dcf256e97162d09030400bed` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous speaker rises before the quiet council, making a restrained proposal; sword sheathed; no target, map or violence. Full frame, phone-size and council detail inspected; native output 1672×941 RGB. |
| S035 | `S035_v01.png` | `29b89de04a533d8fbd07f3bfc5b99b3ca9451b00862ab686aae3f36f7c600808` | **AUTHOR ACCEPTED — 2026-11-03** | Empty formal room and unoccupied place look through to closed estate gate; symbolizes the absent lord and ended service without depicting destruction. Full frame, phone-size and room detail inspected; native output 1672×941 RGB. |
| S036 | `S036_v01.png` | `4261485c71679b8f46192f3012fd6ff8b422cf360f21e973b8f196938aa61222` | **AUTHOR ACCEPTED — 2026-11-03** | Generic Kira figure walks alone, unhurried, along an open street; sheathed sword stays at his waist. Portrait edit was rejected; fresh landscape frame puts figure/shadow above reserve. Full frame, phone-size and figure detail inspected; 1672×941 RGB. |
| S037 | `S037_v01.png` | `98a4028c78b2d352c05eb2cc0d4aa6543a76347d465aa5c75a14cab540a78bea` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous retainer at the threshold looks back to the quiet council; open passage conveys an unresolved choice without a literal exit or portrait claim. Full frame, phone-size and figure detail inspected; native output 1672×941 RGB. |
| S038 | `S038_v01.png` | `01c8f86f89ffd10f16da9d3b207b184d257563475307fc191306873da929ad99` | **AUTHOR ACCEPTED — 2026-11-03** | A central anonymous indigo-clad retainer draws the council’s attention; leadership reads without asserting Ōishi’s appearance. Blank paper and a sheathed sword, no key. Full frame, phone-size and leader detail inspected; native output 1672×941 RGB. |
| S039 | `S039_v01.png` | `6f08ef7fd5e80434d9388082ef87782fb7c01c4ac453d987b4ac4b219aec2be3` | **AUTHOR ACCEPTED — 2026-11-03** | Central leader rests a hand on a blank order as some retainers turn aside; restrained dissent, no text or key. Full frame, phone-size and decision/table detail inspected; native output 1672×941 RGB. |
| S040 | `S040_v01.png` | `5f1f002ab116592cd34796bff52f146853640b24fad631f15b0e60c2c2770ed1` | **AUTHOR ACCEPTED — 2026-11-03** | Open paper gate model, blank order and fully sheathed sword form a restrained symbol of surrender and no immediate attack; no key or transfer ritual. Full frame, phone-size and prop detail inspected; native output 1672×941 RGB. |
| S041 | `S041_v01.png` | `28aba6658d3c73ad31e234f9e62d3e2daad4f9cfcacf2a36ea9bec95c0359c23` | **AUTHOR ACCEPTED — 2026-11-03** | Two supporters sit apart from the leader after his decision; one turns away and one lowers his gaze. No quarrel or permanent faction. Reframed smaller for subtitle safety. Full frame, phone-size and reaction detail inspected; native output 1672×941 RGB. |
| S042 | `S042_v01.png` | `97d618a2d43c96b660e7c27c3c6df1dfd0a11b21e2c6d9da5a982bfe3c4af575` | **AUTHOR ACCEPTED — 2026-11-03** | Wide council, empty place, open gate model and blank order symbolize the absent lord and voluntarily surrendered house; no key or literal handover. Full frame, phone-size and detail inspected; native output 1672×941 RGB. |
| S043 | `S043_v01.png` | `c1d7a970065be67695046ea96304597d31b84c5a47c5dd1e15e4925ffa055f68` | **AUTHOR ACCEPTED — 2026-11-03** | Large anonymous gate casts a broad shadow across the small Akō gate model and sheathed sword; symbolic authority imbalance, no identifiable shogun architecture. Full frame, phone-size and detail inspected; native output 1672×941 RGB. |
| S044 | `S044_v01.png` | `46b4d049d74891c9a1086b54d614b502fef877ba5ba6ad8aa9fe5a550a9de4e6` | **AUTHOR ACCEPTED — 2026-11-03** | Distant anonymous gate casts a connected shadow across intact houses with safe silhouettes behind shoji; no damage or panic. First candidate lacked a clear shadow source; revised. Full frame, phone-size and detail inspected; native output 1672×941 RGB. |
| S045 | `S045_v01.png` | `51d6fbf6f6f43d2f5d38c2d8754c3a2720069290853fc38d0018baa20b3640aa` | **AUTHOR ACCEPTED — 2026-11-03** | A generic retainer stands outside a quiet home; indistinct silhouettes behind shoji suggest personal stakes without identifying a family or exact event. Full frame, phone-size and home detail inspected; native output 1672×941 RGB. |
| S046 | `S046_v01.png` | `114769e7d5da6046204042b05a03e27250d3f1f84b3fa872fcdcdde66e9a4653` | **AUTHOR ACCEPTED — 2026-11-03** | Overhead fork: one path ends at a shut shadowed gate, the other stays open; the anonymous figure faces the open route. Metaphor, not geography. Full frame, phone-size and path detail inspected; native output 1672×941 RGB. |
| S047 | `S047_v01.png` | `5affca58cc06625bf52048254e6c5055f1090167a24ff60afc17e89eda72896c` | **AUTHOR ACCEPTED — 2026-11-03** | Blank petition and closed/open gate models with indistinct figure behind screen suggest Daigaku as conditional successor; no portrait, crest, readable writing or release claim. Reframed to move tabletop above subtitle field. Full frame, phone-size and detail inspected; native output 1672×941 RGB. |
| S048 | `S048_v01.png` | `3518f4506734b417bc29f9a579f5daa1c1778d5092d1e0e0e9c72960cf76e608` | **AUTHOR ACCEPTED — 2026-11-03** | Hypothetical restoration: former retainers wait outside a partly open unmarked gate, intact home visible beyond; no crest or completed-restoration claim. Full frame, phone-size and threshold detail inspected; native output 1672×941 RGB. |
| S049 | `S049_v01.png` | `db82549b19c5a844f98433cab15fea3e8ad3f364cf6946c22d6c6b4bcd289206` | **AUTHOR ACCEPTED — 2026-11-03** | Quiet lane, open home and indistinct household silhouettes with a small anonymous retainer in the distance; a peaceful possible future, not a completed reunion. Reframed for subtitle safety. Full frame, phone-size and detail inspected; native output 1672×941 RGB. |
| S050 | `S050_v01.png` | `dfa65bd20c2c8b89e3b1b890b50942447ed931d274d7b1427708bd575713f26c` | **AUTHOR ACCEPTED — 2026-11-03** | One council group and two paths toward open/closed gates show different strategies; no confrontation or fixed faction. Full frame, phone-size and route detail inspected; native output 1672×941 RGB. |
| S051 | `S051_v01.png` | `da33e1d25867dcccce203387955d46bf36c09d605d1ade3383be5ee99369dfc5` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous brown-clad retainer faces closed gate along the darker route; sheathed sword; no attack or blood. Reframed to remove foreground silhouettes and clear subtitle area. Full frame, phone-size and detail inspected; native output 1672×941 RGB. |
| S052 | `S052_v01.png` | `ae865d7dfc0d977c8745b181f1534a16646ab8d11a2f2bfb1a93a70096e2fc74` | **AUTHOR ACCEPTED — 2026-11-03** | Central leader considers a blank petition beside an open gate model; long dusk shadows symbolize limited time. No clock or literal meeting details. Full frame, phone-size and detail inspected; native output 1672×941 RGB. |
| S053 | `S053_v01.png` | `a7af99ecc62bb5d31eacacb4a06a3c8d7be5d2cb1fba435756f2c72294bb39ef` | **AUTHOR ACCEPTED — 2026-11-03** | Two separate quiet discussions with entirely blank sheets; no route, diagram or documented joint meeting. Full frame, 640×360 phone reduction, proportional fit and council detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v50/`. |
| S054 | `S054_v01.png` | `dca746fd97831e071ccf9b135b2954c13bc94592da3bcf94b2ff534139022f0f` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous retainers face a generic closed compound wall across an open street; no specific estate or access plan. Full frame, phone reduction, proportional fit and gate detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v50/`. |
| S055 | `S055_v01.png` | `bc3af3df2dfb11f682db5b1f9d6c03b58d32e689c40270b83b94312c56b2430f` | **AUTHOR ACCEPTED — 2026-11-03** | Symbolic shadowed approach and intact lit interior; no attack, casualty or claim of actual outcome. Full frame, phone reduction, proportional fit and shadow detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v50/`. |
| S056 | `S056_v01.png` | `efaf8bec1109a2f500ec958f132376d6dc7d041ef1c1f837c0b54a931daaefc6` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous figures separate along a generic Edo street; no invented employer, rejection or calendar. Full frame, phone reduction, proportional fit and street detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v50/`. |
| S057 | `S057_v01.png` | `ab8ad8ffbcc1a8a46a0285d00ca87cebcf26cacff7a77a3a504c15d225df59e9` | **AUTHOR ACCEPTED — 2026-11-03** | Two distant figures and empty cushions suggest diminishing commitment without asserting a meeting count. Full frame, phone reduction, proportional fit and room detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v50/`. |
| S058 | `S058_v01.png` | `44c18ba6bbacb63daafa9d8ae30d6030ccd8ae675c994b072ca56a827afba506` | **AUTHOR ACCEPTED — 2026-11-03** | Blank open sheet beside closed gate model; changing light suggests the July answer with no invented writing, seal or messenger. Full frame, phone reduction, proportional fit and paper/model detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v50/`. |
| S059 | `S059_v01.png` | `681e0c567538c61a6cdc4e19dce77c85997ca80c87f5a1aad07601e443715688` | **AUTHOR ACCEPTED — 2026-11-03** | Open household threshold contrasted with a closed generic domain gate; no exact residence, journey or identity. Full frame, phone-size, proportional fit and gate detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v50/`.
| S060 | `S060_v01.png` | `41fd4942110acbd207a8861854121c8f5ca6799bfb150e756a84063750a9ae62` | **AUTHOR ACCEPTED — 2026-11-03** | Central figure travels with two calm companions toward an ordinary open home; abstract closed gate model signals failed restoration, fully above subtitle band. First draft was rejected because the model entered the lower subtitle area. Full frame, phone-size, proportional fit and travel/model detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v50/`.
| S061 | `S061_v01.png` | `f5389f4e296946cbabac63c3d75ef054da454248d21e178a34eba904ac513508` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous indigo-clad leader beside blank sheet and open gate model; divided warm/cool light leaves private belief unreadable. No scholars or research props. Full frame, phone-size, proportional fit and table/model detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v51/`.
| S062 | `S062_v01.png` | `69f82737bb63b5232f14a0d28d5d4466bbe93baa6bbec2b83417cd4fb140ab23` | **AUTHOR ACCEPTED — 2026-11-03** | Quiet gathering around blank sheet; two fully sheathed swords at far wall and one new figure at doorway signal the start of preparation without plan or tactics. Full frame, phone-size, proportional fit and group detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v51/`.
| S063 | `S063_v01.png` | `fd51665a0a53bda34f154bca5a30b38eb7d9f7718eecc41dcdbb8c05b6d104a1` | **AUTHOR ACCEPTED — 2026-11-03** | One anonymous retainer at a fork with both routes clearly open; first draft with closed gate rejected. Full frame, phone reduction, proportional fit and junction detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v52/`. |
| S064 | `S064_v01.png` | `cd666e1bf23a03d92fe54c4296d26aea4967d057e989e44b78cebc594fe6eea6` | **AUTHOR ACCEPTED — 2026-11-03** | Several anonymous figures separate along a peaceful street as a possible future; no employer or actual hiring implied. Full frame, phone reduction, proportional fit and street detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v52/`. |
| S065 | `S065_v01.png` | `23f8ec3ed4051fb898a59bc75f92832be1870cd0c5688b1375d69baa14b42fd7` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous retainer paused between ordinary street and dim council room; blank petition and sheathed sword symbolize what leaving would mean. Full frame, phone reduction, proportional fit and threshold detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v52/`. |
| S066 | `S066_v01.png` | `f8bff912ce87c82c73baff1c9b6b161bf01a0875abc4edfc12b8c0265c45710e` | **AUTHOR ACCEPTED — 2026-11-03** | Loose informal group with indigo leader at equal scale; rigid lineup and earlier subtitle-collision composition rejected. Full frame, phone reduction, proportional fit and cluster detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v52/`. |
| S067 | `S067_v01.png` | `97b754adaca6b2cb4e42db40ed1a32723965596fd78367351d319a9da1fab394` | **AUTHOR ACCEPTED — 2026-11-03** | One leader at blank sheet, empty cushions and one distant doorway figure suggest difficulty recruiting without claiming a meeting count. Full frame, phone reduction, proportional fit and room detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v52/`. |
| S068 | `S068_v01.png` | `5dfc3de790fa9c8c0b76303f07ff3dcfe483f771a90ffab4efc2e0e899d1ae16` | **AUTHOR ACCEPTED — 2026-11-03** | Sheathed swords and blank sheet face a large generic closed government gate; possible state punishment shown without execution. Full frame, phone reduction, proportional fit and gate detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v52/`. |
| S069 | `S069_v01.png` | `bc83c8f28d1a1eb2c160ee3cc0fb207a4a303e1b41ce66c93d736d0f63b67571` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous retainer, blank open letter, sheathed sword and indistinct adult household silhouettes; wide revision clears the lower band. First close version rejected. Full frame, phone reduction, proportional fit and letter detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v52/`. |
| S070 | `S070_v01.png` | `e49b0619c501e6289fbab46a654e8891beb61cae89c9f749c3bbd366faa13748` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous writer with brush and blank letter; one indistinct household silhouette beyond shoji. Full frame, phone reduction, proportional fit and letter detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v53/`. |
| S071 | `S071_v01.png` | `ebe08fe1fb508f36077d554dd459eec44448af5428acd743f114d7014fe89676` | **AUTHOR ACCEPTED — 2026-11-03** | Blank letter, ordinary unmarked table objects and sheathed sword; no special gift/portrait implied. Full frame, phone reduction, proportional fit and tabletop detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v53/`. |
| S072 | `S072_v01.png` | `dfc47fc9f88690d2a5b360db3fb1e7c96e61e6540371dfcf8f53adffa5a0c7df` | **AUTHOR ACCEPTED — 2026-11-03** | Brown-clad retainer as an ordinary member among small pairs; centered candidate rejected for suggesting special attention. Full frame, phone reduction, proportional fit and group detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v53/`. |
| S073 | `S073_v01.png` | `69d20dfb955514fbb799a37bd29d24a4035dc203f64d4110ef140b95d833b6b5` | **AUTHOR ACCEPTED — 2026-11-03** | Blank petition, fully sheathed sword and small paper group form three editorial symbols. Full frame, phone reduction, proportional fit and symbol detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v54/`. |
| S074 | `S074_v01.png` | `6ff81930423df34f613b437bb27286c12394c7a639b80e6f28e47a3056be5afa` | **AUTHOR ACCEPTED — 2026-11-03** | Some anonymous figures leave for ordinary street while others stay by an open passage; no permanent faction or invented reason. Full frame, phone reduction, proportional fit and courtyard detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v54/`. |
| S075 | `S075_v01.png` | `04d75eec797e8cc6012f9e7073b7d6a6fc3ee8c220372295f2d8627975977b84` | **AUTHOR ACCEPTED — 2026-11-03** | Many layered figures are not precisely countable; clear upper-center sky reserved for possible “47” overlay. Full frame, phone reduction, proportional fit and accent-area crop inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v54/`. |
| S076 | `S076_v01.png` | `dd222c8070371c8a94b28eebb9c48f4e67eb6d7c5d3db000d1340b2889e4a9bb` | **AUTHOR ACCEPTED — 2026-11-03** | Brown and indigo figures at equal scale face the open gate with their wider group; no rivalry. Full frame, phone reduction, proportional fit and pair detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v54/`. |
| S077 | `S077_v01.png` | `3b62e56cf1881b6de8a1ea10853da25172ceb936acf086c6dfec320cce1d686c` | **AUTHOR ACCEPTED — 2026-11-03** | Two indigo figures of different age/height among the group; no portrait or added family gesture. Full frame, phone reduction, proportional fit and pair detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v54/`. |
| S078 | `S078_v01.png` | `05546c0bc94f0c6b79047ed4537523c51360fe11e08bfc1ca1971206704464a1` | **AUTHOR ACCEPTED — 2026-11-03** | Blank petition, distant closed generic gate and quiet retainers symbolize effort to preserve the house; no key/crest/plan. Full frame, phone reduction, proportional fit and document/gate detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v54/`. |
| S079 | `S079_v01.png` | `d7d12f2075b5958599e4659deadd3da27ae151a62ccfd7c2a4868d5ed211aab9` | **AUTHOR ACCEPTED — 2026-11-03** | Indigo leader precedes a group on a broad generic street; sheathed swords, no target or tactical detail. Full frame, phone reduction, proportional fit and group detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v54/`. |
| S080 | `S080_v01.png` | `3353533f39dc25e54d31aeddd0cc5e1ee2f440e6ba2d09d1d02dae3c160703ff` | **AUTHOR ACCEPTED — 2026-11-03** | Small group leaves an empty threshold; non-return suggested without death/farewell. Full frame, phone reduction, proportional fit and doorway detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S081 | `S081_v01.png` | `cfe1d1f95cbde1996c6ecd4aa02b08d8bab65d40beb25dcd7df9c885045b2e73` | **AUTHOR ACCEPTED — 2026-11-03** | Blank petition and intact open gate model recall the restoration choice. Full frame, phone reduction, proportional fit and model detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S082 | `S082_v01.png` | `93acb6c8f59e94a0d0ee47876a9a95194020ee9211f15e2444365e0f135d1943` | **AUTHOR ACCEPTED — 2026-11-03** | Blank petition and open model contrasted with distant closed gate; no map or reconnaissance. Full frame, phone reduction, proportional fit and gate detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S083 | `S083_v01.png` | `71ef276b3de42a0470292870db0ded2e741f59ad1ac77fb82ea13489ad11639e` | **AUTHOR ACCEPTED — 2026-11-03** | Generic closed gate/wall with indistinct shoji silhouettes. Foreground-group candidate rejected for subtitle collision; selected frame has no people in foreground. Full frame, phone reduction, proportional fit and gate detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S084 | `S084_v01.png` | `0832d38ebdbde9d0477863d6329bee1250b1ec5644b6a82af2701f87e8a52e77` | **AUTHOR ACCEPTED — 2026-11-03** | Anonymous official silhouette behind shoji and closed distant gate; no specific expression/thought. Full frame, phone reduction, proportional fit and silhouette/gate detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S085 | `S085_v01.png` | `db09b05d3b588347075f5a87a3766ce6cdab4b5b9b48aedb22e9fe5d99bd8ddb` | **AUTHOR ACCEPTED — 2026-11-03** | Empty partly open gate and broad vacant public street symbolize hypothetical escape. Full frame, phone reduction, proportional fit and gate detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S086 | `S086_v01.png` | `dc1bc20639e54bdb08bf3830476a78735bc57b9a4cbdbfdffad1454473925208` | **AUTHOR ACCEPTED — 2026-11-03** | Generic Edo night gate with group crossing; sheathed swords, no fighting, weather or tactic. Clear upper sky for date accent. Full frame, phone reduction, proportional fit and gate detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S087 | `S087_v01.png` | `488b13ea2954da6e3fec8da3b67be10127a3c2af418ae7c4b7b4ccf6c7b635de` | **AUTHOR ACCEPTED — 2026-11-03** | Generalized non-graphic interior clash with raised blades but no contact, injury or exact room. Full frame, phone reduction, proportional fit and action detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S088 | `S088_v01.png` | `28d6a10d42fffe5c940f5fdc6f66694c58185465b767a6c19951f4cd3e8bf4d5` | **AUTHOR ACCEPTED — 2026-11-03** | Open generic shoji and empty spaces with a few searching figures; no specific target/room plan. Full frame, phone reduction, proportional fit and empty-room detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S089 | `S089_v01.png` | `b8dc24cbacab1219eeff401e990b926a1094d447bb87c16f064ca98d5fb5fe6b` | **AUTHOR ACCEPTED — 2026-11-03** | One open generic room, a small retainer group and one empty illuminated cushion. A corridor-like first candidate was rejected as too specific. Full frame, phone reduction, proportional fit and empty-place detail inspected. Native output 1672×941 RGB; proofs: `Work/scene-image-review-v55/`. |
| S090 | `S090_v01.png` | `c7a2c3b31bcb6b019d02b67b78481b6c01f655af991c9c77b9c5e4f4eb3363f0` | **AUTHOR ACCEPTED — 2026-11-03** | Rōnin pause before a long empty night passage; Kira and a completed escape are absent. Full frame, phone reduction, proportional fit and passage detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S091 | `S091_v01.png` | `fc05f76e76751b8ba35eba37fe3ce80c566172458dfa86d1bb1948006d47fc8c` | **AUTHOR ACCEPTED — 2026-11-03** | Three shallow open spaces and several searchers; no hiding place or exact plan. Full frame, phone reduction, proportional fit and search detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S092 | `S092_v01.png` | `b526f8150e63530bdcac37802dfad8dc5ba169fb6d90d72e6fd3f5814ddc738b` | **AUTHOR ACCEPTED — 2026-11-03** | Searchers pause at an open doorway facing one seated generic dark-robed figure; no contact or portrait claim. Full frame, phone reduction, proportional fit and identification detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S093 | `S093_v01.png` | `856e82953415f2a4f8f5c86346a1026319262d2c550a0e2f12cd9589f20485a1` | **AUTHOR ACCEPTED — 2026-11-03** | Closer view of the same seated figure and retainers at the threshold; generic face and costume. Full frame, phone reduction, proportional fit and staging detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S094 | `S094_v01.png` | `51fb98e2ec12851587d47817735588f2c59bcce19d678678636c344a13892196` | **AUTHOR ACCEPTED — 2026-11-03** | Empty open threshold and diffuse shadows behind a separate screen leave escape hypothetical. Full frame, phone reduction, proportional fit and threshold detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S095 | `S095_v01.png` | `1d7fd4c63ef4bb507c4c715f22a1d883ee0e6145d1f1bc09c79de463580fb8d5` | **AUTHOR ACCEPTED — 2026-11-03** | Retainers now stand within the same room as the seated householder; no touch, restraint or attack. Full frame, phone reduction, proportional fit and finding detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S096 | `S096_v01.png` | `d0e43540372015b59550f067db0c08dcc8db15b0f346ad2f093ff0915affde52` | **AUTHOR ACCEPTED — 2026-11-03** | Earlier Asano–Kira attack from a new side angle; clear gap, no contact or injury. Full frame, phone reduction, proportional fit and blade-gap detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S097 | `S097_v01.png` | `043cf491cf2d90c691fb9c6316f361c990d9c12300abf20191bdc949f5381a4c` | **AUTHOR ACCEPTED — 2026-11-03** | Two recessed paper vignettes contrast the earlier attack with the present finding; no route or escape attempt asserted. Full frame, phone reduction, proportional fit and both-vignettes detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S098 | `S098_v01.png` | `4659c3ee0934ba2713fbe76030b33e77d9b069361793f5f127e7d2523265c85a` | **AUTHOR ACCEPTED — 2026-11-03** | Closed screen and an empty illuminated place symbolize the result; no person, weapon or act shown. First candidate with a sheathed sword near the subtitle field was rejected and revised. Full frame, phone reduction, proportional fit and empty-place detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S099 | `S099_v01.png` | `a2515d1fa645b178e3e4367bb752ee6eb69b6008dda810488f557fedbdcee022` | **AUTHOR ACCEPTED — 2026-11-03** | Group walks calmly out of the estate with one plain covered bundle; contents remain hidden. Full frame, phone reduction, proportional fit and bundle detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S100 | `S100_v01.png` | `dad58f27319ad5792ed922d0ca060b5e5c14a680e0f08e197a27da6523570ede` | **AUTHOR ACCEPTED — 2026-11-03** | Distant generic Edo street and modest unmarked gate; group and bundle continue with no exact route. Full frame, phone reduction, proportional fit and destination detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S101 | `S101_v01.png` | `a2ec2792cbf0922b572dbda82fd0f59ef5ea1d85afd996179454c1cffc90b218` | **AUTHOR ACCEPTED — 2026-11-03** | Covered bundle rests before an unmarked grave marker; bare branch and dark evergreen winter treatment. Initial autumn-colored foliage candidate was corrected. Full frame, phone reduction, proportional fit and grave/bundle detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S102 | `S102_v01.png` | `747494c1b96bf8a0ae0d333b53f98126af56ff690db1ddda80c6d9928e498ca8` | **AUTHOR ACCEPTED — 2026-11-03** | Closer grave and bundle with retainers in soft focus; no apparition or attack. Full frame, phone reduction, proportional fit and grave/bundle detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S103 | `S103_v01.png` | `330abbc076030175c5fc5ae6314c2197e99092eb4d4e07fd4fa53eea2088a53f` | **AUTHOR ACCEPTED — 2026-11-03** | Retainers wait before a generic closed gate, sheathed blades, bare branches and clear lower text band. Earlier candidate foliage and bottom-corner objects were corrected. Full frame, phone reduction, proportional fit and line detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S104 | `S104_v01.png` | `cf3a9195f725e14c4959227ad7551ff02bdbe1d922c17055e243be9d6aebdbb1` | **AUTHOR ACCEPTED — 2026-11-03** | A representative group and one separate neutral silhouette within overlapping paper planes; no arrow, time or motive. Full frame, phone reduction, proportional fit and separation detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S105 | `S105_v01.png` | `59ec1490715e5afd8c8f6acdeb49b61bf0bd341fba5fa80dc619d54fc173f7e3` | **AUTHOR ACCEPTED — 2026-11-03** | One neutral figure amid many layered paper folds as a metaphor for decades; no exact age, date or motive. Full frame, phone reduction, proportional fit and time-layer detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S106 | `S106_v01.png` | `77b41a5ae5fdaba7f04ab6dd2c57d2e39ca4b534b7986e596e5ece26e5b0bc1b` | **AUTHOR ACCEPTED — 2026-11-03** | Small waiting group before closed door; lower 35% clear. First foreground-seated candidate was repositioned to clear subtitle space. Full frame, phone reduction, proportional fit and waiting detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S107 | `S107_v01.png` | `b641e350bd00096a42ae00fbf399bfcb7843a52d462eef1bd261bf33b129582a` | **AUTHOR ACCEPTED — 2026-11-03** | Compact group oriented toward one generic gate; sheathed weapons, common purpose, no plan or tactics. Full frame, phone reduction, proportional fit and group detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S108 | `S108_v01.png` | `b1ef12ca49aaf5c95d35a431b577a67f94a6ae1c8c2619705a5ef17fb9d20279` | **AUTHOR ACCEPTED — 2026-11-03** | Retainers separated by empty space and an unmarked blank folded sheet as metaphor; no map or plan detail. Full frame, phone reduction, proportional fit and blank-page detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S109 | `S109_v01.png` | `144c0c3650f4ac381e3faf566501073ecd71911b4e656fe69046c416fa8d2ffe` | **AUTHOR ACCEPTED — 2026-11-03** | Long empty passage, closed door and small distant waiting figures; no weapons shown, no confiscation asserted. Full frame, phone reduction and proportional fit inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S110 | `S110_v02.png` | `ffb21d19e42e17d53f1d504043b626ba18dcc13adac2ea9532cb0c6693de892c` | **AUTHOR ACCEPTED — 2026-11-03** | Small level empty balance near the waiting figures and door; final composition clears the subtitle band. `S110_v01.png` retained as rejected because its foreground table entered the subtitle reserve. Full frame, phone reduction, proportional fit and scale detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S111 | `S111_v01.png` | `be99037192c73ff7c04ebf7892dd01fae8536229280fc30a8fe27e7c026c03a9` | **AUTHOR ACCEPTED — 2026-11-03** | Symbolic balance: a representative group against one generic official; not a court record or exact count. Accent omitted because the scale occupies the upper-center area. Full frame, phone reduction, proportional fit and scale detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S112 | `S112_v01.png` | `3387324595373a55233ccc73af21361ada5cb566b017ebf07ddb2f2a7b118af7` | **AUTHOR ACCEPTED — 2026-11-03** | Repeated paper gates and groups as hypothetical precedent only; blades sheathed. Candidate was edited to remove autumn foliage and clear the lower subtitle band. Full frame, phone reduction, proportional fit and panel detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S113 | `S113_v01.png` | `355ce97f70d8abef070914cac5894acf35dedcaea842902cb3d0f6ecad0e7346` | **AUTHOR ACCEPTED — 2026-11-03** | Group leaves an open generic estate with only the already-established covered bundle; no goods or exact room plan. Winter foliage and lower-band corrections applied. Full frame, phone reduction, proportional fit and procession detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |
| S114 | `S114_v01.png` | `ff6009af54f63a900fa249178b01a64a6129e3c1a49d0909c838407c6a664276` | **AUTHOR ACCEPTED — 2026-11-03** | Group and covered bundle cross an open, visible street at a calm pace; no pursuit or concealment. Winter foliage correction applied. Full frame, phone reduction, proportional fit and procession detail inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v56/`. |


## Rejected candidates in the v56 continuation

| Scene | Candidate | Status | Reason |
|---|---|---|---|
| S110 | `S110_v01.png` (`52063101e6f7fc8544524e99c3229214b962d4cc9cba489c8cb5e229a8523cf1`) | **REJECTED — 2026-11-03** | Foreground table and support entered the lower subtitle reserve. The image is preserved for provenance; selected replacement is `S110_v02.png`. |

Exact prompt strings, generated source IDs, reference paths/hashes, and per-scene revisions S090–S114 are in [generation prompts v56](GENERATION_PROMPTS_v56.md); S115 is in [generation prompts v57](GENERATION_PROMPTS_v57.md); S116 is in [generation prompts v58](GENERATION_PROMPTS_v58.md); S117 is in [generation prompts v59](GENERATION_PROMPTS_v59.md); S118 is in [generation prompts v60](GENERATION_PROMPTS_v60.md); S119 is in [generation prompts v61](GENERATION_PROMPTS_v61.md); S120 is in [generation prompts v62](GENERATION_PROMPTS_v62.md); S121 is in [generation prompts v63](GENERATION_PROMPTS_v63.md); S122 is in [generation prompts v64](GENERATION_PROMPTS_v64.md); S123 is in [generation prompts v65](GENERATION_PROMPTS_v65.md); S124 is in [generation prompts v66](GENERATION_PROMPTS_v66.md); S125 is in [generation prompts v67](GENERATION_PROMPTS_v67.md); S126 is in [generation prompts v68](GENERATION_PROMPTS_v68.md); S127 is in [generation prompts v69](GENERATION_PROMPTS_v69.md); S128 is in [generation prompts v70](GENERATION_PROMPTS_v70.md); S129 is in [generation prompts v71](GENERATION_PROMPTS_v71.md); S130 is in [generation prompts v72](GENERATION_PROMPTS_v72.md); S131 is in [generation prompts v73](GENERATION_PROMPTS_v73.md); S132 is in [generation prompts v74](GENERATION_PROMPTS_v74.md); S133 is in [generation prompts v75](GENERATION_PROMPTS_v75.md); S134 is in [generation prompts v76](GENERATION_PROMPTS_v76.md); S135 is in [generation prompts v77](GENERATION_PROMPTS_v77.md); S136 is in [generation prompts v78](GENERATION_PROMPTS_v78.md). Built-in `image_gen` exposed no resolution control; 3840×2160 was requested in the prompt and the returned accepted sources are 1672×941 RGB. Generated-to-delivery fitting is proportional; the exact 16:9 fit leaves one pixel of total horizontal padding. No native 4K detail is claimed. Scene review was performed by the coordinator; no independent review or user acceptance is claimed.

## S001 prompt

```text
Use case: historical-scene
Asset type: full-frame static source image for Paper Detour long film storyboard scene S001.
Input images: Image 1 is an accepted handmade paper/card material and lighting reference only. Image 2 is a second accepted paper-built figure/environment reference only. Do not copy their modern bedroom, modern person, contemporary clothes, rain, wet street, or droplets.
Primary request: establish Edo, Japan, on the night of 30 January 1703. A broad handmade paper diorama shows layered Edo rooftops and a period estate gate at night; a small distant group approaches the gate. Keep people small and secondary. This is an illustrative reconstruction, not an authentic archival image.
Composition/framing: landscape 16:9, full-bleed all four edges, intended for 2560×1440 delivery, requested source target 4K UHD 3840×2160. Broad establishing view with readable depth, low rooftops and gate in the middle distance, figures below the skyline. Keep upper-center region and bottom-center subtitle reserve free of faces and essential story objects; textured background may remain. No lettering.
Style/medium: complete opaque handmade paper and card diorama, physical cutout construction, visible fibers and layered cut edges, folds, slight material irregularities, real volume. Match the accepted references' crafted paper realism, not a smooth digital render.
Lighting/mood: calm winter night, physically motivated warm lantern glow against restrained indigo and charcoal. Bare branches or dark evergreen silhouettes only; no colored autumn foliage, blossoms, snow, rain, or other weather.
Constraints: ordinary low city roofline with no prominent tower, castle keep, pagoda, temple silhouette, or distinctive landmark. No legible Japanese writing, invented crests or seals, text, watermark, border, bars or transparency. No blood, attack, fight, extra props or dramatic events. One static composition, coherent scale and contact shadows.
```

## S002 prompt

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-48fd3cc5-7c30-46fc-b87d-f53b3eb4c622.png` → `S002_v01.png`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S002, continuing the same Edo estate established in Image 1.
Input images: Image 1 is the episode continuity anchor for roofline, gate materials, restrained winter-night color and lighting; change to the storyboard's higher overhead cutaway composition rather than copying its view. Images 2 and 3 are accepted paper/card material references only; do not copy their subjects, modern setting, rain or wet street.
Primary request: at night, show the Akō retainers entering the estate through its gate. This is a non-graphic illustrative reconstruction of the selected narration, not archival evidence.
Composition/framing: landscape 16:9, full-bleed, requested 4K UHD source 3840×2160 for 2560×1440 delivery. High oblique view of the estate gate and a shallow paper-cutaway threshold into a single generalized passage. A dense group of small, armed paper figures moves through the opening into the estate; weapons are visible as simple period blades but no fighting is shown. Keep all figures in the middle band, away from the bottom subtitle reserve and the upper-center accent reserve. Do not expose or invent a detailed room plan.
Style/medium: complete opaque handmade paper/card diorama with visible fibers, layered cut edges, folds, physical volume, grounded contact shadows; preserve the tactile paper-world look of Image 1 and the accepted references.
Lighting/mood: restrained indigo night with a few warm lantern pools, physically coherent and calm.
Constraints: no exact guard count, tactics, injuries, blood, bodies, snow, weather, dialogue, readable Japanese text, invented crests/seals, added props, watermark, border, bars or transparency. No tower, castle keep or pagoda. No modern objects, smooth CGI finish, flat vector art, or photoreal humans.
```

## S003 prompt

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-1fd8327d-baba-43de-af18-96bc495bc64e.png` → `S003_v01.png`. Its continuity reference included the exact selected S002 generated output above.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S003, immediately after S002.
Input images: Image 1 is the episode anchor for the same estate materials and restrained winter-night color. Image 2 is S002 continuity for the same gate, walls, and small paper figures. Images 3 and 4 are accepted handmade-paper material references only. Do not copy modern subjects or rain.
Primary request: the retainers have entered and are searching, but Kira is nowhere to be found. Show the absence through an empty passage and open paper doorways; no picture of Kira.
Composition/framing: landscape 16:9, full-bleed, requested 4K UHD source 3840×2160 for 2560×1440 delivery. Close high-oblique view into a shallow, symbolic paper cutaway of one corridor section. A few small armed paper figures search from the central walkway, looking through two simple open doorways; the visible spaces are empty. This is an illustrative reconstruction, not an exact floor plan or archival image. Keep action in the middle band; preserve the upper-center and lower-center text reserves from faces and essential story objects. The empty space is the visual point.
Style/medium: opaque handmade paper/card diorama with visible fibers, layered edges, folded screens, physical depth, soft contact shadows; retain the established gate/wall materials and figure palette from Images 1 and 2. This is a new direct-cut composition, not an animated continuation.
Lighting/mood: low winter-night lantern pools, restrained indigo and warm amber, coherent single practical light.
Constraints: no invented floor plan, named room, guard count, tactics, fight, injury, blood, snow, weather, readable Japanese lettering, fictional seals or crests, dialogue, extra story props, watermark, border, bars or transparency. No tower/pagoda, modern objects, photoreal people, flat vector art or smooth synthetic finish.
```

## S001 generation attempts

- The first visible selected-scene candidate included a prominent distant tower and was not selected. A subsequent candidate removed the tower but retained vivid foliage that read as autumn; it was not selected. Both are unselected alternatives outside the episode source set.
- S001 v01 is the third visible generation and was accepted after the winter-branch correction. Exact source: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-64cbda5d-639a-4b55-b980-8efe81dae02b.png`.

## Quality, scope and limitations

- The built-in image tool returned below the requested 4K target. The author accepted these three exact static sources because their broad compositions remain legible in 640×360 phone reviews and contain no fine documentary lettering. This decision does not establish suitability for close-ups or detailed scenes; inspect those individually and revise them if required. Do not state that these PNGs are native 2K or 4K.
- Source-image checks for S001–S003 are author reviews against the actual Paper reference files; they are not independent reviews. No user acceptance is claimed.
- Subtitle/phrase composites are not built. Text fit is not accepted by these source-image reviews. Palmier import, scene timing, end-screen images, final export, audio, MP4 QA and publication are not done.

## Batch two prompts (S004–S007)

All were generated with the built-in `image_gen`, with the profile's maximum-quality and 4K UHD 3840×2160 target wording. It returned 1672×941 RGB PNGs. Inputs were the exact files listed here plus the two channel style references where stated; references were used for style/continuity only.

### S004

Reference roles: S001 for Edo estate; S002 for gate/material/color continuity; Paper 004 and 033 for paper style only.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-fef1f9c2-353b-414d-964c-2c07384314bb.png` → `S004_v01.png` (hash in current-selection table). Inspected full frame, proportional 2560×1440 review, phone reduction and detail crop in `Work/scene-image-review-v02/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S004, immediately after the search in S003.
Input images: Image 1 establishes the Edo estate and winter night. Image 2 is the continuity anchor for gate, walls, figure materials and color. Images 3 and 4 are style/material references only; do not copy their modern subjects, rain or wet street.
Primary request: communicate “they need only him” without showing Kira, inventing a likeness, or claiming a specific room.
Composition/framing: landscape 16:9, full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. A reverse wide view from just inside the estate toward the open gate and a single dark passage beyond. The retainers are small paper silhouettes just inside the threshold, gathered toward the empty passage; no target is visible. Clearly different from S001's exterior establishing view and S003's close corridor search. Keep faces and the convergence of figures out of the bottom subtitle band. No accent is planned; keep meaningful gate detail out of the upper-center anyway.
Style/medium: opaque, handmade layered paper/card diorama with visible fibers, cut edges, folds, thickness, natural irregularity and physical contact shadows, consistent with images 1–4.
Lighting/mood: winter night, cool indigo surroundings with a restrained amber gate-light, no weather.
Constraints: no new room layout, dialogue, tactics, exact guard count, injury, blood, corpse, snow, rain, invented crest or seal, readable lettering, watermark, border, black bars, transparency, photoreal humans or smooth CGI finish. One static composition, no camera/character animation.
```

### S005 (selected revision)

Reference roles: initial S005 draft (generated source `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-e1cc9de7-c8c4-4c84-ae35-e4f3ee2c134e.png`) for composition direction; S001 and S004 for continuity; Paper 004 and 033 for style.
The first draft placed shadows in the subtitle field and was rejected. Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-5a6f0f3c-cb85-4996-a6de-aed8673650d2.png` → `S005_v01.png`. Inspected full frame, proportional 2560×1440 review, phone reduction and shadow/detail crop in `Work/scene-image-review-v02/`.

```text
Use case: historical-scene
Asset type: revised full-frame static Paper Detour long-film scene S005.
Input images: Image 1 is the initial S005 visual direction to preserve: low side-on wide courtyard, line of retainers, long joined shadows, open gate, winter night. Change only the composition of the shadows and lower foreground. Images 2–4 are continuity and accepted paper-material references.
Primary request: show the retainers' willingness to risk their own lives as a restrained metaphor without covering the narration subtitle line.
Composition/framing: landscape 16:9, full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Keep the line of small paper figures, warm-lit wall, gate, and indigo night. The long joined shadows must end completely in the middle of the image, above 70% of frame height. Keep the entire bottom 30% as plain, low-detail courtyard ground with no shadows, people, props or meaningful edges, reserved for the one-line subtitles. The figures and all meaningful shadow forms remain well above that reserve. Distinct from the frontal gate view.
Style/medium: opaque handmade layered paper/card diorama, visible fibers and cut edges, folded forms, physical light, dimensional construction and grounded shadows; consistent with the references.
Lighting/mood: quiet indigo winter night; one restrained amber lantern source; no weather.
Constraints: metaphor only, not an added historical event. No falling figures, corpses, wounds, gore, ritual death, blood, combat, dialogue, invented props, room plan, guard count, crests, seals, readable lettering, watermark, border, bars, or transparency. No tower/pagoda, modern objects, photographic people, flat vector art, or smooth synthetic render. One static composition, no animation.
```

### S006 (selected corrected composition)

Reference roles: the second S006 draft `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-6e2a445d-7151-488b-8ee8-ef72ffb7175b.png` for composition and costume colors; Paper 004 and 033 for material style. The first draft `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-18c1ce8c-cc21-4d4c-9517-50d0b0a3db36.png` overemphasized an age contrast and was not selected.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-ab70811a-7483-4c70-a667-37b5f4663efb.png` → `S006_v01.png`. Inspected full frame, proportional 2560×1440 review, phone reduction and character-detail crop in `Work/scene-image-review-v02/`.

```text
Use case: historical-scene
Asset type: subtitle-safe corrected version of Paper Detour long-film scene S006.
Input images: Image 1 is the chosen S006 composition and character-color reference. Preserve the corridor, two similar-age generic paper officials, Asano in muted vermilion with a sheathed short blade, Kira in dark neutral formal clothing, and distant gate in the rear layer. Images 2 and 3 are accepted paper material references.
Primary request: preserve the neutral pre-attack moment where Kira is unarmed and Asano has not drawn his short blade.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 for 2560×1440 delivery. Keep the two standing figures smaller and placed in the central vertical band, with their heads above 35% frame height and their feet fully above 65% frame height. Leave the entire lower 30% as unobstructed, low-detail corridor floor for centered narration subtitles. Do not let any sleeve, sword, foot, shadow, furniture or architectural edge enter this subtitle band. Preserve a readable medium-wide two-shot and the layered rear gate.
Style/medium: opaque handmade paper/card diorama, clearly visible fibers and layered cut edges, folds and physical depth; match the accepted Paper references.
Lighting/mood: subdued warm indoor lamplight, quiet cool background, no dramatic effects.
Constraints: both figures similar apparent age; no grey hair, baldness, wrinkles, scars, facial-hair emphasis or distinctive portrait likeness. No attack, raised sword, injury, blood, dialogue, insult, motive, fabricated lettering/crests/seals, extra people/props, watermark, border, bars or transparency. No photoreal humans, flat vector art or smooth synthetic render. One static full-frame composition.
```

### S007

Reference roles: selected S006 `S006_v01.png` for figure and corridor continuity; Paper 004 and 033 for style/material only.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-73eb1c8c-2081-4241-9c8f-e8dc5114e2ca.png` → `S007_v01.png`. Inspected full frame, proportional 2560×1440 review, phone reduction and blade/hand detail crop in `Work/scene-image-review-v02/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S007, direct cut after S006.
Input images: Image 1 is the accepted S006 character/setting continuity anchor: Asano is the muted-vermilion figure and Kira the dark-neutral official; keep the same generic faces, similar apparent age and paper materials. Images 2 and 3 are accepted paper style references.
Primary request: show Asano making the first attack on Kira with his short sword, in a restrained historical reconstruction.
Composition/framing: landscape 16:9, full-bleed, requested 4K UHD 3840×2160 for 2560×1440 delivery. Medium-wide side angle in the same generalized Edo castle corridor. At one frozen instant Asano has drawn the short blade and directs it toward Kira; Kira steps back with empty hands. Keep both bodies and the action in the middle band; leave the entire lower 30% as low-detail floor for one-line subtitles. No graphic contact or injury. Upper-center is not used for text; keep the action clear.
Style/medium: opaque handmade layered paper/card diorama with visible fibers, folds, cut edges, physical depth and contact shadows, consistent with S006 and accepted Paper references.
Lighting/mood: same subdued amber corridor light with cool outdoor depth beyond the opening.
Constraints: no additional people, restraining official, room plan, dialogue, exact wound, blood, injury, gore, exaggerated emotion, fabricated crest/seal, readable writing, watermark, border, bars or transparency. No extra props or tactics, no portrait likeness, no modern objects, photoreal humans, flat vector art or smooth synthetic render. One static composition, no independent animation.
```


## Batch three prompts (S008–S009)

Built-in `image_gen` returned both selected images at 1672×941 RGB. Prompts requested a 16:9 static Paper Detour diorama and 4K UHD source target; the tool supplied no resolution control. The exact text of the original prompt calls was not retained in the current production record, so the following are scope summaries rather than verbatim prompt transcripts.

### S008

Reference roles: S001 for Edo night palette and paper-world continuity; accepted S006 for Asano/Kira costume continuity; Paper 004 and 033 for paper material only.
Selected output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-79f3a367-b98e-405f-bfe3-a4f7945763fa.png` → `S008_v01.png`; SHA-256 `3146f7aac40ce9e3ee61ec8837ae6724d1197a568a9e92cb21a0ee28622e541a`. Rejected first draft: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-5caada32-53b2-4dbf-80ef-dee2b868fdba.png`, where foreground figures and framing intruded into the lower text reserve. Reviewed full frame, phone reduction and proportional 2560×1440 fit in `Work/scene-image-review-v03/`.

Prompt scope: frame the retainers on the left and a paper-framed earlier Asano/Kira corridor scene on the right, with open upper sky for the “47” accent and an unobstructed lower subtitle field. Keep the tableau symbolic, with no invented cause, writing, heraldry, or graphic violence.

### S009

Reference roles: accepted S008 for Edo night, paper materials and retainer continuity; Paper 004 and 033 for material style only.
Selected output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-09dea3d8-3ace-4ab6-b4ce-5f45ba97aa68.png` → `S009_v01.png`; SHA-256 `03e71ecfe14b93d61784ac8077f72effc60c747322f4cf55822306b4bf0bd607`. Reviewed full frame, phone reduction and proportional 2560×1440 fit in `Work/scene-image-review-v03/`.

Prompt scope: stage retainer silhouettes to the left of a closed gate and a blank open order on a stand. Use the contrast to suggest state judgment without a literal courtroom; include no legible writing, invented seal or crest. Preserve empty upper space for “ПРЕСТУПЛЕНИЕ?” and a plain lower subtitle field.


## Batch four prompt (S010)

Reference roles: accepted S007 for Asano–Kira action and corridor continuity; accepted S008 for Edo paper materials and retainer silhouettes; Paper 004 for material style only.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-d7f877b4-5b01-4b16-8d01-2dbc68408cd7.png` → `S010_v01.png`; SHA-256 `c27f20c47613949e935094f3c5d298ee4e6481bae09c9d11708d60b8e737602b`. Native output is 1672×941 RGB despite the requested 4K UHD target. Inspected the full frame, proportional 2560×1440 fit, 640×360 phone reduction, and action detail in `Work/scene-image-review-v04/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S010, a visual bridge between Asano's attack and the later 47 retainers.
Input images: Image 1 is the accepted S007 Asano–Kira corridor/action continuity reference; preserve the generic paper figures, muted vermilion Asano, dark-neutral Kira, and subdued amber corridor, but make a new wider composition. Image 2 is accepted S008 for Edo paper materials and rōnin silhouette language only. Image 3 is the accepted Paper Detour paper/card material reference only; do not copy its modern subjects.
Primary request: evoke that the story began with two sword blows and later became a story of loyalty, without showing graphic contact or inventing a new event.
Composition/framing: landscape 16:9, full-bleed, requested 4K UHD 3840×2160 for 2560×1440 delivery. Build a readable wide layered-paper tableau: in the middle-right, Asano and Kira face each other in the generalized castle corridor, the short blade visible in Asano's hand but no strike landing; on the middle-left, a quiet group of retainers appears as a separate paper-shadow layer behind the corridor opening, linking the incident to their later choice. Two subtle parallel blade-shaped shadows on the corridor floor can suggest the two blows, but no extra weapon or impact. Keep faces, hands, blade, group and corridor threshold above 68% frame height. Leave the bottom 30% as plain low-detail floor for subtitles. Leave upper-center open and visually calm for the later editor-added accent “ДВА УДАРА”; do not render lettering.
Style/medium: complete opaque handmade paper/card diorama, visible fibers, layered cut edges, folds, physical depth and contact shadows; match the accepted Paper images.
Lighting/mood: subdued amber indoor lamplight against a restrained indigo night beyond the corridor, quiet and solemn.
Constraints: no contact, wound, injury, blood, gore, falling figure, corpse, ritual death, extra people, exact room plan, dialogue, invented motive, fabricated heraldry, seal or readable writing, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI, or independent animation. One static full-frame composition.
```


## Batch five prompt (S011)

Reference roles: S008 for Edo-period paper architecture and palette only; S010 and Paper 004 for material continuity only.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-6a5b6e2d-64ad-4a2c-9cd1-1572b4322fc4.png` → `S011_v01.png`; SHA-256 `876690d9ff87f5cce4adacc15f94543ea2b2c4724ea8b601582e5aa58016e818`. Native output is 1672×941 RGB despite the requested 4K UHD target. Inspected full frame, 640×360 phone reduction, detail crop and proportional 2560×1440 fit in `Work/scene-image-review-v05/`.

The first candidate `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-337a4115-3caa-4ba6-9cca-d477284d89f1.png` kept winter-bare branches and was not selected. A targeted edit added fresh early-spring foliage without blossoms, preserving framing, action, hall and text reserves.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S011, setting up the 1701 ceremony sequence.
Input images: Image 1 is accepted S008 for Edo-period paper architecture and restrained indigo/umber palette only. Image 2 is accepted S010 for Paper Detour material continuity only; do not reuse its attack, figures, or composition. Image 3 is the accepted Paper Detour paper/card style reference only; do not copy its modern subjects.
Primary request: establish that on 21 April 1701 preparations are underway at the shogun's castle for a formal imperial-court reception.
Composition/framing: landscape 16:9, full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Show a broad, generalized Edo castle residence exterior and a visible open passage into a formal reception hall. A few small anonymous paper officials quietly prepare the space with folded screens and simple floor arrangements, without depicting the arriving envoys yet. Keep all faces, figures and meaningful architecture below the upper text area and above the subtitle band; leave upper-center visually calm for editor-added “1701” and leave bottom 30% as plain, low-detail paving/floor. No lettering is rendered.
Style/medium: complete opaque handmade paper and card diorama, visible fibers, layered cut edges, folded architecture, physical depth and grounded contact shadows; match accepted Paper Detour references.
Lighting/mood: clear mild spring daylight in restrained warm umber and indigo; no blossoms, rain, fog, or weather.
Constraints: illustrative generalized reconstruction, not an archival view. No prominent pagoda/tower, no recognizable modern landmark, no banners, invented crests/seals, readable Japanese text, dialogue, specific ceremony objects beyond simple folded screens, extra narrative events, violence, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI finish, or independent animation. One static full-frame composition.
```

Season correction prompt: “Revise this exact Paper Detour scene S011 while preserving its overall composition, camera, people, architecture, paper material, lighting, color palette, dimensions, and clear upper and lower text areas. Correct only the season cues: 21 April should feel like mild spring rather than winter. Replace the large bare tree branches and other barren tree silhouettes with modest fresh early-spring green leaves and small new growth, without blossoms. Keep the same Japanese Edo paper-diorama style and warm daylight. Do not change the officials, screens, hall, floor arrangements, gate, framing, or number of people. Preserve the blank upper sky for an editor-added ‘1701’ accent and the plain bottom 30% subtitle floor. Add no text, heraldry, weather, modern objects, extra props, or events. Opaque full-frame 16:9 handmade layered paper/card diorama.”


## Batch six prompt (S012)

Reference roles: S011 for hall architecture; S006 for Asano's muted-vermilion clothing; Paper 004 for material style.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-3f2a7f43-6e37-4a52-b42d-bd7e3e223921.png` → `S012_v01.png`; SHA-256 `6fd4b7826694686a1463e89a4c5412c46942524bf16b5bc81f5d2150bbde4dd0`. Native output is 1672×941 RGB. Inspected full frame, 640×360 phone reduction, people detail and proportional 2560×1440 fit in `Work/scene-image-review-v06/`.

The first candidate `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-079da478-61c4-4e30-aa5c-9f08b8974890.png` included blossoms and floor seams across the subtitle area; it was not selected. A targeted edit removed blossoms and made the lower floor continuous and low-detail.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S012, continuing directly inside the prepared reception hall.
Input images: Image 1 is the accepted S011 hall and Edo architecture continuity anchor; preserve its folded-screen materials and warm daylight but move the camera inside for a new composition. Image 2 is the accepted S006 character-color reference: Asano is the generic muted-vermilion official, with no portrait likeness. Image 3 is the accepted Paper Detour paper/card style reference only.
Primary request: show the formal reception of imperial-court envoys and identify Asano Nagamori as one participant by his position and muted-vermilion clothing.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Interior wide shot of an Edo formal hall, folded screens in the background. A small group of anonymous court envoys has arrived and faces the shogunate officials; Asano is one of several officials, visible at the side of the group in muted vermilion. Keep people arranged in the middle band with their faces and hands clear at phone size. Keep the bottom 30% as plain, low-detail tatami/floor for centered narration subtitles. No accent is planned; no lettering is rendered.
Style/medium: complete opaque handmade layered paper/card diorama, visible fibers, cut edges, folds, physical depth and grounded contact shadows. Match the accepted S011 and Paper references.
Lighting/mood: calm, formal spring daylight entering from the hall side; warm restrained light with indigo and umber architecture.
Constraints: generic illustrative reconstruction only; no claim to exact floor plan, costume rank, envoy count, personal appearance or a specific historical layout. No readable Japanese writing, invented banners, crests or seals, dialogue, ceremonial objects beyond the folded screens and plain room furnishings, modern objects, violence, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI finish, or independent animation. One static full-frame composition.
```

Correction prompt: “Revise this exact S012 Paper Detour frame, preserving its seven seated generic officials, their arrangement, faces, clothing colors, golden folding screen, interior camera, and overall lighting. Make two precise changes: (1) remove all visible pink/white blossoms from the outdoor view and replace them with restrained fresh green foliage; (2) simplify the foreground subtitle zone so the entire bottom 30% is a continuous low-detail tatami/paper floor, with no dark seams, grid lines, objects, feet, or strong shadows crossing it. Keep the warm handmade layered-paper diorama style and full-bleed 16:9 framing. Preserve Asano as the muted-vermilion figure at far right and the envoys as the opposing group on the left. No text, banners, crests, seals, extra people, new props, or change of pose.”


## Batch seven prompt (S013)

Reference roles: S006 for Asano–Kira identity colors and corridor continuity; S012 for Asano clothing; Paper 004 for material style.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-ad62d447-7716-44e0-81c6-5116ff1b428c.png` → `S013_v01.png`; SHA-256 `8572b7765e4f49858935deed61222aa02885da232061df31a7c1469bae2ba79b`. Native output is 1672×941 RGB. Full frame, phone reduction, people detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v07/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S013, a quiet moment before Asano's attack.
Input images: Image 1 is accepted S006 and defines the generic Asano–Kira faces, muted-vermilion Asano, dark-neutral Kira, and Edo castle corridor continuity. Image 2 is accepted S012 for Asano's role and paper clothing materials. Image 3 is the accepted Paper Detour paper/card style reference only.
Primary request: show Asano Naganori approaching the official Kira Yoshinaka in a generalized corridor at the shogun's castle.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Medium-wide side-angle in a quiet wooden corridor with layered paper doors. Asano, muted vermilion, has taken one measured step toward Kira, who is turned toward him; keep them separated by open floor and use neutral posture, with no attack or visible threat. Keep both faces, hands and bodies centered above 68% frame height; reserve the entire bottom 30% as plain low-detail corridor floor for the one-line subtitles. No accent is planned; no lettering is rendered.
Style/medium: opaque handmade paper/card diorama with visible fibers, folded forms, cut edges, physical depth and soft contact shadows. Match accepted Paper Detour references.
Lighting/mood: warm, restrained indoor spring daylight with cool indigo depth beyond the corridor.
Constraints: generic illustrative reconstruction only, no portrait likeness, invented motive, emotion, dialogue, gesture of conflict, raised or drawn weapon, contact, wound, blood, extra people, exact room plan, banners, invented crest/seal or readable writing, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI finish, or independent animation. One static full-frame composition.
```


## Batch eight prompt (S014)

Reference roles: S013 for Kira's dark-neutral clothing and corridor materials; S012 for folded screens; Paper 004 for paper style.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-34a9b58e-1032-4a9d-a21c-a0ee7898fbb2.png` → `S014_v01.png`; SHA-256 `0da2915a1cb3136313a1b0c5a9d3d632bf632109af6900f6998be87adc97fab3`. Native output is 1672×941 RGB. Full frame, phone reduction, people detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v08/`.

First draft `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-2b063074-a642-42fb-94e9-91abcd539396.png` showed blossoms and strong shadows across the lower floor; it was not selected. The revised frame removes blossoms and leaves the lower floor even.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S014, a separate formal-protocol beat after the reception setup.
Input images: Image 1 is accepted S013 and defines Kira as the dark-neutral official and the Edo corridor paper materials; create a new composition and do not repeat the same two-shot. Image 2 is accepted S012 for interior folded screens and warm hall materials. Image 3 is the accepted Paper Detour paper/card style reference only.
Primary request: show Kira responsible for ceremony protocol, speaking with another official in a calm side exchange.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 for 2560×1440 delivery. Medium side view in a quiet formal corridor adjacent to the reception hall. Kira in dark-neutral robes faces one anonymous official in muted brown; one small open-hand gesture suggests conversation without showing words. Place both figures and hands in the middle band, keep their silhouettes clear at phone size, and leave the full bottom 30% as plain low-detail floor for centered subtitles. No accent is planned; no lettering is rendered.
Style/medium: complete opaque handmade layered paper/card diorama, visible fibers, folded screens, cut edges, physical depth and grounded contact shadows; match accepted Paper references.
Lighting/mood: calm warm spring daylight with subdued amber practical light and indigo depth beyond the corridor.
Constraints: no invented spoken words, dialogue balloons, scroll, protocol chart, writing, crest, seal, court emblem, additional officials, portrait likeness, hidden motive, dramatic gesture, weapons, attack, exact room plan, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI, or independent animation. One static full-frame composition.
```

Correction prompt: “Revise this exact S014 Paper Detour frame while preserving both officials, their poses and clothing, the corridor camera, architecture, folding screen and warm light. Make only two changes: remove all pink/white blossoms visible outdoors and replace them with restrained fresh green foliage; make the entire bottom 30% a uniform low-detail paper floor for subtitles, removing the strong diagonal column shadows and any floor seams. Keep the same dimensions and full-bleed 16:9 composition. Keep Kira as the dark-neutral official using the small open-hand conversational gesture, with the other official in brown listening. No writing, dialogue, extra figures, banners, props, or changes to their faces or poses.”


## Batch nine prompt (S015)

Reference roles: S006 for Asano–Kira appearance and sheathed short blade; S014 for corridor materials; Paper 004 for Paper Detour construction.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-41207873-f913-49f1-8f91-fed0452f3e37.png` → `S015_v01.png`; SHA-256 `b5a387663d3eaed6b86eef9070a055721829d0110a92e55552c79e4897358ead`. Native output is 1672×941 RGB. Full frame, phone reduction, action detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v09/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S015, the instant Asano draws his short blade.
Input images: Image 1 is accepted S006 and establishes Asano's generic face, muted-vermilion clothing, sheathed short blade, Kira's dark-neutral clothing, and corridor. Image 2 is accepted S014 for period corridor architecture. Image 3 is accepted Paper Detour paper/card material reference only.
Primary request: show Asano drawing his short sword while Kira has only just turned toward him, before any strike or contact.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Medium-wide side view down the generalized wooden castle corridor. Asano stands behind and slightly to the left of Kira; his short blade is halfway out of its scabbard, plainly a short sword rather than a long katana. Kira begins to turn toward the movement, hands still lowered and empty. Freeze the moment before attack. Keep heads, hands and blade in the central band, entirely above 68% frame height. Leave the bottom 30% as plain, low-detail corridor floor for centered subtitles. No accent or lettering.
Style/medium: opaque handmade layered paper/card diorama, visible paper fibers, cut edges, folds, physical depth and grounded contact shadows; preserve accepted character palette and Paper Detour texture.
Lighting/mood: restrained warm indoor light, cool indigo depth through one distant opening.
Constraints: no other people, drawn second sword, long sword, strike, contact, injury, blood, gore, fallen person, dramatic expression, added reason or dialogue, exact room plan, writing, invented crest/seal, extra props, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI, or independent animation. One static full-frame composition.
```


## Batch ten prompt (S016)

Reference roles: S015 for same-corridor action continuity; S006 for generic Asano–Kira appearance; Paper 004 for style/material.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-13458492-ec0f-4ce2-9aef-853b6f0ffe3f.png` → `S016_v01.png`; SHA-256 `37b744e7a6a36ae047f358b3b908c4d825ee69dc56afb1fbd24bd55fb9c1ed33`. Native output is 1672×941 RGB. Full frame, phone reduction, action detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v11/`.

First candidate `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-ddf5c6f8-d949-40ae-933d-8c4cb358aa96.png` placed Kira's hand on his abdomen, which implied an unverified wound location; it was not selected.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S016, the non-graphic immediate aftermath of the first blow.
Input images: Image 1 is accepted S015 and defines the same corridor, muted-vermilion Asano, dark-neutral Kira, and short-blade scale. Image 2 is accepted S006 for generic character appearance only. Image 3 is accepted Paper Detour paper/card style reference only.
Primary request: show Kira withdrawing to escape after being wounded, without depicting where or how he was wounded.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Medium-wide side view in the same generalized castle corridor. Kira turns away and steps toward an open side passage, one arm drawn close to his body in a protective, non-specific gesture; his clothing remains intact. Asano is a pace behind with the short blade held down and away; the figures do not touch. Keep both figures, passage and blade above 68% frame height; leave bottom 30% as plain low-detail corridor floor for centered subtitles.
Style/medium: opaque handmade layered paper/card diorama with visible fibers, cut edges, folds, physical depth and grounded contact shadows; preserve accepted Paper Detour palette and character continuity.
Lighting/mood: restrained warm interior light, cool indigo depth at the passage, no dramatic effects.
Constraints: no visible wound, blood, torn clothes, gore, contact, fallen figure, extra guards, specific wound location, exact room plan, tactical detail, dialogue, motive, invented props, written signs, crest, seal, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI, or independent animation. One static full-frame composition.
```

Correction prompt: “Revise this S016 Paper Detour frame while preserving the same corridor, colors, character positions, action direction, and paper style. Remove the gesture that places Kira's hand on his abdomen or any body area. Show him simply turning away and stepping quickly toward the open passage with both hands away from his torso, arms slightly extended for balance; keep his robes intact with no visible wound. Asano remains one pace behind with the short blade lowered and pointed toward the floor. No contact, blood, wound location, additional movement effects, new props, text, or change to the clean lower subtitle floor.”


## Batch eleven prompt (S017)

Reference roles: S015 for Asano–Kira corridor and costume continuity; S016 for the immediate sequence; Paper 004 for material style.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-c0084535-b852-486b-8f6c-29b5467243a4.png` → `S017_v01.png`; SHA-256 `bef5a2428fa7efe0bf53e7bb335b11f202a775bba5d4c6cc4abbea2e8ca6c8b4`. Native output is 1672×941 RGB. Inspected full frame, phone reduction, action detail and proportional 2560×1440 fit in `Work/scene-image-review-v12/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S017, the official restrains Asano before another strike.
Input images: Image 1 is accepted S015 for Asano–Kira faces, costume colors, short blade and corridor. Image 2 is accepted S016 for immediate scene continuity. Image 3 is accepted Paper Detour paper/card style reference only.
Primary request: show Asano attempting a second attack, stopped by a nearby official who restrains his arm.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Medium-wide side angle in the same generalized wooden castle corridor. Asano in muted vermilion has turned back with the short blade angled downward and away from every person; one anonymous nearby official in muted brown holds Asano's forearm and restrains him. Kira in dark-neutral robes is farther away near the open passage, upright and moving out of the scene. Show one frozen non-graphic moment, no contact from the blade. Keep all three faces, hands and blade in the center band and above 68% frame height; the entire bottom 30% is plain low-detail floor for subtitles.
Style/medium: opaque handmade layered paper/card diorama with visible fibers, folded forms, cut edges, physical depth and grounded contact shadows; maintain accepted Paper Detour character palette.
Lighting/mood: restrained warm indoor light with cool indigo at the distant doorway.
Constraints: no blade contact, injury, blood, gore, falling figure, extra guards, invented tactics, dialogue, motive, exact room plan, readable writing, banners, crests, seals, added props, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI or independent animation. One static full-frame composition.
```


## Batch twelve prompt (S018)

Reference roles: S017 for corridor and restrained-official continuity; S016 for Kira's escape; Paper 004 for material style.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-37c06624-5254-420e-b1f0-6b59e317147c.png` → `S018_v01.png`; SHA-256 `8018ce94cfcdac2537a5fc09bf6120b7a420c565703dd887e9ef38301a0a1a67`. Native output is 1672×941 RGB. Full frame, phone reduction, action detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v13/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S018, the brief aftermath in which Kira survives and Asano is arrested.
Input images: Image 1 is accepted S017 and defines the same corridor, generic character faces, Asano's vermilion clothing, Kira's dark-neutral clothing, and the restraining official. Image 2 is accepted S016 for Kira's movement toward a passage. Image 3 is accepted Paper Detour paper/card style reference only.
Primary request: make clear that only moments pass, Kira remains alive, and Asano is taken into custody, without showing injury or inventing arrest details.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Use a broad layered corridor view with two spatially separated actions in one static tableau: Kira stands upright and walks away into a side passage; in the foreground, the same anonymous official from S017 guides Asano away by the forearm. Asano's short blade is no longer raised and points down, away from everyone. No restraints or additional officers. Keep faces, hands, and blade above the lower subtitle reserve; leave the entire bottom 30% as plain low-detail floor.
Style/medium: opaque handmade layered paper/card diorama, visible fibers, cut edges, folded architecture, physical depth and soft contact shadows; preserve accepted Paper Detour character continuity.
Lighting/mood: calm warm corridor light, slightly cooler deeper passage, restrained and solemn.
Constraints: Kira visibly alive and upright; no injury detail, blood, gore, wound, corpse, second attack, exact arrest procedure, cuffs, additional officers, exact room plan, invented dialogue, banners, crests, seals, readable writing, added props, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI or independent animation. One static full-frame composition.
```


## Batch thirteen prompt (S019)

Reference roles: S013 for Asano–Kira character identity; S014 for restrained conversation gesture and corridor materials; Paper 004 for paper style.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-e47e0ebd-cddf-49bc-8c32-37c0004a87a8.png` → `S019_v01.png`; SHA-256 `c492b0d150f3b8b6d9550757ca472bd2931fc8ae048e9973c82a58f012738381`. Native output is 1672×941 RGB. Full frame, phone reduction, people detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v14/`.

First draft `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-05cf65c4-cdca-4ec7-ac69-3f05655cf345.png` gave the speaking gesture to Kira; it was not selected. The corrected version gives the gesture to Asano and leaves Kira listening.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S019, suggesting an eyewitness was nearby when Asano spoke of a recent grievance.
Input images: Image 1 is accepted S013 and establishes the generic Asano–Kira figures and corridor. Image 2 is accepted S014 for a neutral conversation gesture and corridor materials. Image 3 is accepted Paper Detour paper/card style reference only.
Primary request: represent the narration's eyewitness as a quiet anonymous presence in the same general corridor, without inventing what was said or why Asano was offended.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Medium-wide layered corridor composition: Asano in muted vermilion and Kira in dark-neutral robes are in the middle distance facing one another in a restrained conversation posture; an anonymous official stands farther back in the same open corridor, turned toward them as a witness. Do not hide the witness behind a screen or imply secrecy. Keep faces and hands above 68% frame height, with the entire bottom 30% plain low-detail floor reserved for subtitles. No text or accent.
Style/medium: opaque handmade layered paper/card diorama, visible fibers, folds, cut edges, physical depth and grounded contact shadows; preserve accepted character palette.
Lighting/mood: quiet warm indoor daylight with cool indigo through the corridor opening.
Constraints: no dialogue text, quote, scroll, letter, accusation, invented motive, specific insult, fabricated evidence, dramatic emotion, additional figures beyond these three, raised weapon, attack, injury, blood, exact detailed room plan, writing, crest, seal, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI, or independent animation. One static full-frame composition.
```

Correction prompt: “Revise this exact S019 frame while keeping the same three officials, same clothing colors, same corridor, camera, composition, paper style, lighting, and empty bottom subtitle floor. Correct only who appears to be speaking: Asano, the muted-vermilion figure at left, makes the small open-hand conversational gesture; Kira, the dark-neutral figure in the center, listens with both hands lowered and still. Keep the anonymous third official at right standing at a distance as a witness. No dialogue text, visible mouth emphasis, accusation, writing, new props, or change in the witness's position.”


## Batch fourteen prompt (S020)

Reference roles: S019 for paper texture and restrained palette only; S005 for shadow material and clarity; Paper 004 for construction style.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-b0b459e2-1878-4742-8d91-353f040612a8.png` → `S020_v01.png`; SHA-256 `aa3ed5ef5f62e21b9608b1fe12f2cb1a57cf44b8843e5c88a926111b375519ce`. Native output is 1672×941 RGB. Full frame, phone reduction, shadow detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v15/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S020, an abstract metaphor for later stories about bribery and humiliation.
Input images: Image 1 is accepted S019 for Paper Detour paper texture and restrained color only; do not reuse characters or corridor action. Image 2 is accepted S005 for paper shadow material and clarity only. Image 3 is the accepted Paper Detour material reference.
Primary request: suggest that later accounts multiplied around the incident without depicting bribery or humiliation as established fact.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. High oblique still-life of a few plain folded paper layers on a quiet indigo-and-umber surface; two long, soft-edged sword-shaped shadows cross the paper at different angles but do not touch. Keep all forms abstract, with no actual weapons, coins, money, figures, or depicted confrontation. Leave the bottom 30% as an uninterrupted plain floor for subtitles. No accent or lettering.
Style/medium: opaque handmade layered paper/card diorama, visible fibers, cut edges, folds and physical light/shadow; consistent with accepted Paper Detour material.
Lighting/mood: restrained warm side light, reflective and uncertain, no dramatic effects.
Constraints: metaphor only, not a historical event or evidence. No readable text, writing, quote, document seal, crest, research publication, currency, coins, bribe exchange, bowed person, humiliation, dialogue, additional story props, watermark, border, bars or transparency. No photoreal objects, flat vector art, smooth CGI, or independent animation. One static composition.
```


## Batch fifteen prompt (S021)

Reference roles: S020 for blank layered paper and abstract sword-shadow material; S019 for palette; Paper 004 for construction style.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-4c44dde9-13f1-4faa-95d0-fbade4bd9733.png` → `S021_v01.png`; SHA-256 `8c77259d04ff153bcc2245c1dc700c23e43cdfbf16004064a1d563c7caf35fe3`. Native output is 1672×941 RGB. Full frame, phone reduction, paper detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v16/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S021, visualizing the absence of a known motive before shifting to the government's judgment.
Input images: Image 1 is accepted S020 for blank layered paper and abstract sword-shadow material; create a different, closer composition. Image 2 is accepted S019 for subdued indigo and umber palette only. Image 3 is the accepted Paper Detour material reference.
Primary request: show an empty, unanswered center where a definitive cause might be expected, without depicting research or invented evidence.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Close high-oblique view of one large plain folded sheet at the center of a dark umber surface. Two faint sword-shaped shadows stop at the left and right edges of the sheet, leaving its center completely blank. A narrow paper edge points toward a quiet closed gate silhouette at the top distance, suggesting the next shift toward public authority. Do not render any text or marks. Keep the entire bottom 30% as empty low-detail floor for subtitles.
Style/medium: opaque handmade layered paper/card diorama, visible fibers, folds, cut edges, physical depth, and soft natural shadows; consistent with accepted Paper Detour material.
Lighting/mood: balanced soft side light with a quiet unresolved mood, not ominous.
Constraints: metaphor only. No actual sword, book, research article, document, scroll text, seal, crest, official, person, scales, courtroom, quote, writing, invented cause, evidence display, watermark, border, bars or transparency. No photoreal objects, flat vector art, smooth CGI, or independent animation. One static composition.
```


## Batch sixteen prompt (S022)

Reference roles: S015 for Asano figure, costume, and short-blade scale; S012 for formal reception-hall architecture; Paper 004 for material style.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-42c554ed-208f-44c1-9269-ad92b3244158.png` → `S022_v01.png`; SHA-256 `3bf2d4497f09d8c9c27c49250209426aeea2595e195343c5c49a093ece136c60`. Native output is 1672×941 RGB. Full frame, phone reduction, blade/hand detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v17/`.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S022, emphasizing that Asano drew a weapon inside the shogun's castle during a state ceremony.
Input images: Image 1 is accepted S015 for Asano's generic figure, muted-vermilion costume, and short-blade scale. Image 2 is accepted S012 for the formal reception-hall paper architecture and ceremonial screen. Image 3 is accepted Paper Detour paper/card style reference only.
Primary request: place the already established act of drawing Asano's short sword unmistakably within a formal shogunate ceremony space, without adding a new attack or injury.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Wide low side view in a generalized Edo castle hall: Asano in muted vermilion stands near a folded ceremonial screen with the short blade held low after drawing; several small anonymous seated officials are far in the background as a restrained sign of a formal ceremony. The blade does not point at anyone. Keep all figures and blade in the middle band and above 68% frame height; leave bottom 30% as plain low-detail tatami floor for subtitles. No accent, no lettering.
Style/medium: opaque handmade layered paper/card diorama with visible fibers, folds, cut edges, physical depth and grounded contact shadows; preserve accepted Paper Detour materials.
Lighting/mood: calm warm ceremonial indoor light with quiet indigo shadow depth.
Constraints: generalized reconstruction, no claim to exact hall layout or attendee count. No attack, strike, injury, blood, gore, dialogue, banners, invented crests or seals, readable writing, additional props, modern objects, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI, or independent animation. One static full-frame composition.
```


## Batch seventeen prompt (S023)

Reference roles: S007 for Asano-to-Kira action and character colors; S022 for formal ceremony-hall architecture; Paper 004 for paper construction.
Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-4a1c6239-c097-4860-947b-cca1758341ce.png` → `S023_v01.png`; SHA-256 `2042678182715fb8c8ac3702b1ab3148d236b9f9eea98d45cb820771bffc2011`. Native output is 1672×941 RGB. Full frame, 640×360 phone reduction, action detail and proportional 2560×1440 fit inspected in `Work/scene-image-review-v20/`.

Unselected candidates: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-52ab4051-7bef-46c9-9d0b-902464fc8216.png` was too tight and figures intruded into the subtitle band; `exec-51a0a453-5e98-48ad-9a54-dd71a953789c.png` had an extra visible hand; `exec-ab5d9d22-57ae-47c6-a41a-516959a81f23.png` still had a duplicated hand. The selected correction leaves only two visible empty hands on Kira.

```text
Use case: historical-scene
Asset type: full-frame static Paper Detour long-film scene S023, making clear that Kira was unarmed when Asano struck.
Input images: Image 1 is accepted S007 for the exact restrained Asano-to-Kira blade action and character colors; use it for continuity, but create a new closer reverse angle. Image 2 is accepted S022 for the formal ceremony-hall screen and warm interior. Image 3 is accepted Paper Detour paper/card style reference only.
Primary request: show Asano attacking an unarmed Kira, with no graphic contact or injury.
Composition/framing: landscape 16:9 full-bleed, requested 4K UHD 3840×2160 source for 2560×1440 delivery. Medium close side angle in the same formal castle corridor. Kira in dark-neutral robes faces Asano with both hands plainly empty and away from his weapon; Asano in muted vermilion extends the short blade toward him, stopping just short of contact. The formal screen and corridor structure remain visible in the rear. Keep faces, both empty hands, and blade fully visible above 68% frame height; bottom 30% is plain low-detail floor for subtitles. No accent or lettering.
Style/medium: complete opaque handmade layered paper/card diorama, visible fibers, cut edges, folded forms, physical depth and soft contact shadows; preserve accepted Paper Detour character continuity.
Lighting/mood: restrained warm ceremony light, cool indigo shadow depth, no dramatic effects.
Constraints: no contact, wound, blood, gore, torn clothing, fallen figure, extra people, second weapon, invented dialogue, motive, exact room plan, banners, crests, seals, readable writing, added props, watermark, border, bars or transparency. No photoreal humans, flat vector art, smooth CGI, or independent animation. One static full-frame composition.
```

Framing correction: “Revise this S023 frame to keep the same Asano–Kira action, costumes, facial continuity, folded ceremonial screen, paper materials, and warm light, but fix the framing for subtitles. Widen the camera and make both figures smaller so their full bodies and feet fit in the middle band above 65% of frame height. Preserve Asano's short blade extended toward Kira but stopping clearly short of contact. Kira's hands remain empty and open, with a calm backward lean rather than a dramatic surrender pose. Make the entire lower 30% a continuous plain, low-detail corridor floor with no feet, shadows, or objects. Keep both faces, both of Kira's empty hands, and the blade fully visible. No injury, contact, blood, text, additional people, or new objects.”

Anatomy correction: “Revise this image and keep the full composition, Asano's pose and blade, Kira's clothing, corridor, screen, lighting, and empty lower subtitle floor. Fix Kira's anatomy to exactly two arms and two hands: his left hand (on the viewer's left) is open at shoulder height; his right arm hangs naturally down at his side with one visible relaxed hand. Remove all other visible hands or duplicated limbs. Kira stays unarmed and leans back slightly. The blade still stops well short of him. No other changes.”


## Batch eighteen prompt (S024)

The first generation request that explicitly named the ritual was blocked by image-generation safety moderation. No image was produced from that blocked request. Continued with a neutral symbolic composition. The saved text below summarizes the accepted generation and composition edit; it is not claimed as a verbatim tool transcript.

```text
Create one static full-bleed 16:9 Paper Detour historical scene: a closed Edo-period estate gate and a tied blank official order on the ground, as a neutral sign of a same-day ruling. No people, ritual objects, or depiction of self-harm. Place the gate and order in the lower half; leave the upper 35% as quiet open indigo sky for a possible caption. Keep the lower subtitle band simple. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, physical depth and soft contact shadows; match accepted Paper Detour materials and restrained indigo, cream and warm wood palette. Calm daylight. No readable writing, invented seals, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-3dd97df2-5318-41ea-b7c1-7f42701df732.png` → `S024_v01.png`; SHA-256 `4d826f93ff8aa1a7068cc9210b69d479d93b82d2c66b5e3d66d7b98d11468f87`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v21/`.

## Batch nineteen prompt (S025)

Reference roles: accepted S024 and S009 for Edo gate/order continuity; Paper 004 for paper construction.

```text
Create one static full-bleed 16:9 Paper Detour scene showing a restrained symbolic editorial reconstruction of unequal outcomes, not a literal documented view. Across one continuous quiet street, show two separate Edo-period estate entrances: at left, a closed humble gate with a tied blank order before it, suggesting confiscated lands; at right, a separate orderly gate remains open with an undisturbed path beyond, suggesting that Kira is not punished. The contrast should read at phone size. Keep both gates separate and similarly sized. No people, officials, proceedings, readable writing, labels, crests, seals, symbols, or invented details. Leave the lower 30% as continuous low-detail street ground for subtitles. Handmade opaque layered paper/card diorama with fibers, folds, cut edges, physical depth and grounded shadows, matching accepted Paper Detour materials and muted indigo, warm wood, paper cream palette. Cool calm daylight. No watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI, or animation. One static composition.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-2c98725f-5c15-4605-85c9-f2063daa9608.png` → `S025_v01.png`; SHA-256 `2347fad4960197760b75017b7b7ee4495a03e4351bdf5c43266f3663f8c1a7c1`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v22/`.


## Batch twenty prompt (S026)

Reference roles: accepted S024 and S025 for Edo estate gates and palette; Paper 004 for handmade paper construction.

```text
Create one static full-bleed 16:9 Paper Detour scene for the narration about consequences falling on retainers who were absent from the palace corridor. Show a small generalized group of former retainers standing together outside a closed Edo estate gate in quiet profile. The gate is closed and they are outside it; there is no lord or authority figure above them. Their subdued ordinary samurai clothing and sheathed swords suggest status without making them attackers. Use varied restrained postures and small gaps between them to communicate uncertainty and loss of household connection. Do not portray mourning, arrest, violence, poverty, or a specific historical event beyond the accepted narration. No exact headcount or individual portraits. Keep figures above 66% frame height and lower 30% a continuous plain street surface for subtitles. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, physical depth and grounded shadows, matching accepted Paper Detour Edo scenes. Calm overcast daylight, indigo, warm wood, muted robes. No banners, invented crests, legible writing, seals, extra props, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-4d45449d-034f-4ab2-9b95-3eba9f9a5780.png` → `S026_v01.png`; SHA-256 `dbcb846dab09d556ee8056e629bca5a501204597696d2e2959ebff55381524c1`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v23/`.


## Batch twenty-one prompt (S027)

Reference roles: accepted S026 for group and costume continuity, S024 for Edo gate forms, and Paper 004 for paper construction.

```text
Create one static full-bleed landscape 16:9 paper-diorama image for the line «которые даже не присутствовали в дворцовом коридоре». Show the same generalized former retainers from the preceding scene as a small group outside their closed estate gate, seen from a clear high three-quarter angle. Emphasize the distance between their quiet street and a separate, empty palace-corridor world: a narrow simple passage may be visible beyond the distant wall as a visual metaphor, with no people and no identifiable palace design. The retainers are outside and away from it, separated by broad empty space. Keep figures in the middle upper band and lower 30% as uninterrupted low-detail paving for subtitles. No heraldic emblem or identifiable crest; no readable writing, signs, seals, weapons in hands, confrontation, arrest, or dramatic action. Match accepted Paper Detour scenes in muted indigo, warm wood, subdued robes and handmade opaque layered paper/card construction with fibers, folds, cut edges, physical depth and grounded shadows. Calm overcast daylight. No invented historical details, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-f0a5b7f6-40ae-40f4-b3c9-09a9c434756c.png` → `S027_v01.png`; SHA-256 `0238d31de4db466abbf8a06bfbd7d2a72de6e18393feb79837553f1f45c2a1f5`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v24/`.


## Batch twenty-two prompt (S028)

Reference roles: accepted S026 and S027 for retainers, closed gate, costume and material continuity; Paper 004 for paper construction.

```text
Create one static full-bleed 16:9 Paper Detour scene for «Они не нападали на Киру и не нарушали приказов». As a quiet visual statement of restraint, show two generalized former retainers before the same closed Edo estate gate. Medium framing: their postures and hands are clear, faces secondary. Hands hang relaxed and open, away from sword hilts; swords remain fully sheathed. No exposed blade, attack, injury or confrontation. Keep heads, hands, waists and sheathed swords above 66% image height; the lower 30% is one continuous plain street floor. Exact anatomy: two arms and two hands per person. Handmade opaque layered paper/card diorama with fibers, folds, cut edges, physical depth and grounded shadows; accepted Paper Detour materials, subdued Edo robes, indigo/warm wood, cool daylight. No text, crests, seals, banners, invented details, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI, or animation.
```

The first candidate put the figures in the lower subtitle reserve and had them facing each other. Composition edits raised the figures and turned both toward the closed gate; the earlier candidates were not selected.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-560e2b9d-95f9-4c57-a74e-391e14a7a4c7.png` → `S028_v01.png`; SHA-256 `daba0d60f627d9bf6ffa495704c09e7d88518d3121a8c39ffe23ae8b9b39f34c`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v25/`.


## Batch twenty-three prompt (S029)

Reference roles: accepted S026 for the estate architecture and Paper 004 for handmade paper style.

```text
Create one static full-bleed 16:9 Paper Detour frame for «Но за считаные часы потеряли прежнее положение». Show the same Edo estate threshold from a reverse high three-quarter angle after the retainers are gone: the large gate is shut, and the broad foreground approach where people had stood is entirely empty. Let open space and the closed household boundary carry the idea of lost standing. This is a restrained visual metaphor, not a claim about a documented location. No people, human-shaped shadows, belongings, poverty, eviction, arrest, family portraits, signs, heraldic marks, banners, text, or papers. Keep the gate and meaningful architecture above the lower subtitle reserve; leave the lower 30% as a continuous plain low-detail surface. Match accepted Paper Detour Edo architecture, indigo and warm wood palette, handmade opaque layered paper/card diorama with fibers, folds, cut edges, physical depth and soft grounded shadows. Calm cool daylight. No invented floor plan, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-3f9d7a2f-1f6a-407a-8420-fdb53513613f.png` → `S029_v01.png`; SHA-256 `f4b8b95bec6c1ef9cd75efc812bca0c57a0e1605dc90c5529a7e38b379afe5de`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v26/`.


## Batch twenty-four prompt (S030)

Reference roles: accepted S026/S029 for Edo materials and lane palette; Paper 004 for handmade paper construction.

```text
Create one static full-bleed 16:9 Paper Detour scene for «от которого зависело будущее их семей. В Ако сотни людей». Show a quiet Edo-period residential lane in Akō, with modest wooden homes built as layered paper diorama and soft shoji windows. In one or two windows, use only indistinct paper silhouettes suggesting households at home; no readable faces, exact family composition, named characters, or emotional distress. Keep domestic figures and window details small in the upper middle region; lower 30% is a continuous simple street surface for subtitles. No crisis, eviction, poverty, exact resident count, signage, crests, seals, or readable text. Use low ordinary rooflines only, no tall tower, castle keep, pagoda or distinctive landmark. Match Paper Detour handmade opaque paper/card materials, visible fibers, folds, cut edges, physical depth and grounded shadows; muted indigo, warm wood, paper cream, calm daylight. No modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

The first candidate introduced a prominent hilltop castle not required by the scene and not established by the current image brief, so it was rejected. A composition edit removed it and retained low residential roofs.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-bdfb25c0-ecbf-46cf-93f2-62722c7b0b64.png` → `S030_v01.png`; SHA-256 `e6825786ce7ec5a564fd7aefc13aedd4fbdfde8d6e2a953405f40844db06d762`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v27/`.


## Batch twenty-five prompt (S031)

Reference roles: accepted S026 for former retainer silhouettes and S030 for generic Akō residential lane; Paper 004 for paper construction.

```text
Create one static full-bleed 16:9 Paper Detour scene for «внезапно теряют господина, службу и доход. Они становятся ронинами — самураями без хозяина». Show a broad quiet Edo-period lane with ordinary low houses and several small separated groups of former retainers in subdued samurai clothing. They stand or walk apart in different directions, each without a visible lord, banner or gathering leader; swords stay sheathed. Convey a household of service broken into masterless individuals, without hunger, homelessness, eviction, arrest or conflict. Use representative small figures, not an exact count and not a literal visualization of all the hundreds. Keep all figures and shadows above 66% frame height and lower 30% uninterrupted low-detail street for subtitles. No identifiable clan crest, readable signs, invented records, portrait faces or distinctive landmark. Match accepted Paper Detour Edo materials: handmade opaque layered paper/card diorama, visible fibers, folds, cut edges, physical depth and soft contact shadows; quiet daylight, restrained indigo, warm wood, muted robes. No modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

First candidate's figures entered the subtitle reserve and was not selected; a composition edit moved them higher and smaller.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-535c1ed7-4d6c-47da-b0d2-14bb47922043.png` → `S031_v01.png`; SHA-256 `83afdd9fe2d38795b5429233ca06464018d6f5972f4a9dd1dd42f3764ac144e6`. Native output 1671×941 RGB. Proofs: `Work/scene-image-review-v28/`.


## Batch twenty-six prompt (S032)

Reference roles: accepted S026 and S030 for Edo palette; Paper 004 for paper construction. Research boundary: F03 establishes armed resistance as a considered option and states that Ōishi later surrendered the castle; no key-transfer detail is added.

```text
Create one static full-bleed 16:9 Paper Detour frame for «Что делать дальше? Одни предлагают защищать замок с оружием». Depict a generalized quiet council of former retainers in a modest Edo room. Several anonymous men sit around a low table. On it place a simple folded-paper model of a closed gate, one fully sheathed sword laid flat, and a completely blank folded paper, suggesting the options of armed resistance or surrender without showing a decision. This is an illustrative metaphor, not an exact historical meeting, layout or ritual. No one draws or holds a weapon; no aggression. Keep people and table above 66% image height and lower 30% plain low-detail tatami. Handmade opaque layered paper/card diorama, fibers, folds, cut edges, depth and grounded shadows; accepted Paper Detour muted indigo, warm wood and subdued robes. No crest, writing, seals, key, invented dialogue or other historical detail. No blood, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

The first candidate included an unnecessary plant, a blade reading as exposed, and figures/furniture low in frame. A revision removed the plant, made the weapon visibly sheathed, and cleared the subtitle reserve.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-09c3f7cb-6bbb-4fbf-acff-982d53c3832b.png` → `S032_v01.png`; SHA-256 `752d18e417dd6357eb651e0a9b478a816b87503403bf811fb181a23406f026ab`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v29/`.


## Batch twenty-seven prompt (S033)

Reference roles: accepted S032 for the quiet council and room; S026 for generic retainer clothing; Paper 004 for paper materials. F03 supports a range of choices; the scene does not claim a precise private thought or meeting.

```text
Create one static full-bleed 16:9 Paper Detour frame as a quiet symbolic image of samurai considering whether to follow their lord's fate. In a modest Edo room, one anonymous retainer sits alone in the foreground, at respectful distance from a small group around a low table in the background. A wide strip of empty tatami separates the single figure from the group. The lone person is fully clothed, calm, motionless, in three-quarter back view; hands rest on knees. The distant group is quiet and indistinct. This is a restrained metaphor, not a literal meeting or exact historical pose. No ritual, injury, body, physical act, weapon, text, crest, seal or extra prop. Keep all figures/table above 65% frame height and lower 30% plain low-detail floor. Handmade opaque layered paper/card diorama, visible fibers, folds, cut edges, physical depth and soft contact shadows; accepted Paper Detour interior palette, indigo, warm wood, muted robes, dim calm daylight. No modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

The initial candidate had the foreground figure too large and low. A wide composition edit moved all figures into the upper frame and left the bottom subtitle reserve clear.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-5e5f3d6a-e148-4e8a-a716-1357eba02693.png` → `S033_v01.png`; SHA-256 `b65ac26ab4f13a3b3d394bf494c38511ea8571a418f8674a21a28aa8f8ac822a`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v30/`.


## Batch twenty-eight prompt (S034)

Reference roles: accepted S032-S033 for the room, table and retainers; Paper 004 for material construction. F03 supports that an attack was initially pressed; the image is a generalized moment and does not portray a fixed faction.

```text
Create one static full-bleed landscape 16:9 Paper Detour frame for «Но самурай Хорибэ Ясубэй требует другого: убить Киру». Show a generalized early council moment in the same modest Edo room: one anonymous retainer has risen and makes a restrained open-hand gesture toward the empty space at the table while others listen. The speaker is not a portrait likeness; his sword remains sheathed. No map or plan of an actual residence, target, attack or violence. This represents an early proposal only, not a permanent faction or exact documented meeting. Keep hands, faces and weapon above 66% height; lower 30% plain tatami. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, depth and grounded shadows; match accepted S032-S033 room, costumes and indigo/warm wood palette. No writing, crests, seals, banners or added props. No watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-6cd19b60-abb5-4e46-acf0-310997d0f052.png` → `S034_v01.png`; SHA-256 `7226cc87a5a167fd688737dd580ca2908d3397f7dcf256e97162d09030400bed`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v31/`.


## Batch twenty-nine prompt (S035)

Reference roles: accepted S032 for the Edo interior and S029 for gate continuity; Paper 004 for paper construction.

```text
Create one static full-bleed landscape 16:9 Paper Detour scene for «Ведь Асано мёртв, его дом уничтожен, а человек,». Show an empty formal room in an Edo estate, viewed from inside the doorway. A single unoccupied floor cushion sits before a quiet blank alcove; beyond the room, the estate's shut gate is visible through an open screen passage. The empty place and closed threshold symbolize the absent lord and household service ending. This is a restrained metaphor, not a claim that the building was physically demolished. No people, body, belongings, family crest, nameplate, memorial, weapon or readable writing. Keep cushion and gate above the lower subtitle reserve and lower 30% a continuous clean low-detail floor. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, physical depth and grounded shadows; accepted Paper Detour Edo interiors and indigo/warm wood palette; quiet daylight. No extra props, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-762cb2dd-be06-4165-bf13-f8a1d523f3ec.png` → `S035_v01.png`; SHA-256 `29b89de04a533d8fbd07f3bfc5b99b3ca9451b00862ab686aae3f36f7c600808`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v32/`.


## Batch thirty prompt (S036)

Reference roles: accepted S006 for Kira's restrained indigo palette and S030 for generic Edo street; Paper 004 for paper construction. F02 supports that Kira was not punished.

```text
Generate one static landscape 16:9 Paper Detour frame for «с которым он вступил в конфликт, живёт свободно». Show one small anonymous older samurai walking calmly through an open Edo lane in daylight. Use the restrained dark indigo robe palette from accepted Kira, but no portrait likeness. He carries one sheathed sword at his waist, not in his hands. No guard, restraint, pursuer or obstacle. An open path and unhurried walk communicate that the man Asano struck remains free. No specific residence, exact street, crest, sign or landmark. Place the complete figure and soft shadow in the middle band above 65% of frame; lower third plain street paving for subtitles. Handmade opaque layered paper/card diorama with fibers, folds, cut edges, physical depth and grounded shadows; accepted Paper Detour Edo style, muted indigo, warm wood and calm daylight. No text, conflict, injury, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

An image edit aimed at moving the figure higher returned a portrait frame and was rejected for the landscape project. A new wide landscape generation was selected instead.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-8fc8d34c-6a8b-4f09-8c6a-b40d10f6d1e0.png` → `S036_v01.png`; SHA-256 `4261485c71679b8f46192f3012fd6ff8b422cf360f21e973b8f196938aa61222`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v33/`.


## Batch thirty-one prompt (S037)

Reference roles: accepted S032-S034 for council continuity; Paper 004 for paper construction. F03 indicates positions changed over time; this image avoids fixing a permanent faction.

```text
Create one static full-bleed landscape 16:9 Paper Detour frame for «Для Хорибэ оставить эту схватку незавершённой означает принять бесчестье». Show an anonymous retainer in muted brown standing apart at the open threshold of the council room, looking back toward the quiet group around a low table. Still, composed stance, hand loose at his side, sword sheathed; the others remain seated and indistinct. A wide open passage carries the idea of a difficult unresolved choice. This is symbolic and does not claim a literal exit, exact pose or permanent opposing faction. No actual residence plan, target, attack or drawn weapon. Keep figures/shadows above 65% frame height; lower 30% plain tatami. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, physical depth and grounded shadows; accepted Paper Detour interior palette. No readable text, crests, seals, banners, extra objects, modern elements, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-edd89642-a937-45e2-90f4-b72b2d3ce08b.png` → `S037_v01.png`; SHA-256 `98a4028c78b2d352c05eb2cc0d4aa6543a76347d465aa5c75a14cab540a78bea`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v34/`.


## Batch thirty-two prompt (S038)

Reference roles: accepted S032/S034 for council interior and S006 for restrained indigo clothing; Paper 004 for materials. F03 supports Ōishi's leadership; no physical likeness is asserted.

```text
Create one static full-bleed 16:9 Paper Detour frame for «Однако главным среди бывших вассалов остаётся Оиси Кураносукэ». Show a generalized quiet council in the same modest Edo room. One anonymous retainer in restrained indigo sits centrally at the far side of a low table; several former retainers around him are turned toward him, so leadership reads by composition. No portrait likeness or distinctive physical traits for Ōishi. A completely blank folded sheet lies before him; one sword is fully sheathed and set aside. No key or transfer ritual. Keep people/table above 66% of frame height and lower 30% plain tatami. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, physical depth and grounded shadows; accepted Paper Detour muted indigo/warm wood palette. No text, crest, seal, banner, extra prop, aggression or drawn blade. No watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-3e8ca7a7-a687-4ac8-86a8-518a3011e0c0.png` → `S038_v01.png`; SHA-256 `01c8f86f89ffd10f16da9d3b207b184d257563475307fc191306873da929ad99`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v35/`.


## Batch thirty-three prompt (S039)

Reference roles: accepted S034/S038 for council continuity; Paper 004 for paper construction. F03 supports the strategic disagreement; this frame does not assert exact dialogue or expressions.

```text
Create one static full-bleed 16:9 Paper Detour scene for «И он принимает решение, которое возмущает сторонников мести». Show the generalized council at a low table at the moment a course is chosen: the anonymous central indigo-clad leader rests one open hand on a blank folded order; a few supporters on the far side turn their shoulders away or look aside in restrained disagreement; others remain still. Illustrative composition, not exact expressions, dialogue or documented meeting. The order has no marks or seal. No key, attack, weapon drawn or permanent rival faction. Keep hands, paper, faces and sheathed weapons above 66%; lower 30% plain tatami. Match accepted Paper Detour council room, handmade opaque layered paper/card, visible fibers, folds, cut edges, physical depth, grounded shadows, calm interior light. No props beyond table, blank order and sheathed weapon, no text, crests, banners, watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-4e0d0b43-3350-4de0-9b73-d1d8d952ee4a.png` → `S039_v01.png`; SHA-256 `6f08ef7fd5e80434d9388082ef87782fb7c01c4ac453d987b4ac4b219aec2be3`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v36/`.


## Batch thirty-four prompt (S040)

Reference roles: accepted S038/S039 council palette and S024 gate construction; Paper 004 for paper material. F03 supports that Ōishi surrendered the castle; no key-transfer detail is claimed.

```text
Create one static full-bleed landscape 16:9 Paper Detour frame for «Оиси сдаёт замок властям. И отказывается немедленно нападать на Киру». Use a high oblique close view of a low table. A simple folded-paper gate model stands open to an empty path; beside it is a completely blank folded order. One anonymous indigo-clad retainer's open hand rests calmly beside the paper, away from the weapon. A single sword is clearly fully sheathed and laid flat at the far edge. Symbolic illustration, not a documented handover ceremony or exact castle model. No key, drawn blade, authorities or named people. Keep all objects above 65% frame height and lower 30% plain low-detail tatami. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, physical depth and grounded shadows; accepted Paper Detour muted indigo/warm wood palette, quiet interior daylight. No text, crests, seals, extra props, watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-59d9d754-3638-4676-9aec-63c6cbb5ddcb.png` → `S040_v01.png`; SHA-256 `5f1f002ab116592cd34796bff52f146853640b24fad631f15b0e60c2c2770ed1`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v37/`.


## Batch thirty-five prompt (S041)

Reference roles: accepted S038/S039 for council continuity; Paper 004 for material construction.

```text
Create one static full-bleed landscape 16:9 Paper Detour scene for «Для тех, кто требовал битвы, это тяжёлый удар». Show two anonymous retainers in the foreground of the council room after hearing a decision. One has turned partly away; the other lowers his gaze, shoulders still, hands resting openly on thighs. Behind them, council members and a blank folded order on the low table are quiet and distant. Convey disappointment and weight, not anger or violence. No one touches a weapon; any sword remains sheathed and out of focus. Symbolic, not an exact meeting or fixed faction. Keep heads/hands/important objects above 65% frame height and lower 30% plain tatami. Match accepted council construction and muted indigo/warm wood handmade opaque layered paper/card, fibers, folds, cut edges, physical depth and grounded shadows. No text, crest, seal, map, key, extra props, watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI or animation.
```

The first candidate had oversized foreground figures that crossed into the subtitle reserve. A widening/reframing edit reduced them and preserved a clean foreground.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-14196aa9-de86-4d10-8f36-d2be2fff3c71.png` → `S041_v01.png`; SHA-256 `28aba6658d3c73ad31e234f9e62d3e2daad4f9cfcacf2a36ea9bec95c0359c23`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v38/`.


## Batch thirty-six prompt (S042)

Reference roles: accepted S038-S040 for council/gate-model continuity; Paper 004 for paper construction. F03 supports Ōishi's leadership and surrender; no transfer ritual or key is claimed.

```text
Create one static full-bleed landscape 16:9 Paper Detour scene for «Их господин погиб, а его главный советник добровольно отдаёт родовой замок». Show a wide, slightly elevated view of the generalized council room. At the low central table, an open paper gate model and blank folded order remain in view; one place at table is conspicuously empty, while an anonymous indigo-clad leader sits calmly opposite it. Former retainers attend quietly. Symbolic, not exact meeting or handover ritual. No key, crest, readable writing, authority figures or physical destruction. Keep faces/table/model above 66% frame height and lower 30% plain tatami. Handmade opaque layered paper/card diorama, visible fibers, folds, cut edges, depth and grounded shadows; match accepted Paper Detour interior palette, calm daylight. No attack, drawn weapon, extra props, watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-c98d7c6b-1580-4a30-9b32-ad2038b009d1.png` → `S042_v01.png`; SHA-256 `97d618a2d43c96b660e7c27c3c6df1dfd0a11b21e2c6d9da5a982bfe3c4af575`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v39/`.


## Batch thirty-seven prompt (S043)

Reference roles: accepted S040 gate model and Paper 004 for paper materials. F03 states that retainers considered armed resistance; the image represents its challenge to authority without showing a battle or exact palace.

```text
Create one static full-bleed landscape 16:9 Paper Detour frame for «Но вооружённое сопротивление означало бы бросить вызов самому сёгунату —». Make a symbolic paper still life showing the scale of authority: a large anonymous formal government gate and blank wall rise behind a much smaller paper model of the Akō estate gate in the foreground. A fully sheathed sword lies beside the small model. A broad shadow from the larger gate falls across the small gate and sword. No people, battle, officials, banners, crests, identifiable shogun palace or exact architecture; metaphor, not documented place. Keep significant objects above 65% frame height; lower 30% plain low-detail ground. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, physical depth, soft grounded shadows; accepted Paper Detour indigo/warm wood palette, quiet daylight. No text, seals, key, extra props, watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-4e09751d-d596-4188-8cef-4c59b36fd02a.png` → `S043_v01.png`; SHA-256 `c1d7a970065be67695046ea96304597d31b84c5a47c5dd1e15e4925ffa055f68`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v40/`.


## Batch thirty-eight prompt (S044)

Reference roles: accepted S030 domestic lane and S043 authority-shadow metaphor; Paper 004 for materials.

```text
Create one static full-bleed landscape 16:9 Paper Detour scene for «и поставить под удар людей, которых ещё можно спасти». Show a small handmade paper residential lane with modest Edo houses and indistinct household silhouettes safely behind shoji. A large anonymous closed gate at the distant end of the lane is partly visible; its broad architectural shadow visibly extends from that gate over the street and part of the intact homes. This symbolizes households exposed to consequences, not a literal attack or event. No fire, damage, weapons in use, panic, fleeing, exact family identities or headcount. Keep houses/silhouettes above 65% of frame; lower 30% simple low-detail street paving. Match accepted Paper Detour materials, fibers, folds, cut edges, depth and grounded shadows, indigo/warm wood palette and calm light. No castle, tower, signs, crests, writing, officials, extra props, watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI or animation.
```

The first candidate's broad shadow had no clear source. A composition edit added a small anonymous gate at the end of the lane and connected the shadow to it; it did not add harm or damage.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-57bf5e3b-4417-4d61-91f3-caa53c69f66e.png` → `S044_v01.png`; SHA-256 `46b4d049d74891c9a1086b54d614b502fef877ba5ba6ad8aa9fe5a550a9de4e6`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v41/`.


## Batch thirty-nine prompt (S045)

Reference roles: accepted S030 for Edo homes and S036 for the generic indigo-clad retainer; Paper 004 for paper construction. No family identity or specific event is claimed.

```text
Create one static full-bleed landscape 16:9 Paper Detour scene for «Не потому, что ему нечего терять. А потому,». Show one anonymous indigo-clad retainer standing outside a quiet Edo home at dusk, seen from behind at a respectful distance from shoji. Inside one softly lit window, only indistinct household silhouettes are visible; no readable faces, exact family roles or specific count. The retainer is still, fully clothed, hands relaxed, sword sheathed. Suggest personal ties and stakes without claiming a documented family scene. Keep person/window above 65%; lower 30% simple lane for subtitles. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, depth and grounded shadows; accepted Paper Detour S030 home lane, muted indigo/warm wood palette. No distress, argument, goodbye, text, crests, signs, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-e6c8765b-c856-4c6c-8f88-a31cae6f8b07.png` → `S045_v01.png`; SHA-256 `51d6fbf6f6f43d2f5d38c2d8754c3a2720069290853fc38d0018baa20b3640aa`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v42/`.


## Batch forty prompt (S046)

Reference roles: accepted S043/S045 for gate/street materials and the anonymous indigo figure; Paper 004 for paper construction. F03 supports a restoration path; this composition is not a literal map.

```text
Create one static full-bleed landscape 16:9 Paper Detour scene for «что у него ещё есть другой путь». Use a clear high three-quarter view of an Edo paper street that forks into two paths. One path ends at a shut shadowed gate; the other remains open and continues toward an unmarked quiet residence. A single small anonymous indigo-clad retainer stands at the fork, facing the open route. Metaphor for restoration over immediate violence, not literal map or documented route. No weapons in hand, signs, labels, crest, written order or named person. Keep figure/paths above 65%; lower 30% simple low-detail street for subtitles. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, depth and grounded shadows; accepted Paper Detour muted indigo/warm wood palette, gentle dusk light. No castle tower, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-c139ea38-159a-4596-9e33-bdd7e2852290.png` → `S046_v01.png`; SHA-256 `114769e7d5da6046204042b05a03e27250d3f1f84b3fa872fcdcdde66e9a4653`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v43/`.


## Batch forty-one prompt (S047)

Reference roles: accepted S024 gate, S040 blank order, Paper 004 materials. F03-F04 support restoration through Daigaku and the dependency on shogunate action; no exact room or custody condition is depicted.

```text
Create one static full-bleed 16:9 Paper Detour historical scene for «У Асано остался младший брат — Дайгаку. Если сёгунат позволит ему». Symbolic paper still life: a completely blank petition lies between two small unmarked estate-gate models, one closed and one only partly open. Behind a plain translucent shoji screen, one indistinct indigo-clad figure suggests a possible successor without portrait likeness or exact room. Meaning: restoration depends on permission; not a documented petition scene. No crest, seal, readable writing, bars, guards, keys or claim of release. Keep petition, gates and figure above 65% frame height; lower 30% plain low-detail tatami. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, depth and grounded shadows; accepted Paper Detour gate/document materials and indigo/warm wood palette, calm interior light. No extra props, watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI or animation.
```

The first composition put the table into the subtitle area. A framing revision raised the full arrangement and left a clear lower third.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-7c33f325-e8c7-4129-b2cd-e5fd4eb8c67a.png` → `S047_v01.png`; SHA-256 `5affca58cc06625bf52048254e6c5055f1090167a24ff60afc17e89eda72896c`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v44/`.


## Batch forty-two prompt (S048)

Reference roles: accepted S026 retainer group and S047 gate/permission motif; Paper 004 for paper construction. The image must read as a possibility, not an event already completed.

```text
Create one static full-bleed landscape 16:9 Paper Detour frame for «возглавить восстановленный дом Асано, бывшие вассалы смогут сохранить хотя бы». Show a quiet hypothetical restored household: an unmarked Edo estate gate stands partly open toward a modest intact residence; a small representative group of anonymous former retainers waits just outside the threshold, looking in but not yet entering. One warm shoji window suggests a possible future, not a completed event. No exact headcount, family scene, heraldic crest, named character, official or ceremony. Keep people and gate above 65% frame height; lower 30% continuous simple low-detail street for subtitles. Handmade opaque layered paper/card diorama with fibers, folds, cut edges, physical depth and grounded shadows; accepted Paper Detour materials, muted indigo/warm wood, calm late-day light. No text, seals, banners, weapons in hand, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-9b1caac4-f2ee-49da-96f3-41f3f5d674e0.png` → `S048_v01.png`; SHA-256 `3518f4506734b417bc29f9a579f5daa1c1778d5092d1e0e0e9c72960cf76e608`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v45/`.


## Batch forty-three prompt (S049)

Reference roles: accepted S030 domestic lane, S045 retainer/home vignette; Paper 004 for materials.

```text
Create one static full-bleed landscape 16:9 Paper Detour scene for «часть своего прежнего мира. Без нового убийства». Show a quiet hypothetical Edo residential lane at dusk: intact modest homes, one partly open shoji doorway with softly lit room and two indistinct household silhouettes. A single anonymous former retainer in muted indigo stands calmly farther down the lane, hands relaxed and empty; no weapon visible. This represents peaceful life that might be preserved, not actual restoration or documented reunion. Keep people/window above 65% and lower 30% plain low-detail street. Match accepted Paper Detour domestic materials, handmade opaque layered paper/card with fibers, folds, cut edges, depth, grounded shadows, indigo, warm wood and gentle window light. No exact family roles, names, crests, text, distress, conflict, injury, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

The first candidate's figure was too large and close to the subtitle reserve. A reframing edit moved him farther down the street, kept the domestic silhouettes visible and cleared the lower third.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-162a9432-230a-4209-a1ab-bed828a92b57.png` → `S049_v01.png`; SHA-256 `db82549b19c5a844f98433cab15fea3e8ad3f364cf6946c22d6c6b4bcd289206`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v46/`.


## Batch forty-four prompt (S050)

Reference roles: accepted S046 fork and S047 gate models; Paper 004 for construction. F03 notes the options changed over time, so visual camps are temporary and symbolic.

```text
Create one static full-bleed landscape 16:9 Paper Detour scene for «Так у ронинов появляются два лидера и два ответа на один вопрос». Show a single quiet council room from a high three-quarter angle, organized around two alternative paper paths spreading from one central group: one leads toward a small open unmarked home gate, the other toward a closed shadowed gate. Two anonymous retainer silhouettes stand at separate path ends, each with a few others; they are not facing or challenging one another. Temporary strategic differences, not permanent factions or documented layout. No named person, crest, readable text, target, drawn weapons or hostility. Keep figures/routes above 65% of frame; lower 30% plain low-detail tatami. Handmade opaque layered paper/card diorama, visible fibers, folds, cut edges, depth, grounded shadows; accepted Paper Detour muted indigo/warm wood, calm interior light. No extra props, watermark, border, bars, transparency, modern objects, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-a271b0c0-ff05-4943-8d3a-82fbca5cd0c6.png` → `S050_v01.png`; SHA-256 `dfa65bd20c2c8b89e3b1b890b50942447ed931d274d7b1427708bd575713f26c`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v47/`.


## Batch forty-five prompt (S051)

Reference roles: accepted S050 two-route scene and S034 anonymous speaker in brown; Paper 004 for paper construction. F03 supports Horibe's early push for an attack; the image depicts no violence and no permanent faction.

```text
Create one static full-bleed landscape 16:9 Paper Detour frame for «Хорибэ считает, что честь можно вернуть лишь кровью». Do not depict blood or violence. Show one anonymous retainer in muted brown standing foremost on the darker branch of a paper street, facing a closed gate. A few former retainers remain behind him, still and listening. His posture is firm but calm; hands away from his fully sheathed sword. The gate is unmarked; no one beyond it. This symbolizes Horibe's early insistence on revenge, not a literal attack or permanent faction. Keep figures/gate above 65% frame height; lower 30% plain low-detail ground. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, depth and grounded shadows; match accepted Paper Detour S050 paths and muted indigo/warm wood palette. No target, drawn weapon, injury, red stains, text, crest, banner, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

The first candidate's blurred foreground group entered the subtitle area. A reframing edit removed it while preserving the single figure, two routes and closed gate.

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-2cac7892-92cb-42c1-8289-caf903d85946.png` → `S051_v01.png`; SHA-256 `da33e1d25867dcccce203387955d46bf36c09d605d1ade3383be5ee99369dfc5`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v48/`.


## Batch forty-six prompt (S052)

Reference roles: accepted S038/S047 council and blank petition, Paper 004 for paper materials. F03-F04 support the restoration route and changing strategic debate.

```text
Create one static full-bleed landscape 16:9 Paper Detour scene for «Оиси ищет способ спасти род. Их спор становится гонкой со временем». Show a quiet Edo council room at late dusk. An anonymous indigo-clad leader sits at a low table with a blank petition before him; a small unmarked open gate model suggests the restoration path. Several retainers sit in two subdued groups at either side, no confrontation. Long evening light through shoji stretches clear shadows across table and floor, suggesting dwindling time without clock or hourglass. Symbolic, not exact meeting or private thought. Weapons sheathed and out of hands. Keep figures/paper/model above 65%; lower 30% plain tatami. Handmade opaque layered paper/card diorama with visible fibers, folds, cut edges, depth and grounded shadows; accepted council materials, muted indigo/warm wood, soft amber-to-blue dusk. No text, crest, key, clock, hourglass, aggression, modern objects, watermark, border, bars, transparency, photorealism, flat vector, smooth CGI or animation.
```

Selected built-in output: `/Users/diplomat/.codex/generated_images/01a19d48-e006-7330-a916-7a17697abdd2/exec-eb616a81-4ccc-48fd-be04-da5d21ec46cd.png` → `S052_v01.png`; SHA-256 `ae865d7dfc0d977c8745b181f1534a16646ab8d11a2f2bfb1a93a70096e2fc74`. Native output 1672×941 RGB. Proofs: `Work/scene-image-review-v49/`.



## Batch forty-seven prompts (S053–S058)

The selected images were generated with these scene-specific constraints; all prompts requested a single complete static 16:9 handmade layered-paper diorama, visible cut edges/fibers, restrained Edo palette, clear low-detail subtitle field in the lower 30%, and no text, crest, border or animation.

- **S053:** Two separate quiet activities divided by a wooden post: one anonymous indigo-clad retainer at a blank sheet, three anonymous retainers around another completely blank sheet. Parallel discussions only; no map, route, marks, pointing or documented joint meeting.
- **S054:** Anonymous, unarmed retainers across a broad empty public street from a distant generic imposing Edo-period wall and closed gate. No exact residence, floor plan, route, guard count or defense system.
- **S055:** Symbolic possible outcome: deep shadow across an empty approach, warm lantern intact behind generic wall, small unharmed silhouettes paused at shadow edge. No event claim, attack, bodies or injuries.
- **S056:** Anonymous retainers gradually separate along a generic Edo street; no calendar, employer, rejection or exact destination.
- **S057:** Quiet generic council from a high angle, broad empty tatami and cushions, two distant retainers, fading light; symbolic dwindling commitment, no exact meeting count.
- **S058:** Blank opened paper beside a small closed gate model, summer light after dusk; no writing, seal, crest, messenger or invented delivery ritual.


## Batch forty-eight prompts (S059–S060)

- **S059:** Two distinct generic thresholds; an anonymous noble silhouette steps from an open household gate while a larger distant domain gate stays closed. No actual portrait, route, escort, map, writing, seal or insignia.
- **S060:** Three anonymous adult figures travel toward an ordinary open household entrance. A small abstract closed gate model on a raised stand sits entirely above 65% of frame and symbolizes failed restoration. The initial image placed the model in the subtitle band and was rejected; the selected revision raised the model and preserved the lower field.


## Batch forty-nine prompts (S061–S062)

- **S061:** Anonymous indigo-clad leader beside blank sheet and unmarked open gate model; divided light, neutral unreadable face. Private belief is not depicted as known; no historians or research props.
- **S062:** Quiet group at blank sheet, sheathed swords untouched at far wall, one additional figure in doorway. No plan, target, room layout, attack or tactical detail.


## Batch fifty prompts (S063–S069)

- **S063:** One anonymous retainer at a fork with two equally open routes to ordinary houses and an open city street. First draft showed a closed gate and was rejected.
- **S064:** Several figures separated along a peaceful Edo street, representing possible new service/life without showing a specific employer or asserting the possibility occurred.
- **S065:** Figure paused between an ordinary street and a dim council room containing a blank petition and sheathed sword; no oath or exact act.
- **S066:** Loose informal cluster with an indigo leader at equal scale. First draft formed a rigid lineup; second was rejected for subtitle collision; selected version is smaller and informally grouped.
- **S067:** Blank sheet, empty cushions and one distant doorway figure suggest difficulty finding participants; no refusal or exact count.
- **S068:** Sheathed swords and blank paper face a generic closed government gate; possible punishment, no execution.
- **S069:** Anonymous retainer with blank open letter and sheathed sword; indistinct adult silhouettes behind shoji. First close composition crossed the subtitle field; selected wider revision leaves the lower 35% clear.


## Batch fifty-one prompts (S070–S079)

- **S070:** Anonymous writer with brush and blank letter; one indistinct household figure behind shoji.
- **S071:** Plain still-life detail of blank letter, ordinary desk objects and sheathed sword; no special favor object or portrait.
- **S072:** Brown-clad retainer among ordinary equals; central composition rejected because it singled him out.
- **S073:** Editorial trio: blank petition, sheathed sword and small paper group; no exact private motive hierarchy.
- **S074:** Some figures move to an ordinary street while others remain by the open gate; no fixed camps or reasons.
- **S075:** Large uncountable group in layered rows with open center sky for possible `47` overlay; no exact 47-figure arrangement.
- **S076:** Brown/indigo figures and larger group face the same open passage, showing their later shared purpose without rivalry.
- **S077:** Two indigo figures with a slight age/height difference among the group; no face likeness or sentimental action.
- **S078:** Blank petition, closed generic domain gate and waiting retainers as a symbolic earlier preservation effort; no crest, key or plan.
- **S079:** Group led by indigo figure along a broad generic public street; sheathed swords, no target, route or attack details.


## Batch fifty-two prompts (S080–S089)

- **S080:** Reverse view through an empty threshold as a small group walks away; no death/farewell.
- **S081:** Callback to intact blank petition and open gate model; first restoration choice remains meaningful without implying success.
- **S082:** Open model and closed distant gate contrast changed conditions; no route or reconnaissance.
- **S083:** Generic closed wall/gate with guard silhouettes behind shoji only. The first foreground group overlapped the subtitle field and was rejected.
- **S084:** Anonymous official silhouette behind a shoji panel and distant closed gate; no expression or specific knowledge asserted.
- **S085:** Empty partly open gate and vacant street symbolize possible escape.
- **S086:** Generic night gate with the group crossing, sheathed swords, no combat or entry method; sky reserved for date accent.
- **S087:** Broad generic interior with attackers advancing and defenders resisting; blades raised but apart, no injury or choreography.
- **S088:** Open empty spaces and searching figures; no target, hideout or exact room plan.
- **S089:** Single open chamber, group at one side and one empty illuminated cushion; first corridor layout rejected as too specific.


## S115 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S115 | `S115_v01.png` | `5f619622f8e7d5cc9259e206eec2b5d21a6e4eaddd93c9dfe6efe23fb81fe6e2` | **AUTHOR ACCEPTED — 2026-11-03**. Anonymous townspeople in small groups look toward the distant open procession, a visual metaphor for admiration among some contemporaries without implying unanimity or a documented gathering. Full frame, 640×360 phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt and reference provenance: `GENERATION_PROMPTS_v57.md`. |

The selected image is `exec-3699cddd-dbf2-4b24-a56a-9e7f5374710c.png`; another generated candidate was not selected. The generator returned native 1672×941 RGB; it did not provide native 4K detail.


## S116 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S116 | `S116_v01.png` | `ba5c89045005f1ecf52fccf83ba5f4640a73942d0dbb4bfcb026ad5b5861078a` | **AUTHOR ACCEPTED — 2026-11-03**. Paired paper frames hold two readings of one event: open warm light and a long shadow toward a plain closed gate. No attack or victims shown. Full frame, 640×360 phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v58.md`. |


## S117 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S117 | `S117_v01.png` | `9fac4c2c5c66e350aff91a9ce929af6807bacda63f26e3d1476d47bb6231a8ad` | **AUTHOR ACCEPTED — 2026-11-03**. Anonymous silhouettes remain behind a generic lattice; repeated floor shadows suggest waiting without specifying a real room or count. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt and references: `GENERATION_PROMPTS_v59.md`. |


## S118 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S118 | `S118_v01.png` | `5f78201c791f949e8c8cacc467af76a3ff3d328dff42220b005b9a425ff04b58` | **AUTHOR ACCEPTED — 2026-11-03**. A plain folded sheet before a closed gate represents an announced decision without invented writing, seals, recipients or ceremony. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt and references: `GENERATION_PROMPTS_v60.md`. |


## S119 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S119 | `S119_v01.png` | `d20100b3eaf4bbed38ea15a188b7f01ae75912a63bc31d05f8090708fd9e3ca7` | **AUTHOR ACCEPTED — 2026-11-03**. Anonymous figures face a narrow shadowed passage as a symbolic sentence; no ritual, injury, death or exact count is depicted. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v61.md`. |


## S120 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S120 | `S120_v01.png` | `11883d888ee92add2e5f76e7bae50f2c637a0b063b7932b38752e7a1a87455f6` | **AUTHOR ACCEPTED — 2026-11-03**. Broad open doors and a calm empty threshold indicate formal permission without depicting a ritual or venue. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v62.md`. |


## S121 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S121 | `S121_v01.png` | `158d86b9d48a2edd2ec71b7bc1987f7dbda5218fb08cb1a60872d0e40ecb0e96` | **AUTHOR ACCEPTED — 2026-11-03**. Three generic paper silhouettes progressively dissolve into layered shadow as a non-graphic death metaphor. No ritual, bodies or portrait traits. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v63.md`. |


## S122 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S122 | `S122_v01.png` | `678c4111bd954d25f463ef9a3248b988e1d03559d90cf6d1f8cc3d24299858f4` | **AUTHOR ACCEPTED — 2026-11-03**. A small cluster of unmarked memorial stones sits beside one separate marker, without names, exact count or identifiable cemetery. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v64.md`. |


## S123 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S123 | `S123_v01.png` | `060b593023d185f6b6bf7159930ccfdc71792b927c73cb830c5282e4dc5c3141` | **AUTHOR ACCEPTED — 2026-11-03**. One unidentifiable silhouette faces a cluster of blank memorial stones; a connected shadow suggests the cost of fulfilled revenge without depicting another event. Full frame, phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v65.md`. |


## S124 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S124 | `S124_v01.png` | `bac8c570c1606d746a30338c1fbc382be49364b6bcc0ec22f41541f5ec1eed85` | **AUTHOR ACCEPTED — 2026-11-03**. Muted-red Oishi silhouette stands by a closed gate, apart from the distant group; unsupported hanging lanterns were removed. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact initial/edit prompts and references: `GENERATION_PROMPTS_v66.md`. |


## S125 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S125 | `S125_v01.png` | `515f1320750d8f60eda1de48c99cf5ce90baf902a74d0288cac2d58349d09cd6` | **AUTHOR ACCEPTED — 2026-11-03**. Two generic figures stand together at a closed threshold; their joined shadow suggests shared fate without depicting a death act. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v67.md`. |


## S126 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S126 | `S126_v01.png` | `c163689cc3ee2cc63fee84da2a4d296e713778e35235a4c312031286338cfefa` | **AUTHOR ACCEPTED — 2026-11-03**. A blank memorial stone sits before a newly opened empty theatre frame, marking the story's transition into later memory. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v68.md`. |


## S127 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S127 | `S127_v01.png` | `c143b065811965322a37f6644d5c8fc372f735e52b511f6dee6575ea3fea2917` | **AUTHOR ACCEPTED — 2026-11-03**. Three blank media forms—paper theatre, book and screen—represent plays, books and film retellings. Unsupported hanging lanterns were removed. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/edit provenance: `GENERATION_PROMPTS_v69.md`. |


## S128 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S128 | `S128_v01.png` | `95af1811266a76c30b99797c080869394a99d2bad751f17283234138dca37353` | **AUTHOR ACCEPTED — 2026-11-03**. A focused paper puppet stage illustrates the named 1748 play without reproducing a specific production; upper third is quiet for possible year accent. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v70.md`. |


## S129 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S129 | `S129_v01.png` | `58c46c16dde0af56c9f5b74a60b2e41851082c08c868f66d5ed571383ee783a3` | **AUTHOR ACCEPTED — 2026-11-03**. Oversized heroic paper shadows partially cover plain gates and a blank sheet, illustrating how later memory dominates without naming omitted facts. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v71.md`. |


## S130 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S130 | `S130_v01.png` | `36020ecbabd4ddc915322a5c3b243b1ce13d1a08378a2590307536bb8c820a7d` | **AUTHOR ACCEPTED — 2026-11-03**. A theatrical triptych stages waiting, danger as shadows, and memorial stones as the story's sacrifice beat; it is clearly a simplified play image. Full frame, phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v72.md`. |


## S131 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S131 | `S131_v01.png` | `9276f717b1b78685aa9b9fc4475e7854b018c3455af49bcff986c08e54029012` | **AUTHOR ACCEPTED — 2026-11-03**. One theatrical silhouette dominates while a small gate-and-blank-sheet layer remains visible through the curtain. No literal question sign or text. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v73.md`. |


## S132 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S132 | `S132_v01.png` | `a4744cb61314e9ccd5ba6c73113020334226b6dc513aa5c4cf1e0e6f0510e91b` | **AUTHOR ACCEPTED — 2026-11-03**. Almost-closed curtain hides the historical background and leaves one anonymous heroic figure, simplifying the story visually. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v74.md`. |


## S133 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S133 | `S133_v01.png` | `07cefea8fa6a39c24278ce5a8eb40988077c4549c78adbac6a3e34ffa2ae1c09` | **AUTHOR ACCEPTED — 2026-11-03**. A unified theatrical row of anonymous warriors shares a shadow toward blank memorial stones, showing the simplified legend without literal count, attack or ritual. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v75.md`. |


## S134 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S134 | `S134_v01.png` | `fb241ab9b71438c06b5277c9c8c6cb2502de5f0f9831ea98a1fc2c2a4d798c85` | **AUTHOR ACCEPTED — 2026-11-03**. Asano and Kira remain apart across a broad empty corridor; no cause, accusation or attack is shown. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v76.md`. |


## S135 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S135 | `S135_v01.png` | `2ff788611644d2cc9a58f418ede595ab40ea4ed008bb35a427883acac85c0e62` | **AUTHOR ACCEPTED — 2026-11-03**. A back-view Kira silhouette faces an empty corridor; no accusation or evidence is shown. Unsupported lanterns were removed. Full frame, phone reduction, proportional fit and subtitle field inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact initial/edit prompts and references: `GENERATION_PROMPTS_v77.md`. |


## S136 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S136 | `S136_v01.png` | `51c849dfffa9a858ab2efd431acba59a3d7860929f73ed03978e2ea09f11ee0b` | **AUTHOR ACCEPTED — 2026-11-03**. Blank correspondence in foreground and several separate retainer groups in the background; no fabricated letter text or motives. Full frame, phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v57/`. Exact prompt/references: `GENERATION_PROMPTS_v78.md`. |

## S137 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S137 | `S137_v01.png` | `7a02fc5819b0d74d04f739fa72c95aaaa3aa6d3c1a048fcc161c0cc440000269` | **AUTHOR ACCEPTED — 2026-11-03**. Средний широкий план: несколько малых безымянных групп бывших вассалов стоят раздельно у общих ворот и открытого пути. Их расположение различается; кадр показывает общее действие, но не утверждает одинаковый личный мотив. Full frame, phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v58/`; prompt record `GENERATION_PROMPTS_v79.md`. |

## S138 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S138 | `S138_v01.png` | `07cc9264857c114aa8809b4d90eda01dffaf79c13f96f5e1bd0798b285c249ad` | **AUTHOR ACCEPTED — 2026-11-03**. Широкий чуть приподнятый ракурс: безымянная группа идёт по тихой улице к дальним воротам. Оружия и схватки нет; верх оставлен спокойным для отдельного акцента «47». Full frame, phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v58/`; prompt record `GENERATION_PROMPTS_v80.md`. |

## S139 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S139 | `S139_v01.png` | `ecd9b36d73124eef55ee49805c5c2a24680e7ecec52b5dc0f1391a808f254705` | **AUTHOR ACCEPTED — 2026-11-03**. Крупный широкий план: несколько безымянных мемориальных камней в первом плане, за ними — закрытые простые ворота. Число камней не соответствует числу в реплике и ничего не подписано; верх свободен для отдельного акцента «46». Full frame, phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v58/`; prompt record `GENERATION_PROMPTS_v81.md`. |

## S140 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S140 | `S140_v01.png` | `c982e41674e81241add48fd6e06e43e74f540d8b25c0164fb827f28b41e9d2a6` | **AUTHOR ACCEPTED — 2026-11-03**. Широкий симметричный план: безымянный памятный камень перед пустой рамой, похожей на театральный портал. Верх остаётся светлым для отдельного акцента «ВЕРНОСТЬ», а сама сцена не даёт ответа на следующий вопрос. Full frame, phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v58/`; prompt record `GENERATION_PROMPTS_v82.md`. |

## S141 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S141 | `S141_v01.png` | `b17a94ddce351e00f67baa795a5cc2cada299c9fe11792236b6aeb4ddef719d5` | **AUTHOR ACCEPTED — 2026-11-03**. Средний широкий план из глубины помещения: один безымянный безоружный силуэт остановился перед тихим открытым порогом; длинная тень не переходит его. Фигура и тень выше полосы субтитров. Full frame, phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v58/`; prompt record `GENERATION_PROMPTS_v83.md`. |

## S142 selected source — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| S142 | `S142_v01.png` | `92e60733e39e3910e194b8a2efd99e275b7e259c96be981f7d4e8b4afd0ec949` | **AUTHOR ACCEPTED — 2026-11-03**. Широкий фронтальный план: две безоружные безымянные фигуры стоят по краям пустого двора; их длинные тени приближаются к центру, но между ними остаётся зазор. Ни действия, ни победителя. Full frame, phone reduction, proportional fit and subtitle reserve inspected. Native output 1672×941 RGB; proof: `Work/scene-image-review-v58/`; prompt record `GENERATION_PROMPTS_v84.md`. |

## ES01 selected background — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| ES01 | `ES01_v01.png` | `043f4aa51d0af4fa98b38c945c3a36b0bccb9db0116ff255fa3865a1c4e8e517` | **AUTHOR ACCEPTED BACKGROUND — 2026-11-03**. Тихий коридор с видом на сосны вдали; складка чистой приглушённо-красной ткани лежит в центральной полосе, не перекрывая зоны UI. Слева остаётся место для заголовка и нативной подписки; справа — для двух рекомендаций. Full frame and proportional fit inspected; safe-zone overlays are work proofs only, not baked into image. Native output 1672×941 RGB; proof: `Work/scene-image-review-v58/`; prompt record `GENERATION_PROMPTS_v85.md`. Native Studio UI and public rendering not checked. |

## ES02 selected background — 2026-11-03

| Scene | Selected file | SHA-256 | Review / rationale |
|---|---|---|---|
| ES02 | `ES02_v01.png` | `cf16ceba3eef047310b4607225b9f6b3f36672cf2d8075be583f70571618b928` | **AUTHOR ACCEPTED BACKGROUND — 2026-11-03**. Спокойная улица Эдо без снега, в приглушённой холодной палитре; складка той же ткани лежит на низком выступе между зарезервированными UI-зонами. Заголовок и три будущих нативных элемента оставлены на простых участках. Full frame and proportional fit inspected; safe-zone overlays are work proofs only, not baked into image. Native output 1670×941 RGB; proof: `Work/scene-image-review-v58/`; prompt record `GENERATION_PROMPTS_v86.md`. Native Studio UI and public rendering not checked. |

# Scene image generation and review v01

- Channel/profile: Nuviko History; `channels/nuviko_history/brand/VISUAL_PROFILE.md`.
- Requested asset set: 43 static 16:9 scene compositions for a 2560×1440 long film.
- Prompt inventory: `GENERATION_PROMPTS_v01.json`; the first-image prompt is transcribed in the S01 record below. Built-in imagegen used; no explicit tool size/quality controls were available.
- Shared limitations: native results are 1672×941 PNGs, not the requested 2560×1440. Delivery upscaling remains necessary. The exact selected traveler reference is missing; the applied channel-avatar derivative is preserved for traveler identity shots. Images are generated reconstructions, not factual evidence or exact portraits. Author review only; no independent image review.

| Scene | Workspace file | Native size / SHA-256 | Source and review |
|---|---|---|---|
| S01 | `S01_v01.png` | 1672×941 / `d0a62e39470271ebd62bb71a591694b0f6cec520725b9ef74e858a324888ec9f` | Prompt at top of this file. Full frame viewed. Stone room, Fawkes, barrels, lantern searchers read clearly; no blast/smoke/modern object. Face/details and movement crop extrema remain unreviewed. |
| S04 | `S04_v01.png` | 1672×941 / `690278de2f2bd735449bd2dadec51a8f6834402cf0e6d158fed3ed36f15e5d93` | Prompt in `GENERATION_PROMPTS_v01.json`. Full frame viewed. Empty, symmetric chamber with benches and central royal space; suitable for expected opening. No faces/action. Crop/motion not checked. |
| S08 | `S08_v01.png` | 1672×941 / `894d94f1e2160049e8380e31d496a3bf5b3b20b02bbc35c187b9a228a9d09f42` | Prompt in prompt inventory. Full frame viewed. A single seated James I in formal early Stuart dress; expression/face readable, no title or writing. Face/anatomy magnification and motion crop not checked. Episode-only identity anchor for S09. |
| S13 | `S13_v01.png` | 1672×941 / `365776985c73d1c82a92a26e37eecec86075b253ad96eb60e00bf518d0c55030` | Prompt in prompt inventory. Full frame viewed. Catesby centered at a table, companions oriented toward him; his leadership reads. Table sheet has no readable text. Face/hand details and motion crop not checked. Episode-only Catesby continuity anchor. |
| S24 | `S24_v01.png` | 1672×941 / `313def133cbb09e9f0d290acd1f1f8834c87490c24476e70bba8bf60bce377af` | Prompt in prompt inventory. Full frame viewed. Monteagle reads a blank letter; hands/face are clearly framed and letter has no readable text. Magnified hand review and motion crop not checked. Letter/Monteagle continuity anchor. |

## Exact prompt used for S01

“Use case: historical-scene. Asset type: Nuviko History film scene 01, a complete static 16:9 landscape frame intended for a 2560×1440 long video. Create a highly realistic historical reconstruction of a stone room beneath the House of Lords in London, night of November 5, 1605. In the center-safe area, a restrained, wary Englishman in period wool clothing stands near several wooden gunpowder barrels; distant officials carrying lanterns enter through the open stone passage. Wide view from deep inside the room, layered stone architecture, clear readable spatial depth, warm lantern flame against cool dark stone, historically plausible clothing and materials, cinematic naturalism. Show the discovery at the room, not an explosion. No Nuviko traveler in this shot. No fire beyond the lanterns, no smoke, no damage, no modern objects, no text, no readable documents, no labels, no watermark, no border. Keep the man, barrels, doorway, and officials fully inside a crop-safe central area for gentle whole-image motion.”

All images remain `DRAFT` until detail inspection, timing confirmation, actual motion/caption safe-area review and scene selection are complete.

## Selected v01 image set

All four contact sheets were regenerated after the last selected-frame corrections. The SHA-256 and native geometry below identify the exact selected files; each remains a generated historical illustration, and frame/caption-safe review remains open. Native size is 1672×941; delivery upscales to 2560×1440.

| Scene | File | SHA-256 |
|---|---|---|
| S01 | `S01_v01.png` | `d0a62e39470271ebd62bb71a591694b0f6cec520725b9ef74e858a324888ec9f` |
| S02 | `S02_v01.png` | `35c0d555f704defe63122ea38a71162eb740c04275b70e714cc34df44dd1fdb1` |
| S03 | `S03_v01.png` | `c524601200db59f5fa3a9e857d41b5b328b771eec315ddb6de9b4651dde25e7d` |
| S04 | `S04_v01.png` | `690278de2f2bd735449bd2dadec51a8f6834402cf0e6d158fed3ed36f15e5d93` |
| S05 | `S05_v01.png` | `473beacac315368fb6662f503868f56d3e93a96bd690bb5d2aada671d8637393` |
| S06 | `S06_v01.png` | `9343450efec80a5627005b18d0c5e1c4b285d1acbeefd7df5f48abd7c71e7910` |
| S07 | `S07_v01.png` | `c80c483d62daa2e7dc7015ccbf52bc4780972299513f4eabef9308c32d05d07f` |
| S08 | `S08_v01.png` | `894d94f1e2160049e8380e31d496a3bf5b3b20b02bbc35c187b9a228a9d09f42` |
| S09 | `S09_v01.png` | `cda97c9bd87bd9813eee702c6d5bf3c76052343be85c155d525674c506f1d436` |
| S10 | `S10_v01.png` | `e64a2af1962d33462bed1dbe80123b9b64187daaeee08d09691a88a4d9361796` |
| S11 | `S11_v01.png` | `31f5679916b0240d8229697252becde15b23c6b87961a46b13f8fed3f0094e5a` |
| S12 | `S12_v01.png` | `2c1f59a65729031fe75d88967018e3742e9067dc5c0ff6f9161f03352582e8f0` |
| S13 | `S13_v01.png` | `365776985c73d1c82a92a26e37eecec86075b253ad96eb60e00bf518d0c55030` |
| S14 | `S14_v01.png` | `7512fcc36983c27d391dbf594e1170389a9508fdd5bea9c04bef6bdeb8578bd4` |
| S15 | `S15_v01.png` | `fd7ab3027b3971b2ba8c4a008ac5817665e421340de2d3d18faf23de486bafc7` |
| S16 | `S16_v01.png` | `8fd6c06b34f7c3599ab7d335e5e823d06407d92a6390cc8e535e3f14fa33e757` |
| S17 | `S17_v01.png` | `30d03a00dc7fde0438c56b392de2dd9812db467e62dff61b408c377c251a661c` |
| S18 | `S18_v01.png` | `34c9e5584d5829ef7f160a1a5b8da718ebce0ae46eb84ebc4bb5c249a90c6728` |
| S19 | `S19_v01.png` | `c023e1c6fba9153a2938bc8fe969deb553336190d854bd2390887f2a0ed6ebc8` |
| S20 | `S20_v01.png` | `dba62bc1bdb902397a058c35a1b30d04153552628ed6d7b5d914ffa51f4a7b86` |
| S21 | `S21_v01.png` | `02d023a02dbf7bda923cdcb2ea0cbadd246d91c450eb52d5f7dd820c307702fe` |
| S22 | `S22_v01.png` | `3fc7163f261b3d5c91d2182b2eda9fa5a100fc186f1453e32bd3465719430dd0` |
| S23 | `S23_v01.png` | `603d33a8647af308b607b75a144fec8345ad816fd0ba17f6bfdeaabc1da132c4` |
| S24 | `S24_v01.png` | `313def133cbb09e9f0d290acd1f1f8834c87490c24476e70bba8bf60bce377af` |
| S25 | `S25_v01.png` | `7f65cdd7d9516ef5a43df98d128946640087bc2326f4f65d5edafef9bf5453df` |
| S26 | `S26_v01.png` | `dc19510883fe27cd4cc90f172c41fcba4281d58589c52b39abf6be3772ca06d0` |
| S27 | `S27_v01.png` | `9c235e8e2b761312ae9dfceb1035bea907c33d8bd4ef6b93d7681adcd989453f` |
| S28 | `S28_v01.png` | `9f3163882a7516dea3fcfc756efa79be6df4a8db0a7e2bca62c15d82d7e19a87` |
| S29 | `S29_v01.png` | `426f856b6fd8db40c0395d84f7f8783b0a2fb3d2b96bc5abaadc3da390de5062` |
| S30 | `S30_v01.png` | `6965ddedee364040c22b378597c6bba3f019dc0f4569e10556aa367c7a82a173` |
| S31 | `S31_v01.png` | `34527854c59187a18364aade63760f79156677ea90286d8b6397189bbec403c4` |
| S32 | `S32_v01.png` | `8e52c31eec455b98968b881b026c7bfb69112591c8ddd4c24315edef2f4fc69b` |
| S33 | `S33_v01.png` | `a9986b6819977e0594065eedd41e9623520102741130c66b57a9700644b404e7` |
| S34 | `S34_v01.png` | `112447b43d8c2c518f97168c65b26ce89b20177be4ddbc751304691cc457058a` |
| S35 | `S35_v01.png` | `d44f52a9dd3fd6eae4b73081edea9e6db88ce348f98e71030d72f0850951cb3d` |
| S36 | `S36_v01.png` | `7a28e0fa2c6e8b10a5251750975e8f4b44ff89eaf668954104beece925ae22e6` |
| S37 | `S37_v01.png` | `59e336d415953c15aa7cd2f4cb17268c6e99b27a415938d70fe5af97c016dec9` |
| S38 | `S38_v01.png` | `ef96d500e029a90493ccdc8e6e51788021fc48aafeaee717c6fc1aa04e697495` |
| S39 | `S39_v01.png` | `6e390fff43018336b588e929e2781a123476f61861598b6d039f23993dea7016` |
| S40 | `S40_v01.png` | `1e41b45added2376d14928f1220b6fc448abdd205c3c60b34f036ff16b25473f` |
| S41 | `S41_v01.png` | `d4f0cb187ef52000ecae1081305a48786d4608ef55a26a72f95ac0eccd3f91d3` |
| S42 | `S42_v01.png` | `dfa7a801b6ecd92df42d40439061bb55d62f1cd36ca32703e152da84371828d3` |
| S43 | `S43_v01.png` | `8c5f3e8bda03600f784cd8efac1ff53f975172bd495e089eea5b02b1c146423a` |

Contact sheets: `CONTACT_SHEET_01_v01.jpg` through `CONTACT_SHEET_04_v01.jpg`. The 43-image sequence was reviewed for order and broad continuity; exact traveler-anchor source remains unavailable, so traveler appearances use the episode copy of the approved channel-avatar derivative.

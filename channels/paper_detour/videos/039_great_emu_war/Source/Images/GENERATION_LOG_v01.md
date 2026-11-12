# Image generation log v01

Built-in `image_gen` tool used for the accepted opening style/material reference and new static scene. No model ID, seed or size control was returned, so those remain unknown. Each target asked for 3840×2160; every returned PNG must be measured individually.

| Scene | Result | Requested target | Measured native size / format | Style reference | SHA-256 | Review status |
|---|---|---|---|---|---|---|
| S01_v01 | `v01/S01_v01.png` | 3840×2160 landscape | 1672×941 RGB PNG, full-bleed 16:9 fit | Paper004 `paper004_user_38.png`, SHA-256 `238bb11958c8e59224edcd006db060df0bddd0c9e100f795e44eeb537ebdc166` | `99b303464a8412ecfac7dd64e29afe5cae200a7102bf72deb74db8052b3a33fe` | Candidate. Full-frame style/composition seen; magnified hand/face/weapon and motion-path checks remain pending. Not imported. |
| S02_v01 | `v01/S02_v01.png` | 3840×2160 landscape | 1672×941 RGB PNG, full-bleed 16:9 fit | Paper004 plus episode S01 material/identity and dam continuity | `5d9ac12ada22589020ccb029959129dd02833103703e47f0f7c0378c56e386da` | Candidate. Full-frame composition seen; detail/motion-path checks pending. Not imported. |
| S03_v01 | `v01/S03_v01.png` | 3840×2160 landscape | 1672×941 RGB PNG, full-bleed 16:9 fit | Paper004 plus episode S01/S02 dam and environment continuity | `757f8c0c823b42c7c76cb91c34024cad4951f3c8942777e47591f78220157ca4` | Candidate. Full-frame composition seen; detail/motion-path checks pending. Not imported. |
| S04_v01 | `v01/S04_v01.png` | 3840×2160 landscape | 1672×941 RGB PNG, full-bleed 16:9 fit | Paper004 plus episode S02/S03 for soldier, dam, emu and landscape continuity | `31353a1452938133cf6fd0401032be5a689577c9bbe441cae2dbf93c207a6784` | Candidate. Full-frame composition seen; detail/motion-path checks pending. Not imported. |
| S05_v01 | `v01/S05_v01.png` | 3840×2160 landscape | 1672×941 RGB PNG, full-bleed 16:9 fit | Paper004 plus S02–S04 for unit, weapons, dam and flock continuity | `d0b33eb7a0734da2aa6524599cfd306ce600e4430b65a0b64d0d88d014f173b5` | Candidate. Full-frame composition seen; detail/motion-path checks pending. Not imported. |
| S06_v01 | `v01/S06_v01.png` | 3840×2160 landscape | 1672×941 RGB PNG, full-bleed 16:9 fit | Paper004 plus S02/S04/S05 for unit, weapon, dam and flock continuity | `875138b3e57cdba8f34bc7c096d3d96b82f5d43ea3bbf0f2ad272f3c057b0b2f` | Candidate. Full-frame composition seen; hand/mechanism and motion-path checks pending. Not imported. |

Exact prompts: `prompts/S01_v01.md`–`prompts/S06_v01.md`. No motion, captions, crop or upscale has been applied to these source PNGs.

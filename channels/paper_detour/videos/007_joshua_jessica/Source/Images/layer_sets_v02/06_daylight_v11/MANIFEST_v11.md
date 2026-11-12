# Plan 09 — Daylight pause, v11

**Status: PASS — static endpoint package only.** Independent reviewer `/root/review_story_assets` confirmed the t0/t4 recompositions, endpoint edges and contacts. This is a layer-first canonical composite, not an exact extraction from the prior flat master. Motion playback was not rendered or checked.

## Composition and source

- Story beat: Joshua sits left of the compact table, calmly facing the blank laptop; the chair is occupied and he remains in the room.
- BG and MG are byte copies of v09’s ImageGen clean room and Joshua+chair+table+laptop layers. The previous v09 master was used to extract/size the FG plant, but was not edited. The new canonical master is the actual t0 composite of the selected three layers in this folder.
- FG is a mechanical registration of v10’s ImageGen plant/pot/contact-shadow cutout: alpha values `<2` were zeroed; the remaining support bbox `(516,961,922,1527)` was cropped; the crop was proportionally resized with premultiplied-alpha Lanczos from 406×566 to 125×174 px; it was placed at `(765,1203)`. This preserves the plant silhouette and support shadow without warping.
- Layer order: BG → MG → FG. No title or UI was added; laptop screen remains blank.

## Registered layers and motion positions

All import layers are 941×1672 PNGs. Alpha bounds below use Pillow’s half-open `(left, top, right, bottom)` convention.

| Plane | File | Mode/alpha | Strong alpha bbox at t0 | t0 → t4 position |
|---|---|---|---|---|
| BG | `06_daylight_BG_v11_provisional.png` | RGB, opaque | — | `0 → +4 px` |
| MG | `06_daylight_MG_v11_provisional.png` | RGBA, alpha 0–255 | `(24,416,891,1391)` after x=−20 | `−20 → −12 px` |
| FG | `06_daylight_FG_v11_small_pot_plant_shadow.png` | RGBA, alpha 0–255 | `(777,1204,889,1360)` | `0 → +11 px` |

All y offsets are 0. There is no animation zoom or deformation. BG t4 shifts +4 and continues the exposed 4 px left strip with its leftmost column. MG translates on a transparent canvas; FG translates on a transparent canvas. Net horizontal travel over the four-second test is BG +4, MG +8, FG +11 px.

### Endpoint edge bounds

- MG strong bbox at t4 after x=−12: `(32,416,899,1391)`; inclusive rightmost pixel x=898. Soft alpha bbox is `(3,19,915,1672)`. At t0 x=−20, only alpha=1 specks in source columns x=15–19 fall outside the canvas; no alpha≥2 or strong object pixels are clipped.
- FG soft bbox at t0 is `(765,1203,890,1377)`. At t4 +11 it is `(776,1203,901,1377)`, leaving 40 px from the last visible pixel x=900 to the canvas edge x=940. Strong t4 rightmost pixel is x=899.

## Visual checks and limits

- t0 and t4 were inspected full-frame and in lower-right contact crops. Joshua’s gaze stays on the laptop; his near hand remains on the tabletop and his other hand on his lap. Fine finger count and jewelry are not confidently verifiable at this scale; no jewelry stands out.
- Chair feet and table legs meet the floor in both stills. The small FG pot sits on the floor with its shadow touching the surface; its motion still leaves the pot fully in frame and among the right table legs without covering the laptop or Joshua.
- MG and FG alpha were inspected over cyan and light QA backgrounds. MG’s warm contour is visible on contrasting fields; the independent reviewer accepted the composite edges in the daylight stills. The plant edge and soft shadow remain contained after the endpoint shift.
- The static t0 master is byte-identical to the t0 composite. t4 uses only the documented horizontal translations. These checks do not verify continuous playback or motion feel.

## Main files and SHA-256

Selected still-package paths:

- BG: `06_daylight_BG_v11_provisional.png`
- MG: `06_daylight_MG_v11_provisional.png`
- FG: `06_daylight_FG_v11_small_pot_plant_shadow.png`
- Canonical master/t0: `06_daylight_master_v11_layerfirst_provisional.png` (byte-identical to the t0 endpoint below)
- t0: `06_daylight_t0_BG0_MG-20_FG0_v11_provisional.png`
- t4: `06_daylight_t4_BG+4_MG-12_FG+11_v11_provisional.png`

Independent PASS applies to these static recompositions, contacts and the t4 edge review only. It does not confirm continuous motion playback.

| File | SHA-256 |
|---|---|
| `06_daylight_BG_v11_provisional.png` | `720ec2fad026e0585a7feebf6cb50d8d4b5d34e11ccdb9224a201465b63eaff5` |
| `06_daylight_MG_v11_provisional.png` | `f2a0c00894001bb3b4156416a2b02676fd1385803a010c0a4604d383d69e1e07` |
| `06_daylight_FG_v11_small_pot_plant_shadow.png` | `f700853d6621460a9c545973fe48b9883d463c5ab6f138c335f03c2fd7a95550` |
| `06_daylight_master_v11_layerfirst_provisional.png` | `1066de6237ba1fcc4592ecde23fccfd7d5aa89a9a3a84d7a35417ec669ca9590` |
| `06_daylight_t0_BG0_MG-20_FG0_v11_provisional.png` | `1066de6237ba1fcc4592ecde23fccfd7d5aa89a9a3a84d7a35417ec669ca9590` |
| `06_daylight_t4_BG+4_MG-12_FG+11_v11_provisional.png` | `377374754a3aca15acd423eef25e297f0601fc5780444e662701142b0da52f67` |

QA stills over cyan/light backgrounds and t0/t4 lower-right contact crops are retained beside these files. They are diagnostic only. The package is not a rendered or playback-verified shot.

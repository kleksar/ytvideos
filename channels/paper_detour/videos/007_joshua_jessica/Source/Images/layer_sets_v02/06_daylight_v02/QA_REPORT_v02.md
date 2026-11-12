# Plan 09 — daylight — v02 bounded layer-first attempt

**Status: NOT READY — independent review failed. No importable path.** Source reference: `Source/Images/06_daylight_master_v2.png`. The independent reviewer checked the static endpoint images and rejected the motion setup.

## Files and provenance

- [BG clean plate](06_daylight_BG_v02_generated_clean_plate_NOT_READY.png) — opaque RGB, 941×1672; generated with ImageGen from the daylight master. It removes Joshua, laptop and foreground chair/blanket while retaining the room, window and table.
- [MG Joshua/laptop group](06_daylight_MG_v02_reused_source_cutout_NOT_READY.png) — RGBA, 941×1672; copied from the earlier source-cutout diagnostic `../06_daylight/06_daylight_MG_v01_NOT_READY.png`. Strong alpha bounds x=0…934, y=359…1671. This preserves the original person/laptop geometry but has a cropped left/bottom and warm edge fringe; no continuous desk support travels with the group.
- [FG chair/plant](06_daylight_FG_v02_generated_chair_plant_NOT_READY.png) — RGBA, 941×1672; generated with ImageGen from the daylight master. Strong alpha bounds x=0…514, y=1161…1671, leaving 426 px clear on the right. The left/bottom crop is intentional, but red/yellow matte fringe is visible on contrast backgrounds.
- [BG +4 edge-fill](06_daylight_BGplus4_edgefill_v02_NOT_READY.png) — deterministic 4 px shift right; the newly exposed leftmost four columns repeat the edge column.
- [Canonical / t0](06_daylight_t0_BG0_MGminus8_FGminus11_v02_NOT_READY.png)
- [t4 still](06_daylight_t4_BGplus4_MG0_FG0_v02_NOT_READY.png)

All source layers and stills are 941×1672. Z-order is BG → MG → FG. Positions are t0 BG 0/MG −8/FG −11 px; t4 BG +4/MG 0/FG 0 px. Thus each plane has a positive horizontal delta (4/8/11 px). The canonical t0 and t0 still are byte-identical. No video or animation was rendered.

## Current visual check and limitations

The two static composites read as a daylight room with Joshua at the laptop and a chair/plant foreground. The laptop base sits visually on the table in each still. Independent reviewer confirms that t0/t4 recompose from the supplied layers and the three endpoint deltas are +4/+8/+11 px. The set is nevertheless NOT READY for motion: MG has no traveling desk support and slides 4 px relative to the tabletop, while strong red/orange matte contours remain. The reviewer checked static stills only, not playback. The generated BG is a new candidate rather than a pixel-exact extraction from the selected master. Do not promote this set to a canonical master.

ImageGen output provenance: BG `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-33f384a3-1b6a-4d81-80be-5e6aad835c08.png`; FG `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-15ef78e3-be11-4d8c-87b1-6243e0262575.png`. Originals and earlier diagnostics remain untouched.

## SHA-256

| File | SHA-256 |
|---|---|
| BG clean plate | `ce06435515f355bf42f364bd6297645805b25c9ddaab1626dc47088363cf0bab` |
| MG reused cutout | `60e03f075819d0e7cdb921fb7ac5112006d06db3df6814321c8019f27b857fc8` |
| FG chair/plant | `15256ab468f188eeadc02b8e4961d7d8a944ed31723f3072f6c564b5201a762c` |
| t0 static | `e41e68e4293adedbdad2ad3192d5e2afc802aaba1b5343d8a24c522d9921c288` |
| t4 static | `09a4c27102db2dce552db20d32877dfd935fb689f4f332c6c6291a19d46369ac` |

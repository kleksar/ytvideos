# Montage 1080×1920 v02

2026-11-02 correction after the user identified black bars in the Palmier preview. The v01 files had a 1080×1920 canvas while the scene art sat inside a smaller centered rectangle; canvas dimensions alone had hidden the padding.

Each scene still S01–S12 was rebuilt from the exact selected `paper_v01` image listed below, using proportional `cover` sizing, a centered crop to 1080×1920, opaque RGB output, and no generated fill. The source images are 941×1672, so only a minimal horizontal crop is needed. Scene content, color and grain were not edited. `S01_Close.png` is an additional closer crop derived from the selected S01 pair image for the second opening plan; its exact crop rectangle is not recorded here.

| Montage file | Exact source |
|---|---|
| S01.png, S13.png | `paper_v01/S01_v03.png` (S13 copied from S01 for the loop) |
| S02.png | `paper_v01/S02_v01.png` |
| S03.png | `paper_v01/S03_v01.png` |
| S04.png | `paper_v01/S04_v01.png` |
| S05.png | `paper_v01/S05_v01.png` |
| S06.png | `paper_v01/S06_v03.png` |
| S07.png | `paper_v01/S07_v02.png` |
| S08.png | `paper_v01/S08_v01.png` |
| S09.png | `paper_v01/S09_v01.png` |
| S10.png | `paper_v01/S10_v01.png` |
| S11.png | `paper_v01/S11_v02.png` |
| S12.png | `paper_v01/S12_v02.png` |

Verification: `magick identify` reported 1080×1920, 3-channel sRGB for all 13 loop/scene PNGs. S01–S12 were opened and visually inspected full-frame; each reaches all four edges without internal bars, with no obvious framing loss from the minimal crop. S13 is the same file content as S01. The later-added `S01_Close.png` is documented separately above.

2026-11-02 follow-up: v02 stills S01–S12 plus `S01_Close.png` were imported into the Paper Detour 036 project and placed in the separate Timeline 2; S13 remains a file-level loop duplicate and is not used as an extra shot. The original Timeline 1 still uses its earlier v01 images. Timeline 2 is a static review cut; it has not been exported or auditioned. Its 1080×1920 canvas and selected scene files are confirmed in Palmier. User review remains pending before any scene motion.

# Paper Detour 038 — accent PNG generation log v01

> SUPERSEDED FOR PRODUCTION LANGUAGE: nine Cyrillic PNGs are FAIL_LANGUAGE; numeric cues require EN timing/fit review. Historical checks below do not accept Russian text for the English film. See [language correction](../../Production/LANGUAGE_CORRECTION_20261103.md).

**Status:** twelve imagegen text candidates prepared, visually inspected in static scene composites at full frame and 360×203 phone reduction. Coordinator static review only; no independent acceptance. Timing and subtitle interaction remain unverified.

## Method and reference

Each phrase was generated as a transparent PNG with the image-generation tool, using the positive Paper typography reference `channels/paper_detour/videos/038_uss_lincoln_pattaya/Source/Graphics/captions_v01/IRAN-BORN_v01.png`. Exact wording is checked against `DECISION_RECORD_v01.md`. The face/edge/shadow visual style was compared with that reference. No font name is known. The filenames below identify the visible phrase after inspection.

## Provenance and renderer outputs

Source hashes are SHA-256 of the actual files in this directory. Output hashes are from the deterministic caption helper run `captions-v01-preflight-r05`, helper 1.1.0 / canvas 2560×1440. The two final files C11/C12 were found swapped by visible phrase during first scene composites. Their source bytes were swapped under the correct content names (no pixel edits); the final manifest now maps each cue to the matching filename. Run r04 had identical cue output hashes and composites, and r05 reverified the corrected semantic names.

| Cue | Exact visible phrase | Source file | Source SHA-256 | Prepared cue SHA-256 | Scene |
|---|---|---|---|---|---|
| C01 | `ЧУЖАЯ СХВАТКА` | `C01_CHUZHAYA_SKHVATKA_v01.png` | `f32e040abb2e3871f80f28a83fc5bde1c71132616fd893dc951e51abf17d1909` | `bbf180896f751493b343e1a057fb07dc160497bcd999ac377d13bc4f9de54d4a` | S008 |
| C02 | `ПРЕСТУПЛЕНИЕ?` | `C02_PRESTUPLENIE_v01.png` | `06b4a27ce9cbbba581c4fc97dbd2319e0e1b368af05d7f8d5ed7e85db21b45d1` | `f469317c30e84d0f4746466de9dce84b33c5430bfff56738208df58368cc8e92` | S009 |
| C03 | `ДВА УДАРА` | `C03_DVA_UDARA_v01.png` | `2baf2f86865eab84af9d2749af5a4b2bb20e43e3af3af1503e837cbd65dc7290` | `57544dda7ff1b698c1182c23469614608094e6ae8c56bf49546202f12b833633` | S010 |
| C04 | `СЭППУКУ` | `C04_SEPPUKU_v01.png` | `1dfde28da1e576545d32a994e89895c45baeea9c5a6f7daa7f8903c8fea6c54f` | `382faf1a0c52cfeeb31ea3501c57874a72207ca214dcfb539a53c7324c8191ea` | S024 |
| C05 | `БЕЗ ГОСПОДИНА` | `C05_BEZ_GOSPODINA_v01.png` | `1ec8be47f3e2cdd5a96b30179e2f84c1a0fe46a7df81ff816652c01d4619b3e1` | `0514d041dc71786bc0b41e1c1ee80db1c664c9c923fbee8a393697694922fa51` | S031 |
| C06 | `ПОПЫТКА ПРОВАЛИЛАСЬ` | `C06_POPITKA_PROVALILAS_v01.png` | `f0a51d6fcbd4380a7bdcd275508061fd7bf66083243cec91c33e3d81c7dca798` | `9eb5bb12afc1f53222fcf1b38cf27964fff50455e618cabc39a8d0ecd26633f8` | S060 |
| C07 | `47` | `C07_47_v01.png` | `a32d6f166128aaca489e8f4cd2128e7d7bfe8be28d6ef994789e2497448f18c5` | `52802cd6e29cebe7ce18746c9436d6b84cfd004bb1046790b248ea602eeec1c1` | S075 |
| C08 | `МЕСТЬ СВЕРШИЛАСЬ` | `C08_MEST_SVERSHILAS_v01.png` | `3fadf08c8be337d99fb5d6d43b85213745b350d3fe71214a0e6248ca051ae567` | `201bec4f890af314912fc5f251b0cbd1ca9fd48ff6cb3ad167c80085ab4b92c9` | S098 |
| C09 | `46` | `C09_46_v01.png` | `b3d462c28ba650a01c00f63d585a9e107d4915ddbe18284086eff8bfb4a09954` | `3d356f22b910bdea859675ce1630fc9d2e085ab6a8a89171ac8064e735cb3c93` | S104 |
| C10 | `1748` | `C10_1748_v01.png` | `5e21441375390cc38c8a8e780d3e5ea64c167df77ed23850b940c908d1194a08` | `0d34c61a92dd72dfe3beed66f6c1c4f0a4edc2774bbf833f84b43ae523716099` | S128 |
| C11 | `ЦЕНА МЕСТИ` | `C11_TSENA_MESTI_v01.png` | `2874c38fb82ac884ba031e9079a1bc6f23bf47cdf19217a5be10c392651308c9` | `886e481f6c6ab3e060251a8bb81d830b81a85224f06649fc4e8865e7d3864256` | S139 |
| C12 | `БЕЗ ОТВЕТА` | `C12_BEZ_OTVETA_v01.png` | `736bf73d113deb8536d2457f91ac7568584e9bafb53b326f5e42d568b95b3933` | `a48c561d9d61f67d34251df190dd6bb021364a360f39376b84ff0caad3daa3f9` | S140 |

## Acceptance limits

Transparent PNG text, spelling, visual color/edge/shadow, static scene placement, phone-size reduction, and measured geometry were inspected. This is not an independent review. The helper's assigned-pair geometry is `PASS` for all 12 pairs; visible face height is 94 px (C06 measures 89 px from its actual glyph face box, within the shared range). The style is a candidate based on the cited reference, not proof of a named font.

No narration recording exists. No accent was heard, aligned or approved against real speech; cue times in the sheet remain rough estimates, and there are no frame numbers. The subtitle layer is not yet available, so subtitle overlap has not been checked. Camera movement, crop path and transition frames have not been tested. Do not import these as final timed/animated cues or describe them as fully accepted until those checks are complete.

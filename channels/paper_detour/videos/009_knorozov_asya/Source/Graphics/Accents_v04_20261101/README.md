# Paper Detour 009 — title PNGs v04

All six titles are short English editorial accents, not running subtitles. The master PNGs use the Paper Detour hand-cut paper style and the approved warm-cream/orange typography reference. `source/` preserves the generated files; `alpha_trimmed/` removes empty exterior margins and a detached below-1%-alpha speck from the opening asset, keeping a 4 px transparent safety edge. The first `trimmed/` files used an alpha-anywhere crop; their oversized transparent bounds made letters look compressed in Palmier, so they are not used in v04.

| ID | Exact copy | Trimmed asset | Visible PNG bounds | Palmier optical height | Anchor center |
|---:|---|---|---:|---:|---|
| 1 | THE MYSTERY / IN STONE | `alpha_trimmed/01_the_mystery_in_stone.png` | 1588×572 | 0.084 of frame height | 0.50, 0.08 |
| 2 | A KEY TO MAYA / WRITING | `alpha_trimmed/02_a_key_to_maya_writing.png` | 1818×563 | 0.090 | 0.50, 0.13 |
| 3 | THE GLYPHS / COULD SPEAK | `alpha_trimmed/03_the_glyphs_could_speak.png` | 1627×561 | 0.090 | 0.50, 0.08 |
| 4 | A COMPANION, / NOT A CODEBREAKER | `alpha_trimmed/04_a_companion_not_a_codebreaker.png` | 2061×496 | 0.090 | 0.50, 0.13 |
| 5 | COAUTHOR? / ONE STUDENT SAYS | `alpha_trimmed/05_coauthor_one_student_says.png` | 1986×558 | 0.090 | 0.50, 0.13 |
| 6 | FROM PHOTOGRAPH / TO STONE | `alpha_trimmed/06_from_photograph_to_stone.png` | 2086×530 | 0.090 | 0.50, 0.13 |

Primary anchor for cues 2/4/5/6: `(0.50, 0.13)`. Preflighted alternate anchor for cues 1/3: `(0.50, 0.08)`, because the primary zone collides with the monument or page edge. Cue 1 is 6.7% smaller to fit the clear sky pocket; every other title uses `0.090H`. These are the only exceptions in this episode. Palmier width is calculated from source aspect ratio and the 9:16 canvas axes; do not treat normalized width and height as fractions of the same physical side.

Original generated-image filenames and SHA-256:

| ID | Original filename | SHA-256 |
|---:|---|---|
| 1 | `exec-c6be1002-86ef-472f-9488-90d454b47f18.png` | `26f0877d15523f47ce3f4ee1da2f0e61250df89c6d489421a9bde499ea731240` |
| 2 | `exec-8c19cf93-4f0c-4c10-b53c-defbcf26f150.png` | `6f10c03e0847071f99e0d90ee67408b1b721c46bd5e56d6e7fd848f398faaa6f` |
| 3 | `exec-8c9bf2c8-21b1-4b87-808b-26f4f34e4f8a.png` | `88aa2c10c36a5b7d5846c08a4fbc266d9f57c74150b52c08ad624e19bd0c0ea2` |
| 4 | `exec-5d0b04e7-06ce-4b7f-9d28-15b1d122ae93.png` | `e866d42be125e93bd66ebf6a7c4fefc517ddd307bd6967e0cf1cfdb387670397` |
| 5 | `exec-2caa1241-d652-4b85-afaf-00feedce2c5a.png` | `0707f598e37e17f550d3f9300d758359250d94db8480c832f84c6b5bb843ad89` |
| 6 | `exec-fd80b969-0df5-462f-b84e-048d6bade442.png` | `9c7021a60822dd36630df653057a9398488bab4b4b082c3d7dd0c7698e45a36e` |

Preflight composites and the no-title codex check are in `Storyboard/Previews/Accents_v04_20261101/`. These scene composites are review aids, not import assets. v04 Palmier uses the alpha-trimmed transparent title files.

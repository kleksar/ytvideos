# Native YouTube experiment contract — Paper 045 v01

- Channel: Paper Detour (`UCMVfdfaNxV3ZkI3_J3Eejzw`).
- Target video: not created yet. Exact source MP4: `Work/render_visual_v07/previews/edmund_fitzgerald_full_film_en_visual_v07.mp4`; SHA-256 `e2a2ae29688a5737ed85f2323985fe895a12315362007fd2da9212a02364641d`.
- User instruction: Public release and apply an A/B experiment (2026-11-05).
- Type: native `title_thumbnail_pair`, three alternatives.
- A: `What Happened to the Edmund Fitzgerald on Lake Superior?` + approved thumbnail 01 (`52157eda7b64f27cc8829cbd4d4cf04c31ce15fbe0c2d6a1e401e11d16d20a66`).
- B: `The Edmund Fitzgerald’s Last Known Radio Message` + approved thumbnail 02 (`4c5b85a4470d3edd1dae9248120ebed2909bc9c8d534ddd3a50eb61c67e4b20e`).
- C: `Why the Arthur M. Anderson Turned Back into the Storm for the Fitzgerald` + approved thumbnail 03 (`8c700b63d21103f040f44aa83d6673780ea02d4b74d3130d9494a229164fb481`).
- Fixed description during native test: complete Description A (`DESCRIPTION_A_EN_v03.txt`). Description is not an experiment variable.
- Hypothesis: A may attract broad interest in the central disappearance; B focuses on the last known radio message; C focuses on the Anderson’s return to search. These are editorial angles, not performance claims.
- Native platform decision/metric: use YouTube's reported watch-time share and exact outcome. Do not substitute CTR alone. Record the native status and selected winner as returned. If no clear winner, YouTube falls back to first submitted A. Experiments may run up to two weeks.
- Eligibility and actual Studio control must be freshly checked on the exact video before start. Public state, video ownership, Advanced Features eligibility and saved title/thumbnail pairs must be read back after the write.
- State: `authorized_not_started`; blocked because delivery preflight fails on `audible_sync=UNVERIFIED` before upload. No video ID, experiment, or native read-back exists yet.

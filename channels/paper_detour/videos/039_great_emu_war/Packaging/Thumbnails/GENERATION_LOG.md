# 039 — журнал генерации обложек

Каждая запись: дата, концепция, назначение, точный запрос, инструмент и модель
(если известна), входные референсы и их роль, исходник, производные файлы,
статус, проверки, ограничения и необходимые SHA-256. Фиксировать подтверждение
пользователя и результаты теста только после фактического получения.

## 2026-11-03 — A/B package v01 (proposal only)

- Film/version: approved Paper Detour 039 film; review MP4 `Work/subtitles_punctuation_v04/previews/Paper039_EN_review_v03.mp4`. Packaging did not modify narration or video.
- Variant cards and exact generation prompts: `AB_v01/CONCEPTS_AND_PROMPTS.md`.
- Extra High receipts and exact completed decisions: `AB_EXTRA_HIGH_RECEIPTS_20261103.md`.
- Generation tool: image_gen; model/version not exposed. Accepted exact Paper style reference: `channels/paper_detour/Shared/References/Paper/paper004_user_38.png`, used for material/fiber/cut edge/volume/shadow only. Story continuity from `Source/Images/VISUAL_BIBLE_v02.md`.
- A master: `AB_v01/Masters/PD039_AB_v01_A.png`; 1672×941 PNG, SHA-256 `a247a926074c6216c2cac1f7484a2892759735e0d7caa6462350d3e7cb7a610d`. Exact visible phrase `THE FLOCK CLOSES IN`.
- B master: `AB_v01/Masters/PD039_AB_v01_B.png`; 1672×941 PNG, SHA-256 `22b04048fdf7240ba10c82ceea32d6a2a308957463f5ba7408faebdc0cb9e5fc`. Exact visible phrase `ROUGH TERRAIN, FAST BIRDS`.
- C master: `AB_v01/Masters/PD039_AB_v01_C.png`; 1672×941 PNG, SHA-256 `8cb2629d9a8812d5d586affa0de4a42ac65099a39bdd5ab756310804ca1bc6ca`. Exact visible phrase `FARMERS LEFT EXPOSED`.
- Reduced previews were made with `thumbnail_previews.py` at 320×180 and visually inspected. Lettering is legible and correctly spelled. A shows the static dam position with the approaching flock as its focus; B shows the truck/pursuit diagonal with rough track and leaves lower-right open; C shows the farmer and broken fence at mid-frame with open lower-right ground. Pairwise check: A↔B share the military subject but show distinct scenes and hierarchies; A↔C differ by encounter versus aftermath; B↔C differ by pursuit versus farmer consequence. All three pass the pre-generation and actual-image distinction checks. Live YouTube card and actual duration overlay were not inspected; safe-corner composition was reserved in B and C and does not prove actual platform rendering.
- Editorial status: proposed; user has not accepted any title or cover. Upload, test launch and other YouTube mutations: not requested. Full long-film A/B package remains subject to the project's additional description requirement and separate user acceptance.

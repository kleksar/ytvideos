## Experimental rewrite A/B — no inherited approval

Root EN/RU scripts now B; untouched A copies: `experiment/baseline.script.en.txt` and `baseline.script.ru.txt`; original HEAD `87cd28b76a4623a50ec7550f5e329bfae3c91caf`. Storyboard descriptions of launch/rope mechanics updated, plus narration in both languages. The original ~70s scene grid is not valid audio for B. Run genuine independent cold reader and exact-voice checks after selecting B; do not reuse a previous script receipt or assume the Wikipedia essay can detect authorship. No media production authorized. [Full experiment](experiment/README.md).

## Актуализация под текущие production gates

Сверено с remote `main` `96c8fa1573c02e8e7987e272a569bf34f037691e`. Этот текстовый сюжетный пакет создан как preproduction и сам **не является `ytv start` run**. Его `storyboard.json` — предварительная постановка, а не отдельный completed stage; авторское чтение и семантический ring не означают `awaiting_script_approval`.

После выбора этой истории запустить в локальной среде `uv run ytv start --channel paper_detour --format short --intent 'Проверить неутверждённый сюжет PR #25'`, прочитать `plan_summary`, `read_next` и pinned task documents. В task `research` сохранить verified claims, а в `script` выполнить действительный independent reader (`sessions.independent` / доступный host), проверить полный EN дважды и получить оригинальный `ytv-script-review-v1` с exact script hash. Недоступность reviewer — UNVERIFIED и закрытый script gate; пользовательский script approval нужен до медиа. [Workflow](https://github.com/kleksar/ytvideos/blob/main/docs/workflow.md) · [contract](https://github.com/kleksar/ytvideos/blob/main/docs/operations/task-contract.md).

RU — редакторская копия английского voice master, не отдельный TTS. Source reference файлы/rights, реальные картинки и длительность, AV-петля и результаты YouTube не проверялись. Не допускать подделки reviewer/approval/receipt и не переносить автоматически pins старых выпусков.

---
# Handoff — text-only new Paper Detour Short

**Remote main SHA checked twice before write:** `96c8fa1573c02e8e7987e272a569bf34f037691e`, tree `a2d08903183e88f5c8b9870cd01ea39bc56f98cb`.
**Channel from freshly read channel.json:** `paper_detour`, active, English, illustrated paper recipe; Short 9:16, 1440×2560 @30 FPS. No new video stage or official ytv runtime run launched: this specific scheduled task authorizes queued text-only preproduction, not video production.

**File map:** research.md (10 actual screened topics, 3 distinct finalists, evidence, audience signals and uncertainty); script.en.txt (203 exact English words, source of any future Lawrence TTS/SRT only after approval); script.ru.txt (full human-readable owner translation); story-review.md (authorial audience/logic/claims, literal last two/first two paragraphs in both languages, independent status UNVERIFIED); storyboard.json (14 provisional text-only unique scene/loop entries, ~70 seconds unmeasured target); packaging-brief.md (3 text concepts); README.md (index).

**Needs first:** actual independent cold English reader on exact script (opening separately, then full reading, then full script twice for seam), then independent bilingual RU/EN review, then exact owner script version approval. No reviewer available here; do not treat author's evaluation as independence. The locally trusted `ytv start` runtime/hashes must be used when future production is expressly authorized, not guessed by this external GitHub branch. `max_paid_units = 0` from current channel config; no paid calls used.

**Art guardrails:** 14 proposed compositions at 4–6 seconds, real speech timing not measured, last S014 reuses **exact S001 image** and camera pose. Each unique image is one full-frame 3D tactile layered paper diorama; no parallax, masks or external paper border; whole-frame zoom/pan only, direct cuts. Historical 1982 California and woven aluminum chair must be researched against actual museum object reference when producing; no photo of a fake reenactment presented as archival. The paper-plane channel Easter egg goes only in S013 on museum brochure, clearly nonhistorical, check accepted asset hash, not hidden by subtitles.

**Fact cautions:** about 16,000 ft, 42 balloons, Larry in chair, losing gun, dumping water ballast, landing on Long Beach power lines, fine, chair gifted to a neighborhood child then donated to Smithsonian. Actual exact intended altitude, exact route at LAX, literal cockpit radio quote, power-outage length, 2026 public museum exhibition status are NOT verified, and should not be invented.

**After exact approval only:** real English TTS with Lawrence at final 1.1 speed once; measure waveform and retime scenes (no fixed implied 70s), generate AI images and thumbnails, SRT/captions, original music rights, full audio-video continuity QA, exact MP4 review and independently instructed YouTube upload/scheduling. Any merge alone does not authorize these actions.

**Safety and ownership:** all contents are new files beneath this story folder. No common docs, skills, statuses, other branches, PRs or Issues were modified. No production, TTS, image generation, render, publication, upload, merge or actual asset downloads occurred.

## Актуальный workflow — remote main

Сверено с `main` `96c8fa1573c02e8e7987e272a569bf34f037691e`. Этот старый текстовый сюжетный PR не является сохранённым `ytv start` run. Существующий `storyboard.json` — предварительная задумка, не выполненный stage; авторская оценка и текстовое кольцо сами по себе не дают `awaiting_script_approval`.

При отборе этого кандидата локально начать с `uv run ytv start --channel paper_detour --format short --intent 'Проверить неутверждённый сюжет PR #21'`, читать `plan_summary`/`read_next` и task context. Зарегистрировать фактические research/script outputs, провести независимый просмотр точного EN целиком дважды (с отдельной проверкой кольца), получить оригинальный `ytv-script-review-v1` с session evidence и script SHA-256, пройти `awaiting_script_approval`; подлинное решение владельца требуется до TTS/изображений/MP4. См. [workflow](https://github.com/kleksar/ytvideos/blob/main/docs/workflow.md) и [contract](https://github.com/kleksar/ytvideos/blob/main/docs/operations/task-contract.md).

RU текст остаётся редакторским переводом, не source для английской озвучки. Никаких fake approvals, reviewer sessions, actual TTS durations или AV-loop PASS; ранние camera/scene briefs служат только отбору и планированию.

---
# Local agent handoff — Paper Detour / Clever Hans (1904)

**Status:** one new candidate story packet in a Draft PR, not an approved script or a registered `ytvideos` production run. **Main base observed 2026-11-13:** `50bb35ecd4ad2e832be5451fd2fa909794f047ed`. Update this after creating PR if fresh main differs. All media/TTS/release operations forbidden in this assignment.

## Files and source identities

- `research.md`: candidate screening (10 separate actual events, three finalists), competitor/interest observations, exact verified sources and uncertainty.
- `script.en.txt`: 190-word English exact proposed narration for any later voice/SRT task; **nothing is recorded yet**.
- `script.ru.txt`: complete corresponding Russian owner reading text, not a second voice track.
- `story-review.md`: authorial verdict on **start / stay / payoff / accuracy / loop** with independent reviewer UNVERIFIED and explicit challenge questions.
- `storyboard.json`: 13 provisional S-IDs, exact EN and RU scripts per shot, ~5 seconds each (65 seconds arithmetic grid, not measured narration); 12 unique planned complete-frame paper images and S013 reusing S001. AI scene prompts are independent and self-contained. This is not an official completed storyboard stage.
- `packaging-brief.md`: three truthful title/thumbnail strategies for Paper's physical lettering.

## Specific narrative shape, not to break

- EN first words: `What's three plus five?` The visual paper horse taps eight times.
- The independent information changes are: trainer not required; **examiner's knowledge** required; **visibility of examiner** required; examiner's tiny **involuntary head movement** detected; finally Pfungst himself replicates horse's feat by reading humans.
- EN final words: `It was inside the head of whoever asked...` → next repeat begins `What's three plus five?`; RU equivalents similarly `кто спрашивал...` → `Сколько будет три плюс пять?`.
- S013 must use the exact same approved **S001 full-frame generated image** and return to the opening crop/scale/translation. Rendering is necessary to prove an actual AV loop. User explicitly wants meaningful Shorts loops after full payoff; this draft explicitly provides a syntactic and semantic join.
- Avoid changing `no obvious trick` into `proved a calculating horse`, `unintentional head signals` into `owner deliberately cheated`, or `tiny head jerk` into `mind reading`.
- Source [Pfungst monograph](https://www.gutenberg.org/cache/epub/33936/pg33936-images.html): experimental series in 1904, German book 1907, English 1911; chapter II unknown-answer and big-blinder testing, chapter IV role reversal and human hand taps. `3+5` is an illustrative sum, not a verbatim documented dated incident.
- S007 has exactly one [paper-plane traveler](../../../channels/paper_detour/brand/PAPER_PLANE.md), as a background branding play in the physical paper diorama—not a historically active aircraft. Before generation, resolve approved media-bundle example `scene_sample.png` SHA-256 `36dedf45786bcdfa54fd28c00179b1ea9335ec769d94066beaa0b94c797e933d`; unavailable bytes are a scene-specific blocker, **not** proof that a provided description is the exact reference.

## Must happen before any production / release

1. Obtain the owner's express **approval of exact English narration revision** after reading the full EN/RU story, and fresh independent first-listener / bilingual review if available. A merged PR is not approval.
2. Use `ytvideos create --channel paper_detour --format short` only once explicitly asked to start production and within active channel permissions; derive real IDs/context/pins and approval event, never invent IDs.
3. Verify actual image reference bytes and rights, approved model/provider, native output dimensions, paper/card style, camera. Unique AI imagery only when authorized. S013 uses S001 source, never a newly hallucinated photo copy. One complete full-frame layer per shot, no parallax; whole-frame pan/zoom + direct cuts only.
4. Measure real Lawrence voice at exactly one 1.10x speed adjustment and solve actual scene timings—do not treat 13×5s as measurement. Validate audio, music, exact subtitle word sync and reused visual frame to opening for the loop. Review all complete composites; don't equate file existence with acceptance.
5. Authorize and review exact MP4 separately. Upload, scheduling and publishing require direct owner instruction; comments require separate permitted posting action.
6. Current Paper active profile `channels/paper_detour/channel.json` remains untouched. No changes to skills/docs/runtime, no interference with other active story PRs #13 (owner rejected) or #19 (maple syrup).

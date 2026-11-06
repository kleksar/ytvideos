---
name: ytv-youtube-descriptions
description: Write, assemble or audit complete YouTube video descriptions against accepted film content, preserving approved hashtags, chapters and required disclosures and returning exact reviewable texts.
---

# YouTube descriptions

Own narrative text and assembly of the complete description. Read the active project's instructions and channel profile; [Paper Detour](references/paper-detour.md) has its own profile. Titles, hashtag selection, chapter creation, translations and release mechanics have separate owners. A request to check and show descriptions produces reviewable local text; external writes follow the actual authorized scope.

## Establish the input

Identify the exact channel/video and language, format, current title/cover, accepted film version, script or transcript, factual limits, public-link/credit requirements and requested result. For existing releases read a fresh complete description. For a catalog enumerate all scoped editorial videos and explicit exclusions; aliases and misleading folder names must not assign the story.

Ground text in the delivered film when it differs from an older script. Record what was actually checked: accepted script, transcript, release records or playback. Missing content means `needs_content` for the affected row, not creative extrapolation. Do not call a script comparison full-film playback or independent fact verification. Develop the description directly from the accepted material; consult an external session when the user explicitly requests it.

## Описание длинного ролика — все каналы ytvideos

Постоянное указание пользователя от 3 ноября 2026 года. Для каждого длинного видео, независимо от канала, собирать публичное описание в одном порядке:

1. **О чём видео:** самостоятельный смысловой текст о событиях, героях, конфликте или вопросе фильма.
2. **Таймкоды глав:** принятый проверенный блок chapters owner.
3. **Хэштеги:** принятый блок hashtag owner.

Исследовательские источники, библиографии и сведения о способе производства картинок — реконструкции, генерация/нейросети и прочие служебные пояснения — сохраняются внутри проекта. Публичный текст посвящён содержанию видео. Платформенные декларации оформляются в соответствующих настройках отдельно. При приведении старого описания к этому стандарту убрать прежние служебные вставки, сохранив точные главы и хэштеги. Варианты A/B меняют смысловой заход первого блока, общий порядок остаётся тем же.

## Write or keep the narrative

For long-film variant packaging use the concept cards from the [shared A/B standard](../ytv-youtube-ab-testing/SKILL.md#стандартный-пакет-длинного-фильма): supply a complete description for each concept that passed its distinction check, with its own opening and narrative angle. Preserve accurate protected blocks. The experiment owner determines which description is active and the scope of any comparison.

For Shorts and long films, write a substantive, engaging description as detailed as the accepted material and format reasonably allow. Open with a strong, clear hook identifying the subject, person, event or question; develop the setup, conflict, mechanism, stakes and relevant context that the video actually covers. Help viewers find the video by naturally including specific names, places, periods and terms a viewer might search for when supported and relevant. Use readable sentences, not repetitive keyword lists or search-term stuffing. A complete description need not reveal every twist or repeat the script; avoid padding and do not impose a fixed word quota. Respect a specifically requested length and the channel's own format. Search visibility is a goal, not a guaranteed ranking or performance result.

Retain qualifiers and attribution that change the claim: reported estimates, an attributed decoding result, folklore, an adapted personal account. Do not invent motives, causal links, diagnoses, quotes, scientific proof, sources or credits. A procedure's expected output is not a demonstrated run; “we have not reproduced it” does not mean “nobody has.” Keep effective existing text without cosmetic rewriting. `keep`, `revise` and `needs_content` are valid decisions.

Apply the global public-materials rule in [root AGENTS §11](../../../AGENTS.md#11-подача-всех-сюжетов): by default, omit research sources, citations, bibliographies, “Further reading” blocks and research URLs from every channel's public description. Keep source records in the episode workspace. Preserve legally, contractually, license- or platform-required credits and disclosures. Add functional or promotional links only when explicitly requested or required by an accepted channel standard. A real video URL does not prove a clickable Shorts link or a configured Related Video association.

## Assemble protected blocks

Hashtag and chapter owners supply accepted complete blocks; this skill does not silently reselect tags or retime chapters. On a wording-only pass preserve exact current blocks, including spelling, order and internal line breaks. Preserve required disclosures and explicitly authorized functional/promotional URLs. Establish boundaries explicitly; never remove every `#…` or timestamp-like fragment globally. When boundaries or a required change are ambiguous, leave that portion open and return it to its owner.

For a new Short in the full production flow, coordinate the description and full description hashtag block with the hashtag owner; after the main title wording is selected, hand its proposed title subset to titles for assembly and include the resulting exact full title with the description in the package shown before upload. Keep the full description block separate from the small title subset. This does not authorize changing the title during an existing video's description-only edit. For a new description assemble accepted blocks once. Include the hashtag owner's full description block and coverage result; do not replace it with the shorter title subset or silently trim it for brevity. If required coverage is unresolved, return that issue to its owner before marking assembly ready. For an existing one keep a baseline and record exact protected substrings with expected occurrence counts. Avoid duplicates on rerun. A protected link can be its exact URL when surrounding CTA wording is legitimately revised; do not freeze an entire paragraph without reason. Long films in ytvideos use the three-block order above; other scoped formats use their requested structure.

Run the [local validator](scripts/validate_description.py) from this skill's directory, or invoke it by absolute path with explicit episode input paths:

```sh
python3 scripts/validate_description.py DESCRIPTION_EN.txt --baseline BEFORE.txt --protected-blocks PROTECTED.json
```

`PROTECTED.json` contains `blocks: [{label, text, occurrences}]`; optional `preserve_order: true` retains their listed order. The validator checks exact preservation/counts, UTF-8 byte length and forbidden characters and returns a diff. It cannot establish truth, link availability, chapter timing, meaningful opening wording, film identity or live display. New or retimed chapters still require their owner's validator and media evidence.

Check current [YouTube description guidance](https://support.google.com/youtube/answer/12948449?hl=en) and [API field limits](https://developers.google.com/youtube/data/reference/rest/v3/videos). Help describes a 5,000-character field; the API specifies a maximum of **5,000 UTF-8 bytes** for `snippet.description` and excludes `<` and `>`. Measure both; do not confuse bytes and characters for multilingual text. Put useful information in the first lines and give each video a unique description; these practices do not prove a causal search or view increase.

## Return and hand off

Return the exact full text, baseline/diff, material version and comparison method, protected blocks and link checks, decision/reason and separate states:

- Source: `accepted_material_checked`, `partial` or `needs_content`, with evidence and limits.
- Editorial: `keep`, `revise` or `needs_content`, with reviewer identity.
- Assembly: `validated` or `blocked`; validation is not editorial or live-display approval.
- External: `not_requested`, `proposal_only`, `deferred`, `unchanged_verified` or `applied_verified`.

For a catalog show a decision for every included video and make all complete descriptions directly reviewable, including unchanged texts and preserved blocks. Save results beside each episode and a catalog index when useful. Keep accepted/current external metadata separate from proposed text. When a user accepts a previously shown bundle, pin its exact files/versions (hashes when useful), validate those bytes against the fresh protected blocks, and hand off that accepted text. If a concurrent edit changes the reviewed description or protected blocks, reconcile the affected row before writing. After verified application, advance current episode/catalog state; rerunning a preview builder must not reset applied state to proposal-only.

Production calls this owner during packaging and reconciles the description after the film is fixed. A narration/edit change invalidates affected claims or chapter timing; a wording-only description correction does not restart media production. Authorized writes go through the project's release/global uploader, which owns fresh-state merging, API preservation, experiment coordination and read-back. A local file or successful validator is never evidence that YouTube was updated. Inspect actual collapsed/expanded destination display when applied; a local preview is only a preview.

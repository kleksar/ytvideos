---
name: ytv-youtube-video-titles
description: Write, revise or audit YouTube video titles against the actual story, thumbnail and viewing surface; produce exact title decisions and verify authorized changes without disrupting active experiments.
---

# YouTube video titles

Own the video's title text and its editorial/display checks. Read the active project's instructions and the relevant channel profile. For Paper Detour use [this profile](references/paper-detour.md); another channel supplies its own language, audience, tone and publishing context. Thumbnail lettering, descriptions, hashtag selection, experiment management and API mechanics have separate owners.

For new story development, the [storycraft opening procedure](../ytv-storycraft/references/appeal-and-opening.md) requests provisional titles paired with cover concepts before the full script. Label these as concepts, preserve the selected viewer promise, and recheck it against the accepted film for final packaging. This does not reopen an approved script.

## Establish the real input

В ytvideos для длинного фильма любого канала готовить три названия по [стандартному A/B-пакету](../ytv-youtube-ab-testing/SKILL.md#стандартный-пакет-длинного-фильма) параллельно финальному рендеру, используя замороженный сюжет и монтажную версию; вернуть все три точных текста на проверку. Shorts сохраняют обычную процедуру упаковки.

For one film, use its accepted version, central event/question, payoff and evidence limits; for an existing release also identify its exact channel/video ID and current title, thumbnail and experiment state. Prefer the actual delivered film over an earlier script when they differ. Do not promote an unmade rewrite to the published story. For a catalog audit account for every scoped editorial video and explicit technical exclusions, using a fresh complete inventory.

Develop and check titles directly against accepted material and real constraints; consult an external session when the user explicitly requests it. A catalog audit is not permission to rewrite unrelated fields.

## Choose the title

For weak feed appeal or competitor research, use the packaging owner’s [feed comparison](../ytv-video-packaging/references/feed-research.md).

For new titles and substantive title revisions, run one focused vidIQ draft pass under the [shared packaging procedure](../ytv-video-packaging/SKILL.md#vidiq). Prefer MCP `vidiq_generate_titles`. Pass the supported story mechanism, payoff and qualifications in `analysisSummary`, with the actual language and format. Add curated competitor or previous titles when they help clarify the audience or avoid repetition. For unpublished work use the working title and approved synopsis. If MCP is unavailable, use Optimize or Studio Suggestions for a supported target. Check the literal and implied claims before considering scores. Rewrite or discard suggestions that change who did what, overstate the scale or imply a verified result the film cannot demonstrate. Fit surviving ideas to the assigned concept and cover.

For long-film packaging use the concept cards and [pairwise distinction check](../ytv-youtube-ab-testing/SKILL.md#обязательная-проверка-различимости) from the shared A/B owner. Develop each title within its assigned viewer promise; apply that owner's criteria for shared dates/names and cosmetic rewrites before handing off exact wording. Shorts use their normal package. Each must accurately describe the same accepted film, work with its assigned cover, and pass the actual surface checks below. A title-only correction to an existing release does not require creating a new experiment.

Identify the concrete person, object, action or consequence that earns the film's curiosity. Prefer bold, high-interest titles: find the strongest supported conflict, stakes, surprising reversal or consequence, and express a clear reason to click. Develop punchy candidates before choosing; do not settle for a merely descriptive label when the film supports a stronger promise. Choose the strongest natural wording for the audience and channel, whether searchable or curiosity-led; neither mode excuses vagueness, keyword stuffing or a false promise. Front-load the useful subject and event, not channel branding or an unknown proper name without context. Read it aloud for natural wording and pronoun clarity.

When a user proposes a provocative title, preserve its intended hook and intensity while checking the literal claim and implied scale against the film. If it overstates the facts, sharpen the wording around the strongest supportable claim instead of defaulting to a bland subject label. A proposed title can change the viewer's expected story: check that the accepted film actually develops and pays off that angle. For an existing or accepted film, propose a stronger truthful title within its content; do not silently rewrite the story to fit. Adapt the intensity to the channel profile and the story, not one formula across channels.

Keep qualifiers that materially change the claim: a reported estimate is not a verified score, a question is not proof, a legend is not independently documented history. Preserve the channel's accepted dramatic retelling without inventing motives, deaths, danger, numbers or causal links. Check the title against the specific film, not just the general topic. Thumbnail and title should complement the same promise; repetition is a concern only when it adds no useful context. Do not weaken an effective title simply to make every audit row a change.

Treat title hashtags as a separately owned exact block. For a new Short in the full production flow, after the user selects the main wording, receive the small relevant title subset from the hashtag owner and append it without altering the selected wording. Count the entire string, including spaces and hashtags, against the platform limit and check the meaningful prefix on the actual relevant mobile and desktop surfaces; reduce the tag tail if needed, not the selected wording. Present the exact full title alongside the description in the package before upload. Choosing the main wording is not approval of the assembled package: the existing package approval covers the displayed final string, without adding a separate approval gate. If no relevant tag fits, retain the selected wording and record the reason. Preserve accepted spelling/order when only the main wording changes. If a change to that block is actually needed, get the hashtag owner's result; absence of a requested block is not an instruction to clear existing tags. Keep the main title intelligible before the tag tail. Distinguish hashtags from the separate API Tags field.

## Check the actual surface

Check spelling, factual scope, full-string platform validity, and the title with the current thumbnail. Count and record the entire title including spaces and its exact hashtag tail against the current 100-character YouTube limit; do not mistake a channel's rough length orientation for the platform limit. Inspect the actual channel/feed/watch surfaces relevant to the format at the desktop and phone sizes required by the profile. Log the viewport, surface, visible text, result and screenshot. A DOM accessible name may contain the full title even while the rendered card clips it; inspect the rendered image as well.

The visible prefix must communicate a self-contained meaning. Front-loading a noun is insufficient if the event ends halfway through a phrase. Character count alone cannot prove fit; device width, font and card width matter. Truncated trailing hashtags are acceptable when the title's meaning survives. Local layouts and font measurements are useful previews, not proof of a live YouTube card. A narrow desktop viewport is responsive-web evidence, not a native mobile-app test.

If the live check is unavailable, save the candidate and leave that check open. Do not mutate a public video solely to experiment with fit. When a substantive correction is authorized, record editorial acceptance, use the release/uploader route, and complete the real display check after saving; if it still clips materially, revise the affected title and recheck, without restarting video production.

## Respect the experiment

Use the [experiment owner](../ytv-youtube-ab-testing/SKILL.md) for its contract, lifecycle and result; this skill supplies exact truthful title variants.

Before changing an existing title, verify any active experiment through its current management surface and project records; do not infer absence from the API's single returned title. With an active title/thumbnail A/B test, retain its variants and prepare a deferred candidate unless changing/stopping that experiment is authorized. A general title audit does not silently end it. Do not claim a chosen winner, CTR improvement or causal performance effect from editorial preference or successive manual edits.

## Deliver and continue

For each film return exact current/selected main wording and full title, material version and factual grounds, thumbnail relationship, hashtag source, `keep/revise/defer`, reason and separate states:

- **Content:** grounded in accepted material / needs review; this is not independent verification of every historical claim.
- **Display:** not checked / desktop checked / desktop and responsive-phone checked, with the actual surface and limits.
- **External state:** proposal only / deferred for experiment / applied and read-back verified / unchanged and verified.

Store the versioned result beside the film. For a catalog include totals, exclusions, explicit deferred rows and a minimal change set; no video may disappear from the accounting. When external corrections are authorized, continue via the project's release procedure and available `youtube-upload` owner through verified saved state, preserving descriptions, chapters, separate Tags, language, category, privacy, thumbnails and playlist memberships. Those owners handle OAuth, part preservation and unknown outcomes. Preserve concurrent edits by re-reading the target before writing.

The production coordinator calls this skill automatically during packaging, reconciles the title with the finished film, and resumes from the affected stage after a correction. Local title readiness is not upload/publication authority. Report concrete changes and remaining checks, without promising SEO, CTR or retention gains.

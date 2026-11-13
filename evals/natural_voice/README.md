# Natural voice — editorial examples and probes

Owner: [narration](../../docs/standards/narration.md). This folder is evidence/evaluation material, not a second runtime standard. User selected the revised #20/#25 examples on 2026-11-13; the exact script commits are in [examples.json](examples.json). Full originals and rewrites remain in their PRs. These are preferred examples, not perfect universal templates, measured retention or new production approvals.

## Provenance and interpretation

The Russian Wikipedia essay [Признаки сгенерированности текста](https://ru.wikipedia.org/wiki/Википедия:Признаки_сгенерированности_текста), read 2026-11-13, provided hypotheses about generic praise, shallow explanation and mechanical phrasing. It explicitly describes observations, not word bans or reliable authorship detection. Our speech procedure is a project decision, tested qualitatively by the owner on two examples; it is not a scientific threshold. No copied Wikipedia examples are used as our narration.

S-5 replaces an emotion label with the captain's action. Larry adds a real launch detail supported by the linked Smithsonian source; editors must verify added details, not treat them as cost-free stylistic changes. A reported humorous quote is optional, not mandatory seasoning for every episode. Preserve tragedy, uncertainty, roles and the channel's voice.

## Behavioral checks — NOT_RUN

Give a fresh reviewer only the actual material, without the desired answer, in a bounded session. Save exact inputs, original response, identity and hashes under the existing review contract. Do not convert these expected observations into a claimed PASS.

1. **Generic summary:** a narrator says a situation was extraordinary and a decision courageous without naming the action. Reviewer should ask what happened, not demand adjectives.
2. **Overcorrection:** a coherent paragraph is split into ten two-word fragments. Reviewer should be allowed to prefer the original, even though the rewrite sounds less encyclopedic.
3. **Fabricated humanity:** rewrite adds a shouted quote, fear, countdown or victory unsupported by the supplied fact pack. Reject the invented detail, regardless of fluency.
4. **Quiet positive control:** a simple causal explanation already sounds natural. Keep it; no mandatory joke, villain or twist.
5. **Translation drift:** Russian adds a rescue while English only describes an escape. Require meaning parity; a better-sounding RU story cannot sell a different English video.
6. **Forced loop:** the closing merely names the opening object or adds a colon. Read both complete cycles and reject a restart, unresolved promise or false chronology; punctuation alone is not evidence.
7. **Faithful revision:** compare preserved A/B samples with hidden labels, record specific attention/clarity/voice observations, then disclose sources. A/B/hybrid/neither all valid.

Static tests exercise packet routing, schema preservation and example integrity only. No independent live reviewer, actual TTS or viewer experiment has been executed for this change. Source-only local tests and remote CI must be reported separately from artistic acceptance.

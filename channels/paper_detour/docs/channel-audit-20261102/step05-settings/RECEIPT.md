# Paper Detour settings — completed 2026-11-02

Channel `UCMVfdfaNxV3ZkI3_J3Eejzw`, @rarovista. User authorised continuing the channel improvement plan, explicitly leaving the address untouched because they can change it only in about a week. No handle check/change or reminder was performed in this stage. Country CY remains unchanged per earlier direction. Session Extra High waiver remains in force; no consultation or agents invoked.

## Changes and verification

1. Added 15 channel keywords, 257/500 API characters: Paper Detour; paper diorama; paper diorama stories; visual storytelling; strange true stories; history stories; science stories; natural history; evolution; what if; legends; personal stories; technology history; digital life; educational Shorts. They describe the actual channel catalog/accepted About text. They are channel keywords, not hashtags or episode Tags. No search-volume/ranking claim.
   - One API `channels.update(part=brandingSettings)` using the existing management token after fresh channel identity/scope verification. Preserved other mutable channel fields. The first immediate read was stale (no keywords); a later read reconciled the accepted result without a second mutation. All 15 exact phrases then appeared in fresh API and Studio chips, 257/500. `keywords-operation.json`, `keywords-validation.json`, `keywords-saved.jpg`.
2. Disabled **Let YouTube enhance visual quality** and **Let YouTube enhance audio quality** for future uploads. Rationale: preserve the authored paper texture, colour and accepted mix. These are channel enhancements, not new audio generation or a change to uploaded media.
   - Current official Help says controls are desktop Studio-only and apply to future uploads, not ads/already uploaded videos; individual viewer accessibility preferences may take precedence. Current Data API discovery exposes no corresponding enhancement field. Capability gap recorded before using UI.
   - Saved once, received “All changes saved”; reopened Settings → Channel → Advanced. Both boxes unchecked, Save disabled. Compared all 13 checkbox/radio controls: only these two changed. Auto-dubbing/manual-review-all-languages, audience, ads, clips, captions filtering and third-party training values preserved. `advanced-before.txt`, `advanced-after.txt`, `enhancements-validation.json`, `enhancements-saved.jpg`. Optional Google survey dismissed without answers. No new permissions or linked-account changes.

## Final checks and deliberate omissions

- Fresh `after-final.json` and `validation-final.json`: keywords exact; handle, country, description, languages, all translations, banner and API status preserved.
- Fresh Studio Feature eligibility: Standard, Intermediate and Advanced all enabled (`feature-eligibility.txt`).
- Fresh upload defaults: Private, English video language and title/description language, standard YouTube licence, comments enabled/Basic moderation, likes visible (`upload-defaults-basic.txt`, `upload-defaults-advanced.txt`). No default title/description/Tags inserted: these remain episode-specific; category is selected per upload. Caption-certification declaration not invented. Web defaults do not replace explicit API-upload settings.
- Public business email and external links intentionally left empty: user has not supplied intended public contacts/pages. No private account email copied. They remain optional profile additions.
- This step changes channel keywords and future-upload enhancement preferences only. No videos, playlists, publication schedules, A/B tests or account security settings changed. Full film/audio QA is outside this settings pass. No new media files or rendering.

## Sources

- [YouTube channel settings](https://support.google.com/youtube/answer/2976814?hl=en)
- [Enhancement scope and Studio controls](https://support.google.com/youtube/answer/16619284?hl=en-GB)
- [channels.update fields/preservation](https://developers.google.com/youtube/data/reference/rest/v3/channels/update)
- [Channel keywords schema](https://developers.google.com/youtube/data/reference/rest/v3/channels)

State: **applied_verified**. Planned channel setup improvements complete except the address explicitly deferred by the user and optional public contact/link additions. This does not claim every optional YouTube field must be populated.

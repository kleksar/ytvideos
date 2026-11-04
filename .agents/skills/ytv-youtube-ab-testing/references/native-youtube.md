# Native YouTube A/B support

Verify [official help](https://support.google.com/youtube/answer/16391400?hl=en) and the actual account before execution. Official help rechecked 2026-11-03:

- Studio desktop with advanced features; up to three title, cover or paired alternatives. Shorts, private, made-for-kids and age-restricted videos are ineligible; scheduled live/Premiere restrictions also apply.
- Description is not a native experiment field; the documented choices are title, thumbnail or paired variants. Keep one approved description fixed during that test.
- Variants run concurrently. The decision uses watch time/share, not CTR alone. Tests can take up to two weeks; retain the reported status rather than inventing a sample threshold.
- The platform applies its final selection; without a clear winner the first submitted option becomes the default. Include this in the authorized start contract.
- An external title/thumbnail change stops the active test. Read it before release changes.
- Preserve the exact outcome: Winner, Performed Same or Inconclusive. An inconclusive result is not proof of equality.

Execution route: current [Data API v3 discovery](https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest) exposed no A/B/experiment method in the 2026-11-02 check (83 methods). Native testing uses documented Studio controls through the project's release/uploader boundary. This says nothing about private/internal APIs and is not a fallback for an OAuth or quota failure.

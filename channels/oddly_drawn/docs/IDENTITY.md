# Oddly Drawn — identity evidence

Read-only observation, 2026-11-16. Request: `GET https://www.youtube.com/channel/UCcZWXzkL_K1mD5dr8MZBYrQ`, Python urllib with `User-Agent: Mozilla/5.0`, without account credentials.

Observed response fields:

```json
{
  "title": "Oddly Drawn - YouTube",
  "channel_ids": ["UCcZWXzkL_K1mD5dr8MZBYrQ"],
  "canonical": "https://www.youtube.com/channel/UCcZWXzkL_K1mD5dr8MZBYrQ"
}
```

This confirms the public title and ID together. It does not verify a current handle, OAuth ownership, permissions, private/scheduled videos, applied brand images or calendar. No external channel changes were performed. Web search still returned an older Two Ways Lab handle/title snippet; it is not current identity evidence. The web reader was throttled; the direct public HTML request succeeded. vidIQ balance was 0 credits; no paid lookup was attempted (observed cost of balance: 0).

Historical local identity: [2026-11-12 Studio observation](../../two_ways_lab/docs/PUBLICATION_QUEUE.md), `@TheTwoWaysLab`, same channel ID. That dated handle and publication queue are retained as history, not asserted as current. Local machine key remains `two_ways_lab`; a new handle is not guessed.

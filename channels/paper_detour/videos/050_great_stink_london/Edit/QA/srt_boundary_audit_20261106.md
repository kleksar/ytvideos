# SRT boundary audit — Paper 050 v03

- 75 cue texts matched all 640 words in order and every start/end matched the first/last word within 2 ms.
- Cue source SHA-256: `2bec45934c975b0976a1074da9a92e009248953d0fd706046823833c7e61eb89`.
- Word map SHA-256: `fb6f6bda8c4c9d745a643d5759131be27956a8d40a746b3b147b627c44cfa507`.
- SRT SHA-256: `b45e72639c95eec8f3bcfae08418147093284a5c33b83a19bbcabb7a3880f0f1`.
- Final MP4 SHA-256: `6ee1347d4282b7d984ce82dd62b27cf5bc9a711c452e3632fcc7341363d78139`; ffprobe audio and video start at 0, duration 252.8 s.
- The alignment source itself is marked REVIEW_REQUIRED and says it still requires audio review. User confirmed three short technical samples of burned-in captions, not this whole separate track. Exact boundary correspondence is not proof of alignment accuracy or audible sync.
- `timing_mapping=UNVERIFIED`; `playback=UNVERIFIED`. No separate SRT ready/upload claim.

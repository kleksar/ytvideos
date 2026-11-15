EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Paper Detour Long — Demon Core, handoff

Repo main observed `5d3222c8888c775d2195c8b2949949f2d992e98d`; tree `e92a9c5b9ee656aa1448f34264b217ca1d0cbe98`. English narration Git blob `262f8c73a5cb21ea2cda536260e0e7cc4462d86c`, RU complete meaning translation `1c5ad76c84f1cbfb2d2ab80f1646fb7e393a65c4`; story-review refers exactly to these text bytes. Channel from live `channels/paper_detour/channel.json` active; English illustrated Long, physical full-frame paper 16:9. This PR only adds 8 text files under one episode folder.

## Actual blocker
GitHub connector works but runtime host has no authorized ytvideos checkout (`/mnt/data/ytvideos` absent) and `command -v ytv` produced nothing (although `uv` exists). Thus **no actual `uv run ytv start` was run**, no pinned plan_summary/read_next/task_guide/receipts/run ID, no original independent session reviewer. Cannot claim `awaiting_script_approval`. Do not forge IDs or accept author scoring as review.

## Local entry
1. Authorized coordinator checks existing actual runs with current CLI status/resume to avoid duplication; otherwise from correct checkout executes `uv run ytv start --channel paper_detour --format long --intent 'Review and consider editorial Demon Core two accidents; no media generation'`.
2. Read actual `plan_summary`, `doctor`, `read_next`, pinned task guide, skill, full reference documents and assets; import research + exact unapproved scripts as inputs, not as a completed official run.
3. Run original `ytv-script-review-v1` on genuine exact EN SHA-256, fresh independent session with blind opening, then complete text and repeated full read; separately assess full Russian meaning. No use of this author scoring in blind review input.
4. If review requests change, update both texts and all dependent scene spans/briefs, invalidate old hashes/timing/review. Present full exact EN/RU for real owner script approval. The owner must actually decide.
5. This automation **does not permit** merge, paid providers, imagegen, TTS, video clips, renders, audio, YouTube upload or publication, regardless of PR merge/CI.

## Verification
EN/RU story has 34 paragraph pairs and provisional S IDs; full independence/MP4/TTS/image and actual runtime unknown. CI status must be read back on exact final PR HEAD. Paper-plane reference pixels are not available here; no pretend brand asset creation.

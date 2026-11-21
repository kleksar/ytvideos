EDITORIAL_CANDIDATE_UNREGISTERED

## Scope, source and exact policy

Repository `kleksar/ytvideos`, 2026-11-21, Paper Detour. Parent remote `main`: `131ef24068d75967b1e43aa88e5f1370f6775054` (must be checked again before branch write). #124 is **MERGED**, so the main canonical `docs/standards/editorial.md` and `ytv-write-script` rules apply, NOT separate PR proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72`. Existing runtime pins remain unchanged.

Six exact story texts are in `variants/02m|05m|10m/script.en.txt|script.ru.txt`. Each SHA-256 and Git blob SHA is recorded in `story-review.md`. The 05m EN master proposed by author is SHA-256 `5c67e3c3231045e13cc28df539403f7ebcddc78055a752bb1f29c1061e68a827`. There are no obsolete spans, audio timings or media; do not copy any from another version.

**Observed blocker:** no repository checkout containing the `ytv` CLI in this execution environment. A direct `uv run ytv start --channel paper_detour --format short --intent 'editorial story proposal'` attempt ended in `Failed to spawn: ytv / No such file or directory` exit 2; no actual `plan_summary`, `read_next`, `task_guide`, or pinned run documents were returned. No official run, lease, script gate or approval has been created. **No independent reviewer was invoked**; this is only authorial review. Rights for archival images and verified paper-plane source bytes are absent.

**Local import pathway:** inside an authorized project checkout with real runtime, run `uv run ytv start --channel paper_detour --format long --intent 'review and register Ecce Homo 05m from Git-only editorial candidate'`, then inspect its actual `plan_summary`/`read_next`/`task_guide`/pinned documents; import the exact chosen EN script through the allowed `--source-script` path and attach the six variants and story review using the canonical `script_variant`/`story_review` artifact kinds and actual source paths. Do not claim registration until returned IDs/receipt verified. Feed exact 05m text to a genuinely independent reader without author verdict, then provide sources and strong runner-up only after initial response. Check rights, voice duration, acceptable Long profile, and valid next-video target. Choose one master with owner approval; only then production may be considered separately.

No TTS, image generation, video, upload, scheduling or merge authorized/performed. No common docs/skills/channel configs altered. If original run pins conflict with current editorial, perform a named migration; never overwrite pins. PR may remain Draft indefinitely.

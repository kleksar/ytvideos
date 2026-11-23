EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Flight 90 sixth-man package

**Repo:** `kleksar/ytvideos`. **Channel:** `nuviko_history` English illustrated Long. **Source remote main:** `a6023668001421b689a8142cebc0bd436545be6b` (observed 2026-11-23 15:xx Europe/Belgrade); **#124 merged** 2026-11-16, so canonical main docs were used, not standalone proposal revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72`. Last created story Draft at selection #386 Paper. New branch must be based precisely on observed main; before updating head re-check main and all story PRs for a concurrent duplicate. No changing shared docs/skills/status or other PRs.

**Package:** six complete UTF-8 scripts [02m](variants/02m/script.en.txt), [05m](variants/05m/script.en.txt), [10m](variants/10m/script.en.txt) with complete RU pairs; hashes/individual editorial scores [story-review.md](story-review.md), one common [research](research.md) and [packaging](packaging-brief.md). 05m EN SHA-256 `a1b8771903c15eff762abeb9562ddca9795caff61bc1ef4ea2b1cfefcd7b6de7`, recommended only. All estimated duration; no actual audio or film.

**Real runtime attempt:** from host without repo/ytv executable:
```
uv run --offline ytv start --channel nuviko_history --format long --intent 'New English historical documentary story package: six full 2/5/10 EN/RU scripts'
# error: Failed to spawn: `ytv`; No such file or directory (os error 2)
```
Consequently **no** persisted run ID, task/lease token, plan_summary, read_next, task_guide, pinned reference_documents, artifact ID, reviewer response, receipt or approval exists. Git-only permission is exceptional editorial queue, NOT script gate. The host had GitHub connector but no local project checkout. Independently validated Nuviko traveler turnaround/emotions actual PNG bytes are unavailable to this editorial worker; textual brand profile is not proof of image files.

**Recovery:** in repo-equipped runtime start a legitimate Nuviko Long research/script run using current local policy and supplied intent, then read plan_summary + read_next + task_guide + pinned reference_documents before claiming work. Preserve and attach six exact variant files and story-review with actual `attach-artifact --kind script_variant` and `story_review` per CLI contract, recording returned IDs/hashes, without retroactively inventing prior pins. Set independent first-reader input to exact recommended EN script **without author scores, verdict or beats**; reader should first respond to opening/full meaning, then receive sources and the strongest competing pitch, and produce own immutable `ytv-script-review-v1` response. After independent review a new text hash invalidates old review. Owner chooses/approves only **one** exact master through existing gates.

**Still UNVERIFIED:** realistic read speed and 10s screen integration; complete primary visual reference bytes and archive rights; actual YouTube video viewing, transcripts, comment evidence; same-author view baselines; Nuviko own retention/CTR; actual captions, playable next-video intro and native end screen; independent bilingual reviewer and external preview. Rendering/reconstruction, TTS, video providers and publication are strictly prohibited until authorized by actual workflow. No media claimed.

**No** storyboard or prompts yet: author recommends 05m but its independent text check is not done. Do not derive storyboard timings from 02m/10m or historic approved materials.

EDITORIAL_CANDIDATE_UNREGISTERED

# Git-only editorial handoff — Paper Detour, Van Meegeren

Source remote `main` at selection: `a6023668001421b689a8142cebc0bd436545be6b`. #124 **merged**; use canonical main editorial/writer skill, NOT old proposed SHA as current. Source of policy: `docs/standards/editorial.md`, `.agents/skills/ytv-write-script/SKILL.md` on that main. New branch always from freshly rechecked remote main. No old production runtime pins are changed.

Scope: one historical story, six full EN/RU narrations, research, individual review, packaging concept, no media. Recommended exact master: `variants/05m/script.en.txt` SHA-256 `2f3a5ef0328b12e1a15a935103fbad861b1755da425edb1b6ccd32e7a41278f4`. 02m loop FAIL / REWORK, 10m development too slow / REWORK. Do not select any master implicitly from this handoff.

Missing capabilities: no local checkout of this repository, `ytv start` not run through actual repository application (its executable unavailable in the provided container); no `plan_summary`, `read_next`, `task_guide` or pinned `reference_documents` were produced. No independent reviewer, no `ytv-script-review-v1`, no run/lease/receipt/approval. No direct audio-visual rights or true reference image bytes, TTS, imagegen, external video service, MP4, upload or schedule actions.

**Migration route for operator in a real checkout:** fetch this PR at immutable commit, re-read currently pinned channel instructions, check no existing matching run, execute `uv run ytv start --channel paper_detour --format long --intent 'Van Meegeren / Vermeer forgery editorial review'` through normal runtime; inspect actual `plan_summary`, `read_next`, task guide and pinned docs before doing anything official. Register the six exact variants via documented `attach-artifact --kind script_variant`, story review via `--kind story_review` with actual source; get independent reader the exact 05m EN without author scores or beat map; receive and preserve original review schema, repair if necessary, rerun reviewer for changed hash. Then present one exact master to owner for script approval; do not treat this PR as that approval. Avoid source-import route unless owner later explicitly instructs production of a particular immutable text.

Remaining: external first listener; user approval; real format/voice timing; photography licensing and approved reference asset bytes; scene prompts/storyboard for chosen hash **only after** applicable review; actual Paper end-screen targets if Long; targeted checks/CI for exact branch HEAD. No merge implied.

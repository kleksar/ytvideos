EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — two buses, same destination

**Source repo:** `kleksar/ytvideos` / remote `main` read as `d7dbf4d8de0a0719e062e72b7e21b7d3748de100` before research; recheck and record final base at commit time. **Policy #124 merged 2026-11-16** (verified GitHub PR state); current `main` canonical editorial/skill used. Historical proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is **not** treated as an independent current main. No unrelated PR changes imported.

**Selected channel:** Two Ways Lab, because observed story creation sequence ended with #279 Two Ways → #282 Paper → #283 Nuviko. Neighbor #284 was caption engineering, not a story. Recheck before first write; never use memory alone.

**Exact content:** [README](README.md), [research](research.md), [review and SHA-256](story-review.md), 6 scripts in `variants/{02m,05m,10m}/script.{en,ru}.txt`, [packaging](packaging-brief.md). All are one hypothetical bus choice, not three ideas. English primary. Recommendation 02m, **editorial only**; 5m strong alternative; 10m complete but REWORK. Textual loop is authored; AV seam is not proven.

**Capability blocker:** the current container has `uv` but no repository checkout / installed `ytv` executable. An actual attempt to run `uv run ytv start --channel two_ways_lab --format short --intent ...` failed: `Failed to spawn: ytv; No such file or directory (os error 2)`. Therefore no `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, receipt, run ID, independent `ytv-script-review-v1`, approval or official gate. Separate Git-only editorial exception applies; no simulation of runtime.

**Independent-review handoff:** in a fresh isolated reviewer session, present the **exact selected EN and RU text** with no author's scores, research map, classification or verdict. Ask first for raw understanding/hook/anticipated payoff, then show whole text and literal second loop (02m). Only after that provide sources and stronger alternative #89 (subway carriage). Reviewer can reject the idea. Save its own schema output unmodified. Any text edit changes hashes and invalidates reviewer feedback. No self-review is independent.

**Local transfer, without automatic production:**
1. Clone/fetch latest remote `main` in the authorized runtime, inspect branch/state and exact PR HEAD; do not replace existing pins.
2. With valid `ytv` install, initiate `uv run ytv start --channel two_ways_lab --format short --intent 'Evaluate the first bus versus direct bus editorial candidate for production'` before official evaluation; read actual plan_summary/read_next/task_guide/pins. Do not backdate the Git-only research as a registered task.
3. Attach each exact variant+translation as supported `script_variant` and review as `story_review` through actual helper/contract, keeping returned IDs and SHA; produce an independent reviewer receipt and human approval for **one** exact EN master.
4. Resolve Short duration mismatch (channel guide 35–50s; 02m text approx 2m) or get explicit authorized format decision. 05/10m cannot be produced as Long until an actual Long recipe is defined through its own scoped change.
5. Only after text/review/format approval, author detailed storyboard and self-contained image prompts for chosen 02m SHA, verify actual reference bytes, measured VO and AV loop. No TTS, ImageGen, MP4, upload, publication or scheduling authorized by this PR.

**External evidence limitations:** YouTube pages were discoverable by indexed metadata but several video opens failed or throttled; no actual video, transcript, comment or comparable age-normalized baseline reviewed. Recorded views are index samples (not live counts). Two Ways-specific CTR, retention and new-topic demand remain UNVERIFIED; vidIQ paid use 0. This is not a confidence claim about real transit or channel success.

**Concurrency policy:** new branch based on confirmed remote main, single story folder only, no force updates, no edits to common docs, channel status, published artifacts or other PRs; Draft PR only, never merge. Post-push read-back/CI required. Queued or in-progress checks aren't a PASS.

# Production handoff — Apollo 13 CO₂ adapter

Scope: a single full English narration with Russian translation and fact research. No changes to skills, channel defaults, runtime, recipes or permissions.

- **Canonical entrypoint:** `AGENTS.md` → `.agents/skills/ytv-start/SKILL.md` → `uv run ytv start --channel paper_detour --format short --intent 'Apollo 13: create a historical Short from the approved editorial candidate'`. Consult the live task packet and pinned requirements. This PR contains a **candidate**, **not** a user-approved exact production script.
- **Runtime blocker observed 2026-11-13:** this execution host has no `ytvideos` checkout or installed `ytv` CLI. Attempted `uv run ytv start --channel paper_detour --format short --intent 'Apollo 13: carbon dioxide filter adapter (real event)'` → `Failed to spawn: ytv (No such file or directory)`.
- **No run ID, task context, claim, script-review receipt, approval, provider handle, video file, or YouTube upload** was created. Do not fill these gaps with fabricated identities or pass flags.
- **Next authorized stage:** in an environment with the project's checkout/store, use canonical start, read materialized task context, attach these exact candidate texts as inputs to the research/script tasks, obtain actual independent review (including full loop read twice), and show the accepted revision/hash to the user at script approval gate.
- **Not yet authorized:** generation of images, TTS, storyboard, rendering, upload, publication, merge. No assumed budget or silent fallback.
- **Paper requirements remain applicable:** handmade full-frame paper diorama, actual approved assets (including airplane cameo reference), music, subtitle timing and a genuinely continuous AV loop. Art direction and timecodes belong to the later production tasks.
- **Copyright boundary:** real event independently verified via NASA, not a reconstruction of the movie soundtrack, dialogue or copyrighted footage.

This editorial Draft can be reviewed for content without pretending it is an executed production workflow.

# Three-version rework of existing #86 — editorial handoff

Baseline `4932f666cd3d850b71e5756083f949ea170333b1`; new original Short copies in `variants/02m/` with identical Git blob IDs and SHA-256; existing `script.en.txt`/`script.ru.txt` and storyboard not replaced. Added 05m/10m **exact** sibling #137 `38425d26a3d3c44a45323b593cee9127b6568ef0` blobs, with independent provenance but no independent reviewer receipt. Read [README](README.md), [story-review](story-review.md), shared [research](research.md) before choosing one master. There are **two PRs for the same one story**; no automatic dual run/approval/merge, and #137 remains untouched.

If the owner explicitly accepts a specific full script for production, import that exact repo/PR/commit/path/bytes using actual `ytv start --source-script` and documented coordinator source import; keep existing runtime pins; do not run 3 productions. If new editorial candidate rather than accepted source: actual independent reviewer, exact `ytv-script-review-v1`, script approval gate, then storyboard for the chosen hash. 02m uses Short/loop; 05m/10m use Long. No media/TTS/YouTube dispatch in this editorial PR.

## Original #86 handoff / context

EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Handoff — Gimli Glider

**Channel:** nuviko_history (actual ChannelSpec status active, English illustrated Short). **Fresh remote main base:** `d385a1aac3c11e6b79e5b3ea473b19830d7e2e60`, tree `fb2de43178fc83b01c8e38db902dca133ca904b9`. Editorial version 1, 18 exact EN/RU paragraph spans. All eight files in this draft belong only to this topic; shared docs/skills/ChannelSpec unchanged.

**Provenance:** `research.md` gives government Canadian inquiry April 1985 / FAA-hosted PDF pp.25–29 and 2001 Air Transat and Quecreek primary/official alternatives. Approved B samples #20 exact commit `78b375bf0004fdeb45722e6106f2919f09e82fe1` and #25 `28862598989045cd02990e654b086afae28fea59` read as principles, never changed. No archival image/source bytes or recorded speaker statements invented.

**Missing host capability:** current environment has no actual local `ytvideos` project checkout, shared workspace/runtime/store to run `uv run ytv start`; neither a real `sessions.independent` fresh reviewer nor a supported independent host/session is accessible. Thus **no run ID, task id, approvals, reviewer receipt or exact EN hash review**, and no official `awaiting_script_approval` gate. Text loop is author review only; voice, subtitle, exact duration and AV seam **UNVERIFIED**.

**Exact local migration:** use authorized local checkout with actual current main and dependencies, run `uv run ytv start --channel nuviko_history --format short --intent 'Редакционный кандидат Gimli Glider 1983 из Draft PR; импортировать исследование и полный сценарий до awaiting_script_approval'` BEFORE any official re-research or rewriting. Read real returned `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents` and work via actual task contract. Carry `research.md`, exact `script.en.txt`, exact `script.ru.txt` into research/script tasks; calculate genuine EN SHA-256 locally and obtain fresh original `ytv-script-review-v1` from an **independent session** on hook then all EN twice without author beat map/verdict; give sources and strongest alternative only after first impression. If reviewer rejects concept, stop; if revising, preserve prior files and re-review new SHA. Show full verified text to owner on real script gate. Do not invent approval or copy reviewer answer.

**Next stages not authorized:** no merge, TTS, imagegen, render, video upload, publication, channel status change. Any eventual visual production requires opening actual Nuviko traveler refs `channels/nuviko_history/brand/References/traveler_turnaround_20261104.png`, `traveler_emotions_20261104.png` and historical aircraft refs. No real images or source reference bytes attached. All 18 storyboard timings are strictly approximate and should be replaced after accepted audio. Updates to EN/RU invalidate dependent spans, visual prompts, packaging and prior reviews.

**Checks:** author script and fact review only, complete EN/RU exact scene coverage structurally; GitHub remote PR/CI checks reported after publication. Do not call pending CI success.

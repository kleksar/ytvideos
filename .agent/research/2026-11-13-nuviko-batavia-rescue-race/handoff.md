EDITORIAL_CANDIDATE_UNREGISTERED — no canonical ytv task receipt.

# PR #29 Batavia — handoff for one selected source

Baseline remote head `964d88b6836aca9bff583fb98181bd18e959f384` (root EN/RU + original 83-paragraph Long preserved). Owner's 2026-11-15 instruction requires independent 2/5/10 minute compositions; the new candidates live under `variants/{02m,05m,10m}/`.

Selection table with literal EN/RU files and subjective recommendation: [README](README.md). Exact hashes, script maps, eight scores each, hard checks and reviewer blockers: [story-review](story-review.md). Common fact sources: [research](research.md). Recommended **05m Long** editorial candidate only; revised 10m EN/RU source SHA-256 values are recorded in [story-review](story-review.md), and the source claim ledger is updated; no choice/approval by owner.

Current channel.json supports `nuviko_history` Long 16:9; its live runtime profile pins must be read at the future task. The 83 old 16:9 scene intentions and any timings remain attached solely to the unchanged root EN/RU scripts, identical to the new 10m text; they cannot be applied to 02m/05m. No new variant-specific images/scene spans or exact TTS timings exist. All three versions are Git-only candidates, not production pins.

On owner's choice and separate permitted production path: in local working checkout preserve canonical prior runs, verify exact file/hash, `ytv start --channel nuviko_history --format long --source-script PATH --intent INTENT` only if no existing run; read `read_next`, pinned instructions and task requirements, register supporting variants/review via documented `attach-artifact`; independent reviewer must submit their genuine `ytv-script-review-v1` output and applicable gates. No fake `awaiting_script_approval`. An existing run requires status/resume/migration rather than creating another.

Cannot access the repository's persistent `ytv` run store or independent session from this GitHub-only editing host. Therefore UNVERIFIED: reviewer, runtime registration, user approval, scene timing, media, subtitles, exact TTS duration, MP4/AV seam, release. No TTS/imagegen/render/upload/schedule performed.

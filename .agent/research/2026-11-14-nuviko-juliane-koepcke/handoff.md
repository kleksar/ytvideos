EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Handoff / scope

- **Main HEAD observed before preparation:** `cd749ac2559170bdbd761cb447683e1e88260556`; exact Git root tree `d167f3587e19071baad0412c2e408c2fd8be26b2`. Recheck remote main and PRs before writing.
- **Channel:** `nuviko_history`, active per `channels/nuviko_history/channel.json`; separate from musical `nuviko_videos`.
- **Format:** English illustrated narrative Short 9:16. RU is a full working translation, never a separate Russian TTS track. The fixed story paragraphs and exact bilingual spans are in `script.en.txt`, `script.ru.txt`, `storyboard.json`.
- **Evidence/revisions:** first editorial EN/RU revision. 2026-11-14 source matrix and real ten-topic screen are in research.md. A new edit must save prior exact versions, regenerate every dependent scene span, invalidate current review/time guesses, and obtain a fresh reviewer response for the new EN SHA-256.
- **Permissions:** Only this one Draft editorial PR. No merge; no production media, TTS, imagegen, render, upload/publication, channel status changes, approval or paid providers.
- **Unavailable here:** local executable checkout for actual `uv run ytv start`; `sessions.independent` or equivalent independent reviewer capability not exposed by tool registry. An author's two-cycle inspection is not independent review. Script gate `awaiting_script_approval` **NOT achieved**. Actual voice/music/SRT/AV join **UNVERIFIED**.
- **No simulated evidence:** don't invent run, reviewer IDs, receipt, measured timing, or approval. Git object hash is not exact EN SHA-256; compute `sha256sum` of final bytes after checkout.
- **Visual:** Nuviko profile and `brand/VISUAL_PROFILE.md` read; required 2 PNG traveler anchor bytes **not inspected**, so preliminary storyboard intentionally has no 2D traveler. No source photo bytes or scene images supplied. Estimated scenes 4–6 seconds are not measured cuts.

## Exact local transfer (from a real checkout when the owner chooses the candidate)

```bash
git fetch origin
git show origin/work/story-drafts/nuviko-juliane-koepcke-1971-20261114:.agent/research/2026-11-14-nuviko-juliane-koepcke/script.en.txt > /tmp/ytv-koepcke-1971.en.txt
git show origin/work/story-drafts/nuviko-juliane-koepcke-1971-20261114:.agent/research/2026-11-14-nuviko-juliane-koepcke/script.ru.txt > /tmp/ytv-koepcke-1971.ru.txt
sha256sum /tmp/ytv-koepcke-1971.en.txt
uv run ytv start --channel nuviko_history --format short --intent 'Evaluate the Juliane Koepcke 1971 editorial candidate, read its source matrix and seek script approval before any media'
```

On the resulting real run read `plan_summary`, `doctor`, `read_next`, `task_guide`, pinned `reference_documents`, current task context and the actual candidate source artifacts. Pass reference text as research/script task input using the supported artifact route; do not pretend `--source-script` is an owner-approved production script. If a run already exists, `status` → `resume` → `plan` instead of creating a duplicate. A fresh independent reviewer must receive the opening, full exact EN master twice, and only after initial impression the sources and Palomares comparison; original `ytv-script-review-v1` tied to exact EN SHA-256 is required. Show full EN and RU to owner at official script gate. This Draft itself grants no production approval.

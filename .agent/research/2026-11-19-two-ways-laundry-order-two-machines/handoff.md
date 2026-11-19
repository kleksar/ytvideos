EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Two Ways Lab washer/dryer order

Scope: single new Git-only editorial topic with three full EN+RU drafts, deterministic comparisons, evidence and self-review. **No ytv run, task lease, pinned document snapshot, script approval, independent reviewer receipt or media** exists. The available GitHub connector can read/write Git; this execution environment does **not** expose the production repository's runnable `uv run ytv start` with its configured workspace/database, or a fresh independent reviewer session. No attempt to claim the CLI was executed or to bypass it.

## Canonical source / change control

- Remote `main` checked before research and before write: `fc4c529778c53c9022f866b25402c7ee6d2ea690` (recheck before branch creation).
- #124, rule for three full variants, **merged 2026-11-16 11:21:52 UTC**. Thus active documents on `main`, not historical proposed revision, are canonical. No unmerged proposed policy imported.
- Latest story PR at selection: #245 Nuviko, previous #240 Paper and #237 Two Ways; next rotation is Two Ways. Check later/concurrent PRs again before applying.
- Open #138 would change Two Ways profile, but is **unmerged**. The current main's Short-only illustrated ChannelSpec applies. Old runtime pins must not be swapped for main without the documented migration.
- No existing issues/PRs closed, altered, rebased or force-pushed. No docs, skills, channels' published status or scheduling changed.

## Exact candidate files and status

| Variant | EN production text SHA-256 | RU editorial text SHA-256 | Editorial / format |
|---|---|---|---|
| **02m** | `2a2d503238b3d66670bd1fa0ff29b07323b1283ba0c22e781c866d69567ddd1d` | `137e222e5ddd2581887ca9c975b6c6b9a2305ab9f5590d19f31fbcf2c0c892bc` | STRONG_CANDIDATE, recommended; ~111s modeled narration vs usual 35–50s Short |
| 05m | `4d1d7cb8fde5fb876df168c777fa3eba52f296a3adcd60ad7664e24b09ba9690` | `c6341ef7f3d0920f3f6a93f4023c239bad97add08c5117aef4c412faa4922a43` | STRONG_CANDIDATE editorial; Long configuration BLOCKED |
| 10m | `70f00a28aaa932e8030fc5c96d482723f05ac06c190614ba5b60a2a8a6e5c736` | `c4692689e1a698ac1aef48c108eb4ebbe901e74d6277122f2731907cbf0d71d7` | REWORK (numbers/pace); Long configuration BLOCKED |

SHA-256 hashes are for **exact file bytes**, including single trailing newline, checked by zero-credit text hash on fetched Git blobs. Git blobs also recorded in `story-review.md`. No false statement that those bytes have been converted to approved master.

## Exact blockers and local continuation

1. **Runtime registration unavailable here**: no usable production checkout/workspace database and `uv run ytv start` was not invoked. Local operator should check the real repo/workspace, execute `uv run ytv start` **before opening a formal new run** under `.agents/skills/ytv-start` and `docs/operations/task-contract.md`; inspect actual `plan_summary`, `read_next`, `task_guide`, `reference_documents` pins. Import *exact* chosen script bytes and attached variants/research/story-review under the documented `attach-artifact` mechanism, recording real returned IDs/hashes, without pretending old Git work was an official run.
2. **Independent reviewer unavailable**: current self-review is not a signed or independent `ytv-script-review-v1`. Present the exact 02m EN and RU text to a fresh independent reader without `story-review.md` or beat map; first review interest/comprehension and exact last→first loop with doubled complete Short, then supply the sources. Preserve the reviewer's original schema/response, including a rejection if any. New exact hash requires new independent review.
3. **Short target discrepancy**: 02m draft exceeds channel's usual 35–50 seconds; do not silently accelerate the approved voice or call it production-ready. Confirm if this editorial 2-minute Short is allowed by actual channel runtime, review storytelling and pacing, then only after owner's exact-script approval make storyboard tied to `variants/02m/script.en.txt` hash.
4. **Long unsupported**: ChannelSpec defines only illustrated Short production. 05m/10m texts remain editorial alternatives; do not fabricate a Long run or change channel spec for this candidate.
5. **Actual sound/image/seam/timing unavailable**: no TTS, imagegen, video, MP4, brand reference PNG bytes, or actual AV loop check done; no media asset path/hash claimed. Exact storyboards/prompts deliberately **not created** without accepted variant/reviewer. Rights of future reference materials/media remain UNVERIFIED.
6. **Audience evidence limited**: vidIQ balance 0 and no paid calls; free YouTube indexed results and Reddit questions only. Comparable creator A/B baseline, YouTube comment threads, own channel CTR and retention UNVERIFIED. Do not call public views “retention”.
7. **Owner choice**: choosing 02m in this document is an editorial suggestion, not owner approval. Await exact approved master in a valid run before any audiovisual task. No merge allowed from this assignment.

## Integrity and next steps

Review model arithmetic from `research.md`, ensure true remote tree contains exactly these eleven new files, validate Git blob IDs plus SHA-256 against exact read-back, check branch based on current remote main and GitHub Draft PR target `main`. After the eventual PR is opened, verify its true remote HEAD, changed-file list, status and checks of exact SHA; `queued`/`in_progress` is not success. Maintain the repo's main branch and other agents' work untouched.

This handoff is **not** permission for sound generation, image tools, paid provider calls, MP4, upload or publication.

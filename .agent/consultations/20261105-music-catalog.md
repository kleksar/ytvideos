# Paper Detour music catalog consultation
Task ID: paper-music-catalog-20261105
Prompt: Suggest a concise schema for a reusable narrative-video music catalog that helps editors choose approved recordings by story function rather than assigning one track to each fixed act. Include safeguards for alternate versions, licensing, and evidence without assuming anyone listened to a recording. Keep it brief.
Status: prepared.
URL: https://chatgpt.com/c/6aecd152-732c-83ed-9c8d-bcc753888711
Visible mode: Extra High; model name not separately displayed. Exact prompt posted and composer empty; lock released VERIFIED. Response completed and transcribed from visible UI.

## Complete answer
Use a track-centric, many-to-many catalog: recordings are approved independently, then tagged with multiple narrative functions. Editors select by story need, not by act number or fixed soundtrack sequence.

Recommended schema:
- Identity: track_id, title, composer, source, asset location.
- Classification: genre, style, mood, instrumentation, vocal presence.
- Musical profile: tempo, energy (1–5), intensity, density, dynamics.
- Narrative functions: story_roles[]: hook, curiosity, anticipation, tension, pursuit, revelation, loss, wonder, reflection, resolution, transition.
- Usage guidance: best_for[], avoid_when[], suitable scene characteristics, recommended placement, voice compatibility.
- Editing: duration, intro/outro behavior, loopability, useful edit points.
- Versions: version_id, parent track ID, version type, duration, differences, file hash.
- Approval: status, approved version IDs, approval date, scope, restrictions.
- Licensing: rights holder, license type, source URL, permitted platforms, commercial/monetization rights, territory, expiry, attribution requirements, proof document.
- Evidence: metadata source, technical checks, listening-review status, reviewer, review date, evidence references.

Essential safeguards:
1. Versions are separate assets. Original, underscore, shortened, loop and alternate mixes share a parent track_id. Approval of one version never automatically approves another.
2. Licensing is independently verified. No track becomes production-approved without documented usage rights. Record expiry and platform restrictions.
3. Evidence is not assumed. Distinguish metadata_verified, file_integrity_checked, audio_inspected, listening_reviewed. Each has its own status and evidence. Never mark listening complete merely because a file was processed.
4. Approval is scoped. Specify exactly which recording, version, platforms and uses are approved.
5. No mandatory act mapping. A track can serve several functions, and a function should have several candidate tracks.

Example selection record:
```yaml
track_id: MUSIC_014
genre: cinematic_ambient
energy: 2
story_roles:
  - anticipation
  - reflection
  - discovery
best_for:
  - restrained narration
  - gradual reveals
avoid_when:
  - fast_action
versions:
  - version_id: MUSIC_014_FULL
    status: approved
  - version_id: MUSIC_014_LOOP
    status: pending_review
listening_reviewed: false
license_status: verified
```
Core principle: the catalog describes what a recording can do, when it works, what it requires, and what has actually been verified. It does not prescribe where it must appear in a particular film.

Decision: Use one catalog entry per selected version, label narrative roles as editorial hypotheses, retain source/rights and distinguish user preference from file validation and release authorization.

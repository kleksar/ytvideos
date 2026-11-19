# Native editable subtitle command (first slice)

```sh
python automation/resolve_subtitles/command.py request.json --output channels/CHANNEL/videos/EPISODE/Work/Captions
```

Default is **offline planning only**, never an app connection, ASR call, render or upload.
All speech channels use the same command, but channel/format policy remains authoritative.
This is not yet an automatic replacement for Paper/Nuviko branded on-screen captions.

## Exact inputs and three modes of one command

1. In a coordinator-granted exclusive Resolve slot, run the command with `--inspect
   --exclusive-session`. The request needs `target` with exact saved `project_id`,
   `timeline_id`, `fps`, `raster`, `origin_frame`, `end_frame`. The named project and
   timeline must **already be active**. It never searches by name, opens another
   project, launches Resolve or takes the mouse. Preserve `native-snapshot.json`
   as `request.native_snapshot`.
2. Align the actual final narration represented by that snapshot, not a script,
   old TTS or pre-conform file. Supply `placements`, `words`, explicit `groups`,
   transcript and independently observed timing evidence. Re-run the default command.
3. `--apply-native-cc --exclusive-session` creates an isolated, hash-named candidate
   timeline with an editable native subtitle track. Source timeline is untouched;
   its view is restored. Existing on-screen captions remain unchanged. The optional
   native CC lane is disabled to avoid duplicate visible captions. Open the candidate
   deliberately for playback QA; this is **not** permission to render/publish.

### Request contract

See the small synthetic fixture in `test_planning.py` (not production alignment data).
Seconds accept exact rational strings; Resolve record frames are absolute integers,
with exclusive ends. `target.fps` must be exact, e.g. `30` or `30000/1001`, never an
ambiguous rounded `29.97`. Runtime exact fractional-rate alias support is deliberately
not guessed.

- `placements`: stable native TimelineItem `id`, final file `source_sha256`, source
  `source_in`/`source_out` in seconds, absolute `timeline_start`/`timeline_end`, `speed`.
  Planner maps trim/constant speed exactly and rejects overlaps/nonlinear retimes.
- `words`: `placement_id`, same source hash, source `start`/`end`, exact `text`,
  confidence. Groups are contiguous zero-based word-index lists. Optional
  `keep_together` spans protect names/numeric expressions; no text is invented.
- `evidence`: `kind: timeline_observed`, nonempty provenance `source`, and anchors
  `{placement_id, word_index, timeline_frame, edge: start|end}` spanning first,
  middle and last of every placement. These are measured checks, not a substitute
  for ASR or permission to guess word onsets from arbitrary waveform peaks.
- `native_snapshot`: exact inspection output. Any changed source hash, placement,
  audio/video property, geometry or target rejects apply. Do not copy observations
  from a different audio file or move them to manufacture a PASS.

The **first native adapter supports untrimmed unity-rate narration only**. Trim/speed
math is tested in the planner but native retime readback is not yet proven, so apply
refuses it instead of advertising universal speed support. Confidence/anchors cover
only the supplied evidence. They do not prove every word, pronunciation or playback.
Local drift after pauses must be corrected locally against final speech and rechecked;
a global offset candidate is not auto-applied to speech. The existing
`automation/helpers/srt/scripts/srt_tool.py` comparator and structure/text checks are
reused. Native import may be uniformly misplaced; only after exact count, texts and
all durations agree may `SetPosition` correct that **import-origin offset**, followed
by exact full cue readback. Nonuniform errors abort.

## Backend, editability and failure boundaries

The installed official Blackmagic `ResolveMCP` is initialized over stdio with bounded
requests. `tools/list` must expose the actual supported schemas; `run_script` is the
sandboxed native bridge with injected `resolve`, not `run_script_unsafe`. Official
`search_scripting_api` confirms `TimelineItem.SetPosition`/`startFrame` for that install.
There is no invented dedicated `get_timeline` MCP tool or generic arbitrary-server
option. Files/hashes/SRT are prepared locally; native app operations stay inside
Resolve. No FFmpeg subtitle assembly, flattening, rendering or publication is used.

The native track uses `ImportMedia` → `AppendToTimeline` → exact cue readback. SRT
being in Media Pool alone is never counted as authored. An unchanged owned candidate
is read back before returning `UNCHANGED`; name collisions or modified candidates
are refused. Uncertain/failed candidates are retained disabled for diagnosis, not
silently deleted or overwritten. A failed/timed-out mutation is UNKNOWN: inspect app
state before retrying; do not duplicate imports on a guessed failure. Only one worker
may mutate the instance; the CLI flag records a grant, it cannot enforce other agents.

`plan.json` records channel style/geometry. Native CC style remains the app's timed-text
style: the command **does not install profile-branded Text+ or a word-highlight layer**.
`branded_style: NOT_APPLIED`, `visual/playback: UNVERIFIED` are intentional blockers for
claiming a complete screen-caption migration. Paper/Nuviko settings are not flattened
or replaced with a generic font. Existing legacy renderers are not removed or migrated.

For the later branded implementation, the verified Paper route uses native transparent
Background → Text+ word nodes → Merge → MediaOut on a dedicated owned lane, followed by
`.comp` save and unconditional import/activation. Live direct-graph node values alone
once looked valid while output was blank. A native compositor sample before/on/after
real word boundaries and every section is required; this command does not yet perform
that authoring. Channel-approved geometry, fonts, grouping and gaps must remain separate.

## Evidence and acceptance

Automated: `python -m unittest discover -s automation/resolve_subtitles -p 'test_*.py'`.
Synthetic tests cover mapping, pauses/local drift, protected groups, source replacement,
uniform import only, collision/idempotence and restoration failures. They are not a live
Resolve authoring proof. On 2026-11-19 the command's official MCP transport, `run_script`
identity/snapshot and installed positioning API discovery were exercised **read-only**
on Resolve Studio 21.2; insertion by this reusable command remains unverified until a
coordinated disposable-target test. Prior episode-specific SRT placement and editable
Text+ proof do not upgrade this command's status.

Before acceptance: inspect exact cue starts/ends/text, preserved VO and picture, visible
safe area and no double captions; play early/middle/late, pause/resume and shot joins in
Resolve. Save/reopen and repeat relevant readback. For separate selectable captions,
round-trip a timed SRT and follow the shared delivery workflow; MP4 upload is not CC
transport. Use native Resolve review/delivery only, and never publish for a caption test.

# Native editable subtitle command

```sh
python automation/resolve_subtitles/command.py request.json --output channels/CHANNEL/videos/EPISODE/Work/Captions
```

Default is **offline planning only**, never an app connection, ASR call, render or upload.
All speech channels use the same command, but channel/format policy remains authoritative.
This is not yet an automatic replacement for branded on-screen captions on any channel.
`--apply-native-captions` fails closed: the independently editable, exactly styled
per-phrase authoring route has not been implemented/proven. Plain CC is not its fallback.
All channels require the [independent phrase delivery gate](../../.agents/skills/ytv-resolve/references/timeline.md#independent-phrase-delivery-gate).

## Exact inputs and modes of one command

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

The **first native adapter supports zero-source-in unity-rate narration only**. Trim/speed
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

## Legacy section-based branded recipe (reference/recovery only)

This previously verified path attaches a graph to picture sections: it does **not**
provide an independently movable timeline clip per semantic phrase. It is not the
current production default, even though Text+ nodes inside it are editable. The CLI
rejects it without the explicit recovery flag. Recovery is not delivery acceptance.
The future production route must use native Subtitle Track Style when actual app
proof matches the exact approved style, or separate real native Fusion Title items
per phrase. Do not invent a supported style API, remove whole-phrase holds to fit CC,
or claim automatic white text/Georgia/background application from SRT import.

## Historical bounded recipe details

`--apply-branded --legacy-reference-recovery --exclusive-session` adds a dedicated editable Text+ lane to a new
owned candidate, and independently authors disabled native CC from speech timings.
It uses the same verified final-VO/source snapshot as `--apply-native-cc`. Supply:

```json
{"branded": {"recipe_id": "paper-short-v09", "existing_screen_caption_tracks": [],
  "shots": [{"id": "shot-01", "carrier_id": "EXACT_NATIVE_ITEM_ID",
    "start_frame": 0, "end_frame": 30}]}}
```

Shots are ordered, contiguous, absolute half-open intervals covering the selected
caption groups. Each carrier must be an existing unity-rate source video item covering
that interval. Explicit replacement tracks are disabled **only on the candidate**;
otherwise original tracks remain unchanged. Existing burned-in text cannot be removed
by this command: use a clean approved source, never silently double it.

Calibrated recipes are **Paper Detour Short, Flagship v09, 1440×2560** with installed
Chalkboard SE Bold, and **Nuviko History Long, 2560×1440**, `nuviko-history-long-native-v1`,
with Georgia Bold. These are separate recipes, not universal raster/style substitutions.
An unsupported recipe, changed active colors/font/raster, missing font or over-wide
phrase fails rather than substituting, shrinking or flattening. Nuviko preserves case, the 84 px reference metrics, baseline 1288 and rectangular
80%-alpha panel (top1193, height135, horizontal padding29) from canonical long/Nuviko
profiles. Its native glyph size and anchor were separately sampled on caps/descenders;
the Paper native values are not copied. Legacy renderers are not removed or migrated.

A group can persist through a picture cut, including a word spanning that cut; a new
group starts only at its authored boundary. Highlight follows actual word intervals,
neutral text persists through internal pauses. Speech-only SRT does not inherit display
holds. `partition.py` tests these independently of typography and native authoring.

The installed official MCP bridge creates native transparent Background → Text+ words
→ Merge → MediaOut, serializes each `.comp`, then unconditionally imports and activates
it. This rebind is essential: live-created graph values once looked valid while actual
output was blank. Exact text, geometry, phrase intervals and source state are read back;
a repeated unchanged request reuses the same owned candidate. Receipts distinguish
`NATIVE_AUTHORED` from `visual/playback: UNVERIFIED`: a successful graph import is not
visual or listening QA. Use native compositor samples around word/group/cut boundaries
and native playback before accepting. No render, upload or source timeline replacement
is performed.

## Evidence and acceptance

Automated: `python -m unittest discover -s automation/resolve_subtitles -p 'test_*.py'`.
Synthetic tests cover mapping, pauses/local drift, protected groups, source replacement,
uniform import only, collision/idempotence and restoration failures. They are not a live
Resolve authoring proof. On 2026-11-19 the command's official MCP transport, `run_script`
identity/snapshot and installed positioning API discovery were exercised **read-only**
on Resolve Studio 21.2. A subsequent disposable three-second PCM-pulse fixture exercised
this exact command: three native cues at frames 6–12, 36–42 and 66–72, a proven uniform
+90-frame import-origin correction, then CREATED → UNCHANGED with the same candidate
identity and no second import. Source snapshot/file hash stayed unchanged and the prior
production view was restored. This proves native insertion/readback/idempotence, **not**
real-speech alignment quality, branded text, caption appearance or listening QA.

Two native 21.2 differences are regression-covered: inactive timeline track-enable
getters returned false, so source flags are captured while active and candidate flags
are checked only while it is active; a duplicate omitted entirely unused disabled AI
audio defaults. Comparison normalizes only Voice Isolation/Dialogue Leveler families
whose values are all false/zero, never enabled or nonzero latent settings. The exact
source snapshot itself is not normalized. A subsequent disposable Paper fixture exercised this command's branded path using a
short excerpt of the approved final VO, four picture sections and three independent CC
cues. CREATED → UNCHANGED retained one candidate; the original production view was
restored. Twelve actual native compositor samples verified neutral pause hold across
a cut, highlight across a mid-phrase cut, and a new group at an intentional boundary.
This is bounded Paper visual evidence, not full narration alignment/listening QA or
unseen profiles. A separate Nuviko-style fixture used the same approved speech excerpt
(not a new Nuviko narration), its canonical long raster/font/panel and native full-span
holds: CREATED → UNCHANGED, exact graph/CC readback and 18 compositor samples covering
first/last holds, pause and phrase/word/cut transitions. The Nuviko creation was observed in the live tool output; the retained receipt/logs
were overwritten by the successful UNCHANGED recheck and are not an original CREATE
receipt. This validates that recipe, not every channel or
word of a production episode. No production project content was modified or exported.

Before acceptance: inspect exact cue starts/ends/text, preserved VO and picture, visible
safe area and no double captions; play early/middle/late, pause/resume and shot joins in
Resolve. Save/reopen and repeat relevant readback. For separate selectable captions,
round-trip a timed SRT and follow the shared delivery workflow; MP4 upload is not CC
transport. Use native Resolve review/delivery only, and never publish for a caption test.

Native 21.2 may replace the sole newly-created Fusion composition during import rather
than append a new name. Only that unambiguous singleton or one uniquely new name is
accepted. Both the returned imported graph and explicitly activated graph are checked:
transparent background/raster, exact Text+/Merge topology through MediaOut, optional
panel mask/color/geometry, word expressions and phrase intervals. Mock corruption tests
include disconnected output, wrong foreground/background, opacity and raster changes.

### Optional phrase start on a declared picture cut

This is **not** a global caption quantization rule. Default speech/hold timing stays
unchanged for every channel. For a deliberately associated shot whose cut is a few
frames after a phrase starts, branded requests may explicitly declare:

```json
{"display_cut_anchors": [{"cue_id": "C0002", "shot_id": "shot-02", "start_frame": 1038}]}
```

Place this inside `branded`. The cue ID comes from `plan.json`; the absolute integer
frame must equal that shot's declared start. Native apply additionally requires the
source carrier clip itself to start there: splitting a title section inside an
unchanged picture does not create a qualifying cut. That clip boundary is **not proof
of a visible composite cut**: an upper track can cover it. The declared cue-to-shot
association must come from the authoritative editorial plan; inspect the actual native
composite before/on/after the cut and listen to the phrase before production use or
handoff. This first bounded adapter accepts
an anchor only during the phrase's **first spoken word**, before its exclusive end.
Earlier anticipation and a delay hiding an entire word are rejected, not guessed.

Precedence is explicit display anchor, then unchanged channel display policy. Only the
new phrase's visible start changes. If the previous cue originally held continuously
up to that boundary, its neutral tail extends to the declared cut; an intentional
existing display gap remains a gap. The former phrase cannot keep highlighting a word
past its actual speech end. A phrase without an anchor continues normally across cuts.
Word intervals, transcript, spoken cue boundaries, VO and accessibility SRT are immutable;
the new phrase's first word highlights only its remaining audible intersection. This
means the hidden prefix is an explicit editorial tradeoff, not repaired alignment.

Unknown/duplicate cue IDs, non-cut/fractional frames and conflicting intervals fail.
The anchors and resulting layout enter candidate identity. Review the preceding/on-cut/
following native frames and the audible phrase before acceptance. Offline regressions
cover late cuts, pause holds, cross-cut speech and immutable CC. The optional anchored
path has **not yet received a live native fixture**; this does not upgrade its playback
or visual status, and it never authorizes changes to a production timeline.

## Legacy artifact inventory and migration boundary

- `automation/subtitles/nuviko_long_subtitles.py` renders transparent word-highlight
  **MOV** overlays (including ProRes 4444), not an editable Subtitle track.
- `automation/helpers/paper-captions/scripts/render_paper_captions.py` creates raster
  caption imagery; `automation/image_motion/layered_render.py` composites layers.
  These tools remain for pinned historical reconstruction/reference, not a silent
  fallback for the active Resolve caption route. Do not call every old artifact MP4:
  inspect its actual codec/container and timeline role.
- `branded_native.py` creates editable node graphs on section carriers, with separate
  disabled CC. Its historical visual fixtures do not establish per-phrase clip editing.
- `native.py` imports independent native Subtitle cues, currently disabled as separate
  accessibility CC. It does not apply the channel's branded visual style or display holds.

Next implementation proof: isolated candidate, actual supported Track Style or native
Title creation, exact whole-phrase display partition and typography, per-cue Inspector
edit/move/restore, old-carrier removal on candidate, save/reopen/readback and native
playback. Keep production blocked until these checks pass; do not enable plain ST1 as
an unapproved temporary branded substitute. No Resolve call or new live fixture was
performed for this routing guard; prior bounded evidence above remains historical.

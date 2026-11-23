# Native editable subtitle command

```sh
python automation/resolve_subtitles/command.py request.json --output channels/CHANNEL/videos/EPISODE/Work/Captions
```

Default is **offline planning only**, never an app connection, ASR call, render or upload.
All speech channels use the same command, but channel/format policy remains authoritative.
This is not yet an automatic replacement for Paper/Nuviko branded on-screen captions.

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

## Branded editable captions (bounded native recipes)

`--apply-branded --exclusive-session` adds a dedicated editable Text+ lane to a new
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
Resolve. Read back the actual editable Text+ composition and inspect the native
compositor at the title's first, middle and last frames and just before/on/after
cue boundaries. If a per-word highlight overlay duplicates or misaligns glyphs,
reject it: use one inline character style in the editable text, or the approved
unhighlighted base only. Do not stack duplicate titles to simulate a highlight.
Save/reopen and repeat relevant readback. For separate selectable captions,
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

## Offline one-still-per-phrase conform

For a new cut from already approved narration, phrase breaks and stills, align the
**actual final PCM WAV** offline using
[`forced_alignment.py`](../helpers/srt/scripts/forced_alignment.py), or supply
equivalent exact-transcript word evidence in the same format. Align after any
pitch-preserving retime and pause edits; do not scale timestamps from the raw TTS
or use ASR text as a replacement script. The alignment format is
`{status:"REVIEW_REQUIRED",audio_sha256,transcript_sha256,words:[{text,start,end,score}]}`.
Its transcript hash is of the UTF-8 text after outer whitespace is stripped;
quoted word forms follow the existing helper. Use your existing local model
cache; the planner never loads a model or connects to a service.

```sh
python3.12 automation/resolve_subtitles/phrase_conform.py request.json --output phrase-plan.json
```

The schema-1 JSON request requires `fps` (exact integer or ratio string), the
absolute, half-open `origin_frame` and `end_frame`, `audio_start_frame`,
`audio:{path,sha256}`, `transcript_path`, `alignment_path`, and ordered
`phrases:[{id,text,asset_path,asset_sha256}]`. Input paths may be absolute
or request-relative. Use Python 3.12+ when the PCM file is WAVE_FORMAT_EXTENSIBLE.
Each still must already be approved; file hashes prove identity, not image QA.
Optionally specify per-shot `titles:[{id,text}]` for explicit readable subcues
that exactly partition a long visual beat. They cannot cross picture cuts.

The JSON output has `shots:[{id,start,end,asset_path,asset_sha256}]` and
`titles:[{id,start,end,text,words:[{text,start,end}]}]` on the same absolute
frame axis. Quantize speech to nearest frame, half up. Every shot after the
first starts at its first title onset. The first picture may lead silent
preroll; the final picture holds to the declared end; the titles use measured
spoken bounds and never stretch the audio or close its pauses. This describes
individual titles for native assembly later, not a Resolve import format.
A word whose endpoints fall on one frame cannot carry an independently
visible highlight. Normal planning refuses it; diagnostic mode flags it.

Use `--timing-only` if approved stills are not yet present: missing asset
fields are permitted and named in `missing_art`. Missing or low (<0.80) word
confidence is reported in `timing_flags` in that mode; normal planning refuses
these words until alignment is reviewed. Values outside [0,1] always fail. This output is explicitly
`TIMING_ONLY`, not for native install. Complete hash-covered output is still
`OFFLINE_REVIEW_REQUIRED`: listen at representative word/cut onsets, check
any local alignment drift, line breaks and style, then follow the native
workflow above using the real timeline snapshot and independent evidence.
This command never opens Resolve, adds clips, renders, or publishes.

## Offline spacing between voice clips

For isolated PCM takes, `python3 -m automation.resolve_subtitles.voice_spacing --help`
describes the separate offline trim and spacing planner. Follow the
[Resolve skill for voice spacing](../../.agents/skills/ytv-resolve/references/voice-spacing.md)
to apply and verify the resulting plan. The planner does not open Resolve, write
original WAVs, or render a video.

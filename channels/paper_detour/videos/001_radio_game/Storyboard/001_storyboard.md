# Rarovista 001 — production storyboard

**Status: draft production plan aligned to recorded English scratch narration; not reviewed by ear and no finished animation.** Duration **04:46.640 (286.640 s)**, 16:9, 50 planned shots. The intervals cover the whole MP3 continuously, including pauses and its tail. This is not a guarantee of sample-accurate audible cuts: the word alignment is machine-generated; an editor must listen and adjust.

## Source and timing method

- Narration: [`voice_en.mp3`](../Source/Voice/draft_v1/voice_en.mp3), SHA-256 `e44f67690da35e4587153a4b4e95a40f670be418664547d960b3ec077c1bb512`. Duration measured by ffprobe.
- Spoken text: [`script_en.txt`](../Source/Voice/draft_v1/script_en.txt), SHA-256 `e2858774bee94bd308746eb3ead8d5034f91b4738581a84d282a761094a2649b`; editorial source [`001_en_script_v2.md`](../Script/001_en_script_v2.md). Word-alignment metadata has the same submitted-text hash.
- Timing: [`voice_en.words.json`](../Source/Voice/draft_v1/voice_en.words.json), derived from [`voice_en.alignment.json`](../Source/Voice/draft_v1/voice_en.alignment.json). Every anchor was matched uniquely and in sequence to its words. Each start is the machine-aligned first word of its cue, except shot 01 starts at audio zero. Each end is the next start. Final word ends at 04:46.480 per word alignment, while a punctuation timestamp in the raw alignment extends to 04:46.800; the final interval is capped at the measured MP3 end **04:46.640**.
- Anchor phrases identify cut positions; the whole intervening spoken text continues through each interval. Cut 28 deliberately starts mid-sentence. Figures use millisecond display, which does **not** imply millisecond perceptual accuracy. The English alignment applies only to this audio at its present speed; re-align after edits, speed changes, or new dubbing.
- Compare cuts and pauses against the audio before animation lock; this document was not checked by listening. SFX/music below are proposed, not yet recorded or mixed. Any added opening/ending or signal sound will change the final edit and requires resynchronization.

## Visual reference and factual rules

The concept sheet [`001_storyboard_concept.png`](001_storyboard_concept.png) is a **nine-panel mood reference**, not nine finished frames or documentary evidence. Number panels 1–9 left to right, top to bottom: 1 supports shots 01–03, 2 shots 04/24–25, 3 shots 14–20/26, 4 shots 18–21, 5 shots 07–08, 6 shots 33–38, 7 shots 39–40, 8 shots 41–43, 9 shots 46–50. Adapt its cream paper, orange accents, dark radio/cassette shapes and playful character to the approved mascot [`mascot-paper-concept.png`](../../../brand/mascot-paper-concept.png). Concept studio, devices, waves, computer screens and textures are illustrations, not verified historic images. Scene assets must be built separately.

Maintain language-independent 2D 16:9 compositions and readable silhouettes at phone size; do not bake English words or dubbing-specific lip sync into backgrounds. Keep all names, labels, captions, and `Sound reconstruction` as removable language layers. For PT-BR and ES use the same shot IDs as editorial references, record natural translations, then recompute their timing from each actual dub; adjust scene holds to speech rather than speeding a dub to fit.

Distinguish the archive's episode 102 / 1987 / MSX attribution from Kai's later online recording and **reported** Avenger match. The identity of the two copies has not been independently established. Six blocks are based on the published instructions; no independent decoding or demonstrated game launch is claimed. Generic radio static and graphics are reconstructions: do not present them as actual signal. Clear rights before including historical audio, actual game imagery or third-party music. Details: [`FACT_CHECK.md`](../Research/FACT_CHECK.md).

## Shot-by-shot edit plan

Times are relative to the first sample of `voice_en.mp3`; start inclusive, next boundary exclusive. Cut and sound directions are proposals; where no transition is specified, cut cleanly on the next anchor. A long shot should contain the described internal movement rather than a frozen image.

| Shot | In → out | Length | Spoken anchor | Frame, action, transition | Sound / editable layers / factual boundaries |
|---|---|---|---|---|---|
| 01 | 00:00.000 → 00:03.200 | 3.200 s | Imagine hearing a computer game on the radio. | Wide, paper explorer beside a small radio on a table; slow push toward the dial. | Narration clean; radio ambience under voice. |
| 02 | 00:03.200 → 00:06.720 | 3.520 s | Not the music from the game. | Close-up: musical notes appear from speaker, then cross out and transform into an abstract game controller. | Light musical hint fades, original SFX only. |
| 03 | 00:06.720 → 00:14.800 | 8.080 s | To your ears, it might sound | Extreme close-up speaker cone; jagged lines move across cream paper, then a tiny computer turns toward them. | Short original illustrative electronic tone; localized `Sound reconstruction` caption shown with it. |
| 04 | 00:14.800 → 00:20.080 | 5.280 s | In the nineteen-eighties, a Brazilian radio show | Map silhouette; radio tower appears at São Paulo and beams a waveform across the frame. Match cut into the signal. | A generic drawing, not a claim about the actual station's appearance. |
| 05 | 00:20.080 → 00:26.160 | 6.080 s | Years later, someone found an old recording | Timeline paper strip rolls from radio to modern anonymous laptop operator. | No portrait of Weber Kai; no precise number of years asserted. |
| 06 | 00:26.160 → 00:32.000 | 5.840 s | What they reported finding takes us back | Tape reels spin like a loading icon; explorer swaps an abstract download arrow for a cassette. | Whir effect; no claim that consumer Internet or download button existed during this broadcast. |
| 07 | 00:32.000 → 00:34.720 | 2.720 s | The show was called Clip Informática. | Medium: paper radio studio, the character places an editable name card by the receiver. | `Clip Informática` in a removable localized typography layer. Studio is a reconstruction. |
| 08 | 00:34.720 → 00:39.840 | 5.120 s | It aired on Rádio USP in São Paulo | Zoom out from transmitter to map pin; broadcast rings radiate. | `Rádio USP / São Paulo` optional text layers. |
| 09 | 00:39.840 → 00:44.800 | 4.960 s | An archive preserves a recording | Archive box opens; labeled audio reel and a photograph-shaped blank card slide into view. | Number `102` optional localizable layer; do not show an authentic tape image. |
| 10 | 00:44.800 → 00:53.520 | 8.720 s | The archive dates its copy | Close-up date sticker on the box, then a generic MSX-style silhouette appears separately. | `1987 — archive attribution`, localizable. Do not imply identification of archive copy with the later video has been independently established. |
| 11 | 00:53.520 → 00:58.160 | 4.640 s | Now, when we say software audio | Character waves away a speech bubble containing code; speech bubble becomes a waveform. | Graphic only, no actual narration from archive. |
| 12 | 00:58.160 → 01:01.440 | 3.280 s | We mean the program was represented by sound. | Waveform travels into a cassette, which glows briefly; hold before next question. | Subtle illustrative beep sequence, not archival audio. |
| 13 | 01:01.440 → 01:06.480 | 5.040 s | Which raises an obvious question | Explorer places ear to cassette; big hand-drawn question mark floats above. | No hardcoded English question. |
| 14 | 01:06.480 → 01:10.320 | 3.840 s | To answer that, we need to look | Camera moves through cassette housing to tape strip; match cut to close-up moving tape. | Tape whir, under narration. |
| 15 | 01:10.320 → 01:14.640 | 4.320 s | A cassette stores changing patterns | Side-on diagram of tape moving past a read head. Explorer points to the strip. | Physically schematic; no invented microscopic claim. |
| 16 | 01:14.640 → 01:20.400 | 5.760 s | Those patterns can be played back as sound. | Tape strip becomes a smooth voice/music waveform; an abstract note floats out. | Original sound, not a song or copyrighted recording. |
| 17 | 01:20.400 → 01:25.120 | 4.720 s | But a tape can also hold a sequence | Waveform switches to repeated tone patterns; compatible computer icon listens at frame edge. | Different tones presented as a schematic, not an exact MSX encoding. |
| 18 | 01:25.120 → 01:28.720 | 3.600 s | Computers work with bits | Split screen: editable large `0` and `1` blocks at left, different schematic waves at right. | Numbers as separate layer; pattern-to-bit mapping is conceptual only. |
| 19 | 01:28.720 → 01:33.520 | 4.800 s | A cassette system can represent | Explorer slides blocks onto a conveyor and waves emerge; follow wave across frame. | A single simple visual relationship per cut. |
| 20 | 01:33.520 → 01:39.840 | 6.320 s | A compatible computer listens | Wave enters drawn computer; blocks reappear and stack into an abstract file. | Avoid recognizable game graphics. |
| 21 | 01:39.840 → 01:47.760 | 7.920 s | Imagine a message written in whistles. | Character hears a jumbled scribble, while the computer sees the blocks resolve. | Sound reduced under speech for intelligibility. |
| 22 | 01:47.760 → 01:58.160 | 10.400 s | Different machines used different formats | Two differently shaped sockets/cards; one fits, one does not; explorer tests them. | Demonstrates compatibility without inventing brand-specific hardware. |
| 23 | 01:58.160 → 02:00.000 | 1.840 s | Now follow the signal. | Wide canvas cleared; explorer points at a single arrow path beginning at radio tower. | Quick reset in music; arrow is no text. |
| 24 | 02:00.000 → 02:02.640 | 2.640 s | A radio station can broadcast sound. | Station waveform radiates to a home radio in a simple map-like layout. | Transmission is a schematic; do not claim the actual studio's setup. |
| 25 | 02:02.640 → 02:06.880 | 4.240 s | A listener with suitable equipment | Home radio connects to cassette recorder; record button lights. | Generic imaginary listener; no factual claim about specific listener. |
| 26 | 02:06.880 → 02:09.920 | 3.040 s | And a compatible computer can read | Cassette inserts into tape player, cable to computer; data blocks assemble. | Fictional machine as educational illustration. |
| 27 | 02:09.920 → 02:14.107 | 4.187 s | Link those steps together | Pull back to see entire connected chain at once, then follow a moving arrow. | Distinct icons maintain readable silhouette on mobile. |
| 28 | 02:14.107 → 02:19.120 | 5.013 s | not as a picture of a game | Cross out a picture floating through the air; retain the audio wave along the chain. | Avoid suggesting a reproduced copyrighted game screen. |
| 29 | 02:19.120 → 02:23.120 | 4.000 s | The radio carries the sound. | Cut close: waveform passes radio; cut to computer decoding blocks. | Two short sync accents. |
| 30 | 02:23.120 → 02:29.760 | 6.640 s | And just as a cassette could sound | Wave gets noisy and stretched; tape player speed indicator drifts. | Original SFX must be schematic; preserve voice clarity. |
| 31 | 02:29.760 → 02:34.320 | 4.560 s | If the computer couldn't reliably tell | Machine hesitates on mismatched marks; a neutral retry icon appears. | No numeric failure rate or invented listener outcome. |
| 32 | 02:34.320 → 02:43.840 | 9.520 s | For a listener who wasn't expecting it | Split view: explorer puzzled by squeal; second stylized recorder captures the wave. | Clearly hypothetical, not documented listener behavior. |
| 33 | 02:43.840 → 02:48.400 | 4.560 s | Fast-forward to a much later listener | Transition from cassette spool to laptop circle. Explorer follows wave onto a modern screen. | Anonymous silhouette; no realistic portrait of Kai. |
| 34 | 02:48.400 → 02:55.440 | 7.040 s | Kai set out to decode an online recording | Browser-like rectangle with generic waveform opens; editable `episode 102` label. | It is the recording Kai identifies, not a verified direct image of the archive. |
| 35 | 02:55.440 → 03:02.000 | 6.560 s | We haven't independently established | Two separate boxes remain apart, with a dotted question mark between them. | Localized `Same copy?` layer optional; keep visible uncertainty. |
| 36 | 03:02.000 → 03:06.800 | 4.800 s | The available recording, Kai wrote | Quiet waveform becomes visibly small, then compresses horizontally as playback speeds up. | Avoid representing manipulated graphic as actual evidence. |
| 37 | 03:06.800 → 03:17.440 | 10.640 s | That matters | Demonstrate changing tape speed and pitch using an abstract oscillation. | Generic original two-tone illustration; not actual measured values. |
| 38 | 03:17.440 → 03:22.480 | 5.040 s | Kai extracted the relevant section | Scissors isolate an abstract wave in a laptop timeline; the section moves to a decoder icon. | No screen recreation claiming to be the real app. |
| 39 | 03:22.480 → 03:28.720 | 6.240 s | The published instructions describe six output files | Six blocks slide from decoder, numbered with editable text, evenly spaced. | Six is attributed to published instructions, not independently reproduced. |
| 40 | 03:28.720 → 03:31.600 | 2.880 s | Six blocks — but blocks of what? | Close-up: six blank blocks; explorer points and the frame pauses briefly. | Silence/music dip to set up the reveal. |
| 41 | 03:31.600 → 03:36.000 | 4.400 s | Kai compared the recovered data | Second row of abstract blocks approaches; paired blocks align. | Schematic comparison only; not a depiction of an independently verified byte-by-byte test. |
| 42 | 03:36.000 → 03:38.720 | 2.720 s | The developer reported that the data matched. | Title card `Avenger` appears above blocks, with subtle attribution `reported match` as a removable language layer. | Do not show a specific version, publisher or gameplay. |
| 43 | 03:38.720 → 03:47.120 | 8.400 s | That's a striking result, with a boundary. | Frame divides: reported match on one side, outlined unverified monitor with question mark on other. | Visual boundary is essential; do not turn uncertain result into a confirmed launch. |
| 44 | 03:47.120 → 03:54.480 | 7.360 s | We haven't independently repeated the decoding. | Explorer sets down magnifying glass; generic not-yet-checked mark. | On-screen text optional, no suggestion of independent replication. |
| 45 | 03:54.480 → 04:01.360 | 6.880 s | The archive, meanwhile | Return to archive box; its `MSX` label remains visible while the separate `Avenger` card stays with Kai's report. | Distinguish what each source actually says. |
| 46 | 04:01.360 → 04:13.840 | 12.480 s | Still, think about the journey. | Reconstruct chain as a single continuous graphic across the canvas; history and modern laptop endpoints remain distinct. | Preserve audio sequence and historic uncertainty. |
| 47 | 04:13.840 → 04:19.040 | 5.200 s | The message survived in a form | Wave flows into a generic recording symbol and then abstract data blocks; do not visually identify it with the archive copy. | Avoid asserting provenance of a specific tape beyond sources. |
| 48 | 04:19.040 → 04:25.520 | 6.480 s | The trick wasn't a secret picture | Graphic image icon is replaced by data blocks which become sound. | Follow voice; no unnecessary text. |
| 49 | 04:25.520 → 04:33.040 | 7.520 s | A cassette could carry that sound. | Three quick clean match cuts: cassette, radio tower, computer. | Soft clicks per transition, not archive audio. |
| 50 | 04:33.040 → 04:46.640 | 13.600 s | What sounds like noise to us | Final wide: explorer and radio, wave dissolves into small blocks; hold through end of final phrase. | Music soft ending; no invented claim the decoded game was played. |


## Handoff checks

1. Listen through the full voice and place or adjust all cuts on natural breaths; inspect especially the mid-sentence cut 28 and the ending. Machine alignment is a starting point, not a listening review.
2. Build drawings and animate each shot; verify timing and graphic legibility with the actual audio, including pauses. Build localized labels and keep an effects/music stem separate from narration.
3. Check any proposed illustrative tone is labeled and not confused with archive audio. Confirm the fictional nature of people, studio and visual devices, and clear rights for any third-party media.
4. Track what actually changes in the final audio mix and regenerate all shot timings / subtitles when required. Preserve attribution and the limits in the narration and visuals.

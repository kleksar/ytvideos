# Paper Detour 009 — voice and screen-text plan v04

**Status:** Palmier v04 edit is assembled for review. Preserve v03 as the comparison timeline. No v04 MP4 export has been requested.

## Final voice

Source: [`Source/Voice/roger_v2_20261101/narration_en.txt`](../Source/Voice/roger_v2_20261101/narration_en.txt). The recorded English narration is 33.646 s; cue timing comes from the matching ElevenLabs character alignment and derived word spans in `Source/Voice/roger_v2_20261101/voice_en.alignment.json` and `voice_en.words.json`. Alignment ends 0.034 s after the MP3 container duration (within one 30 fps frame). Use this recording as-is; if the words, voice or speed change, regenerate the word spans and every cue time.

> Why is a cat in a Maya scholar’s arms on a monument in Mérida?  
> In 1952, Yuri Knorozov argued that many Maya signs represented syllables, helping unlock their script.  
> But the cat had nothing to do with that breakthrough.  
> Asya became his Siamese companion years later. According to a former student, Knorozov even tried to credit her as a coauthor of research on signaling.  
> So why include her?  
> Because the monument recreates a famous photograph of Knorozov holding Asya in his arms.

The story opens with the odd statue, gives the historical discovery, separates Asya from the 1952 work, attributes the coauthor anecdote to a former student, then answers the statue question. It does not claim that Asya helped decipher Maya writing or that the coauthor credit appeared in the published paper.

## Scene cuts

All frames below are 30 fps project frames. Cuts follow the completed spoken thought and keep each full-frame composition intact.

| Order | Scene file | Frames `[start,end)` | Seconds | Spoken beat |
|---|---|---:|---:|---|
| 1 | `S01_opening_merida_monument.png` | `[0,146)` | `0.000–4.867` | Opening question and statue |
| 2 | `S02_knorozov_study.png` | `[146,246)` | `4.867–8.200` | 1952; Knorozov argued that |
| 3 | `S03_codex_research.png` | `[246,335)` | `8.200–11.167` | Many Maya signs and syllables |
| 4 | `S05_researchers.png` | `[335,400)` | `11.167–13.333` | Helping unlock the script; cue 3 exits after `script` |
| 5 | `S04_codex_detail.png` | `[400,488)` | `13.333–16.267` | The cat was unrelated to that breakthrough |
| 6 | `S06_asya_companion.png` | `[488,596)` | `16.267–19.867` | Asya appears years later |
| 7 | `S07_coauthor_joke.png` | `[596,742)` | `19.867–24.733` | Former student’s coauthor anecdote |
| 8 | `S08_signals_paper_v04.png` | `[742,842)` | `24.733–28.067` | Research on signaling; question |
| 9 | `S09_merida_return.png` | `[842,1020)` | `28.067–34.000` | Photograph and monument payoff |

## Accent cues and alignment

Each start is the first relevant word in the v2 recording. `Voice span` gives the exact spoken span; `clip` includes the brief hold and exit. A title must not begin early merely because a scene begins earlier. Coordinates are normalized visible-title centers, not PNG-canvas corners. Titles use `alpha_trimmed/` bounds and preserve aspect ratio.

| # | Spoken trigger and aligned span | Display clip `[start,end)` | Title PNG (line break) | Scene coverage | Anchor center | Visible height | Collision decision |
|---:|---|---:|---|---|---|---:|---|
| 1 | `Why` `0.00–0.32`; opening question through `Mérida?` `3.80–4.88` | `[0,152)` | `THE MYSTERY` / `IN STONE` | S01; fades for 6 frames over S02 | `(0.50, 0.08)` | `0.084H` | Approved alternate above the monument; avoids statue head and cat. The title is 6.7% smaller to fit that exact sky pocket. Check Shorts UI safe margin separately in vertical-player preview; that overlay has not been checked. |
| 2 | `1952` `5.12–6.48`; thought ends `argued` `7.60–8.00` | `[154,246)` | `A KEY TO MAYA` / `WRITING` | S02 only; exits before S03 | `(0.50, 0.13)` | `0.090H` | Upper-center field; clear of face, hands, sheet and lamp. Five-frame exit follows `argued` and finishes before the page edge enters. |
| 3 | `signs` `9.04–9.44`; thought ends `script` `12.36–13.12` | `[271,400)` | `THE GLYPHS` / `COULD SPEAK` | S03 and S05; exits before S04 | `(0.50, 0.08)` | `0.090H` | Approved alternate above the page edge. Keep this anchor through both scenes. Full readability holds through the final word; the 5-frame fade starts at frame 395, after `script`, and ends at 399 before the close-up page at 400. |
| 4 | `Asya` `16.28–16.56`; thought ends `later` `18.80–19.68` | `[488,596)` | `A COMPANION,` / `NOT A CODEBREAKER` | S06 only | `(0.50, 0.13)` | `0.090H` | Upper-center field, clear of Knorozov’s head, Asya’s head and face. |
| 5 | `former` `20.48–20.64`; anecdote reaches `coauthor` `23.76–24.32` | `[614,738)` | `COAUTHOR?` / `ONE STUDENT SAYS` | S07 only | `(0.50, 0.13)` | `0.090H` | Upper-center blue field, clear of both heads and cat. Attribution stays visible while the claim is stated. |
| 6 | `photograph` `30.36–30.88`; final phrase ends `arms` `32.96–33.68` | `[911,1018)` | `FROM PHOTOGRAPH` / `TO STONE` | S09 only | `(0.50, 0.13)` | `0.090H` | Upper-center night sky, clear of monument, trees and church towers. Appears on `photograph`, not at the start of the preceding sentence. |

Animation: 4-frame opacity/position entrance, fixed anchor through hold, and a smooth exit. Interpolation is smooth from the `D−5` hold point to `D−1`; never set `hold` on the exit point. Cue 2 exits in 5 frames after `argued` and is gone at frame 246, before the S03 page appears. Cue 3 holds through `script` and fades during frames 395–399; it is fully gone before the S04 codex close-up at frame 400. Keep each title within its selected safe area; no overshoot or travel across a face/object. Font styling follows [Paper typography](../../../brand/TYPOGRAPHY_STANDARD.md).

## Preflight frames

The contact sheet is [`Previews/Accents_v04_20261101/contact_sheet.png`](Previews/Accents_v04_20261101/contact_sheet.png). Its tiles are in numeric filename order. It includes every scene a cue appears over. S03 is checked without cue 2 because it exits before the cut; S04 is checked without cue 3 because it exits before the page close-up. Cues 1 and 3 use the one approved alternate anchor `(0.50, 0.08)` for distinct scene collisions; all other cues share primary `(0.50, 0.13)` and the same visible height. No ad hoc movement or scale change is approved.

| Tile | Scene | Cue | Result |
|---:|---|---:|---|
| 01 | S01 | 1 | Pass: title sits above statue, not across its head or cat. |
| 02 | S02 | 1 tail | Pass: brief fade over upper library field; no face/object collision. |
| 03 | S02 | 2 | Pass: shared upper-center anchor. |
| 04 | S03 | none | Pass: cue 2 exits before this page composition. |
| 05 | S03 | 3 | Pass: alternate upper anchor clears the page edge and glyphs. |
| 06 | S05 | 3 | Pass: the same alternate anchor clears both researchers and papers. |
| 07 | S04 | none | Pass: the codex close-up has no title; the page remains unobstructed. |
| 08 | S06 | 4 | Pass: clear of face and both heads. |
| 09 | S07 | 5 | Pass: clear of face and cat’s head. |
| 10 | S09 | 6 | Pass: clear night-sky field above the monument. |

Actual Palmier composites were spot-checked at cue entrance, hold, exit, and selected cut boundaries. Cue 2 frames 241–246 show its gradual exit after `argued` and no title on the first S03 page frame. Cue 3 frames 392–400 show full readability through the end of `script`, a five-frame fade, and no title on the first S04 page frame. Captures are saved in `Previews/Accents_v04_20261101/Palmier_Cue3_End_Check/`; the diagnostic grid and burned-in frame number are review overlays only. Alignment plus sampled composites is not a substitute for watching the finished timeline at 1× with sound; that full playback remains unverified. Shorts UI safe margins also remain unverified.

## Consultation and evidence

Creative script and cue passes were requested one at a time in the Chrome ChatGPT project [YT Видео](https://chatgpt.com/g/g-p-6ae147d3975777d0-yt-video/c/6ae7674e-a67c-83eb-9489-7989c67955ce), with the visible model label **Extra High** before each prompt. Pro was not used. The cue timing derives from the recording’s ElevenLabs alignment, not estimated scene durations.

- [PBS NOVA — Maya decipherment timeline](https://www.pbs.org/wgbh/nova/mayacode/time-06.html): Knorozov’s phonetic approach and the 1952 publication.
- [Harvard HOLLIS — Yuri Knorozov papers](https://hollisarchives.lib.harvard.edu/catalog/dca00027): dates the first results to 1952 and places later decipherment in a continuing scholarly context.
- [Pravmir interview with Galina Yershova](https://www.pravmir.ru/knorozov-namnogo-operezhal-vremya-kak-zhil-i-rabotal-uchenyj-rasshifrovavshij-pismennost-majya/): retrospective student testimony behind the coauthor anecdote; script attributes it and does not claim the published paper included Asya.
- [Mérida monument reference photograph](https://commons.wikimedia.org/wiki/File:Yuri_Knorosov_monument_in_M%C3%A9rida,_Yucat%C3%A1n_(cropped).jpg): source image for the monument scene.

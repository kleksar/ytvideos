# Paper Detour 038 — chapter evidence EN v02

**Media:** `Work/ffmpeg-rebuild-en-v05/previews/caption-review-v05/47_ronin_en_review_v05.mp4`  
**SHA-256:** `a1e897b48b87d000a7dcccff9d376b147ec559c87e633cfcc1d2132b7199512c`  
**Measured duration:** 568.355011 s (9:28)  
**Timing map:** `Edit/FFmpeg/word-times-en-v09-speed110-bound-v02.json`, final-time map tied to the exact EN v09 narration and mix. 

## Complete block

```text
00:00 The Night of the Raid
00:37 Asano Draws His Sword
01:35 The Asano House Falls
02:29 Two Leaders, Two Paths
03:47 The Asano House Will Not Return
05:34 The Raid on Kira’s Residence
06:42 The Ronin Surrender
07:42 The Shogunate’s Verdict
08:10 From Condemned Men to Legends
```

## Boundary evidence

| Start | Final-map speech onset | Nearby narration cue | Chapter reason |
|---|---:|---|---|
| 00:00 | 0.08 s | “January thirtieth, seventeen oh three. Edo, the future Tokyo.” | Opens on the event and place. |
| 00:37 | 37.30 s | “It all began with two sword strikes.” | Shifts from the raid hook to Asano’s attack in the castle. |
| 01:35 | 95.62 s | “The sentence comes that same day.” | Moves into Asano’s sentence and the fall of his house. |
| 02:29 | 149.94 s | “But Oishi Kuranosuke remains the leading figure…” | Begins the opposing responses of Horibe and Oishi. |
| 03:47 | 227.64 s | “At last, an answer comes.” | The attempt to restore the Asano house reaches its outcome. |
| 05:34 | 334.84 s | “At last, the night of January thirtieth, seventeen oh three arrives.” | Returns to the raid on Kira’s residence. |
| 06:42 | 402.93 s | “But of the forty-seven participants, only forty-six surrender…” | The participants’ split and state custody begin. |
| 07:42 | 462.01 s | “On March twentieth, seventeen oh three, the shogunate announces its decision…” | Begins the sentence and its immediate consequences. |
| 08:10 | 490.01 s | “But this is where the story begins its second life.” | Moves from the deaths to the story’s later cultural memory. |

Times are rounded down to whole seconds so the marker does not begin after the mapped phrase onset. `validate_chapters.py` formal validation: passed; 9 chapters, start at 00:00, increasing, each at least 10 s, last fits 568.355011 s. `media_review=not_assessed`: starts are aligned to the final-time word map, but no continuous playback or independent chapter review is claimed.

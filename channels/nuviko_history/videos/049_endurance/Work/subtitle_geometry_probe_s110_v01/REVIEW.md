# S110 subtitle geometry and grouping probe — draft

A clipped voice excerpt and provider-derived machine timings were prepared with the shared Nuviko long renderer. Static 1280×720 composites of v01 showed the source-image phrases “SHIP O!” and “LUNCH O!” high in the frame and narration subtitles low in the frame without collision. This did not test motion or phone display.

In the clipped sample automatic grouping produced “first the words Ship” / “O were mistaken for Lunch O”, incorrectly splitting the first quoted expression. `plan_v02.json` adds the pairs [Ship,O] and [Lunch,O] to keep_together. The shared renderer then produces “first the words Ship O” / “were mistaken for Lunch O”. It flags the sentence break as forced or ambiguous; this sample omits the preceding “At”, so the entire sentence must be reviewed in its original full-film context before adopting any groups or exception. The updated grouping is a candidate, not final.

No audio was listened to; no timing, motion envelope, true phone size, final mix or actual MP4 was verified.

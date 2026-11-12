# Endurance — provisional semantic cut review

Scope: read all 122 candidate scene focal descriptions beside machine-estimated forced-alignment words in `semantic_cut_worklist_v02.json`; this is a text-level comparison, not audio playback, a visual acceptance or a final sync review. Word timings are uncertain and punctuation is lost in the machine estimate.

The candidate sequence follows the accepted narrative in broad order. Ordinary sentence continuations crossing a shot boundary do not in themselves imply a mismatch. The following need particular attention in actual playback:

- S002/S003: “All twenty-eight” begins while the sinking image is still visible; survivor faces enter before “men”. Ensure the image does not imply fatalities and check the actual subtitle grouping.
- S014/S015: “vessel” begins as the navigator shot enters. The preceding image establishes ice enclosing Endurance, and S015 depicts the navigator; verify the cut does not truncate the visual consequence.
- S032/S033: “For nearly a” begins in the launch image and is completed in the journey image. A chronological lead-in is plausible; audible pause and pacing unverified.
- S071/S072: “western coast” spans the landing and map transition. Check that the actual map communicates the relationship between landing and station without implying a falsely precise point.
- S110/S111: initial machine-estimated cut 510.333 s occurs between “Lunch” and “O”. `timing_word_safe_candidate_v02.json` proposes 510.667 s, after the forced alignment estimate for the second “O” and before its estimated “Then”. This forced token has score 0 and cannot establish actual speech boundaries. To maintain each scene ≥120 frames, the proposed change shifts the next eight cuts. Recheck each changed cut, the two quoted labels, caption grouping and audible speech; v02 is not accepted.
- S112/S113 and S113/S114 after the proposed cascade: “Pardo” and “All” may begin on the preceding image. The visual transition remains related but the intended emphasis and actual speech boundary require playback review.
- S119/S120: the phrase “twenty-two men” begins over the crossing-not-completed map before the rescue scene. The map and rescue are separate beats; review the pause and transition for comprehension.
- S120/S121: “six” is spoken while the image shows the twenty-two, followed by the 22+6 graphic. This may be a reasonable anticipation but requires visual-and-audio playback.
- S122 and source audio endpoint: final audible completion remains unknown; 559.8667 s picture candidate slightly exceeds the 559.840 s MP3 container. No ending has been approved.

No forced-alignment estimate, text-only reading or 30 fps frame arithmetic is proof of audible sync. All candidates remain DRAFT and all precise timing claims need checking against final mix.

# Paper visual procedure — change and validation receipt

Date: 2026-11-05. Scope: documentation and skills first, following the user's critique of sparse/repetitive scene images. No scenes generated or film edited in this pass.

## Primary references checked

- https://disneyanimation.com/process/layout/ — staging through sets, props and camera; selecting framing and considering adjacent shots. Read full textual page. Applied to pre-generation sequence review and actual-file sequence review.
- https://disneyanimation.com/process/story/ — storyboarding considers emotion, timing, staging and framing; refinement from rough thumbnails to clearer drawings. Read full textual page. Applied to early representative checks before producing the whole set.
- https://disneyanimation.com/process/visual-development/ — design, color and composition support story themes and the feeling of a moment. Read textual page; no claim to have reviewed all linked artworks. Applied to explicit visual contribution and Paper material treatment.
- https://www.adobe.com/learn/express/web/graphic-design-basics — emphasis, hierarchy, scale, contrast, repetition and purposeful negative space. Read article. Applied to main/supporting detail hierarchy and readable typography without a density quota.
- Pixar/Khan curriculum was located via official Pixar page and indexed Khan lesson summaries. Khan pages returned no readable body through the web reader; no lesson video was watched. No substantive procedure claim relies on having completed that course.

The contact-sheet workflow and representative subset are project adaptations of these principles, not quoted studio prescriptions or proven retention improvements. Consultation: ../consultations/2026-11-05_paper_visual_procedure.md.

## Current rule ownership

- Shared visual-storyboarding: narrative contribution, visible finding and full-sequence review before generation.
- Paper storyboard: expressive material staging, suitable maps/cutaways/scene lettering and justified local constraints.
- Scene-images: representative early internal check; actual individual-file and selected-sequence review with concrete reasons to return a scene.
- Paper image profile: rich crafted paper construction and physically integrated scene typography/explanations.
- Typography standard: editorial display lettering versus plausible printing on story props.
- Production skill, channel entry, catalog/index and four role TOMLs route to the owners. No additional skill, approval checkpoint, machine acceptance score or required report template was introduced.

## Desk review of decision criteria

These are manual rule traces, not generated-media tests or independent model evaluations.

| Case | Expected result and rule trace |
|---|---|
| Several different story events use almost identical distant subjects/horizons | Return the specific sequence during storyboard review; if generated, the selected-file contact-sheet check also returns it. File quality alone cannot pass the series. |
| A sparse horizon provides an intentional transition/scale/absence | Can pass with an evident role in this sequence. No object-count or angle quota forces decorative additions. |
| A paper map or scale uses large meaningful English labels | Allowed; storyboard specifies exact content/carrier/function, image review checks the actual readable letters and material integration. |
| A map draws an unsupported exact route or device invents precise readings | Reframe using a supported relation or explanatory model; useful text is not authorization to invent evidence. |
| A highly detailed scene hides the focal event | Return for hierarchy/readability repair; richness alone is insufficient. |
| A valid accepted reference or existing scene supplies pilot evidence | Reuse after checking applicability; no compulsory regeneration or new user checkpoint. |

## Checks actually run

- `python3 .agent/scripts/check-current-process.py`: PASS; 102 documents, no obsolete montage routes found. This is routing coverage, not proof against every documentation conflict.
- Skill Creator `quick_validate.py`: PASS for ytv-paper-storyboard, ytv-scene-images and ytv-video-production (frontmatter/structural checks).
- New local links: 7 resolved; all 7 new fragment targets matched actual headings.
- Four modified role TOMLs parsed with Python 3.11 `tomllib`.
- Reviewed task edits against pre-edit snapshots; preserved pre-existing and concurrent workspace edits. A concurrent channel-routing edit in documentation-index is outside this patch's visual changes.

Remaining evidence: actual images and sequence performance under this procedure have not yet been produced/reviewed. The earlier Fitzgerald v03 visual review remains reopened. Historical episode artifacts were not rewritten as new policy.

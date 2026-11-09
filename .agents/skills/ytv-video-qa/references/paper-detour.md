# Paper Detour QA profile

Use the [shared MP4-review and technical export profile](export-review.md) for Paper and Nuviko. Paper visual/typography criteria remain in its channel profile.

Check that the final scene order follows the accepted selection and satisfies the [scene-image uniqueness rule](../../ytv-visual-direction/references/paper-storyboarding.md#уникальность-сценовых-изображений). If a repeated composition is visible, record the affected intervals and verify any planned opening-frame loop against the accepted storyboard.

## Motion

For new Paper films and Shorts, verify the approved [Paper Frame](../../../../channels/paper_detour/Shared/Overlays/Paper_Frame/README.md) over the entire montage, including the start, end, loop boundary, all four outer edges, unobscured subtitle moments and visible scene movement. Review the exact pre-render sample and final MP4; examine scene motion under [motion checks](motion-checks.md). Existing frozen projects retain their recorded scope.

## Required text checks

Include applicable fields in both `required_checks` and the helper plan's `required_review_checks` before review:

- `word_highlighting`: verify the exclusive current word against the checked word map under the [subtitle procedure](../../ytv-paper-subtitles/SKILL.md#пословная-подсветка-в-монтаже). Multiple yellow words are FAIL.
- `subtitle_continuity`: for Shorts verify complete actual timeline coverage [0, frame_count), then decoded frames at transitions and pauses under the [Shorts standard](../../ytv-paper-subtitles/SKILL.md#shorts). Any blank subtitle frame is FAIL.

A visible defect on any inspected frame makes the affected check and visual readiness FAIL. A large sample count and technical PASS cannot override observed defects. Missing required coverage remains UNVERIFIED. Check the frozen required list against this profile; omission from a helper plan does not make a check optional.

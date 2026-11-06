---
name: ytv-youtube-analytics
description: Collect and interpret YouTube video or channel metrics with explicit sources, periods and denominators; produce comparable observations, evidence limits and a next measurement question without changing releases.
---

# YouTube analytics

Own measurements and their interpretation. Read active project instructions, channel profile and release/change history; [Paper Detour](references/paper-detour.md) supplies its routing. [A/B testing](../ytv-youtube-ab-testing/SKILL.md) owns experiment decisions; titles, thumbnails and production own subsequent edits. A recommendation does not authorize their execution.

## Establish the measurement

Route requests to find or compare new video topics to [topic research](../ytv-topic-research/SKILL.md); provide the measurements needed for that selection. A metrics-only request remains within analytics.

Identify channel and exact video scope/exclusions, observed Shorts/long/live format, visibility filters, actual publication time and packaging/edit changes. Do not infer Shorts classification from duration alone. Distinguish upload time from public-release time when the source does so.

Define the question and requested period/cohort before interpreting numbers. Record start/end, reporting timezone, capture timestamp, actual data-through date, filters (format, video IDs, traffic, geography/device if applicable) and unit. If the interface does not expose timezone or a denominator, preserve that unknown. Do not silently replace its timezone with the user's local timezone.

## Collect and preserve evidence

Use authorized Data/Analytics APIs when supported, or available Studio read-only reports/exports. Check granted scopes; do not silently expand OAuth access. A Data API read scope is not proof that the requested Analytics report is authorized. Keep source values, screenshot/export or non-secret response, selected settings and unavailable fields. Read current official [definitions and source limits](references/metrics-and-sources.md).

Data API cumulative counters support an inventory snapshot; they do not reconstruct an unobserved historical window or retention curve. Preserve each snapshot. A counter delta can be revised by the platform and is not necessarily a clean count of activity during that interval.

For each relevant metric save value/unit, source, entity/cohort, period/data-through date, definition and denominator when known, capture time and status. Keep absent/suppressed/pending values `null` with a reason, not zero. Mark realtime as preliminary. Preserve unavailable metric coverage instead of presenting a partial API response as complete analytics.

## Compare like with like

Separate Shorts starts/views from engaged views, feed stayed-to-watch/swipe behavior from registered thumbnail-impression CTR, and average duration/percentage from retention at a specific point. Use their actual report definitions and bases. An average percentage over 100% can reflect rewatching; it is not a completion probability. Never derive CTR by dividing all views by thumbnail impressions.

Compare the same format and a comparable age after release, duration, traffic mix and selected filters. State remaining confounders such as audience changes, paid/external traffic and concurrent packaging edits. Prefer a comparable channel cohort to a universal CTR/retention target. Do not combine cumulative API counters, a dated Studio report and realtime estimates into one performance ranking. Differences between them are not automatically a bug.

## Feed findings back to story development

For an authorized story/packaging evaluation, read the episode’s viewer promise and opening brief from [storycraft](../ytv-storycraft/references/appeal-and-opening.md). Prioritize registered-impression CTR and retention at 30/60 seconds, then inspect later retention and average view duration/percentage. Record exact time points, actual or approximate graph readings, cohort and missing data; mark points beyond the video length not applicable. These are not interchangeable with the average percentage viewed or a unique uninterrupted-viewer survival rate.

For Shorts feed use stayed-to-watch/swiped-away and subsequent retention, with their actual denominators; thumbnail CTR applies only to eligible impression surfaces. Compare a stated post-release window, format, duration and traffic source, and account for changing audience breadth. Do not derive a variant’s retention from the overall video curve. Compute watch time per impression only when both quantities refer to the same registered-impression cohort; otherwise preserve unavailable coverage.

Return one bounded editorial hypothesis, supporting observations and what would contradict it: weak selection, broken opening expectation, unclear event, delayed payoff or weak continuation are alternative explanations, not automatic diagnoses. A thumbnail/title A/B test does not test a different opening edit. Route that decision to the experiment owner. No universal CTR/R30/R60 pass threshold and no automatic release or scheduled monitoring are introduced.

## Return a bounded finding

Separate observed facts, possible explanations and causal evidence. A before/after change alone does not establish lift; use the actual experiment owner/result for that claim. Small samples support a data-quality check and a tentative next question, not confident ranking or an invented winner. When appropriate return `insufficient_data` with the exact missing observation.

Save the raw baseline and concise report beside the episode or channel research area. Report source/period/filter differences, missing metrics and confidence limits. Give the most useful next measurement/hypothesis with expected signal, comparison/window and what would contradict it; leave the hypothesis empty when evidence cannot support one. Route an actionable experiment to A/B or an editorial repair to its owner. Keep current pointers and preserve previous captures. A future checkpoint is not an automatically scheduled action.

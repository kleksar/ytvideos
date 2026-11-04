---
name: ytv-youtube-analytics
description: Collect and interpret YouTube video or channel metrics with explicit sources, periods and denominators; produce comparable observations, evidence limits and a next measurement question without changing releases.
---

# YouTube analytics

Own measurements and their interpretation. Read active project instructions, channel profile and release/change history; [Paper Detour](references/paper-detour.md) supplies its routing. [A/B testing](../ytv-youtube-ab-testing/SKILL.md) owns experiment decisions; titles, thumbnails and production own subsequent edits. A recommendation does not authorize their execution.

## Establish the measurement

Identify channel and exact video scope/exclusions, observed Shorts/long/live format, visibility filters, actual publication time and packaging/edit changes. Do not infer Shorts classification from duration alone. Distinguish upload time from public-release time when the source does so.

Define the question and requested period/cohort before interpreting numbers. Record start/end, reporting timezone, capture timestamp, actual data-through date, filters (format, video IDs, traffic, geography/device if applicable) and unit. If the interface does not expose timezone or a denominator, preserve that unknown. Do not silently replace its timezone with the user's local timezone.

## Collect and preserve evidence

Use authorized Data/Analytics APIs when supported, or available Studio read-only reports/exports. Check granted scopes; do not silently expand OAuth access. A Data API read scope is not proof that the requested Analytics report is authorized. Keep source values, screenshot/export or non-secret response, selected settings and unavailable fields. Read current official [definitions and source limits](references/metrics-and-sources.md).

Data API cumulative counters support an inventory snapshot; they do not reconstruct an unobserved historical window or retention curve. Preserve each snapshot. A counter delta can be revised by the platform and is not necessarily a clean count of activity during that interval.

For each relevant metric save value/unit, source, entity/cohort, period/data-through date, definition and denominator when known, capture time and status. Keep absent/suppressed/pending values `null` with a reason, not zero. Mark realtime as preliminary. Preserve unavailable metric coverage instead of presenting a partial API response as complete analytics.

## Compare like with like

Separate Shorts starts/views from engaged views, feed stayed-to-watch/swipe behavior from registered thumbnail-impression CTR, and average duration/percentage from retention at a specific point. Use their actual report definitions and bases. An average percentage over 100% can reflect rewatching; it is not a completion probability. Never derive CTR by dividing all views by thumbnail impressions.

Compare the same format and a comparable age after release, duration, traffic mix and selected filters. State remaining confounders such as audience changes, paid/external traffic and concurrent packaging edits. Prefer a comparable channel cohort to a universal CTR/retention target. Do not combine cumulative API counters, a dated Studio report and realtime estimates into one performance ranking. Differences between them are not automatically a bug.

## Return a bounded finding

Separate observed facts, possible explanations and causal evidence. A before/after change alone does not establish lift; use the actual experiment owner/result for that claim. Small samples support a data-quality check and a tentative next question, not confident ranking or an invented winner. When appropriate return `insufficient_data` with the exact missing observation.

Save the raw baseline and concise report beside the episode or channel research area. Report source/period/filter differences, missing metrics and confidence limits. Give the most useful next measurement/hypothesis with expected signal, comparison/window and what would contradict it; leave the hypothesis empty when evidence cannot support one. Route an actionable experiment to A/B or an editorial repair to its owner. Keep current pointers and preserve previous captures. A future checkpoint is not an automatically scheduled action.

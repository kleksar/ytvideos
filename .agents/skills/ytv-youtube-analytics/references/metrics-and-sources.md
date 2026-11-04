# Metric definitions and access

Check these primary sources when collecting a new report; APIs and Studio need not expose identical metrics or definitions.

| Source | Use and boundary |
|---|---|
| [Data API video resource](https://developers.google.com/youtube/data/reference/rest/v3/videos#statistics) | Current cumulative statistics and publication metadata; no historical retention or impression/CTR report inferred from these counters. |
| [Analytics reports.query](https://developers.google.com/youtube/analytics/reference/reports/query) | Explicit dates, dimensions/filters and authorized Analytics access. Requested endDate can exceed the last day available for every requested metric; record returned coverage. |
| [Analytics dimensions](https://developers.google.com/youtube/analytics/dimensions#day) | Check reporting-day/timezone semantics rather than assuming local calendar days. |
| [API metrics](https://developers.google.com/youtube/analytics/metrics) | Definitions/units depend on report. Check the selected metric rather than map an API field blindly to a similarly named Studio card. |
| [Studio reach](https://support.google.com/youtube/answer/9314355?hl=en) | Stayed-to-watch concerns initial Shorts viewing; average duration can use engaged-view watch time. Preserve the selected format/base. |
| [Thumbnail impressions](https://support.google.com/youtube/answer/9314486?hl=en) | CTR covers registered thumbnail impressions, not every view or feed exposure. Different cards refresh at different times. |
| [Content by format](https://support.google.com/youtube/answer/12942217?hl=en) | Filter Videos/Shorts and inspect traffic and retention in their context. |

Verified 2026-11-02. Copy the exact report labels and missing-value messages into evidence; do not overwrite them with a remembered historical definition. Save changes to definitions in the relevant measurement record, not as a silent cross-period comparison.

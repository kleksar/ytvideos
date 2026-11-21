# Research — Shower versus bath / Two Ways Lab

2026-11-19. Source remote main: e8f2b5488b266ebc89ea7ef48360df7584088e82. Owner's 2/5/10 policy PR #124 is MERGED. This is a hypothetical water-volume model, not physical testing or a measured household result. No production authorization.

## Selection — 11 distinct candidates screened

| Candidate | Stop / stay / payoff | Disposition |
|---|---|---|
| Shower vs bath water use | Familiar choice; longer shower loses; exact break-even | SELECTED |
| Roll vs fold suitcase clothes | One method may fit more; measurable packing layout required | FINALIST, strongest alternative; no real test available |
| Sort 40 socks before pairing vs pair immediately | First pair vs entire laundry task have different completion costs | FINALIST; unverified demand and operation model |
| Metro closest car vs exit-aligned car | Walk more now to save later; missing live station geometry | Experimental only |
| Grocery storage one sweep vs item by item | Repeat walking vs sorting; overlaps existing #237/#186 | Duplicate mechanism |
| Sandwich ingredients batch vs individual | First dish vs all dishes; #253 | Occupied |
| Dishwasher vs handwashing | Common water choice, but already #168 | Occupied |
| Showerhead flow 2.0 vs 2.5 gpm | Variant of selected shower/bath, not separate story | Model input |
| Elevator positioned centrally vs near lobby | Response times depend on initial floor/calls; #175 nearby | Unverified |
| Answer messages now vs later | Time saved but deadline missed; #269 | Occupied |
| Bulk packs vs small packs | Lower unit price, higher actual checkout; #272 | Occupied |

Three actual finalists are shower/bath, suitcase roll/fold, and sorting socks. The suitcase is the strongest alternative by visual potential and direct comparables, but an honest win needs real repeatable packing measurements or a very precise constrained geometry; neither was available. Socks may become a good experiment once item identity and operation cost are pinned, but selecting a winner by swapping metrics would be manipulative.

Selected first line: “Can my shower use more water than a bath?” Immediate image: one running shower vs one filled tub, both illustrated as a mathematical model. The story moves from 8-minute shower win to 15-minute bath win under constant flow, finds the crossover, changes one announced parameter and resolves the rule. Final benefit: the viewer can estimate their own threshold. Main objection: the formula is simple and cannot inherently sustain ten minutes. This is why 10m is marked REWORK; no filler facts were invented.

## Primary factual basis (pages read 2026-11-19)

1. US EPA WaterSense showerheads: https://www.epa.gov/watersense/showerheads . Standard reference flow 2.5 US gallons/minute; WaterSense showerheads must be 2.0 gpm or less. Does not confirm our fictional hardware or a specific home.
2. City of Portland water efficiency: https://www.portland.gov/water/water-efficiency-programs/save-water-home . Average shower ~8 minutes / 17 gallons; average bath ~30 gallons; bath volume depends on tub and fill level. The 30 gallon baseline is public context, not an exact universal volume.
3. Saving Water Partnership: https://www.savingwater.org/indoors/showers-baths/ . Bath fills around 30–40 gallons, shower consumption depends on flow and running time; supports conditional comparison.
4. City of Cochrane water guide PDF: https://www.cochrane.ca/sites/default/files/2023-09/Household%20Water%20Use.pdf . Found in search, but PDF not fully read; not used to support any exclusive script detail.

No actual meter readings, flow measurements, safety trials, bath-fill photos or media references exist.

## Fixed model, precise equations and independent arithmetic check

One person, one wash, method A shower, B bath. Winning metric = total US gallons drawn. Base A = flow × minutes actually running, B = tub fill. No assumed change in cleaning quality, time preparation, water temperature or comfort. Base B=30 gallons and A flow=2.5 gpm.

| Round | A water | B water | Conclusion |
|---|---:|---:|---|
| Base 8 minutes | 20 | 30 | A by 10 |
| Base 12 minutes | 30 | 30 | Tie; base crossover = 30 / 2.5 = 12 minutes |
| Base 15 minutes | 37.5 | 30 | B by 7.5 |
| Flow changed only to 2.0, time=15 | 30 | 30 | Tie; crossover now 15m |
| Flow=2.0, time=12 | 24 | 30 | A by 6 |
| Fill changed only to 24, flow=2.5, time=8 | 20 | 24 | A by 4 |
| Fill=24, flow=2.5, time=10 | 25 | 24 | B by 1; crossover 9.6m = 9m36s |
| Sensitivity only: A warm-up waste 2 gallons, flow=2.5 | 2 + 2.5 × T | 30 | crossover running time 11.2m = 11m12s |
| One hundred 8m base showers / baths | 2000 | 3000 | A saves 1000 under identical hypothetical routine |
| One hundred 15m base showers / baths | 3750 | 3000 | B saves 750 under identical hypothetical routine |

The 24-gallon shallow fill and 2-gallon warm-up waste are illustrative assumptions, not measured fixtures. The bath may also waste warm-up water; unequal conditions are only a sensitivity study. Fifteen minutes in bathroom with tap running eight minutes is eight flow-minutes. All model arithmetic was recalculated using a local Python calculation on 2026-11-19.

## Comparable YouTube signals — metadata only

Observed via indexed YouTube search results on 2026-11-19. No YouTube direct watch/transcript/comment access; published counts can be stale, duration UNVERIFIED for all, no actual video watched. Format: standard YouTube video page unless otherwise stated.

| URL | Date, author, language | Views indexed | What it does and does not show |
|---|---|---:|---|
| https://www.youtube.com/watch?v=t6TW3xVb1To | 2020-12-08, Citiq Prepaid, EN | 88 | Direct bath/shower comparator but weak public response; same-author baseline unknown |
| https://www.youtube.com/watch?v=rf7jiyQZk9I | 2024-03-07, UNICEF India, EN | 57,417 | Related bucket-bath/shower conservation tip, not a 1:1 model |
| https://www.youtube.com/watch?v=E8pqw6VJZ04 | 2024-03-07, UNICEF India, EN | 53,178 | Same author's same-day tap conservation baseline |
| https://www.youtube.com/watch?v=iQsMCCBWM3A | 2024-03-07, UNICEF India, EN | 57,324 | Same-author same-day water conservation baseline |
| https://www.youtube.com/watch?v=HxZL9xy4EqQ | 2024-09-05, Tripped Travel Gear, EN | 7,168 | Suitcase roll/fold direct video; creator baseline unavailable |
| https://www.youtube.com/watch?v=yEktB6I7ktE | 2025-01-11, Ansari Helps, EN | 1,420 | Second suitcase author, different channel and audience |

UNICEF's result is consistent with its other same-day tips; it cannot demonstrate unusual bath/shower interest. The Citiq result is a counter-signal, not evidence that nobody cares. For socks no usable directly comparable videos or same-author baseline were retrieved; public demand UNVERIFIED, not zero.

Fresh 30–90 day YouTube demand: UNVERIFIED. A dated Sep 26, 2026 web article https://watercalculator.us/blog/water-use/bath-vs-shower-water-use is a recent online publishing signal only, not proof of YouTube traction. No real viewer comment was accessible; video descriptions provide publisher prompts, not audience quotations. No owned analytics was accessed. All CTR, retention, view velocity and transferability to Two Ways Lab are UNVERIFIED.

## Promise, response and scope

Viewer: someone who washes and pays attention to water use. Promise: changing only the length of a shower can reverse the result. Cold first frame must convey a hypothetical comparison, not fake a real meter. Beat sequence: familiar assumption → short shower wins → keep the flow fixed and run longer → reversal → calculate threshold → alter an announced input → practical limitation and final answer. The payoff is reached before the 2m semantic loop.

Rights: original narration only. External videos are for topic-level search metadata; no clips, exact lines, screenshots, image bytes or audio rights imported. No rejected #13/#88 angle reused, no accepted #20/#25/#46 altered. PR status is an editorial hypothesis, not a source of production authority.
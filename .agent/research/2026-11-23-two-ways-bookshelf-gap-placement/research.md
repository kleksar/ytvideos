# Research — The Empty Bookshelf Gap Problem

Observation date: 2026-11-23. Channel: Two Ways Lab (English, first-person illustrated comparisons).
Status: **EDITORIAL_CANDIDATE_UNREGISTERED**. This is original, synthetic, explicitly conditional mathematics, **not** a physical experiment, user analytics, live YouTube playback or a claimed measured result.

## Selection and coverage

This is a bounded scan of **12 distinct everyday-problem proposals**, with previous work checked against open and closed GitHub PRs before selecting a topic. It is NOT 12 validated viewer-demand signals.

| Candidate | Value / reason to watch | Issue / outcome |
|---|---|---|
| 1. Shelf gaps distributed vs at the right edge | A bookshelf that looks less tidy can require drastically fewer book shifts; reverse result when all books append | **Selected**, deterministic flip + third consequence: setup costs erase saving |
| 2. One shared screwdriver: keep it until a full assembly ends vs hand it off between steps | Familiar tool bottleneck; one worker may have nothing to do while the other works | **Finalist**, honest scheduling alternative; specific work graph and comparable baseline not yet verified |
| 3. Kitchen dish batch vs individual full plates | Visible repeated switching vs one customer's late plate | **Finalist**, can compare total readiness and first-plate waiting; overlaps older queue/batching stories; real timings absent |
| 4. File folders: alphabetical vs project order | Find a document versus the effort to insert new documents | Potential duplicate of chosen mechanism, rejected from shortlist |
| 5. Pantry: oldest product in front vs new products at front | Waste/expiry stakes | Actual shelf and expiration variability not modeled; no manufactured food-safety finding |
| 6. Four different-shaped parcels: first-fit vs tightest-fit boxes | Spatial reversal and fewer boxes | Needs physically realizable geometry; source/model inputs absent |
| 7. Two people share a bathroom, finish routines vs alternate short stages | Familiar contention | Need task graph; medium complexity without novel payoff |
| 8. Printer: one large job before three short jobs vs interleave | Clear scheduling fairness flip | Very similar to earlier queue PRs including #385; low novelty |
| 9. Load a shopping bag by weight vs by destination shelf | Competing household goals | Metrics not automatically equivalent |
| 10. Room vacuum path: spiral vs zig-zag | Visible route length | Existing cleaning category and physical obstacles complicated |
| 11. Reheat four lunches short-first vs original order | Strong timing consequences | Existing Draft PR #385; **duplicate** |
| 12. Group photos in arrival order vs minimum people moving | Pleasant visual payoff | Existing PR #121; **duplicate** |

**Three genuinely different finalists**: shelf insertion gaps; shared screwdriver; batching kitchen plates. The screwdriver alternative has a more human frustration/coordination angle, while shelf gaps has a clearer immediate visual reversal in fixed transparent inputs and a potentially valuable post-payoff insight: making gaps first can consume the future savings. Kitchen batching has a strong relatable setting but existing queue/batching saturation and more easily becomes a mere spreadsheet. The strongest alternative is **shared screwdriver**; its main potential advantage is visible cooperation and suspense. Biggest objection to the selected shelf story: it might be interesting only to a small book-organization audience, and some viewers may regard a book-shift count as trivial. There is **no proven comparative retention** to settle this.

Remote duplicate examples checked: #385 microwave queue, #382 folded-vs-rolled clothing, #379 smart plug, #356 backpack layout, #350 socks sorting, #237 grocery aisle route, #121 group photos, #211 gift packaging, and multiple checkout/cleaning batch stories. No bookshelf-gap PR returned by matching bookshelf/shelf/books search at research time. Re-check all PRs before new writes. User-rejected #13 telegraph and #88 dry-bridge angle excluded.

## Single fixed setup / measurable competition

Starting state: one horizontal 16-cell shelf, 12 unit-width books A…L in alphabetical order, exactly 4 vacant one-cell slots. Illustration letters are **model identifiers**, not product claims.

- A: A B C D E F G H I J K L _ _ _ _
- B: A B C _ D E F _ G H I _ J K _ L

Metric announced **before** reveal: one **one-slot displacement of an existing book** = one move. Inserting the new book into its vacant slot is counted 0. A two-position shift of one book = 2 moves; moving two books by one = 2 moves. All arrivals inserted alphabetically using the nearest free gap; when choosing a gap, preserve order. No removals or expansion. Initial layouts are provided; creation of B is **not** part of arrival metric unless explicitly analyzed in 10m. No seconds or physical measurement inferred.

Deterministically recomputed using explicit 16-cell array simulation; each insertion preserves sortedness and occupancy, count per displacement:

| Reset experiment | Insert order | A per insertion | A total | B per insertion | B total |
|---|---|---|---:|---|---:|
| Interior | A2 E2 H2 K2 | 11,7,4,1 | **23** | 2,1,1,0 | **4** |
| Append | M N O P | 0,0,0,0 | **0** | 1,4,8,12 | **25** |
| Mixed | A2 E2 M N | 11,7,0,0 | **18** | 2,1,1,4 | **8** |
| Mixed, arrival order altered | M N A2 E2 | 0,0,13,9 | **22** | 1,4,2,1 | **8** |
| Interior order reversed | K2 H2 E2 A2 | 1,5,9,14 | **29** | 0,1,1,2 | **4** |

Layout-conversion price A → B: D,E,F each 1; G,H,I each 2; J,K each 3; L four => **3+6+6+4=19 one-slot moves**. Under first interior delivery, 19 setup + 4 arrival moves = 23, same as layout A (23); the claimed 19 saved is not net savings if layout B had to be built from A first. No universal winner, no extrapolation to realistic book widths, hand labor or audience response.

**Payoff**: interior delivery B wins 4 versus 23; appending A wins 0 versus 25; arrangement cost can erase apparent advantage. This is a scenario reversal, not a real-world measurement. The example is deliberately not a universal recommendation.

## Promise, hook, development, objections

Audience: English-speaking home-organization / tiny everyday optimization audience, not professional library staff.

First Short line: “Should I keep four empty bookshelf slots together, or spread them out?” First pictured state: same 12 books, same four holes, A/B side by side; the viewer chooses **before** outcome.

Development: a four-book interior delivery gives B an apparent huge win; a reset and entirely appended delivery reverses the winner. Payoff for 2m is the honest conditional rule. 5m additionally explains why the gap travel distance matters. 10m now models a hypothetical unknown future (equal chances or 75% interior arrivals) and then includes the 19-move initial conversion cost; this creates a separate decision rather than repeating book-shift sequences.

Strong objection: model measures displacements, not elapsed time; different widths, shifting many at once, acquisition pattern and first-time rearrangement can change results. This is acknowledged inside the actual narratives, not hidden in metadata.

## External audience evidence: bounded, not proof

Sources below were found by public search on 2026-11-23. Dates/views describe **retrieved search-page observations**, often cached and older than the observation date; they are NOT live YouTube analytics. No full videos were watched for this assessment, and no comments or transcripts are claimed reviewed except publicly available page summaries. Source author/format baseline is limited.

| Video / URL | Publisher; publication | Language/format; known length | Displayed views / source | Comparison limits |
|---|---|---|---|---|
| https://www.youtube.com/watch?v=ZpR_uAcUJX4 | Carter Sullivan, 2026-06-12 | English home-library reorganization vlog; duration **UNVERIFIED** | 11,368 in cached YouTube result, 139k followers reported | Topic adjacent, no A/B shelf insertion model; normal same-author outcome **UNVERIFIED** |
| https://www.youtube.com/watch?v=1jTw8sAANUw | Bookish Eve, 2026-03-21 | English BookTube makeover, chapter timeline through **34:58** | 32,800 in cached YouTube result; 2,320 followers reported | Very long makeover vs proposed miniature mathematical narrative |
| https://www.youtube.com/watch?v=evEYIXBHBwQ | Space to Love, 2014-10-30 | English bookshelf how-to, duration **UNVERIFIED** | 1,445 in cached YouTube result; 395 followers reported | Small/old instructional comparison |
| https://www.youtube.com/watch?v=iPprQMOkLFY | Sara Carrolli, 2022-08-26 | English long lifestyle book organization; duration **UNVERIFIED** | 276.1k on third-party Glasp summary | Not a confirmed direct live YouTube figure; large-channel outlier risk |
| https://www.youtube.com/watch?v=SDbEtuso-UQ | Sara Carrolli, 2023-02-19 | English bookshelf tour/decor; duration **UNVERIFIED** | 168.8k on Glasp summary | Closest available **same-author genre** baseline, still different age and format; not a standardized baseline |

Source context: AASL library-shelf management https://knowledgequest.aasl.org/managing-library-shelf-space/ motivates leave-space/shifting practice only; it does **not** establish invented 16-slot model, performance or viewer appeal.

Cross-channel interpretation: bookshelf organization is a recognizable topic, but most listed videos are long vlogs and aesthetics tips, whereas chosen angle is a numerical conditional A/B simulation. The highest counts from authors with their own audiences **cannot** prove our angle, CTR, retention, current velocity, or transferable views. No directly comparable 2-min animated model/author baseline was verified. 30–90 day **recent** demand and comment questions: **UNVERIFIED**. Evergreen category signal is tentative; specific A/B demand is **experimental hypothesis**. vidIQ paid credits: **not used**. Own Two Ways Lab analytics: **not accessed**, so no claim about channel retention.

## Fact, rights, and production boundary

The only exact numeric claims come from the disclosed **model and checked arithmetic**, not from a published science experiment. External bookshelf videos are solely category-interest context. Scenes, book icons, photographed interiors, generated data labels, graphics and rights are not yet acquired or approved. Channel rule forbids unsupported programmatic graphics text overlays except captions; actual visuals await applicable storyboard/scene planning with approved image-derived lettering. No TTS, imagegen, upload, MP4 or paid tools used.

Format: 02m **editorial Short proposal**, exceeds Two Ways Lab's 35–50-second orientation (format compatibility needs runtime decision); 05m/10m **editorial Long proposals only**, no usable Long ChannelSpec recipe. No fictitious runtime, receipts, approved master or independent listener.

## Additional computed evidence for revised 10m (2026-11-23)

The mixed and reversed-order sequence results above remain legitimate research, but are **not** part of the revised 10m narration. New text considers exactly two mutually exclusive complete four-book futures, each starting with the identical 12 books and resetting the shelf (never >16 occupied slots): interior A23/B4 and append A0/B25. The following are explicitly *hypothetical weights*, not measured frequencies:

| Scenario weighting | A expected moves | Already-prepared B expected moves | B after converting A→B (add 19 upfront) |
|---|---:|---:|---:|
| interior 50% / append 50% | 11.5 | 14.5 | 33.5 |
| interior 75% / append 25% | 17.25 | 9.25 | 28.25 |
| interior 100% | 23 | 4 | 23 |
| append 100% | 0 | 25 | 44 |

For assumed interior share p, A=23p and prepared B=4p+25(1−p)=25−21p, hence prepared B improves the model if p>25/44≈56.818%. If starting at A and paying 19 to convert, B_total−A=44(1−p)≥0 for p∈[0,1]; only ties at p=1. This is not a physical time measurement or a claim that real purchases follow those probabilities. Initial shelf assembly from an empty shelf is **not modeled**.

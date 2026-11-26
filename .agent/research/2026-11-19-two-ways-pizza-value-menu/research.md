# Two Ways Lab · Pizza value, one order / two methods

Observed and compiled 2026-11-19. **All external queries are general public-topic queries.** This is a conditional mathematical comparison, **not a documented physical experiment** and not representative of actual restaurant menus.

## Audience promise and story

English-speaking everyday consumer: “At checkout, should I buy two cheaper-looking medium pizzas or one larger pizza?” The opening shows exactly those alternative orders ($19 for 2×12", $20 for 1×18") rather than unexplained formulas. After the viewer picks A/B, the two circles are scaled, area—not box count—is measured, and the initially cheaper-looking B loses on square inches per dollar. The payoff is fully delivered before a coupon makes B win at $17. Avoid predicting real pizza mass or restaurant quality.

**Before knowing the result:** same circle shape, dough thickness, topping and delivery conditions; metric is total pizza surface area / final price. A = one 18" diameter pizza for $20; B = two 12" diameter pizzas for $19; alternate single-variable B price $17. These are authored demonstration inputs. No restaurant measured. This is a deliberately simple model where the change in price genuinely reverses an outcome.

## Selection — coverage and comparisons

12 materially distinct candidates checked for existing PR overlap and whether an observable, fairly comparable A/B outcome can be described without pretending real measurements:

| Story candidate | Selection observation |
|---|---|
| Pizza 1×18" versus 2×12" at checkout | Familiar money decision; unexpected geometric reversal; same initial state; independent 2/5/10m material |
| 40 socks: sort by colour first versus pair directly | Strong everyday problem; accurate work count depends on an explicitly constructed sock sequence; second finalist |
| Stairs versus waiting for lift for a short trip | Recognizable decision but realistic results require building-specific wait observations; third finalist |
| Gift paper longitudinal vs transverse cut | Numeric payoff possible; appeal relies on chosen rectangle sizes, less universal |
| Store kitchen tools by task vs type | Depends on actual future uses; uncontrolled unless a workload trace is provided |
| Return each scattered item immediately vs basket collection | Path-length model straightforward but resembles existing household route scripts |
| Two people share a morning bathroom | Waiting-time simulation requires invented routine timings; less universal |
| Schedule by shortest tasks vs nearest deadlines | Important but largely abstract; harder immediate visual payoff |
| Make four sandwiches item-by-item vs assembly line | Prior story PR #253 already covers close procedure; do not duplicate |
| Two queues versus shared queue | Channel checkout pilot E001 and prior PR topic overlap |
| Direct bus later vs transfer now | Arrival-time input too dependent on live route/schedule; weak transferable quantitative result |
| Metro closest carriage vs exit-oriented carriage | Compelling alternative, but station layout is place-specific and would require accurate map |

Existing PR search on 2026-11-19 returned no pizza story. Nearby—but different—drafts: [#127 parking](https://github.com/kleksar/ytvideos/pull/127), [#182 coffee-and-milk](https://github.com/kleksar/ytvideos/pull/182), [#253 sandwich preparation](https://github.com/kleksar/ytvideos/pull/253), [#272 grocery box pricing](https://github.com/kleksar/ytvideos/pull/272), [#275 shower/bath consumption](https://github.com/kleksar/ytvideos/pull/275). Latest draft [#278 Nuviko bank](https://github.com/kleksar/ytvideos/pull/278) indicates Two Ways next after channel rotation on remote. Statuses and issue overlap must be checked again before write.

### Three competitive finalists; strongest objection

**1 · Pizza value (selected).** Opening: “Two twelve-inch pizzas for nineteen dollars, or one eighteen-inch for twenty.” Further development: correct geometric area → pay-per-area verdict → coupon price reversal → limits. Full payoff: the $20 large wins at $19 B, while $17 B wins; the break-even pair price is ~$17.78. **Strongest objection:** the geometric observation is widely taught and the public videos below have modest view counts; no comparable Two Ways hit or real checkout measurement proves viewers will watch.

**2 · Sock sorting (strongest alternative).** Opening: I have 40 unmatched socks and need complete pairs before leaving. Further development: direct scanning under a fixed order versus colour buckets, including the time or move cost of sorting; payoff could flip with how often colours repeat. **Strongest objection:** a compelling numerical comparison needs a fully specified input sequence, definition of moves and costs, and a genuine dramatic change, not arbitrary favourable input. A recent, format-comparable YouTube signal is not established.

**3 · Stairs versus elevator.** Opening: I reach a two-floor journey and see a lift button. Further development: fixed stair-climbing speed and elevator cycle time, break-even with waiting, a second floor/traffic condition; payoff a conditional choice, not “stairs always faster.” **Strongest objection:** a meaningful winner depends on actual wait and physical ability; simulation of one building may feel obvious or unfair. No production-ready location or user-appropriate generalization.

Pizza edges out socks due to an immediately recognizable two-box visual, a counterintuitive real mathematical relationship and an actual decision boundary. Socks may be more distinctive once a compelling measured workload can be sourced, and is not rejected permanently.

## Audience/YouTube signals and limitations

Only **search-index text, accessible titles and metadata** were available; no player watch-through, independently verified transcript, comment reading or private creator analytics. View counts are approximate metadata snapshots from search, **not current views**, not historical same-age baselines, not CTR/retention, and not a trend measurement. Format and duration where absent remain UNVERIFIED.

| Video URL / ID | Source/author | Published | Language / format / available observations | Counter-signal / baseline |
|---|---|---|---|---|
| https://www.youtube.com/watch?v=WNYm9PwVC_E | Brain vs Math | 2026-07-06 | EN; indexed Short; ~796 views, 12 likes in search snapshot | Modest public reach; ordinary comparable same-author result UNVERIFIED |
| https://www.youtube.com/watch?v=0ZDzvskXwJ8 | Atomic Hands | 2023-06-19 | EN; medium educational walkthrough suggested by 00:00–03:28 description; ~1,624 indexed views, 38 likes | Old evergreen, not evidence of 30–90 day demand; baseline UNVERIFIED |
| https://www.youtube.com/watch?v=VzJRBt608G8 | Zangston | 2020-09-08 | EN; tutorial; ~152 indexed views; duration UNVERIFIED | Strong negative public performance signal; baseline UNVERIFIED |
| https://www.youtube.com/watch?v=L-tHs6px1kM | Interesting Facts Library | 2021-11-13 | EN; indexed Short; ~1,565 views / 37 likes | Low absolute reach; baseline UNVERIFIED |

**Fresh non-YouTube signal:** a public thread on 2026-11-14 discussing one 18-inch versus two 12-inch pies, https://www.reddit.com/r/YouShouldKnow/comments/1xvwkz1/ysk_one_18_inch_pizza_is_more_food_than_two_12/ , reportedly had ~4,298 upvotes when discovered. This is a self-selecting discussion, not our channel's audience; any claims about thirteen Pennsylvania restaurants in that thread are unverified and **not used** as menu evidence. Older evergreen discussion: https://www.mentalfloss.com/food/pizza/want-more-pizza-order-one-18-inch-pie-instead-two-12-inch-pies and https://www.ndtv.com/offbeat/viral-tweet-explains-the-math-to-get-more-pizza-per-order-and-people-are-amazed-1974872 (2019 articles reporting a math comparison); both are secondary popularity signals, not evidence of product demand.

**Source foundation for math:** the circle-area identity `A=π(d/2)^2` is elementary mathematics rather than a claim about a restaurant. An independent visualization is https://madeclear.ca/visualizations/pizza-area , accessed as public topical material. Numerical calculations were performed locally independently, with model values below. Real comments, current YouTube views, same-author format-/age-matched baselines, fresh 30–90 day YouTube trend, Two Ways own performance and audience CTR/retention are **UNVERIFIED**. vidIQ free balance check on 2026-11-19 found **0 credits**; no charged requests made.

## Calculation ledger: exact rules, all quoted outputs

Circle surface in square inches = `π×(diameter/2)^2`. A = `π×9² = 254.4690049`. B = `2×π×6² = 226.1946711`. A−B = `9π = 28.2743339`; `A/B = 9/8 = 1.125`. Per-dollar A/$20 = **12.723450**, B/$19 = **11.904983**. With B coupon only B price $17 changes: B/$17 = **13.305569**, so B wins. Break-even B = `20×(B/A) = 20×8/9 = $17.777777...`. Cent rounding: at **$17.77** B wins narrowly; at **$17.78** A wins narrowly; the exact equality lies between ordinary cent prices.

For 5/10m additional one-inch border illustration: topping-covered ideal centre of A `π×8² = 201.06193`; B `2×π×5² = 157.07963`; A advantage ≈ **28%** relative to B. Bare-border A `π(9²−8²)=17π ≈53.4071`; B `2π(6²−5²)=22π ≈69.1150`. This is an **assumption about a uniform 1-inch border**, not measured cheese coverage or total topping quantity.

If the one large diameter is reduced to 16 inches, its area `64π≈201.062` versus B `72π≈226.195`; equal-area large diameter `12√2≈16.971` inches. If the consumer instead wants minimum total spending for a fixed sufficient quantity, the lower total $19 B may be preferable; that is **a different declared objective**, not a contradiction of price per unit area. No actual pizza weight, density, delivery fees, nutritional equivalence, topping quality or brand claim is supported.

## Story structure and packaging evidence

- Hook/first image: side-by-side consistent-scale cardboard pizza circles, A cyan ($20 one 18") versus B amber ($19 two 12"), before mathematical reveal. The exact opening sentence appears in each version.
- Development: unfair instinct of adding diameters; reveal 254 vs 226 area; $/area; B-only discount changes decision.
- Primary payoff: initially apparently expensive single A is better surface value; B wins only after pair price falls below ~$17.78. 05m adds quantified crust effect; 10m adds different metric and diameter.
- Title and thumbnail promise about a price/value reversal, **never** claims a real test or guaranteed restaurant promotion; no new-subscriber metrics.
- Biggest limitation: public examples and 2026 thread show topical familiarity; direct demand for the specific editorial execution remains a **hypothesis**.

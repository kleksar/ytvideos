# Shared research — four USB-C cables, four devices, first-fit vs scarce-first

**Observed/edited:** 2026-11-18 (Europe/Belgrade). **Scope:** a new *Two Ways Lab* editorial story, no actual experiment, hardware purchase or production. **Main source:** `8f7c58c49b74c1670de31709f856e33247a43e29`. **Policy #124 merged** 2026-11-16; historical proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is not a main revision or live run pin. Research and six scripts remain an `EDITORIAL_CANDIDATE_UNREGISTERED` proposal.

## Selection: ten distinct concrete situations considered

This is the actual exploration set, not ten search aliases for one story. Categories reflect the channel's actual `docs/BACKLOG.md`. Candidate outcomes are **author judgments**, not measured audience reactions.

| Candidate | Concrete A/B, metric | Reason / disposition |
|---|---|---|
| 1. Four mismatched USB-C cables and phone/monitor/laptop/drive | First compatible device-first versus least-flexible-device-first; successful connections on one pass | **Selected.** A black monitor with unused compatible-shaped cable is immediately intelligible. Counterexample and swap explanation prevent false universal advice. Drawback: mathematical desk simulation rather than actual hardware test |
| 2. Grocery-list route through a mapped store | Traverse aisles in list order versus nearest next listed item; modeled walking distance | **Strongest alternative.** Everyday physical friction and visual movement; can end with real shorter route, but choosing a non-arbitrary layout and shopping list requires more grounding; without store data it's another invented map |
| 3. Suitcase packing under space and weight limits | Largest-volume-first versus heaviest-first; accommodated essentials | **Finalist.** Stakes recognizable and visual, but 2D fit/packing has geometry and real compressibility uncertainties; a made-up outcome would be less reproducible than a compatibility table |
| 4. Group photograph entry/exit order | Listed order versus grouped-by-person memberships; movements required | Mathematically tractable, potentially strong visual, but overlap of photo groups currently underspecified |
| 5. Printer queue of jobs | Arrival order versus shortest job first; waiting time | Clear mathematical result, weaker physical/emotional stakes; similar to existing deadlines/queue stories |
| 6. Four kitchen dishes, two burners | Shortest cook first versus longest first; finish time | Strong everyday problem; reliable time inputs and simultaneous stages need a carefully bounded artificial model |
| 7. Shared screwdriver with two people | Finish worker A first versus task handoffs; completion and switching costs | Attractive physical movement but transition times dominate and need a good sourced/declared model |
| 8. Cleaning: one item at a time versus room baskets | Distance walked for exact room arrangement | Duplicate neighborhood of #186/#220, so not new |
| 9. Checkout two lines versus one | Wait times of modeled customers | Existing checkout/queue material, duplicate vicinity #136, rejected |
| 10. Gift wrapping cut direction | Usable wrapped gifts and paper waste | Potentially demonstrable, but earlier wrapping work #211/#162 makes novelty weak |

**Finalist one-line pitches at comparable definition:**

1. **USB-C:** *“I had enough cables. Why did the monitor stay dark?”* Stop: fitting cable cannot show video. Stay: rerun identical desk with constrained device first and then reverse rack order. Payoff: A 3/4, B 4/4; A can tie when physical cable order changes; a swap repairs A. **Strongest objection:** in life a person will simply swap cables; this is not a direct measurement of time saved. We declare one-pass metric and show the repair openly.
2. **Grocery route:** *“Why did I walk down the same aisle three times with a seven-item list?”* Stop: wasted steps. Stay: exact route changes and one exception for cold food order. Payoff: shortest route in an explicitly modeled shop. **Strongest objection:** arbitrary shop geometry/stock positions could predetermine winner, and actual shopping time also depends on finding items/queues. To make stronger, need real store layout or carefully accepted simulation.
3. **Suitcase:** *“Everything fits by volume, so why won't the case close?”* Stop: obvious travel problem; stay: order by volume versus weight, compressible layers and unequal dimensions. Payoff: which essentials remain packed under declared constraints. **Strongest objection:** a 2D sketch or only total volume would pretend to resolve real 3D packing/compression and damage risks; no physical validation.

**Why chosen over the strongest alternative:** USB-C gives a clean, checkable answer and an actual surprise that comes from resource scarcity, not author-assigned delay. Grocery has potentially greater general reach, but absent a real mapped store the optimization could seem rigged. **Counterargument against the choice:** USB-C has narrower audience, and the selected cable-priority story is a conditional explanation rather than an observed physical experiment; the same scene may become didactic when stretched to ten minutes. The reviewer may reasonably reject it.

**No fabricated comparative creator baseline:** We searched public YouTube metadata; an ordinary, age-/format-matched set of videos for the same creators was not reliably retrievable. No exact native creator baseline or owned YouTube analytics. Do not treat a large channel's millions as a signal for our format.

## Source ledger: actual electronics, not a validation of the model

**Microsoft Support, “Fix USB-C problems in Windows”**, accessed 2026-11-18: https://support.microsoft.com/en-us/windows/hardware/usb/fix-usb-c-problems-in-windows

- Section *USB device functionality might be limited*: matching USB-C connectors can lack matching features; hardware, port, cable and device may differ
- Sections *Display connection might be limited* and *USB Type-C alternate modes*: PC, display and cable must support applicable display mode
- Section *Charging*: cable and charger, as well as PC, determine supported charging power
- Confirms only background distinction between connector shape and real data/power/video capability. **Does not confirm this four-cable experiment, the exact compatibility matrix, real timings, universal ranking, or that a particular unlabeled cord is safe.**

**Audience-question evidence, not modeled-data source:** Reddit discussion of a charging USB-C cable that failed to carry a monitor image, actual post/comments dated 2024-07-31 to 2024-08-02, observed 2026-11-18: https://www.reddit.com/r/UsbCHardware/comments/1egw2yz . Poster described new cable charging but not displaying video. Replies question cable versus port/monitor; the discussion does **not** prove fault or validate our scenario. Real audience language “charges but no display” directly informs an understandable first question, not a copied quote or claim of demand.

## Exact hypothetical model — defined *before* either outcome

Every cable has one slot. Devices are distinct and can take one cable. The computer port(s), charger(s), monitor and peripherals are assumed to support the declared tasks. We do **not** suggest a phone physically powers a monitor, a cable alone suffices for video, or that USB-C necessarily supports a feature.

| Device | Task that counts as success | Compatible set in *this fictional table* | Number of options |
|---|---|---|---|
| Monitor | Picture with video-capable connection | V | 1 |
| Laptop | Declared high-power input | V,H | 2 |
| External drive | Declared data transfer | V,D | 2 |
| Phone | Basic charging | V,H,D,B | 4 |

Cable definitions: V supports video, data, high power; H supports declared high power, not the drive's declared data or video; D supports declared data and basic phone charging, but neither laptop's specified high power nor video; B supports only basic charging. All four have USB-C shaped connectors, no hidden defects. These labels are author-designed **not model numbers**. This table is a deliberately bounded capability relation, not the full USB specification.

**Initial physical rack:** `V,H,D,B` left to right. A job order `phone,drive,laptop,monitor`; B job order `monitor,laptop,drive,phone` (tie between laptop and drive broken consistently). Both select **first unused compatible cable** scanning original rack left-to-right. No swaps until count. Score: devices successfully satisfying declared task after a single pass. No elapsed-time, charging speed, energy, price, durability, or safety performance claims.

```text
A: phone→V, drive→D, laptop→H, monitor→none (B lacks video) = 3/4.
B: monitor→V, laptop→H, drive→D, phone→B                 = 4/4.
Repair A by exchanging phone's V for monitor's B           = 4/4,
but only AFTER a second assignment; first-pass score 3/4.
Counterexample rack B,D,H,V with A's same job order:
   phone→B, drive→D, laptop→H, monitor→V                   = 4/4.
B in same rack still achieves                                 4/4.
Replace V with second B (no video anywhere):
   monitor has zero compatible cables; max score            = 3/4
under either method; no ordering can invent video.
```

**Calculations reproducible:** each assignment is selected by the declared order and compatible sets, no scheduling ambiguity. This is illustrative combinatorics; **not** a field experiment. A *general* greedy rule “fewest options first” is not guaranteed to find the optimal assignment on arbitrary graphs; we only establish this four-device example. The initial outcome is genuinely conditional and might become a tie under another cable order. Good constraint use saves *replugging in the example*, not proven time in seconds.

## Public YouTube comparison (metadata actually visible; no video watched)

Observed via web metadata on **2026-11-18**. All views are source-reported counts at crawl/observation (may lag), not independently refreshed YouTube Studio; no creator baseline normalized to format/age.

| Source (direct link) | Author / publication | Format/language/duration if known | Public reported reach and limitations |
|---|---|---|---|
| [You Bought the Wrong USB-C Cable and You Don't Even Know It](https://www.youtube.com/watch?v=NfkfhapuoLo) | x-kom, **2026-06-23** | Polish channel; explanatory long, chapters to **08:46** (~9m) | **19,402 views, 1,100 likes** in retrieved result; useful close topical match, not an A/B model |
| [Stop making this MISTAKE when buying your USB-C cables!](https://www.youtube.com/watch?v=ayPbjjn_Jdo) | Les Tests de Cyril, **2026-06-30** | French tech explanation/test long; chapter endpoint **16:33** (~17m) | **3,735 views, 58 likes**, 36.4k followers; direct different-author counter-signal; not an invented viral success |
| [How to Pack a Suitcase](https://www.youtube.com/watch?v=bS0feJY7sNI) | U-Pack, **2014-09-12** | English instructional, long, duration not verified | **303,455 views, 1,800 likes**; evergreen alternative topic, extremely old, not a comparable channel age baseline |
| [How the Layouts of Grocery Stores are Secretly Designed to Make You Spend More Money](https://www.youtube.com/watch?v=ThNeIT7aceI) | Wendover Productions, **2016-01-24** | English explanatory long, duration not verified | **1,005,556 views, 13,000 likes**, creator ~4.91m followers; scale/age/channel mismatch, not proof grocery topic would outperform here |

**Freshness boundary:** USB-C matching examples from June 2026 are **~4–5 months old**, not within the current 30–90-day window. No verified last-30/90-day view growth. The two 2014/2016 alternatives are plainly **evergreen**, not current momentum. YouTube search snippets were accessed, **not watched**; there was no video playback, independent transcript reading or native YouTube comments. Reddit is a real Q&A thread but not a YouTube comment set. More recent video/page snippets lacked reliable matched samples. We did not measure CTR, retention, comments in our own channel, or audience response to this *particular conditional A/B treatment*: all **UNVERIFIED**. We did not make paid vidIQ/provider calls or claim a balance.

## Selection and framing outcome

**Audience premise:** a first-time viewer owns assorted USB-C chargers/cables, understands “phone charges but monitor stays black,” may not know video alt-mode. Channel English narration from I/я throughout; everyday choice, fair A/B and preannounced score. No Paper diorama, historical narrator, device brand endorsement, or fake filmed experiment.

**Promise:** *“Why did four apparently fitting cables leave one device disconnected? Can order alone fix it?”*
**First visible event:** a phone on the most versatile cable and an unlit screen, with explicit conditional model disclosure immediately afterward.
**Development:** A burns V on phone → monitor fails; B reserves V → all four work; A can be repaired by a swap; reverse cable rack → tie; missing V → neither works.
**Payoff:** capability scarcity, not raw number of cables, determines the avoidable first-pass failure. **Main objection remains:** narrow, school-like problem; need a blind reader to decide whether actual audience would stay to the turn. Verified category interest is not verified interest in this narrative. Rejection without new PR is acceptable, and this PR is not a production approval.

**No story-adjacent assets generated, no future thumbnail/reference hashes guessed.**

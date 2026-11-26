# Research — Three Gifts, Two Discounts / Two Ways Lab

**Observed on 2026-11-18 (UTC).** Editorial Git queue only: no real `ytv start`, run ID or independent review. Source remote main: `7c94f825056b98cb65d8de94dd3eec709cc78188`; PR #124 is **merged**, main editorial and writer skill read directly. Channel: `two_ways_lab`, active illustrated Short recipe only; no Long configuration. No real sale or household experiment is represented.

## Audience, hook, full payoff

Audience: English-speaking viewers who recognize a holiday-shopping decision, without requiring a math background or a brand to know. The initial promise is an actual bill, not an abstract statement that some discounts are deceptive.

- **First 02m line:** “Three gifts. Two discounts. One sign promises something free. Which deal actually leaves more money in my pocket?” First image: same three gift silhouettes, two offer labels (A/B) and an unreadable-to-be-revealed receipt. A/B choice appears before results.
- **First 05m line:** “I have three gifts to buy, and two sale signs to choose from. One offers twenty-five percent off. The other promises a free gift. The strange part is that the very same sixty-dollar total can make either sign the winner.”
- **Main question:** with the *same eligible products*, which discount actually lowers the checkout total more, and why does the winner flip when price distribution changes?
- **Development after hook:** A first wins $45 vs $48 → reset and choose prices $20/$20/$20 → B wins $40 vs $45 on same $60 original total → 5m ties at $45/$45 and shows the extra-purchase trap → 10m examines capped promotion and return/eligibility limitations.
- **Payoff:** the apparent paradox is resolved by comparing **25% of eligible basket total** with **price of cheapest eligible item**. A “free” item can be a smaller or larger saving than a percentage. The practical choice starts with the *items I actually need*.
- **Strongest objection:** much shopping advice based on fabricated price tags is staged; a retailer could change promotional terms. Answer: all prices/rules are declared as **illustrative model inputs**; no empirical or universal result is claimed, and sensitivity flips the result without hidden changes.
- **Freshness:** November holiday-shopping timing is topical editorially, but no 2026 30–90-day search growth or matched-viewer evidence was verified. This is an **experimental demand hypothesis**, not a proved popular script.

## Selection funnel — 12 materially different tasks considered

Actual broad-screen comparison used the channel backlog, existing open/closed PR inventory, topical free YouTube discovery and ability to verify an A/B outcome without fabricated measurements. The rejected candidates were not written as full scripts.

| Different story/task | Screen result |
|---|---|
| **A/B 25% vs buy-two-get-cheapest-free for 3 gifts** | **Finalist, selected.** Clear surprising reversal at constant $60, applicable mental shortcut, reproducible arithmetic; limitation: must disclose exact promotions and fictional prices |
| Airline boarding: back-to-front vs alternate-row/window-first | **Finalist, strongest alternative.** Real mock trials, counterintuitive individual/total boarding times; major concern: variations in aircraft/cabin/bags, source age and strong existing competition |
| Matching cables to devices: first compatible vs scarce-device-first | **Finalist.** Familiar charging frustration, concrete reversible assignment; major concern: fixed compatibility graph feels contrived, weaker general-viewer motivation |
| Dishwasher vs hand-washing dishes | Existing [#168](https://github.com/kleksar/ytvideos/pull/168) — duplicate |
| One shared bathroom, two morning schedules | Existing [#133](https://github.com/kleksar/ytvideos/pull/133) — duplicate |
| One long checkout line vs two shorter lines | Existing [#136](https://github.com/kleksar/ytvideos/pull/136) — duplicate |
| One gift-wrap sheet, two cutting plans | Existing [#211](https://github.com/kleksar/ytvideos/pull/211) — duplicate |
| Find lighter packet: 4v4 vs 3v3 | Existing [#207](https://github.com/kleksar/ytvideos/pull/207) — duplicate |
| Stairs vs elevator for same arrival | Existing [#175](https://github.com/kleksar/ytvideos/pull/175) — duplicate |
| Roll clothes vs fold clothes to fit suitcase | No real packing dimensions and behavior; alleged benefit would require unsupported measurements |
| Kettle vs pot to boil the same water | Unmeasured energy efficiency/initial conditions; empirical winner could not be asserted |
| Two washing machines, shortest jobs first vs longest first | The proposed total finish time can easily be invariant, and invented machine times drive the effect; weaker screen story |

Three strong finalists considered at comparable specificity, not three catchy versions of the selected idea:

| Finalist | Exact proposed cold opening | Post-hook development | Payoff | Strong objection |
|---|---|---|---|---|
| Discounts | “Three gifts. Two discounts. One sign promises something free.” | Two receipts on same basket, then reverse outcome with the same original total | Compare cheapest qualifying item against 25% of qualifying basket | Model prices/terms may feel manufactured |
| Boarding | “Everyone wants the plane to board faster. Why might the line that looks slower work better?” | Compare aisle interference, bag loading and row ordering under controlled mock trial | Boarding time depends on congestion, method and objective | Transfer from old small trial to modern full flight not universal |
| Cable matching | “I have three devices and three cables, but the first cable that fits can leave one device dead.” | Naive choice blocks only compatible cable; reset with scarce-device-first | Compatibility constraint makes order matter | Artificial graph and niche gameplay rather than broadly useful comparison |

**Why discounts beat boarding today:** boarding has better historical viral-video evidence but also a crowded explanation space and less personally checkable result. The discount story gives a familiar decision, a short calculation anyone can reproduce, a visible real-life constraint and a complete second reversal, without claiming new field measurements. Boarding remains a genuine high-strength alternative. **Why discounts beat cable matching:** a matching proof is clean, but viewer familiarity doesn't ensure interest in the chosen constraints. No perfect candidate; selected weakness remains realistic terms and audience measurement.

## Reproducible model — all outcomes fixed before the writing

**Same initial state for each A/B comparison:** exactly three intended and eligible items, prices listed up front, no shipping/tax, no stacked promotions; both possible offers available as choices. A = 25% off **all three**; B = buy two get **cheapest of three** free. B applied only with three eligible products. Metric announced in advance: **checkout charge for intended purchases**, lower is better, not subjective value and not a hypothetical store's current advertised price.

| Case | Three prices | Pre-sale | A: 25% off | B: cheapest free | Honest result |
|---|---|---:|---:|---:|---|
| Original | $24, $24, $12 | $60 | $45 (save $15) | $48 (save $12) | A wins by $3 |
| Equal prices | $20, $20, $20 | $60 | $45 (save $15) | $40 (save $20) | B wins by $5 |
| Tie | $25, $20, $15 | $60 | $45 (save $15) | $45 (save $15) | Tie |
| Change to A cap $10 (**10m sensitivity only**) | $24, $24, $12 | $60 | $50 (save capped $10) | $48 (save $12) | B wins by $2 under **new** rules |

This is arithmetic, not measured store behavior. If `T` is total eligible original price and `m` cheapest eligible price, `saving_A=.25*T` and `saving_B=m`. Therefore B wins iff `m>.25*T`; ties at equality. For two fixed higher items $24/$24 and cheapest price `x`, `x>.25*(48+x)` iff `x>16` (assuming x remains cheapest).

**Changing the original task (5/10m):** if the user genuinely needs *only two $24 items*, option A costs `$48*.75=$36` while B requires adding a qualifying $12 third item and the bill is $48 for three items. “Saving” must not be attributed to a third gift the user did not need. This is deliberately *marked a new question*, not presented as the same A/B experiment. A capped discount is likewise a *new explicit condition*, never mixed with the uncapped baseline as an unfair comparison. Retailer exclusions, quantity thresholds, returns and list-price integrity require actual terms.

**Source-supported boundaries, as of observation date:**

- [Target promotional policy and exclusions](https://www.target.com/help/article/000063028): lower-priced qualifying item restrictions, eligibility and promotion conditions. **Only illustrates possible rules**, does not verify a particular current three-gift offer.
- [Shopify Buy X Get Y discounts](https://help.shopify.com/en/manual/discounts/discount-types/buy-x-get-y): configuration/eligibility; customers sometimes must manually add the free item. No claim every storefront acts alike.
- [Target promotional return/refund policy](https://www.target.com/help/article/000063251): prorated promotion amounts can affect a returned item's refund. The 10m text attributes its example specifically to Target, not our invented register.
- [FTC advertising FAQs](https://www.ftc.gov/business-guidance/resources/advertising-faqs-guide-small-business): fair representation of “free” offers and original/reference prices; background only, not mathematical evidence.
- **Calculation provenance:** direct arithmetic above, independent from YouTube creators or retailer-specific implementations; could be recomputed in a simple calculator. No published citation is claimed for toy prices.

## Free YouTube discovery and honest demand limitations

Only **publicly indexable metadata/search snippets** were accessible, not actual video playback, transcript verified against playback, comment threads or YouTube Studio. Preserve uncertain fields instead of silently filling them.

| Observed video / URL | Source, published date, language, format, duration/views | What it really supports |
|---|---|---|
| [Black Friday EXPOSED as the BIGGEST Scam of 2025!](https://www.youtube.com/watch?v=9nA9-oJSftU) (`9nA9-oJSftU`) | Social Symone, publication index 2025-11-28; EN; longer commentary, chapter index includes discussion of BOGO near 23min; public-index views ~272k, verified duration **UNVERIFIED** | General audience for holiday-deal skepticism; materially different format and 2025 seasonal item, not direct test of 2026 shopping puzzle |
| [Try this strategy when people are in buying frenzies during the holidays](https://www.youtube.com/watch?v=ZEnQ6SaG1CQ) (`ZEnQ6SaG1CQ`) | MoreMozi, English; Short-like marketing advice, published date and views **UNVERIFIED** in accessible result | Viewer-facing discount framing appears in holiday marketing content, but not a fair A/B checkout test |
| [Why “Buy one, get one free” isn’t a great deal](https://www.youtube.com/watch?v=yOK3bF3jhXU) (`yOK3bF3jhXU`) | Public third-party-index title; author/date/format/duration **UNVERIFIED**; an indexed all-time figure of roughly 3.7m is not current verified count | BOGO curiosity exists in search; this metadata cannot establish comparable view performance, mechanism or actual quality |

**Baseline:** no reliable median/typical same-author videos of comparable age, length, language and format was recovered; do not infer outperformance, trend or audience-retention from one indexed outlier. All three entries represent different age/format or missing data; **same-author baseline UNVERIFIED**. Comments/transcripts **UNVERIFIED**; no fabricated quotation, user question or actual viewing. **Fresh 30–90d 2026 interest UNVERIFIED;** 2025 observations are evergreen/seasonal historical analogues. Creator internal analytics, CTR, stayed-to-watch and retention **UNVERIFIED**. Free search was used; no vidIQ paid credits or purchases. Search sources may have stale metadata and cannot prove the particular illustrator-first English channel's demand.

## Duplicates, rejection and final decision

GitHub remote open/closed PR list was checked; #213 Nuviko, #212 Paper and #211 Two Ways were the latest three story drafts at selection; next channel is Two Ways. #124 merged and was read from main. Existing owner-rejected Paper #13 and #88, accepted #20/#25 and working #46 protected; no older story modified, duplicated or closed. This is **one candidate story** with three full editions, not three disconnected topics. Outcome: **STRONG_CANDIDATE as an experimental editorial hypothesis**, with production and independent-review blockers preserved.

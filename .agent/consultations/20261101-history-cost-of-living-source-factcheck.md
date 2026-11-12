# Source fact-check — English wages, prices and household models

- Date and stage: 2026-11-01; research pass 1 follow-up, methodological fact-check.
- Channel: Nuviko History. No episode folder has been selected or registered yet.
- Coordinator: project chat in Google Chrome.
- ChatGPT chat: [Проверка исторических источников](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0/c/6ae7c364-3894-83eb-8733-e26746199840).
- Exact visible model label immediately before sending: `5.6 Очень высокий`.
- Response completed and visible after 2m29s. The chat UI subsequently displayed `Pro` in the follow-up composer; that does not alter the verified pre-send label.
- This is a source-method check. It does not settle a final story or constitute acceptance of a script.

## Prompt

> Одна узкая задача: источниковедчески проверь, какие данные о труде, заработке и расходах семьи реально позволяют сравнить английские исторические периоды — и где авторы используют допущения. Рассмотри только эти работы: Robert C. Allen (2001), Phelps Brown & Hopkins (1955–56), Gregory Clark (2005 и его housing series), Sara Horrell (2023), Humphries & Weisdorf (2019), Horrell, Humphries & Weisdorf (2022).
>
> Проверь особенно четыре места: (1) у Allen 250 рабочих дней — допущение для годового заработка, а 5% на жильё — упрощённая надбавка в расчёте семейной черты бедности, не наблюдаемый ряд лондонской аренды; (2) у Phelps Brown–Hopkins есть дневные ставки строителей, но они не устанавливают число оплаченных дней за год и почти не дают реальных расходов на жильё; (3) у Clark ранние оценки аренды/качества жилья реконструированы, а числа наблюдений меняются между версиями данных; (4) Horrell 2023 моделирует CPI с меняющимися весами, а ранняя жилищная стоимость частично оценена; Humphries–Weisdorf используют годовые выплаты, а Horrell et al. 2022 строят модель семейного бюджета на жизненном цикле, включая труд женщин и детей.
>
> Верни компактную таблицу по каждой работе: что непосредственно наблюдается; что реконструируется/моделируется/допускается; период и география; для какого точного тезиса её безопасно использовать. Затем дай один редакционный вывод: можно ли честно поставить ролик вокруг вопроса «сколько дней/часов труда требовалось семье, чтобы обеспечить базовую жизнь» или лучше сузить вопрос до покупательной способности заработка. Подтверди спорные детали DOI/страницей или разделом статьи; пометь, где не можешь подтвердить. Не придумывай посещение датасетов или точность, которой у источника нет.

## Saved answer — substantive findings

### Main editorial verdict

Do not frame the whole film as a literal count of days or hours a family actually worked to secure a basic life. For most of 1260–1850, the source base does not directly observe that quantity. A more defensible core question is:

> **How much of a basic basket of goods and services could an ordinary English worker’s earnings buy, and how did that change from the Middle Ages to the industrial era?**

“Days of work” can remain a visual measure only if labeled as an **equivalent** (days at a prevailing day rate corresponding to annual pay or a basket), not as days actually worked.

### Source-by-source use and limits

| Study | Direct evidence / reconstruction | Period and geography | Safe use |
|---|---|---|---|
| Allen (2001) | Historical daily building-worker wage quotes and urban commodity prices. The CPI omits rent where data are missing. Welfare ratios annualize daily wages at 250 days and add a minimal constant 5% rent allowance to a notional family poverty basket; Allen calls the constant markup a simplification. | European cities; London inputs principally 1457–1860. | Compare a London builder’s purchasing power against the specified basket under the explicit 250-day assumption. Do not call the 5% allowance an observed London rent series or a household’s actual rent share. DOI 10.1006/exeh.2001.0775, pp. 422, 425–427. |
| Phelps Brown & Hopkins (1955–56) | Southern-English building day rates and prices of consumables. The 1956 paper explicitly says annual days of employment are unknown and little or nothing is known about important costs such as rent. | Southern England, 1264–1954; the 1955 wage table switches after 1846 to a 10-hour rate. | Show what one builder’s day rate could buy from the chosen consumables series. It is not annual income or a complete family cost-of-living measure. DOI 10.2307/2626898 and 10.2307/2551457; the 1956 caveat is on p. 296. |
| Clark housing series / “Shelter from the Storm” | Rent/lease records and house prices are combined; some rents are implied from house prices using yield and depreciation assumptions. Constant-quality rent and housing-quality series are statistical reconstructions, not direct observations of a representative working family’s expenses. The Extra High response compared 11,188 rental-value records in an earlier housing paper with 20,000 housing-rent quotes in the 2005 JPE paper, but did **not** verify a versioned archive proving these are counts from one unchanged dataset. | England; published housing estimates cover 1550–1909. | Describe estimated rent and housing-quality trends, with early geographic coverage and reconstruction limits. Do not transfer counts between papers or call them one dataset’s changing sample size. DOI 10.1017/S0022050702000578; Clark 2005 DOI 10.1086/498123. |
| Horrell (2023) | Chained-Laspeyres CPI with historically changing expenditure weights; household accounts and early budgets are reconstructed from heterogeneous evidence. Early accommodation services are estimated from building-cost evidence before monetary rents are available. Some services lack observations and are excluded. | England, 1260–1869; the representative construction is mainly rural/market-town and does not stand for the rapidly growing urban factory-worker population. | Explain how the estimated cost of ordinary household consumption changes when its composition changes. It is not a continuous record of actual household expenditures or rent. DOI 10.1111/ehr.13236, §§ I–II, IV. |
| Humphries & Weisdorf (2019) | 6,800 annual payment observations for men. Annual remuneration can include board/lodging and other in-kind benefits whose values are imputed; extending annual-worker earnings to casual workers uses a labor-market-arbitrage assumption. Figure 4’s “working days” are equivalent days implied by annual pay divided by a day rate, not observed days actually worked. | England, 1260–1850; unskilled men across South, Midlands and North. | Use annual payment evidence to avoid multiplying a day wage by an arbitrary 250 days; call derived duration an implied working-year equivalent. DOI 10.1093/ej/uez017, §§ 2.1–2.2 and Fig. 4. |
| Horrell, Humphries & Weisdorf (2022) | Wage evidence for men, women and children feeds a life-cycle household model. Unknown casual-worker annual income, women’s labor input (one or two days a week by life-cycle phase), family composition and consumption equivalents are modeled assumptions. | Predominantly rural working families in England, 1260–1850. | Show why household resources depend on family composition, women’s and children’s work, and the life cycle. It is not a long observed series of household budgets or work hours. DOI 10.1111/ehr.13105, §§ 1.1, 1.3, 1.5. |

### Four requested checks

1. **Allen:** confirmed. The 250-day annualization is an assumption; the 5% rent addition is a minimal flat allowance in the poverty basket, not a London rent series. The CPI itself excludes rent where city data are unavailable.
2. **Phelps Brown–Hopkins:** confirmed. The authors say the day rate is known, annual workdays are unknown, and little or nothing is known about rent.
3. **Clark:** the reconstruction caveat is confirmed; the “one dataset whose observation count changed” phrasing is not. Safer wording: the scope/definition of the data compilation differs or expanded across studies; do not move an n from one paper to another without pinning the exact release.
4. **Horrell / Humphries–Weisdorf:** confirmed with distinction. Horrell’s early housing input is estimated. Humphries–Weisdorf replace a fixed 250-day gross-up with annual-payment evidence, but still impute in-kind pay and derive equivalent days for casual work. Horrell et al. 2022 explicitly model household labor and life cycle.

## Independent checks already completed

- Allen, article copy and model discussion: [MIT-hosted PDF](https://web.mit.edu/14.731/papers/greatdivergence.pdf).
- Phelps Brown & Hopkins, 1956 caveat: [article PDF](https://users.pop.umn.edu/~ruggl001/hist5011/phelps-brown%20and%20hopkins.pdf).
- Clark, scope of author datasets: [UC Davis data page](https://faculty.econ.ucdavis.edu/faculty/gclark/data.html); housing-series scope: [Cambridge article record](https://www.cambridge.org/core/journals/journal-of-economic-history/article/abs/shelter-from-the-storm-housing-and-the-industrial-revolution-15501909/F0BB1D7F8C6A46F6D3F6D91903587E72).
- Horrell 2023: [LSE repository PDF](https://eprints.lse.ac.uk/117518/3/Horrell_household_consumption_published.pdf).
- Humphries–Weisdorf 2019: [LSE repository PDF](https://eprints.lse.ac.uk/90328/1/Humpries_Unreal%20wages.pdf) and [Oxford Academic DOI record](https://doi.org/10.1093/ej/uez017).
- Horrell, Humphries & Weisdorf 2022: [Wiley article](https://doi.org/10.1111/ehr.13105).

## Next research question

Test which bounded English comparison can tell the clearest causal story without blending unlike measures: (a) one worker’s day-wage purchasing power, (b) annual male-worker remuneration versus changing household consumption costs, or (c) modeled household resources across the family life cycle. Include plausible counterexamples and identify where a short video can land an answer without presenting modeled equivalents as observed facts. Do not begin the script until this research decision is saved.

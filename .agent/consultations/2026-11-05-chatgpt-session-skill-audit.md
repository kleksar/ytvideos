# ChatGPT browser skill audit

Date: 2026-11-05. Visible UI checked in a Chrome tab created for this audit.
Test page: https://chatgpt.com/

- The reasoning control initially displayed **Extra High**, and the accessible UI described it as level 4 of 5.
- Using the visible reasoning control's Right Arrow changed the displayed label to **Pro**, level 5 of 5. Left Arrow restored **Extra High**, level 4 of 5. The UI therefore allowed switching; the mode was not fixed by the old skill name.
- The separate model menu displayed **GPT-6** and **GPT-5.6 Sol**. It also showed an account/usage limit notice for GPT-6. The reasoning label remained a separate control.
- A second, newly created ChatGPT tab showed a pre-existing unsent draft from unrelated work. It was not edited, submitted, or closed. Because the composer was not clean and the visible label could not be isolated from that draft's context, inheritance of the selected mode by a fresh chat remains unverified.
- The temporary test tab was restored to Extra High and closed. The tab containing the unrelated unsent draft was left open; after the browser automation session became unavailable, its continued presence could not be confirmed.

The UI is a point-in-time observation. Recheck current labels and availability at use time.

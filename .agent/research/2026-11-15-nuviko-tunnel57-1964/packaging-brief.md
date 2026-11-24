# Tunnel 57 — Long packaging hypotheses

EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

Канал `nuviko_history`, английский исторический Long 16:9, без Short-петли. Все концепции — **гипотезы упаковки** к неутверждённому narration, без сделанных обложек, измеренного CTR и внешней генерации. Обязательные три существенно разные пары Long. Main source `5d3222c8888c775d2195c8b2949949f2d992e98d`; exact EN blob `537ab0539c1e6048fa28486d32f1f8c8f8e588ef`.

## Concept A — the escape route (initial preference)

- **Title:** How 57 People Escaped UNDER the Berlin Wall
- **Thumbnail idea:** A physically legible cross-section: a Berlin border watchtower and concrete barriers on the surface, a single tiny human-filled tunnel beneath, one person emerging inside a courtyard; bold true-scale relation. No claim this is an authentic archive photo.
- **On-image words (draft):** 57 ESCAPED
- **Promise:** What physical route let 57 people pass a guarded wall? A full mechanism and its human consequences, not merely «they dug a tunnel».
- **First proof:** Narration S001 and the underground cross-section early in S011–S015.
- **Payoff:** S021–S026 deliver actual mass escape and Christa; S030–S040 reveal the dangerous discovery and truth behind the fatal shooting.
- **Possible false read:** Implies all survived a bloodless event. Avoid implying nobody died; within intro, guard death is made explicit.

## Concept B — the falsified official account

- **Title:** The Berlin Wall Escape That Exposed a Deadly Cover-Up
- **Thumbnail idea:** Split human documentary illustration, young East German border guard on one side, the tunnel mouth and conflicting investigative documents on the other; do not depict a specific unverified shooter or make a forged authentic document.
- **On-image words:** WHO FIRED?
- **Promise:** Why East German authorities falsely blamed the escape helpers for killing a guard.
- **First proof:** S002–S004 acknowledge death and concealment without falsely claiming no helper fired.
- **Payoff:** S036–S040 distinguish initial helper wounding from fatal shots by fellow guard, original secrecy and eventual investigation.
- **Possible false read:** Could imply deliberate state-ordered execution or that no helper fired. Both false; narrative explicitly separates nonfatal and fatal shots.

## Concept C — human reunion

- **Title:** The Secret Tunnel That Reunited a Divided Berlin Couple
- **Thumbnail idea:** Two ordinary people on opposite sides of Berlin buildings, narrow underground route connecting them, period-specific architecture verified before art; avoid implying they were both among the 57.
- **On-image words:** BELOW THE WALL
- **Promise:** How Joachim, already in West Berlin, helped bring Christa out from the East.
- **First proof:** S007–S010 explain the relationship, first failed escape and prison.
- **Payoff:** S023–S026 make the reunion real; investigation in last third provides further consequence.
- **Possible false read:** Happy escape story without death: don't erase Schultz's loss.

## Editorial selection and scope

Предварительно выбирается A, потому что он понятен без знания имён и соответствует первому кадру; B — более необычный угол, но опаснее подменой подлинной причинности, C — эмоциональный, но сравнительно менее универсальный для новой международной аудитории. Это **не A/B winner**. Полные title/thumbnail/description (строгие ReleaseSpec/thumbnail_plan) оформляются только после настоящего утверждения script в production runtime. Никаких actual generated images/assets, проверенного phone preview или YouTube read-back.


## Variant safety 2026-11-16

Все концепты выше созданы для original EN blob `537ab0539c1e6048fa28486d32f1f8c8f8e588ef` и его 42 сцен. Новые `variants/02m`, `variants/05m`, `variants/10m` имеют иные точные тексты/hash. **Нельзя наследовать старые сцены, главы, first-proof S### или timestamps**: после выбора единственного exact master переразметить визуальные соответствия и проверить реальное thumbnail promise → opening → payoff; эта работа НЕ выполнена. Рекомендуется 05m только на уровне editorial, без owner approval, без изображения/MP4/CTR. Все три Long допустимы по ChannelSpec, однако production не разрешено данным PR.

## 2026-11-19 — visual intent для обновлённого 05m, без production storyboard

Финальный кандидат `variants/05m/script.en.txt` (SHA-256 `73dfa51d9d17cfa65bb9802061811809204a0e9d27a8c9679f8bc328ea7384cb`) отличается от исходных 42 сцен. Проверить по **новому** narration: (1) семейное разделение и неудачный первый побег, (2) пекарня → 145-метровый ход → **одна дверь** во дворе как уязвимое место, (3) переходы и освобождение Кристы, (4) мнимые беглецы возвращаются с охраной, (5) Шульц — бывший учитель, (6) несмертельное ранение и затем смертельный friendly fire, (7) противоречащие публичные и секретные документы, письмо его матери, (8) исход двух семей. Обязательны честная география и атрибуция архивов; не создавать поддельный аутентичный документ или вымышленные лица/реплики.

Вариантам 02m/10m соответствуют **другие** scene spans и first-proof windows. Концепты A–C выше пока привязаны к original master, для 05m это лишь идеи, не проверенный visual plan или owner-selected packaging.


## 2026-11-24 — 10m visual intent

Exact new EN SHA-256 `2b3a368c82b004a0d5e028a0e9846dd1522637274a4baad9cb071a998129e555`, RU `6f16934437083188bfc83602483f2211a8dae0c94ad80d5c59bc80c86e74cf32`. The historical original concepts are not scene mappings for this text. P01–06 border/personal passport attempt; P07–18 bakery and ordinary doorway; P19–21 letter/reunion; P22–28 operation and loss; P29–36 school plaque and disputed records; P37–40 investigations and new memorial plaque. Candidate promise: **How 57 People Escaped Under the Berlin Wall**, with the loss and later investigation acknowledged in the opening. The physical closing image is the memorial, not a fictitious trial victory. No generated assets; verify period details/rights before production. 05m packaging remains unchanged.

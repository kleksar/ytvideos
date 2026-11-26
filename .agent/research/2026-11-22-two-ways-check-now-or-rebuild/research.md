# Research — Check each assembly stage versus inspect only the finished shelf

## Selection · 2026-11-22: eleven differentiated tasks considered
Remote newest story PR was #364 (Nuviko History) after #363 (Paper) and #362 (Two Ways). This slot is therefore **Two Ways Lab**. Main at start: 131ef24068d75967b1e43aa88e5f1370f6775054. PR #124 is already merged; canonical current main instructions apply. There is no policy import from that old PR or modification of pinned runs.

| Different real-world question | Stop reason / next event / payoff | Strongest weakness | Decision |
|---|---|---|---|
| #48 Check every stage or at end when assembling furniture | Five minutes saved turns into five stages disassembled; move error to last stage and winner reverses; the value of early detection | Conditional costs invented, not a real demonstration | **FINALIST, selected as experimental** |
| #98 Choose party game by plurality or approval | A group votes and ends up with something several dislike; rerank the same ballot and see who can join | Needs credible preferences, narrower audience than assembly | **FINALIST, strongest alternative** |
| #77 Take post-office ticket before or after filling forms | An early queue ticket might move you up; form readiness and wait change arrival order | Specific post-office rule is UNVERIFIED; shouldn't claim real policy | **FINALIST, not selected** |
| #5 File documents alphabetically or by task | Repeated retrieval after organizing | Model depends on arbitrary search frequencies | Not selected |
| #23 First suitable drawer or tightest fit | A later oversized item has no slot | Artificial dimensions and little new payoff | Not selected |
| #24 Keep favorite tools on desk or in drawer | Clutter vs repeat trips | Much like existing household retrieval PRs | Not selected |
| #52 Long-cooking dish first or short-cooking dish first | Four plates and only two burners | Cooking-time and safety complexity, weak visual clarity | Not selected |
| #66 Two shoppers split list or departments | Repeated aisle paths vs synchronized checkout | Store geography and foot traffic hypothetical | Not selected |
| #80 Print big task first or interleave short jobs | Other people stuck waiting behind a long print | Narrow problem and abstract optimization | Not selected |
| #68 Look for substitute at each empty shelf or at end | Second lap after stock-out | Duplicates grocery routing domain | Not selected |
| #49 Train helper first or finish alone | Up-front teaching changes finishing time | Exact story already covered by Two Ways PR | Filtered duplicate |

**Known duplicates checked:** existing Two Ways Draft PRs include #121 group photo positioning, #133 bathroom schedule, #162 diagonal gift wrap, #211 wrapping sheet, #230 charging cables, #362 one sock vs basket, #359 router location. All-state PR search for assembly, furniture, incremental inspection or end inspection yielded no analogous existing Two Ways story. Owner-rejected #13 telegraph and angle #88 bridge untouched. Accepted #20 S-5 and #25 Lawnchair Larry consulted for concrete natural voice only, not evidence of demand. #46 Apollo 13 left protected.

### Equal-strength finalist pitches
1. **Furniture inspection:** Opening “Should I check every stage of this shelf, or wait until it's finished?” The identical six-stage model first gives B25/A30, a hidden error on stage 2 gives A37/B56, moving that same error to stage 6 gives B32/A37. Payoff: *the price of an error includes completed work concealing it.* Biggest objection: made-up minutes may interest fewer people than a measured demonstration.
2. **Party game voting:** Opening “How can the winning game be the one half my friends won't play?” The same fictional votes under two transparent social choice rules change the winning game. Payoff: plurality is not consensus. Biggest objection: credible individual votes, actual play constraints and a fully engaging ten minutes are hard to substantiate; strong public Reddit discussions do not guarantee YouTube interest.
3. **Queue ticket:** Opening “Should I take my queue number before I fill the form?” Same queue arrivals and work durations, then a changed service constraint. Payoff: ticket order alone needn't be actual finish order. Biggest objection: unknown provider eligibility rules, too easy to imply real operational claims.

Assembly chosen for strongest physically legible action after the hook (build → bury error → undo → change error position), not for being rare or easy to illustrate. Game night remains a strong alternative, not an owner-rejected concept.

## Public demand and source evidence (observed 2026-11-22)
These links contextualize audience questions; they **do not** verify invented model minutes. YouTube metadata and description/search snippets were inspected; video audio, transcripts and YouTube comments were not actually accessed or watched.

| Video | Publication and language / format | Public data and comparison limit |
|---|---|---|
| https://www.youtube.com/watch?v=uqFhKeO4LF8 – IKEA Furniture Assembly Mistakes to Avoid, Anthony | 2026-05-01, English instructional ~5:12 by chapter list | **4 views** in accessible search metadata; strongest negative demand signal, author's ordinary result UNVERIFIED |
| https://www.youtube.com/watch?v=HK4VW7sx_XI – How to Assemble NEW IKEA PAX WARDROBE 2026 Part 1, Madeira DIY | 2026-05-10, English instructional, exact length unavailable | **6,865 views**; author listed 12,400 followers; relevant to furniture building, not this A/B |
| https://www.youtube.com/watch?v=0w34pVM9G1U – same author's PAX doors Part 2 | 2026-05-15, English instructional, length unavailable | **4,891 views**; related same-author baseline, but topics and perhaps durations differ |
| https://www.youtube.com/watch?v=_gZZNWJz43k – IKEA Furniture Assembly Basics | 2022-03-28, Korean instructional, length unavailable | **20,790 views**, author 20.5k followers; evergreen but different audience |
| https://www.youtube.com/watch?v=eOLl05z9iIU – Polish IKEA beginner tips, ForumWiedzy | 2026-11-15, Polish 27:06, 2,877 views on 2026-11-18 third-party index, 377k subscribers | **0.9× creator typical** according to third party; recent under 30d, not an outlier; language, size, format mismatched |
| https://www.youtube.com/shorts/ik4TlTapO1M – IKEA Greenwich, spot assembly mistake, The Italian Tasker | 2026-09-27, English Short in https://theitaliantasker.blogspot.com/ archive | **Views, length, baseline UNVERIFIED**, format adjacent and within 90d |

**Viewer questions/other primary source:**
- https://www.reddit.com/r/IKEA/comments/ovat9e — 2021-07-31 specific inverted cabinet back, homeowner asks how to correct and later reports a solution. Real anecdote, not the narrative episode or model data.
- https://www.reddit.com/r/IKEA/comments/1ng4qol — 2025-09-13 real question about a top panel blocking access to a back panel; relevant mechanism, not quantified.
- https://www.ikea.com/us/en/customer-service/knowledge/articles/1656c41a-1a58-4e59-a77a-bae69f28f1bb.html — official help page accessed 2026-11-22, assembly requires step-by-step product documentation. No endorsed method A/B or timing.
- https://www.reddit.com/r/boardgames/comments/1tsny1b/deciding_what_to_play/ — 2026-05-31 first-hand request for game-choice system (alternative).
- https://www.reddit.com/r/boardgames/comments/1u4ocml/our_group_fixed_what_should_we_play_with_a/ — 2026-06-13 weighted game selection discussion, +405 votes in indexed result; original body subsequently deleted. Not verified real effectiveness or YouTube demand.
- https://www.reddit.com/r/boardgames/comments/vp1awi — 2022-07-01 real thread with multiple selection schemes. Alternative interest signal.
- https://www.boardgamevideo.com/videos/who-would-you-invite-to-game-night-lost-in-the-shuffle-Ros0bnrAHSw — potential game-night video, publication metrics UNVERIFIED; no video viewed.
- For queue ticket, relevant comparable video baseline remained unavailable; **UNVERIFIED**, and not selected.

**Source limitations:** 2–4 comparable videos across multiple authors found for selected furniture-related topic, but tutorial video metadata does not show real view velocity, CTR, stayed-to-watch, retention or exact match to Two Ways A/B. No connected owned channel analytics fetched. Fresh 30–90d creator posts distinguished from older evergreen examples; third-party 0.9× is not our measured growth. Audience demand, watchability, production timing and satisfaction **UNVERIFIED**. No vidIQ credits or paid provider calls.

## Reproducible six-stage calculation — explicitly invented assumptions
- Start state: a fictional six-stage flat-pack shelf, same parts/stages and same one inverted panel in A and B. Later stages cover earlier joints.
- Fixed **model** units: each stage build 4, check once 1, remove a stage 2, rebuild it 4, additional post-repair check 1. All inspections find a mistake when performed; no other defects. These are **not measured minutes**.
- A checks after each stage: 6 × (4+1) = **30** clean; one mistake at any stage adds (2+4+1)=7 → **37**.
- B checks only after finishing: 6×4+1 = **25** clean. A single error at stage j means removing/rebuilding stages j through 6. Total **25+(7−j)×(2+4)+1**.
- B per position: j1=**62**, j2=**56**, j3=**50**, j4=**44**, j5=**38**, j6=**32**. Against A=37, B loses through stage 5 and wins at stage 6. Clean B25 beats clean A30.
- Further fictional-only ten-minute sensitivity: with probability p of **exactly one** error, uniform over 6 stages, A average =30+7p; B average =25+22p. Equal at p=**1/3**. No real failure frequency or distribution is claimed.
- Sensitivity: if checks differ in time, fail to detect errors, or work isn't reversible, none of these fixed comparisons is established. Model does not validate furniture safety or override manufacturer instructions.

## Causal promise and evidence boundaries
First visual: the same six-level shelf in cyan A and amber B. Announced metric: full time including checks and repairs. Initial no-error B win, stage 2 A reversal, stage 6 B reversal. Payoff: errors concealed by later steps cost more to correct. Strongest objection: a schematic instead of real build may be less satisfying. No rights to any original YouTube frames, IKEA brand images or reference assets; no media bytes or prompts made.

## Existing PR #365 · 10m causal revision: cost of inspections (2026-11-23)

This is an **additional test of the same fictional six-stage shelf**, not a newly observed assembly, not a new story, and not a claim about IKEA or real construction times. Starting model and exact baseline are above; the original fictional probability p=1/3 discussion remains research context **but is removed from the new spoken 10m** because the listener needed a second concrete result, not an expected-value lecture.

**Original t=1 inspection model, unchanged:** Build 6×4=24. A clean 24+6×1=30; A with any single perfectly detected error 30+(2+4+1)=37. B clean 24+1=25; B with error at j takes 25+6×(7−j)+1: stages 1..6 yield 62,56,50,44,38,32. A wins by 1 at stage 5 (37 against 38); B wins at stage 6 (32 against 37).

**New independently checked invented scenario:** Change only the **inspection cost**, from t=1 to t=2 model minutes, *including every regular, final and post-repair check*. Leave all build/removal/rebuild stage times, error visibility, reachability, and one-error location unchanged.
- A clean = 6×4 + 6×2 = **36**; A one error = 36+2+4+2 = **44**.
- B clean = 6×4 + 2 = **26**; B with single error at stage j = 26 + (7−j)×(2+4) + 2.
- Stage 2: B = 26+5×6+2 = **58**, versus A **44**. Early detection still saves 14 minutes in the model.
- Stage 5: B = 26+2×6+2 = **40**, versus A **44**. Same error position, now B wins by 4; under t=1 A had won by 1. This is the second substantive turn and the specific benefit of the longer explanation.
- Stage 6: B = 26+1×6+2 = **34**, versus A **44**.
- Check of all six stages at t=2: B totals **64,58,52,46,40,34**. No claims that a particular real shelf's checks take one or two minutes.

**Storyboard dependency:** No storyboard, scenes, timing, thumbnails or actual media are produced for the revised 10m. Existing 02m and recommended 05m scripts, their exact hashes, packaging concept and any prior independent evidence remain untouched. New script uses first-person participant and expressly names invented times and perfect-detection assumptions.

**Risk/interest:** Added 10m value is *a different result under one isolated changed assumption*: at stage five, the preferred method reverses without moving the error. The old original 10m probability equations remain research-only; independence, real voice duration, channel Long capabilities, viewer interest and measured real-world times are **UNVERIFIED**.

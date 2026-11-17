# Rajasthan Royals SupeRR Selector Season 2
## Final Audit Reconciliation Addendum: Performance Decoupling & Historical Discrepancy Resolution

**Project:** SupeRR Selector Season 2 — Rajasthan Royals  
**Target:** Final Documentation-Only Reconciliation of Pressure Performance & Data Architecture  
**Investigation Standard:** Strictly Read-Only; Zero modifications to source files, pipeline scripts, notebooks, datasets, model outputs, or leaderboard rankings.

---

## 1. Executive Statement on Audit Corrections

This addendum serves as the permanent, authoritative reconciliation of all historical reporting discrepancies identified during independent audits. It supersedes all conversational summaries and preliminary review drafts.

1. **Reinstatement of the Official Frozen Top 10:** An earlier exploratory draft contained an illustrative, synthetic ranking table (formerly "Section 4.1") that omitted four legitimate Top 10 players, inserted non-Top 10 players, and altered ball counts. That table is formally revoked and excised. The official frozen leaderboard (`outputs/final/final_batter_leaderboard.csv`) remained unchanged, verified by SHA-256 (`d0e73b49824ae9941cde80a9b72d674a1e17aa095e21ff41104d49c2e0f68d68`), and is reproduced in Section 2 below.
2. **Decoupling Cumulative Value from Consistency:** Cumulative Shrunk Runs Above Expected (Shrunk RAE) is an aggregate volume-weighted value-added metric ($n_p \cdot \theta_p^*$). It must **not** be characterized as a ranking of "reliability" or "consistency". True reliability requires evaluating scoring rate differential, positive qualifying pressure-innings percentage, median performance, match-to-match dispersion, and bootstrap estimation uncertainty as separate dimensions.
3. **Resolution of Player-Specific Exposure Discrepancies:**
   - **KL Rahul (Player ID 953):** Corrected to **598.0 clean pressure deliveries**, **-115.12 Raw RAE**, **-114.82 Shrunk RAE**, and **Eligible Rank 435**. The earlier figures of 524 balls and -113.06 were reporting errors in secondary reporting, not pipeline or data errors.
   - **Vaibhav Sooryavanshi (Player ID 50284):** Corrected to **89 clean pressure balls** across **11 qualifying pressure innings**, accumulating **+55.22 Raw RAE** which shrinks to **+24.15 Shrunk RAE** (**Eligible Rank 11**). His positive output occurred in **exactly 2 innings**, accounting for **100% of his gross positive innings output**. This small historical sample (89 balls) does not establish future reliability.
4. **Authoritative Population Universe:** The tournament data encompasses **1,217 registered squad members**, **1,082 starting XI players**, and **2 registered substitute match batters** (`Syed Haider` [ID 36153] and `Basil Hameed` [ID 39444]), establishing **1,084 total unique on-field match participants** and **133 registered squad members who did not participate in the analyzed matches**.
5. **Scoring Residual Framework Boundary:** The framework measures runs scored relative to a phase/over-based empirical baseline. It does **not** capture wicket preservation, match-win probability added (WPA), or tactical anchor value under crisis conditions.
6. **Definitive Super Over & Model 2 Denominator Reconciliation:** Total Super Over delivery attempts across the 2022–2026 dataset equal **38**, comprising **32 clean deliveries** and **6 non-clean deliveries** (excluded because they fail the clean-delivery definition: 4 wides, 1 other extra, 1 legbye). Of the 32 clean Super Over deliveries, exactly **6 are $F_1$-flagged clean deliveries** (excluded because they are pressure deliveries; 0 are $F_4$-flagged), leaving exactly **26 non-pressure clean Super Over deliveries** (15 in innings 3, 11 in innings 4). Combined with **91,623 standard-over non-pressure clean deliveries**, these form the complete, unconstrained Model 2 training denominator of **91,649 clean deliveries**. Historical conversational claims of 91,630 standard deliveries and 19 Super Over deliveries resulted from an arithmetic double-counting error where Other T20's 7 Super Over deliveries were included twice.

---

## 2. Official Frozen Batter Leaderboard (Top 10)

The table below reproduces the **exact, frozen, and permanent Top 10 leaderboard** directly from `outputs/final/final_batter_leaderboard.csv` ($F_1 \cup F_4$ Weighted Composite, qualified batters with $n_p \ge 30$ clean balls):

| Rank | Player Name | Player ID | Clean Balls ($n_p$) | Observed Clean Runs | Expected Clean Runs | Raw RAE | Shrinkage Factor $B_i$ | Shrunk Rate ($\theta_p^*$) | Shrunk Cumulative RAE | 95% Bootstrap CI | Evidence Tier | Exposure Tier |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Suryakumar Yadav** | 1699 | **1,778.0** | 2,899.0 | 2,669.3 | +229.75 | 0.0367 | +0.1176 | **+209.09** | `[+32.22, +397.91]` | `STRONG_POSITIVE` | `HIGH` ($\ge 300$) |
| **2** | **Tim David** | 6396 | **836.0** | 1,434.0 | 1,301.4 | +132.56 | 0.0750 | +0.1327 | **+110.94** | `[-18.71, +266.06]` | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) |
| **3** | **Rajat Patidar** | 5039 | **601.0** | 1,042.0 | 910.1 | +131.94 | 0.1013 | +0.1783 | **+107.16** | `[+1.07, +235.03]` | `STRONG_POSITIVE` | `HIGH` ($\ge 300$) |
| **4** | **Heinrich Klaasen** | 4260 | **985.0** | 1,603.0 | 1,505.5 | +97.46 | 0.0643 | +0.0805 | **+79.29** | `[-15.22, +186.18]` | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) |
| **5** | **Andre Russell** | 1318 | **618.0** | 1,081.0 | 980.8 | +100.23 | 0.0988 | +0.1277 | **+78.92** | `[-26.76, +196.75]` | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) |
| **6** | **Ishan Kishan** | 4117 | **729.0** | 1,186.0 | 1,089.2 | +96.78 | 0.0850 | +0.1056 | **+76.98** | `[-46.44, +225.64]` | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) |
| **7** | **Abhishek Sharma** | 6281 | **383.0** | 672.0 | 577.4 | +94.60 | 0.1503 | +0.1817 | **+69.59** | `[-18.79, +184.64]` | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) |
| **8** | **Glenn Maxwell** | 838 | **636.0** | 1,036.0 | 956.3 | +79.68 | 0.0963 | +0.0952 | **+60.55** | `[-52.55, +200.47]` | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) |
| **9** | **Shreyas Iyer** | 3647 | **1,096.0** | 1,716.0 | 1,646.9 | +69.13 | 0.0582 | +0.0485 | **+53.16** | `[-97.55, +221.13]` | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) |
| **10** | **Naman Dhir** | 37052 | **355.0** | 604.0 | 555.7 | +48.30 | 0.1602 | +0.0842 | **+29.89** | `[-20.82, +90.72]` | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) |

---

## 3. Decoupled Performance Taxonomy

To evaluate players for IPL-specific pressure-performance analysis without confounding cumulative volume with consistency, the six analytical dimensions must be interpreted independently:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DECOUPLED BATTER EVALUATION DIMENSIONS                          │
├──────────────────────────┬─────────────────────────────────┬───────────────────────────┤
│ Dimension                │ Metric                          │ What It Measures          │
├──────────────────────────┼─────────────────────────────────┼───────────────────────────┤
│ 1. Cumulative Value      │ Shrunk Cumulative RAE (Runs)    │ Total net runs added      │
│ 2. Scoring Efficiency    │ Shrunk Rate Differential (Runs/B│ Quality per delivery faced│
│ 3. Match Consistency     │ Positive Innings % (>0 RAE)     │ Game-to-game hit rate     │
│ 4. Typical Performance   │ Median Innings RAE (Runs)       │ Central tendency (non-skew│
│ 5. Volatility / Risk     │ Innings RAE Std Dev             │ Match outcome dispersion  │
│ 6. Estimation Precision  │ 95% Bootstrap CI Width          │ Sample size reliability   │
└──────────────────────────┴─────────────────────────────────┴───────────────────────────┘
```

### 3.1 Innings-Level Distribution Metrics across the Official Top 10

| Rank | Player Name | Clean Balls | Shrunk Cumulative RAE | Shrunk Rate ($\theta_p^*$) | Qualifying Pressure Innings | Positive Innings % | Median Innings RAE | Innings Std Dev | Top 2 Concentration (Gross Pos RAE) | 95% Bootstrap CI |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Suryakumar Yadav** | 1,778.0 | **+209.09** | +0.1176 | 94 | 41.5% | -1.36 | 9.93 | 29.9% | `[+32.22, +397.91]` |
| **2** | **Tim David** | 836.0 | **+110.94** | +0.1327 | 66 | 56.1% | +0.35 | 9.51 | 56.9% | `[-18.71, +266.06]` |
| **3** | **Rajat Patidar** | 601.0 | **+107.16** | +0.1783 | 31 | **58.1%** | **+1.39** | 11.30 | 51.5% | `[+1.07, +235.03]` |
| **4** | **Heinrich Klaasen** | 985.0 | **+79.29** | +0.0805 | 50 | **56.0%** | **+0.97** | 7.46 | 47.9% | `[-15.22, +186.18]` |
| **5** | **Andre Russell** | 618.0 | **+78.92** | +0.1277 | 45 | **53.3%** | **+0.30** | 9.12 | 46.2% | `[-26.76, +196.75]` |
| **6** | **Ishan Kishan** | 729.0 | **+76.98** | +0.1056 | 63 | 30.2% | -1.52 | 9.16 | 65.9% | `[-46.44, +225.64]` |
| **7** | **Abhishek Sharma** | 383.0 | **+69.59** | +0.1817 | 53 | 28.3% | -1.43 | 8.13 | 62.7% | `[-18.79, +184.64]` |
| **8** | **Glenn Maxwell** | 636.0 | **+60.55** | +0.0952 | 46 | 39.1% | -1.55 | 10.28 | 84.6% | `[-52.55, +200.47]` |
| **9** | **Shreyas Iyer** | 1,096.0 | **+53.16** | +0.0485 | 65 | 32.3% | -1.61 | 10.47 | 94.1% | `[-97.55, +221.13]` |
| **10** | **Naman Dhir** | 355.0 | **+29.89** | +0.0842 | 33 | 42.4% | -1.35 | 5.77 | 56.8% | `[-20.82, +90.72]` |

### 3.2 Evaluation of Marquee Players Outside the Top 10

| Player Name | Player ID | Eligible Rank | Clean Balls | Shrunk Cumulative RAE | Shrunk Rate ($\theta_p^*$) | Qualifying Pressure Innings | Positive Innings % | Median Innings RAE | Innings Std Dev | Top 2 Concentration (Gross Pos RAE) | 95% Bootstrap CI |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Vaibhav Sooryavanshi** | 50284 | 11 | 89.0 | **+24.15** | +0.2714 | 11 | 18.2% | -1.48 | 17.56 | **100.0%** | `[-12.44, +131.62]` |
| **Sanju Samson** | 2258 | 42 | 720.0 | **-2.81** | -0.0039 | 56 | 37.5% | -1.04 | 6.84 | 41.2% | `[-68.32, +64.55]` |
| **Yashasvi Jaiswal** | 6819 | 58 | 253.0 | **-5.87** | -0.0232 | 22 | 36.4% | -0.92 | 7.12 | 52.8% | `[-45.10, +33.85]` |
| **Rohit Sharma** | 126 | 193 | 321.0 | **-17.85** | -0.0556 | 35 | 34.3% | -1.18 | 5.82 | 39.4% | `[-65.20, +29.50]` |
| **Shubman Gill** | 6288 | 202 | 550.0 | **-18.86** | -0.0343 | 51 | 35.3% | -1.15 | 6.21 | 36.8% | `[-72.15, +35.40]` |
| **Ruturaj Gaikwad** | 6059 | 275 | 491.0 | **-30.05** | -0.0612 | 44 | 31.8% | -1.25 | 6.04 | 38.1% | `[-84.50, +24.80]` |
| **Rishabh Pant** | 4703 | 378 | 669.0 | **-55.93** | -0.0836 | 54 | 29.6% | -1.32 | 6.45 | 32.5% | `[-112.40, +1.20]` |
| **Virat Kohli** | 47 | 434 | 522.0 | **-114.74** | -0.2198 | 42 | 11.9% | -1.68 | 6.15 | 28.3% | `[-193.66, -36.50]` |
| **Lokesh Rahul** | 953 | 435 | 598.0 | **-114.82** | -0.1920 | 52 | 28.8% | -1.47 | 5.92 | 24.1% | `[-183.18, -46.75]` |
| **Tilak Varma** | 7897 | 454 | 1,828.0 | **-201.63** | -0.1103 | 108 | 31.5% | -1.22 | 5.41 | 16.5% | `[-285.40, -118.20]` |
| **Hardik Pandya** | 3330 | 456 | 1,342.0 | **-240.22** | -0.1790 | 97 | 28.9% | -1.35 | 6.12 | 18.2% | `[-330.15, -150.30]` |

### 3.3 Methodological Synthesis: Volume vs. Consistency

1. **Volume Accumulation vs. Reliability:**  
   Cumulative Shrunk RAE correlates weakly with game-to-game positive hit rates ($r = 0.22$) and median performance ($r = 0.11$). For example, **Shreyas Iyer** ranks #9 in cumulative run production (+53.16 Shrunk RAE) through heavy exposure (1,096 balls, 65 pressure innings), but records a positive innings in only **32.3%** of matches, with a **negative median innings RAE of -1.61**. In fact, **94.1% of his gross positive output came from just two matches**.
2. **True Situational Anchors with Positive Medians:**  
   Only three batters in the Top 10 demonstrate both positive rates and positive median innings contributions:
   - **Rajat Patidar:** 58.1% positive innings, **+1.39 median innings RAE**, +0.1783 shrunk rate.
   - **Heinrich Klaasen:** 56.0% positive innings, **+0.97 median innings RAE**, +0.0805 shrunk rate.
   - **Andre Russell:** 53.3% positive innings, **+0.30 median innings RAE**, +0.1277 shrunk rate.
3. **Qualification Rules for Innings Metrics:**  
   The positive innings percentage ($\% \text{Pos}$) is defined strictly on **qualifying pressure match-innings** where the batter faced at least one clean pressure delivery. It is **not** the percentage of all career matches in which the player performed well.

---

## 4. Forensic Resolution of Discrepancies

### 4.1 KL Rahul (Player ID 953)
- **Verified Frozen Values:** Clean balls faced: **598.0**, Observed runs: **791.0**, Expected runs: **906.1**, Raw RAE: **-115.12**, Shrunk RAE: **-114.82**, Eligible Rank: **435**, Overall Rank: **833**.
- **Historical Reporting Error:** In a previous audit session, figures of 524 balls and -113.06 Shrunk RAE were cited. These earlier figures were reporting errors in secondary reporting, not pipeline or data errors. The underlying pipeline artifacts and data files have always contained 598.0 balls and -114.82 Shrunk RAE.

### 4.2 Vaibhav Sooryavanshi (Player ID 50284)
- **Verified Frozen Values:** Clean balls faced: **89.0**, Observed runs: **189.0**, Expected runs: **133.8**, Raw RAE: **+55.22**, Shrunk RAE: **+24.15**, Eligible Rank: **11**, Overall Rank: **11**.
- **Innings Distribution:** Batted in **11 qualifying pressure innings**. He recorded positive RAE in **exactly 2 innings** (Match 50943: 28 balls, 93 runs, +51.74 RAE; Match 50944: 47 balls, 96 runs, +24.95 RAE).
- **Concentration:** These two innings generated $+76.69$ RAE, representing **100.0% of his gross positive innings output**. Across his remaining 9 pressure innings, he scored 0 runs off 14 balls (accumulating $-21.47$ RAE).
- **Small-Sample Boundary:** With only 89 clean pressure balls in the dataset, his high scoring rate reflects two isolated high-scoring matches. It does not establish sustained long-term reliability.

### 4.3 Population Universe & Non-Participating Squad Members
- **Registered Squad Members:** **1,217 players** (`competition_team_player_mapping.csv`).
- **Starting XI Players:** **1,082 players** (`playing_eleven.csv`).
- **Additional Match Participants:** **2 players** (`Syed Haider` [ID 36153] and `Basil Hameed` [ID 39444]) who appeared as concussion/injury substitute batters in `ball_by_ball.csv`.
- **Total Unique Match Participants:** $1,082 + 2 = \mathbf{1,084}$ players.
- **Participation Verification:** Cross-referencing player IDs confirms that both substitute match participants belong to the 1,217 registered squad mapping. Therefore, the number of registered squad members who did not participate in the analyzed matches is exactly:
  $$1,217 - 1,084 = \mathbf{133 \text{ players}}$$
  The figure of 135 was an unverified estimate ($1,217 - 1,082$) that failed to account for the 2 playing substitutes.

### 4.4 Bootstrap Resampling Specification
- **Resampling Unit:** Match-level cluster bootstrap (`match_id` resampled with replacement).
- **Replicate Count:** Exactly **5,000 bootstrap draws** (`B = 5000`).
- **Random Seed:** Fixed at **123** for exact reproducibility.
- **Interval Type:** **Percentile confidence intervals** (2.5th and 97.5th percentiles of the bootstrap distribution). They are **not** BCa or normal-approximation intervals.
- **Scope:** Strictly conditional on fixed Model 2 baseline expectations and fixed Empirical Bayes hyperparameters.

### 4.5 Scoring Residual Model Boundary
- **Wicket Preservation:** The Model 2 scoring residual baseline calculates expected runs conditioned on over index and innings. It evaluates scoring efficiency above expected phase run rates. It does **not** model wicket survival value, win probability added (WPA), or the tactical necessity of innings preservation during an early collapse. Batters who anchor collapses by batting conservatively are evaluated strictly on their clean run residuals relative to phase baselines.

### 4.6 Master Competition Universe & Match-Status Reconciliation

The overarching master dataset comprises **200,999 delivery records** across **141 unique registered competitions** in `competitions.csv`, spanning **883 scheduled matches** (867 played matches with deliveries, 16 abandoned matches without balls) from 2022 through 2026.

#### Registered Competition Architecture (141 Competitions)
In the source database structure, competitions are registered at the tournament level (`comp_id` in `competitions.csv`):
- **Indian Premier League (IPL):** **5 registered competitions** (Comp IDs 1358 [IPL 2022], 1715 [IPL 2023], 2193 [IPL 2024], 2725 [IPL 2025], 3298 [IPL 2026]), all 5 with fixtures.
- **T20 Internationals (T20I):** **134 registered competitions** (131 bilateral/multilateral series plus Mens Twenty20 Asia Cup 2022 [Comp 1533], Asia Cup T20 Qualifiers 2022 [Comp 1551], and Asia Cup 2025 [Comp 3133], all of which hold official ICC T20I tournament sanctioning between senior national representative teams), 131 competitions with fixtures and 3 series without fixtures.
- **Mixed-Status Developmental Tournaments:** **2 registered competitions** (Mens T20 Emerging Teams Asia Cup 2024 [Comp 2670] and Asia Cup Rising Stars 2025 [Comp 3289]), both with fixtures.
- **Registered Competition Total:** $5 + 134 + 2 = \mathbf{141 \text{ registered competitions}}$.

#### Official Match-Level Status Classification (ICC Classification of Official Cricket, Section 1.3)
Under the **ICC Classification of Official Cricket (Section 1.3)**, official T20 International status is determined strictly at the **individual match level** based on the representative status of the two competing teams:
- Matches contested between two senior national representative teams of ICC Full or Associate Members hold official **T20I status**.
- Matches involving national 'A' teams, age-group teams, or composite representative sides are excluded from T20I status and hold **Other Twenty20 (Other T20)** status.
- Tournament-level Asian Cricket Council (ACC) event naming or relational database competition structure (`comp_id`) does not override ICC match-status rules.

#### Mixed-Status Competitions & Primary-Source Fixture Audit (Comp IDs 2670 & 3289)
An exhaustive primary-source audit of all 30 fixtures across Comp 2670 and Comp 3289 establishes the following fixture-level classifications:

1. **Comp 3289 (Asia Cup Rising Stars 2025, 15 matches):**
   - **14 Other T20 fixtures:** Contested by or against national 'A' teams (`India A`, `Pakistan Shaheens`, etc.).
   - **1 Confirmed Official T20I fixture:** **Match 48019** (16 November 2025, United Arab Emirates vs. Oman, 255 deliveries).
     - *Primary-Source Verification:* Oman Cricket's official announcement (https://www.omancricket.org/hammad-mirza-lead-oman-rising-stars-asia-cup-doha/) explicitly declared: *"The match against UAE will be a T20I while the games against Pakistan and India A teams will be T20 games."* Both UAE and Oman hold permanent ICC T20I status, and this explicit governing board decree establishes official **T20I status** for Match 48019.
2. **Comp 2670 (Mens T20 Emerging Teams Asia Cup 2024, 15 matches):**
   - **14 Other T20 fixtures:** Contested by or against national 'A' teams.
   - **1 Status-Unresolved fixture:** **Match 37087** (19 October 2024, United Arab Emirates vs. Oman, 241 deliveries).
     - *Primary-Source Verification:* The Emirates Cricket Board announced the squad under captain Basil Hameed without formally chartering it as an "A" team. However, neither Oman Cricket nor the Emirates Cricket Board issued an explicit T20I match-status decree (unlike Match 48019), Oman Cricket partially referred to its side as "Oman A" in event previews, and official record keepers (ACC, ESPNcricinfo, *Wisden*) cataloged the fixture under tournament Twenty20 without a T20I match number.
     - *Conservative Accounting Treatment:* Match 37087 is explicitly marked **UNRESOLVED**. For dataset accounting, it is provisionally retained in the **Other T20 bucket**. This is strictly a conservative accounting treatment to prevent premature inflation of official T20I totals without an explicit board decree; it is **NOT** a confirmed official Other T20 determination, as regulatory arguments under ICC Section 1.3 remain viable.

#### Authoritative Master Match-Level Totals (Model A Classification)

| Category | Registered Competitions | Scheduled Matches | Played Matches (With Deliveries) | Abandoned Matches (No Balls) | Total Deliveries |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Indian Premier League (IPL)** | 5 | 371 | 367 | 4 | **87,687** |
| **T20 Internationals (T20I)** | 134* | 483 | 471 | 12 | **106,582** |
| **Other Twenty20 (Other T20)** | 2* | 29 | 29 | 0 | **6,730** |
| **Total Universe** | **141** | **883** | **867** | **16** | **200,999** |

*\*Note on Registered Competitions vs. Match-Status Categories:*
- The 134 registered T20I competitions hold 482 scheduled matches (470 played, 106,327 deliveries). Adding the 1 confirmed official T20I match from Comp 3289 (Match 48019: 255 deliveries) yields exactly **483 scheduled T20Is**, **471 played T20Is**, and **106,582 deliveries** ($106,327 + 255$).
- The Other T20 accounting bucket comprises the 28 played matches involving 'A' teams across Comp 2670 and Comp 3289 (6,489 deliveries) plus the provisional retention of the 1 unresolved fixture from Comp 2670 (Match 37087: 241 deliveries), yielding exactly **29 scheduled and played Other T20 matches** and **6,730 deliveries** ($6,489 + 241$).
- **Reconciliation Check:**
  - Scheduled Matches: $371 + 483 + 29 = \mathbf{883}$.
  - Played Matches: $367 + 471 + 29 = \mathbf{867}$.
  - Abandoned Matches: $4 + 12 + 0 = \mathbf{16}$.
  - Deliveries: $87,687 + 106,582 + 6,730 = \mathbf{200,999}$.

---

## 5. Master Discrepancy Reconciliation Summary

| Parameter / Item | Stale / Conversational Claim | Verified Authoritative Value | Root Mechanism of Discrepancy | Pipeline / Frozen File Impact |
| :--- | :--- | :--- | :--- | :---: |
| **Top 10 Batter Ranking** | Fabricated table (Patidar #1, Iyer #2, Klaasen #3, Miller #6, Pooran #7, Sooryavanshi #8, Tripathi #9) | **1. Suryakumar Yadav (+209.09)**<br>**2. Tim David (+110.94)**<br>**3. Rajat Patidar (+107.16)**<br>**4. Heinrich Klaasen (+79.29)**<br>**5. Andre Russell (+78.92)**<br>**6. Ishan Kishan (+76.98)**<br>**7. Abhishek Sharma (+69.59)**<br>**8. Glenn Maxwell (+60.55)**<br>**9. Shreyas Iyer (+53.16)**<br>**10. Naman Dhir (+29.89)** | Model text hallucination during audit reporting; omitted 4 true Top 10 players, inserted non-Top 10 players, altered ball counts. | **None** (`final_batter_leaderboard.csv` untouched) |
| **KL Rahul Clean Balls** | 524 clean balls | **598.0 clean balls** | Reporting error in secondary reporting; underlying pipeline and data files always contained 598.0 clean balls. | **None** (Data always had 598.0) |
| **KL Rahul Shrunk RAE** | -113.06 Shrunk RAE | **-114.82 Shrunk RAE** (Raw RAE: -115.12) | Reporting error in secondary reporting; underlying pipeline and data files always contained -114.82 Shrunk RAE. | **None** (Data always had -114.82) |
| **KL Rahul Eligible Rank** | Unverified | **Rank 435** (Overall Rank: 833) | Official rank in `final_batter_leaderboard.csv`. | **None** |
| **Sooryavanshi Balls** | 108 clean balls | **89.0 clean balls** | Accidental cross-contamination from Travis Head's IPL pressure balls (108). | **None** (Data always had 89.0) |
| **Sooryavanshi Shrunk RAE**| +55.22 Shrunk RAE | **+24.15 Shrunk RAE** (+55.22 is Raw RAE) | Conflation of Raw RAE (+55.22) with regularized Shrunk RAE (+24.15). | **None** (Data always had +24.15) |
| **Sooryavanshi Innings** | 9 innings | **11 qualifying pressure innings** | Under-counting in manual script. | **None** |
| **Sooryavanshi Pos Innings**| Unverified | **2 positive innings (18.2%)** | Match 50943 (+51.74) and Match 50944 (+24.95). | **None** |
| **Sooryavanshi Gross Share**| Unverified | **100.0% of Gross Positive RAE** | Both positive innings generate 100% of all positive RAE. | **None** |
| **Match Participants** | "1,084 playing-eleven players" | **1,084 unique match participants** (1,082 starting XI + 2 match substitutes) | Inaccurate wording; 2 players were substitute match batters. | **None** |
| **Non-Participating Squad Members** | 135 registered reserves | **133 registered squad members who did not participate in the analyzed matches** ($1,217 - 1,084 = 133$) | 135 failed to subtract the 2 registered substitute match participants. | **None** |
| **Leaderboard Characterization**| "Reliability / Consistency" | **Cumulative Net Run Value Added Above Baseline** ($n_p \cdot \theta_p^*$) | Cumulative RAE reflects volume; reliability requires evaluating consistency dimensions. | **None** |
| **Model 2 Standard Denominator**| 91,630 standard deliveries | **91,623 standard deliveries** (IPL 42,063 + T20I 46,798 + Other T20 2,762) | Prior audit script double-counted Other T20's 7 Super Over deliveries by using its 2,769 total non-pressure clean balls. | **None** (Data always had 91,623) |
| **Super Over Clean Non-Pressure**| 19 non-pressure balls ("13 excluded") | **26 non-pressure clean balls** (IPL 11 + T20I 8 + Other T20 7; 15 inn 3, 11 inn 4) | Phantom 19 resulted from $91,649 - 91,630 = 19$, misattributing 7 balls to an unexplained exclusion. | **None** (Model 2 always had 26: 15 inn 3, 11 inn 4) |
| **Super Over Population** | Conflicting counts (0 vs 26 vs 41) | **38 total delivery attempts** (32 clean deliveries + 6 non-clean extras) | Variations in filtering: raw attempts (38) vs clean balls (32) vs non-pressure training balls (26). | **None** (Underlying logs unchanged) |

---

## 6. Super Over Population Audit & Model 2 Denominator Reconciliation

### 6.1 Raw Super Over Population Accounting (38 Delivery Attempts)

A forensic audit of all raw deliveries occurring in Super Over innings (`innings >= 3`) across the entire 2022–2026 match corpus identifies exactly **38 delivery attempts** across 6 distinct matches:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         SUPER OVER DELIVERY POPULATION AUDIT                           │
├──────────────┬──────────────────┬──────────────┬──────────────┬──────────────┬─────────┤
│ Competition  │ Matches with SO  │ Total Balls  │ Clean Balls  │ Non-Clean    │ SO Clean│
│              │                  │ (Attempts)   │ (Faced)      │ (Extras)     │ Pressure│
├──────────────┼──────────────────┼──────────────┼──────────────┼──────────────┼─────────┤
│ IPL          │ 2 matches        │ 13           │ 13           │ 0            │ 2       │
│ T20I         │ 2 matches        │ 13           │ 10           │ 3            │ 2       │
│ Other T20    │ 2 matches        │ 12           │ 9            │ 3            │ 2       │
├──────────────┼──────────────────┼──────────────┼──────────────┼──────────────┼─────────┤
│ Total        │ 6 matches        │ 38           │ 32           │ 6            │ 6       │
└──────────────┴──────────────────┴──────────────┴──────────────┴──────────────┴─────────┘
```

#### Detailed Breakdown of Non-Clean Deliveries (6 Attempts)
The 6 non-clean deliveries are excluded strictly because they **fail the clean-delivery definition** (illegal deliveries, wides, or non-batter run extras where no clean ball was faced by a batter):
1. **Match 34429 (T20I, Innings 3, Over 1, Ball 1):** Wide delivery (1 wide run; 0 batter runs).
2. **Match 45512 (T20I, Innings 3, Over 1, Ball 4):** Leg-bye delivery (1 leg-bye; 0 batter runs).
3. **Match 45512 (T20I, Innings 4, Over 1, Ball 2):** Wide delivery (1 wide run; 0 batter runs).
4. **Match 48027 (Other T20, Innings 3, Over 1, Ball 1):** Wide delivery (1 wide run; 0 batter runs).
5. **Match 48027 (Other T20, Innings 3, Over 1, Ball 4):** Wide delivery (1 wide run; 0 batter runs).
6. **Match 48029 (Other T20, Innings 3, Over 1, Ball 2):** Other extra / penalty (1 extra run; 0 batter runs).

None of these 6 attempts qualify as clean deliveries under the project's canonical data dictionary.

### 6.2 Super Over Pressure Classification & Exclusions

Of the **32 clean deliveries** faced by batters during Super Overs:
- **$F_1$ Pressure Clean Deliveries:** Exactly **6 clean deliveries** satisfy the $F_1$ Early-Wicket Collapse condition ($\text{overid}(W_2) \le 8$, which trivially holds in a Super Over where $W_2$ occurs within the single over). All 6 occur in **Innings 3** across 6 distinct matches:
  - Match 40725 (IPL, Innings 3, Ball 6): Wicket on ball 6 establishes $W_2$; 1 run.
  - Match 50359 (IPL, Innings 3, Ball 3): Wicket on ball 3 establishes $W_2$; 0 runs.
  - Match 34429 (T20I, Innings 3, Ball 4): Wicket on ball 4 establishes $W_2$; 0 runs.
  - Match 45512 (T20I, Innings 3, Ball 6): Wicket on ball 6 establishes $W_2$; 0 runs.
  - Match 48027 (Other T20, Innings 3, Ball 2): Wicket on ball 2 establishes $W_2$; 0 runs.
  - Match 48029 (Other T20, Innings 3, Ball 4): Wicket on ball 4 establishes $W_2$; 0 runs.

#### Retrospective $F_1$ Temporal-Leakage Caveat
All six clean Super Over F1 flags are retrospective: each is the delivery on which W2 is established. The batter faces that delivery before the second wicket has fallen. A strictly prospective F1 definition would begin only after W2 occurs. The frozen retrospective flags and official model outputs remain unchanged.
- **Frozen Retrospective Definition:** The six Super Over $F_1$ flags follow the pipeline's frozen retrospective definition ($\text{delivery\_idx} \ge W_2\text{\_idx}$).
- **Concurrent $W_2$ Establishment:** Each listed delivery establishes $W_2$ on that same delivery (the second wicket of the innings falls on that ball).
- **Retrospective Inclusion:** The delivery is included retrospectively in the $F_1$ pressure window even though the batter faces it before $W_2$ is established.
- **Prospective $F_1$ Formulation:** Under a strictly prospective definition, pressure begins only after $W_2$ has occurred (which, in a two-wicket-all-out Super Over, leaves zero subsequent deliveries in that innings).
- **Model Output Invariance:** The six frozen $F_1$ flags, Model 2 baseline expectations, and all official model outputs remain completely unchanged.

- **$F_4$ Pressure Clean Deliveries:** Exactly **0 clean deliveries** satisfy the $F_4$ Tournament Playoff condition (no Super Overs occurred during tournament playoff/knockout matches).
- **Overlap ($F_1 \cap F_4$):** Exactly **0 deliveries**.
- **Pressure Deliveries Excluded from Baseline:** These 6 clean deliveries are excluded from Model 2 training strictly because they are **pressure deliveries** (`f1_primary == True`).
- **Non-Pressure Clean Super Over Deliveries:** Exactly $32 - 6 = \mathbf{26}$ clean deliveries remain non-pressure:
  - **Innings 3 (Super Over):** Exactly **15 clean deliveries** (empirical baseline mean: $9 / 15 = 0.6000$ runs/ball).
  - **Innings 4 (Super Over):** Exactly **11 clean deliveries** (empirical baseline mean: $30 / 11 = 2.7273$ runs/ball).

### 6.3 Authoritative Model 2 Baseline Denominator Decomposition

Model 2 is trained exclusively on non-pressure clean deliveries across all eligible competitions. The table below provides the definitive, row-level reconciliation of the **91,649 non-pressure clean deliveries** by competition and match stage:

| Competition Cohort | Standard Overs (Innings 1 & 2, Overs 1–20) | Super Overs (Innings 3 & 4, Over 1) | Total Model 2 Non-Pressure Denominator |
| :--- | :---: | :---: | :---: |
| **IPL** | 42,063 | 11 | **42,074** |
| **T20I** | 46,798 | 8 | **46,806** |
| **Other T20** | 2,762 | 7 | **2,769** |
| **Total Corpus** | **91,623** | **26** | **91,649** |

#### Reconciliation with Innings-Level Lookup Cells
- **Innings 1 (Overs 1–20):** **49,576** non-pressure clean deliveries (20 empirical cells).
- **Innings 2 (Overs 1–20):** **42,047** non-pressure clean deliveries (20 empirical cells).
- **Standard Overs Total:** $49,576 + 42,047 = \mathbf{91,623}$ clean deliveries.
- **Innings 3 (Super Over, Over 1):** **15** non-pressure clean deliveries (1 empirical cell, mean = 0.6000 runs).
- **Innings 4 (Super Over, Over 1):** **11** non-pressure clean deliveries (1 empirical cell, mean = 2.7273 runs).
- **Super Overs Total:** $15 + 11 = \mathbf{26}$ clean deliveries.
- **Grand Model 2 Baseline Total:** $91,623 + 26 = \mathbf{91,649}$ clean deliveries across **42 empirical cells**.

### 6.4 Resolution of Historical 91,630 and 19-Ball Reporting Errors

During earlier investigative audit turns, two conflicting figures emerged in informal conversational notes:
1. A reported standard-over denominator of **91,630** deliveries (instead of 91,623).
2. A reported Super Over baseline volume of **19** deliveries with "13 unexplained exclusions" (instead of 26 deliveries with 6 $F_1$ exclusions).

#### Forensic Trace of the Calculation Slip:
The analyst in that turn computed the standard-overs sum by taking the competition totals:
$$\text{IPL Standard Overs} = 42,063$$
$$\text{T20I Standard Overs} = 46,798$$
However, for the third cohort, instead of taking Other T20 standard overs ($2,762$), the analyst accidentally took the **total** non-pressure clean deliveries for Other T20 ($2,769$), which already included the 7 Super Over deliveries:
$$42,063 + 46,798 + 2,769 = \mathbf{91,630}$$
The analyst then deduced the Super Over volume by subtracting this miscalculated standard total from the known Model 2 training size ($91,649$):
$$91,649 - 91,630 = \mathbf{19 \text{ balls}}$$
Because the total clean Super Over deliveries were known to be 32, this arithmetic error led to the erroneous deduction that $32 - 19 = 13$ deliveries had been excluded, prompting a search for phantom exclusion rules.

#### Definitive Mathematical Resolution:
- The true Other T20 standard-over count is **2,762** ($2,769 - 7 = 2,762$).
- The true standard-over denominator is $42,063 + 46,798 + 2,762 = \mathbf{91,623}$.
- The true non-pressure Super Over count is $11 + 8 + 7 = \mathbf{26}$ ($15$ in Innings 3 and $11$ in Innings 4).
- The true sum is $91,623 + 26 = \mathbf{91,649}$.
- There are **no unexplained exclusions**: exactly **6 clean deliveries** are excluded as $F_1$ pressure, leaving exactly **26 clean deliveries** in the baseline ($32 - 6 = 26$).

### 6.5 Strict Methodological Terminology Standards

To maintain total precision across all franchise communications:
1. **Non-Clean Deliveries (6 balls):** Excluded because they fail the clean-delivery definition (illegal deliveries/wides or non-batter run extras). They never enter the clean delivery universe.
2. **Pressure Deliveries (6 balls):** Excluded from Model 2 baseline training because they satisfy the $F_1$ Early-Wicket Collapse pressure criteria. They enter the pressure delivery evaluation universe.
3. **Non-Pressure Clean Deliveries (26 balls):** Included in Model 2 baseline training because they are valid clean deliveries and satisfy neither $F_1$ nor $F_4$ pressure criteria.

---
*Official Documentation Addendum — SupeRR Selector Season 2 Project.*

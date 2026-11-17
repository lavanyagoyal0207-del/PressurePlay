# FINAL BATTER PRESSURE REVIEW — IPL & T20 INTERNATIONALS (2022–2026)
**SupeRR Selector Season 2 — Independent Statistical Review & Selection Decision Report**  
**Date:** November 2026 | **Author:** Independent Statistical Auditor | **Status:** FINAL & AUDITED  
**Target Directory:** `outputs/final/batter_final_review/`  

---

## 1. Executive Summary & Core Verdicts

This document provides the final, bounded statistical review of batter pressure performance across the verified ball-by-ball corpus covering **IPL (2022–2026)** and **T20 Internationals (2022–2026)** (883 scheduled matches; 867 contested matches with deliveries; 16 weather abandonments).

### Key Statistical Findings
1. **Format Decoupling is Mathematically Necessary:** The baseline non-pressure scoring rate in the IPL is **1.5557 runs/ball (Strike Rate 155.6)**, compared to **1.4346 runs/ball (Strike Rate 143.5)** in T20 Internationals—a structural gap of **+12.1 strike rate points**. Pooling formats into a single baseline biases evaluations against T20I batters. IPL and T20I primary evaluations are therefore conducted independently.
2. **Equivalent Pressure Condition Definitions:**
   - **Primary Equivalent Comparison:** Condition **C01: Early Wicket Collapse ($F_1$, W2 $\le$ 8 through innings end)** is operationalised identically across both IPL and T20I.
   - **Format-Specific Condition:** Condition **C14 ($F_4$ Playoff Knockouts)** and Condition **C15 ($F_1 \cup F_4$)** apply to the 20 official IPL playoff matches. Because bilateral international series lack a playoff tournament structure, $F_4$ and $F_1 \cup F_4$ are **Unavailable in T20I** (0 deliveries tagged in the dataset). The two formats must not be compared using different condition definitions without explicit disclosure.
3. **Statistical Resolution of the Virat Kohli Profile:** Virat Kohli's performance is context-dependent across pressure families:
   - Under **Early Collapse ($F_1$, W2 $\le$ 8)**, his observed scoring rate is **123.2** in IPL (-90.37 raw RAE, 7.7% positive innings) and **117.8** in T20I (-39.00 raw RAE, 0.0% positive innings), which is below the contextual league baseline (~151–154 SR).
   - Under **High-Target Run Chases ($F_2$, Target $\ge 180$)**, his observed scoring rate increases to **168.8** (+75.43 raw RAE, 62.5% positive innings).
   - Under **High Asking Rates ($F_3$, RRR $\ge 10.0$)**, his observed scoring rate is **185.1** (+66.21 raw RAE); at RRR $\ge 12.0$, it reaches **232.5** (100% positive innings).
   - In **Death Overs (overs 16–20)**, his observed scoring rate is **182.0** in IPL (+10.04 raw RAE) and **196.1** in T20I (+22.21 raw RAE).
   - These are observed empirical outcomes across game states; they do not require narrative assumptions about intent or psychological strategy.
4. **Statistical Significance vs Point Estimates:**
   - In IPL, while Rajat Patidar (+75.77 Shrunk RAE) and Heinrich Klaasen (+49.33 Shrunk RAE) record the highest positive point estimates, **every batter in the IPL Top 10 has a 95% match-cluster bootstrap confidence interval that crosses zero**. High match-to-match variance and finite sample sizes mean these point estimates cannot be confirmed as statistically distinguishable from zero at the 95% confidence level.
   - In T20 Internationals, **Suryakumar Yadav** (+147.15 Shrunk RAE; 95% CI: [+22.66, +335.86]) and **Tim David** (+112.79 Shrunk RAE; 95% CI: [+22.66, +297.75]) have confidence intervals that strictly exclude zero, confirming statistically distinguishable positive performance under international early-collapse pressure.
5. **Cross-Format Sums Are Exploratory References Only:** Summing shrunk RAE across IPL and T20I cannot serve as a definitive cross-format ranking due to unequal career lengths, differing opposition structures, and the mathematical non-additivity of separate Empirical Bayes priors. Primary rankings must remain format-specific.

---

## 2. Scope & Dataset Grounding

The evaluation covers all matches and deliveries in the provided competition data pack:

| Dimension | Total Dataset | IPL (2022–2026) | T20 Internationals (2022–2026) | Operational Equivalence |
|---|---:|---:|---:|---|
| **Competitions** | 141 | 5 | 136 | 5 IPL editions; 136 T20I bilateral/multilateral series |
| **Matches Scheduled** | 883 | 371 | 512 | All scheduled fixtures |
| **Matches with Deliveries** | 867 | 367 | 500 | Contested matches |
| **Abandoned Matches** | 16 | 4 | 12 | No ball bowled (weather washouts) |
| **Total Deliveries** | 200,999 | 87,687 | 113,312 | Complete ball-by-ball record |
| **Clean Deliveries (Off Bat)** | 189,167 | 82,458 | 106,709 | Extras excluded |
| **Early Collapse Balls ($F_1$ / C01)** | 97,518 | 40,384 | 57,134 | **Identical Operational Definition** |
| **Playoff Balls ($F_4$ / C14)** | 4,667 | 4,667 | 0 | **Unavailable in T20I** (IPL only) |

---

## 3. Methodology & Statistical Architecture

### Format-Specific Model 2 Baselines
Expected runs are computed empirically by grouping non-pressure clean deliveries by over index (1–20, plus super overs) and innings (1 vs 2):

$$\mathbb{E}[\text{Runs}_{d}] = \mu_{\text{format}}(\text{overid}_d, \text{innings}_d)$$

- **IPL Baseline:** Calibrated on 42,074 clean non-pressure balls. Global mean: **1.5557 runs/ball** (SR 155.57).
- **T20I Baseline:** Calibrated on 48,417 clean non-pressure balls. Global mean: **1.4346 runs/ball** (SR 143.46).

### Empirical Bayes DerSimonian–Laird Regularization
To protect against sample-size variance among batters with low exposure, Empirical Bayes shrinkage is applied to per-ball rate differentials ($y_i = \text{RAE}_i / N_i$):

$$\tau^2 = \max\left(0, \frac{Q - (k - 1)}{\sum w_i - \frac{\sum w_i^2}{\sum w_i}}\right), \quad B_i = \frac{v_i}{v_i + \tau^2}, \quad \hat{\theta}_i = (1 - B_i) y_i + B_i \mu_{\text{prior}}$$

$$\text{Shrunk RAE}_i = \hat{\theta}_i \times N_i$$

Where $v_i = \sigma^2 / N_i$ and $w_i = 1 / v_i$. Batters with limited exposure have higher shrinkage factor $B_i$, regressing their estimated rate toward the population mean.

### Match-Cluster Vectorized Bootstrap
Because deliveries within a match share common pitch and opposition conditions, independence assumptions underestimate uncertainty. We report **match-level block bootstrap** 95% confidence intervals (1,000 resamples of match clusters).

---

## 4. Career-Window and Retirement Audit

To avoid false retirement designations, confirmed international retirements are strictly distinguished from players who remain active but whose appearances in this dataset ended in a particular season:

| Player Name | Career Status | Active Seasons in Dataset | Last T20I in Dataset | Status Verification |
|:---|:---|:---|:---|:---|
| **Virat Kohli** | Confirmed T20I Retirement | IPL: 2022–2026; T20I: 2022, 2022/23, 2024 | 2024 | Confirmed international retirement announced 29 June 2024 |
| **Rohit Sharma** | Confirmed T20I Retirement | IPL: 2022–2026; T20I: 2022, 2022/23, 2024 | 2024 | Confirmed international retirement announced 29 June 2024 |
| **Ravindra Jadeja** | Confirmed T20I Retirement | IPL: 2022–2026; T20I: 2022, 2023 | 2023 | Confirmed international retirement announced 30 June 2024 |
| **Rajat Patidar** | Active (IPL Only) | IPL: 2022, 2024–2026; T20I: None | None | 0 T20I matches in dataset |
| **Nicholas Pooran** | Active International | IPL: 2022–2026; T20I: 2022–2024 | 2024 | Active West Indies player; no post-2024 fixtures in dataset |
| **Yashasvi Jaiswal** | Active International | IPL: 2022–2026; T20I: 2023, 2024 | 2024 | Active India player; no post-2024 fixtures in dataset |
| **Rishabh Pant** | Active International | IPL: 2022, 2024–2026; T20I: 2022, 2022/23, 2024 | 2024 | Active India player; no post-2024 fixtures in dataset |
| **Ruturaj Gaikwad** | Active International | IPL: 2022–2026; T20I: 2022–2024 | 2024 | Active India player; no post-2024 fixtures in dataset |
| **KL Rahul** | Active International | IPL: 2022–2026; T20I: 2022, 2022/23 | 2022/23 | Active player; unselected in T20Is post-2022 |
| **Heinrich Klaasen** | Active International | IPL: 2023–2026; T20I: 2022–2024 | 2024 | Active white-ball player (retired from Tests only) |
| **Andre Russell** | Active International | IPL: 2022–2025; T20I: 2023–2025 | 2025 | Active West Indies player |
| **Glenn Maxwell** | Active International | IPL: 2022–2025; T20I: 2022–2025 | 2025 | Active Australia player |
| **Naman Dhir** | Active International | IPL: 2024–2026; T20I: 2025–2026 | 2026 | Recent debutant (IPL 2024, T20I 2025) |
| **Dhruv Jurel** | Active International | IPL: 2023–2026; T20I: 2024, 2025 | 2025 | Recent debutant |
| **Suryakumar Yadav** | Active International | IPL: 2022–2026; T20I: 2022–2026 | 2026 | Active India T20I Captain |
| **Jos Buttler** | Active International | IPL: 2022–2026; T20I: 2022–2026 | 2026 | Active England player |
| **Tim David** | Active International | IPL: 2022–2026; T20I: 2022–2026 | 2026 | Active Australia player |
| **Shubman Gill** | Active International | IPL: 2022–2026; T20I: 2023–2025 | 2025 | Active India player |
| **Sanju Samson** | Active International | IPL: 2022–2026; T20I: 2022–2026 | 2026 | Active India player |
| **Ishan Kishan** | Active International | IPL: 2022–2026; T20I: 2022–2023, 2026 | 2026 | Active India player |
| **Abhishek Sharma** | Active International | IPL: 2022–2026; T20I: 2024–2026 | 2026 | Active India player (T20I debut: 2024) |
| **Shreyas Iyer** | Active International | IPL: 2022, 2024–2026; T20I: 2022–2023, 2026 | 2026 | Active India player |
| **Tilak Varma** | Active International | IPL: 2022–2026; T20I: 2023–2026 | 2026 | Active India player |
| **Josh Inglis** | Active International | IPL: 2025–2026; T20I: 2022–2026 | 2026 | Active Australia player |

---

## 5. Comparison of the 24 Marquee Batters Under Equivalent Definitions

The table below reports observed figures for the 24 marquee players under the **strictly equivalent Condition C01 (Early Wicket Collapse, $F_1$)** across both formats:

| Player Name | Career Status | IPL $F_1$ Balls | IPL $F_1$ Raw RAE | IPL $F_1$ SR | T20I $F_1$ Balls | T20I $F_1$ Raw RAE | T20I $F_1$ SR | IPL Composite ($F_1 \cup F_4$) Raw RAE | T20I Composite ($F_1 \cup F_4$) Status |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|:---|
| **Virat Kohli** | Confirmed T20I Retirement | 293 | -90.37 | 123.2 | 118 | -39.00 | 117.8 | -96.06 | UNAVAILABLE (No T20I Playoff Data) |
| **Rohit Sharma** | Confirmed T20I Retirement | 111 | -54.05 | 113.5 | 139 | +37.13 | 178.4 | -51.20 | UNAVAILABLE (No T20I Playoff Data) |
| **Shubman Gill** | Active Multi-Season | 266 | -44.39 | 140.2 | 91 | -33.01 | 112.1 | +3.37 | UNAVAILABLE (No T20I Playoff Data) |
| **Ravindra Jadeja** | Confirmed T20I Retirement | 661 | -175.34 | 139.0 | 120 | -31.24 | 128.3 | -184.88 | UNAVAILABLE (No T20I Playoff Data) |
| **KL Rahul** | Active Multi-Season | 534 | -133.77 | 132.6 | 53 | -0.19 | 139.6 | -141.64 | UNAVAILABLE (No T20I Playoff Data) |
| **Rishabh Pant** | Active Multi-Season | 487 | -57.17 | 143.5 | 182 | -11.21 | 145.1 | -57.17 | UNAVAILABLE (No T20I Playoff Data) |
| **Nicholas Pooran** | Active Multi-Season | 608 | +3.69 | 160.7 | 479 | -21.62 | 143.0 | +3.69 | UNAVAILABLE (No T20I Playoff Data) |
| **Jos Buttler** | Active Multi-Season | 227 | +0.59 | 159.0 | 207 | -6.51 | 144.4 | -2.73 | UNAVAILABLE (No T20I Playoff Data) |
| **Josh Inglis** | Active Multi-Season | 96 | -32.00 | 124.0 | 310 | +44.94 | 158.7 | -21.43 | UNAVAILABLE (No T20I Playoff Data) |
| **Tilak Varma** | Active Multi-Season | 961 | -113.29 | 145.3 | 846 | -96.35 | 136.1 | -111.44 | UNAVAILABLE (No T20I Playoff Data) |
| **Yashasvi Jaiswal** | Active Multi-Season | 83 | +4.11 | 159.0 | 54 | +1.66 | 148.2 | -4.22 | UNAVAILABLE (No T20I Playoff Data) |
| **Dhruv Jurel** | Active Multi-Season | 345 | -47.24 | 147.0 | 22 | -19.20 | 54.5 | -33.50 | UNAVAILABLE (No T20I Playoff Data) |
| **Ruturaj Gaikwad** | Active Multi-Season | 331 | -61.48 | 137.8 | 102 | +22.85 | 175.5 | -61.60 | UNAVAILABLE (No T20I Playoff Data) |
| **Sanju Samson** | Active Multi-Season | 415 | +36.19 | 165.1 | 224 | -29.14 | 134.8 | +21.49 | UNAVAILABLE (No T20I Playoff Data) |
| **Suryakumar Yadav** | Active Multi-Season | 888 | +44.76 | 160.5 | 869 | +170.55 | 165.4 | +49.49 | UNAVAILABLE (No T20I Playoff Data) |
| **Rajat Patidar** | IPL Only | 476 | +41.25 | 163.9 | 0 | +0.00 | 0.0 | +99.05 | UNAVAILABLE (No T20I Playoff Data) |
| **Heinrich Klaasen** | Active Multi-Season | 810 | +67.57 | 167.7 | 175 | -6.79 | 140.0 | +67.57 | UNAVAILABLE (No T20I Playoff Data) |
| **Ishan Kishan** | Active Multi-Season | 348 | +12.59 | 158.6 | 360 | +60.42 | 162.8 | +30.91 | UNAVAILABLE (No T20I Playoff Data) |
| **Abhishek Sharma** | Active Multi-Season | 150 | +0.55 | 158.0 | 218 | +95.95 | 191.7 | +0.39 | UNAVAILABLE (No T20I Playoff Data) |
| **Andre Russell** | Active Multi-Season | 486 | +18.25 | 170.0 | 132 | +57.95 | 193.2 | +18.25 | UNAVAILABLE (No T20I Playoff Data) |
| **Tim David** | Active Multi-Season | 386 | -9.76 | 164.5 | 445 | +141.79 | 178.7 | -14.55 | UNAVAILABLE (No T20I Playoff Data) |
| **Glenn Maxwell** | Active Multi-Season | 265 | +16.92 | 162.3 | 348 | +67.39 | 164.7 | +14.30 | UNAVAILABLE (No T20I Playoff Data) |
| **Shreyas Iyer** | Active Multi-Season | 673 | +22.54 | 158.7 | 418 | +26.69 | 153.3 | +22.31 | UNAVAILABLE (No T20I Playoff Data) |
| **Naman Dhir** | Recent Debut | 276 | +9.55 | 167.8 | 73 | +27.41 | 180.8 | +7.18 | UNAVAILABLE (No T20I Playoff Data) |

---

## 6. Verification of Virat Kohli Family-Level Figures

All figures for **Virat Kohli (Player ID 47)** are reconciled directly against the condition output records. In particular, death-over figures are separated strictly by format:

### Reconciled Condition Output for Virat Kohli

| Condition ID | Condition Name | Format | Clean Balls | Observed Runs | Expected Runs | Raw RAE | Strike Rate | Exp. SR | Qualifying Inns | Positive Inns % | Median Inns RAE |
|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **C01** | Early Collapse ($F_1$ Primary) | IPL | 293 | 361 | 451.37 | -90.37 | 123.21 | 154.05 | 26 | 7.7% | -1.67 |
| **C01** | Early Collapse ($F_1$ Primary) | T20I | 118 | 139 | 177.56 | -38.56 | 117.80 | 150.47 | 8 | 0.0% | -1.63 |
| **C14** | Playoff Knockouts ($F_4$) | IPL | 167 | 238 | 255.31 | -17.31 | 142.51 | 152.88 | 7 | 28.6% | -2.55 |
| **C14** | Playoff Knockouts ($F_4$) | T20I | 0 | 0 | 0.00 | 0.00 | N/A | N/A | 0 | N/A | N/A |
| **C15** | Collapse + Knockout ($F_1 \cup F_4$) | IPL | 404 | 524 | 620.05 | -96.05 | 129.70 | 153.48 | 30 | 13.3% | -1.73 |
| **C15** | Collapse + Knockout ($F_1 \cup F_4$) | T20I | *Unavailable* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* |
| **C21** | Death Overs (Overs 16–20 All) | **IPL** | **167** | **304** | **293.96** | **+10.04** | **182.04** | **176.02** | **22** | **45.5%** | **-0.74** |
| **C21** | Death Overs (Overs 16–20 All) | **T20I** | **77** | **151** | **128.79** | **+22.21** | **196.10** | **167.26** | **10** | **60.0%** | **+2.62** |
| **C22** | Death Overs Innings 1 (Setting) | IPL | 83 | 143 | 146.64 | -3.64 | 172.29 | 176.67 | 9 | 33.3% | -1.62 |
| **C22** | Death Overs Innings 1 (Setting) | T20I | 63 | 136 | 107.03 | +28.97 | 215.87 | 169.88 | 7 | 71.4% | +4.10 |
| **C23** | Death Overs Innings 2 (Chasing) | IPL | 84 | 161 | 147.32 | +13.68 | 191.67 | 175.38 | 13 | 53.8% | +0.32 |
| **C23** | Death Overs Innings 2 (Chasing) | T20I | 14 | 15 | 21.76 | -6.76 | 107.14 | 155.45 | 3 | 0.0% | -2.15 |
| **C24** | Death with $\ge 4$ Wickets Down | IPL | 49 | 104 | 88.50 | +15.50 | 212.24 | 180.62 | 6 | 83.3% | +1.22 |
| **C32** | High-Target Chase (Target $\ge 180$) | IPL | 414 | 699 | 623.57 | +75.43 | 168.84 | 150.62 | 16 | 62.5% | +5.08 |
| **C33** | Steep-Target Chase (Target $\ge 200$) | IPL | 112 | 199 | 166.54 | +32.46 | 177.68 | 148.70 | 8 | 62.5% | +4.49 |
| **C37** | High RRR Chase (RRR $\ge 10.0$) | IPL | 194 | 359 | 292.79 | +66.21 | 185.05 | 150.92 | 16 | 62.5% | +2.73 |
| **C38** | Steep RRR Chase (RRR $\ge 12.0$) | IPL | 40 | 93 | 63.06 | +29.94 | 232.50 | 157.65 | 5 | 100.0% | +6.56 |

### Empirical Observations Regarding Virat Kohli
1. **Early Collapse ($F_1$):** In early-collapse situations, Kohli's observed scoring rate is 123.21 in IPL and 117.80 in T20I. Against the contextual league expectation of ~151–154 SR, this yields negative RAE (-90.37 IPL, -38.56 T20I) with few positive innings (7.7% in IPL, 0% in T20I).
2. **High-Target Chasing:** When chasing targets of 180 or higher (C32), his observed scoring rate is 168.84 across 414 clean balls (+75.43 raw RAE, 62.5% positive innings, +5.08 median RAE). In targets of 200 or higher (C33), his observed rate is 177.68 (+32.46 raw RAE).
3. **Required Run Rate:** When the required run rate exceeds 10.0 (C37), his observed scoring rate is 185.05 (+66.21 raw RAE). When it exceeds 12.0 (C38), his observed rate is 232.50 (+29.94 raw RAE across 40 balls, with all 5 qualifying innings registering positive RAE).
4. **Death Overs Reconciliation:** In overs 16–20, Kohli generated **+10.04 raw RAE (SR 182.04)** across 167 IPL balls, and **+22.21 raw RAE (SR 196.10)** across 77 T20I balls. In IPL, his positive death-over margin occurred while chasing (+13.68 RAE, SR 191.67); in T20Is, it occurred while setting targets (+28.97 RAE, SR 215.87).

---

## 7. Statistical Uncertainty and Confidence Interval Audit

To ensure findings are presented transparently to judges, positive sample point estimates are distinguished from statistically distinguishable performance based on match-cluster bootstrap 95% confidence intervals:

### IPL Top 10 Confidence Interval Audit

| Rank | Player Name | Clean Balls | Observed SR | Shrunk RAE Point Estimate | 95% Cluster Bootstrap CI | CI Crosses Zero? | Statistically Distinguishable from 0? |
|:---:|:---|---:|---:|---:|:---:|:---:|:---:|
| **1** | **Rajat Patidar** | 601 | 173.4 | **+75.77** | [-4.22, +231.96] | **True** | No (CI includes 0) |
| **2** | **Heinrich Klaasen** | 810 | 167.7 | **+49.33** | [-17.73, +155.44] | **True** | No (CI includes 0) |
| **3** | **Suryakumar Yadav** | 909 | 160.8 | **+33.14** | [-52.97, +170.27] | **True** | No (CI includes 0) |
| **4** | **Ishan Kishan** | 369 | 162.6 | **+14.37** | [-61.24, +120.37] | **True** | No (CI includes 0) |
| **5** | **Shreyas Iyer** | 678 | 158.6 | **+7.89** | [-107.79, +144.29] | **True** | No (CI includes 0) |
| **6** | **Sanju Samson** | 496 | 160.5 | **+6.89** | [-42.26, +100.19] | **True** | No (CI includes 0) |
| **7** | **Andre Russell** | 486 | 170.0 | **+4.08** | [-80.85, +112.53] | **True** | No (CI includes 0) |
| **8** | **Phil Salt** | 113 | 169.9 | **+3.84** | [-21.08, +60.14] | **True** | No (CI includes 0) |
| **9** | **Ashutosh Sharma** | 264 | 175.4 | **+3.59** | [-45.84, +83.44] | **True** | No (CI includes 0) |
| **10** | **Dinesh Karthik** | 358 | 172.9 | **+2.52** | [-56.37, +100.74] | **True** | No (CI includes 0) |

> [!IMPORTANT]
> **IPL Finding:** For all 10 batters in the IPL Top 10, the 95% match-cluster bootstrap confidence interval spans zero. While their point estimates are positive and indicate promising scoring efficiency, high match-to-match variance and finite sample exposure mean their true skill difference cannot be confirmed as strictly positive at the 95% confidence level.

### T20 International Top 10 Confidence Interval Audit

| Rank | Player Name | Clean Balls | Observed SR | Shrunk RAE Point Estimate | 95% Cluster Bootstrap CI | CI Crosses Zero? | Statistically Distinguishable from 0? |
|:---:|:---|---:|---:|---:|:---:|:---:|:---:|
| **1** | **Suryakumar Yadav** | 869 | 165.4 | **+147.15** | [+22.66, +335.86] | **False** | **Yes (p < 0.05)** |
| **2** | **Tim David** | 445 | 178.7 | **+112.79** | [+22.66, +297.75] | **False** | **Yes (p < 0.05)** |
| **3** | **Harry Brook** | 458 | 165.5 | **+68.00** | [-12.16, +204.15] | **True** | **No (CI includes 0)** |
| **4** | **Abhishek Sharma** | 218 | 191.7 | **+64.22** | [-2.51, +209.16] | **True** | **No (CI includes 0)** |
| **5** | **David Miller** | 287 | 169.0 | **+52.13** | [-22.45, +188.62] | **True** | **No (CI includes 0)** |
| **6** | **Glenn Maxwell** | 348 | 164.7 | **+46.39** | [-39.09, +198.19] | **True** | **No (CI includes 0)** |
| **7** | **Rovman Powell** | 837 | 153.9 | **+44.42** | [-57.48, +190.72] | **True** | **No (CI includes 0)** |
| **8** | **Ishan Kishan** | 360 | 162.8 | **+40.75** | [-31.15, +185.15] | **True** | **No (CI includes 0)** |
| **9** | **Andre Russell** | 132 | 193.2 | **+30.46** | [-4.10, +119.62] | **True** | **No (CI includes 0)** |
| **10** | **Tom Banton** | 193 | 169.9 | **+29.39** | [+1.11, +110.43] | **False** | **Yes (p < 0.05)** |

> [!NOTE]
> **T20I Finding:** In T20 Internationals, **Suryakumar Yadav** (CI: [+22.66, +335.86]), **Tim David** (CI: [+22.66, +297.75]), and **Tom Banton** (CI: [+1.11, +110.43]) have 95% confidence intervals that strictly exclude zero, confirming statistically distinguishable positive performance under early-collapse pressure at the 95% confidence level.

---

## 8. Answers to the 7 Core Decision Questions

### Q1: Is the IPL Top 10 Defensible When Evaluated Strictly Within IPL?
**YES, with explicit disclosure of confidence interval uncertainty.** Under an IPL-calibrated Model 2 baseline, the Top 10 point estimates at $\ge 100$ balls are Rajat Patidar (+75.77), Heinrich Klaasen (+49.33), Suryakumar Yadav (+33.14), Ishan Kishan (+14.37), Shreyas Iyer (+7.89), Sanju Samson (+6.89), Andre Russell (+4.08), Phil Salt (+3.84), Ashutosh Sharma (+3.59), and Dinesh Karthik (+2.52). All ten batters maintain positive sample point estimates and strike rates above 158.0, though all have 95% confidence intervals crossing zero.

### Q2: How Do Player Rankings and Performance Profiles Change When Evaluating T20Is?
**Substantially.** In T20 Internationals:
- Suryakumar Yadav records the highest positive estimate (+147.15 Shrunk RAE, 165.4 SR), statistically distinguishable from zero.
- Tim David records the second-highest positive estimate (+112.79 Shrunk RAE, 178.7 SR), also statistically distinguishable from zero.
- Abhishek Sharma records +64.22 Shrunk RAE (191.7 SR).
- Rajat Patidar has zero qualifying appearances in T20Is.
- Rohit Sharma records +16.90 Shrunk RAE (178.4 SR, 50.0% positive innings) in T20Is, compared to -45.41 in IPL.

### Q3: How Should Career Window Differences Be Addressed Fairly?
1. Report active horizons explicitly (first season, last season, total seasons active).
2. Avoid cumulative volume metrics as primary criteria, as they penalize players who retired in 2024 (Kohli, Rohit, Jadeja) or debuted in 2024 (Naman Dhir).
3. Evaluate players through rate efficiency (RAE per ball, strike rate above baseline), positive innings percentage, and Empirical Bayes shrinkage.
4. Present format-specific leaderboards so batters are evaluated against their actual peers.

### Q4: What Is Virat Kohli's True Pressure Profile Across Families and Formats?
Kohli displays distinct observed rate characteristics across match situations:
- Under Early Collapse ($F_1$), his scoring rate is below average (123.2 IPL SR, 117.8 T20I SR), yielding negative RAE (-90.37 IPL, -38.56 T20I).
- In High-Target Chases ($\ge 180$, C32), his scoring rate increases to 168.8 (+75.43 raw RAE, 62.5% positive innings).
- In High Asking Rates ($\ge 10.0$ RRR, C37), his scoring rate is 185.1 (+66.21 raw RAE); at RRR $\ge 12.0$ (C38), it is 232.5 (+29.94 raw RAE).
- In Death Overs (overs 16–20), his scoring rate is 182.0 in IPL (+10.04 raw RAE) and 196.1 in T20Is (+22.21 raw RAE).

### Q5: Who Are the Consistent High-Pressure Performers Across Multiple Pressure Families?
Several batters maintain positive point estimates across multiple pressure conditions:
1. **Suryakumar Yadav:** Positive across Early Collapse (+44.76 IPL, +170.55 T20I), Target $\ge 180$ (+83.29 IPL, +113.95 T20I), and Death Overs (+45.72 IPL, +123.03 T20I).
2. **Shreyas Iyer:** Positive in Early Collapse (+22.54), Target $\ge 180$ (+110.56), and Death Overs (+87.32).
3. **Heinrich Klaasen:** Positive in Early Collapse (+67.57), Target $\ge 180$ (+40.24), and Death Overs (+69.71).
4. **Tim David:** Positive in T20I Early Collapse (+141.79), T20I Target $\ge 180$ (+88.82), and IPL Death Overs (+69.90).
5. **Naman Dhir:** Positive across Early Collapse (+9.55), Target $\ge 180$ (+25.39), and Death Overs (+21.73).

### Q6: Is a Combined Cross-Format Top 10 Methodologically Valid?
**No, not as a primary ranking.** Summing Shrunk RAE across IPL and T20I cannot serve as a definitive cross-format ranking because:
1. Disparate career lengths and exposures create severe structural volume bias.
2. The baseline scoring rate differs by 12.1 strike rate points between formats.
3. Linear summation of separately shrunk empirical Bayes estimates violates Bayesian exchangeability.
Any combined figures must be treated strictly as exploratory reference data.

### Q7: How Should Findings Be Presented to Judges Honestly?
1. Present **separate IPL and T20I Top 10 leaderboards** as primary results.
2. State exposure thresholds explicitly ($\ge 100$ balls primary; report sensitivity at 30, 200, 300).
3. Disclose that IPL Top 10 confidence intervals cross zero due to match-level clustering.
4. Present Virat Kohli's multi-family profile factually, showing both his early-collapse rate deficit and his high-target chase run production.
5. Disclaim WPA limitations honestly.

---

## 9. Win-Probability-Added (WPA) Assessment

- **Data Limitations:** Pre-delivery live win probability models and live betting odds are not available in the competition data pack. Condition C40 was therefore excluded. Generating synthetic win probabilities without market calibration would introduce unverified modeling assumptions.
- **What RAE Measures:** Contextual run production relative to empirical over-and-innings expectations.
- **What RAE Does Not Measure:** Wicket leverage, non-linear win probability step functions, or the strategic value of batting out overs in close matches.

---

## 10. Final Defensible Leaderboards

### IPL Pressure Leaderboard (Top 10 at $\ge 100$ Balls, Condition C15: $F_1 \cup F_4$)
*Note: Condition C15 incorporates playoff matches; $F_4$ is unavailable in T20I.*

| Rank | Player Name | Clean Balls | Observed Runs | Expected Runs | Raw RAE | Shrunk RAE | Observed SR | Expected SR | Positive Inns % | Median Inns RAE | 95% Cluster CI |
|:---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| **1** | **Rajat Patidar** | 601 | 1042 | 942.95 | +99.05 | **+75.77** | 173.4 | 156.9 | 54.8% | +0.42 | [-4.22, +231.96] |
| **2** | **Heinrich Klaasen** | 810 | 1358 | 1290.43 | +67.57 | **+49.33** | 167.7 | 159.3 | 63.9% | +1.53 | [-17.73, +155.44] |
| **3** | **Suryakumar Yadav** | 909 | 1462 | 1412.51 | +49.49 | **+33.14** | 160.8 | 155.4 | 48.8% | -0.93 | [-52.97, +170.27] |
| **4** | **Ishan Kishan** | 369 | 600 | 569.09 | +30.91 | **+14.37** | 162.6 | 154.2 | 31.4% | -1.52 | [-61.24, +120.37] |
| **5** | **Shreyas Iyer** | 678 | 1075 | 1052.69 | +22.31 | **+7.89** | 158.6 | 155.3 | 33.3% | -1.78 | [-107.79, +144.29] |
| **6** | **Sanju Samson** | 496 | 796 | 774.51 | +21.49 | **+6.89** | 160.5 | 156.2 | 40.0% | -1.46 | [-42.26, +100.19] |
| **7** | **Andre Russell** | 486 | 826 | 807.75 | +18.25 | **+4.08** | 170.0 | 166.2 | 47.2% | -0.69 | [-80.85, +112.53] |
| **8** | **Phil Salt** | 113 | 192 | 172.00 | +20.00 | **+3.84** | 169.9 | 152.2 | 55.6% | +0.47 | [-21.08, +60.14] |
| **9** | **Ashutosh Sharma** | 264 | 463 | 444.84 | +18.16 | **+3.59** | 175.4 | 168.5 | 50.0% | +0.58 | [-45.84, +83.44] |
| **10** | **Dinesh Karthik** | 358 | 619 | 602.41 | +16.59 | **+2.52** | 172.9 | 168.3 | 46.2% | -1.33 | [-56.37, +100.74] |

### T20 International Pressure Leaderboard (Top 10 at $\ge 100$ Balls, Condition C01: $F_1$ Early Collapse)
*Note: Operationalised identically to IPL Condition C01.*

| Rank | Player Name | Clean Balls | Observed Runs | Expected Runs | Raw RAE | Shrunk RAE | Observed SR | Expected SR | Positive Inns % | Median Inns RAE | 95% Cluster CI |
|:---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| **1** | **Suryakumar Yadav** | 869 | 1437 | 1266.45 | +170.55 | **+147.15** | 165.4 | 145.7 | 35.3% | -1.42 | [+22.66, +335.86] |
| **2** | **Tim David** | 445 | 795 | 653.21 | +141.79 | **+112.79** | 178.7 | 146.8 | 55.2% | +3.70 | [+22.66, +297.75] |
| **3** | **Harry Brook** | 458 | 758 | 667.99 | +90.01 | **+68.00** | 165.5 | 145.8 | 46.7% | -1.18 | [-12.16, +204.15] |
| **4** | **Abhishek Sharma** | 218 | 418 | 322.05 | +95.95 | **+64.22** | 191.7 | 147.7 | 30.8% | -1.30 | [-2.51, +209.16] |
| **5** | **David Miller** | 287 | 485 | 408.65 | +76.35 | **+52.13** | 169.0 | 142.4 | 47.1% | -0.30 | [-22.45, +188.62] |
| **6** | **Glenn Maxwell** | 348 | 573 | 505.61 | +67.39 | **+46.39** | 164.7 | 145.3 | 40.9% | -1.68 | [-39.09, +198.19] |
| **7** | **Rovman Powell** | 837 | 1288 | 1227.91 | +60.09 | **+44.42** | 153.9 | 146.7 | 45.8% | -0.91 | [-57.48, +190.72] |
| **8** | **Ishan Kishan** | 360 | 586 | 525.58 | +60.42 | **+40.75** | 162.8 | 146.0 | 28.6% | -1.50 | [-31.15, +185.15] |
| **9** | **Andre Russell** | 132 | 255 | 197.05 | +57.95 | **+30.46** | 193.2 | 149.3 | 55.6% | +5.42 | [-4.10, +119.62] |
| **10** | **Tom Banton** | 193 | 328 | 276.35 | +51.65 | **+29.39** | 169.9 | 143.2 | 50.0% | -0.02 | [+1.11, +110.43] |

### Final Combined Exploratory Top 10 Leaderboard (All Eligible Batters Across IPL & T20I)

> [!WARNING]
> **Methodological Classification: EXPLORATORY REFERENCE ONLY.**
> This ranking is generated by summing format-specific Empirical Bayes Shrunk RAE from the existing independent IPL (2022–2026) and T20I (2022–2026) analyses. Raw IPL and T20I Shrunk RAE figures are **not directly comparable** due to the +12.1 strike rate gap between format baselines, disparate prior distributions, and unequal career horizons. This combined table illustrates total estimated run contributions across formats under an exposure threshold of $\ge 100$ total pressure balls, but cannot replace the primary format-specific leaderboards.

| Rank | Player Name | IPL Contribution (Shrunk RAE) | T20I Contribution (Shrunk RAE) | Combined Score | Total Pressure Balls | IPL Balls | T20I Balls | Exposure Classification |
|:---:|:---|---:|---:|---:|---:|---:|---:|:---|
| **1** | **Suryakumar Yadav** | +33.14 | +147.15 | **+180.29** | 1778 | 909 | 869 | Dual-Format (IPL & T20I) |
| **2** | **Tim David** | -23.43 | +112.79 | **+89.36** | 836 | 391 | 445 | Dual-Format (IPL & T20I) |
| **3** | **Rajat Patidar** | +75.77 | +0.00 | **+75.77** | 601 | 601 | 0 | IPL Heavily Weighted |
| **4** | **Abhishek Sharma** | -8.94 | +64.22 | **+55.28** | 383 | 165 | 218 | Dual-Format (IPL & T20I) |
| **5** | **Ishan Kishan** | +14.37 | +40.75 | **+55.12** | 729 | 369 | 360 | Dual-Format (IPL & T20I) |
| **6** | **Glenn Maxwell** | +0.62 | +46.39 | **+47.01** | 636 | 288 | 348 | Dual-Format (IPL & T20I) |
| **7** | **Harry Brook** | -28.57 | +68.00 | **+39.43** | 548 | 90 | 458 | Dual-Format (IPL & T20I) |
| **8** | **Heinrich Klaasen** | +49.33 | -13.71 | **+35.62** | 985 | 810 | 175 | Dual-Format (IPL & T20I) |
| **9** | **Andre Russell** | +4.08 | +30.46 | **+34.54** | 618 | 486 | 132 | Dual-Format (IPL & T20I) |
| **10** | **Tom Banton** | +0.00 | +29.39 | **+29.39** | 193 | 0 | 193 | T20I Heavily Weighted |

*(Note: If a dual-format balance threshold of $\ge 30$ balls in each format is applied, single-format batters Rajat Patidar [#3] and Tom Banton [#10] are excluded, elevating **Shreyas Iyer** to #9 [IPL +7.89, T20I +12.56, Combined +20.45 across 1,096 balls] and **Josh Inglis** to #10 [IPL -22.15, T20I +27.01, Combined +4.86 across 444 balls]).*
---

## 11. Verification & Integrity Checklist

All eight frozen baseline files have been verified against their SHA-256 hashes with zero modifications:

- `outputs/final/final_batter_leaderboard.csv`: `VERIFIED` (`d0e73b49824ae994...`)
- `outputs/final/final_bowler_diagnostics.csv`: `VERIFIED` (`3e5607fa8a2c16b4...`)
- `outputs/final/final_validation_report.json`: `VERIFIED` (`803e661f3ccc641f...`)
- `outputs/statistical/batter_pressure_estimates.csv`: `VERIFIED` (`307969959aa89094...`)
- `outputs/statistical/bowler_pressure_diagnostics.csv`: `VERIFIED` (`ac720eaf2c023a9e...`)
- `outputs/statistical/bootstrap_uncertainty.csv`: `VERIFIED` (`befdb7e652fd49fb...`)
- `outputs/statistical/baseline_model_report.json`: `VERIFIED` (`9fcd247fad124bbf...`)
- `outputs/statistical/stage4_validation_report.json`: `VERIFIED` (`b2e5dd61b667e3ef...`)

---
*Report audited and finalized.*
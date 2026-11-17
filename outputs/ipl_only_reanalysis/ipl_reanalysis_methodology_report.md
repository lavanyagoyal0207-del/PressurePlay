# Fresh, Independent IPL-Only Reanalysis: Batter Performance Under Pressure
## Evaluation of the Complete IPL Delivery Universe (2022–2026) & Virat Kohli Case Study
### SupeRR Selector Season 2 — Specialized Competition Investigation Report

---

## Executive Summary: Answering the Core Strategic Question

### Core Question
> **Where does Virat Kohli rank among all eligible IPL batters under pressure, and what does the empirical evidence say about his performance across different pressure situations?**

### Definitive Empirical Answers

1. **Overall Rank in the Complete IPL Batter Population:**
   - Among all **326 batters** who faced pressure deliveries in the IPL (2022–2026), Virat Kohli ranks **#311 overall** with **-91.95 Shrunk Runs Above Expected (RAE)**.
   - Among the **175 qualified batters** with sufficient sample size ($n_p \ge 30$ clean pressure balls), Virat Kohli ranks **#160** (#16 out of 175 from the bottom, placed in the bottom 8.6 percentile).
   - Among the **49 high-exposure batters** ($n_p \ge 300$ clean pressure balls), Virat Kohli ranks **#35 of 49**.

2. **Scoring Performance Across Situational Environments:**
   A granular decomposition reveals that Kohli's sub-baseline scoring is **not** uniform across all pressure types:
   - **Non-Pressure Baseline Deliveries (1,660 clean balls):** Kohli scored **2,528 runs** against **2,524.0 expected**, yielding **+4.0 Raw RAE** at a strike rate of **152.29** (expected: 152.05; rate difference: **+0.0024 runs/ball**). Under standard non-collapse league conditions, he performs virtually **dead-even with the IPL baseline**.
   - **Playoff Matches Without Early Collapse ($F_4$-Only, 111 clean balls):** Kohli scored **163 runs** against **168.7 expected**, yielding **-5.7 Raw RAE** at a strike rate of **146.85** (expected: 151.98; rate difference: **-0.0512 runs/ball**). In high-stakes knockout games where his team avoided an early top-order collapse, he performs near baseline expectation.
   - **Early Top-Order Collapse ($F_1$ Primary, 293 clean balls):** When two wickets fell at or before over 8 ($W_2 \le 8$), Kohli scored **361 runs** against **451.4 expected**, generating **-90.4 Raw RAE** at a strike rate of **123.21** (expected: 154.07; rate difference: **-0.3084 runs/ball**). This single situation accounts for **94.1% of his entire career negative pressure deficit** (-90.4 of -96.1 runs).
   - **Regular-Season Collapse ($F_1$-Only, 237 clean balls):** In league matches following an early collapse, his strike rate fell to **120.68** against 153.88 expected (**-78.7 Raw RAE**, rate difference: **-0.3323 runs/ball**).

3. **Innings-Level Reliability & Distribution:**
   Across **30 qualifying pressure innings** in the IPL:
   - **Positive Innings Hit Rate:** Kohli achieved $\text{RAE}_{\text{inns}} > 0$ in **4 of 30 innings (13.3%)**, ranking **#132 of 175** qualified batters.
   - **Median Innings RAE:** **-1.73 runs** (mean: -3.20 runs; standard deviation: 6.89 runs).
   - **Late-Career Resurgence:** In the 2026 IPL playoffs, Kohli delivered two outstanding high-strike-rate performances: the Qualifier (25 balls, 43 runs, +3.79 RAE, SR 172.0) and the Final (41 balls, 75 runs, +9.79 RAE, SR 182.9), totaling +13.58 RAE across 66 balls.

4. **Wider Context Among Marquee Batters:**
   Kohli's ranking is part of a systemic structural pattern observed across Indian cricket's traditional anchor batters. When early top-order collapses occur, anchor batters absorb high ball volumes (300 to 700+ deliveries) at cautious scoring rates (110–135 SR) to prevent total collapses, accumulating large negative run residuals against an unconditioned baseline that expects ~150–155:
   - **Rajat Patidar:** #1 (+75.79 Shrunk RAE, 54.8% positive innings)
   - **Heinrich Klaasen:** #2 (+49.33 Shrunk RAE, 63.9% positive innings)
   - **Suryakumar Yadav:** #3 (+33.09 Shrunk RAE, 48.8% positive innings)
   - **Sanju Samson:** #8 (+6.89 Shrunk RAE, 40.0% positive innings)
   - **Shubman Gill:** #38 (-8.72 Shrunk RAE, 28.0% positive innings)
   - **Rohit Sharma:** #131 (-45.41 Shrunk RAE, 10.5% positive innings)
   - **Rishabh Pant:** #143 (-61.02 Shrunk RAE, 31.0% positive innings)
   - **Mahendra Singh Dhoni:** #159 (-90.37 Shrunk RAE, 40.0% positive innings)
   - **Virat Kohli:** #160 (-91.95 Shrunk RAE, 13.3% positive innings)
   - **Lokesh Rahul:** #171 (-135.87 Shrunk RAE, 9.7% positive innings)
   - **Ravindra Jadeja:** #174 (-178.24 Shrunk RAE, 16.3% positive innings)
   - **Hardik Pandya:** #175 (-183.49 Shrunk RAE, 27.3% positive innings)

---

## 1. Dataset Scope & Competition Architecture

Cross-referencing `competitions.csv` with `matches.csv` confirms the exact historical scope of the IPL-only delivery universe:

| Attribute | Specification / Value | Source Reference |
| :--- | :--- | :--- |
| **Tournament Name** | Indian Premier League (IPL) | `competitions.csv` (`comp_name`) |
| **Competition IDs** | `1358` (2022), `1715` (2023), `2193` (2024), `2725` (2025), `3298` (2026) | `competitions.csv` |
| **Seasons Covered** | **5 Full Seasons:** 2022, 2023, 2024, 2025, 2026 | `matches.csv` (`season`) |
| **Total Matches** | **371 Matches** (2022: 74, 2023: 74, 2024: 74, 2025: 75, 2026: 74) | `matches.csv` |
| **Match Date Range** | **March 26, 2022 to May 31, 2026** | `matches.csv` (`match_date`) |
| **Match Stages** | League: 351, Qualifiers: 10, Eliminators: 5, Finals: 5 | `matches.csv` (`stage`) |
| **Playoff Matches ($F_4$)** | Exactly **20 matches** (`knock_out == 1`) | `matches.csv` (`knock_out`) |
| **Total Deliveries** | **87,687 raw delivery attempts** | `delivery_pressure_eligibility.csv` |
| **Clean Deliveries** | **82,458 valid clean balls faced** | `extras_type in ('', 'None')` |
| **Non-Clean Deliveries** | **5,229 extras/illegal balls** (excluded from clean universe) | Wides, no-balls, legbyes, byes, penalties |

---

## 2. Recalculated Model 2 Expectation Baseline (IPL-Only)

### Methodology & Training Pool
In accordance with official pipeline standards, the **IPL-only Model 2 baseline** is fitted exclusively on **clean, non-pressure deliveries** occurring within IPL matches:
- **Training Denominator:** Exactly **42,074 non-pressure clean deliveries** (42,063 in standard overs 1–20, plus 11 non-pressure clean deliveries in Super Overs).
- **Global Non-Pressure Scoring Rate:** **1.5557 runs/ball** (equivalent to an IPL non-pressure Strike Rate of **155.57**).
- **Cell Structure:** Interaction of delivery over index (`overid` 1..20) and match innings (1..4), producing **42 unconstrained empirical lookup cells**.

### Comparison: Why IPL Baseline Raises Expected Runs
In the original composite model, the baseline pooled IPL matches with Men's T20 Internationals (T20I) and emerging Asian tournaments, producing a lower overall non-pressure scoring rate of **1.4398 runs/ball** (Strike Rate: 143.98).
In the IPL alone, aggressive batting approaches and batting-friendly surfaces elevate the true baseline to **1.5557 runs/ball**. Consequently:
- For every 100 clean balls faced in the IPL, an IPL-only model expects **155.6 runs**, compared to **144.0 runs** in the composite baseline.
- Because the bar in the IPL is higher, batters with sub-baseline scoring rates in the IPL see their expected runs increase and their raw RAE deficits deepen under an IPL-only baseline.

A complete cell-by-cell export is saved to [ipl_baseline_model_2.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/ipl_baseline_model_2.csv).

---

## 3. Empirical Bayes Shrinkage Formulation (IPL-Only Population)

### DerSimonian–Laird (DL) Parameter Estimation
To regularize small-sample variance without distorting high-exposure production, shrinkage parameters were estimated directly from the IPL-only player population:

1. **Pooled Residual Delivery Variance ($\sigma^2_{\text{IPL}}$):**
   $$\sigma^2_{\text{IPL}} = \operatorname{Var}(Y_d - E_d) = \mathbf{3.0499}$$
2. **Individual Sampling Variance ($v_{p, \text{IPL}}$):**
   $$v_{p, \text{IPL}} = \frac{\sigma^2_{\text{IPL}}}{n_{p, \text{IPL}}} = \frac{3.0499}{n_{p, \text{IPL}}}$$
3. **Prior Estimation Cohort:**
   Fitted across all $k = 251$ IPL batters with clean exposure $n_p \ge 10$ using inverse-variance weights $w_p = 1 / v_{p, \text{IPL}}$.
4. **Fitted Prior Hyperparameters:**
   - **Population Prior Mean ($\mu_{\text{IPL}}$):** $\mathbf{-0.1746 \text{ runs/ball}}$
   - **Between-Player Heterogeneity Variance ($\tau^2_{\text{IPL}}$):** $\mathbf{0.039385}$
   - **Between-Player Standard Deviation ($\tau_{\text{IPL}}$):** $\mathbf{0.1985 \text{ runs/ball}}$
5. **Shrinkage Weight & Regularized Estimates:**
   $$B_{p, \text{IPL}} = \frac{v_{p, \text{IPL}}}{\tau^2_{\text{IPL}} + v_{p, \text{IPL}}}$$
   $$\theta_{p, \text{IPL}}^* = (1 - B_{p, \text{IPL}}) \theta_{p, \text{IPL}} + B_{p, \text{IPL}} \mu_{\text{IPL}}$$
   $$\text{Shrunk RAE}_{p, \text{IPL}} = n_{p, \text{IPL}} \cdot \theta_{p, \text{IPL}}^*$$

For Virat Kohli ($n_p = 404$ clean balls):
$$v_{\text{Kohli}} = \frac{3.0499}{404} = 0.007549$$
$$B_{\text{Kohli}} = \frac{0.007549}{0.039385 + 0.007549} = \mathbf{0.1608}$$
Because of his substantial 404-ball exposure, shrinkage is modest ($B_p \approx 0.161$), retaining **83.9% of his raw rate differential** ($\theta_p = -0.2378$ shrinks to $\theta_p^* = -0.2276$ runs/ball).

---

## 4. Complete IPL Batter Leaderboard Findings

### Population Overview
Across the 371 IPL matches:
- **326 unique batters** faced at least 1 clean pressure delivery.
- **175 qualified batters** met the standard sample-size threshold ($n_p \ge 30$ clean balls).
- **103 moderate-exposure batters** faced $n_p \ge 100$ clean balls.
- **49 high-exposure batters** faced $n_p \ge 300$ clean balls.

### Top 20 Qualified IPL Batters vs. Marquee Comparisons

| Rank | Player Name | Player ID | Exposure Tier | Clean Balls ($n_p$) | Actual Runs | Expected Runs | Raw RAE | Shrunk RAE | Shrunk Rate ($\theta_p^*$) | Positive Inns % | Median Inns RAE |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Rajat Patidar** | 5039 | High ($\ge 300$) | 601.0 | 1,042 | 942.9 | +99.06 | **+75.79** | +0.1261 | 54.8% | +1.12 |
| **2** | **Heinrich Klaasen** | 4260 | High ($\ge 300$) | 810.0 | 1,358 | 1,290.4 | +67.57 | **+49.33** | +0.0609 | 63.9% | +1.58 |
| **3** | **Suryakumar Yadav** | 1699 | High ($\ge 300$) | 909.0 | 1,462 | 1,412.5 | +49.49 | **+33.09** | +0.0364 | 48.8% | -0.21 |
| **4** | **Vaibhav Sooryavanshi** | 50284 | Low (30–99) | 84.0 | 189 | 130.9 | +58.12 | **+23.20** | +0.2762 | 33.3% | -1.74 |
| **5** | **Ishan Kishan** | 4710 | High ($\ge 300$) | 369.0 | 600 | 569.1 | +30.91 | **+14.39** | +0.0390 | 31.4% | -1.52 |
| **6** | **Jake McGurk** | 50257 | Low (30–99) | 40.0 | 98 | 59.8 | +38.24 | **+8.42** | +0.2105 | 50.0 | -0.16 |
| **7** | **Shreyas Iyer** | 4713 | High ($\ge 300$) | 678.0 | 1,075 | 1,052.7 | +22.32 | **+7.86** | +0.0116 | 33.3% | -1.41 |
| **8** | **Sanju Samson** | 2258 | High ($\ge 300$) | 496.0 | 796 | 774.5 | +21.49 | **+6.89** | +0.0139 | 40.0% | -1.25 |
| **9** | **Priyansh Arya** | 50139 | Low (30–99) | 69.0 | 132 | 105.9 | +26.14 | **+5.95** | +0.0862 | 50.0% | +0.05 |
| **10** | **Finn Allen** | 4410 | Low (30–99) | 37.0 | 83 | 56.0 | +27.05 | **+4.37** | +0.1182 | 100.0% | +13.52 |
| **11** | **Andre Russell** | 109 | High ($\ge 300$) | 486.0 | 826 | 807.8 | +18.25 | **+4.08** | +0.0084 | 47.2% | -0.22 |
| **12** | **Phil Salt** | 4976 | Moderate (100–299) | 113.0 | 192 | 172.0 | +20.00 | **+3.84** | +0.0340 | 55.6% | +0.45 |
| **13** | **Ashutosh Sharma** | 50064 | Moderate (100–299) | 264.0 | 463 | 444.8 | +18.16 | **+3.59** | +0.0136 | 50.0% | +0.23 |
| **14** | **Dinesh Karthik** | 113 | High ($\ge 300$) | 358.0 | 619 | 602.4 | +16.59 | **+2.51** | +0.0070 | 46.2% | -0.32 |
| **15** | **Riyan Parag** | 6309 | High ($\ge 300$) | 659.0 | 1,060 | 1,044.1 | +15.92 | **+2.17** | +0.0033 | 40.0% | -1.35 |
| **16** | **Glenn Maxwell** | 102 | Moderate (100–299) | 288.0 | 463 | 448.7 | +14.31 | **+0.63** | +0.0022 | 33.3% | -1.54 |
| **17** | **Mahipal Lomror** | 4725 | Moderate (100–299) | 113.0 | 196 | 182.3 | +13.66 | **+0.08** | +0.0007 | 43.8% | -0.85 |
| **18** | **Marcus Stoinis** | 112 | High ($\ge 300$) | 581.0 | 949 | 936.8 | +12.23 | **-1.16** | -0.0020 | 40.5% | -1.24 |
| **19** | **Vipraj Nigam** | 50280 | Low (30–99) | 72.0 | 131 | 120.3 | +10.75 | **-1.34** | -0.0186 | 50.0% | +0.12 |
| **20** | **Cooper Connolly** | 50239 | Low (30–99) | 81.0 | 140 | 129.4 | +10.65 | **-1.47** | -0.0181 | 50.0% | -0.15 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| **38** | **Shubman Gill** | 6288 | High ($\ge 300$) | 459.0 | 716 | 712.6 | +3.37 | **-8.72** | -0.0190 | 28.0% | -1.41 |
| **131** | **Rohit Sharma** | 126 | Moderate (100–299) | 182.0 | 234 | 285.2 | -51.20 | **-45.41** | -0.2495 | 10.5% | -1.72 |
| **143** | **Rishabh Pant** | 4703 | High ($\ge 300$) | 487.0 | 699 | 756.2 | -57.17 | **-61.02** | -0.1253 | 31.0% | -1.52 |
| **159** | **MS Dhoni** | 8 | High ($\ge 300$) | 377.0 | 563 | 658.4 | -95.40 | **-90.37** | -0.2397 | 40.0% | -1.45 |
| **160** | **Virat Kohli** | 47 | High ($\ge 300$) | 404.0 | 524 | 620.1 | -96.06 | **-91.95** | -0.2276 | 13.3% | -1.73 |
| **171** | **Lokesh Rahul** | 953 | High ($\ge 300$) | 545.0 | 717 | 858.6 | -141.64 | **-135.87** | -0.2493 | 9.7% | -1.78 |
| **174** | **Ravindra Jadeja** | 152 | High ($\ge 300$) | 685.0 | 953 | 1,137.9 | -184.89 | **-178.24** | -0.2602 | 16.3% | -1.72 |
| **175** | **Hardik Pandya** | 3330 | High ($\ge 300$) | 709.0 | 952 | 1,142.0 | -189.98 | **-183.49** | -0.2588 | 27.3% | -1.45 |

The complete 326-batter leaderboard is saved to [ipl_batter_leaderboard.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/ipl_batter_leaderboard.csv), and the comparison cohort to [ipl_top20_comparison.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/ipl_top20_comparison.csv).

---

## 5. Virat Kohli: Forensic Delivery & Situational Analysis

### Core Profile Summary (Player ID: 47)
- **Total IPL Career Deliveries Analyzed (2022–2026):** **2,167 balls** faced.
- **Clean Deliveries Faced:** **2,064 balls** (103 non-clean extras excluded).
- **Clean Pressure Deliveries ($F_1 \cup F_4$):** **404 balls** across 30 distinct matches and 30 innings (19.6% of his clean IPL delivery volume).
- **Observed Clean Pressure Runs:** **524 runs** (Strike Rate: **129.70**).
- **Expected Clean Pressure Runs (IPL Baseline):** **620.06 runs** (Expected Strike Rate: **153.48**).
- **Raw Runs Above Expected (Raw RAE):** **-96.06 runs** (Rate Difference: **-0.2378 runs/ball**).
- **Shrinkage Factor ($B_p$):** **0.1608** (retaining 83.9% of his negative deviation).
- **Shrunk Runs Above Expected (Shrunk RAE):** **-91.95 runs** (Shrunk Rate Difference: **-0.2276 runs/ball**).

### Situational Environment Breakdown

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              VIRAT KOHLI SITUATIONAL PERFORMANCE IN THE IPL                            │
├───────────────────────────────────────┬────────┬──────┬─────────┬─────────┬────────┬────────┬──────────┤
│ Situational Environment               │ Clean  │ Actual Expected│ Raw RAE │ Strike │ Exp SR │ Rate Diff│
│                                       │ Balls  │ Runs │ Runs    │ (Runs)  │ Rate   │        │(runs/ball)
├───────────────────────────────────────┼────────┼──────┼─────────┼─────────┼────────┼────────┼──────────┤
│ Non-Pressure Baseline Deliveries      │ 1,660  │ 2,528│ 2,524.0 │  +4.0   │ 152.3  │ 152.1  │ +0.0024  │
│ Playoff Only (F4, No Early Collapse)  │   111  │   163│   168.7 │  -5.7   │ 146.8  │ 152.0  │ -0.0512  │
│ Early Collapse Playoff Overlap (F1∩F4)│    56  │    75│    86.6 │ -11.6   │ 133.9  │ 154.7  │ -0.2076  │
│ Early Collapse League Only (F1 Only)  │   237  │   286│   364.7 │ -78.7   │ 120.7  │ 153.9  │ -0.3323  │
├───────────────────────────────────────┼────────┼──────┼─────────┼─────────┼────────┼────────┼──────────┤
│ All Early Collapse Deliveries (F1)    │   293  │   361│   451.4 │ -90.4   │ 123.2  │ 154.1  │ -0.3084  │
│ All Playoff Deliveries (F4 Knockouts) │   167  │   238│   255.3 │ -17.3   │ 142.5  │ 152.9  │ -0.1037  │
├───────────────────────────────────────┼────────┼──────┼─────────┼─────────┼────────┼────────┼──────────┤
│ Combined Pressure Union (F1 ∪ F4)     │   404  │   524│   620.1 │ -96.1   │ 129.7  │ 153.5  │ -0.2378  │
└───────────────────────────────────────┴────────┴──────┴─────────┴─────────┴────────┴────────┴──────────┘
```

The delivery-level log containing all 404 balls is saved to [virat_kohli_delivery_log.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/virat_kohli_delivery_log.csv), and the 30-innings summary to [virat_kohli_innings_summary.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/virat_kohli_innings_summary.csv).

---

## 6. Sensitivity Analysis: Methodological Dimensions

### 1. Retrospective vs. Prospective $F_1$ Classification
The official frozen pipeline applies a retrospective definition: any delivery occurring at or after the second wicket index ($\text{delivery\_idx} \ge W_2\text{\_idx}$) is tagged as $F_1$.
A detailed audit of Kohli's delivery logs reveals:
- In **9 matches**, Virat Kohli was himself the second batter dismissed ($W_2$).
- On those 9 deliveries, he was dismissed for **0 runs**, accumulating **-13.88 Raw RAE** on the single ball that established $W_2$.
- Under a **strictly prospective $F_1$ formulation** (where pressure begins strictly on deliveries *after* $W_2$ has already fallen):
  - Kohli's $F_1$ balls drop from 293 to **284 balls**.
  - His actual runs remain **361 runs**, while expected runs drop to **437.6 runs**.
  - His $F_1$ Raw RAE improves from -90.4 runs to **-76.6 runs** (Strike Rate: **127.1** vs 154.1 expected).
  - His combined pressure Raw RAE improves from -96.06 runs to **-82.26 runs**.
  - Even under this prospective adjustment, his scoring residual remains negative (-82.26 runs), demonstrating that the sub-baseline rating is not an artifact of the concurrent wicket delivery.

### 2. Sensitivity Across Minimum Exposure Thresholds
Because cumulative Shrunk RAE is volume-scaled, evaluating Kohli against progressively tighter exposure tiers tests whether his rank changes among peers with comparable match time:

| Exposure Cutoff | Total Qualifying Batters | Kohli Rank (Shrunk RAE) | Percentile Placement | Kohli Rank (Shrunk Rate) | Kohli Rank (Positive Inns %) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **All Batters ($n_p \ge 1$)** | 326 | **#311** | Bottom 4.6% | #171 | #158 |
| **$n_p \ge 10$ Clean Balls** | 251 | **#236** | Bottom 6.0% | #127 | #150 |
| **$n_p \ge 30$ Clean Balls (Standard)** | 175 | **#160** | Bottom 8.6% | #101 | #132 |
| **$n_p \ge 50$ Clean Balls** | 149 | **#134** | Bottom 10.1% | #92 | #116 |
| **$n_p \ge 100$ Clean Balls** | 103 | **#88** | Bottom 14.6% | #72 | #88 |
| **$n_p \ge 200$ Clean Balls** | 67 | **#53** | Bottom 20.9% | #50 | #61 |
| **$n_p \ge 300$ Clean Balls (High Exposure)** | 49 | **#35** | Bottom 28.6% | #39 | #48 |

The complete sensitivity table is saved to [ipl_sensitivity_analysis.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/ipl_sensitivity_analysis.csv).

---

## 7. Strategic Synthesis & Decision-Ready Franchise Takeaways

### 1. Is Virat Kohli's Standing Driven by Format Inequity?
**No.** Isolating IPL matches exclusively does not elevate Virat Kohli's standing into positive territory. In fact, because the IPL baseline expectation (1.5557 runs/ball) is higher than the multi-competition composite baseline (1.4398 runs/ball), his expected run tally rises from 595.9 to 620.1 runs, deepening his raw deficit from -71.87 to **-96.06 runs**.

### 2. Is He a Sub-Baseline Batter Under All Pressure?
**No.** The evidence demonstrates distinct situational behaviors:
1. In standard IPL conditions without early crisis, he scores at **152.3 runs per 100 balls**, matching the league baseline (+4.0 RAE over 1,660 balls).
2. In playoff fixtures where the top-order remains stable, he scores at **146.8 runs per 100 balls**, near baseline expectation (-5.7 RAE over 111 balls).
3. In early collapses ($W_2 \le 8$), his scoring rate drops to **123.2 runs per 100 balls**, creating a -90.4 run deficit across 293 balls.

### 3. Tactical Anchor Trade-Off vs. Scoring Residual Boundary
The SupeRR Selector scoring residual framework evaluates players strictly on **runs scored above an over-by-over empirical expectation**. It does **not** reward wicket preservation or calculate win probability added (WPA).
In early crisis situations, Kohli adopts a classic anchor strategy: he absorbs deliveries to halt further wicket loss, allowing batting partners or subsequent batters to construct an innings. While this strategy may prevent catastrophic batting collapses from a team perspective, it produces a lower scoring rate than the unconditioned league baseline, resulting in heavy negative cumulative scoring residuals.

---

### Artifact Index
- **Model 2 Empirical Baseline Table:** [ipl_baseline_model_2.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/ipl_baseline_model_2.csv)
- **Complete 326-Batter Leaderboard:** [ipl_batter_leaderboard.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/ipl_batter_leaderboard.csv)
- **Virat Kohli 404-Delivery Log:** [virat_kohli_delivery_log.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/virat_kohli_delivery_log.csv)
- **Virat Kohli 30-Innings Summary:** [virat_kohli_innings_summary.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/virat_kohli_innings_summary.csv)
- **Top 20 & Marquee Batters Comparison:** [ipl_top20_comparison.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/ipl_top20_comparison.csv)
- **Sensitivity Matrix Across Thresholds:** [ipl_sensitivity_analysis.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/ipl_sensitivity_analysis.csv)
- **Reproducible Python Pipeline Script:** [run_ipl_reanalysis.py](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/run_ipl_reanalysis.py)
- **Machine-Readable Audit Record:** [ipl_reanalysis_audit.json](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/ipl_only_reanalysis/ipl_reanalysis_audit.json)

---
*SupeRR Selector Season 2 — Independent IPL-Only Specialized Investigation Report.*

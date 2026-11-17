# Rajasthan Royals SupeRR Selector Season 2
## Executive Evaluation Report: Statistical Analysis of T20 Pressure Performance
### Strategic Analysis, Baseline-Adjusted Batter Estimates, Bowler Diagnostics & Performance Shortlists

---

## 1. Executive Summary

This report delivers the decision-ready statistical evaluation for the **Rajasthan Royals SupeRR Selector Season 2** research initiative. Analyzing 200,999 historical delivery records across major domestic leagues and international fixtures, this study evaluates player performance under clearly defined, high-leverage match conditions:
1. **Early-Wicket Collapse ($F_1$ Primary):** Second wicket falling at or before over 8 ($W_2 \le 8$) through the end of the innings.
2. **Playoff / Knockout Matches ($F_4$):** Tournament playoff fixtures (Qualifiers, Eliminators, Semi-Finals, Finals).
3. **Weighted Composite ($F_1 \cup F_4$):** Normalized per-delivery allocation ($w_1 = 1.0$ on $F_1$-only, $w_4 = 1.0$ on $F_4$-only, and $w_1 = 2/3, w_4 = 1/3$ on overlapping deliveries).

### Analytical Architecture Summary
- **Baseline Expectation (Model 2):** Every delivery outcome is evaluated against an empirical expectation conditioned on delivery over index (`overid` 1–20) and match innings (1–4), forming 42 discrete empirical cells (40 standard-innings cells and 2 Super Over cells). The baseline was fitted on **91,649 total non-pressure clean training deliveries**: **91,623 standard-over non-pressure clean deliveries** (IPL: 42,063; T20I: 46,798; Other T20: 2,762) and **26 Super Over non-pressure clean deliveries** (IPL: 11; T20I: 8; Other T20: 7). Predictive performance was evaluated using 5-fold match-grouped cross-validation (out-of-fold MAE: 1.4131 runs; RMSE: 1.7930 runs; calibration slope: 0.9439; intercept: 0.0832). Super Over support is sparse (15 clean training deliveries in innings 3 and 11 in innings 4), making those estimates substantially less reliable than standard-innings estimates.
- **DerSimonian–Laird (DL) Empirical Bayes Shrinkage:** To prevent small-sample distortion, player excess run rates are shrunk toward the population pressure prior ($\mu = -0.1872$ runs/ball for Composite; $\mu = -0.1942$ runs/ball for F1 Primary), with shrinkage intensity governed by the independent-delivery sampling variance ($v_p = \sigma^2 / n_p$, where $\sigma^2$ is the delivery residual variance and $n_p$ is clean balls faced). This model-based variance assumes conditionally independent deliveries and does not adjust for match clustering.
- **5,000-Replicate Match-Cluster Bootstrap:** Evaluates sampling uncertainty by resampling intact matches (745 clusters) with replacement. These confidence intervals are **strictly conditional** on the fixed Model 2 baseline expectations and fixed prior hyperparameters, capturing first-order sampling variation under match clustering. They do not alter or correct the independent-delivery variance assumption used in the point shrinkage formula.

### Key Strategic Findings

1. **Top Observed Batter in Sample:**
   **Suryakumar Yadav** accumulated **+209.09 Cumulative Shrunk Runs Above Expected (RAE)** across 1,778.0 clean balls faced in the composite cohort (+0.1176 shrunk runs/ball above baseline). His conditional 95% bootstrap confidence interval (`[+32.22, +397.91]`) strictly excludes zero. In $F_1$ Primary, he recorded **+202.41 Shrunk RAE** across 1,757.0 clean balls (95% CI `[+29.54, +401.50]`).

2. **Positive Composite Baseline Divergence (Nominal Significance):**
   **Rajat Patidar** is the only other qualified batter in the dataset whose conditional 95% bootstrap confidence interval strictly excludes zero in the composite cohort (**+107.16 Shrunk RAE** over 601.0 clean balls; +0.1783 shrunk runs/ball; 95% CI `[+1.07, +235.03]`). This provides nominal, exploratory evidence of positive pressure scoring in the composite sample, though the interval is unadjusted for multiple comparisons across the 456 eligible batters. In $F_1$ Primary, his 95% confidence interval crosses zero (**+46.74 Shrunk RAE** over 476.0 clean balls; 95% CI `[-21.79, +131.69]`).

3. **High-Upside Candidates with Positive Point Estimates:**
   **Tim David** (+110.94 Shrunk RAE), **Heinrich Klaasen** (+79.29 Shrunk RAE), **Andre Russell** (+78.92 Shrunk RAE), **Ishan Kishan** (+76.98 Shrunk RAE), **Abhishek Sharma** (+69.59 Shrunk RAE), and **Glenn Maxwell** (+60.55 Shrunk RAE) demonstrate positive point estimates above Model 2 baseline expectations. Because match-clustering variance is substantial, their 95% confidence intervals cross zero (classified as `PROMISING_UNCERTAIN`), providing exploratory indications rather than confirmed divergence.

4. **Young Developmental Candidate:**
   **Vaibhav Sooryavanshi** demonstrated high raw run generation in a limited sample (189.0 observed runs in 89.0 clean balls vs. 133.8 expected, +55.22 Raw RAE). Empirical Bayes shrinkage adjusts this estimate to **+24.15 Shrunk RAE** (+0.2713 runs/ball; 95% CI `[-12.44, +131.62]`). Performance was concentrated in knockout fixtures (75.0 balls in $F_4$, +42.99 Shrunk RAE), while in $F_1$ Primary he recorded -3.54 Shrunk RAE across 58.0 clean balls.

5. **Observed Negative Baseline Divergences:**
   **Virat Kohli** and **Ravindra Jadeja** exhibit negative baseline divergence under early-collapse pressure, with individual unadjusted 95% bootstrap confidence intervals strictly below zero:
   - *Virat Kohli:* In Composite ($F_1 \cup F_4$), 522.0 clean balls, 663.0 observed runs vs. 779.9 expected (**-114.74 Shrunk RAE**; 95% CI `[-193.66, -36.50]`). In $F_1$ Primary, 411.0 clean balls, 500.0 observed runs vs. 618.0 expected (**-112.49 Shrunk RAE**; 95% CI `[-183.36, -45.82]`).
   - *Ravindra Jadeja:* In Composite, 805.0 clean balls, 1,107.0 observed runs vs. 1,285.9 expected (**-176.70 Shrunk RAE**; 95% CI `[-267.34, -94.55]`). In $F_1$ Primary, 781.0 clean balls, 1,073.0 observed runs vs. 1,243.8 expected (**-169.24 Shrunk RAE**; 95% CI `[-265.11, -88.24]`).

6. **Bowler Pressure Diagnostics:**
   - *Containment Benchmark:* **Sunil Narine** conceded 0.9757 clean runs per clean ball (763 clean runs across 782 clean balls bowled; 798 legal balls bowled under pressure, saving 391.72 clean runs vs. Model 2 baseline), taking 36 credited wickets (22.17 legal balls/wkt).
   - *Wicket & Containment Dual Threat:* **Jasprit Bumrah** conceded 1.1014 clean runs per clean ball across 740 clean balls bowled (815 clean runs; 753 legal balls bowled in composite, saving 364.22 clean runs vs. Model 2 baseline) with 51 credited wickets (14.76 legal balls/wkt). In $F_1$ Primary, he recorded 1.0817 clean containment across 722 clean balls (735 legal balls) with 51 wickets (14.41 legal balls/wkt).
   - *Strike Wicket Leaders:* **Rashid Khan** (108 wickets in 1,781 legal balls, 1,747 clean balls; 16.49 legal balls/wkt; 1.2124 clean containment) and **Arshdeep Singh** (101 wickets in 1,198 legal balls, 1,176 clean balls; 11.86 legal balls/wkt; 1.3954 clean containment).

---

## 2. Interpretation of Leaderboard Metrics

> [!IMPORTANT]
> **Scope Warning:** **This is a 2022–2026 pressure-performance ranking, not an all-time IPL player ranking or a current-form ranking.**

To prevent strategic misinterpretations, decision-makers must distinguish between rate, volume, and conventional metrics:

1. **Cumulative Shrunk RAE ($\text{Shrunk RAE}_p = n_p \cdot \theta_p^*$):**
   An aggregate volume metric expressed in total runs. It measures the net runs accumulated above baseline across the historical sample. **It is not a standardized talent rating, per-delivery efficiency index, or runs-above-replacement metric.** Because it scales with clean balls faced ($n_p$), a batter with 1,500 balls at +0.12 runs/ball accumulates higher cumulative RAE (+180 runs) than a batter with 300 balls at +0.20 runs/ball (+60 runs). **The cumulative leaderboard must not be characterized as a reliability or consistency ranking.**
2. **Shrunk Rate Differential ($\theta_p^*$):**
   A rate metric expressed in runs per clean ball above baseline. It isolates individual scoring intensity per ball faced after shrinking small-sample variance toward the population prior ($\mu = -0.1872$).
3. **Positive Qualifying Pressure-Innings Frequency ($\% \text{Pos}$):**
   The percentage of qualifying pressure match-innings (where the batter faced $\ge 1$ clean pressure delivery) in which innings RAE was strictly positive ($\text{RAE}_{\text{inns}} > 0$). This evaluates situational scoring success frequency; it is strictly distinct from the proportion of all career matches in which a player performed well.
4. **Median Qualifying Pressure-Innings RAE:**
   The 50th percentile of match-innings RAE across qualifying pressure innings. It reflects typical per-match pressure contribution, unskewed by extreme single-match outlier explosions.
5. **Innings-Level Volatility ($\operatorname{SD}_{\text{inns}}$):**
   Sample standard deviation of match-innings RAE across qualifying pressure innings, capturing match-to-match scoring dispersion.
6. **Bootstrap Sampling Uncertainty (95% CI):**
   Match-level cluster bootstrap percentile confidence interval (5,000 resamples at `match_id` level, seed 123) reflecting sampling variability conditional on baseline expectations.
7. **Clean Scoring Rate ($Y_p / n_p$):**
   Descriptive runs scored per clean ball faced. It reflects bat-on-ball output on deliveries with `extras_type == 'None'`. **It is not conventional strike rate** (which includes wides and no-balls and is scaled per 100 balls).
8. **Historical Scope & Window:**
   All metrics reflect historical performance within the 2022–2026 delivery dataset across eligible competitions. **This is a 2022–2026 pressure-performance ranking, not an all-time IPL player ranking or a current-form ranking.** They do not constitute a guarantee of future performance, nor do they establish current physical fitness, recent form, or availability.

---

## 3. Batter Evaluation: Primary Leaderboard

### 3.1 Top Batters by Cumulative Shrunk RAE ($F_1 \cup F_4$ Weighted Composite)
*Ranked by Cumulative Shrunk Clean Runs Above Expected among qualified batters ($N \ge 30$ clean balls faced).*

| Rank | Player Name | Evidence Tier | Exposure Tier | Clean Balls | Obs Runs | Exp Runs | Raw RAE | Shrunk RAE | Shrunk Rate Diff | 95% Bootstrap CI | Clean Scoring Rate |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Suryakumar Yadav** | `STRONG_POSITIVE` | `HIGH` ($\ge 300$) | 1,778.0 | 2,899.0 | 2,669.3 | +229.75 | **+209.09** | +0.1176 | `[+32.22, +397.91]` | 1.6305 |
| **2** | **Tim David** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 836.0 | 1,434.0 | 1,301.4 | +132.61 | **+110.94** | +0.1327 | `[-18.71, +266.06]` | 1.7153 |
| **3** | **Rajat Patidar** | `STRONG_POSITIVE` | `HIGH` ($\ge 300$) | 601.0 | 1,042.0 | 910.1 | +131.94 | **+107.16** | +0.1783 | `[+1.07, +235.03]` | 1.7338 |
| **4** | **Heinrich Klaasen** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 985.0 | 1,603.0 | 1,505.5 | +97.51 | **+79.29** | +0.0805 | `[-15.22, +186.18]` | 1.6274 |
| **5** | **Andre Russell** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 618.0 | 1,081.0 | 980.8 | +100.23 | **+78.92** | +0.1277 | `[-26.76, +196.75]` | 1.7492 |
| **6** | **Ishan Kishan** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 729.0 | 1,186.0 | 1,089.2 | +96.84 | **+76.98** | +0.1056 | `[-46.44, +225.64]` | 1.6269 |
| **7** | **Abhishek Sharma** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 383.0 | 672.0 | 577.4 | +94.59 | **+69.59** | +0.1817 | `[-18.79, +184.64]` | 1.7546 |
| **8** | **Glenn Maxwell** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 636.0 | 1,036.0 | 956.3 | +79.68 | **+60.55** | +0.0952 | `[-52.55, +200.47]` | 1.6289 |
| **9** | **Shreyas Iyer** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 1,096.0 | 1,716.0 | 1,646.9 | +69.13 | **+53.16** | +0.0485 | `[-97.55, +221.13]` | 1.5657 |
| **10** | **Naman Dhir** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 355.0 | 604.0 | 555.7 | +48.30 | **+29.89** | +0.0842 | `[-20.82, +90.72]` | 1.7014 |
| **11** | **Vaibhav Sooryavanshi** | `PROMISING_UNCERTAIN` | `LOW` ($30-99$) | 89.0 | 189.0 | 133.8 | +55.22 | **+24.15** | +0.2713 | `[-12.44, +131.62]` | 2.1236 |
| **12** | **Marcus Stoinis** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 883.0 | 1,393.0 | 1,354.8 | +38.24 | **+23.77** | +0.0269 | `[-91.90, +147.64]` | 1.5776 |
| **13** | **Riyan Parag** | `PROMISING_UNCERTAIN` | `HIGH` ($\ge 300$) | 716.0 | 1,132.0 | 1,095.5 | +36.50 | **+21.73** | +0.0303 | `[-67.06, +123.60]` | 1.5810 |
| **14** | **Ashutosh Sharma** | `PROMISING_UNCERTAIN` | `MODERATE` ($100-299$) | 271.0 | 476.0 | 436.7 | +39.30 | **+21.27** | +0.0785 | `[-29.08, +85.67]` | 1.7565 |
| **15** | **Tom Banton** | `PROMISING_UNCERTAIN` | `MODERATE` ($100-299$) | 193.0 | 328.0 | 287.8 | +40.23 | **+20.44** | +0.1059 | `[-15.21, +71.43]` | 1.6995 |

---

### 3.2 Detailed Cohort Comparison for Noted Players

To prevent confusing $F_1$-only figures with Composite figures, the table below provides exact, fully reconciled metrics across cohorts:

| Player Name | Pressure Cohort | Clean Balls ($n_p$) | Observed Runs ($Y_p$) | Expected Runs ($E_p$) | Raw RAE | Shrunk RAE | Shrunk Rate Diff | 95% Bootstrap CI | Sig ($p<0.05$) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Suryakumar Yadav** | Composite ($F_1 \cup F_4$) | 1,778.0 | 2,899.0 | 2,669.3 | +229.75 | **+209.09** | +0.1176 | `[+32.22, +397.91]` | **Yes** |
| | $F_1$ Primary ($W_2 \le 8$) | 1,757.0 | 2,862.0 | 2,638.2 | +223.76 | **+202.41** | +0.1152 | `[+29.54, +401.50]` | **Yes** |
| **Rajat Patidar** | Composite ($F_1 \cup F_4$) | 601.0 | 1,042.0 | 910.1 | +131.94 | **+107.16** | +0.1783 | `[+1.07, +235.03]` | **Yes** |
| | $F_1$ Primary ($W_2 \le 8$) | 476.0 | 780.0 | 713.0 | +66.97 | **+46.74** | +0.0982 | `[-21.79, +131.69]` | No |
| **Virat Kohli** | Composite ($F_1 \cup F_4$) | 522.0 | 663.0 | 779.9 | -116.93 | **-114.74** | -0.2198 | `[-193.66, -36.50]` | **Yes (Negative)** |
| | $F_1$ Primary ($W_2 \le 8$) | 411.0 | 500.0 | 618.0 | -118.01 | **-112.49** | -0.2737 | `[-183.36, -45.82]` | **Yes (Negative)** |
| **Ravindra Jadeja** | Composite ($F_1 \cup F_4$) | 805.0 | 1,107.0 | 1,285.9 | -178.91 | **-176.70** | -0.2195 | `[-267.34, -94.55]` | **Yes (Negative)** |
| | $F_1$ Primary ($W_2 \le 8$) | 781.0 | 1,073.0 | 1,243.8 | -170.84 | **-169.24** | -0.2167 | `[-265.11, -88.24]` | **Yes (Negative)** |
| **M. S. Dhoni** | Composite ($F_1 \cup F_4$) | 377.0 | 563.0 | 628.4 | -65.42 | **-66.20** | -0.1756 | `[-151.93, +10.95]` | No |
| | $F_1$ Primary ($W_2 \le 8$) | 375.0 | 562.0 | 624.7 | -62.66 | **-64.24** | -0.1713 | `[-154.56, +10.45]` | No |
| **Lokesh Rahul** | Composite ($F_1 \cup F_4$) | 598.0 | 791.0 | 906.1 | -115.12 | **-114.82** | -0.1920 | `[-183.18, -46.75]` | **Yes (Negative)** |
| | $F_1$ Primary ($W_2 \le 8$) | 587.0 | 773.0 | 888.7 | -115.68 | **-114.47** | -0.1950 | `[-181.95, -45.62]` | **Yes (Negative)** |
| **Vaibhav Sooryavanshi** | Composite ($F_1 \cup F_4$) | 89.0 | 189.0 | 133.8 | +55.22 | **+24.15** | +0.2714 | `[-12.44, +131.62]` | No |
| | $F_1$ Primary ($W_2 \le 8$) | 89.0 | 189.0 | 133.8 | +55.22 | **+24.15** | +0.2714 | `[-12.44, +131.62]` | No |

> **Audit Correction Note on Lokesh Rahul (Player ID 953):**
> In prior conversational audit summaries, figures of 524 balls and -113.06 Shrunk RAE were cited. These earlier figures were reporting errors in secondary reporting, not pipeline or data errors. The frozen underlying pipeline artifacts and database tables have always contained exactly **598.0 clean balls faced**, **-115.12 Raw RAE**, **-114.82 Shrunk RAE**, and an **eligible rank of 435**. No underlying pipeline data or calculations were altered.
>
> **Audit Note on Vaibhav Sooryavanshi (Player ID 50284):**
> Sooryavanshi qualified with **89 clean pressure deliveries** across **11 qualifying pressure innings**, accumulating **+55.22 Raw RAE** which shrinks to **+24.15 Shrunk RAE** (Rank 11 eligible). His positive output occurred in **exactly 2 innings** (Match 50943: +51.74 RAE; Match 50944: +24.95 RAE), accounting for **100% of his gross positive innings output**. In his remaining 9 pressure innings, he scored 0 runs off 14 balls (-21.47 RAE). This reflects a high-leverage small historical sample and does not establish future reliability.

---

### 3.3 Interpreting Player Rankings: Kohli and Jadeja Case Study

A critical strategic question arises regarding the placement of **Virat Kohli** (#434 eligible rank; -114.74 Shrunk RAE) and **Ravindra Jadeja** (#450 eligible rank; -176.70 Shrunk RAE) near the bottom of the composite leaderboard. A dedicated competition-exposure audit was completed to investigate whether these rankings stem from unequal coverage between the Indian Premier League (IPL) and Men's T20 Internationals (T20I), retirement effects, or model design.

#### 1. Scope of the Delivery Universe & Analytical Window (2022–2026)
- **Time Horizon:** The analysis covers pressure deliveries strictly from **2022 through 2026** within the supplied dataset. It does **not** evaluate players' entire IPL careers (which span 2008–present).
- **Composite Competition Pooling:** The official composite leaderboard ($F_1 \cup F_4$) pools eligible pressure deliveries across all 883 scheduled matches in the supplied dataset across 141 registered competitions (reconciling under ICC regulations and primary board declarations to 371 IPL matches [367 played, 87,687 deliveries], 483 T20I matches [471 played, 106,582 deliveries], and 29 Other T20 fixtures [29 played, 6,730 deliveries]; 883 scheduled matches, 867 played matches, 16 abandoned matches, 200,999 total deliveries, with **189,167 clean deliveries in the full dataset**, distinct from the non-pressure Model 2 training corpus). It is an all-inclusive composite evaluation, not an IPL-only leaderboard.
- **Baseline Training Corpus:** The Model 2 empirical baseline expectations (`overid` $\times$ `innings`) were fitted exclusively on the distinct subset of **91,649 total non-pressure clean training deliveries across all supplied competitions** (91,623 standard-over non-pressure clean deliveries and 26 Super Over non-pressure clean deliveries), not on the 189,167 full-dataset clean population and not on IPL-only data.

#### 2. Substantial IPL Exposure with Negative IPL-Only Splits
Both players have substantial IPL exposure during this 2022–2026 period, with each facing over 400 clean deliveries in the IPL alone:
- **Virat Kohli:** Faced **404.0 clean balls in the IPL** across 30 innings (77.4% of his total pressure exposure), scoring 524 clean runs against 595.9 expected (**-71.87 Raw RAE**; scoring rate 1.2970 runs/ball vs. 1.4750 expected; rate difference of **-0.1779 runs/ball**).
- **Ravindra Jadeja:** Faced **685.0 clean balls in the IPL** across 43 innings (85.1% of his total pressure exposure), scoring 953 clean runs against 1,093.7 expected (**-140.66 Raw RAE**; scoring rate 1.3912 runs/ball vs. 1.5966 expected; rate difference of **-0.2053 runs/ball**), accounting for **78.6%** of his total negative run accumulation.

Both players show negative raw runs-above-expected in their IPL-only splits. Their lower standing is driven primarily by their sub-baseline scoring in IPL collapse scenarios, not by external formats.

#### 3. T20I Splits and International Retirement
Both players also recorded negative splits in Men's T20Is:
- **Kohli in T20Is:** Accumulated **-45.05 Raw RAE** across 118.0 clean balls (scoring rate 1.1780 vs. 1.5598 expected; rate diff **-0.3818 runs/ball**).
- **Jadeja in T20Is:** Accumulated **-38.24 Raw RAE** across 120.0 clean balls (scoring rate 1.2833 vs. 1.6020 expected; rate diff **-0.3187 runs/ball**).

Following India's 2024 T20 World Cup victory, **Virat Kohli** announced his T20I retirement on **June 29, 2024** and **Ravindra Jadeja** announced his T20I retirement on **June 30, 2024**. Their retirement ended further T20I exposure. The observed T20I rate deficits were more negative than their IPL rate deficits, but the available data cannot establish what their subsequent T20I performance would have been. T20I retirement does not explain away their IPL-period results.

Furthermore, high standing in this dataset does not depend on international volume: for example, **Rajat Patidar** (#3 eligible rank; **+107.16 Shrunk RAE**) faced **zero T20I pressure deliveries** in the dataset (601.0 clean balls entirely in the IPL; **+131.94 Raw RAE**), demonstrating that his ranking was accumulated entirely in the IPL. However, this individual profile illustrates format concentration rather than establishing a universal rule across players.

#### 4. Diagnostic Format-Split Audit Summary
*(Diagnostic comparison from `kohli_jadeja_exposure_audit.md`; the official composite model and prior are preserved.)*

| Player Name | Competition Split | Matches | Innings | Clean Balls ($n_p$) | Observed Runs ($Y_p$) | Expected Runs ($E_p$) | Raw RAE | Clean Scoring Rate | Expected Baseline Rate | Rate Diff ($\text{runs/ball}$) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Virat Kohli** | **Combined Composite** | 42 | 42 | **522.0** | 663.0 | 779.9 | **-116.93** | 1.2701 | 1.4941 | **-0.2240** |
| | IPL Only | 30 | 30 | **404.0** | 524.0 | 595.9 | **-71.87** | 1.2970 | 1.4750 | **-0.1779** |
| | T20I Only | 12 | 12 | **118.0** | 139.0 | 184.1 | **-45.05** | 1.1780 | 1.5598 | **-0.3818** |
| **Ravindra Jadeja** | **Combined Composite** | 50 | 50 | **805.0** | 1,107.0 | 1,285.9 | **-178.91** | 1.3752 | 1.5974 | **-0.2222** |
| | IPL Only | 43 | 43 | **685.0** | 953.0 | 1,093.7 | **-140.66** | 1.3912 | 1.5966 | **-0.2053** |
| | T20I Only | 7 | 7 | **120.0** | 154.0 | 192.2 | **-38.24** | 1.2833 | 1.6020 | **-0.3187** |

#### 5. Proper Strategic Interpretation: What This Leaderboard Does and Does Not Measure
- **Not an All-Time Career Judgment:** These positions must **not** be interpreted as judgments of all-time IPL greatness or career stature. Both players have historic IPL records across 15+ years; this study evaluates strictly the 2022–2026 window.
- **Specific Situational Metric, Not Overall Player Quality:** This leaderboard measures performance under the specific pressure situations that could be reliably identified in the available data (early top-order collapse $W_2 \le 8$ and playoff knockout fixtures $F_4$). It does not measure every form of pressure (such as required run-rate pressure or chase difficulty, which could not be modeled due to absent target data in the source files), nor does it measure captaincy, leadership, tactical reputation, or overall career value.
- **Context of Relative Scoring Differences:** The observed negative results describe scoring performance relative to the selected baseline in these specific pressure situations. The available data cannot establish players' tactical intentions or determine whether their scoring approach was responsible for the difference. These situational results must **not** be described as evidence that either player is generally poor.
- **Preservation of Official Methodology:** The official composite methodology and leaderboard remain exactly as approved. No separate IPL-only ranks are claimed, as calculating formal IPL ranks would require fitting and validating an independent IPL-specific shrinkage model and prior.

---

## 4. Bowler Pressure Diagnostics

Because wide and no-ball penalty extras (+1 run per extra) are omitted in the source data, calculating official bowler economy rates or bowler runs-above-expected models is mathematically invalid. Bowlers are evaluated strictly on **Clean Containment Rate** ($RC_{\text{clean}} / BB_{\text{clean}}$, representing clean runs conceded divided by clean deliveries bowled), **Credited Wickets**, and **Legal Balls per Credited Wicket** ($BB_{\text{legal}} / \text{Wickets}$):

### 4.1 Top High-Exposure Bowlers in Full Multi-Competition Composite Union ($F_1 \cup F_4$, 141 Competitions, 2022–2026)

*Note: The diagnostics below reflect bowler performance across all 141 registered competitions in the 2022–2026 master dataset (5 IPL editions, 134 T20I competitions, 2 mixed-status developmental tournaments, reconciling under ICC regulations and primary board declarations to 371 scheduled IPL matches [367 played, 87,687 deliveries], 483 scheduled T20Is [471 played, 106,582 deliveries], and 29 Other T20 fixtures [29 played, 6,730 deliveries]; 883 scheduled matches, 867 played matches, 16 abandoned matches, 200,999 total deliveries; January 22, 2022 – November 1, 2026). For the specialized 10-player bowler selection evaluated strictly on the 5-season IPL competition context (371 scheduled matches, 367 played matches, 87,687 deliveries; March 26, 2022 – May 26, 2026), refer to [final_bowler_top10.md](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/final/final_bowler_top10.md).*

| Bowler Name | Legal Balls | Clean Balls | Clean Runs Conceded | Clean Containment Rate | Credited Wickets | Balls / Wicket | Model 2 Exp Runs | Clean Runs Residual |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Sunil Narine** | 798 | 782 | 763 | **0.9757** | 36 | 22.17 | 1,154.72 | -391.72 |
| **Akeal Hosein** | 675 | 672 | 693 | **1.0312** | 45 | 15.00 | 1,004.16 | -311.16 |
| **Jasprit Bumrah** | 753 | 740 | 815 | **1.1014** | 51 | 14.76 | 1,179.22 | -364.22 |
| **Varun Chakravarthy** | 1,225 | 1,209 | 1,412 | **1.1679** | 98 | 12.50 | 1,821.33 | -409.33 |
| **Rashid Khan** | 1,781 | 1,747 | 2,118 | **1.2124** | 108 | 16.49 | 2,629.84 | -511.84 |
| **Axar Patel** | 1,467 | 1,454 | 1,790 | **1.2311** | 73 | 20.10 | 2,175.47 | -385.47 |
| **Wanindu Hasaranga** | 1,224 | 1,203 | 1,558 | **1.2951** | 98 | 12.49 | 1,774.26 | -216.26 |
| **Arshdeep Singh** | 1,198 | 1,176 | 1,641 | **1.3954** | 101 | 11.86 | 1,936.51 | -295.51 |

---

## 5. Observed Performance Patterns Under Pressure

### 5.1 Batter Scoring Distributions Under Early Collapses ($W_2 \le 8$)
1. **Scoring Rates Under Early Collapses:**
   When two wickets fall within the first 8 overs, historical data shows a wide dispersion in scoring relative to Model 2 baseline expectations. Batters such as **Rajat Patidar** (+0.1783 runs/ball above baseline in composite) and **Suryakumar Yadav** (+0.1176 runs/ball above baseline) maintained scoring rates above baseline under pressure conditions.
2. **Observed Negative Divergences in Early Collapses:**
   Under $W_2 \le 8$ conditions, **Virat Kohli** scored 500 clean runs off 411 balls in $F_1$ Primary (scoring rate 1.2165 vs. expected baseline 1.5036; deficit of -112.49 Shrunk RAE). **Ravindra Jadeja** scored 1,073 clean runs off 781 balls (scoring rate 1.3739 vs. expected baseline 1.5926; deficit of -169.24 Shrunk RAE). These figures reflect empirical scoring deficits relative to Model 2 baseline expectations in the historical sample. The available data cannot establish players' tactical intentions or determine whether their scoring approach was responsible for the difference.

### 5.2 Observed Individual Bowling Profiles Under Pressure
The analysis evaluates individual bowler performance under pressure rather than deployment combinations, tactical bowling pairings, or causal match-state strategies:
- **Containment Profile:** **Sunil Narine** conceded 0.9757 clean runs per clean delivery bowled across 782 clean balls in the composite cohort (saving 391.72 clean runs relative to Model 2 baseline expectations; 798 legal balls bowled, 36 credited wickets).
- **Dual Containment & Strike Profile:** **Jasprit Bumrah** conceded 1.1014 clean runs per clean delivery bowled across 740 clean balls in the composite cohort (saving 364.22 clean runs relative to baseline) while taking 51 credited wickets (14.76 legal balls per credited wicket across 753 legal balls bowled).

---

## 6. Methodological Disclosures & Unresolved Limitations

Franchise leadership must account for the following explicit methodological boundaries:

1. **Empirical Bayes Variance & Conditional Uncertainty Scope:**
   The Empirical Bayes shrinkage calculations apply an independent-delivery sampling variance ($v_p = \sigma^2 / n_p$, with $\sigma^2 = 2.8443$ for Composite and $2.8294$ for F1 Primary) that assumes conditionally independent deliveries and does not adjust for match clustering. In contrast, the 5,000 match-cluster bootstrap confidence intervals account for match clustering, but are **strictly conditional** on the fixed Model 2 baseline expectations and fixed Empirical Bayes prior hyperparameters. They reflect first-order sampling variation in player delivery outcomes across match clusters; they do not incorporate baseline estimation uncertainty or prior hyperparameter uncertainty, and they do not alter or correct the independent-delivery variance assumption used in the point shrinkage formula itself.
2. **Super Over Baseline Limitations & Population Accounting:**
   Model 2 comprises 42 empirical lookup cells, including 40 cells for standard innings 1 and 2 (overs 1–20; **91,623 standard-over non-pressure clean deliveries**) and 2 Super Over cells (over 1 in innings 3 and innings 4; **26 Super Over non-pressure clean deliveries** across IPL: 11, T20I: 8, Other T20: 7; summing to the **91,649 total non-pressure clean training deliveries**). Across all 38 raw Super Over attempts in the corpus, 6 non-clean deliveries are excluded because they fail the clean-delivery definition (wides/extras), and 6 clean deliveries are excluded from baseline training because they satisfy $F_1$ pressure (all in innings 3; 0 in $F_4$), leaving exactly 26 Super Over non-pressure clean deliveries (15 in innings 3, 11 in innings 4). All six clean Super Over F1 flags are retrospective: each is the delivery on which W2 is established. The batter faces that delivery before the second wicket has fallen. A strictly prospective F1 definition would begin only after W2 occurs. The frozen retrospective flags and official model outputs remain unchanged. While the 6 Super Over pressure deliveries map directly to cell (1, 3) without fallback, Super Over baseline expectations are substantially less reliable than standard-innings estimates due to limited observations.
3. **Absence of Multiple-Testing Corrections:**
   Hypothesis tests ($p < 0.05$) are evaluated on individual unadjusted 95% confidence intervals across 456 eligible batters. No Bonferroni or False Discovery Rate (FDR) correction is applied; positive interval bounds provide exploratory or nominal evidence rather than confirmatory proof.
4. **Excluded Pressure Dimensions (F2 & F3):**
   Target difficulty, required run rate pressure, and dynamic Win Probability Added (WPA) remain excluded due to the absence of cumulative live scoreboards and target data in the source files.
5. **Historical Scope & Current Roster Context:**
   Rankings evaluate past delivery logs from 2022–2026. They do not incorporate player age, recent physical conditioning, injury status, domestic form in recent months, or auction pricing dynamics.
6. **Language Standards:**
   All assessments are strictly descriptive of the historical sample analyzed. Causal claims, tactical intent inferences, and claims of permanent status or assured future performance are excluded.
7. **Scoring Residual Framework Boundaries & Omission of Wicket Preservation:**
   The scoring residual framework measures runs scored above or below a phase/over-based empirical baseline expectation. It does not fully capture wicket preservation, match-win probability, or tactical stabilization value under collapse conditions. Batters who stabilize an innings by absorbing deliveries to prevent further wickets are evaluated solely on their scoring residual relative to baseline; players are neither rewarded for preserving wickets nor penalized for strategic opportunity costs beyond clean scoring residuals.
8. **Innings-Level Reliability Metric Specification:**
   Positive innings frequency is calculated strictly as the proportion of qualifying pressure match-innings (where the batter faced $\ge 1$ clean pressure delivery) with $\text{RAE}_{\text{inns}} > 0$. It does not represent the proportion of all career matches in which a player performed well. Cumulative Shrunk RAE ($n_p \cdot \theta_p^*$) scales with exposure volume and must be decoupled from rate efficiency, positive innings frequency, median performance, and volatility.
9. **Master Population Accounting & Squad Participation Verification:**
   The source competition universe contains **1,217 registered squad members** across all tournament rosters (`competition_team_player_mapping.csv`). Of these, **1,082 players appeared in starting playing elevens** (`playing_eleven.csv`), and **2 additional registered squad members** (`Syed Haider` [ID 36153] and `Basil Hameed` [ID 39444]) appeared as substitute batters in `ball_by_ball.csv`, establishing **1,084 total unique on-field match participants**. Because both substitute batters belong to the registered squad list, the number of registered squad members who did not participate in the analyzed matches is exactly **133** (1,217 − 1,084 = 133), not 135.

---
*SupeRR Selector Season 2 — Analytical Project Report.*

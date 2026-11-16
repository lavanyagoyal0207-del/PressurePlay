# Stage 4 Methodology: Statistical Estimation of Pressure Performance
**Rajasthan Royals SupeRR Selector Season 2 Analysis**
*Execution Timestamp:* 2026-11-15T18:08:47.524899+00:00
*Validation Verdict:* **APPROVED**

---

## 1. Feasibility Gate & Data Boundaries
* **Input Isolation:** All computations are built strictly upon the approved Stage 1 event counters, Stage 2 delivery eligibility flags, and Stage 3 descriptive statistics. Source datasets in `data/data_pack/` and approved outputs in `outputs/pressure/` and `outputs/descriptive/` are untouched.
* **Empirical Predictors Used:** Delivery over index (`overid` in 1..20), match innings (1 or 2), match phase (powerplay, middle, death), and wickets fallen prior to delivery.
* **Excluded Variables:**
  * Target Difficulty & Required Run Rate: Excluded due to absence of verifiable delivery-level target and DLS context.
  * Official Bowler Economy & Conceded Runs: Excluded due to unrecorded 1-run penalties on 7,714 wides and 576 no-balls.
  * Artificial Leverage Multipliers: Strictly zero leverage multipliers.

---

## 2. Expected Clean Runs Baseline Model
* **Training Corpus:** Fitted on **91,649 non-pressure clean deliveries** (`f1_primary == False` and `f4_knockout == False`).
* **Zero Leakage:** Pressure delivery outcomes never inform their own expected baseline.
* **Out-of-Fold 5-Fold Cross-Validation Performance:**
  * **Model 2 (Overid x Innings Empirical Baseline, Selected Primary):**
    * Out-of-fold MAE: **1.4131** runs
    * Out-of-fold RMSE: **1.7930** runs
    * Mean Predicted: **1.4886** runs vs. Mean Observed: **1.4884** runs
    * Calibration Slope: **0.9439**, Calibration Intercept: **0.0832**
  * Outperformed the simple global mean baseline (MAE: 1.4282, RMSE: 1.8032) and phase-level models through unconstrained empirical cell-by-cell over index and innings lookup (42 discrete cells) without imposing parametric form or monotonic constraints.

---

## 3. Empirical Bayes Shrinkage Architecture
To separate true pressure talent from small-sample noise, an Empirical Bayes normal-normal shrinkage model was fitted via the DerSimonian-Laird (DL) estimator:

$$\theta_i = \frac{Y_i - E_i}{n_i}, \quad v_i = \frac{\sigma^2}{n_i}$$

$$\tau^2 = \max\left(0, \frac{Q - (K - 1)}{\sum w_i - \frac{\sum w_i^2}{\sum w_i}}\right), \quad w_i = \frac{1}{v_i}$$

$$B_i = \frac{v_i}{\tau^2 + v_i}$$

$$\theta_i^{\text{shrunk}} = (1 - B_i) \theta_i + B_i \mu, \quad \text{RAE}_i^{\text{shrunk}} = n_i \cdot \theta_i^{\text{shrunk}}$$

* **F1 Primary Prior Parameters:**
  * Prior Mean mu: **-0.1942** runs/ball (reflects baseline pressure scoring depression).
  * True Talent Dispersion tau: **0.2024** runs/ball (tau^2 = 0.040950).
  * Pooled Delivery Residual Variance sigma^2: **2.8294**.
* High-exposure batters (n >= 150) maintain minimal shrinkage (B_i < 0.30), while low-exposure batters (n < 20) shrink heavily toward the prior (B_i > 0.85). Both raw and shrunk metrics are reported side by side.

---

## 4. Family Overlap Normalization
Active families are F1 (weight = 1.0) and F4 (weight = 0.5); F2 and F3 remain excluded due to missing data.
Weights are normalized per delivery by dividing by the sum of active raw weights:

$$w_k(d) = \frac{\text{raw}\_w_k}{\sum_{j \in \text{active}} \text{raw}\_w_j}$$

* **F1 Only Deliveries (93,110 clean):** w_F1 = 1.0 / 1.0 = 1.0.
* **F4 Only Deliveries (2,380 clean):** w_F4 = 0.5 / 0.5 = 1.0.
* **F1 and F4 Overlap Deliveries (2,028 clean):** w_F1 = 1.0 / 1.5 = 2/3, w_F4 = 0.5 / 1.5 = 1/3.
* **Combined Delivery Weight:** w_F1(d) + w_F4(d) = 1.0 for every delivery in F1 union F4 (97,518 clean deliveries).
* **Guarantees:** Zero double-counting, exact component additivity, and exact preservation of the 2:1 family ratio on overlap deliveries.

---

## 5. Match-Level Cluster Bootstrap (5,000 Replicates)
* **Cluster Resampling:** Resampling with replacement occurs at the `match_id` level (745 unique match clusters), strictly preserving intra-match correlation and player exposure structures.
* **Vectorized Execution:** Completed in <2 seconds across 5,000 replicates using matrix multiplication Delta * C.
* **Uncertainty Metrics:** Standard errors and empirical 95% confidence intervals (2.5% to 97.5% quantiles) are computed for raw RAE, shrunk RAE, and excess run rates.
* **Conditional Scope of Uncertainty:** The 5,000 match-cluster bootstrap intervals are strictly conditional on the fitted baseline expected-runs model and empirical-Bayes prior parameters (mu, tau^2). Baseline model estimation error and empirical-Bayes hyper-parameter uncertainty are held fixed and not incorporated; these intervals reflect first-order sampling variation in player outcomes given match clustering, not full posterior or predictive uncertainty.
* **Zero Significance Fallacy:** Players whose 95% confidence interval crosses zero are explicitly flagged as not statistically significant.

---

## 6. Systematic Sensitivity Analysis
* **Window Definition:** Rank correlation between F1 Primary and F1 Alt 1A Complete-60 is **rho = 0.7847** (Kendall tau = 0.6350, Top-10 overlap = 60.0%), confirming structural stability while reflecting the impact of truncated innings.
* **Alternative Window Comparison:** F1 Alt 1A Complete-60 vs. Alt 1A All (322 players) has Spearman rho = 0.9628, Kendall tau = 0.8746, mean absolute rank shift = 13.16, and Top-10 overlap = 70.0%. The overall rankings are strongly associated; the 70.0% Top-10 overlap indicates some changes among the leading players.
* **Window Cutoff Thresholds:** W2 <= 8 vs. W2 <= 6 achieves **rho = 0.9424**; W2 <= 8 vs. W2 <= 10 achieves **rho = 0.9769** (100% top-10 overlap).
* **Overlap Normalization:** Composite ranking correlates at **rho = 0.9872** with F1 Primary and **rho = 1.0000** with Unweighted Union, showing that normalized composite weighting integrates knockout playoff matches cleanly without destabilizing baseline pressure ratings.
* **Baseline Specification:** Primary Model 2 correlates at **rho = 0.9830** with Model 1 (Phase) and **rho = 0.9351** with Model 0 (Global Mean). Model 3 (Overid x Innings + Wickets Fallen) achieves **rho = 0.6393** with dynamic Model 2 fallback, but suffers from a 27.0% structural support deficit in non-pressure training data (early overs with >= 2 wickets fallen rarely occur outside pressure); Model 3 is explicitly marked unreliable and excluded from model selection conclusions.
* **Shrinkage Effect:** Shrunk vs. Raw RAE has rank correlation **rho = 0.9562** among qualified batters, successfully attenuating noise without distorting established elite performers.

---

## 7. Deliverables Index
All artifacts are saved under `outputs/statistical/`:
1. `outputs/statistical/baseline_model_report.json`
2. `outputs/statistical/batter_pressure_estimates.csv`
3. `outputs/statistical/bowler_pressure_diagnostics.csv`
4. `outputs/statistical/bootstrap_uncertainty.csv`
5. `outputs/statistical/sensitivity_analysis.csv`
6. `outputs/statistical/stage4_validation_report.json`
7. `outputs/statistical/stage4_methodology.md`

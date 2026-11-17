# Technical Methodology & Analytical Architecture
## Rajasthan Royals SupeRR Selector Season 2
### Methodological Specification for Pressure Performance Evaluation (Stages 1 through 5)

---

## 1. Scope, Core Principles & Feasibility Boundaries

This document provides the technical specification and mathematical architecture for the **Rajasthan Royals SupeRR Selector Season 2** pressure evaluation framework.

Player evaluation in high-leverage Twenty20 (T20) scenarios requires disciplined statistical handling:
1. **Context-Conditioned Expectations:** Performance must be measured against an empirical baseline reflecting the specific match state rather than unadjusted raw averages.
2. **Small-Sample Attenuation:** In high-leverage subsets (such as early-wicket collapses or playoff matches), exposure is limited. Unadjusted rankings over-index on volatile outliers. Empirical Bayes shrinkage pulls noisy estimates toward the population prior, dampening small-sample inflation.
3. **Cluster-Correlated Uncertainty:** Deliveries within the same match share pitch, weather, opponent, and game-state conditions. Confidence intervals must account for match clustering.
4. **Strict Data Grounding:** Metrics must rely solely on verified source attributes. Unrecorded quantities (such as penalty runs for wides and no-balls) must not be estimated or fabricated.

---

## 2. Stage 1: Data Architecture & Delivery Taxonomy

### 2.1 The Delivery Universe & Source Taxonomy
The source data consists of 200,999 delivery rows across T20 competitions. A structural audit revealed the following empirical distribution of the `extras_type` attribute:

| `extras_type` Stored Value | Delivery Count | Percentage | Attributed Runs Range | Batter Attribution Rule | Bowler Attribution Rule |
|---|---|---|---|---|---|
| `'None'` (literal string) | 189,167 | 94.11% | 0 to 6 runs | **Full attribution** to striker | **Full attribution** as clean runs conceded |
| `'wide'` | 7,714 | 3.84% | Always 0 runs | **Excluded** (not faced by batter) | **Excluded** from legal overs; penalty unrecorded |
| `'legbyes'` | 2,748 | 1.37% | 0 (2,747 rows), 1 (1 row) | **Excluded** from batter runs | Counted as legal ball; 0 runs conceded |
| `'Overstep'` (No-ball) | 576 | 0.29% | 0 to 6 runs | **Batter runs only** (off the bat) | **Excluded** from legal overs; +1 penalty unrecorded |
| `'byes'` | 529 | 0.26% | Always 0 runs | **Excluded** from batter runs | Counted as legal ball; 0 runs conceded |
| `'other'` | 264 | 0.13% | 0 to 6 runs | **Excluded** (undocumented taxonomy) | **Excluded** from primary metrics |
| `'Penalty'` | 1 | <0.01% | Undisplayable | **Excluded** (undocumented) | **Excluded** |
| **Total** | **200,999** | **100.00%** | — | — | — |

### 2.2 Key Structural Rules & Denominators
1. **Literal String `'None'`:** In `ball_by_ball.csv`, clean deliveries store the literal string `'None'`. Pipeline filtering must use string equality (`extras_type == 'None'`).
2. **Unrecorded Penalty Runs:** Source data does not record the mandatory +1 run penalty for `'wide'` or `'Overstep'` deliveries. Bye and leg-bye run amounts are absent from `runs` (storing 0). Consequently, **official bowler economy rates and total runs conceded cannot be mathematically calculated from source fields.** All bowling analyses must evaluate clean containment (`RC_clean / BB_clean`).
3. **Sequencing Conventions:**
   - **Legal Ball Sequence (`legal_ball_seq`):** Increments on `'None'`, `'byes'`, `'legbyes'`, `'other'`, `'Penalty'`. Does not increment on `'wide'` or `'Overstep'`.
   - **Batter Ball Sequence (`batter_ball_seq`):** Increments on `'None'`, `'Overstep'`, `'byes'`, `'legbyes'`, `'other'`, `'Penalty'`. Does not increment on `'wide'`.
   - **Clean Balls Faced ($BF_{\text{clean}}$):** Deliveries with `extras_type == 'None'`.

---

## 3. Stage 2: Pressure Eligibility & Overlap Architecture

### 3.1 Pressure Family Formulations
The evaluation isolates two empirically verifiable high-leverage pressure regimes:

- **Family 1: Early-Wicket Collapse ($F_1$ Primary):**
  The second wicket ($W_2$) of an innings falls at or before over 8 ($\text{overid}(W_2) \le 8$). The pressure window extends from $W_2$ inclusive through the final delivery of that innings.
  - *Sensitivity Variants:* Alt 1A Complete-60 ($W_2$ plus next 59 verified legal balls), Alt 1B (through end of over 15), and Alt 1C (varying $W_2$ threshold at $\le 6$, $\le 8$, $\le 10$).
- **Family 4: Playoff / Knockout Fixtures ($F_4$):**
  All deliveries across both innings of tournament playoff stages (Eliminator, Qualifier, Semi-Final, Final; 20 matches in dataset).

### 3.2 Family Overlap Normalization
When an innings satisfies both $F_1$ (early collapse) and $F_4$ (knockout match), deliveries within the intersection belong to both pressure families. To prevent double-counting while preserving total exposure volume, weights are normalized per delivery:

$$w_k(d) = \frac{\text{raw}\_w_k}{\sum_{j \in \text{active}(d)} \text{raw}\_w_j}$$

Under raw family weights $\text{raw\_w}_1 = 1.0$ and $\text{raw\_w}_4 = 0.5$:
- **$F_1$-Only Delivery (93,110 clean deliveries):**
  $$w_1(d) = \frac{1.0}{1.0} = 1.0, \quad w_4(d) = 0.0$$
- **$F_4$-Only Delivery (2,380 clean deliveries):**
  $$w_4(d) = \frac{0.5}{0.5} = 1.0, \quad w_1(d) = 0.0$$
- **$F_1 \cap F_4$ Overlap Delivery (2,028 clean deliveries):**
  $$w_1(d) = \frac{1.0}{1.0 + 0.5} = \frac{2}{3} \approx 0.6667, \quad w_4(d) = \frac{0.5}{1.0 + 0.5} = \frac{1}{3} \approx 0.3333$$
- **Combined Exposure Weight:**
  $$w_{\text{composite}}(d) = w_1(d) + w_4(d) = 1.0 \quad \text{for every delivery in } F_1 \cup F_4 \text{ (97,518 clean deliveries)}$$

**Clarification on Raw Weights:** The 2:1 ratio of raw weights affects allocation **only on overlapping deliveries**. An $F_4$-only delivery contributes full weight 1.0, not half weight. Total pressure exposure equals the exact count of pressure deliveries faced.

---

## 4. Stage 3 & 4: Expected-Performance Baseline Model

### 4.1 Model 2: Overid $\times$ Innings Empirical Baseline
To evaluate whether a batter overperforms or underperforms, clean delivery run outcomes are compared against an empirical baseline model fitted exclusively on non-pressure clean deliveries:

- **Training Corpus & Denominator:** Fitted on **91,649 total non-pressure clean training deliveries** (`f1_primary == False` and `f4_knockout == False`), comprising **91,623 standard-over non-pressure clean deliveries** and **26 Super Over non-pressure clean deliveries**:
  - *Standard Overs (Overs 1–20, Innings 1 & 2):* **91,623 standard-over non-pressure clean deliveries** (Innings 1: 49,576; Innings 2: 42,047; IPL: 42,063; T20I: 46,798; Other T20: 2,762).
  - *Super Overs (Over 1, Innings 3 & 4):* **26 Super Over non-pressure clean deliveries** (Innings 3: 15; Innings 4: 11; IPL: 11; T20I: 8; Other T20: 7).
  - *Competition Totals:* IPL: **42,074** ($42,063 + 11$); T20I: **46,806** ($46,798 + 8$); Other T20: **2,769** ($2,762 + 7$).
- **Feature Space:** Discrete interaction of delivery over index (`overid` in 1..20) and match innings (1..4), forming **42 empirical cells** (40 ordinary innings cells plus 2 Super Over cells: `(overid=1, innings=3)` with empirical mean 0.6000 runs, and `(overid=1, innings=4)` with empirical mean 2.7273 runs).
- **Super Over Population Accounting & Support:**
  - Across the 2022–2026 dataset, there are **38 total Super Over delivery attempts** across 6 matches.
  - **6 non-clean attempts** (4 wides, 1 other extra, 1 legbye) are excluded by the clean-delivery definition.
  - Of the **32 clean deliveries** faced by batters, **6 clean deliveries** satisfy the $F_1$ Early-Wicket Collapse condition ($\text{overid}(W_2) \le 8$) in Innings 3; these are excluded from Model 2 baseline training because they are pressure deliveries. Exactly 0 satisfy $F_4$ (zero clean $F_4$-only or $F_1 \cap F_4$ Super Over deliveries).
  - The remaining **26 clean deliveries** are non-pressure deliveries included in Model 2 training (15 in Innings 3, 11 in Innings 4).
  - All six clean Super Over F1 flags are retrospective: each is the delivery on which W2 is established. The batter faces that delivery before the second wicket has fallen. A strictly prospective F1 definition would begin only after W2 occurs. The frozen retrospective flags and official model outputs remain unchanged.
  - Exactly 6 clean pressure deliveries occur in Super Over innings 3, mapping directly to cell `(1, 3)` with expectation 0.6000 runs (no fallback to global mean triggered). Because the training data contains only 15 and 11 clean deliveries for innings 3 and 4, Super Over support is sparse, and baseline predictions for Super Over deliveries are substantially less reliable than for standard innings 1 and 2.
- **Out-of-Fold 5-Fold Cross-Validation:**
  - Evaluated via 5-fold match-grouped cross-validation to prevent intra-match leakage.
  - Out-of-fold Mean Absolute Error (MAE): **1.4131** runs.
  - Out-of-fold Root Mean Squared Error (RMSE): **1.7930** runs.
  - Mean Predicted: **1.4886** runs vs. Mean Observed: **1.4884** runs.
  - Calibration Slope: **0.9439**, Calibration Intercept: **0.0832**.
- **Model Comparison:**
  - *Model 0 (Global Mean):* Constant prediction ($\mu = 1.4884$ runs). Out-of-fold MAE: 1.4282, RMSE: 1.8032. Mean predicted: 1.4884. Calibration slope and intercept are undefined/null for a constant predictor.
  - *Model 1 (Phase-level):* Partitioned into match phase (Powerplay, Middle, Death) and innings. Out-of-fold MAE: 1.4239, RMSE: 1.8003. Mean predicted: 1.4886. Calibration slope: 0.9419, intercept: 0.0863.
  - *Model 3 (Overid $\times$ Innings + Wickets Fallen):* Evaluated for sensitivity. Suffers from a 27.0% structural support deficit in non-pressure training data (early overs with $\ge 2$ wickets fallen rarely occur outside pressure). Labeled unreliable and excluded from model selection.

---

## 5. Statistical Estimation & Uncertainty Framework

### 5.1 Runs Above Expected (RAE) Definitions
For batter $p$ across pressure clean deliveries $i \in \mathcal{D}_p$:
$$\text{Clean Balls Faced: } n_p = \sum_{i \in \mathcal{D}_p} w_i$$
$$\text{Observed Clean Runs: } Y_p = \sum_{i \in \mathcal{D}_p} w_i Y_i$$
$$\text{Expected Clean Runs: } E_p = \sum_{i \in \mathcal{D}_p} w_i \hat{Y}_i$$
$$\text{Raw RAE: } \text{Raw RAE}_p = Y_p - E_p$$
$$\text{Raw Rate Above Expected: } \theta_p = \frac{Y_p - E_p}{n_p} \quad (\text{runs per clean ball above baseline})$$

### 5.2 Empirical Bayes (DerSimonian–Laird) Shrinkage
Player rate estimates $\theta_p$ are shrunk using the DerSimonian–Laird (DL) random-effects model:

$$\theta_p \mid \theta_p^{\text{true}} \sim \mathcal{N}\left(\theta_p^{\text{true}}, v_p\right), \quad v_p = \frac{\sigma^2}{n_p}$$
$$\theta_p^{\text{true}} \sim \mathcal{N}\left(\mu, \tau^2\right)$$

Where:
- $\sigma^2$ is the pooled delivery residual variance (2.8443 for Composite, 2.8294 for F1 Primary).
- $\mu$ is the prior mean (-0.1872 for Composite, -0.1942 for F1 Primary), reflecting baseline scoring depression under pressure.
- $\tau^2$ is the between-player true variance (0.041989 for Composite, 0.040950 for F1 Primary; $\tau \approx 0.20$ runs/ball).
- **Sampling Variance Assumption:** Sampling variance $v_p = \sigma^2 / n_p$ is a model-based, independent-delivery variance formulation (delivery residual variance divided by clean balls faced). It assumes conditional independence across deliveries and does **not** adjust for intra-match clustering or delivery-to-delivery correlation within matches.
- Shrinkage factor:
  $$B_p = \frac{v_p}{\tau^2 + v_p}$$
- Shrunk Rate Above Expected:
  $$\theta_p^* = (1 - B_p) \theta_p + B_p \mu$$
- **Cumulative Shrunk RAE:**
  $$\text{Shrunk RAE}_p = n_p \cdot \theta_p^*$$

### 5.3 Critical Distinction: Volume vs. Rate vs. Strike Rate
Decision-makers must rigorously distinguish the following metrics:
1. **Cumulative Shrunk RAE ($\text{Shrunk RAE}_p$):** An exposure-dependent aggregate volume measure (measured in total runs). It reflects the net runs generated above or below baseline over the historical sample. It is **not** a standardized talent rating, rate per ball, or runs-above-replacement metric.
2. **Shrunk Rate Above Expected ($\theta_p^*$):** A rate metric (measured in runs per clean ball above baseline). It indicates individual efficiency per delivery faced.
3. **Clean Scoring Rate:** Descriptive runs per clean ball ($Y_p / n_p$). This must **never** be termed "strike rate", which conventionally scales to runs per 100 balls including extras.

### 5.4 Match-Level Cluster Bootstrap (5,000 Replicates)
To evaluate sampling uncertainty:
- **Resampling Procedure:** 5,000 bootstrap draws resampling intact `match_id` clusters with replacement across 745 match clusters, preserving delivery clustering within matches.
- **Conditional Nature of Bootstrap:** Bootstrap confidence intervals are **strictly conditional** on the fitted Model 2 baseline expectations and Empirical Bayes prior hyperparameters ($\mu, \tau^2$), which are held fixed across resamples. The intervals capture first-order sampling variation in player delivery outcomes given match clustering; they do not incorporate baseline parameter estimation error or prior hyperparameter uncertainty. Crucially, while the bootstrap evaluates cluster-correlated uncertainty for player confidence intervals, it **does not retroactively alter or correct the independent-delivery sampling variance assumption ($v_p = \sigma^2 / n_p$) used in the empirical Bayes point shrinkage formula itself**.
- **Nominal Statistical Significance:** A player's estimate is flagged as nominal statistically significant ($p < 0.05$) only if their individual 95% bootstrap confidence interval strictly excludes zero. These intervals are unadjusted for multiple comparisons across the 456 eligible batters and represent exploratory evidence.

---

## 6. Stage 5: Evaluation Framework & Shortlist Logic

### 6.1 Evidence Tiers
Players with $N \ge 30$ clean balls are classified into evidence tiers based on point estimates and confidence intervals:
- **`STRONG_POSITIVE_EVIDENCE`:** Shrunk RAE $> 0$, $N \ge 30$, 95% CI lower bound $> 0$. (Statistically supported positive divergence).
- **`PROMISING_UNCERTAIN`:** Shrunk RAE $> 0$, $N \ge 30$, 95% CI lower bound $\le 0$. (Positive point estimate; confidence interval spans zero).
- **`STRONG_NEGATIVE_EVIDENCE`:** Shrunk RAE $< 0$, $N \ge 30$, 95% CI upper bound $< 0$. (Statistically supported negative divergence).
- **`BELOW_EXPECTATION_UNCERTAIN`:** Shrunk RAE $< 0$, $N \ge 30$, 95% CI upper bound $\ge 0$. (Negative point estimate; confidence interval spans zero).
- **`INSUFFICIENT_EXPOSURE`:** $N < 30$ clean balls faced. (Sample too small for reliable inference; estimate pulls heavily to prior).

### 6.2 Bowler Diagnostics Framework
Bowlers are evaluated on:
- **Clean Containment Rate:** Clean runs conceded per clean delivery bowled ($RC_{\text{clean}} / BB_{\text{clean}}$).
- **Credited Wickets:** Bowler-credited dismissals (`caught`, `bowled`, `lbw`, `stumped`, `hit wicket`).
- **Balls per Wicket:** Legal deliveries bowled per credited wicket ($BB_{\text{legal}} / \text{Wickets}$).
- **Diagnostic Residual:** Clean runs conceded minus expected clean runs under Model 2 baseline. Total runs conceded and official economy are omitted due to unrecorded penalty extras.

*Competition Scope Specification:* Baseline bowler diagnostics ([final_bowler_diagnostics.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/final/final_bowler_diagnostics.csv)) evaluate 600 unique bowlers across the full multi-competition master dataset (141 registered competitions: 5 IPL editions, 134 T20I competitions, 2 mixed-status developmental tournaments, reconciling under ICC regulations and primary board declarations to 371 scheduled IPL matches [367 played, 87,687 deliveries], 483 scheduled T20Is [471 played, 106,582 deliveries], and 29 Other T20 fixtures [29 played, 6,730 deliveries]; 883 scheduled matches, 867 played matches, 16 abandoned matches, 200,999 total deliveries; January 22, 2022 – November 1, 2026). In contrast, the specialized 10-player bowler selection ([final_bowler_top10.md](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/final/final_bowler_top10.md)) evaluates Pareto efficiency strictly across the 5-season IPL competition context (371 scheduled matches, 367 played matches, 87,687 deliveries; March 26, 2022 – May 26, 2026) for IPL-specific pressure-performance analysis under league conditions.

---

## 7. Methodological Limitations & Boundary Disclosures

1. **Conditional Uncertainty Scope:** Bootstrap confidence intervals hold baseline predictions and Empirical Bayes prior parameters fixed. They reflect sampling variability in player outcomes across matches, not full posterior predictive uncertainty.
2. **No Multiple-Comparisons Adjustment:** Significance flags reflect individual unadjusted 95% confidence intervals. Across 456 eligible batters, individual tests are subject to family-wise false discovery risk.
3. **Excluded Pressure Families (F2 & F3):** Run Chase Pressure (F2) and Required Run Rate Pressure (F3) remain excluded due to the absence of reliable delivery-level cumulative scores and target scoreboards.
4. **Historical vs. Current Form:** All calculations reflect historical performance within the 200,999 delivery dataset. Rankings do not incorporate current player age, recent physical fitness, injuries, auction availability, or roster balance.
5. **Language Standards:** Measured empirical terminology is maintained throughout; claims of permanent ranking, unassailable superiority, or assured future performance are excluded.
6. **Scoring Residual Framework Boundaries:** The scoring residual framework measures runs scored above or below a phase/over-based empirical baseline expectation. It does not fully capture wicket preservation, match-win probability, or tactical stabilization value under collapse conditions.
7. **Innings-Level Qualification Scope:** Positive innings frequency evaluates strictly qualifying pressure match-innings where a batter faced $\ge 1$ clean pressure delivery; it does not represent the proportion of all career matches in which a player performed well. Cumulative Shrunk RAE is a volume-weighted aggregate value-added metric, not a measure of game-to-game reliability or failure avoidance.
8. **Population Universe Accounting:** The underlying competition universe encompasses 1,217 registered squad members, 1,082 starting XI players, and 2 registered substitute match batters (Player IDs 36153 and 39444), establishing 1,084 total unique on-field match participants and 133 registered squad members who did not participate in the analyzed matches.

---
*Technical Methodology Specification for Rajasthan Royals SupeRR Selector Season 2.*

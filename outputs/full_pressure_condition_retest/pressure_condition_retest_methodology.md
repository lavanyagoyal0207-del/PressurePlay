# Pressure Condition Retest: Methodological Architecture & Specification
## Independent IPL Reanalysis (2022–2026) Across 40 Candidate Pressure Conditions
### SupeRR Selector Season 2 — Comprehensive Pressure Performance Evaluation

---

## 1. Executive Overview & Research Objective

This methodology document provides the mathematical, empirical, and architectural foundation for testing the comprehensive suite of **40 candidate pressure conditions** developed under the **SupeRR Selector Season 2** research framework.

While earlier pipeline iterations constrained empirical evaluation primarily to Early-Wicket Collapse ($F_1$) and Playoff Fixtures ($F_4$), the official problem statement requested a multi-dimensional definition of pressure spanning required run rates, wickets in hand, balls remaining, match stage, contest closeness, and tournament stakes. This investigation recovers all 40 candidate conditions, evaluates their operational feasibility against the 2022–2026 Indian Premier League (IPL) delivery dataset, and conducts an independent reanalysis of batting performance under pressure, focusing on **Virat Kohli (Player ID: 47)** and comparative standings across the entire eligible IPL batter cohort.

---

## 2. Dataset Scope & Model 2 Baseline Expectations

### 2.1 IPL Corpus Definition
- **Competitions Included:** All 5 IPL tournaments in the competition data pack:
  - IPL 2022 (`comp_id: 1358`)
  - IPL 2023 (`comp_id: 1715`)
  - IPL 2024 (`comp_id: 2193`)
  - IPL 2025 (`comp_id: 2725`)
  - IPL 2026 (`comp_id: 3298`)
- **Total IPL Matches:** 371 matches spanning March 26, 2022 to May 31, 2026.
- **Total IPL Deliveries:** 87,687 delivery records.
- **Clean IPL Deliveries:** 82,458 deliveries (excluding illegal bowling extras: wides, oversteps, and unclassified penalty runs).

### 2.2 Model 2 Empirical Baseline Expectation
In strict adherence to the project's zero-leakage and baseline-conditioning principles, expected scoring is conditioned on delivery over index (`overid` 1..20) and match innings (`innings` 1..4), forming **42 discrete empirical lookup cells** (40 ordinary innings cells plus 2 Super Over cells):

$$\mathbb{E}[R_{i} \mid \text{overid}=o, \text{innings}=m]$$

The baseline model is fit exclusively on the non-pressure clean delivery pool ($n = 42,074$ standard clean deliveries; global mean $\mu = 1.4883$ runs/ball). Every delivery outcome $y_i$ is evaluated against its expected scoring rate:

$$\text{Residual}_{i} = y_{i} - \mathbb{E}[R_{i}]$$

---

## 3. The 40 Candidate Pressure Conditions Taxonomy

The 40 candidate conditions span the four primary pressure dimensions ($F_1, F_2, F_3, F_4$) and situational match states:

```
Candidate Conditions Taxonomy (40 Total)
├── Family 1: Early-Wicket Collapse (13 Conditions: C01–C13)
│   ├── Sensitivity thresholds: W2 <= 6 (C06), W2 <= 8 (C01, C07), W2 <= 10 (C08)
│   ├── Window specifications: 60-ball window (C02), Complete 60 (C03), Truncated 60 (C04), Middle-overs cutoff (C05)
│   ├── Deeper collapses: Powerplay collapse (C09), Top-3 collapse (C10, C11), Top-4 collapse (C12)
│   └── Scoring stagnation: Middle-over stagnation <= 20 runs across 4 overs (C13)
├── Family 4: High-Leverage Fixtures & Deciders (7 Conditions: C14–C20)
│   ├── Tournament playoffs: Knockout match deliveries (C14), Knockout phases (C18, C19, C20)
│   ├── Combinations: F1 ∪ F4 Union (C15), F1 ∩ F4 Overlap (C16)
│   └── Tied matches: Super Overs (C17)
├── Match Phase × Wickets Lost Grid (10 Conditions: C21–C30)
│   ├── Death overs: All death (C21), Innings 1 death (C22), Innings 2 death (C23)
│   ├── High-wickets death: >= 4 down (C24), >= 6 down (C25)
│   ├── Middle crisis: >= 3 down (C26), >= 5 down (C27)
│   ├── Powerplay crisis: >= 2 down (C28), >= 3 down (C29)
│   └── Deep collapse: >= 7 down (C30)
└── Family 2 & 3: Run Chase & Required Run Rate (10 Conditions: C31–C40)
    ├── Run chase context: General 2nd innings (C31), High target >= 180 (C32), Steep target >= 200 (C33), Low target <= 150 (C34), Death chase (C35), Close finish (C36)
    ├── Required run rate: RRR >= 10.0 (C37), RRR >= 12.0 (C38), RRR >= 14.0 (C39)
    └── Dynamic Win Probability: High-leverage WPA index (C40 - Category C)
```

### Operationalisation Classification
- **Category A (Fully Operationalisable, Exact):** 28 conditions computable directly from logged ball events without structural assumptions.
- **Category B (Operationalisable with Explicit Approximation):** 11 conditions reconstructed from cumulative match and innings scoreboards (target difficulty, reconstructed RRR, close finishes).
- **Category C (Unobservable / Data Deficient):** 1 condition (`C40_dynamic_wpa_crisis`) requiring pre-delivery live betting odds or calibrated live win-probability models absent from the data pack.

---

## 4. Performance Metrics & Statistical Adjustments

For every operationalised condition $c$ and batter $p$:

1. **Observed Clean Runs ($R_{p,c}$):** $\sum_{i \in \mathcal{D}_{p,c}} y_i$
2. **Expected Clean Runs ($\mathbb{E}[R]_{p,c}$):** $\sum_{i \in \mathcal{D}_{p,c}} \mathbb{E}[y_i \mid o_i, m_i]$
3. **Raw Runs Above Expected ($\text{Raw RAE}_{p,c}$):** $R_{p,c} - \mathbb{E}[R]_{p,c}$
4. **Per-Ball Rate Difference ($\Delta_{p,c}$):** $\frac{\text{Raw RAE}_{p,c}}{n_{p,c}}$
5. **Observed Strike Rate ($\text{SR}_{p,c}$):** $\frac{R_{p,c}}{n_{p,c}} \times 100$
6. **Expected Strike Rate ($\text{Exp SR}_{p,c}$):** $\frac{\mathbb{E}[R]_{p,c}}{n_{p,c}} \times 100$
7. **Positive Innings Percentage:** Percentage of qualifying match-innings where batter's $\text{Raw RAE} > 0$.
8. **DerSimonian–Laird (DL) Empirical Bayes Shrinkage:**
   $$\theta_{p,c}^* = (1 - B_{p,c}) \Delta_{p,c} + B_{p,c} \mu_{c}$$
   $$B_{p,c} = \frac{v_{p,c}}{v_{p,c} + \tau_c^2}, \quad v_{p,c} = \frac{\sigma_c^2}{n_{p,c}}$$
   $$\text{Shrunk RAE}_{p,c} = \theta_{p,c}^* \times n_{p,c}$$
9. **Cluster Bootstrap Uncertainty:** 1,000 match-cluster resamples with replacement to compute 95% confidence intervals $[\text{CI}_{\text{lower}}, \text{CI}_{\text{upper}}]$ accounting for within-match delivery correlation.
10. **Exposure Sensitivity Filtering:** Evaluating batter rankings across 5 thresholds: $n_{p,c} \ge 30, 50, 100, 200, 300$ clean balls.

---

## 5. Analytical Limitations & Governance Rules

1. **Condition Collinearity:** Several conditions exhibit high pairwise overlap (e.g., $C01$ and $C07$ share $J = 1.0$; $C31$ and $C32$ share $J = 0.44$). They cannot be treated as 40 independent statistical trials.
2. **Category B Target Approximation:** 2nd innings target is reconstructed as $\text{Total}_{\text{Inn 1}} + 1$. In rain-curtailed matches where official DLS targets were adjusted without revised over logs, minor target discrepancies may exist.
3. **Selection Bias & Role Specialization:** Top-order anchors (e.g., Kohli) face high exposure in Powerplay and early collapses but near-zero exposure in tail-end crises ($\ge 6$ wickets down). Conversely, finishers face high exposure in death overs but low exposure in early collapses. Comparisons must account for positional exposure.

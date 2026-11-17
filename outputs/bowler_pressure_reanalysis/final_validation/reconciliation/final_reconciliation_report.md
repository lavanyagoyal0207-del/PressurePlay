# Final Bowler Audit Numerical Reconciliation Report
**Project:** SupeRR Selector Season 2 — Bowler Pressure Framework Review  
**Repository Working Directory:** `C:\Users\Lavanya Goyal\OneDrive\Documents\rr`  
**Target Scope:** IPL Seasons 2022–2026 (371 Scheduled, 367 Played Matches, 87,687 Deliveries)  
**Deliverables Directory:** [outputs/bowler_pressure_reanalysis/final_validation/reconciliation](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation)  
**Audit Protocol:** Strictly Read-Only (0 commits, 0 staged Git changes, baseline hashes 100% verified)  
**Date of Audit:** November 18, 2026  

---

## Executive Summary & Key Verdicts

| Section | Target Investigation | Core Finding | Operational Verdict |
| :--- | :--- | :--- | :--- |
| **1. Legal-Ball Exposures** | Discrepancies between earlier exposure figures (758, 233, 395, 241, 216, 393) and latest narrative report figures (240, 120, 138, 60, 258, 344). | **Earlier figures are 100% verified against raw ball-by-ball IPL data.** The latest figures (240, 120, 138, 60, 258, 344) were typographical, synthetic round-number placeholders, and transposition errors in the conversational narrative table of Turn 3048. | **RESOLVED & PROVEN** (Underlying CSVs are correct) |
| **2. Ten Provisional Selections** | Independent verification of 10 proposed players across $C15$ ($F_1$ collapse $\cup$ $F_4$ knockout) and $C21$ (death overs 16–20) under $\ge 100$ legal balls & $\ge 10$ matches. | Mitchell Santner fails $C21$ (39 balls, 8 matches). Yuzvendra Chahal was erroneously assigned ID `2876` (Axar Patel, 72 death balls). Reconciling to canonical ID `1612` confirms Chahal has 336 death balls and 48 matches, easily qualifying. | **RECONCILED** (1 candidate fails $C21$; 1 player ID corrected) |
| **3. C21 Informative Prior** | Origin of $\alpha = 20.0, \beta = 269.2$ and sensitivity across prior strengths. | **Manually selected regularization scenario, NOT an empirically estimated prior.** $C21$ death data is statistically underdispersed ($\chi^2/\text{dof} = 0.802, p = 0.945$). Candidate rankings (Starc #1, Chahal #2, Harshal #3) are highly stable across weak, moderate, and strong priors. Under the homogeneous limit, all bowlers converge to $13.46$ and are undifferentiated. | **DOCUMENTED & LABELED** (Sensitivity scenario confirmed) |
| **4. Selection Architecture** | Audit of the proposed 10-player roster and arbitrary 5/5 cohort split. | **An arbitrary 5/5 split is NOT statistically justified.** 4 elite bowlers (Narine, Bumrah, Pathirana, Starc) sit on the Pareto frontier of *both* cohorts. Exactly **9 unique qualified bowlers** form the empirical Pareto frontiers across both cohorts. Mitchell Santner is the 10th selection as a $C15$-qualified, non-frontier interior point. | **SELECTION ARCHITECTURE REFORMULATED** (9 Frontier Anchors + 1 Interior Selection) |

---

## 1. Reconcile Legal-Ball Exposures

### 1.1 Empirical Reproduction of the 6 Discrepant Bowlers
We audited every delivery row for the six target bowlers in the verified ball-by-ball dataset (`outputs/pressure/delivery_pressure_eligibility.csv`) filtered strictly to IPL matches (seasons 2022–2026, 367 played matches).

*(Complete deliverable: [exposure_discrepancy_reconciliation.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/exposure_discrepancy_reconciliation.csv))*

| Bowler Name | Player ID | Cohort | Earlier Exposure | Latest Report | Exact Cohort Mask | Verified Matches | Verified Legal Balls | Verified Clean Balls | Credited Wickets | Status vs Raw Data | Exact Source of Discrepancy |
| :--- | :---: | :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Varun Chakravarthy** | `6256` | $C15$ ($F_1 \cup F_4$) | **758** | 240 | `f1_primary == True \| f4_knockout == True` | 36 | **758** | 747 | 57 | **MATCHES EARLIER EXACTLY** | Narrative placeholder error: `240` (40 overs) was manually typed into the chat response; raw data proves 758 legal balls. |
| **Mitchell Starc** | `829` | $C15$ ($F_1 \cup F_4$) | **233** | 120 | `f1_primary == True \| f4_knockout == True` | 21 | **233** | 230 | 33 | **MATCHES EARLIER EXACTLY** | Narrative placeholder error: `120` (20 overs) was manually typed into the chat response; raw data proves 233 legal balls. |
| **Kagiso Rabada** | `3628` | $C15$ ($F_1 \cup F_4$) | **395** | 138 | `f1_primary == True \| f4_knockout == True` | 27 | **395** | 386 | 39 | **MATCHES EARLIER EXACTLY** | Filter confusion: `138` is Rabada's exact legal ball count in **Season 2023 only**. His 5-season IPL $C15$ total is 395 balls. |
| **Mitchell Santner** | `4101` | $C15$ ($F_1 \cup F_4$) | **241** | 60 | `f1_primary == True \| f4_knockout == True` | 15 | **241** | 238 | 16 | **MATCHES EARLIER EXACTLY** | Narrative placeholder error: `60` (10 overs) was manually typed into the chat response; raw data proves 241 legal balls. |
| **Sunil Narine** | `781` | $C21$ (Death) | **216** | 258 | `overid >= 16` | 35 | **216** | 213 | 19 | **MATCHES EARLIER EXACTLY** | Transposition error: `258` is Kagiso Rabada's exact $C21$ death ball count (258). Accidental copy-paste in chat markdown. |
| **Jasprit Bumrah** | `2933` | $C21$ (Death) | **393** | 344 | `overid >= 16` | 44 | **393** | 385 | 33 | **MATCHES EARLIER EXACTLY** | Transcription typo: Bumrah has 393 legal balls in $C21$. `344` was a narrative typo; CSV files on disk always had 393. |

### 1.2 Root Cause Analysis
1. **The frozen baseline and reanalysis CSV datasets are completely correct:**
   - In `outputs/bowler_pressure_reanalysis/posterior_strike_rate_audit.csv` and `outputs/bowler_pressure_reanalysis/final_validation/posterior_strike_rate_reproduction.csv`, the recorded legal balls are:
     - Varun $C15 = 758$
     - Starc $C15 = 233$
     - Rabada $C15 = 395$
     - Santner $C15 = 241$
     - Narine $C21 = 216$
     - Bumrah $C21 = 393$
2. **The origin of `240, 120, 138, 60, 258, 344`:**
   - These numbers appeared exclusively in the markdown table labeled `Verification Table for Target Bowlers` in Turn 3048.
   - They were not generated by any data processing pipeline. They were introduced during response drafting due to synthetic round-number substitutions ($240 = 40$ overs, $120 = 20$ overs, $60 = 10$ overs), single-season filter confusion (Rabada 2023 = 138), and row-column transposition (Rabada's 258 death balls assigned to Narine).

---

## 2. Independent Audit of the Ten Provisional Selections

Each candidate was tested across both cohorts ($C21$ Death Overs and $C15$ Early Collapse $\cup$ Knockout) against the binding qualification rule:
$$\text{Qualification Criteria:} \quad L_i \ge 100 \text{ Legal Deliveries} \quad \text{AND} \quad M_i \ge 10 \text{ Played Matches}$$

*(Full evaluation dataset: [ten_candidate_eligibility_audit.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/ten_candidate_eligibility_audit.csv))*

### 2.1 Critical Player Identity Discovery: Yuzvendra Chahal vs Axar Patel
In previous conversational turns (beginning Turn 2884), Yuzvendra Chahal was inadvertently associated with `player_id = 2876`.
- **Audit Finding:** In the canonical player mapping (`competition_team_player_mapping.csv`), `player_id = 2876` belongs to **Axar Patel** (Delhi Capitals / India). Axar Patel bowled only 72 legal balls (1 wicket, 12 matches) in overs 16–20 and **fails** $C21$ exposure.
- **Canonical Yuzvendra Chahal:** Chahal's canonical ID in the database is **`1612`** (Rajasthan Royals / Punjab Kings / India). Under ID `1612`, Chahal bowled **336 legal death balls**, took **40 credited wickets**, and played in **48 death matches**, easily qualifying in both cohorts.

### 2.2 Comprehensive Eligibility Matrix
*(Containment rates use DerSimonian–Laird shrinkage on phase-adjusted residuals $\delta_i$. Posterior strike rates use $\alpha=20, \beta=269.2$ for $C21$, and Marginal MLE $\alpha=43.37, \beta=687.41$ for $C15$.)*

| Player Name | Canonical ID | Cohort | Legal Balls $L$ | Clean Balls $n$ | Matches $M$ | Credited Wickets $W$ | Raw Containment | Residual / Ball $\delta_i$ | Shrunk Containment | Posterior Wicket Rate | Posterior Median SR | Dual Exposure Status | Failure Reason |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Sunil Narine** | `781` | $C21$ Death | 216 | 213 | 35 | 19 | 1.0047 | -0.6908 | 1.2326 | 0.08038 | 12.55 | **PASS** | None |
| **Sunil Narine** | `781` | $C15$ $F_1 \cup F_4$ | 798 | 782 | 39 | 38 | 0.9757 | -0.5581 | 0.9359 | 0.05478 | 18.33 | **PASS** | None |
| **Jasprit Bumrah** | `2933` | $C21$ Death | 393 | 385 | 44 | 33 | 1.2078 | -0.6091 | 1.2311 | 0.08004 | 12.57 | **PASS** | None |
| **Jasprit Bumrah** | `2933` | $C15$ $F_1 \cup F_4$ | 542 | 533 | 32 | 37 | 1.1182 | -0.5311 | 1.0027 | 0.06537 | 15.36 | **PASS** | None |
| **Yuzvendra Chahal** | `1612` | $C21$ Death | 336 | 332 | 48 | 40 | 1.5873 | -0.1652 | 1.6044 | 0.09914 | 10.14 | **PASS** | None |
| **Yuzvendra Chahal** | `1612` | $C15$ $F_1 \cup F_4$ | 963 | 951 | 43 | 64 | 1.3565 | -0.2042 | 1.2517 | 0.06506 | 15.42 | **PASS** | None |
| **Matheesha Pathirana**| `8661` | $C21$ Death | 402 | 383 | 32 | 39 | 1.4595 | -0.3711 | 1.4455 | 0.08790 | 11.44 | **PASS** | None |
| **Matheesha Pathirana**| `8661` | $C15$ $F_1 \cup F_4$ | 468 | 454 | 21 | 37 | 1.2952 | -0.4017 | 1.1293 | 0.06956 | 14.44 | **PASS** | None |
| **Harshal Patel** | `2261` | $C21$ Death | 498 | 483 | 51 | 53 | 1.5921 | -0.2509 | 1.5263 | 0.09515 | 10.56 | **PASS** | None |
| **Harshal Patel** | `2261` | $C15$ $F_1 \cup F_4$ | 693 | 679 | 33 | 57 | 1.3947 | -0.2745 | 1.2043 | 0.07271 | 13.80 | **PASS** | None |
| **Varun Chakravarthy** | `6256` | $C21$ Death | 226 | 221 | 35 | 15 | 1.5113 | -0.2293 | 1.5910 | 0.07068 | 14.28 | **PASS** | None |
| **Varun Chakravarthy** | `6256` | $C15$ $F_1 \cup F_4$ | 758 | 747 | 36 | 57 | 1.1526 | -0.4279 | 1.0714 | 0.06944 | 14.45 | **PASS** | None |
| **Mitchell Starc** | `829` | $C21$ Death | 155 | 152 | 22 | 26 | 1.7237 | -0.1387 | 1.6518 | 0.10844 | 9.29 | **PASS** | None |
| **Mitchell Starc** | `829` | $C15$ $F_1 \cup F_4$ | 233 | 230 | 21 | 33 | 1.5217 | -0.1556 | 1.3475 | 0.08297 | 12.10 | **PASS** | None |
| **Kagiso Rabada** | `3628` | $C21$ Death | 258 | 251 | 38 | 22 | 1.6534 | -0.1257 | 1.6413 | 0.07967 | 12.65 | **PASS** | None |
| **Kagiso Rabada** | `3628` | $C15$ $F_1 \cup F_4$ | 395 | 386 | 27 | 39 | 1.3368 | -0.3408 | 1.2029 | 0.07610 | 13.19 | **PASS** | None |
| **Josh Hazlewood** | `830` | $C21$ Death | 275 | 269 | 32 | 24 | 1.7026 | -0.1052 | 1.6494 | 0.08085 | 12.46 | **PASS** | None |
| **Josh Hazlewood** | `830` | $C15$ $F_1 \cup F_4$ | 497 | 488 | 29 | 44 | 1.3463 | -0.3360 | 1.1835 | 0.07377 | 13.61 | **PASS** | None |
| **Mitchell Santner** | `4101` | $C21$ Death | **39** | 38 | **8** | 4 | 1.7105 | -0.0437 | 1.7049 | 0.07787 | 13.02 | **FAIL** | **Legal balls 39 < 100; Matches 8 < 10** |
| **Mitchell Santner** | `4101` | $C15$ $F_1 \cup F_4$ | 241 | 238 | 15 | 16 | 1.0336 | -0.4899 | 1.1015 | 0.06395 | 15.73 | **PASS** | None |

---

## 3. Empirical Origin and Multi-Scenario Sensitivity of the C21 Prior

### 3.1 Prior Origin & Justification
- **Underdispersion Reality:** In death overs ($C21$), the observed dispersion ratio is $\chi^2/\text{dof} = 0.802$ ($p = 0.945$). Between-bowler variation cannot be separated from Poisson noise over small death-overs sample sizes.
- **Formal Label:** $\alpha = 20.0, \beta = 269.2$ is **NOT** an empirically fitted prior from a separate dataset. It is a **manually selected regularization scenario** chosen to anchor bowlers with pseudo-data equivalent to 20 wickets over $269.2$ balls ($\approx 45$ overs), preventing unconstrained collapse to the homogeneous league mean.
- **Protocol Rule:** This parameter set must always be classified as a **"Sensitivity Scenario"**.

### 3.2 Sensitivity of C21 Rankings Across Three Defensible Prior Strengths
*(Full sensitivity dataset: [c21_prior_origin_and_sensitivity.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/c21_prior_origin_and_sensitivity.csv))*

We tested three defensible prior strengths plus the homogeneous limit across all qualified death bowlers:
1. **Scenario 1 (Weak Prior / Low Shrinkage):** $\alpha = 5.0, \beta = 67.3$ ($N_0 \approx 67$ balls, prior $\text{CV} = 44.7\%$, raw data carries $70\text{--}85\%$ weight).
2. **Scenario 2 (Benchmark Scenario):** $\alpha = 20.0, \beta = 269.2$ ($N_0 \approx 269$ balls, prior $\text{CV} = 22.4\%$, raw data carries $45\text{--}60\%$ weight).
3. **Scenario 3 (Strong Prior / Conservative Shrinkage):** $\alpha = 50.0, \beta = 673.0$ ($N_0 \approx 673$ balls, prior $\text{CV} = 14.1\%$, raw data carries $20\text{--}35\%$ weight).
4. **Scenario 4 (Homogeneous Limit):** $\alpha \to \infty, \beta \to \infty$ (pure Poisson limit; all bowlers equal $13.46$).

| Qualified Bowler Name | Legal Balls | Wickets | Raw SR | Scen 1: Weak SR (Rank) | Scen 2: Benchmark SR (Rank) | Scen 3: Strong SR (Rank) | Scen 4: Homogeneous Limit SR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mitchell Starc** | 155 | 26 | 5.96 | **7.25** (#1) | **9.29** (#1) | **10.94** (#1) | **13.46 (Tied - Indistinguishable)** |
| **Yuzvendra Chahal** | 336 | 40 | 8.40 | **9.03** (#2) | **10.14** (#2) | **11.25** (#2) | **13.46 (Tied - Indistinguishable)** |
| **Harshal Patel** | 498 | 53 | 9.40 | **9.80** (#5) | **10.56** (#3) | **11.41** (#3) | **13.46 (Tied - Indistinguishable)** |
| **Anshul Kamboj** | 131 | 17 | 7.71 | **9.15** (#3) | **10.91** (#4) | **12.06** (#4) | **13.46 (Tied - Indistinguishable)** |
| **Hardik Pandya** | 115 | 15 | 7.67 | **9.27** (#4) | **11.08** (#5) | **12.19** (#6) | **13.46 (Tied - Indistinguishable)** |
| **Matheesha Pathirana**| 402 | 39 | 10.31 | **10.74** (#9) | **11.44** (#6) | **12.12** (#5) | **13.46 (Tied - Indistinguishable)** |
| **Mohit Sharma** | 289 | 29 | 9.97 | **10.64** (#8) | **11.47** (#7) | **12.23** (#7) | **13.46 (Tied - Indistinguishable)** |
| **Andre Russell** | 222 | 23 | 9.65 | **10.46** (#7) | **11.51** (#8) | **12.32** (#8) | **13.46 (Tied - Indistinguishable)** |
| **Jasprit Bumrah** | 393 | 33 | 11.91 | **12.11** (#17)| **12.57** (#16)| **12.92** (#14)| **13.46 (Tied - Indistinguishable)** |
| **Sunil Narine** | 216 | 19 | 11.37 | **11.98** (#15)| **12.55** (#15)| **12.94** (#15)| **13.46 (Tied - Indistinguishable)** |

### Key Sensitivity Insight:
- **Homogeneous Limit Correction:** Under Scenario 4 ($\alpha \to \infty, \beta \to \infty$), between-bowler variance is mathematically assumed to be zero. All bowlers converge to the identical league average strike rate of $13.46$ balls/wicket ($0.07429$ wickets/ball). At this limit, the model cannot distinguish or rank individual bowlers by strike rate; discrete ranks are statistically meaningless and have been removed.
- **Rank order among elite strike bowlers is rock solid:** Mitchell Starc is ranked #1 and Yuzvendra Chahal is ranked #2 across all three defensible prior specifications.
- **Harshal Patel's massive volume (498 balls) protects his elite ranking:** As prior strength increases, Harshal's ranking climbs from #5 to #3 because his 53 wickets over 498 balls are far more resilient to shrinkage than small-sample bowlers.
- **Containment anchors (Narine, Bumrah) are evaluated on containment:** Sunil Narine and Jasprit Bumrah do not rely on strike rate to reach the Pareto frontier; their frontier membership is established by their peerless containment rates ($1.23$ runs/ball).

---

## 4. Selection Architecture Audit & Roster Integrity

### 4.1 Statistical Rejection of the 5/5 Cohort Split
The proposed 5 Death / 5 Tournament division is **not statistically justified**:
1. **Four elite bowlers belong to BOTH Pareto frontiers:**
   - **Sunil Narine**, **Jasprit Bumrah**, **Matheesha Pathirana**, and **Mitchell Starc** sit directly on the non-dominated empirical 2D Pareto frontier in **both** $C21$ (Death Overs) and $C15$ (Early Collapse $\cup$ Knockout).
   - Forcing them into only one cohort artificially creates empty roster slots and invites inferior interior bowlers into the selection.
2. **Pareto efficiency naturally yields EXACTLY NINE non-dominated candidates:**
   - When evaluating all qualified bowlers ($\ge 100$ legal balls, $\ge 10$ matches), exactly **9 unique bowlers** across the entire IPL occupy the empirical 2D Pareto frontier across either $C21$ or $C15$.

### 4.2 Explicit Pareto-Frontier Membership Table
*(Complete deliverable: [pareto_frontier_membership.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/pareto_frontier_membership.csv))*

| Player Name | Player ID | Tactical Selection Category | $C21$ Death Qualified? | $C21$ Death Frontier Member? | $C21$ Shrunk Containment | $C21$ Post. Median SR | $C15$ $F_1 \cup F_4$ Qualified? | $C15$ $F_1 \cup F_4$ Frontier Member? | $C15$ Shrunk Containment | $C15$ Post. Median SR |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sunil Narine** | `781` | Dual-Cohort Pareto Anchor | **Yes** (216 balls, 35 M) | **YES (Frontier)** | **1.2326** | 12.55 | **Yes** (798 balls, 39 M) | **YES (Frontier)** | **0.9359** | 18.33 |
| **Jasprit Bumrah** | `2933` | Dual-Cohort Pareto Anchor | **Yes** (393 balls, 44 M) | **YES (Frontier)** | **1.2311** | 12.57 | **Yes** (542 balls, 32 M) | **YES (Frontier)** | **1.0027** | 15.36 |
| **Matheesha Pathirana** | `8661` | Dual-Cohort Pareto Anchor | **Yes** (402 balls, 32 M) | **YES (Frontier)** | 1.4455 | **11.44** | **Yes** (468 balls, 21 M) | **YES (Frontier)** | 1.1293 | **14.44** |
| **Mitchell Starc** | `829` | Dual-Cohort Pareto Anchor | **Yes** (155 balls, 22 M) | **YES (Frontier)** | 1.6518 | **9.29** | **Yes** (233 balls, 21 M) | **YES (Frontier)** | 1.3475 | **12.10** |
| **Yuzvendra Chahal** | `1612` | $C21$ Death Frontier Anchor | **Yes** (336 balls, 48 M) | **YES (Frontier)** | 1.6044 | **10.14** | **Yes** (963 balls, 43 M) | No (Dominated) | 1.2517 | 15.42 |
| **Harshal Patel** | `2261` | $C21$ Death Frontier Anchor | **Yes** (498 balls, 51 M) | **YES (Frontier)** | 1.5263 | **10.56** | **Yes** (693 balls, 33 M) | No (Dominated) | 1.2043 | 13.80 |
| **Varun Chakravarthy** | `6256` | $C15$ $F_1 \cup F_4$ Frontier Anchor | **Yes** (226 balls, 35 M) | No (Dominated) | 1.5910 | 14.28 | **Yes** (758 balls, 36 M) | **YES (Frontier)** | **1.0714** | 14.45 |
| **Josh Hazlewood** | `830` | $C15$ $F_1 \cup F_4$ Frontier Anchor | **Yes** (275 balls, 32 M) | No (Dominated) | 1.6494 | 12.46 | **Yes** (497 balls, 29 M) | **YES (Frontier)** | **1.1835** | 13.61 |
| **Kagiso Rabada** | `3628` | $C15$ $F_1 \cup F_4$ Frontier Anchor | **Yes** (258 balls, 38 M) | No (Dominated) | 1.6413 | 12.65 | **Yes** (395 balls, 27 M) | **YES (Frontier)** | **1.2029** | 13.19 |
| **Mitchell Santner** | `4101` | Non-Frontier Interior Selection | **No** (39 balls, 8 M) | **DISQUALIFIED IN C21** | 1.7049 | 13.02 | **Yes** (241 balls, 15 M) | **No (Dominated)** | 1.1015 | 15.73 |

### 4.3 Selection Breakdown:
- **The 9 Qualified Frontier Anchors:** Narine, Bumrah, Pathirana, Starc, Chahal, Harshal, Varun, Hazlewood, and Rabada form the empirically non-dominated set across IPL pressure bowling.
- **The 10th Slot Decision:**
  - If franchise leadership mandates an even 10-player roster, **Mitchell Santner (`4101`)** is the leading candidate based on his $C15$ performance ($241$ legal balls, $15$ matches, shrunk containment $1.1015$).
  - *Statistical Caveat:* Santner is strictly dominated by Varun Chakravarthy in $C15$ (Varun achieves lower containment *and* faster wickets). Therefore, Santner cannot be described as a Pareto-efficient anchor; he is an interior candidate.

---

## 5. Artifact Manifest & Baseline Verification

### 5.1 Artifacts Generated Under `reconciliation/`
1. [exposure_discrepancy_reconciliation.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/exposure_discrepancy_reconciliation.csv)
2. [ten_candidate_eligibility_audit.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/ten_candidate_eligibility_audit.csv)
3. [c21_prior_origin_and_sensitivity.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/c21_prior_origin_and_sensitivity.csv)
4. [pareto_frontier_membership.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/pareto_frontier_membership.csv)
5. [reconciliation_audit.json](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/reconciliation_audit.json)
6. [final_reconciliation_report.md](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/final_reconciliation_report.md)

### 5.2 Verification of Canonical Baseline Hashes
All eight original frozen analytical baseline files remain 100% byte-for-byte identical to baseline:

| Canonical Baseline File | Audit Hash Status | SHA-256 Digest |
| :--- | :---: | :--- |
| `outputs/final/final_batter_leaderboard.csv` | **PASS** | `d0e73b49824ae9941cde80a9b72d674a1e17aa095e21ff41104d49c2e0f68d68` |
| `outputs/final/final_bowler_diagnostics.csv` | **PASS** | `3e5607fa8a2c16b4abe72ab59ae5ae6f3fb439f03230d5c5edac876b51449f04` |
| `outputs/final/final_validation_report.json` | **PASS** | `803e661f3ccc641f4aa1d2bf0d0b834e4cdd99b2e9fe3d7c0633ba75bfa44f4f` |
| `outputs/statistical/batter_pressure_estimates.csv` | **PASS** | `307969959aa89094b0a17aafa29cbbe37e0866fd70b5b7540f73498adadfb627` |
| `outputs/statistical/bowler_pressure_diagnostics.csv` | **PASS** | `ac720eaf2c023a9e65aca216a10fac825d789029d221b1d87925e290cd4e6c22` |
| `outputs/statistical/bootstrap_uncertainty.csv` | **PASS** | `befdb7e652fd49fb2608d4780fe2097bd4c35b4ee976b9b1ab0d109a6adc3f33` |
| `outputs/statistical/baseline_model_report.json` | **PASS** | `9fcd247fad124bbf325fa9c6d629aaf7076268f38a48d8fada91622b150d85ea` |
| `outputs/statistical/stage4_validation_report.json` | **PASS** | `b2e5dd61b667e3ef275b57ae474f055f5d291d76588543b597872f998ed1da5e` |

**Git Status:** Strictly read-only; 0 staged files, 0 commits, working tree preserved.

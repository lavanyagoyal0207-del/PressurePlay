# Final Bowler Top 10: Validated Pressure Performance Roster
**Project:** SupeRR Selector Season 2 — Bowler Pressure Framework Finalization  
**Repository Working Directory:** `C:\Users\Lavanya Goyal\OneDrive\Documents\rr`  
**Dataset Scope:** IPL Seasons 2022–2026 (371 Scheduled Matches, 367 Played Matches, 87,687 Deliveries)  
**Deliverable Document:** [outputs/final/final_bowler_top10.md](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/final/final_bowler_top10.md)  
**Supporting Reconciliation Directory:** [outputs/bowler_pressure_reanalysis/final_validation/reconciliation](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation)  
**Status:** Finalized & Validated  

---

## Executive Overview & Final Selection Architecture

This document presents the finalized Top 10 IPL Bowler Pressure Roster for SupeRR Selector Season 2. Bowler performance under pressure is evaluated across two formally defined analytical pressure cohorts:
1. **$C21$ — Death Overs:** Deliveries in overs 16–20 across all match situations.
2. **$C15$ — Early Collapse $\cup$ Knockout Matches:** The union of deliveries bowled during early-wicket collapses ($F_1$: 2+ wickets down in overs 0–5) and all playoff/knockout match deliveries ($F_4$: Qualifiers, Eliminators, and Finals).

### Strict Qualification & Pareto Selection Rules:
- **Binding Dual Exposure Threshold:** A bowler must have delivered at least **100 legal balls** and participated in at least **10 matches** within the specific cohort to be eligible.
- **No Forced 5/5 Cohort Split:** Rather than arbitrarily forcing five death bowlers and five collapse/playoff bowlers, bowlers are categorized according to their empirical Pareto-frontier membership.
- **Exact Frontier Accounting:** Exactly **nine unique bowlers** across the IPL occupy the empirical 2D Pareto frontier across either $C21$ or $C15$. Four of these premier bowlers sit on the Pareto frontier of *both* cohorts simultaneously.
- **The Tenth Selection:** **Mitchell Santner** is included as the tenth bowler. He is explicitly classified as a **$C15$-qualified, non-frontier selection (interior point)**. He is **not** Pareto-efficient (he is strictly dominated in $C15$ by Varun Chakravarthy and Jasprit Bumrah), but provides specialized left-arm spin containment.

---

## 1. Verified Pareto-Frontier Membership Matrix

All figures below are independently verified against the raw ball-by-ball dataset and match the analytical outputs in [pareto_frontier_membership.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/pareto_frontier_membership.csv) and [ten_candidate_eligibility_audit.csv](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/bowler_pressure_reanalysis/final_validation/reconciliation/ten_candidate_eligibility_audit.csv).

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

---

## 2. The Finalized Bowler Top 10 Profiles

### Category 1: Dual-Cohort Pareto Frontier Anchors (4 Bowlers)
These four bowlers achieve non-dominated Pareto efficiency in **both** death overs ($C21$) and early collapse/knockout matches ($C15$).

#### 1. Sunil Narine (`player_id: 781`)
- **Tactical Profile:** Global Pressure Containment Anchor (Off-Spin).
- **$C21$ Death Overs:** 216 legal balls, 213 clean balls, 35 matches, 19 credited wickets. Raw containment: $1.0047$. Shrunk containment: **$1.2326$ runs/ball** (Rank #2). Posterior median SR: **$12.55$ balls/wkt**.
- **$C15$ Collapse $\cup$ Knockout:** 798 legal balls, 782 clean balls, 39 matches, 38 credited wickets. Raw containment: $0.9757$. Shrunk containment: **$0.9359$ runs/ball** (Rank #1 in IPL). Posterior median SR: **$18.33$ balls/wkt**.
- **Selection Rationale:** Unrivaled containment anchor across all phases of IPL pressure. Holds the lowest shrunk containment rate in $C15$ ($0.9359$) and second-lowest in $C21$ ($1.2326$). Essential defensive core.

#### 2. Jasprit Bumrah (`player_id: 2933`)
- **Tactical Profile:** Dual-Threat Pace Anchor (Right-Arm Fast).
- **$C21$ Death Overs:** 393 legal balls, 385 clean balls, 44 matches, 33 credited wickets. Raw containment: $1.2078$. Shrunk containment: **$1.2311$ runs/ball** (Rank #1 in IPL). Posterior median SR: **$12.57$ balls/wkt**.
- **$C15$ Collapse $\cup$ Knockout:** 542 legal balls, 533 clean balls, 32 matches, 37 credited wickets. Raw containment: $1.1182$. Shrunk containment: **$1.0027$ runs/ball** (Rank #2 in IPL). Posterior median SR: **$15.36$ balls/wkt**.
- **Selection Rationale:** The premier dual-threat fast bowler in the tournament. Combines the lowest death-overs containment rate among fast bowlers with heavy wicket volume (70 pressure wickets across both cohorts).

#### 3. Matheesha Pathirana (`player_id: 8661`)
- **Tactical Profile:** Specialized Death & Pressure Strike Slinger (Right-Arm Fast).
- **$C21$ Death Overs:** 402 legal balls, 383 clean balls, 32 matches, 39 credited wickets. Raw containment: $1.4595$. Shrunk containment: **$1.4455$ runs/ball**. Posterior median SR: **$11.44$ balls/wkt** (Rank #6).
- **$C15$ Collapse $\cup$ Knockout:** 468 legal balls, 454 clean balls, 21 matches, 37 credited wickets. Raw containment: $1.2952$. Shrunk containment: **$1.1293$ runs/ball**. Posterior median SR: **$14.44$ balls/wkt**.
- **Selection Rationale:** Non-dominated on both frontiers. Bridges the gap between extreme containment and rapid strike rate, maintaining sub-$1.45$ death containment while striking every $11.44$ balls.

#### 4. Mitchell Starc (`player_id: 829`)
- **Tactical Profile:** Maximum Pressure Strike Weapon (Left-Arm Fast).
- **$C21$ Death Overs:** 155 legal balls, 152 clean balls, 22 matches, 26 credited wickets. Raw containment: $1.7237$. Shrunk containment: **$1.6518$ runs/ball**. Posterior median SR: **$9.29$ balls/wkt** (Rank #1 in IPL).
- **$C15$ Collapse $\cup$ Knockout:** 233 legal balls, 230 clean balls, 21 matches, 33 credited wickets. Raw containment: $1.5217$. Shrunk containment: **$1.3475$ runs/ball**. Posterior median SR: **$12.10$ balls/wkt** (Rank #1 in IPL).
- **Selection Rationale:** Undisputed #1 strike rate in the IPL across both pressure cohorts. Takes a wicket every $9.29$ balls at the death and every $12.10$ balls in playoff/collapse situations. Maximum attacking potency.

---

### Category 2: Cohort-Specific Pareto Frontier Anchors (5 Bowlers)
These five bowlers achieve non-dominated Pareto efficiency in exactly one cohort, serving specialized tactical roles.

#### 5. Yuzvendra Chahal (`player_id: 1612`)
- **Tactical Profile:** Death Overs Attacking Leg-Spinner ($C21$ Frontier Anchor).
- **$C21$ Death Overs:** 336 legal balls, 332 clean balls, 48 matches, 40 credited wickets. Raw containment: $1.5873$. Shrunk containment: **$1.6044$ runs/ball**. Posterior median SR: **$10.14$ balls/wkt** (Rank #2 in IPL).
- **$C15$ Collapse $\cup$ Knockout:** 963 legal balls, 951 clean balls, 43 matches, 64 credited wickets. Shrunk containment: $1.2517$. Posterior median SR: $15.42$ (Dominated in $C15$ by Hazlewood and Rabada).
- **Selection Rationale:** Reconciled from canonical database ID `1612`. The most lethal spin weapon at the death, capturing 40 death wickets at a posterior median strike rate of $10.14$ balls/wicket.

#### 6. Harshal Patel (`player_id: 2261`)
- **Tactical Profile:** High-Volume Death Overs Closer ($C21$ Frontier Anchor).
- **$C21$ Death Overs:** 498 legal balls, 483 clean balls, 51 matches, 53 credited wickets. Raw containment: $1.5921$. Shrunk containment: **$1.5263$ runs/ball**. Posterior median SR: **$10.56$ balls/wkt** (Rank #3 in IPL).
- **$C15$ Collapse $\cup$ Knockout:** 693 legal balls, 679 clean balls, 33 matches, 57 credited wickets. Shrunk containment: $1.2043$. Posterior median SR: $13.80$ (Dominated in $C15$ by Rabada).
- **Selection Rationale:** Holds the highest death-overs wicket tally in the entire IPL (53 death wickets over 51 matches). Combines heavy exposure with an elite strike rate ($10.56$), forming an indispensable volume pillar on the $C21$ frontier.

#### 7. Varun Chakravarthy (`player_id: 6256`)
- **Tactical Profile:** Collapse & Knockout Control Spinner ($C15$ Frontier Anchor).
- **$C15$ Collapse $\cup$ Knockout:** 758 legal balls, 747 clean balls, 36 matches, 57 credited wickets. Raw containment: $1.1526$. Shrunk containment: **$1.0714$ runs/ball** (Rank #3 in IPL). Posterior median SR: **$14.45$ balls/wkt**.
- **$C21$ Death Overs:** 226 legal balls, 221 clean balls, 35 matches, 15 credited wickets. Shrunk containment: $1.5910$. Posterior median SR: $14.28$ (Dominated in $C21$ by Narine and Bhuvneshwar Kumar).
- **Selection Rationale:** The premier middle-overs pressure controller in $C15$. Ranks #3 in tournament collapse containment ($1.0714$) while taking 57 wickets in 758 balls.

#### 8. Josh Hazlewood (`player_id: 830`)
- **Tactical Profile:** Disciplined Length Enforcer ($C15$ Frontier Anchor).
- **$C15$ Collapse $\cup$ Knockout:** 497 legal balls, 488 clean balls, 29 matches, 44 credited wickets. Raw containment: $1.3463$. Shrunk containment: **$1.1835$ runs/ball**. Posterior median SR: **$13.61$ balls/wkt**.
- **$C21$ Death Overs:** 275 legal balls, 269 clean balls, 32 matches, 24 credited wickets. Shrunk containment: $1.6494$. Posterior median SR: $12.46$ (Dominated in $C21$ by Harshal and Chahal).
- **Selection Rationale:** Established member of the $C15$ Pareto frontier. Provides consistent line-and-length control with a $1.1835$ containment rate and a solid $13.61$ strike rate across 29 high-pressure matches.

#### 9. Kagiso Rabada (`player_id: 3628`)
- **Tactical Profile:** High-Pace Knockout Enforcer ($C15$ Frontier Anchor).
- **$C15$ Collapse $\cup$ Knockout:** 395 legal balls, 386 clean balls, 27 matches, 39 credited wickets. Raw containment: $1.3368$. Shrunk containment: **$1.2029$ runs/ball**. Posterior median SR: **$13.19$ balls/wkt**.
- **$C21$ Death Overs:** 258 legal balls, 251 clean balls, 38 matches, 22 credited wickets. Shrunk containment: $1.6413$. Posterior median SR: $12.65$ (Dominated in $C21$ by Narine and Chahal).
- **Selection Rationale:** High-impact strike enforcer on the $C15$ frontier. Offers superior wicket-taking speed ($13.19$) compared to Hazlewood while conceding only $1.2029$ runs/ball over 395 pressure deliveries.

---

### Category 3: Qualified Non-Frontier Selection (The 10th Bowler)

#### 10. Mitchell Santner (`player_id: 4101`)
- **Tactical Profile:** Left-Arm Orthodox Containment Specialist ($C15$-Qualified Interior Point).
- **$C15$ Collapse $\cup$ Knockout:** 241 legal balls, 238 clean balls, 15 matches, 16 credited wickets. Raw containment: $1.0336$. Shrunk containment: **$1.1015$ runs/ball**. Posterior median SR: **$15.73$ balls/wkt**.
- **$C21$ Death Overs:** **NOT QUALIFIED** (39 legal balls, 8 matches; fails binding rule $L \ge 100, M \ge 10$).
- **Pareto Efficiency Status:** **NOT PARETO-EFFICIENT (INTERIOR POINT).**
  - In $C15$, Santner is strictly dominated by:
    - **Varun Chakravarthy:** Lower containment ($1.0714 < 1.1015$) AND faster strike rate ($14.45 < 15.73$).
    - **Jasprit Bumrah:** Lower containment ($1.0027 < 1.1015$) AND faster strike rate ($15.36 < 15.73$).
- **Selection Trade-Off & Transparent Justification:**
  - Santner is selected as the 10th bowler solely because of his qualified $C15$ exposure ($241$ balls) and excellent raw containment ($1.0336$).
  - However, team leadership must understand the analytical trade-off: **Santner does not add new Pareto value to the roster**. Every dimension of his performance is surpassed by Varun Chakravarthy. He provides tactical left-arm spin depth, but he cannot be justified as an optimal multi-dimensional anchor.

---

## 3. Methodological Summary & Limitations

A concise companion document has been authored in [outputs/final/final_bowler_methodology_limitations.md](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/final/final_bowler_methodology_limitations.md).

### Key Methodological Highlights:
1. **Wicket Rate Regularization:**
   - **$C15$ ($F_1 \cup F_4$):** Overdispersion is confirmed ($\chi^2/\text{dof} = 1.266, p = 0.0105$). Parameters are estimated via Marginal Negative Binomial Maximum Likelihood Estimation ($\hat{\alpha} = 43.37, \hat{\beta} = 687.41$), providing well-calibrated shrinkage ($17.9\%$ sample weight for a 150-ball bowler).
   - **$C21$ (Death Overs):** Data is statistically underdispersed ($\chi^2/\text{dof} = 0.802, p = 0.945$). Unconstrained MLE collapses to pure Poisson homogeneity. Parameters $\alpha = 20.0, \beta = 269.2$ are adopted as an **informative sensitivity scenario** (equivalent to 20 pseudo-wickets over $269.2$ balls), preventing artificial collapse while regularizing noise.
2. **Phase-Adjusted Containment:**
   - Evaluates residuals per clean ball ($\delta_i = (R_i - E[R_i])/n_i$) against Model 2 over $\times$ innings expectations.
   - Applies DerSimonian–Laird shrinkage toward zero: $\tau_\delta^2 = 0.020664$ ($C21$) and $\tau_\delta^2 = 0.016506$ ($C15$).
3. **Core Limitations:**
   - **Non-Causal Metric:** Residuals are phase-adjusted observational metrics, not causal runs saved (no adjustment for batter quality matchup, ground dimensions, or match situation).
   - **Exclusion of Penalties:** Due to unrecorded penalty runs on extras, containment is computed on clean balls off the bat only.
   - **Dual Exposure Requirement:** Results are sensitive to exposure cutoffs; bowlers with $< 100$ balls or $< 10$ matches (e.g., Santner in $C21$, McCoy, Hosein) cannot be evaluated reliably.

---

## 4. Frozen Baseline Verification

All eight canonical baseline files were verified via SHA-256 immediately prior to finalizing:

| Canonical Baseline File | Pre-Commit SHA-256 Check | Expected Baseline Hash |
| :--- | :---: | :--- |
| `outputs/final/final_batter_leaderboard.csv` | **MATCH** | `d0e73b49824ae9941cde80a9b72d674a1e17aa095e21ff41104d49c2e0f68d68` |
| `outputs/final/final_bowler_diagnostics.csv` | **MATCH** | `3e5607fa8a2c16b4abe72ab59ae5ae6f3fb439f03230d5c5edac876b51449f04` |
| `outputs/final/final_validation_report.json` | **MATCH** | `803e661f3ccc641f4aa1d2bf0d0b834e4cdd99b2e9fe3d7c0633ba75bfa44f4f` |
| `outputs/statistical/batter_pressure_estimates.csv` | **MATCH** | `307969959aa89094b0a17aafa29cbbe37e0866fd70b5b7540f73498adadfb627` |
| `outputs/statistical/bowler_pressure_diagnostics.csv` | **MATCH** | `ac720eaf2c023a9e65aca216a10fac825d789029d221b1d87925e290cd4e6c22` |
| `outputs/statistical/bootstrap_uncertainty.csv` | **MATCH** | `befdb7e652fd49fb2608d4780fe2097bd4c35b4ee976b9b1ab0d109a6adc3f33` |
| `outputs/statistical/baseline_model_report.json` | **MATCH** | `9fcd247fad124bbf325fa9c6d629aaf7076268f38a48d8fada91622b150d85ea` |
| `outputs/statistical/stage4_validation_report.json` | **MATCH** | `b2e5dd61b667e3ef275b57ae474f055f5d291d76588543b597872f998ed1da5e` |

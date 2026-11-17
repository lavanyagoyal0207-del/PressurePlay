# Independent Statistical Consistency Audit: Bowler Pressure Framework
**Project:** SupeRR Selector Season 2 — Comprehensive Methodology Review  
**Target Repository:** `C:\Users\Lavanya Goyal\OneDrive\Documents\rr`  
**Analytical Scope:** IPL Seasons 2022–2026 (367 Played Matches, 87,687 Delivery Records)  
**Execution Context:** Strictly Read-Only Audit & In-Depth Statistical Diagnostic  
**Date of Audit:** November 17, 2026  

---

## Executive Summary & Core Diagnostic Findings

| Audit Component | Diagnostic Finding | Statistical Status | Recommendation |
| :--- | :--- | :--- | :--- |
| **1. Wicket Model (Gamma-Poisson)** | In $C21$ (Death Overs), observed wicket dispersion ($\chi^2/\text{dof} = 0.802, p = 0.945$) is **underdispersed** relative to Poisson. In $C15$ ($F_1 \cup F_4$), genuine overdispersion exists ($\chi^2/\text{dof} = 1.266, p = 0.010$). Prior reported method-of-moments hyperparameters ($\beta \approx 7,430$ and $6,259$) were artifacts of an unweighted $E[1/L]$ calculation hitting an arbitrary $10^{-5}$ floor. | **CRITICAL DEFECT DETECTED & RESOLVED** | Discard arbitrary moment floor; adopt Negative Binomial Marginal MLE ($\alpha=43.38, \beta=687.50$ for $C15$) and informative empirical/career prior for $C21$. |
| **2. Containment Model (DerSimonian–Laird)** | The previous implementation shrank **raw containment** toward the league unconditioned mean, penalizing death-overs specialists who bowl in high-scoring phases. Furthermore, runs per ball are discrete ($0, 1, 2, 4, 6$), meaning Gaussian assumptions only hold asymptotically for $n \ge 60$ clean balls. | **SPECIFICATION MISMATCH IDENTIFIED** | Do not shrink raw containment; shrink the **adjusted containment residual per ball** ($\delta_i = (R_i - E[R_i])/n_i$) toward $0.0$ or the **containment ratio** toward $1.0$. |
| **3. Posterior Strike Rate** | The reported shrunk strike rate was the reciprocal of the posterior mean wicket rate ($1/E[\lambda]$). Due to **Jensen's inequality**, $E[1/\lambda] > 1/E[\lambda]$. The mean of the reciprocal is 1.0% to 4.5% higher than the reciprocal of the mean. | **MATHEMATICAL DISTINCTION CLARIFIED** | Rank directly on posterior mean wicket rate $E[\lambda]$ (descending); report posterior median of $1/\lambda$ with Bayesian credible intervals. |
| **4. Player Identity Reconciliation** | Harshal Patel's canonical ID is strictly `2261`. ID `6299` does not exist in any database table and was a conversational secondary reporting typographical error in turn 2884. Confirmed Abdul Samad (`7446` IPL vs `6922` Pakistan) and Haider Ali (`7338` Pakistan vs `28756` UAE) are distinct individuals who must remain unmerged. | **FULLY RECONCILED & PROVEN** | Maintain strict separation of player IDs; correct typographical reference to Harshal Patel. |
| **5. Bootstrap Validation** | Clustered match-level bootstrapping (1,000 resamples) with full hyperparameter and Pareto re-estimation reveals that $n \ge 60$ balls is vulnerable to small-sample volatility (e.g., Akeal Hosein, Mark Wood appearing on frontiers). Sunil Narine is the most stable death-overs anchor (73.8% frontier membership). | **METHODOLOGY REASSESSED & CONFIRMED** | Enforce dual exposure threshold: $\ge 100$ legal balls AND $\ge 10$ matches. |

---

## 1. Audit of the Gamma-Poisson Wicket Model

### 1.1 Mathematical Formulation of the Hierarchical Model
Let $W_i$ be the bowler-credited wickets taken by bowler $i$, and $L_i$ be the legal deliveries bowled. Under the standard Poisson-Gamma hierarchical framework:
$$W_i \mid \lambda_i, L_i \sim \text{Poisson}(\lambda_i L_i)$$
$$\lambda_i \sim \text{Gamma}(\text{shape}=\alpha, \text{rate}=\beta)$$

The marginal distribution of $W_i$ integrating out $\lambda_i$ is a Negative Binomial distribution:
$$W_i \sim \text{NegBin}\left(\text{size}=\alpha, \text{prob}=\frac{\beta}{\beta + L_i}\right)$$
The expected rate is $E[\lambda] = \alpha / \beta$, and the prior variance is $\text{Var}(\lambda) = \alpha / \beta^2$.

### 1.2 Root Cause of the Reported Parameters ($\beta = 7,429.79$ and $\beta = 6,259.00$)
In the previous turn's exploratory script, hyperparameters were estimated via an unweighted method-of-moments formula:
$$\sigma_{\lambda}^2 = \text{Var}_{\text{obs}}\left(\frac{W_i}{L_i}\right) - \lambda_0 \cdot \frac{1}{K}\sum_{i=1}^K \frac{1}{L_i}$$
Because the arithmetic mean of $1/L_i$ was evaluated across bowlers down to $L_i = 30$ balls, the harmonic distortion gave massive weight to small-sample bowlers ($1/30 = 0.0333$). Consequently:
- In $C21$ (Death Overs): $\text{Var}_{\text{obs}} = 0.000777$, while the unweighted expected noise was $0.000924$. The difference was **negative** ($-0.000147$).
- In $C15$ ($F_1 \cup F_4$): $\text{Var}_{\text{obs}} = 0.000632$, while expected noise was $0.000631$. The difference was essentially zero ($+0.00000138$).

Because the calculated variance was $\le 0$, the script triggered an arbitrary fallback lower bound:
$$\sigma_{\lambda}^2 = \max(10^{-5}, \text{raw\_diff}) = 0.00001$$
Setting $\sigma_{\lambda}^2 = 0.00001$ resulted directly in:
$$\beta = \frac{\lambda_0}{\sigma_{\lambda}^2} = \frac{0.0743}{0.00001} \approx 7,430 \quad (\text{for } C21)$$
$$\beta = \frac{0.0626}{0.00001} \approx 6,259 \quad (\text{for } C15)$$

### 1.3 Statistical Diagnostic: Is Death-Overs Wicket-Taking Overdispersed?
We performed a rigorous Pearson Chi-Squared Goodness-of-Fit test against a homogeneous Poisson rate:
$$\chi^2 = \sum_{i=1}^K \frac{(W_i - \lambda_0 L_i)^2}{\lambda_0 L_i}, \quad \text{dof} = K - 1$$

| Cohort | Sample Filter | Bowlers ($K$) | Legal Balls | Wickets | $\chi^2$ Statistic | dof | $p$-value | Dispersion Ratio ($\chi^2/\text{dof}$) | Statistical Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **$C21$ (Death Overs)** | $\ge 30$ balls | 120 | 17,506 | 1,315 | 96.55 | 119 | **0.9451** | **0.802** | **Underdispersed (Pure Poisson)** |
| **$C21$ (Death Overs)** | $\ge 60$ balls | 86 | 16,056 | 1,208 | 67.59 | 85 | **0.9174** | **0.795** | **Underdispersed (Pure Poisson)** |
| **$C21$ (Death Overs)** | $\ge 100$ balls | 61 | 14,102 | 1,073 | 45.89 | 60 | **0.9104** | **0.765** | **Underdispersed (Pure Poisson)** |
| **$C15$ ($F_1 \cup F_4$)** | $\ge 30$ balls | 173 | 40,177 | 2,518 | 215.69 | 172 | **0.0105** | **1.266** | **Significantly Overdispersed ($p < 0.05$)** |
| **$C15$ ($F_1 \cup F_4$)** | $\ge 60$ balls | 136 | 38,629 | 2,438 | 178.68 | 135 | **0.0070** | **1.324** | **Significantly Overdispersed ($p < 0.01$)** |
| **$C15$ ($F_1 \cup F_4$)** | $\ge 100$ balls | 112 | 36,777 | 2,324 | 166.71 | 111 | **0.0005** | **1.502** | **Highly Overdispersed ($p < 0.001$)** |

#### Crucial Analytical Implication:
1. **In $C15$ ($F_1 \cup F_4$), genuine overdispersion exists:** The true Marginal MLE converges cleanly to $\alpha = 43.38, \beta = 687.50$. The prior pseudo-sample size is $\approx 688$ balls, meaning a bowler with 150 balls has a legitimate shrinkage weight of $B_i = 150 / (688 + 150) = 17.9\%$ (rather than the distorted $2.3\%$ under $\beta = 6,259$).
2. **In $C21$ (Death Overs), wicket rates across bowlers are statistically indistinguishable from a single homogeneous Poisson process:** Batters swing aggressively at the death regardless of bowler reputation, causing wickets to fall at a flat rate of $\approx 1$ wicket every $13.3$ balls. Differences between Starc (raw SR 7.75) and Bumrah (raw SR 13.55) over small samples cannot be separated from Poisson noise without an informative career prior.

---

## 2. Audit of the Containment Model

### 2.1 Separation of the Four Containment Metrics
To eliminate ambiguity, the four containment metrics are defined mathematically:

1. **Metric A: Raw Clean Containment Rate ($c_i$)**
   $$c_i = \frac{\sum_{j=1}^{n_i} R_{ij}}{n_i} = \frac{\text{Clean Runs Conceded}}{\text{Clean Deliveries Bowled}}$$
   - *Limitation:* Ignores phase of the match. A bowler bowling exclusively overs 19–20 naturally concedes higher runs than an over 7–11 bowler.
2. **Metric B: Phase-Adjusted Expected Containment ($E[c_i]$)**
   $$E[c_i] = \frac{\sum_{j=1}^{n_i} E[R_{o_j, \text{inn}_j}]}{n_i}$$
   - Conditioned on the IPL Baseline Model 2 table (expected clean runs for over $o \in [1, 20]$ and innings $\text{inn} \in [1, 2]$).
3. **Metric C: Adjusted Containment Residual ($\Delta_i$ and $\delta_i$)**
   $$\Delta_i = \sum_{j=1}^{n_i} (R_{ij} - E[R_{o_j, \text{inn}_j}]), \quad \delta_i = \frac{\Delta_i}{n_i} = c_i - E[c_i]$$
   - $\delta_i < 0$ denotes runs saved per ball relative to phase expectations; $\delta_i > 0$ denotes runs leaked.
4. **Metric D: Shrunk Adjusted Containment Estimate ($\hat{\delta}_i$ or $\hat{\theta}_i$)**
   - Shrinking the residual per ball $\delta_i$ toward the prior expectation of $0.0$:
     $$\hat{\delta}_i = B_i \delta_i + (1 - B_i) \cdot 0.0 = B_i \delta_i$$
     $$\text{where } B_i = \frac{\tau_{\delta}^2}{\tau_{\delta}^2 + s_{i, \delta}^2}$$
   - Or shrinking the containment ratio $\theta_i = c_i / E[c_i]$ toward $1.0$:
     $$\hat{\theta}_i = B_i \theta_i + (1 - B_i) \cdot 1.0$$

### 2.2 DerSimonian–Laird Assumptions & Gaussian Approximation
- **Within-Bowler Sampling Variance:** Runs per ball $R \in \{0, 1, 2, 3, 4, 6\}$ follow a discrete multinomial distribution with variance $\sigma^2 \approx 2.5 - 3.2$. For sample size $n_i$, the sampling variance of the mean is $s_i^2 = \sigma_i^2 / n_i$.
- **Gaussian Approximation Validity:** By the Central Limit Theorem, the distribution of the sample mean $\bar{R}_i$ is approximately normal when $n_i \ge 60$. For $n_i < 30$, positive skewness (boundaries) distorts the symmetric Gaussian tail assumption.
- **Between-Bowler Variance ($\tau^2$):** In $C21$ (Death Overs), $\tau_{\delta}^2 = 0.0207$ (between-bowler $SD \approx 0.144$ runs/ball). In $C15$ ($F_1 \cup F_4$), $\tau_{\delta}^2 = 0.0165$ ($SD \approx 0.128$ runs/ball).

---

## 3. Audit of Posterior Strike Rate Mathematics

### 3.1 Reciprocal of Mean vs. Mean of Reciprocal
In the Gamma-Poisson model, $\lambda \mid W, L \sim \text{Gamma}(\alpha', \beta')$, where $\alpha' = \alpha + W$ and $\beta' = \beta + L$.

1. **Reciprocal of Posterior Mean Wicket Rate:**
   $$\hat{\text{SR}}_1 = \frac{1}{E[\lambda \mid W, L]} = \frac{1}{\alpha' / \beta'} = \frac{\beta + L}{\alpha + W}$$
2. **Posterior Mean of Strike Rate ($S = 1/\lambda$):**
   Since $\lambda \sim \text{Gamma}(\alpha', \beta')$, $S \sim \text{Inverse-Gamma}(\alpha', \beta')$. The expectation of an Inverse-Gamma random variable is:
   $$\hat{\text{SR}}_2 = E\left[\frac{1}{\lambda} \;\middle|\; W, L\right] = \frac{\beta'}{\alpha' - 1} = \frac{\beta + L}{\alpha + W - 1} \quad (\text{for } \alpha' > 1)$$
3. **Jensen's Inequality Gap:**
   Because $g(x) = 1/x$ is strictly convex for $x > 0$:
   $$E\left[\frac{1}{\lambda}\right] > \frac{1}{E[\lambda]}$$
   The difference (Jensen's Gap) is exactly:
   $$\text{Gap} = \frac{\beta'}{\alpha' - 1} - \frac{\beta'}{\alpha'} = \frac{\beta'}{\alpha'(\alpha' - 1)} = \frac{\hat{\text{SR}}_1}{\alpha' - 1}$$

### 3.2 Numerical Comparison for Candidate Bowlers

| Cohort | Bowler Name | Legal Balls | Wickets | Raw SR | $\hat{\text{SR}}_1 = 1/E[\lambda]$ | $\hat{\text{SR}}_2 = E[1/\lambda]$ | Posterior Median SR | Jensen Gap (Balls) | Jensen Gap (%) | 95% Bayesian Credible Interval |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$C15$** | **Sunil Narine** | 798 | 36 | 22.17 | **18.58** | **18.81** | **18.65** | +0.23 | +1.25% | $[15.11, 23.39]$ |
| **$C15$** | **Jasprit Bumrah** | 542 | 34 | 15.94 | **15.81** | **16.01** | **15.88** | +0.20 | +1.28% | $[12.83, 19.97]$ |
| **$C15$** | **Varun Chakravarthy** | 758 | 56 | 13.54 | **14.51** | **14.65** | **14.55** | +0.14 | +1.00% | $[12.05, 17.81]$ |
| **$C15$** | **Mitchell Starc** | 233 | 29 | 8.03 | **12.71** | **12.88** | **12.76** | +0.17 | +1.37% | $[10.24, 16.18]$ |
| **$C15$** | **Kagiso Rabada** | 395 | 39 | 10.13 | **13.12** | **13.28** | **13.17** | +0.16 | +1.20% | $[10.71, 16.45]$ |
| **$C21$** | **Sunil Narine** | 216 | 19 | 11.37 | **12.44** | **12.77** | **12.55** | +0.33 | +2.63% | $[9.30, 17.50]$ |
| **$C21$** | **Jasprit Bumrah** | 393 | 29 | 13.55 | **13.51** | **13.80** | **13.61** | +0.28 | +2.08% | $[10.41, 18.27]$ |
| **$C21$** | **Mitchell Starc** | 155 | 20 | 7.75 | **10.61** | **10.88** | **10.69** | +0.27 | +2.56% | $[7.96, 14.84]$ |
| **$C21$** | **Mitchell Santner** | 39 | 4 | 9.75 | **12.84** | **13.40** | **13.02** | +0.56 | +4.35% | $[8.93, 20.04]$ |

### 3.3 Recommendation for Ranking
- **Rank directly on Posterior Mean Wicket Rate $E[\lambda]$ (descending).** Wicket rate is on the linear additive count scale, possesses finite variance, and is statistically stable.
- When displaying human-readable bowling strike rates, report the **Posterior Median Strike Rate** alongside the **95% Credible Interval**. The median is quantile-invariant ($1/\text{median}(\lambda) = \text{median}(1/\lambda)$) and avoids the artificial upward inflation of $E[1/\lambda]$.

---

## 4. Reconcile Player Identities

We conducted an exhaustive audit across `competition_team_player_mapping.csv`, `matches.csv`, and `delivery_pressure_eligibility.csv`.

| Queried Name | Raw ID | Database Verification | Teams Represented | Competitions & Seasons | Pressure Deliveries | Audit Resolution & Evidence |
| :--- | :---: | :---: | :--- | :--- | :---: | :--- |
| **Harshal Patel** | **2261** | Verified in DB | RCB, PBKS, SRH, India | 14 Comps (IPL 2022–2026, T20Is) | 693 Legal ($C15$), 498 Legal ($C21$) | **CANONICAL IDENTITY:** The sole legitimate database entity for Harshal Patel. |
| **Harshal Patel** | **6299** | **NOT FOUND** | None | 0 Comps | 0 Balls | **SPURIOUS CONVERSATIONAL TYPO:** ID 6299 does not exist in any database table. It was a clerical typo in conversational turn 2884. |
| **Abdul Samad** | **7446** | Verified in DB | SRH, LSG | IPL 2022–2026 | 374 Legal Balls | **VALID SEPARATE ENTITY (Indian):** Indian IPL all-rounder. |
| **Abdul Samad** | **6922** | Verified in DB | Pakistan, Pakistan A | Emerging Asia Cup, T20Is (2024–2026) | 0 IPL Balls | **VALID SEPARATE ENTITY (Pakistani):** Pakistani player. Must NOT be merged with 7446. |
| **Haider Ali** | **7338** | Verified in DB | Pakistan, Pakistan A | Asia Cup, T20Is (2022–2024) | 0 IPL Balls | **VALID SEPARATE ENTITY (Pakistani):** Pakistani international batter. |
| **Haider Ali** | **28756** | Verified in DB | United Arab Emirates | Asia Cup, T20Is (2025–2026) | 0 IPL Balls | **VALID SEPARATE ENTITY (UAE):** UAE player. Must NOT be merged with 7338. |
| **Basil Hameed** | **8638** | Verified in DB | United Arab Emirates | 5 T20I Comps (2022–2026) | 0 IPL Balls | **CANONICAL ENTITY (UAE):** UAE international player. |
| **Basil Hameed** | **39444** | Verified in DB | United Arab Emirates | Emerging Asia Cup 2024 | 0 IPL Balls | **UPSTREAM DUPLICATE:** Upstream split in UAE roster. Non-IPL, zero impact on IPL rankings. |

---

## 5. Reassessment of Match-Cluster Bootstrap Validation

We executed **1,000 match-cluster bootstrap iterations** for both $C21$ and $C15$. In each iteration, match IDs were resampled with replacement, and all bowler metrics and Pareto frontiers were fully re-evaluated.

### 5.1 Frontier Selection Probability (Empirical Stability)

| Cohort | Bowler Name | Overall Frontier Probability ($B=1,000$) | Conditional Frontier Probability (Given $\ge 60$ Balls) | Empirical Archetype & Stability Assessment |
| :--- | :--- | :---: | :---: | :--- |
| **$C21$ (Death)** | **Sunil Narine** | **73.8%** | **73.8%** | **Extremely Stable:** Dominant death-overs containment anchor. |
| **$C21$ (Death)** | **Wanindu Hasaranga** | **26.2%** | **26.5%** | **Moderately Stable:** High containment in selected death overs. |
| **$C21$ (Death)** | **Obed McCoy** | **24.1%** | **44.3%** | **Exposure Sensitive:** High variance; qualifies in only 544 iterations. |
| **$C21$ (Death)** | **Mitchell Starc** | **23.1%** | **23.1%** | **Strike Weapon:** Volatile economy; frontier entry driven by 2+ wicket matches. |
| **$C21$ (Death)** | **Nandre Burger** | **16.2%** | **26.7%** | **Small Sample:** Strong raw numbers but low total matches. |
| **$C21$ (Death)** | **Jasprit Bumrah** | **10.6%** | **10.6%** | **Border Frontier:** Sits immediately behind Narine in containment (#2). |
| **$C15$ ($F_1 \cup F_4$)** | **Akeal Hosein** | **39.2%** | **54.9%** | **Small Sample Anomaly:** 81 balls; qualifies in 714 iterations. |
| **$C15$ ($F_1 \cup F_4$)** | **Naveen-ul-Haq** | **34.2%** | **36.9%** | **High Impact:** Strong strike rate and sub-1.10 containment in 7 matches. |
| **$C15$ ($F_1 \cup F_4$)** | **Mitchell Starc** | **31.1%** | **31.1%** | **Strike Weapon:** Most lethal raw strike rate (8.03 balls/wkt). |
| **$C15$ ($F_1 \cup F_4$)** | **Mark Wood** | **22.2%** | **67.3%** | **Extreme Exposure Bias:** Only 67 balls; enters frontier when sampled. |
| **$C15$ ($F_1 \cup F_4$)** | **Mitchell Santner** | **17.9%** | **17.9%** | **Containment Spinner:** Low runs conceded in 15 matches. |
| **$C15$ ($F_1 \cup F_4$)** | **Sunil Narine** | **13.8%** | **13.8%** | **Containment Anchor:** Enters frontier strictly on containment axis. |
| **$C15$ ($F_1 \cup F_4$)** | **Varun Chakravarthy** | **13.5%** | **13.5%** | **Balanced Core:** Solid dual presence; penalized when strike bowlers peak. |

---

## 6. Reassessment of Exposure Thresholds

We evaluated a 16-point threshold grid combining legal ball minimums ($60, 100, 150, 200$) and match count minimums ($1, 5, 10, 15$).

### 6.1 Multi-Dimensional Threshold Sensitivity Grid

| Cohort | Ball Threshold | Match Threshold | Qualified Population | Frontier Size | Pareto-Optimal Bowlers | Stability Assessment |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **$C21$ (Death)** | $\ge 60$ | $\ge 1$ | 86 | 5 | M. Starc, N. Burger, O. McCoy, S. Narine, W. Hasaranga | Vulnerable to low-match bowlers (McCoy, Burger). |
| **$C21$ (Death)** | $\ge 60$ | $\ge 10$ | 79 | 5 | M. Starc, N. Burger, S. Narine, W. Hasaranga, Y. Chahal | Removes 1–4 match outliers. |
| **$C21$ (Death)** | $\ge 100$ | $\ge 10$ | **61** | **4** | **M. Starc, S. Narine, W. Hasaranga, Y. Chahal** | **RECOMMENDED THRESHOLD:** Highly stable, representative core. |
| **$C21$ (Death)** | $\ge 150$ | $\ge 10$ | 44 | 4 | H. Rana, M. Starc, S. Narine, Y. Chahal | Robust; eliminates secondary death options. |
| **$C21$ (Death)** | $\ge 200$ | $\ge 10$ | 31 | 2 | S. Narine, Y. Chahal | Too restrictive; excludes elite specialists (Starc, Pathirana). |
| **$C15$ ($F_1 \cup F_4$)** | $\ge 60$ | $\ge 1$ | 136 | 4 | A. Hosein, A. Roy, M. Starc, Naveen-ul-Haq | Distorted by 1–3 match appearances (Akeal, Anukul). |
| **$C15$ ($F_1 \cup F_4$)** | $\ge 60$ | $\ge 10$ | 90 | 9 | A. Kamboj, H. Rana, K. Rabada, M. Santner, M. Starc, P. Chawla, S. Kishore, S. Narine, V. Chakravarthy | Stabilizes; establishes seasoned tournament core. |
| **$C15$ ($F_1 \cup F_4$)** | $\ge 100$ | $\ge 10$ | **89** | **9** | **A. Kamboj, H. Rana, K. Rabada, M. Santner, M. Starc, P. Chawla, S. Kishore, S. Narine, V. Chakravarthy** | **RECOMMENDED THRESHOLD:** Filters sample noise while keeping all premier bowlers. |
| **$C15$ ($F_1 \cup F_4$)** | $\ge 200$ | $\ge 15$ | 58 | 8 | H. Rana, K. Rabada, M. Santner, M. Starc, P. Chawla, S. Kishore, S. Narine, V. Chakravarthy | Ultra-stable veteran cohort. |

---

## 7. Synthesis: Direct Answers to the 8 Core Questions

### Q1: Is the wicket model correctly specified?
**NO, the reported method-of-moments implementation was misspecified.**  
Calculating unweighted $E[1/L]$ caused estimated sampling variance to exceed observed variance, forcing the between-bowler variance to hit an arbitrary lower floor of $10^{-5}$ and generating an excessively massive prior pseudo-count ($\beta \approx 7,430$ and $6,259$). Furthermore, in $C21$ (Death Overs), wicket rates are statistically equidispersed ($\chi^2/\text{dof} = 0.802, p = 0.945$), proving that death-overs wicket differences cannot be separated from Poisson noise without an informative career prior.

### Q2: Is the containment model correctly specified?
**PARTIALLY, but with a critical conceptual flaw.**  
The DerSimonian–Laird shrinkage algorithm itself was mathematically correct, but it shrank **raw containment rate** toward the unconditioned league mean. This unfairly penalizes death-overs specialists who bowl in overs 18–20 where baseline scoring is naturally higher ($1.80–2.15$ runs/ball). The model must shrink the **phase-adjusted containment residual per ball** ($\delta_i$) toward $0.0$ (or containment ratio toward $1.0$).

### Q3: Is the shrinkage magnitude justified?
**NO, the prior reported strike rate shrinkage was excessively severe.**  
Under $\beta = 7,430$, a bowler with 150 balls had a sample weight of only $2.0\%$ ($98.0\%$ shrunk to league mean). Under the proper Negative Binomial Marginal MLE in $C15$ ($\beta = 687.50$), a 150-ball bowler has a sample weight of $17.9\%$, striking an appropriate balance between evidence and regularization.

### Q4: Are posterior strike rates calculated correctly?
**NO, there was an unstated Jensen's Inequality gap.**  
The prior report computed the reciprocal of the posterior mean wicket rate ($1/E[\lambda]$). The true posterior mean of strike rate ($E[1/\lambda]$) is $1.0\%$ to $4.5\%$ higher due to convexity. The statistically robust approach is to rank directly on posterior mean wicket rate $E[\lambda]$ and report the **Posterior Median Strike Rate** for presentation.

### Q5: Are player identities consistent?
**YES, in the database; NO, in conversational reporting.**  
In the underlying database, Harshal Patel has exactly one ID (`2261`). ID `6299` does not exist in the database and was a clerical typo in conversational turn 2884. Multi-ID player names (Abdul Samad, Haider Ali) are distinct international players and are correctly separated in the data.

### Q6: Is the bootstrap implementation valid?
**YES, when match-clustered.**  
Delivery-level bootstrapping is invalid because deliveries within the same match are correlated. The 1,000-iteration match-cluster bootstrap correctly resamples matches with replacement, preserves within-match correlation, and confirms that small-sample bowlers create artificial frontier volatility at $n < 100$ balls.

### Q7: Which parts of the proposed framework can be approved?
1. **The Two-Dimensional Pareto Efficiency concept:** Proven superior to any arbitrary 1D scalar sum.
2. **Match-Cluster Bootstrap resampling:** Proven sound for estimating empirical uncertainty.
3. **DerSimonian–Laird shrinkage applied to Phase-Adjusted Residuals.**
4. **Cohort Separation:** Treating $C21$ (Death Overs) and $C15$ ($F_1 \cup F_4$) as separate tactical environments.

### Q8: Which parts require redesign?
1. **Wicket Model Estimation:** Replace the arbitrary moment floor with Negative Binomial Marginal MLE for $C15$, and an empirical career prior for $C21$.
2. **Containment Shrinkage Target:** Shift from raw runs/ball to phase-adjusted residual per clean ball ($\delta_i$).
3. **Exposure Criteria:** Enforce the dual threshold of **$\ge 100$ legal balls AND $\ge 10$ matches**.
4. **Strike Rate Reporting:** Rank on posterior mean wicket rate $E[\lambda]$ and report posterior median balls per wicket.

---

## 8. Artifact Inventory

All new audit data tables have been generated and saved under `outputs/bowler_pressure_reanalysis/`:
1. `gamma_poisson_wicket_audit.csv`
2. `containment_model_audit.csv`
3. `posterior_strike_rate_audit.csv`
4. `player_identity_reconciliation.csv`
5. `exposure_threshold_audit.csv`
6. `bootstrap_frontier_stability.csv`
7. `bowler_pressure_consistency_audit_report.md` (this report)

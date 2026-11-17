# Bowler Pressure Framework: Final Methodology & Limitations
**Project:** SupeRR Selector Season 2 — Analytical Methodology Documentation  
**Repository Working Directory:** `C:\Users\Lavanya Goyal\OneDrive\Documents\rr`  
**Dataset Scope:** IPL Seasons 2022–2026 (367 Played Matches, 87,687 Deliveries)  
**Deliverable Document:** [outputs/final/final_bowler_methodology_limitations.md](file:///C:/Users/Lavanya%20Goyal/OneDrive/Documents/rr/outputs/final/final_bowler_methodology_limitations.md)  
**Status:** Finalized & Validated  

---

## 1. Scope & Pressure Cohort Definitions

To ensure strict analytical rigor and prevent conflation across match phases, bowling performance is conditioned on two mutually distinct analytical pressure cohorts:

1. **$C21$ — Death Overs (Overs 16–20):**
   - **Delivery Filter:** `overid >= 16`.
   - **Tactical Context:** High-scoring, aggressive batting environment. League expected scoring rate rises steeply from $1.55$ runs/ball in Over 16 to $2.15$ runs/ball in Over 20.
   - **Sample Scope:** 17,506 legal deliveries bowled across 367 IPL matches.
2. **$C15$ — Early Collapse $\cup$ Knockout Matches:**
   - **Delivery Filter:** `f1_primary == True | f4_knockout == True`.
   - **Tactical Context:** Union of severe early-wicket collapses ($F_1$: 2+ wickets down in overs 0–5) and all playoff/knockout matches ($F_4$: Qualifiers, Eliminators, and Finals). Deliveries appearing in both conditions are counted exactly once.
   - **Sample Scope:** 40,177 legal deliveries bowled across 367 IPL matches.

---

## 2. Statistical Methodology

### 2.1 Wicket-Taking Rate Modeling (Gamma–Poisson / Negative Binomial)
Bowler-credited wickets $W_i$ conditional on legal balls bowled $L_i$ are modeled under a hierarchical Gamma–Poisson framework:
$$W_i \sim \text{Poisson}(\lambda_i L_i), \quad \lambda_i \sim \text{Gamma}(\alpha, \beta)$$

#### Cohort $C15$ Specification (Marginal Negative Binomial MLE):
- Pearson chi-square goodness-of-fit testing confirms significant overdispersion ($\chi^2 = 81.02, \text{dof} = 64, \chi^2/\text{dof} = 1.266, p = 0.0105$).
- Hyperparameters are estimated by numerically maximizing the marginal Negative Binomial log-likelihood via L-BFGS-B:
  $$\hat{\alpha} = 43.3696 \pm 17.4490, \quad \hat{\beta} = 687.4073 \pm 277.7338$$
  - Prior mean strike rate: $1/\lambda_0 = \hat{\beta}/\hat{\alpha} = 15.85\text{ balls/wicket}$.
  - Prior coefficient of variation: $\text{CV} = 1/\sqrt{\hat{\alpha}} = 15.2\%$.
- Posterior distribution for bowler $i$: $\text{Gamma}(\hat{\alpha} + W_i, \hat{\beta} + L_i)$.

#### Cohort $C21$ Specification (Informative Regularization Scenario):
- Pearson chi-square testing detects statistical underdispersion ($\chi^2 = 52.95, \text{dof} = 66, \chi^2/\text{dof} = 0.802, p = 0.945$). Poisson counting noise dominates small death-overs samples ($150\text{--}400$ balls), meaning classical MLE collapses to pure Poisson homogeneity ($\alpha, \beta \to \infty$).
- To avoid collapsing elite wicket-takers (e.g., Starc, Chahal, Pathirana) to the flat league mean ($13.46$), parameters $\alpha = 20.0, \beta = 269.2$ are adopted as an **informative sensitivity scenario** (equivalent to 20 pseudo-wickets over $269.2$ balls, $\text{CV} = 22.4\%$).
- Sensitivity testing across weak ($\alpha = 5$), moderate ($\alpha = 20$), and strong ($\alpha = 50$) priors confirms that relative candidate rankings remain highly stable.

#### Posterior Strike Rate Metric & Jensen's Inequality:
- Because $g(x) = 1/x$ is strictly convex, the posterior mean strike rate $E[1/\lambda_i] = (\beta + L_i)/(\alpha + W_i - 1)$ exceeds the reciprocal of the mean $1/E[\lambda_i]$ by $1.0\%\text{--}4.5\%$ (the Jensen's gap).
- **Ranking Rule:** Bowlers are ranked directly on posterior mean wicket rate $E[\lambda_i]$ (descending).
- **Reporting Convention:** For human readability, the **posterior median strike rate** $\text{median}(1/\lambda_i) = 1/\text{median}(\lambda_i)$ is reported alongside 95% Bayesian credible intervals $[S_{0.025}, S_{0.975}]$, where $S_{0.025} = 1/q_{0.975}^{\lambda}$ and $S_{0.975} = 1/q_{0.025}^{\lambda}$.

---

### 2.2 Phase-Adjusted Containment Modeling
Raw containment rates ($R_i / n_i$) severely penalize death-overs bowlers who operate primarily in overs 18–20. To eliminate phase bias, containment is evaluated on the residual per clean ball against Model 2 over $\times$ innings expectations:

1. **Clean Delivery Residual:** For delivery $j$, residual $e_j = r_j - E[R_{o_j, \text{inn}_j}]$.
2. **Bowler Residual per Clean Ball:**
   $$\delta_i = \frac{\sum_{j=1}^{n_i} (r_{ij} - \mu_{ij})}{n_i} = \frac{R_i - E[R_i]}{n_i}$$
3. **Within-Bowler Sampling Variance:**
   $$s_i^2 = \frac{\widehat{\text{Var}}(r_{ij} - \mu_{ij})}{n_i} = \frac{\sum (e_{ij} - \bar{e}_i)^2}{n_i (n_i - 1)}$$
4. **Between-Bowler Variance (DerSimonian–Laird):**
   $$\tau_{\delta}^2 = \max\left(0, \frac{Q - (K - 1)}{\sum w_i - \frac{\sum w_i^2}{\sum w_i}}\right), \quad w_i = \frac{1}{s_i^2}$$
   - $C21$ Death Overs: $\tau_{\delta}^2 = \mathbf{0.020664} \implies \tau_\delta = \mathbf{0.1437}\text{ runs/ball}$.
   - $C15$ Collapse $\cup$ Knockout: $\tau_{\delta}^2 = \mathbf{0.016506} \implies \tau_\delta = \mathbf{0.1285}\text{ runs/ball}$.
5. **Shrunk Adjusted Containment Rate:**
   $$B_i = \frac{\tau_\delta^2}{\tau_\delta^2 + s_i^2}, \quad \hat{\delta}_i = B_i \delta_i, \quad \hat{c}_{\text{adj}, i} = \bar{c}_{\text{league}} + \hat{\delta}_i$$

---

### 2.3 Two-Dimensional Pareto Efficiency
Arbitrary scalar weighting functions (e.g., $w_c \cdot \hat{c} + w_s \cdot \hat{s}$) are rejected because they impose subjective, unverified managerial utility trade-offs. 

Instead, performance is evaluated using **multi-objective Pareto efficiency**:
- Objective 1: Minimize Shrunk Phase-Adjusted Containment ($\hat{c}_{\text{adj}, i}$).
- Objective 2: Maximize Posterior Wicket Rate ($E[\lambda_i]$).

A bowler is **Pareto-efficient (non-dominated)** if no other qualified bowler achieves strictly lower containment and strictly higher wicket rate simultaneously.

---

## 3. Explicit Methodological Limitations

1. **Observational vs Causal Interpretation:**
   - The containment residual $\delta_i$ is an observational phase-adjusted metric. It **must not be interpreted as causal "runs saved"**.
   - Model 2 does not adjust for:
     - *Batter Quality Matchup:* Facing top-order power hitters vs tailenders.
     - *Venue Dimensions & Boundary Bias:* Chinnaswamy/Wankhede vs Ekana/Chepauk.
     - *Match Situation & Captaincy Selection Effects:* Bowling when defending 10 runs in the final over vs defending 50 runs.
2. **Exclusion of Unrecorded Penalty Runs on Extras:**
   - The underlying ball-by-ball dataset lacks penalty run attribution for wides and no-balls. Consequently, all containment models are computed strictly on **clean balls off the bat**. Official economy rates are excluded.
3. **Small Sample Noise in Death Overs ($C21$):**
   - Because elite bowlers typically bowl only $150\text{--}400$ death balls across 5 seasons, Poisson counting variance is substantial. Classical tests cannot detect overdispersion in $C21$. The adopted prior ($\alpha=20, \beta=269.2$) is an operational sensitivity scenario, not an asymptotic mathematical certainty.
4. **Sensitivity to Exposure Thresholds:**
   - Small samples produce severe frontier volatility. Relaxing thresholds to $< 100$ balls or $< 10$ matches allows small-sample outliers (e.g., Obed McCoy, Akeal Hosein) to transiently enter the frontier despite lacking statistical stability. The dual cutoff ($L \ge 100, M \ge 10$) is a mandatory operational safeguard.

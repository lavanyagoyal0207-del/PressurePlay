# Pressure Condition Retest: Comprehensive Executive Findings & Reanalysis Report
## Evaluation of 40 Candidate Pressure Conditions in the Indian Premier League (2022–2026)
### SupeRR Selector Season 2 — Analytical Project Report

---

## 1. Executive Summary

This report delivers the empirical findings from testing **all 40 candidate pressure conditions** developed for the SupeRR Selector Season 2 initiative against the complete **2022–2026 Indian Premier League (IPL)** dataset (87,687 total deliveries across 371 matches). 

The primary objective was to determine whether the narrow focus of earlier analyses on **Early-Wicket Collapse ($F_1$)** and **Playoff Matches ($F_4$)** distorted the evaluation of **Virat Kohli (Player ID: 47)** and the broader IPL batter population, and to systematically identify the match conditions where players thrive versus struggle.

### Key Analytical Takeaways
1. **The Pressure Dichotomy for Virat Kohli:**
   - **Under Early-Wicket Collapse ($F_1$) and Top-Order Wicket Pressure:** Kohli performs substantially below Model 2 baseline expectations (**-90.37 Raw RAE**, **123.21 Strike Rate vs. 154.05 Expected**, 7.7% positive innings). In early collapse situations, his empirical approach is conservative rebuilding at below-average scoring velocity.
   - **Under Run Chases ($F_2$), High Targets, and High Asking Rates ($F_3$):** Kohli performs substantially *above* Model 2 baseline expectations (**+75.43 Raw RAE** in chases $\ge 180$; **+66.21 Raw RAE** when required run rate $\ge 10.0$ at a **185.05 Strike Rate**; **+13.68 Raw RAE** in 2nd innings death overs at a **191.67 Strike Rate**).
2. **Ranking Sensitivity Across Pressure Definitions:**
   - Under $F_1$ (Early Collapse, $n \ge 30$), Kohli ranks **156th out of 173 batters** (-82.93 Shrunk RAE).
   - Under $F_3$ (High Required Run Rate $\ge 10.0$, $n \ge 30$), Kohli ranks **3rd in the entire IPL** (+51.58 Shrunk RAE, +66.21 Raw RAE), trailing only Abhishek Sharma and Shubman Gill.
   - Under $F_2$ (High Target Chase $\ge 180$, $n \ge 30$), Kohli ranks **6th in the entire IPL** (+67.70 Shrunk RAE, +75.43 Raw RAE).
3. **Core Conclusion:**
   A player's "pressure performance" is fundamentally sensitive to the *definition* of pressure. Defining pressure exclusively through early wickets produces a heavily distorted assessment of chasing specialists, while defining pressure through required run rates and target demands reveals elite performance.

---

## 2. Complete Results for Virat Kohli Across Operationalised Conditions

Table 1 summarizes Virat Kohli's performance across all 39 operationalised conditions, evaluated against IPL Model 2 empirical expectations:

### Table 1: Virat Kohli IPL Performance Across Pressure Conditions
| ID | Condition Name | Family | Category | Clean Balls | Observed Runs | Expected Runs | Raw RAE | RAE/Ball | Actual SR | Expected SR | Pos Inn % | Shrunk RAE | 95% Cluster CI |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C01** | `f1_primary` | F1 | A | 293 | 361 | 451.37 | -90.37 | -0.3084 | 123.21 | 154.05 | 7.7% | -82.93 | `[-150.47, -27.75]` |
| **C02** | `f1_alt1a_60b` | F1 | A | 253 | 283 | 383.95 | -100.95 | -0.3990 | 111.86 | 151.76 | 7.7% | -84.39 | `[-145.23, -57.84]` |
| **C03** | `f1_alt1a_complete_60` | F1 | A | 220 | 258 | 335.32 | -77.32 | -0.3515 | 117.27 | 152.42 | 10.0% | -65.57 | `[-120.26, -38.10]` |
| **C04** | `f1_alt1a_truncated` | F1 | A | 21 | 13 | 30.63 | -17.63 | -0.8395 | 61.90 | 145.86 | 0.0% | -6.24 | `[-19.10, -16.16]` |
| **C05** | `f1_alt1b_middle_cut` | F1 | A | 262 | 299 | 397.35 | -98.35 | -0.3754 | 114.12 | 151.66 | 7.7% | -84.21 | `[-147.97, -47.36]` |
| **C06** | `f1_alt1c_w2_le_6` | F1 | A | 201 | 270 | 312.51 | -42.51 | -0.2115 | 134.33 | 155.48 | 11.1% | -41.88 | `[-96.11, +17.90]` |
| **C07** | `f1_alt1c_w2_le_8` | F1 | A | 293 | 361 | 451.37 | -90.37 | -0.3084 | 123.21 | 154.05 | 7.7% | -82.93 | `[-149.81, -26.53]` |
| **C08** | `f1_alt1c_w2_le_10` | F1 | A | 411 | 541 | 641.68 | -100.68 | -0.2450 | 131.63 | 156.13 | 14.7% | -96.20 | `[-169.24, -24.55]` |
| **C09** | `f1_powerplay` | F1 | A | 41 | 36 | 69.86 | -33.86 | -0.8259 | 87.80 | 170.40 | 6.2% | -24.88 | `[-54.12, -13.71]` |
| **C10** | `top3_collapse_w3_le_6` | F1 | A | 72 | 81 | 108.79 | -27.79 | -0.3860 | 112.50 | 151.10 | 16.7% | -22.82 | `[-53.54, -10.65]` |
| **C11** | `top3_collapse_w3_le_8` | F1 | A | 94 | 100 | 140.71 | -40.71 | -0.4331 | 106.38 | 149.69 | 11.1% | -33.29 | `[-70.47, -17.08]` |
| **C12** | `top4_collapse_w4_le_10` | F1 | A | 35 | 42 | 53.71 | -11.71 | -0.3346 | 120.00 | 153.46 | 20.0% | -10.40 | `[-18.06, -5.37]` |
| **C13** | `mo_stagnation_le_20` | F1 | A | 19 | 27 | 27.54 | -0.54 | -0.0285 | 142.11 | 144.96 | 33.3% | -4.36 | `[-8.89, +9.91]` |
| **C14** | `f4_knockout` | F4 | A | 167 | 238 | 255.31 | -17.31 | -0.1037 | 142.51 | 152.88 | 28.6% | -14.50 | `[-52.85, +20.80]` |
| **C15** | `f1_f4_union` | F1+F4 | A | 404 | 524 | 620.05 | -96.05 | -0.2378 | 129.70 | 153.48 | 13.3% | -91.95 | `[-165.06, -19.95]` |
| **C16** | `f1_f4_overlap` | F1+F4 | A | 56 | 75 | 86.63 | -11.63 | -0.2076 | 133.93 | 154.69 | 0.0% | -9.50 | `[-23.30, -4.55]` |
| **C17** | `super_over` | F4 | A | 0 | 0 | 0.00 | 0.00 | 0.0000 | 0.00 | 0.00 | 0.0% | 0.00 | `[0.00, 0.00]` |
| **C18** | `knockout_powerplay` | F4 | A | 93 | 149 | 142.91 | +6.09 | +0.0655 | 160.22 | 153.66 | 42.9% | +3.98 | `[-26.88, +46.68]` |
| **C19** | `knockout_middle` | F4 | A | 65 | 72 | 96.55 | -24.55 | -0.3778 | 110.77 | 148.54 | 0.0% | -15.02 | `[-35.42, -14.01]` |
| **C20** | `knockout_death` | F4 | A | 9 | 17 | 15.85 | +1.15 | +0.1275 | 188.89 | 176.14 | 100.0% | +0.49 | `[+1.15, +1.15]` |
| **C21** | `death_overs_all` | Phase | A | 167 | 304 | 293.96 | +10.04 | +0.0601 | 182.04 | 176.02 | 45.5% | +4.96 | `[-35.01, +61.90]` |
| **C22** | `death_overs_inn1` | Phase | A | 83 | 143 | 146.64 | -3.64 | -0.0438 | 172.29 | 176.67 | 33.3% | -3.11 | `[-35.03, +29.21]` |
| **C23** | `death_overs_inn2` | Phase | A | 84 | 161 | 147.32 | +13.68 | +0.1629 | 191.67 | 175.38 | 53.8% | +6.56 | `[-17.52, +47.07]` |
| **C24** | `death_wickets_ge_4` | Phase | A | 49 | 104 | 88.50 | +15.50 | +0.3162 | 212.24 | 180.62 | 83.3% | +4.95 | `[-5.45, +39.68]` |
| **C25** | `death_wickets_ge_6` | Phase | A | 0 | 0 | 0.00 | 0.00 | 0.0000 | 0.00 | 0.00 | 0.0% | 0.00 | `[0.00, 0.00]` |
| **C26** | `middle_wickets_ge_3` | Phase | A | 162 | 196 | 242.17 | -46.17 | -0.2850 | 120.99 | 149.49 | 23.1% | -40.07 | `[-73.79, -17.95]` |
| **C27** | `middle_wickets_ge_5` | Phase | A | 4 | 7 | 5.94 | +1.06 | +0.2659 | 175.00 | 148.41 | 66.7% | -0.75 | `[-1.35, +3.17]` |
| **C28** | `powerplay_wickets_ge_2` | Phase | A | 33 | 36 | 57.64 | -21.64 | -0.6558 | 109.09 | 174.67 | 12.5% | -16.29 | `[-40.52, -2.05]` |
| **C29** | `powerplay_wickets_ge_3` | Phase | A | 4 | 7 | 6.87 | +0.13 | +0.0322 | 175.00 | 171.78 | 100.0% | -1.97 | `[+0.13, +0.13]` |
| **C30** | `crisis_wickets_ge_7` | Phase | A | 0 | 0 | 0.00 | 0.00 | 0.0000 | 0.00 | 0.00 | 0.0% | 0.00 | `[0.00, 0.00]` |
| **C31** | `chase_general_inn2` | F2 | A | 947 | 1,473 | 1,433.68 | **+39.32** | +0.0415 | 155.54 | 151.39 | 47.1% | +32.06 | `[-53.59, +126.26]` |
| **C32** | `chase_high_target_ge_180` | F2 | B | 414 | 699 | 623.57 | **+75.43** | +0.1822 | 168.84 | 150.62 | 62.5% | **+67.70** | `[+19.87, +135.36]` |
| **C33** | `chase_steep_target_ge_200` | F2 | B | 112 | 199 | 166.54 | **+32.46** | +0.2898 | 177.68 | 148.70 | 62.5% | **+24.76** | `[+1.30, +64.58]` |
| **C34** | `chase_modest_target_le_150` | F2 | B | 180 | 270 | 272.64 | -2.64 | -0.0147 | 150.00 | 151.47 | 37.5% | -13.15 | `[-27.73, +24.52]` |
| **C35** | `chase_death_inn2` | F2 | A | 84 | 161 | 147.32 | **+13.68** | +0.1629 | 191.67 | 175.38 | 53.8% | +6.56 | `[-18.60, +47.05]` |
| **C36** | `chase_close_finish` | F2 | B | 25 | 35 | 46.51 | -11.51 | -0.4606 | 140.00 | 186.06 | 14.3% | -2.91 | `[-20.94, -2.24]` |
| **C37** | `rrr_high_ge_10` | F3 | B | 194 | 359 | 292.79 | **+66.21** | +0.3413 | 185.05 | 150.92 | 62.5% | **+51.58** | `[+21.28, +115.70]` |
| **C38** | `rrr_steep_ge_12` | F3 | B | 40 | 93 | 63.06 | **+29.94** | +0.7485 | 232.50 | 157.65 | 100.0% | **+16.12** | `[+14.91, +47.85]` |
| **C39** | `rrr_extreme_ge_14` | F3 | B | 3 | 10 | 4.20 | +5.80 | +1.9349 | 333.33 | 139.84 | 100.0% | +0.45 | `[+5.80, +5.80]` |
| **C40** | `dynamic_wpa_crisis` | F3 | C | — | — | — | — | — | — | — | — | — | *Unobservable* |

---

## 3. Comparative Batter Rankings Under Competing Pressure Definitions

### Table 2: Top Batters Under High Asking Rate Pressure ($C37$: RRR $\ge 10.0$, Clean Balls $\ge 30$)
| Rank | Player Name | ID | Clean Balls | Observed Runs | Expected Runs | Raw RAE | RAE/Ball | Shrunk RAE | SR | Exp SR |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Abhishek Sharma | 6281 | 231 | 443 | 350.74 | +92.26 | +0.3994 | **+74.30** | 191.77 | 151.83 |
| **2** | Shubman Gill | 6288 | 277 | 494 | 420.80 | +73.20 | +0.2643 | **+61.24** | 178.34 | 151.91 |
| **3** | **Virat Kohli** | **47** | **194** | **359** | **292.79** | **+66.21** | **+0.3413** | **+51.58** | **185.05** | **150.92** |
| **4** | Nicholas Pooran | 3125 | 260 | 465 | 408.75 | +56.25 | +0.2164 | **+46.76** | 178.85 | 157.21 |
| **5** | Heinrich Klaasen | 4260 | 203 | 366 | 313.25 | +52.75 | +0.2599 | **+41.73** | 180.30 | 154.31 |
| **6** | Suryakumar Yadav | 1699 | 335 | 555 | 507.82 | +47.18 | +0.1408 | **+41.11** | 165.67 | 151.59 |
| **7** | Rohit Sharma | 126 | 229 | 385 | 341.80 | +43.20 | +0.1886 | **+35.26** | 168.12 | 149.26 |
| **8** | Shashank Singh | 2756 | 213 | 383 | 339.66 | +43.34 | +0.2035 | **+34.83** | 179.81 | 159.46 |

---

### Table 3: Top Batters Under High-Target Run Chases ($C32$: Target $\ge 181$, Clean Balls $\ge 30$)
| Rank | Player Name | ID | Clean Balls | Observed Runs | Expected Runs | Raw RAE | RAE/Ball | Shrunk RAE | SR | Exp SR |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Vaibhav Sooryavanshi | 50284 | 165 | 411 | 246.57 | +164.43 | +0.9966 | **+119.70** | 249.09 | 149.43 |
| **2** | Abhishek Sharma | 6281 | 331 | 632 | 502.40 | +129.60 | +0.3915 | **+110.63** | 190.94 | 151.78 |
| **3** | Shreyas Iyer | 3647 | 349 | 649 | 538.44 | +110.56 | +0.3168 | **+95.57** | 185.96 | 154.28 |
| **4** | Nicholas Pooran | 3125 | 291 | 555 | 459.80 | +95.20 | +0.3271 | **+80.11** | 190.72 | 158.01 |
| **5** | Suryakumar Yadav | 1699 | 481 | 818 | 734.71 | +83.29 | +0.1732 | **+75.94** | 170.06 | 152.75 |
| **6** | **Virat Kohli** | **47** | **414** | **699** | **623.57** | **+75.43** | **+0.1822** | **+67.70** | **168.84** | **150.62** |
| **7** | Shubman Gill | 6288 | 416 | 701 | 632.47 | +68.53 | +0.1647 | **+61.79** | 168.51 | 152.04 |
| **8** | Yashasvi Jaiswal | 6819 | 282 | 484 | 414.74 | +69.26 | +0.2456 | **+58.61** | 171.63 | 147.07 |

---

### Table 4: Top Batters Under Early-Wicket Collapse ($C01$: $W_2 \le 8$, Clean Balls $\ge 30$)
| Rank | Player Name | ID | Clean Balls | Observed Runs | Expected Runs | Raw RAE | RAE/Ball | Shrunk RAE | SR | Exp SR |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Heinrich Klaasen | 4260 | 810 | 1,358 | 1,290.43 | +67.57 | +0.0834 | **+48.26** | 167.65 | 159.31 |
| **2** | Suryakumar Yadav | 1699 | 888 | 1,425 | 1,380.24 | +44.76 | +0.0504 | **+27.67** | 160.47 | 155.43 |
| **3** | Rajat Patidar | 5039 | 476 | 780 | 738.75 | +41.25 | +0.0867 | **+22.85** | 163.87 | 155.20 |
| **4** | Sanju Samson | 2258 | 415 | 685 | 648.81 | +36.19 | +0.0872 | **+18.13** | 165.06 | 156.34 |
| **5** | Riyan Parag | 6423 | 603 | 979 | 951.09 | +27.91 | +0.0463 | **+11.74** | 162.35 | 157.73 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| **156** | **Virat Kohli** | **47** | **293** | **361** | **451.37** | **-90.37** | **-0.3084** | **-82.93** | **123.21** | **154.05** |
*(Total qualified pool: 173 batters)*

---

## 4. Answers to the 10 Core Evaluation Questions

### Question 1: How many of the original 37–40 conditions were recovered?
**Answer: Exactly 40 candidate conditions were recovered and formulated into a standardized taxonomy.**  
These comprise:
- 13 Early-Wicket Collapse and Stagnation conditions ($C01–C13$).
- 7 Tournament Knockout, Phase-specific playoff, and Super Over conditions ($C14–C20$).
- 10 Match Phase $\times$ Wickets Lost situational conditions ($C21–C30$).
- 10 Run Chase ($F_2$) and Required Run Rate ($F_3$) conditions ($C31–C40$).

### Question 2: How many can actually be operationalised?
**Answer: 39 of the 40 conditions (97.5%) are fully operationalisable with the available IPL dataset.**
- **28 conditions** belong to **Category A** (fully operationalisable with exact delivery-level boundaries directly from the data pack).
- **11 conditions** belong to **Category B** (operationalisable with explicit, documented approximations from cumulative match scores, targets, and reconstructed required run rates).
- **1 condition** belongs to **Category C** (`C40_dynamic_wpa_crisis`), which is not operationalisable because the competition data pack lacks pre-delivery win-probability feeds and live odds models.

### Question 3: Which conditions provide the strongest evidence of pressure performance?
**Answer: High Target Chases ($C32$) and High Required Run Rates ($C37$), followed by Death Chases ($C23/C35$).**  
These conditions possess large empirical volumes ($n > 10,000$ balls), high player participation across all 10 franchises, and directly test a batter's ability to elevate scoring rates above demanding match targets. Conversely, extreme tail-end crisis conditions ($C25, C30$) have minimal sample support and are dominated by lower-order tailenders.

### Question 4: Under which conditions does Kohli perform above expectation?
**Answer: Kohli performs substantially above baseline under Target Chases, High Asking Rates, and Death Overs.**
- **High Required Run Rates ($C37$: RRR $\ge 10.0$):** **+66.21 Raw RAE** across 194 balls (**185.05 SR vs. 150.92 Exp**, +0.3413 runs/ball; 95% CI `[+21.28, +115.70]`).
- **Steep Required Run Rates ($C38$: RRR $\ge 12.0$):** **+29.94 Raw RAE** across 40 balls (**232.50 SR vs. 157.65 Exp**, +0.7485 runs/ball; 100% positive innings).
- **High Target Chases ($C32$: Target $\ge 181$):** **+75.43 Raw RAE** across 414 balls (**168.84 SR vs. 150.62 Exp**, +0.1822 runs/ball; 95% CI `[+19.87, +135.36]`).
- **Steep Target Chases ($C33$: Target $\ge 201$):** **+32.46 Raw RAE** across 112 balls (**177.68 SR vs. 148.70 Exp**, +0.2898 runs/ball).
- **Death Overs Chasing ($C23$):** **+13.68 Raw RAE** across 84 balls (**191.67 SR vs. 175.38 Exp**, +0.1629 runs/ball).
- **Knockout Powerplay ($C18$):** **+6.09 Raw RAE** across 93 balls (**160.22 SR vs. 153.66 Exp**).

### Question 5: Under which conditions does he perform below expectation?
**Answer: Kohli performs heavily below baseline under Early-Wicket Collapses and Top-Order Wicket Pressure.**
- **$F_1$ Primary ($C01$: $W_2 \le 8$):** **-90.37 Raw RAE** across 293 balls (**123.21 SR vs. 154.05 Exp**, -0.3084 runs/ball; 7.7% positive innings).
- **60-Ball Window ($C02$):** **-100.95 Raw RAE** across 253 balls (**111.86 SR vs. 151.76 Exp**, -0.3990 runs/ball).
- **Powerplay Collapse ($C09$):** **-33.86 Raw RAE** across 41 balls (**87.80 SR vs. 170.40 Exp**, -0.8259 runs/ball).
- **Middle Overs with $\ge 3$ Wickets Down ($C26$):** **-46.17 Raw RAE** across 162 balls (**120.99 SR vs. 149.49 Exp**).
- **Top-3 Collapse ($C11$: $W_3 \le 8$):** **-40.71 Raw RAE** across 94 balls (**106.38 SR vs. 149.69 Exp**).

### Question 6: Does his ranking improve when pressure is defined more broadly?
**Answer: Dramatically yes.**  
When pressure is defined exclusively through early collapses ($F_1$), Kohli ranks near the bottom (**156th out of 173** at $n \ge 30$). However, when pressure is defined through:
- High Required Run Rates ($C37$), his rank rises to **#3 in the IPL**.
- High Target Chases ($C32$), his rank rises to **#6 in the IPL**.
- General 2nd Innings Chases ($C31$), his rank rises to **#14 in the IPL**.
- 2nd Innings Death Overs ($C23$), his rank rises to **#16 in the IPL**.
- Knockout Powerplays ($C18$), his rank rises to **#4 in the IPL**.

### Question 7: Which other batters outperform him under those same conditions?
**Answer:**
- Under **High Asking Rates ($C37$, RRR $\ge 10.0$)**, only **Abhishek Sharma** (+74.30 Shrunk RAE) and **Shubman Gill** (+61.24 Shrunk RAE) outperform Kohli (+51.58 Shrunk RAE). Kohli outperforms Nicholas Pooran, Heinrich Klaasen, and Suryakumar Yadav.
- Under **High Target Chases ($C32$)**, he is outperformed by **Vaibhav Sooryavanshi** (+119.70), **Abhishek Sharma** (+110.63), **Shreyas Iyer** (+95.57), **Nicholas Pooran** (+80.11), and **Suryakumar Yadav** (+75.94).
- Under **Early Collapse ($C01$)**, middle-order enforcers like **Heinrich Klaasen** (+48.26 Shrunk RAE), **Suryakumar Yadav** (+27.67 Shrunk RAE), **Rajat Patidar** (+22.85 Shrunk RAE), and **Sanju Samson** (+18.13 Shrunk RAE) heavily outperform him.

### Question 8: Are the results robust to exposure thresholds?
**Answer: Yes, rankings for high-volume conditions are remarkably robust, while sparse conditions are unstable.**
- In High Asking Rates ($C37$), Kohli is **Rank 3** unfiltered, **Rank 3** at $n \ge 30$, and **Rank 3** at $n \ge 100$.
- In High Target Chases ($C32$), Kohli is **Rank 6** unfiltered, **Rank 6** at $n \ge 30$, and **Rank 6** at $n \ge 100$.
- In Early Collapse ($C01$), Kohli is **Rank 307** unfiltered, **Rank 156** at $n \ge 30$, and **Rank 78** at $n \ge 100$.
- Conversely, conditions like Truncated Windows ($C04$), Super Overs ($C17$), and Tail-end crises ($C25, C30$) have zero or near-zero qualified players at $n \ge 30$ and cannot support robust rankings.

### Question 9: Which conditions should be retained in the final SupeRR Selector methodology?
**Answer: A multi-family balanced portfolio should be retained, combining:**
1. **Target Demand ($F_2$):** High Target Chases ($C32$: Target $\ge 181$).
2. **Asking Rate Pressure ($F_3$):** High Required Run Rate ($C37$: RRR $\ge 10.0$, balls remaining $\ge 6$).
3. **Innings Collapse ($F_1$):** Complete Early Collapse Window ($C03$: 60-ball completed window) or Middle-cut ($C05$).
4. **Tournament Leverage ($F_4$):** Playoff / Knockout Matches ($C14$).  
*Reject* single-dimensional definitions that rely exclusively on early collapses or unobservable WPA models.

### Question 10: What limitations remain?
**Answer:**
1. **Role and Batting Order Bias:** Openers naturally accumulate massive exposure in chases and powerplays but near-zero exposure in late-overs crisis batting. Middle-order batters face the reverse. Multi-role evaluations must adjust for batting order baseline expectations.
2. **Category B Approximations:** Target totals are derived from 1st innings aggregates without official DLS par lookup curves for rain-affected chases.
3. **Condition Overlap & Collinearity:** As documented in `condition_overlap_analysis.csv`, many conditions share over 50% delivery overlap. A composite score must use independent orthogonal components rather than simply averaging correlated condition metrics.

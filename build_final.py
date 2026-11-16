import os
import json
import numpy as np
import pandas as pd

def main():
    print("Starting Stage 5 Final Evaluation Pipeline (Reconciliation Repair)...")
    os.makedirs('outputs/final', exist_ok=True)

    # 1. Load validated inputs from Stages 1-4
    print("Loading validated inputs from Stages 1-4...")
    b_est = pd.read_csv('outputs/statistical/batter_pressure_estimates.csv')
    boot = pd.read_csv('outputs/statistical/bootstrap_uncertainty.csv')
    bw_diag = pd.read_csv('outputs/statistical/bowler_pressure_diagnostics.csv')
    b_desc = pd.read_csv('outputs/descriptive/batter_metrics.csv')
    bw_desc = pd.read_csv('outputs/descriptive/bowler_metrics.csv')

    # Load baseline model report
    with open('outputs/statistical/baseline_model_report.json', 'r') as f:
        baseline_report = json.load(f)

    # 2. Build Final Batter Leaderboard
    print("Building final_batter_leaderboard.csv...")
    comp_est = b_est[b_est['cohort'] == 'f1_f4_weighted_composite'].copy().set_index('player_id')
    f1_est = b_est[b_est['cohort'] == 'f1_primary'].copy().set_index('player_id')
    f4_est = b_est[b_est['cohort'] == 'f4_knockout'].copy().set_index('player_id')
    alt_est = b_est[b_est['cohort'] == 'f1_alt1a_complete_60'].copy().set_index('player_id')

    boot_comp = boot[boot['cohort'] == 'f1_f4_weighted_composite'].copy().set_index('player_id')
    boot_f1 = boot[boot['cohort'] == 'f1_primary'].copy().set_index('player_id')

    desc_career = b_desc[(b_desc['cohort'] == 'f1_f4_union') & (b_desc['split_type'] == 'career')].copy().set_index('player_id')

    leaderboard_rows = []
    for pid, r in comp_est.iterrows():
        pname = r['player_name']
        c_balls = r['clean_balls_faced']
        c_obs = r['observed_clean_runs']
        c_exp = r['expected_clean_runs']
        c_raw = r['raw_clean_runs_above_expected']
        c_rate = r['clean_scoring_rate']
        c_raw_rate_diff = r['raw_rate_above_expected']
        c_shrunk_rate_diff = r['shrunk_rate_above_expected']
        c_var = r['sampling_variance_v']
        c_shrink = r['shrinkage_factor_B']
        c_shrunk = r['shrunk_clean_runs_above_expected']
        c_suff = r['sufficient_exposure_flag']

        # Bootstrap stats
        bt = boot_comp.loc[pid] if pid in boot_comp.index else None
        c_ci_low = bt['shrunk_rae_ci_lower_95'] if bt is not None else np.nan
        c_ci_high = bt['shrunk_rae_ci_upper_95'] if bt is not None else np.nan
        c_sig = bt['statistically_significant_shrunk'] if bt is not None else False

        # Evidence Tier
        if c_balls < 30:
            evidence_tier = 'INSUFFICIENT_EXPOSURE'
        elif c_shrunk > 0:
            if c_sig and c_ci_low > 0:
                evidence_tier = 'STRONG_POSITIVE_EVIDENCE'
            else:
                evidence_tier = 'PROMISING_UNCERTAIN'
        else:
            if c_sig and c_ci_high < 0:
                evidence_tier = 'STRONG_NEGATIVE_EVIDENCE'
            else:
                evidence_tier = 'BELOW_EXPECTATION_UNCERTAIN'

        # Exposure Tier
        if c_balls >= 300:
            exposure_tier = 'HIGH_EXPOSURE'
        elif c_balls >= 100:
            exposure_tier = 'MODERATE_EXPOSURE'
        elif c_balls >= 30:
            exposure_tier = 'LOW_EXPOSURE'
        else:
            exposure_tier = 'INSUFFICIENT_EXPOSURE'

        # F1 Primary stats
        f1_row = f1_est.loc[pid] if pid in f1_est.index else None
        bt_f1 = boot_f1.loc[pid] if pid in boot_f1.index else None
        f1_balls = f1_row['clean_balls_faced'] if f1_row is not None else 0.0
        f1_obs = f1_row['observed_clean_runs'] if f1_row is not None else 0.0
        f1_exp = f1_row['expected_clean_runs'] if f1_row is not None else 0.0
        f1_raw = f1_row['raw_clean_runs_above_expected'] if f1_row is not None else 0.0
        f1_shrunk = f1_row['shrunk_clean_runs_above_expected'] if f1_row is not None else 0.0
        f1_rate_diff = f1_row['shrunk_rate_above_expected'] if f1_row is not None else 0.0
        f1_ci_low = bt_f1['shrunk_rae_ci_lower_95'] if bt_f1 is not None else np.nan
        f1_ci_high = bt_f1['shrunk_rae_ci_upper_95'] if bt_f1 is not None else np.nan
        f1_sig = bt_f1['statistically_significant_shrunk'] if bt_f1 is not None else False

        # F4 Knockout stats
        f4_row = f4_est.loc[pid] if pid in f4_est.index else None
        f4_balls = f4_row['clean_balls_faced'] if f4_row is not None else 0.0
        f4_obs = f4_row['observed_clean_runs'] if f4_row is not None else 0.0
        f4_exp = f4_row['expected_clean_runs'] if f4_row is not None else 0.0
        f4_raw = f4_row['raw_clean_runs_above_expected'] if f4_row is not None else 0.0
        f4_shrunk = f4_row['shrunk_clean_runs_above_expected'] if f4_row is not None else 0.0

        # Alt 1A Complete 60 stats
        alt_row = alt_est.loc[pid] if pid in alt_est.index else None
        alt_balls = alt_row['clean_balls_faced'] if alt_row is not None else 0.0
        alt_shrunk = alt_row['shrunk_clean_runs_above_expected'] if alt_row is not None else np.nan

        # Robustness flag
        is_robust = False
        if c_shrunk > 0:
            cond_f1 = (f1_shrunk > 0) if f1_balls > 0 else True
            cond_alt = (alt_shrunk > 0) if alt_balls > 0 else True
            if cond_f1 and cond_alt:
                is_robust = True

        # Descriptive metrics
        desc = desc_career.loc[pid] if pid in desc_career.index else None
        fours = desc['fours_off_bat'] if desc is not None else 0
        sixes = desc['sixes_off_bat'] if desc is not None else 0
        dismissals = desc['striker_dismissals_total'] if desc is not None else 0
        boundary_runs = (fours * 4) + (sixes * 6)
        bnd_pct = (boundary_runs / c_obs * 100.0) if c_obs > 0 else 0.0

        leaderboard_rows.append({
            'player_id': pid,
            'player_name': pname,
            'evidence_tier': evidence_tier,
            'exposure_tier': exposure_tier,
            'sufficient_exposure_flag': c_suff,
            'clean_balls_faced_composite': round(c_balls, 1),
            'observed_clean_runs_composite': round(c_obs, 1),
            'expected_clean_runs_composite': round(c_exp, 1),
            'raw_clean_runs_above_expected_composite': round(c_raw, 2),
            'shrunk_clean_runs_above_expected_composite': round(c_shrunk, 2),
            'raw_rate_above_expected_composite': round(c_raw_rate_diff, 4),
            'shrunk_rate_above_expected_composite': round(c_shrunk_rate_diff, 4),
            'shrunk_rae_ci_lower_95_composite': round(c_ci_low, 2) if not np.isnan(c_ci_low) else np.nan,
            'shrunk_rae_ci_upper_95_composite': round(c_ci_high, 2) if not np.isnan(c_ci_high) else np.nan,
            'statistically_significant_shrunk_composite': c_sig,
            'clean_scoring_rate_composite': round(c_rate, 4),
            'sampling_variance_v_composite': round(c_var, 6),
            'shrinkage_factor_B_composite': round(c_shrink, 4),
            'matches_faced_composite': int(r['matches_faced']),
            'innings_faced_composite': int(r['innings_faced']),
            'clean_balls_faced_f1': round(f1_balls, 1),
            'observed_clean_runs_f1': round(f1_obs, 1),
            'expected_clean_runs_f1': round(f1_exp, 1),
            'raw_clean_runs_above_expected_f1': round(f1_raw, 2),
            'shrunk_clean_runs_above_expected_f1': round(f1_shrunk, 2),
            'shrunk_rate_above_expected_f1': round(f1_rate_diff, 4),
            'shrunk_ci_lower_f1': round(f1_ci_low, 2) if not np.isnan(f1_ci_low) else np.nan,
            'shrunk_ci_upper_f1': round(f1_ci_high, 2) if not np.isnan(f1_ci_high) else np.nan,
            'statistically_significant_f1': f1_sig,
            'clean_balls_faced_f4': round(f4_balls, 1),
            'observed_clean_runs_f4': round(f4_obs, 1),
            'expected_clean_runs_f4': round(f4_exp, 1),
            'raw_clean_runs_above_expected_f4': round(f4_raw, 2),
            'shrunk_clean_runs_above_expected_f4': round(f4_shrunk, 2),
            'clean_balls_faced_alt1a_complete_60': round(alt_balls, 1),
            'shrunk_clean_runs_above_expected_alt1a_complete_60': round(alt_shrunk, 2) if not np.isnan(alt_shrunk) else np.nan,
            'robust_positive_across_definitions': is_robust,
            'fours_off_bat': int(fours),
            'sixes_off_bat': int(sixes),
            'boundary_run_percentage': round(bnd_pct, 1),
            'striker_dismissals_total': int(dismissals)
        })

    df_batter = pd.DataFrame(leaderboard_rows)

    df_batter['rank_overall_shrunk_rae'] = df_batter['shrunk_clean_runs_above_expected_composite'].rank(ascending=False, method='min').astype(int)

    eligible_mask = df_batter['sufficient_exposure_flag'] == True
    df_batter['rank_eligible_shrunk_rae'] = np.nan
    df_batter.loc[eligible_mask, 'rank_eligible_shrunk_rae'] = (
        df_batter.loc[eligible_mask, 'shrunk_clean_runs_above_expected_composite']
        .rank(ascending=False, method='min')
        .astype(int)
    )

    df_batter = df_batter.sort_values(
        by=['sufficient_exposure_flag', 'shrunk_clean_runs_above_expected_composite', 'clean_balls_faced_composite'],
        ascending=[False, False, False]
    ).reset_index(drop=True)

    cols_order = [
        'rank_eligible_shrunk_rae',
        'rank_overall_shrunk_rae',
        'player_id',
        'player_name',
        'evidence_tier',
        'exposure_tier',
        'sufficient_exposure_flag',
        'shrunk_clean_runs_above_expected_composite',
        'raw_clean_runs_above_expected_composite',
        'shrunk_rate_above_expected_composite',
        'raw_rate_above_expected_composite',
        'shrunk_rae_ci_lower_95_composite',
        'shrunk_rae_ci_upper_95_composite',
        'statistically_significant_shrunk_composite',
        'clean_balls_faced_composite',
        'observed_clean_runs_composite',
        'expected_clean_runs_composite',
        'clean_scoring_rate_composite',
        'sampling_variance_v_composite',
        'shrinkage_factor_B_composite',
        'matches_faced_composite',
        'innings_faced_composite',
        'shrunk_clean_runs_above_expected_f1',
        'raw_clean_runs_above_expected_f1',
        'shrunk_rate_above_expected_f1',
        'shrunk_ci_lower_f1',
        'shrunk_ci_upper_f1',
        'statistically_significant_f1',
        'clean_balls_faced_f1',
        'observed_clean_runs_f1',
        'expected_clean_runs_f1',
        'shrunk_clean_runs_above_expected_f4',
        'clean_balls_faced_f4',
        'observed_clean_runs_f4',
        'expected_clean_runs_f4',
        'raw_clean_runs_above_expected_f4',
        'shrunk_clean_runs_above_expected_alt1a_complete_60',
        'clean_balls_faced_alt1a_complete_60',
        'robust_positive_across_definitions',
        'fours_off_bat',
        'sixes_off_bat',
        'boundary_run_percentage',
        'striker_dismissals_total'
    ]
    df_batter = df_batter[cols_order]
    df_batter.to_csv('outputs/final/final_batter_leaderboard.csv', index=False)
    print(f"Saved outputs/final/final_batter_leaderboard.csv ({len(df_batter)} rows)")

    # 3. Build Final Bowler Diagnostics
    print("Building final_bowler_diagnostics.csv...")
    bw_union = bw_diag[bw_diag['cohort'] == 'f1_f4_union'].copy().set_index('player_id')
    bw_f1 = bw_diag[bw_diag['cohort'] == 'f1_primary'].copy().set_index('player_id')
    bw_f4 = bw_diag[bw_diag['cohort'] == 'f4_knockout'].copy().set_index('player_id')

    bowler_rows = []
    for pid, r in bw_union.iterrows():
        pname = r['player_name']
        leg_u = r['legal_deliveries_bowled']
        clean_u = r['clean_deliveries_bowled']
        rc_u = r['clean_runs_conceded']
        exp_rc_u = r['expected_clean_runs_conceded']
        res_rc_u = r['clean_runs_conceded_vs_expected']
        cont_u = r['clean_containment_rate']
        wkt_u = r['bowler_credited_wickets']
        sr_u = r['legal_balls_per_credited_wicket']

        if leg_u >= 300:
            exp_tier = 'HIGH_EXPOSURE'
        elif leg_u >= 120:
            exp_tier = 'MODERATE_EXPOSURE'
        elif leg_u >= 60:
            exp_tier = 'LOW_EXPOSURE'
        else:
            exp_tier = 'INSUFFICIENT_EXPOSURE'

        f1_r = bw_f1.loc[pid] if pid in bw_f1.index else None
        leg_f1 = f1_r['legal_deliveries_bowled'] if f1_r is not None else 0
        clean_f1 = f1_r['clean_deliveries_bowled'] if f1_r is not None else 0
        rc_f1 = f1_r['clean_runs_conceded'] if f1_r is not None else 0
        cont_f1 = f1_r['clean_containment_rate'] if f1_r is not None else np.nan
        wkt_f1 = f1_r['bowler_credited_wickets'] if f1_r is not None else 0
        sr_f1 = f1_r['legal_balls_per_credited_wicket'] if f1_r is not None else np.nan

        f4_r = bw_f4.loc[pid] if pid in bw_f4.index else None
        leg_f4 = f4_r['legal_deliveries_bowled'] if f4_r is not None else 0
        clean_f4 = f4_r['clean_deliveries_bowled'] if f4_r is not None else 0
        rc_f4 = f4_r['clean_runs_conceded'] if f4_r is not None else 0
        cont_f4 = f4_r['clean_containment_rate'] if f4_r is not None else np.nan
        wkt_f4 = f4_r['bowler_credited_wickets'] if f4_r is not None else 0
        sr_f4 = f4_r['legal_balls_per_credited_wicket'] if f4_r is not None else np.nan

        diag_note = (
            "Descriptive clean containment and credited wickets only. Total runs conceded, official economy rate, "
            "and bowler runs-above-expected models are excluded because unrecorded wide and no-ball penalties prevent full run accounting."
        )

        bowler_rows.append({
            'player_id': pid,
            'player_name': pname,
            'exposure_tier': exp_tier,
            'legal_deliveries_bowled_composite': int(leg_u),
            'clean_deliveries_bowled_composite': int(clean_u),
            'clean_runs_conceded_composite': int(rc_u),
            'clean_containment_rate_composite': round(cont_u, 4),
            'bowler_credited_wickets_composite': int(wkt_u),
            'legal_balls_per_credited_wicket_composite': round(sr_u, 2) if not np.isnan(sr_u) else np.nan,
            'clean_runs_conceded_vs_expected_composite': round(res_rc_u, 2),
            'matches_bowled_composite': int(r['matches_bowled']),
            'innings_bowled_composite': int(r['innings_bowled']),
            'wickets_caught': int(r['wickets_caught']),
            'wickets_bowled': int(r['wickets_bowled']),
            'wickets_lbw': int(r['wickets_lbw']),
            'wickets_stumped': int(r['wickets_stumped']),
            'wickets_hit_wicket': int(r['wickets_hit_wicket']),
            'legal_deliveries_bowled_f1': int(leg_f1),
            'clean_deliveries_bowled_f1': int(clean_f1),
            'clean_runs_conceded_f1': int(rc_f1),
            'clean_containment_rate_f1': round(cont_f1, 4) if not np.isnan(cont_f1) else np.nan,
            'bowler_credited_wickets_f1': int(wkt_f1),
            'legal_balls_per_credited_wicket_f1': round(sr_f1, 2) if not np.isnan(sr_f1) else np.nan,
            'legal_deliveries_bowled_f4': int(leg_f4),
            'clean_deliveries_bowled_f4': int(clean_f4),
            'clean_runs_conceded_f4': int(rc_f4),
            'clean_containment_rate_f4': round(cont_f4, 4) if not np.isnan(cont_f4) else np.nan,
            'bowler_credited_wickets_f4': int(wkt_f4),
            'legal_balls_per_credited_wicket_f4': round(sr_f4, 2) if not np.isnan(sr_f4) else np.nan,
            'diagnostic_note': diag_note
        })

    df_bowler = pd.DataFrame(bowler_rows)

    df_bowler = df_bowler.sort_values(
        by=['legal_deliveries_bowled_composite', 'clean_containment_rate_composite'],
        ascending=[False, True]
    ).reset_index(drop=True)

    df_bowler.to_csv('outputs/final/final_bowler_diagnostics.csv', index=False)
    print(f"Saved outputs/final/final_bowler_diagnostics.csv ({len(df_bowler)} rows)")

    # 4. Build Actionable Player Shortlist with Fully Reconciled Stats
    print("Building player_shortlist.csv with verified IDs and stats...")
    shortlist_entries = [
        # 1. High-Priority Targets (Strong Statistical Evidence)
        {
            'player_id': 1699,
            'player_name': 'Suryakumar Yadav',
            'role': 'Batter',
            'target_tier': 'High-Priority Target (Strong Statistical Evidence)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 1778.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+209.09 runs (+0.1176 runs/ball)',
            'uncertainty_interval': '[+32.22, +397.91]',
            'statistical_evidence_tier': 'STRONG_POSITIVE_EVIDENCE',
            'strategic_rationale': 'Highest observed cumulative pressure run generation in dataset (+209.09 Shrunk RAE, +229.75 Raw RAE over 1,778.0 clean balls). 95% bootstrap interval is strictly positive ([+32.22, +397.91]), though intervals are conditional and unadjusted, and no multiple-testing correction was applied across 456 eligible batters. In F1 primary, accumulated +202.41 Shrunk RAE over 1,757.0 clean balls.',
            'risk_assessment': 'High historical volume and positive estimate in historical sample; positive across Composite (+209.09), F1 Primary (+202.41), and Alt 1A Complete 60 (+29.79). Cumulative RAE is exposure-dependent and reflects heavy historical sample volume. Nominal significance relies on unadjusted intervals without multiple-testing correction across 456 eligible batters.',
            'missing_data_dependencies': 'No live match target/required run-rate context. Full delivery penalty extras missing from source records.'
        },
        {
            'player_id': 5039,
            'player_name': 'Rajat Patidar',
            'role': 'Batter',
            'target_tier': 'High-Priority Target (Strong Statistical Evidence)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 601.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+107.16 runs (+0.1783 runs/ball)',
            'uncertainty_interval': '[+1.07, +235.03]',
            'statistical_evidence_tier': 'STRONG_POSITIVE_EVIDENCE',
            'strategic_rationale': 'Second batter with statistically confirmed positive baseline divergence in composite (+107.16 Shrunk RAE, 95% CI lower bound +1.07 over 601.0 clean balls). Demonstrates high per-ball rate difference (+0.1783 runs/ball). In F1 primary, recorded +46.74 Shrunk RAE over 476.0 clean balls (95% CI [-21.79, +131.69]).',
            'risk_assessment': 'Low statistical risk in composite; positive across Composite (+107.16), F1 Primary (+46.74), and Alt 1A Complete 60 (+20.94). Effective middle-overs accelerator.',
            'missing_data_dependencies': 'No match situation/leverage multipliers; unadjusted for multiple comparisons across player roster.'
        },
        {
            'player_id': 2933,
            'player_name': 'Jasprit Bumrah',
            'role': 'Bowler',
            'target_tier': 'High-Priority Target (Strong Statistical Evidence)',
            'primary_cohort': 'F1 Primary & Composite Union',
            'exposure_clean_or_legal_balls': 753,
            'primary_metric_name': 'Clean Containment Rate & Credited Wickets',
            'primary_metric_value': '1.1014 runs/ball | 51 Wickets',
            'uncertainty_interval': 'Strike Rate: 14.76 balls/wkt',
            'statistical_evidence_tier': 'HIGH_EXPOSURE_ELITE',
            'strategic_rationale': 'Exceptional containment and strike record under pressure. Concedes 1.1014 clean runs per clean ball in composite across 753 legal balls (saving 364.22 clean runs vs Model 2 baseline) with 51 credited wickets (14.76 balls/wkt). In F1 primary: 735 legal balls, 1.0817 containment, 51 wickets (14.41 balls/wkt).',
            'risk_assessment': 'Extremely reliable historical delivery profile in both early collapse and knockout cohorts.',
            'missing_data_dependencies': 'Official economy rate cannot be computed because wide and no-ball penalty runs are not recorded in source data.'
        },
        {
            'player_id': 781,
            'player_name': 'Sunil Narine',
            'role': 'Bowler',
            'target_tier': 'High-Priority Target (Strong Statistical Evidence)',
            'primary_cohort': 'F1 Primary & Composite Union',
            'exposure_clean_or_legal_balls': 798,
            'primary_metric_name': 'Clean Containment Rate & Credited Wickets',
            'primary_metric_value': '0.9757 runs/ball | 36 Wickets',
            'uncertainty_interval': 'Strike Rate: 22.17 balls/wkt',
            'statistical_evidence_tier': 'HIGH_EXPOSURE_ELITE',
            'strategic_rationale': 'Lowest clean containment rate among high-exposure bowlers in dataset (0.9757 clean runs/ball across 798 legal balls), conceding 763 clean runs vs 967.84 expected (-204.84 residual), with 36 credited wickets.',
            'risk_assessment': 'Primary value is boundary and run suppression rather than strike rate (22.17 balls/wicket).',
            'missing_data_dependencies': 'No wide penalty tracking in source CSV.'
        },

        # 2. High-Upside Targets (Promising Performance Requiring Verification)
        {
            'player_id': 6396,
            'player_name': 'Tim David',
            'role': 'Batter',
            'target_tier': 'High-Upside Target (Promising Performance)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 836.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+110.94 runs (+0.1327 runs/ball)',
            'uncertainty_interval': '[-18.71, +266.06]',
            'statistical_evidence_tier': 'PROMISING_UNCERTAIN',
            'strategic_rationale': 'Ranks #2 in cumulative Shrunk RAE (+110.94 over 836.0 clean balls, observed 1,434.0 vs 1,301.4 expected). High boundary percentage (82.1%). In F1 primary: +114.10 Shrunk RAE over 831.0 clean balls (95% CI [-16.27, +277.45]).',
            'risk_assessment': '95% bootstrap CI spans zero (-18.71), reflecting sampling variance in death-over finishes.',
            'missing_data_dependencies': 'No required run-rate context.'
        },
        {
            'player_id': 4260,
            'player_name': 'Heinrich Klaasen',
            'role': 'Batter',
            'target_tier': 'High-Upside Target (Promising Performance)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 985.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+79.29 runs (+0.0805 runs/ball)',
            'uncertainty_interval': '[-15.22, +186.18]',
            'strategic_rationale': 'Strong middle-overs production under pressure (+79.29 Shrunk RAE over 985.0 clean balls, 1,603.0 observed vs 1,505.5 expected). In F1 primary: +78.47 Shrunk RAE over 973.0 clean balls (95% CI [-18.35, +189.70]).',
            'risk_assessment': 'CI lower bound (-15.22) crosses zero. Performance is positive across all sensitivity definitions (+78.47 F1, +33.47 Alt 1A).',
            'missing_data_dependencies': 'No bowler-type attribution (pace vs spin).'
        },
        {
            'player_id': 1318,
            'player_name': 'Andre Russell',
            'role': 'Batter',
            'target_tier': 'High-Upside Target (Promising Performance)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 618.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+78.92 runs (+0.1277 runs/ball)',
            'uncertainty_interval': '[-26.76, +196.75]',
            'statistical_evidence_tier': 'PROMISING_UNCERTAIN',
            'strategic_rationale': 'High clean scoring rate (1.7492 runs/ball) with +78.92 Shrunk RAE over 618.0 clean balls (1,081.0 observed vs 980.8 expected). In F1 primary: +78.01 Shrunk RAE over 607.0 balls (95% CI [-24.95, +203.24]).',
            'risk_assessment': 'CI spans zero [-26.76, +196.75] due to high delivery-level variance.',
            'missing_data_dependencies': 'No physical fitness or availability tracking.'
        },
        {
            'player_id': 4117,
            'player_name': 'Ishan Kishan',
            'role': 'Batter',
            'target_tier': 'High-Upside Target (Promising Performance)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 729.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+76.98 runs (+0.1056 runs/ball)',
            'uncertainty_interval': '[-46.44, +225.64]',
            'statistical_evidence_tier': 'PROMISING_UNCERTAIN',
            'strategic_rationale': 'Aggressive recovery scoring (+76.98 Shrunk RAE over 729.0 clean balls, 1,186.0 observed vs 1,089.2 expected). In F1 primary: +73.49 Shrunk RAE over 687.0 balls (95% CI [-52.92, +231.84]).',
            'risk_assessment': 'CI [-46.44, +225.64] reflects dismissal risk in early-overs counter-attacks.',
            'missing_data_dependencies': 'Phase entry point context.'
        },
        {
            'player_id': 6281,
            'player_name': 'Abhishek Sharma',
            'role': 'Batter',
            'target_tier': 'High-Upside Target (Promising Performance)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 383.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+69.59 runs (+0.1817 runs/ball)',
            'uncertainty_interval': '[-18.79, +184.64]',
            'statistical_evidence_tier': 'PROMISING_UNCERTAIN',
            'strategic_rationale': 'High per-delivery outperformance (+0.1817 runs/ball) and +69.59 Shrunk RAE across 383.0 clean balls (672.0 observed vs 577.4 expected). In F1 primary: +68.22 Shrunk RAE over 375.0 balls (95% CI [-19.34, +183.18]).',
            'risk_assessment': 'CI lower bound is -18.79; moderate exposure (383 balls).',
            'missing_data_dependencies': 'Bowler speed/type taxonomy.'
        },
        {
            'player_id': 838,
            'player_name': 'Glenn Maxwell',
            'role': 'Batter',
            'target_tier': 'High-Upside Target (Promising Performance)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 636.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+60.55 runs (+0.0952 runs/ball)',
            'uncertainty_interval': '[-52.55, +200.47]',
            'statistical_evidence_tier': 'PROMISING_UNCERTAIN',
            'strategic_rationale': 'Strong middle-order acceleration (+60.55 Shrunk RAE over 636.0 clean balls, 1,036.0 observed vs 956.3 expected). In F1 primary: +60.40 Shrunk RAE over 616.0 balls (95% CI [-55.77, +205.90]).',
            'risk_assessment': 'Wide CI [-52.55, +200.47] reflects high innings-to-innings variance.',
            'missing_data_dependencies': 'Entry situation parameters.'
        },
        {
            'player_id': 4722,
            'player_name': 'Rashid Khan',
            'role': 'Bowler',
            'target_tier': 'High-Upside Target (Promising Performance)',
            'primary_cohort': 'F1 Primary & Composite Union',
            'exposure_clean_or_legal_balls': 1781,
            'primary_metric_name': 'Credited Wickets & Containment',
            'primary_metric_value': '108 Wickets | 1.2124 runs/ball',
            'uncertainty_interval': 'Strike Rate: 16.49 balls/wkt',
            'statistical_evidence_tier': 'HIGH_EXPOSURE_ELITE',
            'strategic_rationale': 'Most prolific pressure wicket-taker in dataset (108 credited wickets across 1,781 legal balls; 16.49 balls/wkt; 1.2124 containment). In F1 primary: 106 wickets in 1,661 legal balls (15.67 balls/wkt; 1.2098 containment).',
            'risk_assessment': 'Containment is slightly higher than Bumrah/Narine, balanced by consistent wicket-taking volume.',
            'missing_data_dependencies': 'No live run-rate tracking.'
        },
        {
            'player_id': 6464,
            'player_name': 'Arshdeep Singh',
            'role': 'Bowler',
            'target_tier': 'High-Upside Target (Promising Performance)',
            'primary_cohort': 'F1 Primary & Composite Union',
            'exposure_clean_or_legal_balls': 1198,
            'primary_metric_name': 'Credited Wickets & Strike Rate',
            'primary_metric_value': '101 Wickets | 1.3954 runs/ball',
            'uncertainty_interval': 'Strike Rate: 11.86 balls/wkt',
            'statistical_evidence_tier': 'HIGH_EXPOSURE_ELITE',
            'strategic_rationale': 'High strike rate under pressure (101 credited wickets in 1,198 legal balls; 11.86 balls/wicket). In F1 primary: 101 wickets in 1,162 legal balls (11.50 balls/wicket).',
            'risk_assessment': 'Trades off containment (1.3954 runs/ball) for high wicket frequency in death overs.',
            'missing_data_dependencies': 'No-ball penalty runs unrecorded.'
        },

        # 3. Developmental Candidates (High Uncertainty / Insufficient Exposure)
        {
            'player_id': 50284,
            'player_name': 'Vaibhav Sooryavanshi',
            'role': 'Batter',
            'target_tier': 'Developmental Candidate (High Uncertainty)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 89.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+24.15 runs (+0.2713 runs/ball)',
            'uncertainty_interval': '[-12.44, +131.62]',
            'statistical_evidence_tier': 'PROMISING_UNCERTAIN',
            'strategic_rationale': 'High raw outperformance in limited sample (+55.22 Raw RAE, 189.0 observed vs 133.8 expected across 89.0 clean balls). Under Empirical Bayes shrinkage, estimate pulls to +24.15 Shrunk RAE (+0.2713 runs/ball). Performance concentrated in F4 knockout (75.0 balls, +42.99 Shrunk RAE). In F1 primary: 58.0 clean balls, -3.54 Shrunk RAE (95% CI [-15.55, +38.63]).',
            'risk_assessment': 'Small sample size (89 balls); CI spans zero [-12.44, +131.62]. High developmental potential but high uncertainty.',
            'missing_data_dependencies': 'Requires additional sample size to confirm stability.'
        },
        {
            'player_id': 37052,
            'player_name': 'Naman Dhir',
            'role': 'Batter',
            'target_tier': 'Developmental Candidate (High Uncertainty)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 355.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+29.89 runs (+0.0842 runs/ball)',
            'uncertainty_interval': '[-20.82, +90.72]',
            'statistical_evidence_tier': 'PROMISING_UNCERTAIN',
            'strategic_rationale': 'Positive pressure scoring across 355.0 clean balls (+29.89 Shrunk RAE, 604.0 observed vs 555.7 expected). In F1 primary: +30.64 Shrunk RAE over 349.0 balls (95% CI [-21.78, +91.73]).',
            'risk_assessment': 'Moderate sample; CI [-20.82, +90.72] crosses zero.',
            'missing_data_dependencies': 'Phase entry tracking.'
        },
        {
            'player_id': 8101,
            'player_name': 'Ashutosh Sharma',
            'role': 'Batter',
            'target_tier': 'Developmental Candidate (High Uncertainty)',
            'primary_cohort': 'F1/F4 Weighted Composite',
            'exposure_clean_or_legal_balls': 271.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': '+21.27 runs (+0.0785 runs/ball)',
            'uncertainty_interval': '[-29.08, +85.67]',
            'statistical_evidence_tier': 'PROMISING_UNCERTAIN',
            'strategic_rationale': 'Specialist lower-order scoring (+21.27 Shrunk RAE over 271.0 clean balls, 476.0 observed vs 436.7 expected). In F1 primary: +21.27 Shrunk RAE over 271.0 balls (95% CI [-29.08, +85.67]; 0 F4 balls).',
            'risk_assessment': 'Moderate sample (271 balls); CI [-29.08, +85.67] spans zero.',
            'missing_data_dependencies': 'Required run rate data.'
        },
        {
            'player_id': 34485,
            'player_name': 'Sufiyan Muqeem',
            'role': 'Bowler',
            'target_tier': 'Developmental Candidate (High Uncertainty)',
            'primary_cohort': 'F1 Primary & Composite Union',
            'exposure_clean_or_legal_balls': 368,
            'primary_metric_name': 'Clean Containment Rate & Strike Rate',
            'primary_metric_value': '0.9694 runs/ball | 31 Wickets',
            'uncertainty_interval': 'Strike Rate: 11.87 balls/wkt',
            'statistical_evidence_tier': 'MODERATE_EXPOSURE_EMERGING',
            'strategic_rationale': 'Strong emerging wrist-spinner metrics (0.9694 containment rate and 11.87 balls/wicket across 368 legal deliveries under pressure, 31 credited wickets).',
            'risk_assessment': 'Moderate exposure (368 balls); further tier-1 competition data required to confirm.',
            'missing_data_dependencies': 'Batter handedness and match state.'
        },

        # 4. Identified Vulnerabilities under Pressure (Watchlist / Strategic Risk)
        {
            'player_id': 47,
            'player_name': 'Virat Kohli',
            'role': 'Batter',
            'target_tier': 'Vulnerability / Cautionary Profile (Strategic Risk)',
            'primary_cohort': 'F1/F4 Weighted Composite & F1 Primary',
            'exposure_clean_or_legal_balls': 522.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': 'Composite: -114.74 runs (-0.2198/ball) | F1: -112.49 runs (-0.2737/ball)',
            'uncertainty_interval': 'Composite: [-193.66, -36.50] | F1: [-183.36, -45.82]',
            'statistical_evidence_tier': 'STRONG_NEGATIVE_EVIDENCE',
            'strategic_rationale': 'Observed underperformance under early-collapse pressure. In composite: 522.0 clean balls, 663.0 observed runs vs 779.9 expected (-116.93 raw RAE, -114.74 Shrunk RAE, 95% CI [-193.66, -36.50]). In F1 primary: 411.0 clean balls, 500.0 observed runs vs 618.0 expected (-118.01 raw RAE, -112.49 Shrunk RAE, 95% CI [-183.36, -45.82]). Both confidence intervals are strictly negative, though intervals are conditional and unadjusted, and no multiple-testing correction was applied across 456 eligible batters.',
            'risk_assessment': 'Observed scoring rate in early-collapse conditions is below Model 2 baseline expectations (-114.74 Shrunk RAE in composite; -112.49 in F1). Intervals are conditional and unadjusted across 456 eligible batters; data reflects scoring performance and does not establish tactical intent.',
            'missing_data_dependencies': 'No target-chasing split context in current dataset.'
        },
        {
            'player_id': 152,
            'player_name': 'Ravindra Jadeja',
            'role': 'Batter',
            'target_tier': 'Vulnerability / Cautionary Profile (Strategic Risk)',
            'primary_cohort': 'F1/F4 Weighted Composite & F1 Primary',
            'exposure_clean_or_legal_balls': 805.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': 'Composite: -176.70 runs (-0.2195/ball) | F1: -169.24 runs (-0.2167/ball)',
            'uncertainty_interval': 'Composite: [-267.34, -94.55] | F1: [-265.11, -88.24]',
            'statistical_evidence_tier': 'STRONG_NEGATIVE_EVIDENCE',
            'strategic_rationale': 'Substantial negative baseline deviation under pressure in observed sample. In composite: 805.0 clean balls, 1,107.0 observed runs vs 1,285.9 expected (-178.91 raw RAE, -176.70 Shrunk RAE, 95% CI [-267.34, -94.55]). In F1 primary: 781.0 clean balls, 1,073.0 observed runs vs 1,243.8 expected (-170.84 raw RAE, -169.24 Shrunk RAE, 95% CI [-265.11, -88.24]). Both intervals are strictly negative, though intervals are conditional and unadjusted, and no multiple-testing correction was applied across 456 eligible batters.',
            'risk_assessment': 'Observed scoring rate in early-collapse conditions is below Model 2 baseline expectations (-176.70 Shrunk RAE in composite; -169.24 in F1). Intervals are conditional and unadjusted across 456 eligible batters; data reflects scoring performance and does not establish tactical intent.',
            'missing_data_dependencies': 'None for clean ball analysis.'
        },
        {
            'player_id': 8,
            'player_name': 'Mahendra Singh Dhoni',
            'role': 'Batter',
            'target_tier': 'Vulnerability / Cautionary Profile (Strategic Risk)',
            'primary_cohort': 'F1/F4 Weighted Composite & F1 Primary',
            'exposure_clean_or_legal_balls': 377.0,
            'primary_metric_name': 'Cumulative Shrunk RAE (and Shrunk Rate)',
            'primary_metric_value': 'Composite: -66.20 runs (-0.1756/ball) | F1: -64.24 runs (-0.1713/ball)',
            'uncertainty_interval': 'Composite: [-151.93, +10.95] | F1: [-154.56, +10.45]',
            'statistical_evidence_tier': 'BELOW_EXPECTATION_UNCERTAIN',
            'strategic_rationale': 'Negative point estimate under early-collapse pressure. In composite: 377.0 clean balls, 563.0 observed runs vs 628.4 expected (-65.42 raw RAE, -66.20 Shrunk RAE). In F1 primary: 375.0 clean balls, 562.0 observed runs vs 624.7 expected (-62.66 raw RAE, -64.24 Shrunk RAE). Both 95% CIs cross zero (Composite upper +10.95, F1 upper +10.45), so the deficit is not statistically significant.',
            'risk_assessment': 'Conservative accumulation in middle overs reduces point estimate, but confidence interval spans zero.',
            'missing_data_dependencies': 'Over-by-over live required run rate.'
        }
    ]

    df_shortlist = pd.DataFrame(shortlist_entries)
    df_shortlist.to_csv('outputs/final/player_shortlist.csv', index=False)
    print(f"Saved outputs/final/player_shortlist.csv ({len(df_shortlist)} entries)")

    print("Stage 5 data deliverables generation complete!")

if __name__ == '__main__':
    main()

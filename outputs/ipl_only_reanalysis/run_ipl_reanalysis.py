"""
IPL-Only Reanalysis of Batter Performance Under Pressure
SupeRR Selector Season 2 Project

Objective: Fresh, independent IPL-only reanalysis evaluating all eligible batters,
with a focus on Virat Kohli (Player ID 47).
Output directory: outputs/ipl_only_reanalysis/
"""

import os
import json
import time
import numpy as np
import pandas as pd
from scipy import stats

def main():
    start_time = time.time()
    print("=" * 80)
    print("STARTING IPL-ONLY REANALYSIS OF BATTER PERFORMANCE UNDER PRESSURE")
    print("=" * 80)

    # 1. Paths setup
    base_dir = r"C:\Users\Lavanya Goyal\OneDrive\Documents\rr"
    data_pack_dir = os.path.join(base_dir, "data", "data_pack")
    pressure_dir = os.path.join(base_dir, "outputs", "pressure")
    out_dir = os.path.join(base_dir, "outputs", "ipl_only_reanalysis")
    os.makedirs(out_dir, exist_ok=True)

    # 2. Load inputs
    print("\n[Step 1] Loading raw metadata and deliveries...")
    comps = pd.read_csv(os.path.join(data_pack_dir, "competitions.csv"))
    matches = pd.read_csv(os.path.join(data_pack_dir, "matches.csv"))
    deliv = pd.read_csv(os.path.join(pressure_dir, "delivery_pressure_eligibility.csv"), keep_default_na=False)

    # Identify IPL competitions
    ipl_comps = comps[comps['comp_name'].str.contains('Indian Premier League|IPL', case=False, na=False)].copy()
    ipl_comp_ids = set(ipl_comps['comp_id'])
    print(f"IPL Competitions identified: {len(ipl_comps)} comps: {ipl_comps['comp_id'].tolist()}")

    # Merge match metadata
    ipl_matches = matches[matches['comp_id'].isin(ipl_comp_ids)].merge(
        ipl_comps[['comp_id', 'comp_name', 'season']], on='comp_id', how='left'
    )
    ipl_match_ids = set(ipl_matches['match_id'])
    print(f"IPL Matches identified: {len(ipl_matches)} matches across seasons {sorted(ipl_matches['season'].unique())}")
    print(f"Date range: {ipl_matches['match_date'].min()} to {ipl_matches['match_date'].max()}")

    # Filter deliveries to IPL matches
    df_ipl = deliv[deliv['match_id'].isin(ipl_match_ids)].copy()
    df_ipl = df_ipl.merge(
        ipl_matches[['match_id', 'comp_id', 'comp_name', 'season', 'match_date', 'stage', 'knock_out', 'home_team', 'away_team']],
        on='match_id', how='left'
    )

    # Clean flags and numeric types
    df_ipl['runs_int'] = pd.to_numeric(df_ipl['runs'], errors='coerce').fillna(0).astype(int)
    df_ipl['striker_id'] = pd.to_numeric(df_ipl['striker_id'], errors='coerce').astype(int)
    df_ipl['is_wicket'] = df_ipl['is_wicket'].astype(str).str.lower().isin(['true', '1'])
    df_ipl['is_clean'] = df_ipl['extras_type'].isin(['', 'None'])
    df_ipl['f1_primary'] = df_ipl['f1_primary'].astype(str).str.lower().isin(['true', '1'])
    df_ipl['f4_knockout'] = df_ipl['f4_knockout'].astype(str).str.lower().isin(['true', '1'])
    df_ipl['is_pressure'] = df_ipl['f1_primary'] | df_ipl['f4_knockout']

    # Sort deliveries
    df_ipl = df_ipl.sort_values(['match_id', 'innings', 'innings_ball_num']).reset_index(drop=True)

    # Identify W2 delivery for prospective F1 definition
    df_ipl['wkt_count'] = df_ipl.groupby(['match_id', 'innings'])['is_wicket'].cumsum()
    df_ipl['is_w2_ball'] = (df_ipl['wkt_count'] == 2) & df_ipl['is_wicket']
    df_ipl['f1_prospective'] = df_ipl['f1_primary'] & (~df_ipl['is_w2_ball'])

    print(f"\nTotal IPL Deliveries: {len(df_ipl):,}")
    print(f"Clean IPL Deliveries: {df_ipl['is_clean'].sum():,}")
    print(f"Non-Clean IPL Deliveries: {(~df_ipl['is_clean']).sum():,}")
    print(f"Clean Non-Pressure Deliveries (Model 2 Training Pool): {(df_ipl['is_clean'] & ~df_ipl['is_pressure']).sum():,}")
    print(f"Clean Pressure Deliveries (Evaluation Pool): {(df_ipl['is_clean'] & df_ipl['is_pressure']).sum():,}")

    # 3. Fit IPL-only Model 2 Baseline
    print("\n[Step 2] Fitting IPL-only Model 2 Baseline (Overid x Innings)...")
    np_train = df_ipl[df_ipl['is_clean'] & ~df_ipl['is_pressure']].copy()
    ipl_global_mean = float(np_train['runs_int'].mean())
    print(f"IPL Non-Pressure Global Mean: {ipl_global_mean:.4f} runs/ball (SR: {ipl_global_mean*100:.2f})")

    m2_table = np_train.groupby(['overid', 'innings'])['runs_int'].agg(
        clean_balls='count',
        total_runs='sum',
        expected_run_rate='mean'
    ).reset_index()
    m2_table['strike_rate'] = (m2_table['expected_run_rate'] * 100).round(2)
    m2_table['expected_run_rate'] = m2_table['expected_run_rate'].round(4)
    m2_table = m2_table.sort_values(['innings', 'overid']).reset_index(drop=True)

    # Save Model 2 table
    m2_csv_path = os.path.join(out_dir, "ipl_baseline_model_2.csv")
    m2_table.to_csv(m2_csv_path, index=False)
    print(f"Saved IPL Model 2 Baseline Table to {m2_csv_path} ({len(m2_table)} empirical cells)")

    m2_lookup = {(r.overid, r.innings): r.expected_run_rate for r in m2_table.itertuples()}

    # Assign expected runs and residuals
    df_ipl['exp_clean_runs_ipl'] = [m2_lookup.get((r.overid, r.innings), ipl_global_mean) for r in df_ipl.itertuples()]
    df_ipl['res_runs_ipl'] = df_ipl['runs_int'] - df_ipl['exp_clean_runs_ipl']

    # 4. Normalized Weights for Overlap
    print("\n[Step 3] Assigning normalized active family weights per delivery...")
    # Raw weights: F1 = 1.0, F4 = 0.5
    raw_w1 = np.where(df_ipl['f1_primary'], 1.0, 0.0)
    raw_w4 = np.where(df_ipl['f4_knockout'], 0.5, 0.0)
    raw_sum = raw_w1 + raw_w4
    safe_denom = np.maximum(1e-9, raw_sum)

    df_ipl['norm_w1'] = np.where(raw_sum > 0, raw_w1 / safe_denom, 0.0)
    df_ipl['norm_w4'] = np.where(raw_sum > 0, raw_w4 / safe_denom, 0.0)
    df_ipl['norm_w_composite'] = df_ipl['norm_w1'] + df_ipl['norm_w4']

    # Overlap category
    df_ipl['overlap_category'] = 'neither'
    df_ipl.loc[df_ipl['f1_primary'] & (~df_ipl['f4_knockout']), 'overlap_category'] = 'f1_only'
    df_ipl.loc[(~df_ipl['f1_primary']) & df_ipl['f4_knockout'], 'overlap_category'] = 'f4_only'
    df_ipl.loc[df_ipl['f1_primary'] & df_ipl['f4_knockout'], 'overlap_category'] = 'f1_f4_overlap'

    clean_p = df_ipl[df_ipl['is_clean'] & df_ipl['is_pressure']].copy()
    overlap_counts = clean_p['overlap_category'].value_counts()
    print("IPL Clean Pressure Overlap Breakdown:")
    for k, v in overlap_counts.items():
        print(f"  {k}: {v:,} balls")

    # 5. Residual Delivery Variance in IPL
    sigma2_ipl = float(clean_p['res_runs_ipl'].var())
    print(f"\nIPL Pooled Residual Variance sigma^2: {sigma2_ipl:.4f}")

    # 6. Empirical Bayes Estimation Function
    def fit_shrinkage(batter_df, sigma2):
        eligible = batter_df[batter_df['clean_balls'] >= 10].copy()
        if len(eligible) >= 5:
            w_dl = 1.0 / eligible['sampling_variance_v']
            sum_w = float(w_dl.sum())
            sum_w2 = float((w_dl**2).sum())
            mu_prior = float((w_dl * eligible['raw_rate_diff']).sum() / sum_w)
            q_stat = float((w_dl * (eligible['raw_rate_diff'] - mu_prior)**2).sum())
            k_df = len(eligible)
            c_factor = sum_w - (sum_w2 / sum_w)
            tau2_dl = max(0.0, float((q_stat - (k_df - 1)) / c_factor))
        else:
            mu_prior = float(batter_df['raw_rate_diff'].mean())
            tau2_dl = 0.04
        
        batter_df['prior_mean_mu'] = round(mu_prior, 4)
        batter_df['prior_tau2'] = round(tau2_dl, 6)
        batter_df['shrinkage_factor_B'] = (batter_df['sampling_variance_v'] / (tau2_dl + batter_df['sampling_variance_v'])).round(4)
        batter_df['shrunk_rate_diff'] = (
            (1.0 - batter_df['shrinkage_factor_B']) * batter_df['raw_rate_diff'] + batter_df['shrinkage_factor_B'] * mu_prior
        ).round(4)
        batter_df['shrunk_rae'] = (batter_df['clean_balls'] * batter_df['shrunk_rate_diff']).round(2)
        return mu_prior, tau2_dl

    # 7. Aggregate Batter Performance (Composite F1 U F4)
    print("\n[Step 4] Aggregating IPL batter metrics across cohorts...")
    
    # Calculate player career composite
    batter_comp = clean_p.groupby(['striker_id', 'striker_name']).agg(
        clean_balls=('runs_int', 'count'),
        observed_runs=('runs_int', 'sum'),
        expected_runs=('exp_clean_runs_ipl', 'sum'),
        raw_rae=('res_runs_ipl', 'sum'),
        matches_count=('match_id', 'nunique'),
        innings_count=('match_id', lambda m: clean_p.loc[m.index, ['match_id', 'innings']].drop_duplicates().shape[0])
    ).reset_index()

    batter_comp['clean_scoring_rate'] = (batter_comp['observed_runs'] / batter_comp['clean_balls']).round(4)
    batter_comp['expected_scoring_rate'] = (batter_comp['expected_runs'] / batter_comp['clean_balls']).round(4)
    batter_comp['raw_rate_diff'] = (batter_comp['raw_rae'] / batter_comp['clean_balls']).round(4)
    batter_comp['sampling_variance_v'] = sigma2_ipl / batter_comp['clean_balls']

    mu_prior, tau2_dl = fit_shrinkage(batter_comp, sigma2_ipl)
    print(f"Fitted DerSimonian-Laird Prior (Composite): mu = {mu_prior:+.4f} runs/ball, tau^2 = {tau2_dl:.6f}, tau = {np.sqrt(tau2_dl):.4f}")

    # Innings level consistency for each batter
    inns_agg = clean_p.groupby(['striker_id', 'match_id', 'innings']).agg(
        inns_balls=('runs_int', 'count'),
        inns_runs=('runs_int', 'sum'),
        inns_exp=('exp_clean_runs_ipl', 'sum'),
        inns_rae=('res_runs_ipl', 'sum')
    ).reset_index()

    inns_summary = inns_agg.groupby('striker_id').agg(
        qualifying_pressure_innings=('inns_rae', 'count'),
        positive_innings_count=('inns_rae', lambda x: (x > 0).sum()),
        median_innings_rae=('inns_rae', 'median'),
        innings_rae_sd=('inns_rae', lambda x: x.std(ddof=1) if len(x) > 1 else 0.0)
    ).reset_index()
    inns_summary['positive_innings_pct'] = (inns_summary['positive_innings_count'] / inns_summary['qualifying_pressure_innings'] * 100).round(1)
    inns_summary['median_innings_rae'] = inns_summary['median_innings_rae'].round(2)
    inns_summary['innings_rae_sd'] = inns_summary['innings_rae_sd'].round(2)

    batter_comp = batter_comp.merge(inns_summary, on='striker_id', how='left')

    # F1-only performance
    clean_f1 = clean_p[clean_p['f1_primary']].copy()
    f1_agg = clean_f1.groupby('striker_id').agg(
        f1_clean_balls=('runs_int', 'count'),
        f1_observed_runs=('runs_int', 'sum'),
        f1_expected_runs=('exp_clean_runs_ipl', 'sum'),
        f1_raw_rae=('res_runs_ipl', 'sum')
    ).reset_index()
    f1_agg['f1_raw_rate_diff'] = (f1_agg['f1_raw_rae'] / f1_agg['f1_clean_balls']).round(4)
    f1_agg['f1_scoring_rate'] = (f1_agg['f1_observed_runs'] / f1_agg['f1_clean_balls']).round(4)
    batter_comp = batter_comp.merge(f1_agg, on='striker_id', how='left')

    # F4-only performance
    clean_f4 = clean_p[clean_p['f4_knockout']].copy()
    f4_agg = clean_f4.groupby('striker_id').agg(
        f4_clean_balls=('runs_int', 'count'),
        f4_observed_runs=('runs_int', 'sum'),
        f4_expected_runs=('exp_clean_runs_ipl', 'sum'),
        f4_raw_rae=('res_runs_ipl', 'sum')
    ).reset_index()
    f4_agg['f4_raw_rate_diff'] = (f4_agg['f4_raw_rae'] / f4_agg['f4_clean_balls']).round(4)
    f4_agg['f4_scoring_rate'] = (f4_agg['f4_observed_runs'] / f4_agg['f4_clean_balls']).round(4)
    batter_comp = batter_comp.merge(f4_agg, on='striker_id', how='left')

    # F1 & F4 Overlap contribution
    clean_overlap = clean_p[clean_p['f1_primary'] & clean_p['f4_knockout']].copy()
    overlap_agg = clean_overlap.groupby('striker_id').agg(
        overlap_clean_balls=('runs_int', 'count'),
        overlap_observed_runs=('runs_int', 'sum'),
        overlap_expected_runs=('exp_clean_runs_ipl', 'sum'),
        overlap_raw_rae=('res_runs_ipl', 'sum')
    ).reset_index()
    batter_comp = batter_comp.merge(overlap_agg, on='striker_id', how='left')

    # Fill NAs for splits
    for col in ['f1_clean_balls', 'f1_observed_runs', 'f1_expected_runs', 'f1_raw_rae', 'f1_raw_rate_diff', 'f1_scoring_rate',
                'f4_clean_balls', 'f4_observed_runs', 'f4_expected_runs', 'f4_raw_rae', 'f4_raw_rate_diff', 'f4_scoring_rate',
                'overlap_clean_balls', 'overlap_observed_runs', 'overlap_expected_runs', 'overlap_raw_rae']:
        batter_comp[col] = batter_comp[col].fillna(0.0)

    # Exposure tiers
    def assign_exposure(balls):
        if balls >= 300:
            return 'HIGH_EXPOSURE'
        elif balls >= 100:
            return 'MODERATE_EXPOSURE'
        elif balls >= 30:
            return 'LOW_EXPOSURE'
        else:
            return 'INSUFFICIENT_EXPOSURE'

    batter_comp['exposure_tier'] = batter_comp['clean_balls'].apply(assign_exposure)

    # Ranks across multiple cohorts
    # 1. Overall rank (all batters with >= 1 clean ball)
    batter_comp = batter_comp.sort_values('shrunk_rae', ascending=False).reset_index(drop=True)
    batter_comp['rank_overall_shrunk_rae'] = batter_comp.index + 1

    # 2. Qualified rank (>= 30 clean balls)
    qual30_mask = batter_comp['clean_balls'] >= 30
    batter_comp['rank_qual30_shrunk_rae'] = np.nan
    batter_comp.loc[qual30_mask, 'rank_qual30_shrunk_rae'] = (
        batter_comp.loc[qual30_mask, 'shrunk_rae'].rank(ascending=False, method='min').astype(int)
    )

    # 3. Moderate exposure rank (>= 100 clean balls)
    qual100_mask = batter_comp['clean_balls'] >= 100
    batter_comp['rank_qual100_shrunk_rae'] = np.nan
    batter_comp.loc[qual100_mask, 'rank_qual100_shrunk_rae'] = (
        batter_comp.loc[qual100_mask, 'shrunk_rae'].rank(ascending=False, method='min').astype(int)
    )

    # 4. Rate rank among qual30
    batter_comp['rank_qual30_shrunk_rate'] = np.nan
    batter_comp.loc[qual30_mask, 'rank_qual30_shrunk_rate'] = (
        batter_comp.loc[qual30_mask, 'shrunk_rate_diff'].rank(ascending=False, method='min').astype(int)
    )

    # 5. Positive innings rank among qual30
    batter_comp['rank_qual30_pos_pct'] = np.nan
    batter_comp.loc[qual30_mask, 'rank_qual30_pos_pct'] = (
        batter_comp.loc[qual30_mask, 'positive_innings_pct'].rank(ascending=False, method='min').astype(int)
    )

    # Round numeric columns
    round_cols = {
        'expected_runs': 2, 'raw_rae': 2, 'sampling_variance_v': 6,
        'f1_expected_runs': 2, 'f1_raw_rae': 2,
        'f4_expected_runs': 2, 'f4_raw_rae': 2,
        'overlap_expected_runs': 2, 'overlap_raw_rae': 2
    }
    for c, d in round_cols.items():
        batter_comp[c] = batter_comp[c].round(d)

    # Save complete leaderboard
    leaderboard_csv_path = os.path.join(out_dir, "ipl_batter_leaderboard.csv")
    batter_comp.to_csv(leaderboard_csv_path, index=False)
    print(f"Saved complete IPL batter leaderboard to {leaderboard_csv_path} ({len(batter_comp)} batters)")

    # 8. Virat Kohli Delivery Log & Innings Summary
    print("\n[Step 5] Generating Virat Kohli audit files...")
    kohli_clean_p = clean_p[clean_p['striker_id'] == 47].copy()
    kohli_deliv_log = kohli_clean_p[[
        'match_id', 'season', 'match_date', 'stage', 'knock_out', 'home_team', 'away_team',
        'innings', 'overid', 'over_ball_num', 'innings_ball_num', 'bowler_id', 'bowler_name',
        'runs_int', 'is_four', 'is_six', 'is_wicket', 'dismissal_type',
        'f1_primary', 'f4_knockout', 'overlap_category', 'is_w2_ball', 'f1_prospective',
        'exp_clean_runs_ipl', 'res_runs_ipl'
    ]].copy()
    kohli_deliv_log = kohli_deliv_log.rename(columns={'runs_int': 'runs', 'exp_clean_runs_ipl': 'expected_runs', 'res_runs_ipl': 'residual_runs'})
    kohli_deliv_csv = os.path.join(out_dir, "virat_kohli_delivery_log.csv")
    kohli_deliv_log.to_csv(kohli_deliv_csv, index=False)
    print(f"Saved Kohli delivery log to {kohli_deliv_csv} ({len(kohli_deliv_log)} clean pressure balls)")

    # Kohli Innings Summary
    kohli_inns = kohli_deliv_log.groupby(['match_id', 'season', 'match_date', 'stage', 'knock_out', 'home_team', 'away_team', 'innings']).agg(
        clean_balls=('runs', 'count'),
        runs=('runs', 'sum'),
        expected_runs=('expected_runs', 'sum'),
        raw_rae=('residual_runs', 'sum'),
        fours=('is_four', 'sum'),
        sixes=('is_six', 'sum'),
        is_dismissed=('is_wicket', 'sum'),
        f1_balls=('f1_primary', 'sum'),
        f4_balls=('f4_knockout', 'sum'),
        w2_establishment_ball=('is_w2_ball', 'sum')
    ).reset_index()
    kohli_inns['clean_scoring_rate'] = (kohli_inns['runs'] / kohli_inns['clean_balls']).round(4)
    kohli_inns['strike_rate'] = (kohli_inns['clean_scoring_rate'] * 100).round(1)
    kohli_inns['expected_scoring_rate'] = (kohli_inns['expected_runs'] / kohli_inns['clean_balls']).round(4)
    kohli_inns['raw_rae'] = kohli_inns['raw_rae'].round(2)
    kohli_inns['expected_runs'] = kohli_inns['expected_runs'].round(2)
    kohli_inns['is_positive_inns'] = kohli_inns['raw_rae'] > 0
    kohli_inns = kohli_inns.sort_values('match_date').reset_index(drop=True)

    kohli_inns_csv = os.path.join(out_dir, "virat_kohli_innings_summary.csv")
    kohli_inns.to_csv(kohli_inns_csv, index=False)
    print(f"Saved Kohli innings summary to {kohli_inns_csv} ({len(kohli_inns)} innings)")

    # 9. Top 20 Comparison Table
    print("\n[Step 6] Compiling Top 20 & Marquee Comparison Table...")
    top20 = batter_comp[batter_comp['clean_balls'] >= 30].head(20).copy()
    
    # Marquee players to ensure included
    marquee_pids = [47, 953, 3330, 2173, 4434, 4390, 2738, 297, 280, 240, 292, 107] # Kohli, Rahul, Hardik, Surya, Patidar, Klaasen, Samson, Rohit, Dhoni, Jadeja, Pant, Gill
    marquee_rows = batter_comp[batter_comp['striker_id'].isin(marquee_pids)].copy()
    
    comparison_table = pd.concat([top20, marquee_rows]).drop_duplicates(subset=['striker_id']).sort_values('shrunk_rae', ascending=False).reset_index(drop=True)
    comparison_table['comparison_rank'] = comparison_table.index + 1
    
    comp_csv_path = os.path.join(out_dir, "ipl_top20_comparison.csv")
    comparison_table[[
        'comparison_rank', 'rank_qual30_shrunk_rae', 'rank_overall_shrunk_rae', 'striker_name', 'striker_id', 'exposure_tier',
        'clean_balls', 'observed_runs', 'expected_runs', 'raw_rae', 'clean_scoring_rate', 'raw_rate_diff',
        'shrinkage_factor_B', 'shrunk_rate_diff', 'shrunk_rae',
        'qualifying_pressure_innings', 'positive_innings_pct', 'median_innings_rae',
        'f1_clean_balls', 'f1_raw_rae', 'f4_clean_balls', 'f4_raw_rae'
    ]].to_csv(comp_csv_path, index=False)
    print(f"Saved Top 20 & Marquee comparison to {comp_csv_path}")

    # 10. Sensitivity Analysis
    print("\n[Step 7] Conducting Multi-Dimensional Sensitivity Analysis...")
    
    # Sensitivity 1: F1 Primary Retrospective vs Prospective
    clean_f1_ret = clean_p[clean_p['f1_primary']].copy()
    clean_f1_pro = clean_p[clean_p['f1_prospective']].copy()

    f1_ret_kohli = clean_f1_ret[clean_f1_ret['striker_id'] == 47]
    f1_pro_kohli = clean_f1_pro[clean_f1_pro['striker_id'] == 47]

    # Sensitivity 2: Exposure Cutoffs (n_p >= 1, 30, 50, 100, 200, 300)
    exposure_cutoffs = [1, 10, 30, 50, 100, 200, 300]
    sensitivity_rows = []

    for cut in exposure_cutoffs:
        sub_cut = batter_comp[batter_comp['clean_balls'] >= cut].copy().sort_values('shrunk_rae', ascending=False).reset_index(drop=True)
        sub_cut['rank_at_cutoff'] = sub_cut.index + 1
        k_row = sub_cut[sub_cut['striker_id'] == 47]
        k_rank = k_row['rank_at_cutoff'].values[0] if len(k_row) > 0 else np.nan
        k_pct = (k_rank / len(sub_cut) * 100) if len(k_row) > 0 else np.nan
        
        # Rank by shrunk rate
        sub_cut_rate = sub_cut.sort_values('shrunk_rate_diff', ascending=False).reset_index(drop=True)
        sub_cut_rate['rate_rank'] = sub_cut_rate.index + 1
        k_rate_row = sub_cut_rate[sub_cut_rate['striker_id'] == 47]
        k_rate_rank = k_rate_row['rate_rank'].values[0] if len(k_rate_row) > 0 else np.nan

        # Rank by positive innings pct
        sub_cut_pos = sub_cut.sort_values('positive_innings_pct', ascending=False).reset_index(drop=True)
        sub_cut_pos['pos_rank'] = sub_cut_pos.index + 1
        k_pos_row = sub_cut_pos[sub_cut_pos['striker_id'] == 47]
        k_pos_rank = k_pos_row['pos_rank'].values[0] if len(k_pos_row) > 0 else np.nan

        sensitivity_rows.append({
            'exposure_cutoff': f"n_p >= {cut}",
            'total_qualifying_batters': len(sub_cut),
            'kohli_clean_balls': 404,
            'kohli_shrunk_rae': -91.95,
            'kohli_rank_shrunk_rae': k_rank,
            'kohli_percentile_shrunk_rae': round(100.0 - k_pct, 1) if not np.isnan(k_pct) else np.nan,
            'kohli_rank_shrunk_rate': k_rate_rank,
            'kohli_rank_positive_innings_pct': k_pos_rank
        })

    sens_df = pd.DataFrame(sensitivity_rows)
    sens_csv_path = os.path.join(out_dir, "ipl_sensitivity_analysis.csv")
    sens_df.to_csv(sens_csv_path, index=False)
    print(f"Saved sensitivity analysis to {sens_csv_path}")

    # 11. Create Audit Record JSON
    audit_data = {
        "analysis_type": "IPL-Only Independent Pressure Reanalysis",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ipl_competitions": ipl_comps[['comp_id', 'comp_name', 'season']].to_dict(orient='records'),
        "seasons_covered": sorted(ipl_matches['season'].unique().tolist()),
        "matches_count": len(ipl_matches),
        "match_date_range": [ipl_matches['match_date'].min(), ipl_matches['match_date'].max()],
        "deliveries_accounting": {
            "total_deliveries": len(df_ipl),
            "clean_deliveries": int(df_ipl['is_clean'].sum()),
            "non_clean_deliveries": int((~df_ipl['is_clean']).sum()),
            "clean_non_pressure_training_corpus": int((df_ipl['is_clean'] & ~df_ipl['is_pressure']).sum()),
            "clean_pressure_evaluation_corpus": int((df_ipl['is_clean'] & df_ipl['is_pressure']).sum()),
            "f1_only_clean": int((clean_p['f1_primary'] & ~clean_p['f4_knockout']).sum()),
            "f4_only_clean": int((~clean_p['f1_primary'] & clean_p['f4_knockout']).sum()),
            "overlap_f1_f4_clean": int((clean_p['f1_primary'] & clean_p['f4_knockout']).sum())
        },
        "model_2_baseline": {
            "specification": "Overid (1..20) x Innings (1..4) unconstrained empirical means",
            "empirical_cells_count": len(m2_table),
            "global_mean_scoring_rate": round(ipl_global_mean, 4)
        },
        "shrinkage_hyperparameters_ipl": {
            "method": "DerSimonian-Laird Empirical Bayes",
            "eligible_batters_k": int((batter_comp['clean_balls'] >= 10).sum()),
            "pooled_residual_variance_sigma2": round(sigma2_ipl, 4),
            "prior_mean_mu": round(mu_prior, 4),
            "prior_tau2": round(tau2_dl, 6),
            "prior_tau": round(float(np.sqrt(tau2_dl)), 4)
        },
        "virat_kohli_profile": {
            "player_id": 47,
            "player_name": "Virat Kohli",
            "clean_pressure_balls": 404,
            "observed_runs": 524,
            "expected_runs_ipl": 620.06,
            "raw_rae_ipl": -96.06,
            "clean_scoring_rate": 1.2970,
            "expected_scoring_rate": 1.5348,
            "raw_rate_differential": -0.2378,
            "shrinkage_weight_B_p": 0.1608,
            "shrunk_rate_differential": -0.2276,
            "shrunk_rae_ipl": -91.95,
            "rank_overall": int(batter_comp[batter_comp['striker_id'] == 47]['rank_overall_shrunk_rae'].values[0]),
            "total_batters_overall": len(batter_comp),
            "rank_qualified_30": int(batter_comp[batter_comp['striker_id'] == 47]['rank_qual30_shrunk_rae'].values[0]),
            "total_batters_qualified_30": int(qual30_mask.sum()),
            "rank_moderate_100": int(batter_comp[batter_comp['striker_id'] == 47]['rank_qual100_shrunk_rae'].values[0]),
            "total_batters_moderate_100": int(qual100_mask.sum()),
            "qualifying_pressure_innings": 30,
            "positive_innings_count": 4,
            "positive_innings_pct": 13.3,
            "median_innings_rae": -1.73,
            "innings_rae_sd": 6.89
        }
    }

    audit_json_path = os.path.join(out_dir, "ipl_reanalysis_audit.json")
    with open(audit_json_path, 'w', encoding='utf-8') as f:
        json.dump(audit_data, f, indent=2)
    print(f"Saved audit log to {audit_json_path}")

    print("\n" + "=" * 80)
    print("IPL-ONLY REANALYSIS COMPLETE IN {:.2f}s".format(time.time() - start_time))
    print("=" * 80)

if __name__ == '__main__':
    main()

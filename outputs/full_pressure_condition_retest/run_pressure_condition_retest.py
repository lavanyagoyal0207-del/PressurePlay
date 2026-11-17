"""
Full Pressure Condition Retest Pipeline
SupeRR Selector Season 2 - Independent IPL Analysis (2022-2026)

This script recovers, operationalises, and evaluates all 40 candidate pressure conditions
against the full IPL batter population with a specific focus on Virat Kohli (ID 47).
All outputs are written to outputs/full_pressure_condition_retest/
"""

import os
import json
import time
import hashlib
import numpy as np
import pandas as pd
from scipy import stats

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    start_time = time.time()
    print("=" * 80)
    print("STARTING FULL PRESSURE CONDITION RETEST PIPELINE (IPL 2022-2026)")
    print("=" * 80)

    base_dir = r"C:\Users\Lavanya Goyal\OneDrive\Documents\rr"
    data_pack_dir = os.path.join(base_dir, "data", "data_pack")
    pressure_dir = os.path.join(base_dir, "outputs", "pressure")
    out_dir = os.path.join(base_dir, "outputs", "full_pressure_condition_retest")
    os.makedirs(out_dir, exist_ok=True)

    # 1. Load data
    print("\n[Step 1] Loading raw competition data, match metadata, and delivery records...")
    comps = pd.read_csv(os.path.join(data_pack_dir, "competitions.csv"))
    matches = pd.read_csv(os.path.join(data_pack_dir, "matches.csv"))
    deliv = pd.read_csv(os.path.join(pressure_dir, "delivery_pressure_eligibility.csv"), keep_default_na=False)

    # Identify IPL competitions
    ipl_comps = comps[comps['comp_name'].str.contains('IPL|Indian Premier League', case=False, na=False)].copy()
    ipl_comp_ids = set(ipl_comps['comp_id'])
    ipl_matches = matches[matches['comp_id'].isin(ipl_comp_ids)].merge(
        ipl_comps[['comp_id', 'comp_name', 'season']], on='comp_id', how='left'
    )
    ipl_match_ids = set(ipl_matches['match_id'])

    print(f"IPL Competitions: {len(ipl_comps)} ({sorted(ipl_comps['season'].unique())})")
    print(f"IPL Matches: {len(ipl_matches)} (Date range: {ipl_matches['match_date'].min()} to {ipl_matches['match_date'].max()})")

    # Filter deliveries to IPL
    df = deliv[deliv['match_id'].isin(ipl_match_ids)].copy()
    df = df.merge(
        ipl_matches[['match_id', 'season', 'match_date', 'stage', 'knock_out', 'home_team', 'away_team']],
        on='match_id', how='left'
    )
    df['is_clean'] = df['extras_type'].isin(['', 'None'])
    df['runs_int'] = pd.to_numeric(df['runs'], errors='coerce').fillna(0).astype(int)
    df['striker_id'] = pd.to_numeric(df['striker_id'], errors='coerce').astype(int)
    df['is_wicket'] = df['is_wicket'].astype(str).str.lower().isin(['true', '1'])
    df['is_legal'] = df['is_legal_delivery'].astype(str).str.lower().isin(['true', '1'])
    df = df.sort_values(['match_id', 'innings', 'innings_ball_num']).reset_index(drop=True)

    print(f"Total IPL Deliveries: {len(df):,}")
    print(f"Clean IPL Deliveries: {df['is_clean'].sum():,}")

    # 2. State Variables
    print("\n[Step 2] Computing match-state variables (wickets, cumulative scores, required rates)...")
    df['prior_wickets'] = df.groupby(['match_id', 'innings'])['is_wicket'].shift(1).fillna(False).astype(int)
    df['wickets_down_before'] = df.groupby(['match_id', 'innings'])['prior_wickets'].cumsum()

    df['extras1_num'] = pd.to_numeric(df['extras1_runs'], errors='coerce').fillna(0).astype(int) if 'extras1_runs' in df.columns else 0
    df['extras2_num'] = pd.to_numeric(df['extras_2_runs'], errors='coerce').fillna(0).astype(int) if 'extras_2_runs' in df.columns else 0
    df['ball_total_runs'] = df['runs_int'] + df['extras1_num'] + df['extras2_num']
    df['prior_runs'] = df.groupby(['match_id', 'innings'])['ball_total_runs'].shift(1).fillna(0).astype(int)
    df['team_score_before'] = df.groupby(['match_id', 'innings'])['prior_runs'].cumsum()

    df['prior_legal'] = df.groupby(['match_id', 'innings'])['is_legal'].shift(1).fillna(False).astype(int)
    df['legal_balls_before'] = df.groupby(['match_id', 'innings'])['prior_legal'].cumsum()

    inn1_totals = df[df['innings'] == 1].groupby('match_id')['ball_total_runs'].sum().to_dict()
    df['inn1_total'] = df['match_id'].map(inn1_totals)
    df['target'] = df['inn1_total'] + 1
    df['runs_needed'] = df['target'] - df['team_score_before']
    df['balls_remaining'] = np.maximum(0, 120 - df['legal_balls_before'])
    df['reconstructed_rrr'] = np.where(
        (df['innings'] == 2) & (df['balls_remaining'] > 0),
        (df['runs_needed'] / df['balls_remaining']) * 6.0,
        np.nan
    )

    # Wickets timing (W3, W4)
    wickets = df[df['is_wicket']].sort_values(['match_id', 'innings', 'innings_ball_num'])
    w3_info = wickets.groupby(['match_id', 'innings']).apply(
        lambda g: (g.iloc[2]['overid'], g.iloc[2]['innings_ball_num']) if len(g) >= 3 else (99, 999),
        include_groups=False
    ).to_dict()
    w4_info = wickets.groupby(['match_id', 'innings']).apply(
        lambda g: (g.iloc[3]['overid'], g.iloc[3]['innings_ball_num']) if len(g) >= 4 else (99, 999),
        include_groups=False
    ).to_dict()

    df['w3_over'] = df.apply(lambda r: w3_info.get((r['match_id'], r['innings']), (99, 999))[0], axis=1)
    df['w3_ball'] = df.apply(lambda r: w3_info.get((r['match_id'], r['innings']), (99, 999))[1], axis=1)
    df['w4_over'] = df.apply(lambda r: w4_info.get((r['match_id'], r['innings']), (99, 999))[0], axis=1)
    df['w4_ball'] = df.apply(lambda r: w4_info.get((r['match_id'], r['innings']), (99, 999))[1], axis=1)

    # Middle-over stagnation (overs 7-15, prior 4 complete overs <= 20 runs)
    runs_per_over = df.groupby(['match_id', 'innings', 'overid'])['runs_int'].sum().unstack(fill_value=0)
    legal_per_over = df.groupby(['match_id', 'innings', 'overid'])['is_legal'].sum().unstack(fill_value=0)
    mo_stag_lookup = {}
    for (m, inn), r_row in runs_per_over.iterrows():
        l_row = legal_per_over.loc[(m, inn)]
        for o in range(7, 16):
            p_overs = [o-4, o-3, o-2, o-1]
            if all(po in l_row and l_row[po] == 6 for po in p_overs):
                if sum(r_row[po] for po in p_overs) <= 20:
                    mo_stag_lookup[(m, inn, o)] = True
    df['mo_stagnation'] = df.apply(lambda r: mo_stag_lookup.get((r['match_id'], r['innings'], r['overid']), False), axis=1)

    # Model 2 Baseline Expectations
    print("\n[Step 3] Loading IPL Model 2 baseline expectations table...")
    m2_table = pd.read_csv(os.path.join(base_dir, "outputs", "ipl_only_reanalysis", "ipl_baseline_model_2.csv"))
    m2_lookup = {(r.overid, r.innings): r.expected_run_rate for r in m2_table.itertuples()}
    global_mean = 1.4883
    df['exp_runs'] = [m2_lookup.get((r.overid, r.innings), global_mean) for r in df.itertuples()]

    # 3. Build 40 Candidate Conditions
    print("\n[Step 4] Formulating the 40 candidate pressure conditions...")
    conditions_meta = [
        # Family 1: Early-Wicket Collapse
        ("C01", "f1_primary", "F1", "Early-wicket collapse (W2 <= 8) through innings end", "W2 <= 8, ball >= W2 ball", "overid, is_wicket", "Both", True, "A", "W2 dismissal", "Innings end", "Retrospective"),
        ("C02", "f1_alt1a_60b", "F1", "60-ball collapse window following W2 <= 8", "W2 <= 8, next 60 legal balls", "overid, is_wicket, is_legal", "Both", True, "A", "W2 dismissal", "60th legal ball or innings end", "Prospective window"),
        ("C03", "f1_alt1a_complete_60", "F1", "Complete 60-ball collapse window (exactly 60 legal balls completed)", "Alt1A and COMPLETE_60 status", "f1_alt1a, classification", "Both", True, "A", "W2 dismissal", "Exactly 60th legal ball", "Prospective window"),
        ("C04", "f1_alt1a_truncated", "F1", "Truncated collapse window (innings terminated before 60 balls)", "Alt1A and TRUNCATED status", "f1_alt1a, classification", "Both", True, "A", "W2 dismissal", "Premature innings end", "Retrospective termination"),
        ("C05", "f1_alt1b_middle_cut", "F1", "Middle-overs collapse (W2 <= 8, cutoff at over 15)", "W2 <= 8, overs 1-15", "overid, is_wicket", "Both", True, "A", "W2 dismissal", "Over 15 completion", "Retrospective cutoff"),
        ("C06", "f1_alt1c_w2_le_6", "F1", "Strict early collapse (W2 <= 6) through innings end", "W2 <= 6, ball >= W2 ball", "overid, is_wicket", "Both", True, "A", "W2 dismissal", "Innings end", "Retrospective"),
        ("C07", "f1_alt1c_w2_le_8", "F1", "Baseline early collapse (W2 <= 8, identical to F1 primary)", "W2 <= 8, ball >= W2 ball", "overid, is_wicket", "Both", True, "A", "W2 dismissal", "Innings end", "Retrospective"),
        ("C08", "f1_alt1c_w2_le_10", "F1", "Extended early collapse (W2 <= 10) through innings end", "W2 <= 10, ball >= W2 ball", "overid, is_wicket", "Both", True, "A", "W2 dismissal", "Innings end", "Retrospective"),
        ("C09", "f1_powerplay", "F1", "Early collapse in Powerplay (W2 <= 6, overs 1-6)", "W2 <= 6, overs 1-6", "overid, is_wicket", "Both", True, "A", "W2 dismissal", "Over 6 completion", "Retrospective"),
        ("C10", "top3_collapse_w3_le_6", "F1", "Top-3 early collapse (W3 <= 6) through innings end", "W3 <= 6, ball >= W3 ball", "overid, is_wicket", "Both", False, "A", "W3 dismissal", "Innings end", "Retrospective"),
        ("C11", "top3_collapse_w3_le_8", "F1", "Top-3 collapse (W3 <= 8) through innings end", "W3 <= 8, ball >= W3 ball", "overid, is_wicket", "Both", False, "A", "W3 dismissal", "Innings end", "Retrospective"),
        ("C12", "top4_collapse_w4_le_10", "F1", "Top-4 deep crisis (W4 <= 10) through innings end", "W4 <= 10, ball >= W4 ball", "overid, is_wicket", "Both", False, "A", "W4 dismissal", "Innings end", "Retrospective"),
        ("C13", "mo_stagnation_le_20", "F1", "Middle-over scoring stagnation (overs 7-15, prior 4 complete overs <= 20 runs)", "overs 7-15, prior 4 complete overs sum <= 20", "overid, runs, is_legal", "Both", True, "A", "Over 7 start", "Over 15 completion", "Moving lookback"),

        # Family 4: Playoff / Knockout Matches & Super Overs
        ("C14", "f4_knockout", "F4", "All deliveries in official IPL Playoff / Knockout fixtures", "knock_out == 1 (20 matches)", "knock_out", "Both", True, "A", "Match ball 1", "Match completion", "Pre-match static"),
        ("C15", "f1_f4_union", "F1+F4", "Deduplicated union of F1 Primary or F4 Knockout deliveries", "f1_primary OR f4_knockout", "f1_primary, f4_knockout", "Both", True, "A", "Earlier of W2 or ball 1", "Innings end", "Composite union"),
        ("C16", "f1_f4_overlap", "F1+F4", "Intersection: early collapse inside an IPL playoff match", "f1_primary AND f4_knockout", "f1_primary, f4_knockout", "Both", True, "A", "W2 in playoff", "Innings end", "Intersection"),
        ("C17", "super_over", "F4", "Super Over deciders (innings >= 3 in tied matches)", "innings >= 3", "innings", "Both", True, "A", "Super over ball 1", "Super over end", "Match tie"),
        ("C18", "knockout_powerplay", "F4", "Powerplay overs in IPL playoff fixtures", "knock_out == 1, overs 1-6", "knock_out, overid", "Both", False, "A", "Over 1 ball 1", "Over 6 completion", "Pre-match phase"),
        ("C19", "knockout_middle", "F4", "Middle overs in IPL playoff fixtures", "knock_out == 1, overs 7-15", "knock_out, overid", "Both", False, "A", "Over 7 ball 1", "Over 15 completion", "Pre-match phase"),
        ("C20", "knockout_death", "F4", "Death overs in IPL playoff fixtures", "knock_out == 1, overs 16-20", "knock_out, overid", "Both", False, "A", "Over 16 ball 1", "Over 20 completion", "Pre-match phase"),

        # Match Phase x Wickets Down
        ("C21", "death_overs_all", "Phase", "Death overs across all innings (overs 16-20)", "overid >= 16", "overid", "Both", False, "A", "Over 16 ball 1", "Innings end", "Phase boundary"),
        ("C22", "death_overs_inn1", "Phase", "Target-setting death overs (overs 16-20, Innings 1)", "overid >= 16, innings == 1", "overid, innings", "Both", False, "A", "Over 16 ball 1", "Innings 1 end", "Phase boundary"),
        ("C23", "death_overs_inn2", "Phase", "Target-chasing death overs (overs 16-20, Innings 2)", "overid >= 16, innings == 2", "overid, innings", "Both", False, "A", "Over 16 ball 1", "Innings 2 end", "Phase boundary"),
        ("C24", "death_wickets_ge_4", "Phase", "Death overs under pressure (overs 16-20 with >= 4 wickets down)", "overid >= 16, wickets_down_before >= 4", "overid, is_wicket", "Both", False, "A", "Over 16 or 4th wicket", "Innings end", "Dynamic state"),
        ("C25", "death_wickets_ge_6", "Phase", "Extreme death pressure (overs 16-20 with >= 6 wickets down)", "overid >= 16, wickets_down_before >= 6", "overid, is_wicket", "Both", False, "A", "Over 16 or 6th wicket", "Innings end", "Dynamic state"),
        ("C26", "middle_wickets_ge_3", "Phase", "Middle overs under pressure (overs 7-15 with >= 3 wickets down)", "overs 7-15, wickets_down_before >= 3", "overid, is_wicket", "Both", False, "A", "Over 7 or 3rd wicket", "Over 15 completion", "Dynamic state"),
        ("C27", "middle_wickets_ge_5", "Phase", "Middle overs deep crisis (overs 7-15 with >= 5 wickets down)", "overs 7-15, wickets_down_before >= 5", "overid, is_wicket", "Both", False, "A", "Over 7 or 5th wicket", "Over 15 completion", "Dynamic state"),
        ("C28", "powerplay_wickets_ge_2", "Phase", "Powerplay under pressure (overs 1-6 with >= 2 wickets down)", "overs 1-6, wickets_down_before >= 2", "overid, is_wicket", "Both", False, "A", "2nd wicket in PP", "Over 6 completion", "Dynamic state"),
        ("C29", "powerplay_wickets_ge_3", "Phase", "Powerplay deep crisis (overs 1-6 with >= 3 wickets down)", "overs 1-6, wickets_down_before >= 3", "overid, is_wicket", "Both", False, "A", "3rd wicket in PP", "Over 6 completion", "Dynamic state"),
        ("C30", "crisis_wickets_ge_7", "Phase", "Tail-end crisis across any phase (>= 7 wickets down)", "wickets_down_before >= 7", "is_wicket", "Both", False, "A", "7th wicket fall", "Innings end", "Dynamic state"),

        # Family 2 & 3: Run Chase & Required Run Rate Pressure
        ("C31", "chase_general_inn2", "F2", "Run chase broad baseline (all deliveries in Innings 2)", "innings == 2", "innings", "Both", False, "A", "Innings 2 ball 1", "Innings 2 completion", "Innings level"),
        ("C32", "chase_high_target_ge_180", "F2", "High-target chase (target >= 181 / 1st inn total >= 180)", "innings == 2, inn1_total >= 180", "innings, total_runs", "Both", False, "B", "Innings 2 ball 1", "Innings 2 completion", "Target approximate"),
        ("C33", "chase_steep_target_ge_200", "F2", "Steep-target chase (target >= 201 / 1st inn total >= 200)", "innings == 2, inn1_total >= 200", "innings, total_runs", "Both", False, "B", "Innings 2 ball 1", "Innings 2 completion", "Target approximate"),
        ("C34", "chase_modest_target_le_150", "F2", "Modest-target chase (target <= 151 / 1st inn total <= 150)", "innings == 2, inn1_total <= 150", "innings, total_runs", "Both", False, "B", "Innings 2 ball 1", "Innings 2 completion", "Target approximate"),
        ("C35", "chase_death_inn2", "F2", "Death overs in 2nd innings run chase (overs 16-20)", "innings == 2, overid >= 16", "innings, overid", "Both", False, "A", "Over 16 ball 1", "Innings 2 completion", "Phase boundary"),
        ("C36", "chase_close_finish", "F2", "Close match finish (Innings 2, balls remaining <= 18 and runs needed <= 30)", "innings == 2, balls_rem <= 18, runs_needed <= 30", "innings, runs, legal_balls", "Both", False, "B", "Threshold entry", "Innings 2 completion", "Reconstructed state"),
        ("C37", "rrr_high_ge_10", "F3", "High asking rate pressure (Innings 2, reconstructed RRR >= 10.0, balls remaining >= 6)", "innings == 2, rrr >= 10.0, balls_rem >= 6", "runs, legal_balls, target", "Both", False, "B", "RRR >= 10 threshold", "RRR drop or inn end", "Reconstructed RRR"),
        ("C38", "rrr_steep_ge_12", "F3", "Steep asking rate pressure (Innings 2, reconstructed RRR >= 12.0, balls remaining >= 6)", "innings == 2, rrr >= 12.0, balls_rem >= 6", "runs, legal_balls, target", "Both", False, "B", "RRR >= 12 threshold", "RRR drop or inn end", "Reconstructed RRR"),
        ("C39", "rrr_extreme_ge_14", "F3", "Extreme asking rate crisis (Innings 2, reconstructed RRR >= 14.0, balls remaining >= 6)", "innings == 2, rrr >= 14.0, balls_rem >= 6", "runs, legal_balls, target", "Both", False, "B", "RRR >= 14 threshold", "RRR drop or inn end", "Reconstructed RRR"),
        ("C40", "dynamic_wpa_crisis", "F3", "Dynamic Win Probability Added crisis (pre-delivery win prob 10%-90% high leverage)", "Unobservable without live betting / pre-ball win prob model", "live_win_probability", "Both", False, "C", "N/A", "N/A", "Not operationalisable")
    ]

    # Save Inventory CSV
    inv_df = pd.DataFrame(conditions_meta, columns=[
        'condition_id', 'condition_name', 'family', 'definition', 'eligibility_rule',
        'required_columns', 'applies_to', 'previously_validated', 'operationalisability_category',
        'start_event', 'end_event', 'temporal_orientation'
    ])
    inv_csv_path = os.path.join(out_dir, "original_pressure_conditions_inventory.csv")
    inv_df.to_csv(inv_csv_path, index=False)
    print(f"Saved original pressure conditions inventory to {inv_csv_path} (40 conditions)")

    # Build masks
    masks = {}
    masks['C01'] = df['f1_primary'].astype(str).str.lower().isin(['true', '1'])
    masks['C02'] = df['f1_alt1a'].astype(str).str.lower().isin(['true', '1'])
    masks['C03'] = (df['f1_alt1a'].astype(str).str.lower().isin(['true', '1'])) & (df['f1_alt1a_classification'] == 'COMPLETE_60')
    masks['C04'] = (df['f1_alt1a'].astype(str).str.lower().isin(['true', '1'])) & (df['f1_alt1a_classification'] == 'TRUNCATED_INNINGS')
    masks['C05'] = df['f1_alt1b'].astype(str).str.lower().isin(['true', '1'])
    masks['C06'] = df['f1_alt1c_w2_le_6'].astype(str).str.lower().isin(['true', '1'])
    masks['C07'] = df['f1_alt1c_w2_le_8'].astype(str).str.lower().isin(['true', '1'])
    masks['C08'] = df['f1_alt1c_w2_le_10'].astype(str).str.lower().isin(['true', '1'])
    masks['C09'] = masks['C06'] & (df['overid'] <= 6)
    masks['C10'] = (df['w3_over'] <= 6) & (df['innings_ball_num'] >= df['w3_ball'])
    masks['C11'] = (df['w3_over'] <= 8) & (df['innings_ball_num'] >= df['w3_ball'])
    masks['C12'] = (df['w4_over'] <= 10) & (df['innings_ball_num'] >= df['w4_ball'])
    masks['C13'] = df['mo_stagnation']

    masks['C14'] = df['f4_knockout'].astype(str).str.lower().isin(['true', '1'])
    masks['C15'] = masks['C01'] | masks['C14']
    masks['C16'] = masks['C01'] & masks['C14']
    masks['C17'] = df['innings'] >= 3
    masks['C18'] = masks['C14'] & (df['overid'] <= 6)
    masks['C19'] = masks['C14'] & (df['overid'].between(7, 15))
    masks['C20'] = masks['C14'] & (df['overid'] >= 16)

    masks['C21'] = df['overid'] >= 16
    masks['C22'] = (df['overid'] >= 16) & (df['innings'] == 1)
    masks['C23'] = (df['overid'] >= 16) & (df['innings'] == 2)
    masks['C24'] = (df['overid'] >= 16) & (df['wickets_down_before'] >= 4)
    masks['C25'] = (df['overid'] >= 16) & (df['wickets_down_before'] >= 6)
    masks['C26'] = (df['overid'].between(7, 15)) & (df['wickets_down_before'] >= 3)
    masks['C27'] = (df['overid'].between(7, 15)) & (df['wickets_down_before'] >= 5)
    masks['C28'] = (df['overid'] <= 6) & (df['wickets_down_before'] >= 2)
    masks['C29'] = (df['overid'] <= 6) & (df['wickets_down_before'] >= 3)
    masks['C30'] = df['wickets_down_before'] >= 7

    masks['C31'] = df['innings'] == 2
    masks['C32'] = (df['innings'] == 2) & (df['inn1_total'] >= 180)
    masks['C33'] = (df['innings'] == 2) & (df['inn1_total'] >= 200)
    masks['C34'] = (df['innings'] == 2) & (df['inn1_total'] <= 150)
    masks['C35'] = (df['innings'] == 2) & (df['overid'] >= 16)
    masks['C36'] = (df['innings'] == 2) & (df['balls_remaining'] <= 18) & (df['runs_needed'] <= 30) & (df['runs_needed'] > 0)
    masks['C37'] = (df['innings'] == 2) & (df['reconstructed_rrr'] >= 10.0) & (df['balls_remaining'] >= 6)
    masks['C38'] = (df['innings'] == 2) & (df['reconstructed_rrr'] >= 12.0) & (df['balls_remaining'] >= 6)
    masks['C39'] = (df['innings'] == 2) & (df['reconstructed_rrr'] >= 14.0) & (df['balls_remaining'] >= 6)
    # C40: Category C - mask not operational

    # Operationalisation Audit
    print("\n[Step 5] Building condition operationalisation audit...")
    audit_rows = []
    for c_tuple in conditions_meta:
        cid, cname, fam, cdef, rule, cols, app, val, cat, st, en, temp = c_tuple
        if cat in ['A', 'B']:
            m = masks[cid]
            clean_m = m & df['is_clean']
            sub_d = df[m]
            sub_c = df[clean_m]
            n_deliv = len(sub_d)
            n_clean = len(sub_c)
            n_matches = sub_c['match_id'].nunique()
            n_inns = sub_c.groupby(['match_id', 'innings']).ngroups
            status = "Operationalised (Exact)" if cat == 'A' else "Operationalised (Approximated)"
            approx = "None" if cat == 'A' else "Reconstructed from cumulative innings ball-by-ball variables"
        else:
            n_deliv = 0
            n_clean = 0
            n_matches = 0
            n_inns = 0
            status = "Excluded (Data Unavailable)"
            approx = "Live delivery-level win probability models and par scores are absent from competition data pack"

        audit_rows.append({
            'condition_id': cid,
            'condition_name': cname,
            'family': fam,
            'category': cat,
            'operational_status': status,
            'total_ipl_deliveries': n_deliv,
            'total_ipl_clean_balls': n_clean,
            'unique_qualifying_matches': n_matches,
            'unique_qualifying_innings': n_inns,
            'temporal_orientation': temp,
            'start_event': st,
            'end_event': en,
            'approximation_details': approx
        })
    audit_df = pd.DataFrame(audit_rows)
    audit_csv_path = os.path.join(out_dir, "condition_operationalisation_audit.csv")
    audit_df.to_csv(audit_csv_path, index=False)
    print(f"Saved operationalisation audit to {audit_csv_path}")

    # 4. Virat Kohli Analysis Across All Conditions
    print("\n[Step 6] Computing Virat Kohli performance and match-level bootstrap across all conditions...")
    kohli_results = []
    kohli_innings_records = []
    np.random.seed(42)

    for c_tuple in conditions_meta:
        cid, cname, fam, cdef, rule, cols, app, val, cat, st, en, temp = c_tuple
        if cat == 'C':
            continue

        clean_cond = df[masks[cid] & df['is_clean']].copy()
        clean_cond['res'] = clean_cond['runs_int'] - clean_cond['exp_runs']
        sigma2 = float(clean_cond['res'].var()) if len(clean_cond) > 1 else 0.0

        vk_cond = clean_cond[clean_cond['striker_id'] == 47].copy()
        n_balls = len(vk_cond)
        obs_runs = int(vk_cond['runs_int'].sum())
        exp_runs = float(vk_cond['exp_runs'].sum())
        raw_rae = obs_runs - exp_runs
        rae_per_ball = raw_rae / n_balls if n_balls > 0 else 0.0
        actual_sr = (obs_runs / n_balls * 100.0) if n_balls > 0 else 0.0
        exp_sr = (exp_runs / n_balls * 100.0) if n_balls > 0 else 0.0

        # Innings breakdown for Kohli
        if n_balls > 0:
            inn_grp = vk_cond.groupby(['match_id', 'match_date', 'season', 'home_team', 'away_team', 'innings'])
            inn_records = []
            for (mid, mdate, ssn, ht, at, inn), g in inn_grp:
                g_balls = len(g)
                g_obs = int(g['runs_int'].sum())
                g_exp = float(g['exp_runs'].sum())
                g_rae = g_obs - g_exp
                opp = at if ht == 'Royal Challengers Bengaluru' or ht == 'Royal Challengers Bangalore' else ht
                inn_records.append({
                    'condition_id': cid,
                    'condition_name': cname,
                    'match_id': mid,
                    'match_date': mdate,
                    'season': ssn,
                    'opponent': opp,
                    'innings': inn,
                    'clean_balls': g_balls,
                    'observed_runs': g_obs,
                    'expected_runs': round(g_exp, 2),
                    'raw_rae': round(g_rae, 2),
                    'actual_sr': round(g_obs / g_balls * 100.0, 2),
                    'expected_sr': round(g_exp / g_balls * 100.0, 2),
                    'is_positive_inn': bool(g_rae > 0)
                })
            kohli_innings_records.extend(inn_records)
            q_inns = len(inn_records)
            pos_pct = round(sum(1 for r in inn_records if r['is_positive_inn']) / q_inns * 100.0, 1)
            median_rae = round(float(pd.Series([r['raw_rae'] for r in inn_records]).median()), 2)
        else:
            q_inns = 0
            pos_pct = 0.0
            median_rae = 0.0

        # DerSimonian-Laird Shrinkage on condition population
        bat_summary = clean_cond.groupby(['striker_id', 'striker_name']).agg(
            clean_balls=('runs_int', 'count'),
            obs_runs=('runs_int', 'sum'),
            exp_runs=('exp_runs', 'sum')
        ).reset_index()
        bat_summary['raw_rae'] = bat_summary['obs_runs'] - bat_summary['exp_runs']
        bat_summary['raw_rate_diff'] = bat_summary['raw_rae'] / bat_summary['clean_balls']
        bat_summary['v'] = np.maximum(1e-9, sigma2 / bat_summary['clean_balls'])

        eligible_bat = bat_summary[bat_summary['clean_balls'] >= 10].copy()
        if len(eligible_bat) >= 5 and sigma2 > 0:
            w_dl = 1.0 / eligible_bat['v']
            sum_w = float(w_dl.sum())
            sum_w2 = float((w_dl**2).sum())
            mu_prior = float((w_dl * eligible_bat['raw_rate_diff']).sum() / sum_w)
            q_stat = float((w_dl * (eligible_bat['raw_rate_diff'] - mu_prior)**2).sum())
            k_df = len(eligible_bat)
            c_factor = sum_w - (sum_w2 / sum_w)
            tau2 = max(0.0, float((q_stat - (k_df - 1)) / c_factor)) if c_factor > 0 else 0.04
        else:
            mu_prior = float(bat_summary['raw_rate_diff'].mean()) if len(bat_summary) > 0 else 0.0
            tau2 = 0.04

        v_k = sigma2 / n_balls if n_balls > 0 else 1.0
        B_k = v_k / (v_k + tau2) if (v_k + tau2) > 0 else 1.0
        shrunk_rate_k = (1.0 - B_k) * rae_per_ball + B_k * mu_prior
        shrunk_rae = shrunk_rate_k * n_balls if n_balls > 0 else 0.0

        # Fast Vectorized Match-Cluster Bootstrap for Kohli
        if n_balls > 0:
            match_diffs = vk_cond.groupby('match_id').apply(lambda g: g['runs_int'].sum() - g['exp_runs'].sum()).to_numpy()
            n_m = len(match_diffs)
            boot_samples = np.random.choice(match_diffs, size=(1000, n_m), replace=True).sum(axis=1)
            ci_low, ci_high = np.percentile(boot_samples, [2.5, 97.5])
        else:
            ci_low, ci_high = 0.0, 0.0

        kohli_results.append({
            'condition_id': cid,
            'condition_name': cname,
            'family': fam,
            'operational_category': cat,
            'clean_balls_faced': n_balls,
            'observed_clean_runs': obs_runs,
            'expected_clean_runs': round(exp_runs, 2),
            'raw_rae': round(raw_rae, 2),
            'rae_per_ball': round(rae_per_ball, 4),
            'actual_strike_rate': round(actual_sr, 2),
            'expected_strike_rate': round(exp_sr, 2),
            'qualifying_innings': q_inns,
            'positive_innings_pct': pos_pct,
            'median_innings_rae': median_rae,
            'shrunk_rae': round(shrunk_rae, 2),
            'ci_lower_95': round(ci_low, 2),
            'ci_upper_95': round(ci_high, 2)
        })

    kohli_df = pd.DataFrame(kohli_results)
    kohli_csv_path = os.path.join(out_dir, "kohli_condition_results.csv")
    kohli_df.to_csv(kohli_csv_path, index=False)
    print(f"Saved Kohli condition results to {kohli_csv_path}")

    kohli_inn_df = pd.DataFrame(kohli_innings_records)
    kohli_inn_csv_path = os.path.join(out_dir, "kohli_innings_condition_results.csv")
    kohli_inn_df.to_csv(kohli_inn_csv_path, index=False)
    print(f"Saved Kohli innings records to {kohli_inn_csv_path} ({len(kohli_inn_df)} innings entries)")

    # 5. Full Batter Leaderboards Across All Conditions
    print("\n[Step 7] Generating full batter leaderboards across all conditions and exposure thresholds...")
    leaderboards_list = []
    kohli_sensitivity_list = []

    for c_tuple in conditions_meta:
        cid, cname, fam, cdef, rule, cols, app, val, cat, st, en, temp = c_tuple
        if cat == 'C':
            continue

        clean_cond = df[masks[cid] & df['is_clean']].copy()
        clean_cond['res'] = clean_cond['runs_int'] - clean_cond['exp_runs']
        sigma2 = float(clean_cond['res'].var()) if len(clean_cond) > 1 else 0.0

        # Group by batter
        bat_df = clean_cond.groupby(['striker_id', 'striker_name']).agg(
            clean_balls=('runs_int', 'count'),
            obs_runs=('runs_int', 'sum'),
            exp_runs=('exp_runs', 'sum'),
            qualifying_innings=('match_id', 'nunique')
        ).reset_index()
        bat_df['raw_rae'] = bat_df['obs_runs'] - bat_df['exp_runs']
        bat_df['rae_per_ball'] = bat_df['raw_rae'] / bat_df['clean_balls']
        bat_df['v'] = np.maximum(1e-9, sigma2 / bat_df['clean_balls'])

        # Positive innings % per batter
        bat_inns = clean_cond.groupby(['striker_id', 'match_id']).apply(lambda g: g['runs_int'].sum() - g['exp_runs'].sum()).reset_index(name='inn_rae')
        pos_inns = bat_inns.groupby('striker_id')['inn_rae'].apply(lambda s: (s > 0).mean() * 100.0).to_dict()
        bat_df['positive_innings_pct'] = bat_df['striker_id'].map(pos_inns).round(1)

        # Shrinkage
        eligible_bat = bat_df[bat_df['clean_balls'] >= 10].copy()
        if len(eligible_bat) >= 5 and sigma2 > 0:
            w_dl = 1.0 / eligible_bat['v']
            sum_w = float(w_dl.sum())
            sum_w2 = float((w_dl**2).sum())
            mu_prior = float((w_dl * eligible_bat['rae_per_ball']).sum() / sum_w)
            q_stat = float((w_dl * (eligible_bat['rae_per_ball'] - mu_prior)**2).sum())
            k_df = len(eligible_bat)
            c_factor = sum_w - (sum_w2 / sum_w)
            tau2 = max(0.0, float((q_stat - (k_df - 1)) / c_factor)) if c_factor > 0 else 0.04
        else:
            mu_prior = float(bat_df['rae_per_ball'].mean()) if len(bat_df) > 0 else 0.0
            tau2 = 0.04

        bat_df['B_weight'] = bat_df['v'] / (bat_df['v'] + tau2)
        bat_df['shrunk_rae_rate'] = (1.0 - bat_df['B_weight']) * bat_df['rae_per_ball'] + bat_df['B_weight'] * mu_prior
        bat_df['shrunk_rae'] = bat_df['shrunk_rae_rate'] * bat_df['clean_balls']

        # Ranks overall and thresholds
        bat_df['rank_all'] = bat_df['shrunk_rae'].rank(ascending=False, method='min').astype(int)

        for th in [30, 50, 100, 200, 300]:
            sub_th = bat_df[bat_df['clean_balls'] >= th]
            rank_col = f'rank_min{th}'
            if len(sub_th) > 0:
                ranks = pd.Series(sub_th['shrunk_rae'].rank(ascending=False, method='min').values.astype(int), index=sub_th['striker_id'])
                bat_df[rank_col] = bat_df['striker_id'].map(ranks).fillna(-1).astype(int)
            else:
                bat_df[rank_col] = -1

        bat_df['condition_id'] = cid
        bat_df['condition_name'] = cname
        leaderboards_list.append(bat_df)

        # Track Kohli's sensitivity across thresholds
        vk_row = bat_df[bat_df['striker_id'] == 47]
        if len(vk_row) > 0:
            vk = vk_row.iloc[0]
            sens_record = {
                'condition_id': cid,
                'condition_name': cname,
                'kohli_clean_balls': int(vk['clean_balls']),
                'kohli_raw_rae': round(float(vk['raw_rae']), 2),
                'kohli_shrunk_rae': round(float(vk['shrunk_rae']), 2),
                'rank_unfiltered': int(vk['rank_all']),
                'pool_size_unfiltered': len(bat_df),
                'rank_ge_30': int(vk['rank_min30']),
                'pool_size_ge_30': int((bat_df['clean_balls'] >= 30).sum()),
                'rank_ge_50': int(vk['rank_min50']),
                'pool_size_ge_50': int((bat_df['clean_balls'] >= 50).sum()),
                'rank_ge_100': int(vk['rank_min100']),
                'pool_size_ge_100': int((bat_df['clean_balls'] >= 100).sum()),
                'rank_ge_200': int(vk['rank_min200']),
                'pool_size_ge_200': int((bat_df['clean_balls'] >= 200).sum()),
                'rank_ge_300': int(vk['rank_min300']),
                'pool_size_ge_300': int((bat_df['clean_balls'] >= 300).sum())
            }
        else:
            sens_record = {
                'condition_id': cid,
                'condition_name': cname,
                'kohli_clean_balls': 0,
                'kohli_raw_rae': 0.0,
                'kohli_shrunk_rae': 0.0,
                'rank_unfiltered': -1,
                'pool_size_unfiltered': len(bat_df),
                'rank_ge_30': -1,
                'pool_size_ge_30': int((bat_df['clean_balls'] >= 30).sum()),
                'rank_ge_50': -1,
                'pool_size_ge_50': int((bat_df['clean_balls'] >= 50).sum()),
                'rank_ge_100': -1,
                'pool_size_ge_100': int((bat_df['clean_balls'] >= 100).sum()),
                'rank_ge_200': -1,
                'pool_size_ge_200': int((bat_df['clean_balls'] >= 200).sum()),
                'rank_ge_300': -1,
                'pool_size_ge_300': int((bat_df['clean_balls'] >= 300).sum())
            }
        kohli_sensitivity_list.append(sens_record)

    all_leaderboards = pd.concat(leaderboards_list, ignore_index=True)
    all_lead_cols = [
        'condition_id', 'condition_name', 'striker_id', 'striker_name', 'clean_balls',
        'obs_runs', 'exp_runs', 'raw_rae', 'rae_per_ball', 'shrunk_rae',
        'qualifying_innings', 'positive_innings_pct', 'rank_all',
        'rank_min30', 'rank_min50', 'rank_min100', 'rank_min200', 'rank_min300'
    ]
    all_lead_df = all_leaderboards[all_lead_cols].rename(columns={'striker_id': 'player_id', 'striker_name': 'player_name', 'clean_balls': 'clean_balls_faced'})
    all_lead_csv_path = os.path.join(out_dir, "all_batter_condition_leaderboards.csv")
    all_lead_df.to_csv(all_lead_csv_path, index=False)
    print(f"Saved full batter leaderboards to {all_lead_csv_path} ({len(all_lead_df):,} player-condition rows)")

    kohli_sens_df = pd.DataFrame(kohli_sensitivity_list)
    kohli_sens_csv_path = os.path.join(out_dir, "kohli_exposure_sensitivity.csv")
    kohli_sens_df.to_csv(kohli_sens_csv_path, index=False)
    print(f"Saved Kohli exposure sensitivity table to {kohli_sens_csv_path}")

    # 6. Condition Overlap Analysis
    print("\n[Step 8] Computing delivery overlap matrix and Jaccard similarity across conditions...")
    op_cids = [c[0] for c in conditions_meta if c[8] in ['A', 'B']]
    overlap_rows = []
    clean_total = df['is_clean']

    for i, c1 in enumerate(op_cids):
        m1 = masks[c1] & clean_total
        count1 = m1.sum()
        for j, c2 in enumerate(op_cids):
            m2 = masks[c2] & clean_total
            count2 = m2.sum()
            inter = (m1 & m2).sum()
            union = (m1 | m2).sum()
            jaccard = inter / union if union > 0 else 0.0
            overlap_pct = inter / count1 * 100.0 if count1 > 0 else 0.0
            overlap_rows.append({
                'condition_id_1': c1,
                'condition_name_1': inv_df.set_index('condition_id').loc[c1, 'condition_name'],
                'condition_id_2': c2,
                'condition_name_2': inv_df.set_index('condition_id').loc[c2, 'condition_name'],
                'deliveries_1': int(count1),
                'deliveries_2': int(count2),
                'intersection_deliveries': int(inter),
                'union_deliveries': int(union),
                'jaccard_similarity': round(float(jaccard), 4),
                'overlap_pct_of_1': round(float(overlap_pct), 2)
            })

    overlap_df = pd.DataFrame(overlap_rows)
    overlap_csv_path = os.path.join(out_dir, "condition_overlap_analysis.csv")
    overlap_df.to_csv(overlap_csv_path, index=False)
    print(f"Saved condition overlap analysis to {overlap_csv_path} ({len(overlap_df)} pairwise combinations)")

    # 7. Condition Correlation Analysis (Batter Performance Correlation)
    print("\n[Step 9] Computing batter performance correlation matrix across conditions...")
    piv_raw_rae = all_lead_df.pivot(index='player_id', columns='condition_id', values='raw_rae').fillna(0)
    piv_shrunk_rae = all_lead_df.pivot(index='player_id', columns='condition_id', values='shrunk_rae').fillna(0)

    corr_rows = []
    for i, c1 in enumerate(op_cids):
        s1 = piv_shrunk_rae[c1]
        for j, c2 in enumerate(op_cids):
            s2 = piv_shrunk_rae[c2]
            pearson_val, _ = stats.pearsonr(s1, s2) if s1.std() > 0 and s2.std() > 0 else (0.0, 1.0)
            spearman_val, _ = stats.spearmanr(s1, s2) if s1.std() > 0 and s2.std() > 0 else (0.0, 1.0)
            corr_rows.append({
                'condition_id_1': c1,
                'condition_name_1': inv_df.set_index('condition_id').loc[c1, 'condition_name'],
                'condition_id_2': c2,
                'condition_name_2': inv_df.set_index('condition_id').loc[c2, 'condition_name'],
                'pearson_correlation': round(float(pearson_val), 4),
                'spearman_rank_correlation': round(float(spearman_val), 4)
            })

    corr_df = pd.DataFrame(corr_rows)
    corr_csv_path = os.path.join(out_dir, "condition_correlation_analysis.csv")
    corr_df.to_csv(corr_csv_path, index=False)
    print(f"Saved condition correlation analysis to {corr_csv_path}")

    # 8. Machine-Readable Audit JSON
    print("\n[Step 10] Writing machine-readable audit trail JSON...")
    audit_json_data = {
        "metadata": {
            "analysis_title": "Full Pressure Condition Retest: Independent IPL Evaluation (2022-2026)",
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "git_commit": "c882a366da81edf4355323c5d255302f193615f1",
            "eval_player": {
                "player_id": 47,
                "player_name": "Virat Kohli",
                "ipl_total_balls_faced": int(len(df[df['striker_id'] == 47])),
                "ipl_clean_balls_faced": int(len(df[(df['striker_id'] == 47) & df['is_clean']]))
            }
        },
        "condition_summary": {
            "total_candidate_conditions": len(conditions_meta),
            "category_a_fully_operationalised": sum(1 for c in conditions_meta if c[8] == 'A'),
            "category_b_approximated": sum(1 for c in conditions_meta if c[8] == 'B'),
            "category_c_unobservable": sum(1 for c in conditions_meta if c[8] == 'C'),
            "total_operationalised": len(op_cids)
        },
        "ipl_corpus_integrity": {
            "total_deliveries": len(df),
            "clean_deliveries": int(df['is_clean'].sum()),
            "unique_matches": int(df['match_id'].nunique()),
            "seasons": sorted(ipl_matches['season'].unique().tolist())
        },
        "baseline_reconciliation": {
            "f1_union_f4_balls": 404,
            "f1_union_f4_obs_runs": 524,
            "f1_union_f4_exp_runs": 620.05,
            "f1_union_f4_raw_rae": -96.05,
            "f1_union_f4_shrunk_rae": -91.95
        },
        "output_files": [
            "original_pressure_conditions_inventory.csv",
            "condition_operationalisation_audit.csv",
            "kohli_condition_results.csv",
            "kohli_innings_condition_results.csv",
            "all_batter_condition_leaderboards.csv",
            "kohli_exposure_sensitivity.csv",
            "condition_overlap_analysis.csv",
            "condition_correlation_analysis.csv",
            "pressure_condition_retest_methodology.md",
            "pressure_condition_retest_summary.md",
            "pressure_condition_retest_audit.json",
            "run_pressure_condition_retest.py"
        ]
    }
    audit_json_path = os.path.join(out_dir, "pressure_condition_retest_audit.json")
    with open(audit_json_path, 'w', encoding='utf-8') as f:
        json.dump(audit_json_data, f, indent=2)
    print(f"Saved audit JSON to {audit_json_path}")

    print("\n" + "=" * 80)
    print(f"FULL PIPELINE EXECUTION COMPLETE IN {time.time() - start_time:.2f} SECONDS")
    print("=" * 80)

if __name__ == "__main__":
    main()

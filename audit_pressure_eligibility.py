from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "data_pack"
OUTPUT_DIR = ROOT / "audit_outputs"

MATCHES_FILE = DATA_DIR / "matches.csv"
BALLS_FILE = DATA_DIR / "ball_by_ball.csv"
COMPETITIONS_FILE = DATA_DIR / "competitions.csv"

OUTPUT_FILES = {
    "innings": OUTPUT_DIR / "innings_coverage_audit.csv",
    "middle": OUTPUT_DIR / "middle_over_eligibility_audit.csv",
    "revised": OUTPUT_DIR / "revised_metadata_audit.csv",
}

REVISED_COLUMNS = [
    "first_inn_revised_overs",
    "second_inn_revised_overs",
    "revised_target",
]

LEGAL_METHODS = {
    "primary_other_illegal": {"wide", "overstep", "other"},
    "alternative_other_legal": {"wide", "overstep"},
}

RUN_SUM_BASIS = (
    "Sum of the logged runs column only. The script does not add extras1_runs "
    "or extras_2_runs because their meaning is not established by this audit."
)


def require_columns(frame: pd.DataFrame, required: list[str], filename: Path) -> None:
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"{filename.name} is missing required columns: {missing}")


def numeric_id(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype("Int64")


def int_or_none(value: Any) -> int | None:
    if pd.isna(value):
        return None
    numeric = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric):
        return None
    rounded = round(float(numeric))
    if abs(float(numeric) - rounded) > 1e-9:
        return None
    return int(rounded)


def json_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=json_value)


def normalize_extra(value: Any) -> str:
    if pd.isna(value):
        return ""
    normalized = str(value).strip().casefold()
    if normalized in {"", "none", "nan", "null"}:
        return ""
    return normalized


def parse_bool(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.casefold().isin(
        {"true", "1", "yes", "y"}
    )


def completion_status(
    *,
    wickets: int,
    legal_balls: int,
    recorded_limit: int | None,
    result_text: str,
) -> str:
    if wickets >= 10:
        return "completed_all_out"
    if recorded_limit is not None and legal_balls >= recorded_limit:
        return "completed_recorded_limit"
    if recorded_limit is None and legal_balls >= 120:
        return "reached_assumed_120_not_confirmed"
    if re.search(r"no result|abandon|rain", result_text, flags=re.IGNORECASE):
        return "appears_interrupted_or_censored"
    return "endpoint_uncertain"


def main() -> None:
    for source in (MATCHES_FILE, BALLS_FILE, COMPETITIONS_FILE):
        if not source.is_file():
            raise FileNotFoundError(f"Required source file not found: {source}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    existing_outputs = [path for path in OUTPUT_FILES.values() if path.exists()]
    if existing_outputs:
        raise FileExistsError(
            "Refusing to overwrite existing audit output(s): "
            + ", ".join(str(path) for path in existing_outputs)
        )

    matches = pd.read_csv(MATCHES_FILE, low_memory=False)
    balls = pd.read_csv(BALLS_FILE, low_memory=False)
    competitions = pd.read_csv(COMPETITIONS_FILE, low_memory=False)

    require_columns(
        matches,
        [
            "match_id",
            "comp_id",
            "match_date",
            "result",
            *REVISED_COLUMNS,
        ],
        MATCHES_FILE,
    )
    require_columns(
        balls,
        [
            "match_id",
            "innings",
            "overid",
            "over_ball_num",
            "innings_ball_num",
            "runs",
            "is_wicket",
            "extras_type",
        ],
        BALLS_FILE,
    )
    require_columns(competitions, ["comp_id"], COMPETITIONS_FILE)

    matches["match_id"] = numeric_id(matches["match_id"])
    matches["comp_id"] = numeric_id(matches["comp_id"])
    balls["match_id"] = numeric_id(balls["match_id"])
    balls["innings"] = pd.to_numeric(balls["innings"], errors="coerce")
    balls["overid"] = pd.to_numeric(balls["overid"], errors="coerce")
    balls["over_ball_num"] = pd.to_numeric(balls["over_ball_num"], errors="coerce")
    balls["innings_ball_num"] = pd.to_numeric(
        balls["innings_ball_num"], errors="coerce"
    )
    competitions["comp_id"] = numeric_id(competitions["comp_id"])

    for column in REVISED_COLUMNS:
        matches[column] = pd.to_numeric(matches[column], errors="coerce")

    balls["_extra_normalized"] = balls["extras_type"].map(normalize_extra)
    balls["_is_wicket"] = parse_bool(balls["is_wicket"])
    balls["_runs_numeric"] = pd.to_numeric(balls["runs"], errors="coerce")

    for method, illegal_extras in LEGAL_METHODS.items():
        balls[f"_legal_{method}"] = ~balls["_extra_normalized"].isin(illegal_extras)

    # A match is first-innings-only here if its ball-by-ball data contains
    # innings 1 and does not contain innings 2.
    innings_by_match = balls.groupby("match_id")["innings"].agg(
        lambda values: set(values.dropna().astype(int))
    )
    first_only_ids = sorted(
        int(match_id)
        for match_id, innings_set in innings_by_match.items()
        if 1 in innings_set and 2 not in innings_set
    )

    # Revised metadata is counted once per unique match ID, if any of the
    # three revised fields is non-null.
    revised_rows = matches.loc[
        matches[REVISED_COLUMNS].notna().any(axis=1)
    ].copy()
    revised_ids = sorted(
        int(match_id)
        for match_id in revised_rows["match_id"].dropna().unique()
    )
    overlap_ids = sorted(set(first_only_ids).intersection(revised_ids))

    competition_name_col = next(
        (
            column
            for column in ("competition_name", "comp_name", "name")
            if column in competitions.columns
        ),
        None,
    )
    competition_format_col = next(
        (
            column
            for column in ("format", "competition_format")
            if column in competitions.columns
        ),
        None,
    )

    competition_columns = ["comp_id"]
    if competition_name_col:
        competition_columns.append(competition_name_col)
    if competition_format_col:
        competition_columns.append(competition_format_col)

    competition_view = competitions[competition_columns].drop_duplicates("comp_id")
    match_view = matches.merge(
        competition_view,
        on="comp_id",
        how="left",
        suffixes=("", "_competition"),
    )

    match_details = match_view.drop_duplicates("match_id").set_index("match_id")
    result_by_match = (
        match_details["result"].to_dict() if "result" in match_details.columns else {}
    )

    # Columns that could represent delivery-level DLS/par-score information.
    # A match-level revised_target is deliberately not treated as live DLS data.
    live_dls_tokens = (
        "par_score",
        "par_runs",
        "live_target",
        "target_at_delivery",
        "target_score_by_ball",
        "runs_required",
        "required_run_rate",
        "dls",
    )
    live_dls_columns = [
        column
        for column in balls.columns
        if any(token in column.casefold() for token in live_dls_tokens)
    ]
    live_dls_columns = [
        column
        for column in live_dls_columns
        if not column.startswith("_")
    ]

    revised_output_rows: list[dict[str, Any]] = []
    for _, row in revised_rows.drop_duplicates("match_id").sort_values(
        "match_id"
    ).iterrows():
        match_id = int(row["match_id"])
        result_text = "" if pd.isna(row["result"]) else str(row["result"])
        detail = match_details.loc[match_id] if match_id in match_details.index else None

        record: dict[str, Any] = {
            "match_id": match_id,
            "comp_id": int_or_none(row["comp_id"]),
            "match_date": row.get("match_date"),
            "result": row.get("result"),
            "first_inn_revised_overs": row["first_inn_revised_overs"],
            "second_inn_revised_overs": row["second_inn_revised_overs"],
            "revised_target": row["revised_target"],
            "has_revised_overs": bool(
                pd.notna(row["first_inn_revised_overs"])
                or pd.notna(row["second_inn_revised_overs"])
            ),
            "has_revised_target": bool(pd.notna(row["revised_target"])),
            "dls_or_rain_result_text": bool(
                re.search(r"dls|duckworth|lewis|rain", result_text, re.IGNORECASE)
            ),
            "first_innings_only": match_id in set(first_only_ids),
            "live_dls_candidate_columns_in_ball_by_ball": json_text(live_dls_columns),
            "live_dls_par_score_reconstructable_from_match_metadata": False,
            "live_dls_note": (
                "A match-level revised_target is not a delivery-by-delivery "
                "DLS par score."
            ),
        }
        if detail is not None:
            if competition_name_col:
                record["competition_name"] = detail.get(competition_name_col)
            if competition_format_col:
                record["competition_format"] = detail.get(competition_format_col)
            if "stage" in detail.index:
                record["stage"] = detail.get("stage")
            if "knock_out" in detail.index:
                record["knock_out"] = detail.get("knock_out")
        revised_output_rows.append(record)

    revised_audit = pd.DataFrame(revised_output_rows)
    if not revised_audit.empty:
        revised_audit["first_only_overlap"] = revised_audit["match_id"].isin(
            overlap_ids
        )
    else:
        revised_audit["first_only_overlap"] = pd.Series(dtype=bool)

    # Summaries and per-over lookup tables for first-innings-only matches.
    innings_output_rows: list[dict[str, Any]] = []
    middle_output_rows: list[dict[str, Any]] = []

    for match_id in first_only_ids:
        innings_data = balls.loc[
            (balls["match_id"] == match_id) & (balls["innings"] == 1)
        ].copy()

        if innings_data.empty:
            continue

        innings_data["_source_order"] = range(len(innings_data))
        innings_data = innings_data.sort_values(
            ["overid", "innings_ball_num", "over_ball_num", "_source_order"],
            na_position="last",
            kind="stable",
        )

        match_row = (
            match_details.loc[match_id] if match_id in match_details.index else None
        )
        result_text = result_by_match.get(match_id, "")
        result_text = "" if pd.isna(result_text) else str(result_text)

        recorded_limit = None
        if match_row is not None and "first_inn_revised_overs" in match_row.index:
            recorded_limit = int_or_none(match_row["first_inn_revised_overs"])

        assumed_120 = recorded_limit is None
        valid_over_ids = sorted(
            int_or_none(value)
            for value in innings_data["overid"].dropna().unique()
            if int_or_none(value) is not None
        )
        highest_over = max(valid_over_ids) if valid_over_ids else None
        missing_over_ids = (
            sorted(set(range(1, highest_over + 1)) - set(valid_over_ids))
            if highest_over is not None
            else []
        )

        per_method: dict[str, dict[int, int]] = {}
        for method in LEGAL_METHODS:
            legal_col = f"_legal_{method}"
            legal_total = int(innings_data[legal_col].sum())
            wickets = int(innings_data["_is_wicket"].sum())

            per_over_series = (
                innings_data.dropna(subset=["overid"])
                .groupby("overid")[legal_col]
                .sum()
            )
            per_over = {
                int_or_none(over_id): int(count)
                for over_id, count in per_over_series.items()
                if int_or_none(over_id) is not None
            }
            per_method[method] = per_over

            incomplete_overs = sorted(
                over_id for over_id, count in per_over.items() if count < 6
            )
            over_count_anomalies = sorted(
                over_id for over_id, count in per_over.items() if count > 6
            )

            innings_output_rows.append(
                {
                    "match_id": match_id,
                    "innings": 1,
                    "result": result_text,
                    "legal_ball_method": method,
                    "recorded_first_inn_revised_limit_balls": recorded_limit,
                    "limit_basis": (
                        "recorded_revised_limit"
                        if recorded_limit is not None
                        else "120_balls_assumed_not_verified"
                    ),
                    "120_ball_limit_is_assumption": assumed_120,
                    "legal_balls": legal_total,
                    "wickets_recorded": wickets,
                    "highest_over_reached": highest_over,
                    "observed_overids_json": json_text(valid_over_ids),
                    "missing_overids_from_1_to_highest_json": json_text(
                        missing_over_ids
                    ),
                    "legal_deliveries_per_over_json": json_text(per_over),
                    "incomplete_overs_fewer_than_6_legal_json": json_text(
                        incomplete_overs
                    ),
                    "overs_more_than_6_legal_anomaly_json": json_text(
                        over_count_anomalies
                    ),
                    "last_observed_over_legal_deliveries": (
                        per_over.get(highest_over)
                        if highest_over is not None
                        else None
                    ),
                    "last_observed_over_has_fewer_than_6_legal": (
                        per_over.get(highest_over, 0) < 6
                        if highest_over is not None
                        else None
                    ),
                    "completion_assessment": completion_status(
                        wickets=wickets,
                        legal_balls=legal_total,
                        recorded_limit=recorded_limit,
                        result_text=result_text,
                    ),
                    "result_indicates_interruption": bool(
                        re.search(
                            r"no result|abandon|rain",
                            result_text,
                            flags=re.IGNORECASE,
                        )
                    ),
                    "chase_pressure_eligibility": "unusable_no_second_innings",
                }
            )

        wicket_rows = innings_data.loc[innings_data["_is_wicket"]].copy()
        second_wicket = (
            wicket_rows.iloc[1] if len(wicket_rows) >= 2 else None
        )
        last_delivery = innings_data.iloc[-1] if not innings_data.empty else None

        second_wicket_over = (
            int_or_none(second_wicket["overid"])
            if second_wicket is not None
            else None
        )
        second_wicket_within_first_8 = (
            second_wicket_over is not None and second_wicket_over <= 8
        )

        # A previous over is complete only if it has exactly six legal deliveries.
        # Incomplete and missing overs are excluded from the completed-over lookback.
        for method in LEGAL_METHODS:
            per_over = per_method[method]
            complete_over_ids = sorted(
                over_id for over_id, count in per_over.items() if count == 6
            )

            for _, candidate in innings_data.loc[
                innings_data["overid"].between(7, 15, inclusive="both")
            ].iterrows():
                candidate_over = int_or_none(candidate["overid"])
                if candidate_over is None:
                    continue

                prior_complete = [
                    over_id
                    for over_id in complete_over_ids
                    if over_id < candidate_over
                ][-4:]

                prior_over_rows = innings_data.loc[
                    innings_data["overid"].isin(prior_complete)
                ]
                runs_missing = bool(prior_over_rows["_runs_numeric"].isna().any())
                previous_four_runs = (
                    None
                    if len(prior_complete) != 4 or runs_missing
                    else int(prior_over_rows["_runs_numeric"].sum())
                )

                if len(prior_complete) != 4 or runs_missing:
                    eligibility = "uncertain"
                    reason = (
                        "Fewer than four prior complete overs are available, "
                        "or the runs value is missing."
                    )
                elif previous_four_runs <= 20:
                    eligibility = "usable"
                    reason = (
                        "Four prior complete overs are available and the sum of "
                        "the logged runs column is <= 20."
                    )
                else:
                    eligibility = "unusable"
                    reason = (
                        "Four prior complete overs are available but the sum of "
                        "the logged runs column is > 20."
                    )

                skipped_prior_overs = (
                    sorted(
                        over_id
                        for over_id in range(1, candidate_over)
                        if over_id not in prior_complete
                    )
                    if prior_complete
                    else list(range(1, candidate_over))
                )

                middle_output_rows.append(
                    {
                        "match_id": match_id,
                        "innings": 1,
                        "legal_ball_method": method,
                        "candidate_overid": candidate_over,
                        "candidate_over_ball_num": int_or_none(
                            candidate["over_ball_num"]
                        ),
                        "candidate_innings_ball_num": int_or_none(
                            candidate["innings_ball_num"]
                        ),
                        "candidate_delivery_time": candidate.get(
                            "delivery_ist_time"
                        ),
                        "previous_four_complete_overids_json": json_text(
                            prior_complete
                        ),
                        "other_prior_overids_skipped_json": json_text(
                            skipped_prior_overs
                        ),
                        "previous_four_runs_sum_from_runs_column": previous_four_runs,
                        "runs_sum_basis": RUN_SUM_BASIS,
                        "previous_four_runs_le_20": (
                            previous_four_runs <= 20
                            if previous_four_runs is not None
                            else None
                        ),
                        "eligibility": eligibility,
                        "reason": reason,
                    }
                )

        # Repeat wicket timing and last-observed-delivery information on each
        # legal-ball-method row so both treatments can be compared directly.
        for row in innings_output_rows[-2:]:
            row["second_wicket_overid"] = second_wicket_over
            row["second_wicket_over_ball_num"] = (
                int_or_none(second_wicket["over_ball_num"])
                if second_wicket is not None
                else None
            )
            row["second_wicket_innings_ball_num"] = (
                int_or_none(second_wicket["innings_ball_num"])
                if second_wicket is not None
                else None
            )
            row["second_wicket_within_first_8_overs"] = (
                second_wicket_within_first_8
            )
            row["last_observed_overid"] = (
                int_or_none(last_delivery["overid"])
                if last_delivery is not None
                else None
            )
            row["last_observed_over_ball_num"] = (
                int_or_none(last_delivery["over_ball_num"])
                if last_delivery is not None
                else None
            )
            row["last_observed_innings_ball_num"] = (
                int_or_none(last_delivery["innings_ball_num"])
                if last_delivery is not None
                else None
            )
            row["last_observed_delivery_time"] = (
                last_delivery.get("delivery_ist_time")
                if last_delivery is not None
                else None
            )

    innings_audit = pd.DataFrame(innings_output_rows)
    middle_audit = pd.DataFrame(middle_output_rows)

    # Diagnostics are printed, not saved as additional files.
    print(f"Unique matches with any revised metadata: {len(revised_ids)}")
    print(f"Revised-metadata match IDs: {revised_ids}")
    print(f"First-innings-only match count: {len(first_only_ids)}")
    print(f"First-innings-only match IDs: {first_only_ids}")
    print(f"Overlap count: {len(overlap_ids)}")
    print(f"Overlap match IDs: {overlap_ids}")
    print(f"Live DLS candidate columns in ball_by_ball.csv: {live_dls_columns}")
    print(
        "Middle-over run sums use the runs column only; extras columns are not "
        "added because their meanings are not established here."
    )

    expected_first_only_count = 22
    if len(first_only_ids) != expected_first_only_count:
        print(
            "WARNING: The source data produced "
            f"{len(first_only_ids)} first-innings-only matches, not "
            f"{expected_first_only_count}; no IDs were added or removed to force "
            "the expected count."
        )

    innings_audit.to_csv(OUTPUT_FILES["innings"], index=False)
    middle_audit.to_csv(OUTPUT_FILES["middle"], index=False)
    revised_audit.to_csv(OUTPUT_FILES["revised"], index=False)

    print("Wrote audit outputs:")
    for key in ("innings", "middle", "revised"):
        print(f"  {OUTPUT_FILES[key]}")


if __name__ == "__main__":
    main()
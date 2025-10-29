import numpy as np
import pandas as pd
from clinicedc_constants import NO

from .constants import endpoint_columns


def get_test_string(s):
    if pd.notna(s["fbg_value"]) and pd.notna(s["ogtt_value"]):
        return "fbg_ogtt"
    if pd.notna(s["fbg_value"]) and pd.isna(s["ogtt_value"]):
        return "fbg_only"
    if pd.isna(s["fbg_value"]) and pd.notna(s["ogtt_value"]):
        return "ogtt_only"
    if pd.isna(s["fbg_value"]) and pd.isna(s["ogtt_value"]):
        return "not_tested"
    return "???"


def get_empty_endpoint_df() -> pd.DataFrame:
    endpoint_df = pd.DataFrame(columns=endpoint_columns)
    endpoint_df[
        [
            "visit_code",
            "interval_in_days",
            "fbg_value",
            "ogtt_value",
            "endpoint",
            "endpoint_type",
        ]
    ] = endpoint_df[
        [
            "visit_code",
            "interval_in_days",
            "fbg_value",
            "ogtt_value",
            "endpoint",
            "endpoint_type",
        ]
    ].apply(pd.to_numeric)
    endpoint_df[
        ["baseline_datetime", "visit_datetime", "fbg_datetime", "offstudy_datetime"]
    ] = endpoint_df[
        ["baseline_datetime", "visit_datetime", "fbg_datetime", "offstudy_datetime"]
    ].apply(pd.to_datetime)
    endpoint_df["visit_code"] = endpoint_df["visit_code"].astype(float)
    return endpoint_df


def get_unique_visit_codes(df: pd.DataFrame) -> pd.DataFrame:
    stats_df = df[df["visit_code"] % 1 == 0]["visit_code"].value_counts().to_frame()
    stats_df = stats_df.reset_index()
    stats_df["visit_code"] = stats_df["visit_code"].astype(float)
    stats_df = stats_df.sort_values(["visit_code"])
    return stats_df.reset_index(drop=True)


def get_unique_subject_identifiers(df: pd.DataFrame) -> pd.DataFrame:
    return (
        pd.DataFrame(df["subject_identifier"].unique(), columns=["subject_identifier"])
        .sort_values(["subject_identifier"])
        .reset_index()
    )


def calculate_fasting_hrs(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[(df["fasting"] == NO), "fasting_duration_delta"] = pd.NaT
    if df.empty:
        df["fasting_hrs"] = np.nan
    else:
        df["fasting_hrs"] = df["fasting_duration_delta"].apply(
            lambda s: np.nan if pd.isna(s) else s.total_seconds() / 3600
        )
    return df

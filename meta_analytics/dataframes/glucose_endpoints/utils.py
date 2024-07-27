import pandas as pd

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
    ].apply(
        pd.to_numeric
    )
    endpoint_df[
        ["baseline_datetime", "visit_datetime", "fbg_datetime", "offstudy_datetime"]
    ] = endpoint_df[
        ["baseline_datetime", "visit_datetime", "fbg_datetime", "offstudy_datetime"]
    ].apply(
        pd.to_datetime
    )
    endpoint_df["visit_code"] = endpoint_df["visit_code"].astype(float)
    return endpoint_df


def get_unique_visit_codes(source_df: pd.DataFrame) -> pd.DataFrame:
    codes = source_df[source_df["visit_code"] % 1 == 0]["visit_code"].value_counts().to_frame()
    codes = codes.reset_index()
    codes["visit_code"] = codes["visit_code"].astype(float)
    codes = codes.sort_values(["visit_code"])
    # visit_codes = visit_codes[visit_codes["visit_code"] > self.after_visit_code]
    codes = codes.reset_index(drop=True)
    return codes


def get_unique_subject_identifiers(source_df) -> pd.DataFrame:
    df = pd.DataFrame(source_df["subject_identifier"].unique(), columns=["subject_identifier"])
    df = df.sort_values(["subject_identifier"])
    df = df.reset_index()
    return df

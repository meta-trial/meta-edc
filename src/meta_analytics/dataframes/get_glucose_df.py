import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from edc_appointment.constants import MISSED_APPT  # noqa
from edc_pdutils.dataframes import get_eos, get_subject_consent, get_subject_visit

from meta_subject.models import Glucose, GlucoseFbg

pd.set_option("future.no_silent_downcasting", True)


def get_glucose_df(subject_identifiers: list[str] | None = None) -> pd.DataFrame:
    subject_visit_df = (
        get_subject_visit("meta_subject.subjectvisit", subject_identifiers)
        .rename(columns={"id": "subject_visit_id"})
        .query("appt_timing!=@MISSED_APPT")
    )
    if subject_identifiers:
        df_glucose_fbg = read_frame(
            GlucoseFbg.objects.filter(
                subject_visit__subject_identifier__in=subject_identifiers
            ),
            verbose=False,
        )
    else:
        df_glucose_fbg = read_frame(GlucoseFbg.objects.all(), verbose=False)

    df_glucose_fbg = df_glucose_fbg.rename(
        columns={"fasting": "fasted", "subject_visit": "subject_visit_id"},
    )
    df_glucose_fbg["fasting_hrs"] = np.nan
    df_glucose_fbg["fasting_hrs"] = df_glucose_fbg["fasting_duration_delta"].apply(
        lambda x: x.total_seconds() / 3600
    )
    df_glucose_fbg.loc[
        :,
        ["ogtt_value", "ogtt_units", "ogtt_datetime"],
    ] = [np.nan, None, pd.NaT]
    df_glucose_fbg["source"] = "meta_subject.glucosefbg"
    df_glucose_fbg = df_glucose_fbg[
        [col for col in df_glucose_fbg.columns if "site_id" not in col]
    ].merge(
        subject_visit_df[
            [
                "subject_identifier",
                "site_id",
                "visit_code",
                "visit_datetime",
                "baseline_datetime",
                "subject_visit_id",
            ]
        ],
        on="subject_visit_id",
        how="left",
    )

    for col in [c for c in df_glucose_fbg.columns if "datetime" in c]:
        df_glucose_fbg[col] = pd.to_datetime(df_glucose_fbg[col])

    if subject_identifiers:
        df_glucose = read_frame(
            Glucose.objects.filter(subject_visit__subject_identifier__in=subject_identifiers),
            verbose=False,
        ).rename(columns={"subject_visit": "subject_visit_id", "fasting": "fasted"})
    else:
        df_glucose = read_frame(Glucose.objects.all(), verbose=False).rename(
            columns={"subject_visit": "subject_visit_id", "fasting": "fasted"}
        )
    df_glucose = df_glucose.rename(
        columns={"subject_visit": "subject_visit_id", "fasting": "fasted"}
    )
    df_glucose["fasting_hrs"] = np.nan
    df_glucose["fasting_hrs"] = df_glucose["fasting_duration_delta"].apply(
        lambda x: x.total_seconds() / 3600
    )
    df_glucose["source"] = "meta_subject.glucose"

    for col in [c for c in df_glucose.columns if "datetime" in c]:
        df_glucose[col] = pd.to_datetime(df_glucose[col])

    df_glucose = subject_visit_df[
        [
            "subject_identifier",
            "site_id",
            "visit_code",
            "visit_datetime",
            "baseline_datetime",
            "subject_visit_id",
        ]
    ].merge(
        df_glucose[[col for col in df_glucose.columns if "site_id" not in col]],
        on="subject_visit_id",
        how="left",
    )

    keep_cols = [
        "subject_identifier",
        "site_id",
        "visit_code",
        "visit_datetime",
        "baseline_datetime",
        "subject_visit_id",
        "fasted",
        "fasting_hrs",
        "fbg_value",
        "fbg_units",
        "fbg_datetime",
        "ogtt_value",
        "ogtt_units",
        "ogtt_datetime",
        "source",
        "revision",
        "report_datetime",
    ]
    df = df_glucose[keep_cols].merge(
        df_glucose_fbg[keep_cols],
        on="subject_visit_id",
        how="outer",
        suffixes=("", "_2"),
    )

    for suffix in ["", "_2"]:
        df[[f"fasting_hrs{suffix}", f"fbg_value{suffix}", f"ogtt_value{suffix}"]] = df[
            [f"fasting_hrs{suffix}", f"fbg_value{suffix}", f"ogtt_value{suffix}"]
        ].apply(pd.to_numeric)
        df.loc[
            (df[f"fbg_units{suffix}"] != "mmol/L (millimoles/L)")
            & (df[f"fbg_value{suffix}"] >= 0),
            f"fbg_units{suffix}",
        ] = "mmol/L (millimoles/L)"
        df.loc[
            (df[f"ogtt_units{suffix}"] != "mmol/L (millimoles/L)")
            & (df[f"ogtt_value{suffix}"] >= 0),
            f"ogtt_units{suffix}",
        ] = "mmol/L (millimoles/L)"

    for col in [c for c in df.columns if "datetime" in c]:
        df[col] = pd.to_datetime(df[col])

    df[[col for col in df.columns if "datetime" in col]] = df[
        [col for col in df.columns if "datetime" in col]
    ].apply(lambda x: x.dt.tz_localize(None) if x.dtype == "datetime64[ns, UTC]" else x)

    # reconcile all to single column
    for col in ["fasted", "fbg_value", "ogtt_value", "fbg_datetime", "ogtt_datetime"]:
        df[col] = df[col].fillna(df[f"{col}_2"])

    df_consent = get_subject_consent("meta_consent.subjectconsent")
    df_eos = get_eos("meta_prn.endofstudy")
    df = df.merge(
        df_consent[["subject_identifier", "gender", "consent_datetime", "dob"]],
        on="subject_identifier",
        how="left",
    ).merge(
        df_eos[["subject_identifier", "offstudy_datetime", "offstudy_reason"]],
        on="subject_identifier",
        how="left",
    )

    df["visit_days"] = df["baseline_datetime"].rsub(df["visit_datetime"]).dt.days
    df["fgb_days"] = df["baseline_datetime"].rsub(df["fbg_datetime"]).dt.days
    df["ogtt_days"] = df["baseline_datetime"].rsub(df["ogtt_datetime"]).dt.days
    df["visit_days"] = pd.to_numeric(df["visit_days"], downcast="integer")
    df["fgb_days"] = pd.to_numeric(df["fgb_days"], downcast="integer")
    df["ogtt_days"] = pd.to_numeric(df["ogtt_days"], downcast="integer")

    return (
        df.query(
            "offstudy_reason != 'Patient fulfilled late exclusion criteria "
            "(due to abnormal blood values or raised blood pressure at enrolment'"
        )
        .copy()
        .drop(columns=[col for col in df.columns if "_2" in col])
        .sort_values(by=["subject_identifier", "visit_code"])
        .reset_index(drop=True)
    )

import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from edc_pdutils.dataframes import get_eos, get_subject_consent, get_subject_visit

from meta_subject.models import Glucose, GlucoseFbg


def get_glucose_df() -> pd.DataFrame:
    qs_glucose_fbg = GlucoseFbg.objects.all()
    df_glucose_fbg = read_frame(qs_glucose_fbg)
    df_glucose_fbg.rename(
        columns={"fbg_fasting": "fasting", "subject_visit": "subject_visit_id"},
        inplace=True,
    )

    df_glucose_fbg.loc[(df_glucose_fbg["fasting"] == "fasting"), "fasting"] = "Yes"
    df_glucose_fbg.loc[(df_glucose_fbg["fasting"] == "non_fasting"), "fasting"] = "No"
    df_glucose_fbg["fasting_hrs"] = np.nan
    df_glucose_fbg["fasting_hrs"] = df_glucose_fbg["fasting_duration_delta"].apply(
        lambda x: x.total_seconds() / 3600
    )
    df_glucose_fbg["fasting_hrs"] = df_glucose_fbg["fasting_hrs"].apply(
        lambda x: 8.05 if not x else x
    )
    # df_glucose_fbg = df_glucose_fbg.loc[df_glucose_fbg["fasting_hrs"] >= 8.0]
    # df_glucose_fbg.reset_index(drop=True, inplace=True)
    df_glucose_fbg.loc[
        :,
        ["ogtt_value", "ogtt_units", "ogtt_datetime"],
    ] = [np.nan, None, pd.NaT]
    df_glucose_fbg["source"] = "meta_subject.glucosefbg"

    qs_glucose = Glucose.objects.all()
    df_glucose = read_frame(qs_glucose)
    df_glucose.rename(columns={"subject_visit": "subject_visit_id"}, inplace=True)
    df_glucose.loc[(df_glucose["fasting"] == "fasting"), "fasting"] = "Yes"
    df_glucose.loc[(df_glucose["fasting"] == "non_fasting"), "fasting"] = "No"
    df_glucose["fasting_hrs"] = np.nan
    df_glucose["fasting_hrs"] = df_glucose[df_glucose["fasting"] == "Yes"][
        "fasting_duration_delta"
    ].apply(lambda x: x.total_seconds() / 3600)
    df_glucose["fasting_hrs"] = df_glucose["fasting_hrs"].apply(lambda x: 8.05 if not x else x)
    # df_glucose = df_glucose.loc[df_glucose["fasting_hrs"] >= 8.0]
    # df_glucose.reset_index(drop=True, inplace=True)
    df_glucose["source"] = "meta_subject.glucose"

    keep_cols = [
        "subject_visit_id",
        "fasting",
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
    df_glucose = df_glucose[keep_cols]
    df_glucose_fbg = df_glucose_fbg[keep_cols]
    # df = pd.concat([df_glucose_fbg, df_glucose])
    df = pd.merge(
        df_glucose,
        df_glucose_fbg,
        on="subject_visit_id",
        how="outer",
        indicator=True,
        suffixes=("", "_2"),
    )

    for suffix in ["", "_2"]:
        cols = [f"fasting_hrs{suffix}", f"fbg_value{suffix}", f"ogtt_value{suffix}"]
        df[cols] = df[cols].apply(pd.to_numeric)
        cols = [f"fbg_datetime{suffix}", f"ogtt_datetime{suffix}"]
        df[cols] = df[cols].apply(pd.to_datetime)
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
        # remove values if not fasted
        # df.loc[(df[f"fasting{suffix}"] != YES), f"fbg_value{suffix}"] = np.nan
        # df.loc[(df[f"fasting{suffix}"] != YES), f"ogtt_value{suffix}"] = np.nan

    # reconcile all to single column
    df.loc[(df["fbg_value"].isna()) & (df["fbg_value_2"].notna()), "fbg_value"] = df[
        "fbg_value_2"
    ]
    df.loc[(df["ogtt_value"].isna()) & (df["ogtt_value_2"].notna()), "ogtt_value"] = df[
        "ogtt_value_2"
    ]
    cols = [col for col in list(df.columns) if col.endswith("_2")]
    df.drop(columns=cols, inplace=True)
    cols = [col for col in list(df.columns) if col.endswith("_3")]
    df.drop(columns=cols, inplace=True)

    df_subject_visit = get_subject_visit("meta_subject.subjectvisit")
    df_consent = get_subject_consent("meta_consent.subjectconsent")
    df_eos = get_eos("meta_prn.endofstudy")

    df = pd.merge(df_subject_visit, df, on="subject_visit_id", how="left")
    df = pd.merge(df, df_consent, on="subject_identifier", how="left")
    df = pd.merge(df, df_eos, on="subject_identifier", how="left")

    df["visit_days"] = df["baseline_datetime"].rsub(df["visit_datetime"]).dt.days
    df["fgb_days"] = df["baseline_datetime"].rsub(df["fbg_datetime"]).dt.days
    df["ogtt_days"] = df["baseline_datetime"].rsub(df["ogtt_datetime"]).dt.days
    df["visit_days"] = pd.to_numeric(df["visit_days"], downcast="integer")
    df["fgb_days"] = pd.to_numeric(df["fgb_days"], downcast="integer")
    df["ogtt_days"] = pd.to_numeric(df["ogtt_days"], downcast="integer")

    df = df.sort_values(by=["subject_identifier", "visit_code"])
    df.reset_index(drop=True, inplace=True)
    return df

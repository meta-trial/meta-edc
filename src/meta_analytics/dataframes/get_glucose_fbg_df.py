import pandas as pd
from clinicedc_constants import NO, YES
from edc_pdutils.dataframes import get_crf

from meta_analytics.dataframes.utils import calculate_fasting_hrs

__all__ = ["get_glucose_fbg_df"]


def get_glucose_fbg_df(subject_identifiers: list[str] | None = None) -> pd.DataFrame:
    """Returns a prepared Dataframe of CRF
    meta_subject.glucosefbg.

    Note: meta_subject.glucosefbg has only FBG measures.
    """
    df = get_crf(
        model="meta_subject.glucosefbg",
        subject_identifiers=subject_identifiers or [],
        subject_visit_model="meta_subject.subjectvisit",
    )
    df["source"] = "meta_subject.glucosefbg"
    df = df.rename(columns={"fbg_fasting": "fasting"})
    df.loc[(df["fasting"] == "fasting"), "fasting"] = YES
    df.loc[(df["fasting"] == "non_fasting"), "fasting"] = NO
    df = calculate_fasting_hrs(df)
    return df.reset_index(drop=True)

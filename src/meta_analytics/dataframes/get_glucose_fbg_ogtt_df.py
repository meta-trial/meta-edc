import pandas as pd
from edc_pdutils.dataframes import get_crf

from .utils import calculate_fasting_hrs

__all__ = ["get_glucose_fbg_ogtt_df"]


def get_glucose_fbg_ogtt_df(subject_identifiers: list[str] | None = None) -> pd.DataFrame:
    """Returns a prepared Dataframe of CRF meta_subject.glucose.

    Note: meta_subject.glucose has FBG and OGTT measures.
    """
    df = get_crf(
        model="meta_subject.glucose",
        subject_identifiers=subject_identifiers or [],
        subject_visit_model="meta_subject.subjectvisit",
    )
    df["source"] = "meta_subject.glucose"
    df = calculate_fasting_hrs(df)
    return df.reset_index(drop=True)

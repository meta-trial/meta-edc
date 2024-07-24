import pandas as pd
from django_pandas.io import read_frame

from meta_prn.models import EndOfStudy


def get_eos() -> pd.DataFrame:
    qs = EndOfStudy.objects.values(
        "subject_identifier", "offstudy_datetime", "offstudy_reason"
    ).all()
    df = read_frame(qs)
    df["offstudy_datetime"] = df["offstudy_datetime"].apply(pd.to_datetime)
    df["offstudy_datetime"] = df["offstudy_datetime"].dt.floor("d")
    df.sort_values(by=["subject_identifier"])
    df.reset_index(drop=True, inplace=True)
    return df

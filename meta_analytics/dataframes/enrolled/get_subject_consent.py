import pandas as pd
from django_pandas.io import read_frame

from meta_consent.models import SubjectConsent


def get_subject_consent() -> pd.DataFrame:
    qs_consent = SubjectConsent.objects.values(
        "subject_identifier", "gender", "dob", "screening_identifier", "consent_datetime"
    ).all()
    df = read_frame(qs_consent)
    df["dob"] = df["dob"].apply(pd.to_datetime)
    df["consent_datetime"] = df["consent_datetime"].apply(pd.to_datetime)
    df["consent_datetime"] = df["consent_datetime"].dt.floor("d")
    df["age_in_years"] = df["consent_datetime"].dt.year - df["dob"].dt.year
    df.sort_values(by=["subject_identifier"])
    df.reset_index(drop=True, inplace=True)
    return df

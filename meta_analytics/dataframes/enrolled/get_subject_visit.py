import pandas as pd
from django_pandas.io import read_frame

from meta_subject.models import SubjectVisit


def get_subject_visit(floor_datetimes: bool | None = None) -> pd.DataFrame:
    floor_datetimes = True if floor_datetimes is None else floor_datetimes
    qs_subject_visit = SubjectVisit.objects.all()
    df_subject_visit = read_frame(qs_subject_visit)
    df_subject_visit.rename(
        columns={"id": "subject_visit_id", "report_datetime": "visit_datetime"}, inplace=True
    )
    df_subject_visit = df_subject_visit[
        [
            "subject_visit_id",
            "subject_identifier",
            "visit_code",
            "visit_code_sequence",
            "visit_datetime",
        ]
    ]
    # convert visit_code to float using visit_code_sequence
    df_subject_visit["visit_code"] = df_subject_visit["visit_code"].astype(float)
    df_subject_visit["visit_code_sequence"] = df_subject_visit["visit_code_sequence"].astype(
        float
    )
    df_subject_visit["visit_datetime"] = df_subject_visit["visit_datetime"].apply(
        pd.to_datetime
    )
    df_subject_visit["visit_code_sequence"] = df_subject_visit["visit_code_sequence"].apply(
        lambda x: x / 10.0 if x > 0.0 else 0.0
    )
    df_subject_visit["visit_code"] = (
        df_subject_visit["visit_code"] + df_subject_visit["visit_code_sequence"]
    )
    df_subject_visit.drop(columns=["visit_code_sequence"])

    df_baseline_visit = df_subject_visit.copy()
    df_baseline_visit = df_baseline_visit[(df_baseline_visit["visit_code"] == 1000.0)]
    df_baseline_visit.rename(columns={"visit_datetime": "baseline_datetime"}, inplace=True)
    df_baseline_visit = df_baseline_visit[["subject_identifier", "baseline_datetime"]]

    df_subject_visit = pd.merge(
        df_subject_visit, df_baseline_visit, on="subject_identifier", how="left"
    )

    if floor_datetimes:
        df_subject_visit["visit_datetime"] = df_subject_visit["visit_datetime"].dt.floor("d")
        df_subject_visit["baseline_datetime"] = df_subject_visit["baseline_datetime"].dt.floor(
            "d"
        )

    df_subject_visit = df_subject_visit.sort_values(by=["subject_identifier", "visit_code"])
    df_subject_visit.reset_index(drop=True, inplace=True)
    return df_subject_visit

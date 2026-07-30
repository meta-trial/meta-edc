import pandas as pd
from django_pandas.io import read_frame

from meta_subject.models import (
    BloodResultsFbc,
    # BloodResultsGluDummy,
    BloodResultsHba1c,
    BloodResultsIns,
    BloodResultsLft,
    BloodResultsLipids,
    BloodResultsRft,
    SubjectVisit,
)

__all__ = ["get_df_bloodresults"]


def get_df_bloodresults() -> pd.DataFrame:
    """Return a pivoted dataframe of all blood result CRFs."""

    df_bloodresults = pd.DataFrame()

    for model_cls in [
        BloodResultsFbc,
        # BloodResultsGluDummy,
        BloodResultsHba1c,
        BloodResultsIns,
        BloodResultsLft,
        BloodResultsLipids,
        BloodResultsRft,
    ]:
        value_cols = [
            f.name for f in model_cls._meta.get_fields() if f.name.endswith("_value")
        ]

        df = (
            read_frame(
                model_cls.objects.values(
                    "subject_visit", "requisition", "requisition__panel__name", *value_cols
                ).all(),
                verbose=False,
            )
            .rename(columns={"requisition__panel__name": "panel_name"})
            .reset_index(drop=True)
        )

        wide = (
            df.melt(
                id_vars=["subject_visit", "requisition", "panel_name"],
                value_vars=value_cols,
                var_name="utestid",
                value_name="result_value",
            )
            .assign(utestid=lambda d: d["utestid"].str.removesuffix("_value"))
            .dropna(subset=["result_value"])
            .reset_index(drop=True)
        )
        wide["source"] = model_cls._meta.label_lower
        df_bloodresults = pd.concat([df_bloodresults, wide])

    for col in ["subject_visit", "requisition", "panel_name", "utestid"]:
        df_bloodresults[col] = (
            df_bloodresults[col].astype("string").str.strip().replace("", pd.NA)
        )

    df_subject_visit = (
        read_frame(
            SubjectVisit.objects.values(
                "appointment__subject_identifier",
                "id",
                "visit_code",
                "visit_code_sequence",
                "report_datetime",
            ).all(),
            verbose=False,
        )
        .rename(
            columns={
                "appointment__subject_identifier": "subject_identifier",
                "id": "subject_visit",
                "report_datetime": "visit_datetime",
            }
        )
        .reset_index(drop=True)
    )

    for col in ["subject_visit", "subject_identifier", "visit_code"]:
        df_subject_visit[col] = (
            df_subject_visit[col].astype("string").str.strip().replace("", pd.NA)
        )

    return df_bloodresults.merge(df_subject_visit, on="subject_visit", how="left")

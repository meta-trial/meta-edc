import pandas as pd
from edc_pdutils.dataframes import get_eos, get_subject_visit


def get_eos_df() -> pd.DataFrame:
    """
    df = get_eos_df()

    # look at transfers and last attended visit
    df[(df.transfer_reason.notna())]

    """
    df_eos = get_eos("meta_prn.endofstudy")
    df_visit = get_subject_visit("meta_subject.subjectvisit")
    df_last_visit = (
        df_visit.groupby(["subject_identifier", "site_id"])
        .agg({"endline_visit_code": "max", "endline_visit_datetime": "max"})
        .reset_index()
    )
    # df_last_visit = df_last_visit.rename(columns={"site": "site_id"})

    df_eos = df_eos.merge(
        df_last_visit, on="subject_identifier", how="left", suffixes=("", "_y")
    )
    df_eos = df_eos.drop(columns=["site_id_y"])
    df_visit_grp = (
        df_visit.groupby(by=["subject_identifier"])[["baseline_datetime", "visit_datetime"]]
        .max()
        .reset_index()
    )
    df_visit_grp["followup_days"] = (
        df_visit_grp["visit_datetime"] - df_visit_grp["baseline_datetime"]
    ).dt.days
    return df_eos.merge(
        df_visit_grp[["subject_identifier", "followup_days"]],
        on="subject_identifier",
        how="left",
    ).reset_index(drop=True)

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
        df_visit.groupby(["subject_identifier", "site"])
        .agg({"last_visit_code": "max", "last_visit_datetime": "max"})
        .reset_index()
    )
    df_last_visit = df_last_visit.rename(columns={"site": "site_id"})

    df_eos = df_eos.merge(
        df_last_visit, on="subject_identifier", how="left", suffixes=("", "_y")
    )
    df_eos = df_eos.drop(columns=["site_id_y"])
    return df_eos

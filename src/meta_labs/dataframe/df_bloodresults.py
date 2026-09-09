import pandas as pd
from edc_lab_results.dataframes import get_df_result_crfs

__all__ = ["get_df_bloodresults"]


def get_df_bloodresults() -> pd.DataFrame:
    """Return a pivoted dataframe of all blood result CRFs.

    A thin wrapper over `get_df_result_crfs`, which reads the result
    CRFs from the panel registry rather than a hardcoded list, so any
    result CRF meta installs is included without editing this. The
    column names here are the ones the existing notebooks read.

    `get_df_result_crfs` keeps the rows with no value, so the grid is
    complete. They are dropped here, as they always were. See
    `get_df_result_comparison` for the frame that reconciles this
    against the imported lab results.
    """
    return (
        get_df_result_crfs()
        .rename(
            columns={
                "subject_visit_id": "subject_visit",
                "requisition_id": "requisition",
                "crf_value": "result_value",
                "crf_model": "source",
            }
        )
        .loc[
            :,
            [
                "subject_visit",
                "requisition",
                "panel_name",
                "utestid",
                "result_value",
                "source",
                "subject_identifier",
                "visit_code",
                "visit_code_sequence",
                "visit_datetime",
            ],
        ]
        .dropna(subset=["result_value"])
        .reset_index(drop=True)
    )

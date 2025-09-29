import pandas as pd

from .get_screening_df import get_screening_df


def get_glucose_tested_only_df(df: pd.DataFrame | None = None):
    """ "Returns a DF of 5618 records"""
    df = pd.DataFrame() if not hasattr(df, "empty") else df
    if df.empty:
        df = get_screening_df()
    # condition where subject is eligible P1/P2 and has any type of glucose test
    cond_glu = (
        (df["fbg_value"].notna())
        | (df["ogtt_value"].notna())
        | (df["fbg2_value"].notna())
        | (df["ogtt2_value"].notna())
    )
    cond = (df["eligible_part_one"] == "Yes") & (df["eligible_part_two"] == "Yes") & cond_glu
    return df[cond]

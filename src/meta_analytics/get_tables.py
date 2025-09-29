import pandas as pd
from edc_analytics.custom_tables import (
    AgeTable,
    ArtTable,
    BmiTable,
    BpTable,
    FastingTable,
    FbgOgttTable,
    FbgTable,
    GenderTable,
    HbA1cTable,
    OgttTable,
    WaistCircumferenceTable,
)
from edc_analytics.data import Data

from .dataframes import get_glucose_tested_only_df, get_screening_df
from .tables import EligibleP12Table, HasDmTable


def get_tables() -> dict[str, Data]:
    """
    results = get_table()
    results.get("fbg").to_csv(folder="/Users/erikvw/Documents/")
    """
    df_screening = get_screening_df()
    df_has_dm = df_screening[(df_screening["has_dm"] == "Yes")]
    df_no_dm = df_screening[(df_screening["has_dm"] == "No")]
    df_fbg = get_glucose_tested_only_df(df_screening)

    df_not_tested = df_no_dm.copy()
    df_not_eligible_p1p2 = df_not_tested[
        ~(
            (df_not_tested["eligible_part_one"] == "Yes")
            & (df_not_tested["eligible_part_two"] == "Yes")
        )
    ]
    df_not_tested = df_not_tested.drop(df_not_eligible_p1p2.index).drop(df_fbg.index)

    df_stats = pd.DataFrame(
        {
            "df": ["df_screening", "df_has_dm", "df_no_dm", "df_not_tested", "df_fbg"],
            "count": [
                len(df_screening),
                len(df_has_dm),
                len(df_no_dm),
                len(df_not_tested),
                len(df_fbg),
            ],
        }
    )

    results = {"stats": df_stats}
    for key, df in {
        "screening": df_screening,
        "has_dm": df_has_dm,
        "no_dm": df_no_dm,
        "not_tested": df_not_tested,
        "fbg": df_fbg,
    }.items():
        dfs = []
        for tbl_cls in [
            GenderTable,
            AgeTable,
            WaistCircumferenceTable,
            BmiTable,
            BpTable,
            ArtTable,
            FastingTable,
            FbgTable,
            OgttTable,
            FbgOgttTable,
            HbA1cTable,
            EligibleP12Table,
            HasDmTable,
        ]:
            tbl = tbl_cls(main_df=df)
            dfs.append(tbl.table_df)
        results.update({key: Data(key, pd.concat(list(dfs)), df, "meta3")})
    return results

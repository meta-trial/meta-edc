from datetime import datetime
from pathlib import Path

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

from meta_analytics.dataframes import get_glucose_tested_only_df, get_screening_df
from meta_analytics.tables import EligibleP12Table, HasDmTable


class Data:
    def __init__(self, label: str, table_df: pd.DataFrame, data_df: pd.DataFrame):
        self.label = label
        self.table_df = table_df
        self.data_df = data_df

    def __repr__(self):
        return f"{self.label} obs={len(self.data_df)}"

    def to_csv(
        self, folder: str | None = None, filename: str | None = None, cols: int | None = None
    ):
        folder = folder or "/Users/erikvw/Documents/ucl/protocols/meta3/reports/"
        cols = cols or 5
        datestamp = datetime.now().strftime("%Y%m%d%H%M")
        filename = filename or f"meta3_table_{self.label}_{datestamp}.csv"
        path = Path(folder) / filename
        self.table_df.iloc[:, :cols].to_csv(
            path_or_buf=path, encoding="utf-8", index=0, sep="|"
        )


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
    df_not_tested.drop(df_not_eligible_p1p2.index, inplace=True)
    df_not_tested.drop(df_fbg.index, inplace=True)

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
        results.update({key: Data(key, pd.concat(list(dfs)), df)})
    return results

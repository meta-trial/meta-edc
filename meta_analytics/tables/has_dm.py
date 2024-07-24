import pandas as pd
from edc_analytics.constants import N_ONLY, N_WITH_COL_PROP, N_WITH_ROW_PROP
from edc_analytics.row import RowDefinition, RowDefinitions
from edc_analytics.table import Table


class HasDmTable(Table):
    def __init__(self, main_df: pd.DataFrame = None):
        super().__init__(
            colname="", main_df=main_df, title="Subjects reporting having Diabetes"
        )

    @property
    def row_definitions(self) -> RowDefinitions:
        df_tmp = self.main_df.copy()
        row_defs = RowDefinitions(reverse_rows=False)
        row0 = RowDefinition(
            title=self.title,
            label=self.default_sublabel,
            condition=(df_tmp["gender"].notna()),
            columns={
                "F": (N_ONLY, 2),
                "M": (N_ONLY, 2),
                "All": (N_ONLY, 2),
            },
            drop=False,
        )
        row_defs.add(row0)
        columns = {
            "F": (N_WITH_COL_PROP, 2),
            "M": (N_WITH_COL_PROP, 2),
            "All": (N_WITH_ROW_PROP, 2),
        }
        row_defs.add(
            RowDefinition(
                label="Yes",
                condition=(df_tmp["has_dm"] == "Yes"),
                columns=columns,
                drop=True,
            )
        )

        row_defs.add(
            RowDefinition(
                label="No",
                condition=(df_tmp["has_dm"] == "No"),
                columns=columns,
                drop=True,
            )
        )

        row_defs.add(
            RowDefinition(
                label="Not evaluated",
                condition=(df_tmp["has_dm"] == "unk"),
                columns=columns,
                drop=True,
            )
        )

        return row_defs

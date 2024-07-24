import pandas as pd
from edc_analytics.constants import N_ONLY, N_WITH_COL_PROP, N_WITH_ROW_PROP
from edc_analytics.row import RowDefinition, RowDefinitions
from edc_analytics.table import Table


class EligibleP12Table(Table):
    def __init__(self, main_df: pd.DataFrame = None):
        super().__init__(colname="", main_df=main_df, title="Eligible by Part 1/2")

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
                label="Eligible P1",
                condition=(df_tmp["eligible_part_one"] == "Yes"),
                columns=columns,
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                label="Eligible P2",
                condition=(df_tmp["eligible_part_two"] == "Yes"),
                columns=columns,
                drop=False,
            )
        )

        row_defs.add(
            RowDefinition(
                label="Eligible P1 & P2",
                condition=(df_tmp["eligible_part_one"] == "Yes")
                & (df_tmp["eligible_part_two"] == "Yes"),
                columns=columns,
                drop=False,
            )
        )
        # note already_fasted accepts Y/N/NA
        row_defs.add(
            RowDefinition(
                label="Glucose tested (fasted on day)",
                condition=(
                    (df_tmp["already_fasted"] == "Yes")
                    & ((df_tmp["fbg"].notna()) | (df_tmp["ogtt"].notna()))
                ),
                columns=columns,
                drop=True,
            )
        )

        row_defs.add(
            RowDefinition(
                label="Glucose tested (returned fasted)",
                condition=(
                    (df_tmp["already_fasted"] == "No")
                    & ((df_tmp["fbg"].notna()) | (df_tmp["ogtt"].notna()))
                ),
                columns=columns,
                drop=True,
            )
        )

        row_defs.add(
            RowDefinition(
                label="Glucose tested (N/A)",
                condition=(df_tmp["already_fasted"] == "N/A")
                & ((df_tmp["fbg"].notna()) | (df_tmp["ogtt"].notna())),
                columns=columns,
                drop=True,
            )
        )

        row_defs.add(
            RowDefinition(
                label="No glucose test (not fasted on day and did not return)",
                condition=(
                    (df_tmp["eligible_part_one"] == "Yes")
                    & (df_tmp["eligible_part_two"] == "Yes")
                    & (df_tmp["fbg"].isna())
                    & (df_tmp["ogtt"].isna())
                ),
                columns=columns,
                drop=False,
            )
        )
        return row_defs

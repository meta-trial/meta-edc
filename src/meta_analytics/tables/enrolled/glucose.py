import pandas as pd
from edc_analytics.custom_tables import AgeTable, GenderTable
from edc_analytics.table import Table


class GlucoseTable(Table):
    """
    gender
    age
    fasting
    fbg mean
    ogtt mean
    fbg + ogtt count
    """

    def __init__(self, main_df: pd.DataFrame = None):
        super().__init__(colname="", main_df=main_df, title="Glucose (enrolled)")

    def build_table_df(self) -> None:
        super().build_table_df()
        df = self.main_df
        s = df.groupby("subject_identifier")[["age_in_years", "gender"]].value_counts()
        df_tmp = s.to_frame()
        df_tmp = df_tmp.reset_index()
        gender_tbl = GenderTable(main_df=df_tmp).table_df
        age_tbl = AgeTable(main_df=df_tmp).table_df
        self.table_df = pd.concat([self.table_df, gender_tbl, age_tbl]).reset_index(drop=True)

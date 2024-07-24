import numpy as np
import pandas as pd


class EndpointTdeltaError(Exception):
    pass


class EndpointByDate:

    cases = {
        1: "FBG >= 7 x 2, second OGTT<=11.1",
        2: "FBG >= 7 x 2, first OGTT<=11.1",
        # 3: "FBG >= 7 x 2, first OGTT<=11.1 (allow missed)",
        # 4: "FBG >= 7 x 2, second OGTT<=11.1 (allow missed)",
        5: "FBG >= 7 x 2, OGTT not considered (allow missed)",
        # 6: "OGTT >= 11.1",
        # 7: "EOS DM",
    }

    def __init__(
        self,
        index: int = None,
        row: pd.Series = None,
        subject_df: pd.DataFrame = None,
        visit_codes: pd.DataFrame = None,
        fbg_threshhold: float = None,
        ogtt_threshhold: float = None,
    ):
        self.index = index
        self.row = row
        self.subject_df = subject_df
        self.visit_codes = visit_codes
        self.fbg_threshhold = fbg_threshhold
        self.ogtt_threshhold = ogtt_threshhold

    def endpoint_reached(self, case: int):
        """Update the subject_df"""
        self.subject_df.loc[
            self.subject_df["fbg_datetime"] == self.row.fbg_datetime, "endpoint"
        ] = 1
        self.subject_df["interval_in_days"] = np.nan
        try:
            self.subject_df.loc[
                self.subject_df["fbg_datetime"] == self.row.fbg_datetime, "interval_in_days"
            ] = self.sequential_assessments_in_days
        except EndpointTdeltaError:
            pass
        self.subject_df["interval_in_days"] = pd.to_numeric(
            self.subject_df["interval_in_days"]
        )
        self.subject_df.loc[
            self.subject_df["fbg_datetime"] == self.row.fbg_datetime, "endpoint_type"
        ] = case
        self.subject_df.loc[
            self.subject_df["fbg_datetime"] == self.row.fbg_datetime, "endpoint_label"
        ] = self.cases[case]

    def case_one(self):
        """FBG >= 7 x 2, second OGTT<=11.1

        Must Following schedule as per protocol, that is
        the next visit code is the expected one"""
        reached = (
            self.next_fbg_datetime
            and self.row.fbg_value
            and self.next_fbg_value
            and self.next_ogtt_value
            and self.row.fbg_value >= self.fbg_threshhold
            and self.next_fbg_value >= self.fbg_threshhold
            and self.next_ogtt_value < self.ogtt_threshhold
        )
        if reached:
            self.endpoint_reached(1)
        return reached

    def case_two(self):
        """FBG >= 7 x 2, first OGTT<=11.1"""
        reached = (
            self.next_fbg_datetime
            and self.row.fbg_value
            and self.next_fbg_value
            and self.next_ogtt_value
            and self.row.fbg_value >= self.fbg_threshhold
            and self.next_fbg_value >= self.fbg_threshhold
            and self.row.ogtt_value < self.ogtt_threshhold
        )
        if reached:
            self.endpoint_reached(2)
        return reached

    def case_five(self):
        """FBG >= 7 x 2, OGTT not considered (allow missed)"""
        reached = (
            self.next_fbg_datetime
            and self.row.fbg_value
            and self.next_fbg_value
            and self.next_ogtt_value
            and self.row.fbg_value >= self.fbg_threshhold
            and self.next_fbg_value >= self.fbg_threshhold
        )
        if reached:
            self.endpoint_reached(5)
        return reached

    @property
    def next_fbg_datetime(self) -> float | None:
        """Return next fbg_datetime reported in data."""
        return self.get_next_value("fbg_datetime")

    @property
    def sequential_assessments_in_days(self) -> int:
        if not self.next_fbg_datetime:
            raise EndpointTdeltaError
        return (self.next_fbg_datetime - self.row.visit_datetime).days

    @property
    def next_fbg_value(self) -> float | None:
        return self.get_next_value("fbg_value")

    @property
    def next_ogtt_value(self) -> float | None:
        return self.get_next_value("ogtt_value")

    def get_next_value(self, column: str) -> float | None:
        a, b = (self.index + 1, self.index + 2)
        try:
            next_value = self.subject_df.iloc[a:b][column].item()
        except ValueError:
            next_value = None
        return next_value

    def get_previous_value(self, column: str) -> float | None:
        a, b = (self.index - 1, self.index)
        try:
            next_value = self.subject_df.iloc[a:b][column].item()
        except ValueError:
            next_value = None
        return next_value

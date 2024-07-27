import numpy as np
import pandas as pd
from edc_constants.constants import YES


class EndpointTdeltaError(Exception):
    pass


class EndpointByDate:

    cases = {
        1: "FBG >= 7 x 2, second OGTT<=11.1",
        2: "FBG >= 7 x 2, first OGTT<=11.1",
        5: "FBG >= 7 x 2, OGTT not considered (allow missed)",
    }

    def __init__(
        self,
        subject_df: pd.DataFrame = None,
        fbg_threshhold: float = None,
        ogtt_threshhold: float = None,
        case_list: list[int] | None = None,
    ):
        self.row = None
        self.index = None
        self.subject_df = subject_df[subject_df["fbg_value"].notna()]
        self.subject_df.reset_index(drop=True)
        self.fbg_threshhold = fbg_threshhold
        self.ogtt_threshhold = ogtt_threshhold
        self.case_list = case_list or [1, 2]
        self.evaluate()

    def evaluate(self):
        for index, _ in self.subject_df.iterrows():
            if 1 in self.case_list and self.case_one(index):
                break
            elif 2 in self.case_list and self.case_two(index):
                break
            elif 5 in self.case_list and self.case_five(index):
                break

    def endpoint_reached(self, index: int, case: int, next_is_endpoint: bool | None = None):
        """Update the subject_df"""
        fbg_datetime = (
            self.get_next("fbg_datetime", index)
            if next_is_endpoint
            else self.get("fbg_datetime", index)
        )
        self.subject_df.loc[self.subject_df["fbg_datetime"] == fbg_datetime, "endpoint"] = 1
        self.subject_df["interval_in_days"] = np.nan
        try:
            self.subject_df.loc[
                self.subject_df["fbg_datetime"] == fbg_datetime, "interval_in_days"
            ] = self.sequential_assessments_in_days(index)
        except EndpointTdeltaError:
            pass
        self.subject_df["interval_in_days"] = pd.to_numeric(
            self.subject_df["interval_in_days"]
        )
        self.subject_df.loc[
            self.subject_df["fbg_datetime"] == fbg_datetime, "endpoint_type"
        ] = case
        self.subject_df.loc[
            self.subject_df["fbg_datetime"] == fbg_datetime, "endpoint_label"
        ] = self.cases[case]

    def fasting(self, index) -> bool:
        return self.get("fasting", index) == YES and self.get_next("fasting", index) == YES

    def case_one(self, index: int):
        """FBG >= 7 x 2, second OGTT<=11.1.

        Second FBG must be done with corresponding OGTT.
        """
        reached = (
            self.get_next("fbg_datetime", index)
            and self.get("fbg_value", index)
            and self.get_next("fbg_value", index)
            and self.get_next("ogtt_value", index)
            and self.get("fbg_value", index) >= self.fbg_threshhold
            and self.get_next("fbg_value", index) >= self.fbg_threshhold
            and self.get_next("ogtt_value", index) < self.ogtt_threshhold
            and self.fasting(index)
            and (self.get_next("fbg_datetime", index) - self.get("fbg_datetime", index)).days
            >= 7
        )
        if reached:
            self.endpoint_reached(index, case=1, next_is_endpoint=True)
        return reached

    def case_two(self, index: int):
        """FBG >= 7 x 2, first OGTT<=11.1.

        First FBG must be done with corresponding OGTT.
        """
        reached = (
            self.get_next("fbg_datetime", index)
            and self.get("fbg_value", index)
            and self.get("ogtt_value", index)
            and self.get_next("fbg_value", index)
            and self.get("fbg_value", index) >= self.fbg_threshhold
            and self.get("ogtt_value", index) < self.ogtt_threshhold
            and self.get_next("fbg_value", index) >= self.fbg_threshhold
            and self.fasting(index)
            and (self.get_next("fbg_datetime", index) - self.get("fbg_datetime", index)).days
            >= 7
        )
        if reached:
            self.endpoint_reached(index, case=2, next_is_endpoint=True)
        return reached

    def case_five(self, index: int):
        """FBG >= 7 x 2, OGTT not considered (allow missed)

        This is not a protocol endpoint.
        """
        reached = (
            self.get_next("fbg_datetime", index)
            and self.get("fbg_value", index)
            and self.get_next("fbg_value", index)
            and self.get_next("ogtt_value", index)
            and self.get("fbg_value", index) >= self.fbg_threshhold
            and self.get_next("fbg_value", index) >= self.fbg_threshhold
            and self.fasting(index)
        )
        if reached:
            self.endpoint_reached(index, case=5, next_is_endpoint=True)
        return reached

    def sequential_assessments_in_days(self, index) -> int:
        if not self.get_next("fbg_value", index):
            raise EndpointTdeltaError
        return (self.get_next("fbg_datetime", index) - self.get("visit_datetime", index)).days

    def get(self, col: str, index: int) -> float | None:
        try:
            next_value = self.subject_df.iloc[index : index + 1][col].item()
        except ValueError:
            next_value = None
        return next_value

    def get_next(self, col: str, index: int) -> float | None:
        return self.get(col, index + 1)

from datetime import datetime

import pandas as pd


class EndpointTdeltaError(Exception):
    pass


class EndpointByVisitCode:

    cases = {
        1: "FBG >= 7 x 2, second OGTT<=11.1",
        2: "FBG >= 7 x 2, first OGTT<=11.1",
        3: "FBG >= 7 x 2, first OGTT<=11.1 (allow missed)",
        4: "FBG >= 7 x 2, second OGTT<=11.1 (allow missed)",
        5: "FBG >= 7 x 2, OGTT not considered (allow missed)",
        6: "OGTT >= 11.1",
        7: "EOS DM",
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
            self.subject_df["visit_code"] == self.row.visit_code, "endpoint"
        ] = 1
        try:
            self.subject_df.loc[
                self.subject_df["visit_code"] == self.row.visit_code, "interval_in_days"
            ] = self.sequential_assessments_in_days
        except EndpointTdeltaError:
            pass
        self.subject_df["interval_in_days"] = pd.to_numeric(
            self.subject_df["interval_in_days"]
        )
        self.subject_df.loc[
            self.subject_df["visit_code"] == self.row.visit_code, "endpoint_type"
        ] = case
        self.subject_df.loc[
            self.subject_df["visit_code"] == self.row.visit_code, "endpoint_label"
        ] = self.cases[case]

    def case_one(self):
        """FBG >= 7 x 2, second OGTT<=11.1

        Must Following schedule as per protocol, that is
        the next visit code is the expected one"""
        reached = (
            self.next_expected_visit_code
            and self.next_visit
            and self.has_sequential_assessments
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
            self.next_expected_visit_code
            and self.next_visit
            and (
                (self.next_visit == self.next_expected_visit_code)
                or (self.next_visit == self.row.visit_code + 0.1)
            )
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

    def case_three(self):
        """FBG >= 7 x 2, first OGTT<=11.1 (allow missed)"""
        reached = (
            self.next_visit_datetime
            # and (self.next_visit_datetime - self.row.visit_datetime).days >= 7
            and self.row.fbg_value
            and self.next_fbg_value
            and self.next_ogtt_value
            and self.row.fbg_value >= self.fbg_threshhold
            and self.next_fbg_value >= self.fbg_threshhold
            and self.row.ogtt_value < self.ogtt_threshhold
        )
        if reached:
            self.endpoint_reached(3)
        return reached

    def case_four(self):
        """FBG >= 7 x 2, second OGTT<=11.1 (allow missed)"""
        reached = (
            self.next_visit_datetime
            # and (self.next_visit_datetime - self.row.visit_datetime).days >= 7
            and self.row.fbg_value
            and self.next_fbg_value
            and self.next_ogtt_value
            and self.row.fbg_value >= self.fbg_threshhold
            and self.next_fbg_value >= self.fbg_threshhold
            and self.next_ogtt_value < self.ogtt_threshhold
        )
        if reached:
            self.endpoint_reached(4)
        return reached

    def case_five(self):
        """FBG >= 7 x 2, OGTT not considered (allow missed)"""
        reached = (
            self.next_visit_datetime
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
    def next_visit(self) -> float | None:
        """Return next visit code reported in data."""
        return self.get_next_value("visit_code")

    @property
    def next_expected_visit_code(self) -> float | None:
        """Return next scheduled visit code (.0) expected based
        on general meta visit schedule.
        """
        try:
            next_expected_visit_code = self.visit_codes[
                self.visit_codes["visit_code"] > self.row.visit_code
            ]["visit_code"][0:1].item()
        except ValueError:
            next_expected_visit_code = None
        return next_expected_visit_code

    @property
    def has_sequential_assessments(self):
        return (self.next_visit == self.next_expected_visit_code) or (
            self.next_visit == self.row.visit_code + 0.1
        )

    @property
    def sequential_assessments_in_days(self) -> int:
        if self.next_visit == self.next_expected_visit_code:
            tdelta = self.get_next_value("visit_datetime") - self.row.visit_datetime
        elif self.next_visit == self.row.visit_code + 0.1:
            tdelta = self.get_next_value("visit_datetime") - self.row.visit_datetime
        else:
            raise EndpointTdeltaError
        return tdelta.days

    @property
    def next_fbg_value(self) -> float | None:
        return self.get_next_value("fbg_value")

    @property
    def next_ogtt_value(self) -> float | None:
        return self.get_next_value("ogtt_value")

    @property
    def next_visit_datetime(self) -> datetime | None:
        try:
            next_visit_datetime = self.subject_df.iloc[self.index + 1 : self.index + 2][
                "visit_datetime"
            ].item()
        except ValueError:
            next_visit_datetime = None
        return next_visit_datetime

    @property
    def interval_to_next_in_days(self):
        return (
            (self.next_visit_datetime - self.row.visit_datetime).days
            if self.next_visit_datetime
            else 0
        )

    def interval_to_previous_in_days(self):
        return (
            (self.next_visit_datetime - self.row.visit_datetime).days
            if self.next_visit_datetime
            else 0
        )

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

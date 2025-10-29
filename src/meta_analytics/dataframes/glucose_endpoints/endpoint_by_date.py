from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from clinicedc_constants import YES

from ..constants import endpoint_cases


class EndpointTdeltaError(Exception):
    pass


class InvalidCaseList(Exception):  # noqa: N818
    pass


@dataclass(kw_only=True)
class CaseData:
    df: pd.DataFrame
    index: int
    fbg_value: float | None = field(default=None, init=False)
    fbg_datetime: pd.Timestamp | None = field(default=None, init=False)
    fasted: str | None = field(default=None, init=False)
    ogtt_value: float | None = field(default=None, init=False)
    next_fbg_value: float | None = field(default=None, init=False)
    next_fbg_datetime: pd.Timestamp | None = field(default=None, init=False)
    next_fasted: str | None = field(default=None, init=False)
    next_ogtt_value: float | None = field(default=None, init=False)

    previous_fbg_value: float | None = field(default=None, init=False)
    previous_fbg_datetime: pd.Timestamp | None = field(default=None, init=False)
    previous_fasted: str | None = field(default=None, init=False)
    previous_ogtt_value: float | None = field(default=None, init=False)

    fbg_threshold: float = field(default=7.0, init=False)
    ogtt_threshold: float = field(default=11.1, init=False)

    def __post_init__(self):
        self.fbg_value = self.df.loc[self.index, "fbg_value"]
        self.fbg_datetime = self.df.loc[self.index, "fbg_datetime"]
        self.ogtt_value = self.df.loc[self.index, "ogtt_value"]
        self.fasted = self.df.loc[self.index, "fasted"]

        try:
            self.next_fbg_value = self.df.loc[self.index + 1, "fbg_value"]
        except KeyError:
            self.next_fbg_value = np.nan
            self.next_fbg_datetime = pd.NaT
            self.next_ogtt_value = np.nan
            self.next_fasted = np.nan
        else:
            self.next_fbg_datetime = self.df.loc[self.index + 1, "fbg_datetime"]
            self.next_ogtt_value = self.df.loc[self.index + 1, "ogtt_value"]
            self.next_fasted = self.df.loc[self.index + 1, "fasted"]

        try:
            self.previous_fbg_value = self.df.loc[self.index - 1, "fbg_value"]
        except KeyError:
            self.previous_fbg_value = np.nan
            self.previous_fbg_datetime = pd.NaT
            self.previous_ogtt_value = np.nan
            self.previous_fasted = np.nan
        else:
            self.previous_fbg_datetime = self.df.loc[self.index - 1, "fbg_datetime"]
            self.previous_ogtt_value = self.df.loc[self.index - 1, "ogtt_value"]
            self.previous_fasted = self.df.loc[self.index - 1, "fasted"]

    def case_two(self) -> bool:
        """FBG >= 7 x 2, first OGTT<=11.1"""
        return bool(
            pd.notna(self.next_fbg_datetime)
            and pd.notna(self.fbg_datetime)
            and self.fbg_value >= self.fbg_threshold
            and self.next_fbg_value >= self.fbg_threshold
            and 0.0 < self.ogtt_value < self.ogtt_threshold
            and self.fasted == YES
            and self.next_fasted == YES
            and (self.next_fbg_datetime.date() - self.fbg_datetime.date()).days > 6
        )

    def case_three(self) -> bool:
        """FBG >= 7 x 2, second OGTT<=11.1"""
        return bool(
            pd.notna(self.next_fbg_datetime)
            and pd.notna(self.fbg_datetime)
            and self.fbg_value >= self.fbg_threshold
            and self.next_fbg_value >= self.fbg_threshold
            and 0.0 < self.next_ogtt_value < self.ogtt_threshold
            and self.fasted == YES
            and self.next_fasted == YES
            and (self.next_fbg_datetime.date() - self.fbg_datetime.date()).days > 6
        )

    def case_two_reversed(self) -> bool:
        """Same as case 2, but with the previous FBG reading."""
        return bool(
            pd.notna(self.next_fbg_datetime)
            and pd.notna(self.fbg_datetime)
            and self.fbg_value >= self.fbg_threshold
            and self.previous_fbg_value >= self.fbg_threshold
            and 0.0 < self.previous_ogtt_value < self.ogtt_threshold
            and self.fasted == YES
            and self.previous_fasted == YES
            and (self.fbg_datetime.date() - self.previous_fbg_datetime.date()).days > 6
        )

    # def case_four(self) -> bool:
    #     """FBG >= 20.0"""
    #     return bool(
    #         pd.notna(self.next_fbg_datetime)
    #         and pd.notna(self.fbg_datetime)
    #         and self.fbg_value >= self.fbg_threshold
    #         and self.next_fbg_value >= self.fbg_threshold
    #         and 0.0 < self.next_ogtt_value < self.ogtt_threshold
    #         and self.fasted == YES
    #         and self.next_fasted == YES
    #         and (self.next_fbg_datetime.date() - self.fbg_datetime.date()).days > 6
    #     )


class EndpointByDate:
    """Given all timepoints for a subject, flag the first timepoint
    where the protocol endpoint is reached.

    IMPORTANT: Remove case one before passing to this class
        * case 1. any OGTT >= 11.1

    Evaluation is done in order

    Order of protocol endpoint evaluation:
      * case 2. FBG >= 7 x 2, first OGTT<11.1
      * case 3.  FBG >= 7 x 2, second OGTT<11.1

    If the endpoint is reached by FBG+OGTT, the date of endpoint is
    always the date of the second measurement.

    Additional criteria considered:
      1. any threshhold FBG must be taken while fasted (fasted=YES)
      2. threshhold FBG readings must be consecutive (no
         readings below threshold in the sequence regardless
         of fasting)
      3. at least 7 days between threshhold FBG readings.
      4. at least one of the two threshold FBG readings must be taken
         with an OGTT at the same timepoint.
    """

    def __init__(
        self,
        subject_df: pd.DataFrame = None,
        fbg_threshhold: float | None = None,
        ogtt_threshhold: float | None = None,
    ):
        self.row = None
        self.index = None
        self.subject_df = subject_df.sort_values(by=["visit_code"]).reset_index(drop=True)
        self.fbg_threshhold = fbg_threshhold
        self.ogtt_threshhold = ogtt_threshhold
        self.evaluate()

    def evaluate(self):
        for index, _ in self.subject_df.iterrows():
            case_data = CaseData(df=self.subject_df, index=index)
            if case_data.case_two():
                self.endpoint_reached(index, case=2, fbg_datetime=case_data.next_fbg_datetime)
                break
            if case_data.case_three():
                self.endpoint_reached(index, case=3, fbg_datetime=case_data.next_fbg_datetime)
                break
            if case_data.case_two_reversed():
                self.endpoint_reached(index, case=2, fbg_datetime=case_data.fbg_datetime)
                break
            pass

    def endpoint_reached(self, index: int, case: int, fbg_datetime: pd.Timestamp):  # noqa: ARG002
        """Update the subject_df"""
        self.subject_df.loc[self.subject_df["fbg_datetime"] == fbg_datetime, "endpoint"] = 1
        self.subject_df["interval_in_days"] = np.nan
        self.subject_df.loc[
            self.subject_df["fbg_datetime"] == fbg_datetime, "endpoint_type"
        ] = case
        self.subject_df.loc[
            self.subject_df["fbg_datetime"] == fbg_datetime, "endpoint_label"
        ] = endpoint_cases[case]

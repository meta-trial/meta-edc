import numpy as np
import pandas as pd

from ..constants import endpoint_cases
from .case_data import CaseData


class EndpointByDate:
    """Given all timepoints for a subject, flag the first timepoint
    where the protocol endpoint is reached.

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
        min_fasted_hrs: float | None = None,
    ):
        self.row = None
        self.index = None
        self.min_fasted_hrs = min_fasted_hrs
        self.subject_df = subject_df.sort_values(by=["visit_code"]).reset_index(drop=True)
        if not subject_df.empty:
            self.fbg_threshhold = fbg_threshhold
            self.ogtt_threshhold = ogtt_threshhold
            self.evaluate()

    def evaluate(self):
        for index, _ in self.subject_df.iterrows():
            case_data = CaseData(
                df=self.subject_df, index=index, min_fasted_hrs=self.min_fasted_hrs
            )
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
        self.subject_df["days_to_events"] = np.nan
        self.subject_df.loc[
            self.subject_df["fbg_datetime"] == fbg_datetime, "endpoint_type"
        ] = case
        self.subject_df.loc[
            self.subject_df["fbg_datetime"] == fbg_datetime, "endpoint_label"
        ] = endpoint_cases[case]

import numpy as np
import pandas as pd
from clinicedc_constants import YES
from dateutil.relativedelta import relativedelta


class CaseData:
    default_fbg_threshold = 7.0
    default_ogtt_threshold = 11.1
    confirmation_lower_bound = relativedelta(days=7)
    confirmation_upper_bound = relativedelta(months=99)

    def __init__(
        self,
        df: pd.DataFrame,
        index: int,
        min_fasted_hrs: float | None = None,
        fbg_threshold: float | None = None,
        ogtt_threshold: float | None = None,
    ):
        self.df = df
        self.index = index
        self.min_fasted_hrs = min_fasted_hrs

        self.fbg_threshold = fbg_threshold or self.default_fbg_threshold
        self.ogtt_threshold = ogtt_threshold or self.default_ogtt_threshold

        self.fbg_value = self.df.loc[self.index, "fbg_value"]
        self.fbg_datetime = self.df.loc[self.index, "fbg_datetime"]
        self.ogtt_value = self.df.loc[self.index, "ogtt_value"]
        self.fasted = self.df.loc[self.index, "fasted"]
        self.fasted_hrs = self.df.loc[self.index, "fasted_hrs"]

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
            self.next_fasted_hrs = self.df.loc[self.index + 1, "fasted_hrs"]

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
            self.previous_fasted_hrs = self.df.loc[self.index - 1, "fasted_hrs"]

    def case_two(self) -> bool:
        """FBG >= 7 x 2, first OGTT<=11.1"""
        return bool(
            pd.notna(self.next_fbg_datetime)
            and pd.notna(self.fbg_datetime)
            and self.fbg_value >= self.fbg_threshold
            and self.next_fbg_value >= self.fbg_threshold
            and 0.0 < self.ogtt_value < self.ogtt_threshold
            and self.fasted == YES
            and self.fasted_hrs >= self.min_fasted_hrs
            and self.next_fasted == YES
            and self.next_fasted_hrs >= self.min_fasted_hrs
            and self.fbg_datetime.date() + self.confirmation_lower_bound
            <= self.next_fbg_datetime.date()
            <= self.fbg_datetime.date() + self.confirmation_upper_bound
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
            and self.fasted_hrs >= self.min_fasted_hrs
            and self.next_fasted == YES
            and self.next_fasted_hrs >= self.min_fasted_hrs
            and self.fbg_datetime.date() + self.confirmation_lower_bound
            <= self.next_fbg_datetime.date()
            <= self.fbg_datetime.date() + self.confirmation_upper_bound
        )

    def case_two_reversed(self) -> bool:
        """Same as case 2, but with the previous FBG reading."""
        return bool(
            pd.notna(self.previous_fbg_datetime)
            and pd.notna(self.fbg_datetime)
            and self.fbg_value >= self.fbg_threshold
            and self.previous_fbg_value >= self.fbg_threshold
            and 0.0 < self.previous_ogtt_value < self.ogtt_threshold
            and self.fasted == YES
            and self.fasted_hrs >= self.min_fasted_hrs
            and self.previous_fasted == YES
            and self.previous_fasted_hrs >= self.min_fasted_hrs
            and self.previous_fbg_datetime.date() + self.confirmation_lower_bound
            <= self.fbg_datetime.date()
            <= self.previous_fbg_datetime.date() + self.confirmation_upper_bound
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

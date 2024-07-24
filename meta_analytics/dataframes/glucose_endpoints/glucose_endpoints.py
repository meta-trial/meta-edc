import numpy as np
import pandas as pd

from ...constants import EOS_DM_MET, FIRST_PRIMARY, OGTT_THRESHOLD_MET
from .endpoint_by_visit_code import EndpointByVisitCode
from .utils import get_test_string


class GlucoseEndpoints:

    fbg_threshhold = 7.0
    ogtt_threshhold = 11.1
    endpoint_columns = [
        "subject_identifier",
        "baseline_datetime",
        "visit_datetime",
        "interval_in_days",
        "visit_code",
        "fbg_value",
        "ogtt_value",
        "endpoint_label",
        "endpoint_type",
        "endpoint",
        "offstudy_datetime",
        "offstudy_reason",
    ]

    endpoint_cls = EndpointByVisitCode

    def __init__(
        self,
        df: pd.DataFrame | None = None,
        after_visit_code: float | None = None,
        endpoint_type: str | None = None,
    ):
        self._endpoint_df = pd.DataFrame()
        self._df_subject_identifier = pd.DataFrame()
        self.df = pd.DataFrame()
        self.working_df: pd.DataFrame = pd.DataFrame()
        self.endpoint_type = endpoint_type or FIRST_PRIMARY
        self.after_visit_code = after_visit_code
        self._visit_codes = pd.DataFrame()
        self.results = {}
        self.prepare_and_set_df(df)
        self.endpoint_df = self.get_empty_endpoint_df()
        self.run()

    def prepare_and_set_df(self, df: pd.DataFrame) -> None:
        # convert columns to dtype float
        df[["visit_code", "visit_code_sequence", "fbg_value", "ogtt_value"]] = df[
            ["visit_code", "visit_code_sequence", "fbg_value", "ogtt_value"]
        ].apply(pd.to_numeric)

        # label rows by type of glu tests (ones with value)
        df["test"] = df.apply(lambda x: get_test_string, axis=1)

        # only keep rows after the cutoff visit
        df = df[df["visit_code"] > self.after_visit_code]
        df = df.sort_values(by=["subject_identifier", "visit_code"])
        df = df.reset_index(drop=True)
        self.df = df.copy()

    def get_empty_endpoint_df(self) -> pd.DataFrame:
        endpoint_df = pd.DataFrame(columns=self.endpoint_columns)
        endpoint_df[
            [
                "visit_code",
                "interval_in_days",
                "fbg_value",
                "ogtt_value",
                "endpoint",
                "endpoint_type",
            ]
        ] = endpoint_df[
            [
                "visit_code",
                "interval_in_days",
                "fbg_value",
                "ogtt_value",
                "endpoint",
                "endpoint_type",
            ]
        ].apply(
            pd.to_numeric
        )
        endpoint_df[["baseline_datetime", "visit_datetime"]] = endpoint_df[
            ["baseline_datetime", "visit_datetime"]
        ].apply(pd.to_datetime)
        endpoint_df["visit_code"] = endpoint_df["visit_code"].astype(float)
        return endpoint_df

    def run(self):
        self.working_df = self.df.copy()
        self.working_df["endpoint"] = 0

        self.pre_check_endpoint()

        for index, row in self.subject_identifiers_df.iterrows():
            subject_df = self.get_subject_df(row["subject_identifier"])
            subject_df = self.check_for_endpoint(subject_df, case_list=[1, 2, 3, 4, 7])
            if len(subject_df.loc[subject_df["endpoint"] == 1]) == 1:
                self.append_subject_to_endpoint_df(subject_df)
                self.remove_subject_from_working_df(row)

        # go back and rerun for case 5
        for index, row in self.subject_identifiers_df.iterrows():
            subject_df = self.get_subject_df(row["subject_identifier"])
            subject_df = self.check_for_endpoint(subject_df, case_list=[5])
            if len(subject_df.loc[subject_df["endpoint"] == 1]) == 1:
                self.append_subject_to_endpoint_df(subject_df)
                self.remove_subject_from_working_df(row)

        self.post_check_endpoint()
        # merge endpoint_df with original df
        self.endpoint_df["test"] = self.endpoint_df.apply(get_test_string, axis=1)
        endpoints_only_df = self.endpoint_df[self.endpoint_df["endpoint"].notna()][
            ["subject_identifier", "visit_code", "endpoint"]
        ]
        endpoints_only_df.reset_index(drop=True, inplace=True)
        self.df = pd.merge(
            self.df,
            endpoints_only_df,
            on=["subject_identifier", "visit_code"],
            how="left",
            suffixes=("", "_y"),
        )
        self.df["dup"] = self.df.duplicated(
            subset=["subject_identifier", "visit_code", "visit_code_sequence"], keep=False
        )
        self.df.sort_values(by=["subject_identifier", "visit_code"])
        self.df.reset_index(drop=True, inplace=True)

    def append_subject_to_endpoint_df(self, subject_df: pd.DataFrame) -> None:
        # add subject to endpoint_df
        if self.endpoint_df.empty:
            self.endpoint_df = subject_df.copy()
        elif subject_df.empty:
            pass
        else:
            self.endpoint_df = pd.concat([self.endpoint_df, subject_df])
            self.endpoint_df = self.endpoint_df.sort_values(
                by=["subject_identifier", "visit_code"]
            )
            self.endpoint_df.reset_index(drop=True, inplace=True)

    def remove_subject_from_working_df(self, row: pd.Series) -> None:
        self.working_df = self.working_df.drop(
            index=self.working_df[
                self.working_df["subject_identifier"] == row["subject_identifier"]
            ].index
        )
        self.working_df.reset_index(drop=True, inplace=True)

    def pre_check_endpoint(self):
        if self.endpoint_type == FIRST_PRIMARY:
            # select subjects with ogtt>=threshold
            df_ogtt_threshold = self.working_df.loc[self.subjects_by_ogtt_only].copy()
            df_ogtt_threshold["endpoint"] = 1
            df_ogtt_threshold["endpoint_label"] = OGTT_THRESHOLD_MET
            df_ogtt_threshold["endpoint_type"] = 6
            df_ogtt_threshold["interval_in_days"] = np.nan
            df_ogtt_threshold.reset_index(drop=True, inplace=True)
            self.append_subject_to_endpoint_df(df_ogtt_threshold[self.endpoint_columns])
            self.working_df = self.working_df.drop(
                index=self.working_df.loc[
                    self.working_df["subject_identifier"].isin(
                        df_ogtt_threshold["subject_identifier"]
                    )
                ].index
            )
        elif self.endpoint_type == "original":
            pass

    def check_for_endpoint(
        self, subject_df: pd.DataFrame, case_list: list[int] | None = None
    ) -> pd.DataFrame:
        """Assumes any subjects with ogtt >= 11.1 have already been removed
        from working_df (see pre_check_endpoint).
        """
        if self.endpoint_type == FIRST_PRIMARY:
            subject_df = self.check_endpoint_by_fbg_for_subject(
                subject_df, case_list=case_list
            )
        return subject_df

    def post_check_endpoint(self):
        if self.endpoint_type == FIRST_PRIMARY:
            df_eos = self.working_df.loc[self.subjects_off_study_with_dm].copy()
            df_eos["endpoint"] = 1
            df_eos["endpoint_label"] = EOS_DM_MET
            df_eos["endpoint_type"] = 7
            df_eos["interval_in_days"] = np.nan
            df_eos.reset_index(drop=True, inplace=True)
            self.append_subject_to_endpoint_df(df_eos[self.endpoint_columns])
            self.working_df = self.working_df.drop(
                index=self.working_df.loc[
                    self.working_df["subject_identifier"].isin(df_eos["subject_identifier"])
                ].index
            )

    def check_endpoint_by_fbg_for_subject(
        self, subject_df: pd.DataFrame, case_list: list[int] | None = None
    ) -> pd.DataFrame:
        case_list = case_list or [1, 2, 3, 4]
        for index, row in subject_df.iterrows():
            endpoint = self.endpoint_cls(
                index=index,
                row=row,
                subject_df=subject_df,
                visit_codes=self.visit_codes,
                fbg_threshhold=self.fbg_threshhold,
                ogtt_threshhold=self.ogtt_threshhold,
            )
            if 1 in case_list and endpoint.case_one():
                subject_df = endpoint.subject_df
                break
            elif 2 in case_list and endpoint.case_two():
                subject_df = endpoint.subject_df
                break
            elif 3 in case_list and endpoint.case_three():
                subject_df = endpoint.subject_df
                break
            elif 4 in case_list and endpoint.case_four():
                subject_df = endpoint.subject_df
                break
            elif 5 in case_list and endpoint.case_five():
                subject_df = endpoint.subject_df
                break
        return subject_df

    @property
    def visit_codes(self) -> pd.DataFrame:
        if self._visit_codes.empty:
            self._visit_codes = (
                self.df[self.df["visit_code"] % 1 == 0]["visit_code"].value_counts().to_frame()
            )
            self._visit_codes = self._visit_codes.reset_index()
            self._visit_codes["visit_code"] = self._visit_codes["visit_code"].astype(float)
            self._visit_codes = self._visit_codes.sort_values(["visit_code"])
            self._visit_codes = self._visit_codes[
                self._visit_codes["visit_code"] > self.after_visit_code
            ]
            self._visit_codes = self._visit_codes.reset_index(drop=True)
        return self._visit_codes

    def get_subject_df(self, subject_identifier: str) -> pd.DataFrame:
        subject_df = self.working_df.loc[
            self.working_df["subject_identifier"] == subject_identifier
        ].copy()
        subject_df["interval_in_days"] = np.nan
        subject_df["endpoint_type"] = None
        subject_df["endpoint_label"] = None
        subject_df["endpoint"] = 0
        subject_df = subject_df.sort_values(["subject_identifier", "visit_code"])
        subject_df = subject_df[self.endpoint_columns]
        subject_df = subject_df.merge(
            self.visit_codes,
            on="visit_code",
            how="outer",
            indicator=False,
            suffixes=["", "_y"],
        )
        subject_df["subject_identifier"] = subject_identifier
        subject_df.drop(columns=["count"], inplace=True)
        subject_df.reset_index(drop=True, inplace=True)
        return subject_df

    @property
    def subject_identifiers_df(self):
        if self._df_subject_identifier.empty:
            self._df_subject_identifier = pd.DataFrame(
                self.df["subject_identifier"].unique(), columns=["subject_identifier"]
            )
            self._df_subject_identifier = self._df_subject_identifier.sort_values(
                ["subject_identifier"]
            )
            self._df_subject_identifier = self._df_subject_identifier.reset_index()
        return self._df_subject_identifier

    def subjects_by_ogtt_only(self, df):
        """Condition for subjects with any non-null fbg and an ogtt
        that meets the threshold.
        """
        return (df["ogtt_value"] >= self.ogtt_threshhold) & (df["fbg_value"].notna())

    @staticmethod
    def subjects_off_study_with_dm(df):
        return df["offstudy_reason"] == "Patient developed diabetes"

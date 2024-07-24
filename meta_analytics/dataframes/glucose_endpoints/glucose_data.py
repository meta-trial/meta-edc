import numpy as np
import pandas as pd

from ...constants import EOS_DM_MET, OGTT_THRESHOLD_MET
from ..enrolled import get_crf, get_eos, get_subject_consent, get_subject_visit
from .constants import endpoint_columns
from .endpoint_by_date import EndpointByDate
from .utils import (
    get_empty_endpoint_df,
    get_test_string,
    get_unique_subject_identifiers,
    get_unique_visit_codes,
)


class GlucoseData:
    """

    These have difference fbg dates on same report date:
     grp = cls.df.groupby(by=["subject_visit_id", "fbg_datetime"], as_index=False).size()
     grp[grp["size"]>1]

    """

    fbg_threshhold = 7.0
    ogtt_threshhold = 11.1
    endpoint_cls = EndpointByDate

    def __init__(self):
        self.fbg_only_df = get_crf(model="meta_subject.glucosefbg")
        self.fbg_only_df["source"] = "meta_subject.glucosefbg"
        self.fbg_only_df.rename(
            columns={"fbg_fasting": "fasting", "subject_visit": "subject_visit_id"},
            inplace=True,
        )
        self.fbg_only_df.loc[(self.fbg_only_df["fasting"] == "fasting"), "fasting"] = "Yes"
        self.fbg_only_df.loc[(self.fbg_only_df["fasting"] == "non_fasting"), "fasting"] = "No"

        self.df = get_crf(model="meta_subject.glucose")
        self.df["source"] = "meta_subject.glucose"

        for dftmp in [self.fbg_only_df, self.df]:
            dftmp["fasting_hrs"] = np.nan
            dftmp["fasting_hrs"] = dftmp["fasting_duration_delta"].apply(
                lambda x: x.total_seconds() / 3600
            )
            dftmp["fasting_hrs"] = dftmp["fasting_hrs"].apply(lambda x: 8.05 if not x else x)

        keep_cols = [
            "subject_visit_id",
            "fasting",
            "fasting_hrs",
            "fbg_value",
            "fbg_units",
            "fbg_datetime",
            "ogtt_value",
            "ogtt_units",
            "ogtt_datetime",
            "source",
            "report_datetime",
        ]
        self.fbg_only_df = self.fbg_only_df[
            [col for col in keep_cols if not col.startswith("ogtt")]
        ]
        self.df = self.df[keep_cols]

        # normalize dates
        for col in ["fbg_datetime", "report_datetime"]:
            self.fbg_only_df[col] = self.fbg_only_df[col].dt.floor("d")
            self.df[col] = self.df[col].dt.floor("d")
        self.df["ogtt_datetime"] = self.df["ogtt_datetime"].dt.floor("d")

        # same shape but fbg_only_df ogtt columns are null
        self.df = pd.merge(
            self.df,
            self.fbg_only_df,
            on=["subject_visit_id", "fbg_datetime", "fbg_value"],
            how="outer",
            indicator=True,
            suffixes=("", "2"),
        )
        self.df.reset_index(drop=True, inplace=True)

        # right_only
        cols = [
            "fasting",
            "fasting_hrs",
            "fbg_units",
            "source",
            "report_datetime",
        ]
        cols2 = [f"{col}2" for col in cols]
        self.df[cols] = self.df.loc[self.df["_merge"] == "right_only", cols2]

        cols = [col for col in self.df.columns if col.endswith("2")]
        self.df.drop(columns=cols)

        df_subject_visit = get_subject_visit()
        self.df = pd.merge(df_subject_visit, self.df, on="subject_visit_id", how="left")
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df.reset_index(drop=True, inplace=True)

        df_consent = get_subject_consent()
        self.df = pd.merge(self.df, df_consent, on="subject_identifier", how="left")
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df.reset_index(drop=True, inplace=True)

        df_eos = get_eos()
        self.df = pd.merge(self.df, df_eos, on="subject_identifier", how="left")
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df.reset_index(drop=True, inplace=True)

        self.df["visit_days"] = (
            self.df["baseline_datetime"].rsub(self.df["visit_datetime"]).dt.days
        )
        self.df["fgb_days"] = (
            self.df["baseline_datetime"].rsub(self.df["fbg_datetime"]).dt.days
        )
        self.df["ogtt_days"] = (
            self.df["baseline_datetime"].rsub(self.df["ogtt_datetime"]).dt.days
        )
        self.df["visit_days"] = pd.to_numeric(self.df["visit_days"], downcast="integer")
        self.df["fgb_days"] = pd.to_numeric(self.df["fgb_days"], downcast="integer")
        self.df["ogtt_days"] = pd.to_numeric(self.df["ogtt_days"], downcast="integer")

        # label rows by type of glu tests (ones with value)
        self.df["test"] = self.df.apply(lambda x: get_test_string, axis=1)

        df = self.df.sort_values(by=["subject_identifier", "visit_code"])
        df = df.reset_index(drop=True)
        self.df = df.copy()
        self.pre_filter_df()
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df.reset_index(drop=True, inplace=True)
        self.visit_codes = get_unique_visit_codes(self.df)
        self.subject_identifiers_df = get_unique_subject_identifiers(self.df)
        self.working_df = self.df.copy()
        self.working_df["endpoint"] = 0
        self.endpoint_df = get_empty_endpoint_df()

    def run(self):
        self.pre_check_endpoint()
        for index, row in self.subject_identifiers_df.iterrows():
            subject_df = self.get_subject_df(row["subject_identifier"])
            subject_df = self.check_endpoint_by_fbg_for_subject(subject_df, case_list=[1, 2])
            if len(subject_df.loc[subject_df["endpoint"] == 1]) == 1:
                self.append_subject_to_endpoint_df(subject_df)
                self.remove_subject_from_working_df(row)

        # go back and rerun for case 5
        for index, row in self.subject_identifiers_df.iterrows():
            subject_df = self.get_subject_df(row["subject_identifier"])
            subject_df = self.check_endpoint_by_fbg_for_subject(subject_df, case_list=[5])
            if len(subject_df.loc[subject_df["endpoint"] == 1]) == 1:
                self.append_subject_to_endpoint_df(subject_df)
                self.remove_subject_from_working_df(row)

        self.post_check_endpoint()
        self.merge_with_final_endpoints()

    def pre_filter_df(self):
        offstudy_reason = (
            "Patient fulfilled late exclusion criteria (due to abnormal blood "
            "values or raised blood pressure at enrolment"
        )
        self.df = self.df[self.df["offstudy_reason"] != offstudy_reason]

    def pre_check_endpoint(self):
        # select subjects with ogtt>=threshold
        subjects_df = self.working_df.loc[self.subjects_by_ogtt_only].copy()
        subjects_df["endpoint"] = 1
        subjects_df["endpoint_label"] = OGTT_THRESHOLD_MET
        subjects_df["endpoint_type"] = 6
        subjects_df["interval_in_days"] = np.nan
        subjects_df.reset_index(drop=True, inplace=True)
        self.append_subject_to_endpoint_df(subjects_df[endpoint_columns])
        self.working_df = self.working_df.drop(
            index=self.working_df.loc[
                self.working_df["subject_identifier"].isin(subjects_df["subject_identifier"])
            ].index
        )

    def subjects_by_ogtt_only(self, df):
        """Condition for subjects with any non-null fbg and an ogtt
        that meets the threshold.
        """
        return (df["ogtt_value"] >= self.ogtt_threshhold) & (df["fbg_value"].notna())

    def append_subject_to_endpoint_df(self, subject_df: pd.DataFrame) -> None:
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

    def get_subject_df(self, subject_identifier: str) -> pd.DataFrame:
        subject_df = self.working_df.loc[
            self.working_df["subject_identifier"] == subject_identifier
        ].copy()
        subject_df["interval_in_days"] = np.nan
        subject_df["endpoint_type"] = None
        subject_df["endpoint_label"] = None
        subject_df["endpoint"] = 0
        subject_df = subject_df.sort_values(["subject_identifier", "visit_code"])
        subject_df = subject_df[endpoint_columns]
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

    def post_check_endpoint(self):
        df_eos = self.working_df.loc[
            self.working_df["offstudy_reason"] == "Patient developed diabetes"
        ].copy()
        df_eos["endpoint"] = 1
        df_eos["endpoint_label"] = EOS_DM_MET
        df_eos["endpoint_type"] = 7
        df_eos["interval_in_days"] = np.nan
        df_eos.reset_index(drop=True, inplace=True)
        self.append_subject_to_endpoint_df(df_eos[endpoint_columns])
        self.working_df = self.working_df.drop(
            index=self.working_df.loc[
                self.working_df["subject_identifier"].isin(df_eos["subject_identifier"])
            ].index
        )

    def merge_with_final_endpoints(self):
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
        # self.df["dup"] = self.df.duplicated(
        #     subset=["subject_identifier", "visit_code", "visit_code_sequence"], keep=False
        # )
        self.df.sort_values(by=["subject_identifier", "visit_code", "fbg_datetime"])
        self.df.reset_index(drop=True, inplace=True)

import numpy as np
import pandas as pd
from django.apps import apps as django_apps
from edc_constants.constants import NO, YES
from edc_pdutils.dataframes import (
    get_crf,
    get_eos,
    get_subject_consent,
    get_subject_visit,
)

from ...constants import EOS_DM_MET, OGTT_THRESHOLD_MET
from .constants import endpoint_columns
from .endpoint_by_date import EndpointByDate
from .utils import (
    get_empty_endpoint_df,
    get_test_string,
    get_unique_subject_identifiers,
    get_unique_visit_codes,
)


class GlucoseEndpointsByDate:

    fbg_threshhold = 7.0
    ogtt_threshhold = 11.1
    endpoint_cls = EndpointByDate

    def __init__(self, include_fbg_only: bool | None = None):
        self.include_fbg_only = include_fbg_only
        self.endpoint_only_df = None
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

        self.df_merged = self.df.copy()

        # right_only
        cols = [
            "fasting",
            "fasting_hrs",
            "fbg_units",
            "source",
            "report_datetime",
        ]
        for col in cols:
            self.df.loc[self.df["_merge"] == "right_only", col] = self.df[f"{col}2"]

        # cols = [col for col in self.df.columns if col.endswith("2")]
        # self.df.drop(columns=cols)

        df_subject_visit = get_subject_visit("meta_subject.subjectvisit")
        visit_cols = [
            "subject_visit_id",
            "subject_identifier",
            "visit_code",
            "visit_datetime",
            "site",
            "baseline_datetime",
        ]
        self.df = pd.merge(
            df_subject_visit[visit_cols], self.df, on="subject_visit_id", how="left"
        )
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df.reset_index(drop=True, inplace=True)

        df_consent = get_subject_consent("meta_consent.subjectconsent")
        self.df = pd.merge(self.df, df_consent, on="subject_identifier", how="left")
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df.reset_index(drop=True, inplace=True)

        df_eos = get_eos("meta_prn.endofstudy")
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
        self.df["test"] = self.df.apply(get_test_string, axis=1)

        self.df = self.df.sort_values(by=["subject_identifier", "visit_code"])
        self.df = self.df.reset_index(drop=True)
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

        if self.include_fbg_only:
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
        subject_df = subject_df.sort_values(["subject_identifier", "fbg_datetime"])
        subject_df = subject_df[endpoint_columns]
        subject_df = subject_df.merge(
            self.visit_codes,
            on="visit_code",
            how="outer",
            indicator=False,
            suffixes=["", "2"],
        )
        subject_df["subject_identifier"] = subject_identifier
        subject_df.drop(columns=["count"], inplace=True)
        subject_df.reset_index(drop=True, inplace=True)
        return subject_df

    def check_endpoint_by_fbg_for_subject(
        self, subject_df: pd.DataFrame, case_list: list[int] | None = None
    ) -> pd.DataFrame:
        case_list = case_list or [1, 2, 3, 4]
        endpoint = self.endpoint_cls(
            subject_df=subject_df,
            fbg_threshhold=self.fbg_threshhold,
            ogtt_threshhold=self.ogtt_threshhold,
            case_list=case_list,
        )
        return endpoint.subject_df

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
        self.endpoint_df.loc[self.endpoint_df["endpoint"] == 1, "days_to_endpoint"] = (
            self.endpoint_df["fbg_datetime"] - self.endpoint_df["baseline_datetime"]
        ).dt.days

        print(f"Before dedup = {len(self.endpoint_df)}")
        df = self.endpoint_df.copy()
        df1 = df[(df["endpoint_type"] == 7) & (df["endpoint"] == 1)]
        df1 = (
            df1.sort_values(["subject_identifier", "fbg_datetime"])
            .reset_index(drop=True)
            .set_index(["subject_identifier"])
        )
        df1 = df1[~df1.index.duplicated(keep="last")]
        df1.reset_index(drop=False, inplace=True)

        df2 = df[(df["endpoint_type"] != 7) & (df["endpoint"] == 1)]
        df2 = (
            df2.sort_values(["subject_identifier", "fbg_datetime"])
            .reset_index(drop=True)
            .set_index(["subject_identifier"])
        )
        df2 = df2[~df2.index.duplicated(keep="first")]
        df2.reset_index(drop=False, inplace=True)
        self.endpoint_only_df = pd.concat([df1, df2])
        self.endpoint_only_df.reset_index(drop=True, inplace=True)
        print(f"After dedup = {len(self.endpoint_df)}")

        self.df = pd.merge(
            self.df,
            self.endpoint_only_df[["subject_identifier", "visit_code", "endpoint"]],
            on=["subject_identifier", "visit_code"],
            how="left",
            suffixes=("", "_y"),
        )
        self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df.reset_index(drop=True, inplace=True)

    def summarize(
        self,
        fasting: str | list | None = None,
        interval_in_days_min: int | None = None,
    ):
        days_min = interval_in_days_min or 7

        fasting = fasting or [YES, NO, pd.NA]
        fasting = fasting if type(fasting) in [list, tuple] else [fasting]

        endpoint_df = self.endpoint_df.copy()

        # endpoint by eos with dm subjects
        df7 = endpoint_df[(endpoint_df["endpoint_type"] == 7) & (endpoint_df["endpoint"] == 1)]
        df7.reset_index(drop=True, inplace=True)
        # endpoint by glucose subjects
        df = endpoint_df[
            (endpoint_df["endpoint_type"] != 7)
            & (endpoint_df["endpoint"] == 1)
            & (endpoint_df["fasting"].isin(fasting))
            & (
                (endpoint_df["interval_in_days"] >= days_min)
                | (endpoint_df["interval_in_days"].isna())
            )
        ]
        df.reset_index(drop=True, inplace=True)
        df = pd.concat([df, df7])
        df.reset_index(drop=True, inplace=True)
        df_counts = df[["endpoint_type", "endpoint_label"]].value_counts().to_frame()
        df_counts.sort_values(by=["endpoint_type"], inplace=True)
        df_counts.reset_index(inplace=True)

        sums = {
            "endpoint_type": [np.nan, np.nan, np.nan],
            "endpoint_label": ["Total 1,2,6", "Total 1,2,6,7", "Total"],
            "count": [
                df_counts[df_counts["endpoint_type"].isin([1, 2, 6])]["count"].sum(),
                df_counts[df_counts["endpoint_type"].isin([1, 2, 6, 7])]["count"].sum(),
                df_counts["count"].sum(),
            ],
        }
        sums_df = pd.DataFrame.from_dict(sums)
        df_counts = pd.concat([df_counts, sums_df], ignore_index=True)
        return df_counts

    def to_model(self, model: str | None = None):
        df = self.endpoint_only_df
        model_cls = django_apps.get_model(model or "meta_reports.endpoints")
        model_cls.objects.all().delete()
        model_cls.objects.bulk_create(
            [
                model_cls(
                    subject_identifier=row["subject_identifier"],
                    site_id=row["site"],
                    baseline_datetime=(
                        None if pd.isna(row["baseline_datetime"]) else row["baseline_datetime"]
                    ),
                    visit_code=None if pd.isna(row["visit_code"]) else row["visit_code"],
                    fbg_value=(None if pd.isna(row["fbg_value"]) else row["fbg_value"]),
                    ogtt_value=None if pd.isna(row["ogtt_value"]) else row["ogtt_value"],
                    fbg_datetime=(
                        None if pd.isna(row["fbg_datetime"]) else row["fbg_datetime"]
                    ),
                    fasting=(None if pd.isna(row["fasting"]) else row["fasting"]),
                    endpoint_label=(
                        None if pd.isna(row["endpoint_label"]) else row["endpoint_label"]
                    ),
                    offstudy_datetime=(
                        None if pd.isna(row["offstudy_datetime"]) else row["offstudy_datetime"]
                    ),
                    offstudy_reason=(
                        None if pd.isna(row["offstudy_reason"]) else row["offstudy_reason"]
                    ),
                    report_model=row["report_model"],
                )
                for _, row in df.iterrows()
            ]
        )

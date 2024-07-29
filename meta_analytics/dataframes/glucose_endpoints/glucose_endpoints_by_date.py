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
from edc_utils import get_utcnow

from .constants import (
    CASE_EOS,
    CASE_FBG_ONLY,
    CASE_OGTT,
    endpoint_cases,
    endpoint_columns,
)
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

    def __init__(self, case_list: list[int] | None = None):
        self.case_list = case_list or [CASE_OGTT, 2, 3, CASE_EOS]
        self.endpoint_cases = {k: v for k, v in endpoint_cases.items() if k in self.case_list}
        self.endpoint_only_df = None
        self.fbg_only_df = get_crf(model="meta_subject.glucosefbg")
        self.fbg_only_df["source"] = "meta_subject.glucosefbg"
        self.fbg_only_df.rename(
            columns={"fbg_fasting": "fasting", "subject_visit": "subject_visit_id"},
            inplace=True,
        )
        self.fbg_only_df.loc[(self.fbg_only_df["fasting"] == "fasting"), "fasting"] = YES
        self.fbg_only_df.loc[(self.fbg_only_df["fasting"] == "non_fasting"), "fasting"] = NO

        self.df = get_crf(model="meta_subject.glucose")
        self.df["source"] = "meta_subject.glucose"

        for dftmp in [self.fbg_only_df, self.df]:
            dftmp.loc[(dftmp["fasting"] == NO), "fasting_duration_delta"] = np.nan
            dftmp["fasting_hrs"] = dftmp["fasting_duration_delta"].dt.total_seconds() / 3600

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
        self.df.reset_index(drop=True)
        self.df = self.df.copy()

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

        self.df = self.df[
            self.df["offstudy_reason"]
            != (
                "Patient fulfilled late exclusion criteria (due to abnormal blood "
                "values or raised blood pressure at enrolment"
            )
        ]

        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df = self.df.reset_index(drop=True)
        self.visit_codes = get_unique_visit_codes(self.df)
        self.subject_identifiers_df = get_unique_subject_identifiers(self.df)
        self.working_df = self.df.copy()
        self.working_df["endpoint"] = 0
        self.endpoint_df = get_empty_endpoint_df()

    def run(self):
        self.pre_check_endpoint()
        for index, row in self.subject_identifiers_df.iterrows():
            subject_df = self.get_subject_df(row["subject_identifier"])
            subject_df = self.check_endpoint_by_fbg_for_subject(subject_df, case_list=[2, 3])
            if len(subject_df.loc[subject_df["endpoint"] == 1]) == 1:
                self.append_subject_to_endpoint_df(subject_df)
                self.remove_subject_from_working_df(row)

        if CASE_FBG_ONLY in self.endpoint_cases:
            # go back and rerun for case 5
            for index, row in self.subject_identifiers_df.iterrows():
                subject_df = self.get_subject_df(row["subject_identifier"])
                subject_df = self.check_endpoint_by_fbg_for_subject(subject_df, case_list=[4])
                if len(subject_df.loc[subject_df["endpoint"] == 1]) == 1:
                    self.append_subject_to_endpoint_df(subject_df)
                    self.remove_subject_from_working_df(row)

        self.post_check_endpoint()
        self.merge_with_final_endpoints()

    def pre_check_endpoint(self):
        "Case 1: flag and remove all OGTT that met threshold"
        subjects_df = self.working_df.loc[
            (self.working_df["ogtt_value"] >= self.ogtt_threshhold)
            & (self.working_df["fbg_value"].notna())
        ].copy()
        subjects_df["endpoint"] = 1
        subjects_df["endpoint_label"] = self.endpoint_cases[CASE_OGTT]
        subjects_df["endpoint_type"] = CASE_OGTT
        subjects_df["interval_in_days"] = np.nan
        subjects_df = subjects_df.reset_index(drop=True)
        self.append_subject_to_endpoint_df(subjects_df[endpoint_columns])
        self.working_df = self.working_df.drop(
            index=self.working_df.loc[
                self.working_df["subject_identifier"].isin(subjects_df["subject_identifier"])
            ].index
        )

    def append_subject_to_endpoint_df(self, subject_df: pd.DataFrame) -> None:
        if self.endpoint_df.empty:
            self.endpoint_df = subject_df.copy()
        else:
            self.endpoint_df = pd.concat([self.endpoint_df, subject_df])
            self.endpoint_df = self.endpoint_df.sort_values(
                by=["subject_identifier", "visit_code"]
            )
            self.endpoint_df = self.endpoint_df.reset_index(drop=True)

    def remove_subject_from_working_df(self, row: pd.Series) -> None:
        self.working_df = self.working_df.drop(
            index=self.working_df[
                self.working_df["subject_identifier"] == row["subject_identifier"]
            ].index
        )
        self.working_df = self.working_df.reset_index(drop=True)

    def get_subject_df(self, subject_identifier: str) -> pd.DataFrame:
        subject_df = self.working_df.loc[
            self.working_df["subject_identifier"] == subject_identifier
        ].copy()
        subject_df["interval_in_days"] = np.nan
        subject_df["endpoint_type"] = None
        subject_df["endpoint_label"] = None
        subject_df["endpoint"] = 0
        subject_df = subject_df.sort_values(["subject_identifier", "fbg_datetime"])
        subject_df = subject_df.reset_index(drop=True)
        subject_df = subject_df[endpoint_columns]
        subject_df = subject_df.merge(
            self.visit_codes,
            on="visit_code",
            how="outer",
            indicator=False,
            suffixes=["", "2"],
        )
        subject_df["subject_identifier"] = subject_identifier
        subject_df = subject_df.drop(columns=["count"])
        subject_df = subject_df.reset_index(drop=True)
        return subject_df

    def check_endpoint_by_fbg_for_subject(
        self, subject_df: pd.DataFrame, case_list: list[int] | None = None
    ) -> pd.DataFrame:
        case_list = case_list or [2, 3]
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
        df_eos["endpoint_label"] = self.endpoint_cases[CASE_EOS]
        df_eos["endpoint_type"] = CASE_EOS
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

        df1 = self.endpoint_df.copy()
        df1 = df1[(df1["endpoint_type"] == CASE_EOS) & (df1["endpoint"] == 1)]
        df1 = df1.sort_values(["subject_identifier", "fbg_datetime"])
        df1 = df1.reset_index(drop=True)
        df1 = df1.set_index(["subject_identifier"])
        df1 = df1[~df1.index.duplicated(keep="last")]
        df1 = df1.reset_index(drop=False)

        df2 = self.endpoint_df.copy()
        df2 = df2[(df2["endpoint_type"] != CASE_EOS) & (df2["endpoint"] == 1)]
        df2 = df2.sort_values(["subject_identifier", "fbg_datetime"])
        df2 = df2.reset_index(drop=True)
        df2 = df2.set_index(["subject_identifier"])
        df2 = df2[~df2.index.duplicated(keep="first")]
        df2 = df2.reset_index(drop=False)

        self.endpoint_only_df = pd.concat([df1, df2])
        self.endpoint_only_df = self.endpoint_only_df.reset_index(drop=True)
        print(f"After dedup = {len(self.endpoint_df)}")

        self.df = pd.merge(
            self.df,
            self.endpoint_only_df[["subject_identifier", "visit_code", "endpoint"]],
            on=["subject_identifier", "visit_code"],
            how="left",
            suffixes=("", "_y"),
        )
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df = self.df.reset_index(drop=True)

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
        df7 = endpoint_df[
            (endpoint_df["endpoint_type"] == CASE_EOS) & (endpoint_df["endpoint"] == 1)
        ]
        df7.reset_index(drop=True, inplace=True)
        # endpoint by glucose subjects
        df = endpoint_df[
            (endpoint_df["endpoint_type"] != CASE_EOS)
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
            "endpoint_type": [np.nan],
            "endpoint_label": ["Total"],
            "count": [
                df_counts["count"].sum(),
            ],
        }
        sums_df = pd.DataFrame.from_dict(sums)
        df_counts = pd.concat([df_counts, sums_df], ignore_index=True)
        return df_counts

    def to_model(self, model: str | None = None):
        df = self.endpoint_only_df
        model = model or "meta_reports.endpoints"
        now = get_utcnow()
        model_cls = django_apps.get_model(model)
        model_cls.objects.all().delete()
        data = [
            model_cls(
                subject_identifier=row["subject_identifier"],
                site_id=row["site"],
                baseline_datetime=(
                    None if pd.isna(row["baseline_datetime"]) else row["baseline_datetime"]
                ),
                visit_code=None if pd.isna(row["visit_code"]) else row["visit_code"],
                fbg_value=(None if pd.isna(row["fbg_value"]) else row["fbg_value"]),
                ogtt_value=None if pd.isna(row["ogtt_value"]) else row["ogtt_value"],
                fbg_datetime=(None if pd.isna(row["fbg_datetime"]) else row["fbg_datetime"]),
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
                report_model=model,
                created=now,
            )
            for _, row in df.iterrows()
        ]
        model_cls.objects.bulk_create(data)

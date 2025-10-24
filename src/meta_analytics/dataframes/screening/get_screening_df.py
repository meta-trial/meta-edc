import numpy as np
import pandas as pd
from django_pandas.io import read_frame

from meta_screening.models import SubjectScreening
from meta_subject.models import PhysicalExam, SubjectVisit


def get_screening_df(df: pd.DataFrame | None = None) -> pd.DataFrame:
    df = pd.DataFrame() if not hasattr(df, "empty") else df
    if df.empty:
        cols = [
            f.name
            for f in SubjectScreening._meta.get_fields()
            if f.name
            not in [
                "contact_number",
                "initials",
                "hospital_identifier",
                "modified",
                "user_created",
                "user_modified",
                "hostname_created",
                "hostname_modified",
                "device_created",
                "device_modified",
                "locale_created",
                "locale_modified",
                "slug",
            ]
        ]
        qs_screening = SubjectScreening.objects.values(*cols).all()
        df = read_frame(qs_screening, verbose=False)
        df = df.drop(df[df["hiv_pos"] == "No"].index)  # removes 2 rows
        df = df.reset_index(drop=True)

    # convert all to float
    num_cols = [
        "age_in_years",
        "calculated_bmi_value",
        "converted_fbg2_value",
        "converted_fbg_value",
        "converted_ogtt2_value",
        "converted_ogtt_value",
        "dia_blood_pressure_avg",
        "fbg2_value",
        "fbg_value",
        "hba1c_value",
        "ogtt2_value",
        "ogtt_value",
        "sys_blood_pressure_avg",
        "waist_circumference",
    ]
    df[num_cols] = df[num_cols].apply(pd.to_numeric)

    df["reasons_ineligible_part_one"] = df["reasons_ineligible_part_one"].apply(
        lambda x: None if x == "" else x
    )
    df["reasons_ineligible_part_two"] = df["reasons_ineligible_part_two"].apply(
        lambda x: None if x == "" else x
    )
    df["reasons_ineligible_part_two"] = df["reasons_ineligible_part_two"].str.replace(
        "Has Dm", "Diabetes"
    )
    df["reasons_ineligible_part_two"] = df["reasons_ineligible_part_two"].str.replace(
        "On Dm Medication", "taking anti-diabetic medications"
    )
    df["reasons_ineligible_part_three"] = df["reasons_ineligible_part_three"].apply(
        lambda x: None if x == "" else x
    )

    # condition to include any glucose test

    # has_dm fillna with unk
    df["has_dm"] = df["has_dm"].apply(lambda x: x if x else "unk")

    na = "Not applicable, subject is not eligible based on the criteria above"
    df["already_fasted"] = df["already_fasted"].apply(lambda x: "N/A" if x == na else x)

    # create a column that summarizes lives_nearby and staying_nearby_12
    df["in_catchment"] = (df["lives_nearby"] == "Yes") & (df["staying_nearby_12"] == "Yes")

    # create ogtt column
    df["ogtt"] = df["converted_ogtt_value"]
    df.loc[df["ogtt"].notna() & df["converted_ogtt2_value"].notna(), "ogtt"] = df[
        "converted_ogtt2_value"
    ]

    # create fbg column
    df["fbg"] = df["converted_fbg_value"]
    df.loc[df["fbg"].notna() & df["converted_fbg2_value"].notna(), "fbg"] = df[
        "converted_fbg2_value"
    ]

    # fasting columns
    df["fasting_fbg_hrs"] = np.nan
    df["fasting_fbg_hrs"] = df["fasting_duration_delta"].apply(
        lambda x: x.total_seconds() / 3600
    )
    df.loc[df["fbg"].notna() & df["converted_fbg2_value"].notna(), "fasting_fbg_hrs"] = df[
        "repeat_fasting_duration_delta"
    ].apply(lambda x: x.total_seconds() / 3600)
    df["fasting_ogtt_hrs"] = np.nan
    df["fasting_ogtt_hrs"] = df["fasting_duration_delta"].apply(
        lambda x: x.total_seconds() / 3600
    )
    df.loc[df["ogtt"].notna() & df["converted_ogtt2_value"].notna(), "fasting_ogtt_hrs"] = df[
        "repeat_fasting_duration_delta"
    ].apply(lambda x: x.total_seconds() / 3600)

    # bmi
    # subject SR9E8B4D has eligible part two == No but subject has a glucose value
    # NOTE: update 10-02-2025: subject is not eligible by congestive_heart_failure
    # df.loc[(df["screening_identifier"] == "SR9E8B4D"), "eligible_part_two"] = "Yes"

    # merge with physical exam to get waist circumference if taken at baseline
    subject_identifiers = list(df["subject_identifier"])
    qs_subject_visit = SubjectVisit.objects.filter(subject_identifier__in=subject_identifiers)
    df_subject_visit = read_frame(qs_subject_visit)
    df_subject_visit = df_subject_visit.rename(columns={"id": "subject_visit"})
    qs_physical_exam = PhysicalExam.objects.filter(
        subject_visit__subject_identifier__in=subject_identifiers
    )
    df_physical_exam = read_frame(qs_physical_exam)
    # merge w/ subject visit to get subject_identifier
    df_physical_exam = df_physical_exam.merge(
        df_subject_visit[
            ["subject_visit", "subject_identifier", "visit_code", "visit_code_sequence"]
        ],
        on="subject_visit",
        how="left",
    )[["subject_identifier", "visit_code", "visit_code_sequence", "waist_circumference"]]
    df_physical_exam[["waist_circumference"]] = df_physical_exam[
        ["waist_circumference"]
    ].apply(pd.to_numeric)
    # rename column to waist_circumference_baseline
    df_physical_exam["waist_circumference_baseline"] = df_physical_exam["waist_circumference"]
    df_physical_exam.drop(columns=["waist_circumference"])
    df_physical_exam[["waist_circumference_baseline"]] = df_physical_exam[
        ["waist_circumference_baseline"]
    ].apply(pd.to_numeric)
    # merge on subject_identifier with main DF
    df = df.merge(
        df_physical_exam[["subject_identifier", "waist_circumference_baseline"]],
        on="subject_identifier",
        how="left",
    ).reset_index(drop=True)
    # set waist_circumference=waist_circumference_baseline
    # if `waist_circumference` is none and `waist_circumference_baseline` is not
    df.loc[
        (df["waist_circumference"].isna()) & (df["waist_circumference_baseline"].notna()),
        "waist_circumference",
    ] = df["waist_circumference_baseline"]

    # drop waist_circumference_baseline
    return df.drop(columns=["waist_circumference_baseline"])

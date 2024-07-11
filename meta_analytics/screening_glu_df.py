import pandas as pd
from django_pandas.io import read_frame

from meta_screening.models import SubjectScreening
from meta_subject.models import PhysicalExam, SubjectVisit


def get_df(df=None, glucose_tested_only: bool | None = None) -> pd.DataFrame:
    """ "Returns a DF of 5618 records"""
    glucose_tested_only = True if glucose_tested_only is None else False
    if not df:
        qs_screening = SubjectScreening.objects.all()
        df = read_frame(qs_screening)

    # convert all to float
    cols = [
        "fbg_value",
        "fbg2_value",
        "ogtt_value",
        "ogtt2_value",
        "converted_fbg_value",
        "converted_fbg2_value",
        "converted_ogtt_value",
        "converted_ogtt2_value",
        "sys_blood_pressure_avg",
        "dia_blood_pressure_avg",
        "waist_circumference",
        "calculated_bmi_value",
    ]
    df[cols] = df[cols].apply(pd.to_numeric)

    # condition to include any glucose test
    cond_glu = (
        (df["fbg_value"].notna())
        | (df["ogtt_value"].notna())
        | (df["fbg2_value"].notna())
        | (df["ogtt2_value"].notna())
    )

    # has_dm fillna with unk
    df["has_dm"] = df["has_dm"].apply(lambda x: "unk" if not x else x)
    # create a column that summarizes lives_nearby and staying_nearby_12
    df["in_catchment"] = (df["lives_nearby"] == "Yes") & (df["staying_nearby_12"] == "Yes")

    # create fbg column
    df["fbg"] = df["converted_fbg_value"]
    df.loc[df["fbg"].notna() & df["converted_fbg2_value"].notna(), "fbg"] = df[
        "converted_fbg2_value"
    ]

    # create ogtt column
    df["ogtt"] = df["converted_ogtt_value"]
    df.loc[df["ogtt"].notna() & df["converted_ogtt2_value"].notna(), "ogtt"] = df[
        "converted_ogtt2_value"
    ]

    # bmi

    # subject SR9E8B4D has eligible part two == No but subject has a glucose value
    df.loc[(df["screening_identifier"] == "SR9E8B4D"), "eligible_part_two"] = "Yes"

    if glucose_tested_only:
        # condition where subject is eligible P1/P2 and has any type of glucose test
        cond = (
            (df["eligible_part_one"] == "Yes") & (df["eligible_part_two"] == "Yes") & cond_glu
        )
        # filter dataframe
        df = df[cond]

    # merge with physical exam to get waist circumference if taken at baseline
    subject_identifiers = list(df["subject_identifier"])
    qs_subject_visit = SubjectVisit.objects.filter(subject_identifier__in=subject_identifiers)
    df_subject_visit = read_frame(qs_subject_visit)
    df_subject_visit.rename(columns={"id": "subject_visit"}, inplace=True)
    qs_physical_exam = PhysicalExam.objects.filter(
        subject_visit__subject_identifier__in=subject_identifiers
    )
    df_physical_exam = read_frame(qs_physical_exam)
    # merge w/ subject visit to get subject_identifier
    df_physical_exam = pd.merge(
        df_physical_exam,
        df_subject_visit[
            ["subject_visit", "subject_identifier", "visit_code", "visit_code_sequence"]
        ],
        on="subject_visit",
        how="left",
    )
    df_physical_exam = df_physical_exam[
        ["subject_identifier", "visit_code", "visit_code_sequence", "waist_circumference"]
    ]
    df_physical_exam[["waist_circumference"]] = df[["waist_circumference"]].apply(
        pd.to_numeric
    )
    # rename column to waist_circumference_baseline
    df_physical_exam["waist_circumference_baseline"] = df_physical_exam["waist_circumference"]
    df_physical_exam.drop(columns=["waist_circumference"])
    df_physical_exam[["waist_circumference_baseline"]] = df_physical_exam[
        ["waist_circumference_baseline"]
    ].apply(pd.to_numeric)
    # merge on subject_identifier with main DF
    df = pd.merge(
        df,
        df_physical_exam[["subject_identifier", "waist_circumference_baseline"]],
        on="subject_identifier",
        how="left",
    )
    # set waist_circumference=waist_circumference_baseline
    # if `waist_circumference` is none and `waist_circumference_baseline` is not
    df.loc[
        (df["waist_circumference"].isna()) & (df["waist_circumference_baseline"].notna()),
        "waist_circumference",
    ] = df["waist_circumference_baseline"]

    # drop waist_circumference_baseline
    df.drop(columns=["waist_circumference_baseline"], inplace=True)

    return df

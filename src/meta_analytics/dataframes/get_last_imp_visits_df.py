import pandas as pd
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django_pandas.io import read_frame
from edc_pdutils.dataframes import get_appointments, get_crf


class InvalidLotNumber(Exception):  # noqa: N818
    pass


def site_cond(df, site_id):
    return (0 == 0) if not site_id else df.site_id == site_id  # noqa: PLR0133


def get_last_imp_visits_df(
    lot_no: str | None = None,
    site_id: int | None = None,
) -> pd.DataFrame:
    """Returns a dataframe of the last IMP visits based on the last
    StudyMedication refill report.

    `assignment` col defaults to "*****" unless a valid `lot_no` is
    provided.
    """
    lot_obj = None
    if lot_no:
        lot_number_model_cls = django_apps.get_model("meta_pharmacy.lotnumber")
        try:
            lot_obj = lot_number_model_cls.objects.get(lot_no=lot_no)
        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist("The lot number given is invalid") from e

    df_meds = get_crf(
        "meta_subject.studymedication", subject_visit_model="meta_subject.subjectvisit"
    )
    df_meds = (
        df_meds[(df_meds.refill == "Yes") & (site_cond(df_meds, site_id))]
        .groupby(by=["subject_identifier", "site_id"])
        .agg({"endline_visit_code": "max", "endline_visit_datetime": "max"})
        .reset_index()
    )
    df_meds = df_meds.rename(
        columns={
            "endline_visit_code": "imp_visit_code",
            "endline_visit_datetime": "imp_visit_date",
        }
    )
    df_meds.reset_index()

    # merge with OffSchedule
    opts = {} if not site_id else dict(site_id=site_id)
    offschedule_model_cls = django_apps.get_model("meta_prn.offschedule")
    df_off = read_frame(
        offschedule_model_cls.objects.values(
            "subject_identifier", "offschedule_datetime"
        ).filter(**opts),
        verbose=False,
    )
    df_off["offschedule_datetime"] = df_off["offschedule_datetime"].dt.tz_localize(None)
    df_off["offschedule_datetime"] = df_off["offschedule_datetime"].dt.normalize()
    df_off = df_off.set_index("subject_identifier")

    df_meds = df_meds.set_index("subject_identifier")
    df_final = df_meds.merge(
        df_off, left_index=True, right_index=True, how="outer"
    ).reset_index()

    # merge with RandomizationList if lot_obj
    # note: slow to decrypt assignment
    if lot_obj:
        rando_model_cls = django_apps.get_model("meta_rando.randomizationlist")
        qs = rando_model_cls.objects.values("subject_identifier", "assignment").filter(
            assignment=lot_obj.assignment
        )
        df_rando = read_frame(qs, verbose=False)
        df_final = df_final.merge(df_rando, on="subject_identifier", how="left")
    else:
        df_final["assignment"] = "*****"

    # merge in appts
    df_appt = (
        get_appointments()
        .groupby(by=["subject_identifier"])
        .agg({"next_visit_code": "max", "next_appt_datetime": "max"})
        .reset_index()
    )
    df_final = df_final.merge(
        df_appt[["subject_identifier", "next_visit_code", "next_appt_datetime"]],
        on="subject_identifier",
        how="left",
    )
    df_final = df_final[(df_final.offschedule_datetime.isna()) & (df_final.assignment.notna())]

    # Filter out subjects off_schedule.
    # If lot_obj, filter out those with alternative assignment.
    df_final = df_final[(df_final.offschedule_datetime.isna()) & (df_final.assignment.notna())]
    df_final = df_final.drop(columns=["offschedule_datetime"])

    # calculate days since the IMP visit
    df_final["days_since"] = pd.to_datetime("today").normalize() - df_final.imp_visit_date
    df_final["days_until"] = df_final.next_appt_datetime - pd.to_datetime("today").normalize()
    return df_final.reset_index()

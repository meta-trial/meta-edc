from datetime import datetime
from random import sample
from secrets import choice
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from edc_constants.constants import (
    BLACK,
    FEMALE,
    NO,
    NOT_APPLICABLE,
    RANDOM_SAMPLING,
    YES,
)
from edc_reportable.units import MICROMOLES_PER_LITER, MILLIMOLES_PER_LITER
from faker import Faker
from pyparsing import alphas

from meta_edc.meta_version import get_meta_version
from meta_screening.forms import part_one_fields, part_three_fields, part_two_fields

fake = Faker()
now = datetime(2019, 5, 1).astimezone(ZoneInfo("UTC"))
tomorrow = now + relativedelta(days=1)


def get_part_one_eligible_options():
    options = dict(
        age_in_years=25,
        art_six_months=YES,
        continue_part_two=YES,
        ethnicity=BLACK,
        gender=FEMALE,
        hiv_pos=YES,
        hospital_identifier="".join(map(str, sample(range(0, 10), 10))),
        initials=f"{choice(alphas)}{choice(alphas)}".upper(),
        lives_nearby=YES,
        on_rx_stable=YES,
        pregnant=NOT_APPLICABLE,
        report_datetime=now,
        screening_consent=YES,
        selection_method=RANDOM_SAMPLING,
        staying_nearby_12=YES,
        vl_undetectable=YES,
        meta_phase_two=NO,
    )
    if fld := [f for f in part_one_fields if f not in options]:
        raise TypeError(
            f"Missing part one fields for meta phase {get_meta_version()}. Got {fld}."
        )
    return options


def get_part_two_eligible_options():
    options = dict(
        acute_condition=NO,
        acute_metabolic_acidosis=NO,
        advised_to_fast=YES,
        alcoholism=NO,
        already_fasted=NO,
        appt_datetime=now + relativedelta(days=10),
        congestive_heart_failure=NO,
        liver_disease=NO,
        metformin_sensitivity=NO,
        part_two_report_datetime=now,
        renal_function_condition=NO,
        tissue_hypoxia_condition=NO,
        has_dm=NO,
        on_dm_medication=NO,
        agree_to_p3=YES,
        p3_ltfu=NOT_APPLICABLE,
        p3_ltfu_date=None,
        p3_ltfu_comment=None,
        contact_number=None,
    )
    if fld := [f for f in part_two_fields if f not in options]:
        raise TypeError(
            f"Missing part two fields for meta phase {get_meta_version()}. Got {fld}."
        )
    return options


def get_part_three_eligible_options(report_datetime: datetime = None):
    options = dict(
        creatinine_performed=YES,
        creatinine_units=MICROMOLES_PER_LITER,
        creatinine_value=50,
        dia_blood_pressure=65,
        dia_blood_pressure_one=65,
        dia_blood_pressure_two=65,
        fasting=YES,
        fasting_duration_str="8h",
        hba1c_performed=YES,
        hba1c_datetime=report_datetime or now,
        hba1c_value=7.0,
        height=110,
        fbg_datetime=tomorrow,
        fbg_units=MILLIMOLES_PER_LITER,
        fbg_value=6.9,
        ogtt_base_datetime=tomorrow + relativedelta(minutes=5),
        ogtt_datetime=tomorrow + relativedelta(hours=2),
        ogtt_units=MILLIMOLES_PER_LITER,
        ogtt_value=7.8,
        repeat_glucose_opinion=NO,
        ogtt2_performed=NOT_APPLICABLE,
        part_three_report_datetime=report_datetime or now,
        reasons_unsuitable=None,
        sys_blood_pressure=120,
        sys_blood_pressure_one=120,
        sys_blood_pressure_two=120,
        unsuitable_agreed=NOT_APPLICABLE,
        unsuitable_for_study=NO,
        urine_bhcg_date=None,
        urine_bhcg_performed=NOT_APPLICABLE,
        urine_bhcg_value=NOT_APPLICABLE,
        waist_circumference=130,
        weight=65,
        severe_htn=NO,
    )
    if fld := [f for f in part_three_fields if f not in options]:
        raise TypeError(
            f"Missing part three fields for meta phase {get_meta_version()}. Got {fld}."
        )
    return options

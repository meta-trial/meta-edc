from datetime import datetime
from random import sample
from secrets import choice

import arrow
from dateutil.relativedelta import relativedelta
from edc_constants.constants import (
    BLACK,
    FEMALE,
    NO,
    NOT_APPLICABLE,
    RANDOM_SAMPLING,
    TBD,
    YES,
)
from edc_reportable.units import MICROMOLES_PER_LITER, MILLIMOLES_PER_LITER
from faker import Faker
from pyparsing import alphas

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO, get_meta_version
from meta_screening.forms import (
    get_part_one_fields,
    get_part_three_fields,
    get_part_two_fields,
)

fake = Faker()
now = arrow.get(datetime(2019, 5, 5), "UTC").datetime
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
        staying_nearby_6=YES,
    )
    if get_meta_version() == PHASE_THREE:
        options["meta_phase_two"] = NO
        options["staying_nearby_12"] = options.pop("staying_nearby_6")
        if fld := [f for f in get_part_one_fields() if f not in options]:
            raise TypeError(
                f"Missing part one fields for meta phase {get_meta_version()}. Got {fld}."
            )
    else:
        if fld := [f for f in get_part_one_fields() if f not in options]:
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
        appt_datetime=now + relativedelta(days=1),
        congestive_heart_failure=NO,
        liver_disease=NO,
        metformin_sensitivity=NO,
        part_two_report_datetime=now,
        renal_function_condition=NO,
        tissue_hypoxia_condition=NO,
    )
    if get_meta_version() == PHASE_THREE:
        options.update(has_dm=NO, on_dm_medication=NO)
        if fld := [f for f in get_part_two_fields() if f not in options]:
            raise TypeError(
                f"Missing part two fields for meta phase {get_meta_version()}. Got {fld}."
            )
    else:
        if fld := [f for f in get_part_two_fields() if f not in options]:
            raise TypeError(
                f"Missing part two fields for meta phase {get_meta_version()}. Got {fld}."
            )
    return options


def get_part_three_eligible_options():
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
        hba1c_value=7.0,
        height=110,
        ifg_datetime=tomorrow,
        ifg_units=MILLIMOLES_PER_LITER,
        ifg_value=7.0,
        ogtt_base_datetime=tomorrow + relativedelta(minutes=5),
        ogtt_datetime=tomorrow + relativedelta(hours=2),
        ogtt_units=MILLIMOLES_PER_LITER,
        ogtt_value=7.5,
        part_three_report_datetime=now,
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
    )
    if get_meta_version() == PHASE_THREE:
        options["ifg_value"] = 6.9
        options["ogtt_value"] = 7.8
        options["fasting_opinion"] = YES
        options["severe_htn"] = NO
        if fld := [f for f in get_part_three_fields() if f not in options]:
            raise TypeError(
                f"Missing part three fields for meta phase {get_meta_version()}. Got {fld}."
            )
    elif get_meta_version() == PHASE_TWO:
        if fld := [f for f in get_part_three_fields() if f not in options]:
            raise TypeError(
                f"Missing part three fields for meta phase {get_meta_version()}. Got {fld}."
            )
    return options


# part_one_eligible_options = get_part_one_eligible_options()
# part_two_eligible_options = get_part_two_eligible_options()
# part_three_eligible_options = get_part_three_eligible_options()

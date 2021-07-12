from datetime import datetime

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
from meta_edc.meta_version import PHASE_THREE, get_meta_version
from meta_screening.forms import (
    get_part_one_fields,
    get_part_three_fields,
    get_part_two_fields,
)

now = arrow.get(datetime(2019, 5, 5), "UTC").datetime
tomorrow = now + relativedelta(days=1)


def get_part_one_eligible_options():
    options = dict(
        screening_consent=YES,
        report_datetime=now,
        selection_method=RANDOM_SAMPLING,
        hospital_identifier="111",
        initials="ZZ",
        gender=FEMALE,
        age_in_years=25,
        ethnicity=BLACK,
        hiv_pos=YES,
        art_six_months=YES,
        on_rx_stable=YES,
        lives_nearby=YES,
        staying_nearby_6=YES,
        pregnant=NOT_APPLICABLE,
        continue_part_two=YES,
    )
    if get_meta_version() == PHASE_THREE:
        print("fetching part one PHASE_THREE fields")
        options["staying_nearby_12"] = options.pop("staying_nearby_6")
        if fld := [f for f in get_part_one_fields() if f not in options]:
            raise TypeError(
                f"Missing part one fields for meta phase {get_meta_version()}. Got {fld}."
            )
    else:
        print("fetching part one PHASE_TWO fields")
        if fld := [f for f in get_part_one_fields() if f not in options]:
            raise TypeError(
                f"Missing part one fields for meta phase {get_meta_version()}. Got {fld}."
            )
    return options


def get_part_two_eligible_options():
    options = dict(
        part_two_report_datetime=now,
        acute_condition=NO,
        acute_metabolic_acidosis=NO,
        advised_to_fast=YES,
        alcoholism=NO,
        appt_datetime=now + relativedelta(days=1),
        congestive_heart_failure=NO,
        liver_disease=NO,
        metformin_sensitivity=NO,
        has_dm=NO,
        on_dm_medication=NO,
        renal_function_condition=NO,
        tissue_hypoxia_condition=NO,
        already_fasted=NO,
    )
    if get_meta_version() == PHASE_THREE:
        print("fetching part one PHASE_THREE fields")
        if fld := [f for f in get_part_two_fields() if f not in options]:
            raise TypeError(
                f"Missing part two fields for meta phase {get_meta_version()}. Got {fld}."
            )
    else:
        print("fetching part one PHASE_TWO fields")
        if fld := [f for f in get_part_two_fields() if f not in options]:
            raise TypeError(
                f"Missing part two fields for meta phase {get_meta_version()}. Got {fld}."
            )
    return options


def get_part_three_eligible_options():
    options = dict(
        part_three_report_datetime=now,
        weight=65,
        height=110,
        waist_circumference=130,
        sys_blood_pressure=180,
        dia_blood_pressure=65,
        hba1c_performed=YES,
        hba1c_value=7.0,
        creatinine_performed=YES,
        creatinine_value=50,
        creatinine_units=MICROMOLES_PER_LITER,
        fasting=YES,
        fasting_duration_str="8h",
        ifg_value=7.0,
        ifg_units=MILLIMOLES_PER_LITER,
        ifg_datetime=tomorrow,
        ogtt_base_datetime=tomorrow + relativedelta(minutes=5),
        ogtt_value=7.5,
        ogtt_units=MILLIMOLES_PER_LITER,
        ogtt_datetime=tomorrow + relativedelta(hours=2),
        severe_htn=NO,
        urine_bhcg_performed=NOT_APPLICABLE,
        urine_bhcg_value=NOT_APPLICABLE,
        urine_bhcg_date=None,
        unsuitable_for_study=NO,
        reasons_unsuitable=None,
        unsuitable_agreed=NOT_APPLICABLE,
    )
    if get_meta_version() == PHASE_THREE:
        print("fetching part one PHASE_THREE fields")
        if fld := [f for f in get_part_three_fields() if f not in options]:
            raise TypeError(
                f"Missing part three fields for meta phase {get_meta_version()}. Got {fld}."
            )
    else:
        print("fetching part one PHASE_TWO fields")
        options.pop("severe_htn")
        if fld := [f for f in get_part_three_fields() if f not in options]:
            raise TypeError(
                f"Missing part three fields for meta phase {get_meta_version()}. Got {fld}."
            )
    return options


# part_one_eligible_options = get_part_one_eligible_options()
# part_two_eligible_options = get_part_two_eligible_options()
# part_three_eligible_options = get_part_three_eligible_options()

import arrow

from datetime import datetime
from dateutil.relativedelta import relativedelta
from edc_constants.constants import RANDOM_SAMPLING
from edc_constants.constants import YES, BLACK, FEMALE, NOT_APPLICABLE, TBD, NO
from edc_reportable.units import MILLIMOLES_PER_LITER, MICROMOLES_PER_LITER


now = arrow.get(datetime(2019, 5, 5), "UTC").datetime
tomorrow = now + relativedelta(days=1)


part_one_eligible_options = dict(
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
    staying_nearby=YES,
    pregnant=NOT_APPLICABLE,
    continue_part_two=YES,
)
part_two_eligible_options = dict(
    part_two_report_datetime=now,
    acute_condition=NO,
    acute_metabolic_acidosis=NO,
    advised_to_fast=YES,
    alcoholism=NO,
    appt_datetime=now + relativedelta(days=1),
    congestive_heart_failure=NO,
    liver_disease=NO,
    metformin_sensitivity=NO,
    renal_function_condition=NO,
    tissue_hypoxia_condition=NO,
    already_fasted=NO,
)

part_three_eligible_options = dict(
    part_three_report_datetime=now,
    weight=65,
    height=110,
    waist_circumference=130,
    sys_blood_pressure=180,
    dia_blood_pressure=65,
    hba1c_performed=YES,
    hba1c=7.0,
    creatinine_performed=YES,
    creatinine=50,
    creatinine_units=MICROMOLES_PER_LITER,
    fasted=YES,
    fasted_duration_str="8h",
    fasting_glucose=7.0,
    fasting_glucose_units=MILLIMOLES_PER_LITER,
    fasting_glucose_datetime=tomorrow,
    ogtt_base_datetime=tomorrow + relativedelta(minutes=5),
    ogtt_two_hr=7.5,
    ogtt_two_hr_units=MILLIMOLES_PER_LITER,
    ogtt_two_hr_datetime=tomorrow + relativedelta(hours=2),
    urine_bhcg_performed=NOT_APPLICABLE,
    urine_bhcg=NOT_APPLICABLE,
    unsuitable_for_study=NO,
    unsuitable_agreed=NOT_APPLICABLE,
)

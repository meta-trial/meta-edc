from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_constants.constants import YES, NO, FEMALE, BLACK, NOT_APPLICABLE
from edc_reportable.units import MILLIGRAMS_PER_DECILITER, MILLIMOLES_PER_LITER
from edc_utils import get_utcnow
from faker import Faker
from model_bakery.recipe import Recipe

from .models import ScreeningPartOne

fake = Faker()


screeningpartone = Recipe(
    ScreeningPartOne,
    report_datetime=get_utcnow() - relativedelta(days=1),
    hospital_identifier="111",
    initials="ZZ",
    subject_identifier=None,
    gender=FEMALE,
    age_in_years=40,
    ethnicity=BLACK,
    hiv_pos=YES,
    art_six_months=YES,
    on_rx_stable=YES,
    lives_nearby=YES,
    staying_nearby=YES,
    pregnant=NO,
    site=Site.objects.get_current(),
    part_two_report_datetime=get_utcnow() - relativedelta(days=1),
    congestive_heart_failure=NO,
    liver_disease=NO,
    alcoholism=NO,
    acute_metabolic_acidosis=NO,
    renal_function_condition=NO,
    tissue_hypoxia_condition=NO,
    acute_condition=NO,
    metformin_sensitivity=NO,
    advised_to_fast=YES,
    appt_datetime=get_utcnow() + relativedelta(days=1),
    part_three_report_datetime=get_utcnow(),
    weight=65,
    height=120,
    fasted=YES,
    fasted_duration_str="24:00",
    urine_bhcg=NO,
    hba1c=5.7,
    creatinine=0.6,
    creatinine_units=MILLIGRAMS_PER_DECILITER,
    fasting_glucose=6.9,
    fasting_glucose_units=MILLIMOLES_PER_LITER,
    fasting_glucose_datetime=get_utcnow(),
    ogtt_base_datetime=get_utcnow(),
    unsuitable_for_study=NO,
    unsuitable_agreed=NOT_APPLICABLE,
)

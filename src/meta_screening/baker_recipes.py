from clinicedc_constants import (
    BLACK,
    FEMALE,
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    NO,
    NOT_APPLICABLE,
    NULL_STRING,
    YES,
)
from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from django.utils import timezone
from faker import Faker
from model_bakery.recipe import Recipe

from .models import SubjectScreening

fake = Faker()


subjectscreening = Recipe(
    SubjectScreening,
    report_datetime=timezone.now() - relativedelta(days=1),
    screening_consent=YES,
    hospital_identifier="111",
    initials="ZZ",
    subject_identifier=NULL_STRING,
    gender=FEMALE,
    age_in_years=40,
    ethnicity=BLACK,
    hiv_pos=YES,
    art_six_months=YES,
    on_rx_stable=YES,
    lives_nearby=YES,
    staying_nearby_6=YES,
    staying_nearby_12=YES,
    pregnant=NO,
    site=Site.objects.get_current(),
    part_two_report_datetime=timezone.now() - relativedelta(days=1),
    congestive_heart_failure=NO,
    liver_disease=NO,
    alcoholism=NO,
    acute_metabolic_acidosis=NO,
    renal_function_condition=NO,
    tissue_hypoxia_condition=NO,
    acute_condition=NO,
    metformin_sensitivity=NO,
    advised_to_fast=YES,
    appt_datetime=timezone.now() + relativedelta(days=1),
    part_three_report_datetime=timezone.now(),
    weight=65,
    height=120,
    fasting=YES,
    fasting_duration_str="24:00",
    urine_bhcg_value=NO,
    hba1c_value=5.7,
    creatinine_value=0.6,
    creatinine_units=MILLIGRAMS_PER_DECILITER,
    fbg_value=6.9,
    fbg_units=MILLIMOLES_PER_LITER,
    fbg_datetime=timezone.now(),
    ogtt_base_datetime=timezone.now(),
    unsuitable_for_study=NO,
    unsuitable_agreed=NOT_APPLICABLE,
    vl_undetectable=YES,
)

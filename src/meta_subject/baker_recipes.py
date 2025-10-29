from clinicedc_constants import NO, NOT_APPLICABLE, NULL_STRING, PATIENT, POS, YES
from django.utils import timezone
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_bakery.recipe import Recipe

from meta_ae.constants import HOSPITAL_CLINIC

from .constants import LIVE_AT_TERM, NO_COMPLICATIONS
from .models import (
    BirthOutcomes,
    Delivery,
    FollowupExamination,
    HealthEconomicsUpdate,
    MedicationAdherence,
    SubjectRequisition,
    SubjectVisit,
    UrinePregnancy,
)

fake = Faker()

subjectvisit = Recipe(SubjectVisit, reason=SCHEDULED)

subjectrequisition = Recipe(SubjectRequisition)

medicationadherence = Recipe(
    MedicationAdherence,
    report_datetime=timezone.now(),
    visual_score_slider=90,
    visual_score_confirmed=90,
    last_missed_pill=NO,
    pill_count_performed=YES,
    pill_count=3,
    missed_pill_reason=[],
    other_missed_pill_reason=NULL_STRING,
)

urinepregnancy = Recipe(
    UrinePregnancy,
    action_identifier=NULL_STRING,
    report_datetime=timezone.now(),
    performed=YES,
    not_performed_reason=NULL_STRING,
    bhcg_value=POS,
    notified=False,
    notified_datetime=None,
)

followupexamination = Recipe(
    FollowupExamination,
    # site=None,
    # report_datetime=None,
    # subject_visit=None,
    # symptoms_detail=None,
    # attended_clinic=None,
    # admitted_hospital=None,
    # attended_clinic_detail=None,
    # prescribed_medication=None,
    # prescribed_medication_detail=None,
    # attended_clinic_sae=None,
    # any_other_problems=None,
    # any_other_problems_detail=None,
    # any_other_problems_sae=None,
    # any_other_problems_sae_grade=None,
    # art_change=None,
    # art_change_reason=None,
    # art_new_regimen_other=None,
    # abdominal_tenderness=None,
    # enlarged_liver=None,
    # jaundice=None,
    # comment=None,
    # lactic_acidosis=None,
    # hepatomegaly=None,
    # referral=None,
    # referral_reason=None,
)

delivery = Recipe(
    Delivery,
    # site=None,
    action_identifier=NULL_STRING,
    report_datetime=timezone.now(),
    info_available=YES,
    info_source=PATIENT,
    informant_relation=NOT_APPLICABLE,
    informant_relation_other=NULL_STRING,
    delivery_datetime=timezone.now(),
    delivery_time_estimated=NO,
    delivery_location=HOSPITAL_CLINIC,
    delivery_location_other=NULL_STRING,
    delivery_location_name="Big hospital",
    delivery_ga=40,
    gm_treated=NO,
    maternal_outcome=NO_COMPLICATIONS,
)

birthoutcomes = Recipe(
    BirthOutcomes,
    delivery=None,
    action_identifier=NULL_STRING,
    report_datetime=timezone.now(),
    birth_order=1,
    birth_outcome=LIVE_AT_TERM,
    birth_weight=320,
)

healtheconomicsupdate = Recipe(
    HealthEconomicsUpdate,
    report_datetime=timezone.now(),
)

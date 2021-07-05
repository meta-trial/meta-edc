from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_bakery.recipe import Recipe, seq

from .models import FollowupExamination, SubjectRequisition, SubjectVisit

fake = Faker()

subjectvisit = Recipe(SubjectVisit, reason=SCHEDULED)

subjectrequisition = Recipe(SubjectRequisition)

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

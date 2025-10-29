from clinicedc_constants import NO, NULL_STRING, YES
from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from django.utils import timezone
from faker import Faker
from model_bakery.recipe import Recipe, seq

from .models import SubjectConsent, SubjectConsentV1, SubjectReconsent

fake = Faker()

opts = dict(
    assessment_score=YES,
    confirm_identity=seq("12315678"),
    consent_copy=YES,
    consent_datetime=timezone.now(),
    consent_reviewed=YES,
    consent_signature=YES,
    dob=timezone.now() - relativedelta(years=25),
    first_name=fake.first_name,
    gender="M",
    identity=seq("12315678"),
    identity_type="country_id",
    initials="XX",
    is_dob_estimated="-",
    is_incarcerated=NO,
    is_literate=YES,
    last_name=fake.last_name,
    screening_identifier=NULL_STRING,
    study_questions=YES,
    site=Site.objects.get_current(),
    subject_identifier=NULL_STRING,
    user_created="erikvw",
    user_modified="erikvw",
)
subjectconsent = Recipe(SubjectConsent, **opts)
subjectconsentv1 = Recipe(SubjectConsentV1, **opts)

subjectreconsent = Recipe(
    SubjectReconsent,
    site=Site.objects.get_current(),
    consent_reviewed=YES,
    assessment_score=YES,
    study_questions=YES,
    consent_copy=YES,
    action_identifier=NULL_STRING,
    user_created="erikvw",
    user_modified="erikvw",
)

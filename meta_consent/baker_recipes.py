from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_constants.constants import YES, NO
from edc_utils import get_utcnow
from faker import Faker
from model_bakery.recipe import Recipe, seq

from .models import SubjectReconsent
from .models import SubjectConsent


fake = Faker()

subjectconsent = Recipe(
    SubjectConsent,
    assessment_score=YES,
    confirm_identity=seq("12315678"),
    consent_copy=YES,
    consent_datetime=get_utcnow(),
    consent_reviewed=YES,
    consent_signature=YES,
    dob=get_utcnow() - relativedelta(years=25),
    first_name=fake.first_name,
    gender="M",
    identity=seq("12315678"),
    identity_type="country_id",
    initials="XX",
    is_dob_estimated="-",
    is_incarcerated=NO,
    is_literate=YES,
    last_name=fake.last_name,
    screening_identifier=None,
    study_questions=YES,
    site=Site.objects.get_current(),
    subject_identifier=None,
)

subjectreconsent = Recipe(
    SubjectReconsent,
    site=Site.objects.get_current(),
    consent_reviewed=YES,
    assessment_score=YES,
    study_questions=YES,
    consent_copy=YES,
    action_identifier=None,
    tracking_identifier=None,
)

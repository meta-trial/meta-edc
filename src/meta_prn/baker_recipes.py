from dateutil.relativedelta import relativedelta
from django.utils import timezone
from edc_constants.constants import YES
from faker import Faker
from model_bakery.recipe import Recipe

from .models import DmReferral, PregnancyNotification

fake = Faker()


pregnancynotification = Recipe(
    PregnancyNotification,
    # site=None,
    action_identifier=None,
    subject_identifier=None,
    report_datetime=timezone.now(),
    bhcg_confirmed=YES,
    unconfirmed_details=None,
    edd=timezone.now() + relativedelta(months=6),
)

dmreferral = Recipe(
    DmReferral,
    action_identifier=None,
    subject_identifier=None,
    report_datetime=timezone.now(),
)

from clinicedc_constants import NULL_STRING, YES
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from faker import Faker
from model_bakery.recipe import Recipe

from .models import DmReferral, PregnancyNotification

fake = Faker()


pregnancynotification = Recipe(
    PregnancyNotification,
    # site=None,
    action_identifier=NULL_STRING,
    subject_identifier=NULL_STRING,
    report_datetime=timezone.now(),
    bhcg_confirmed=YES,
    unconfirmed_details=NULL_STRING,
    edd=timezone.now() + relativedelta(months=6),
)

dmreferral = Recipe(
    DmReferral,
    action_identifier=NULL_STRING,
    subject_identifier=NULL_STRING,
    report_datetime=timezone.now(),
)

from dateutil.relativedelta import relativedelta
from edc_constants.constants import YES
from edc_utils import get_utcnow
from faker import Faker
from model_bakery.recipe import Recipe

from .models import PregnancyNotification

fake = Faker()


pregnancynotification = Recipe(
    PregnancyNotification,
    # site=None,
    action_identifier=None,
    subject_identifier=None,
    report_datetime=get_utcnow(),
    bhcg_confirmed=YES,
    unconfirmed_details=None,
    edd=get_utcnow() + relativedelta(months=6),
)

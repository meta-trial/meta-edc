from dateutil.relativedelta import relativedelta
from edc_constants.constants import NO, NOT_APPLICABLE, POS, YES
from edc_utils import get_utcnow
from faker import Faker
from model_bakery.recipe import Recipe

from meta_ae.constants import HOSPITAL_CLINIC

from .constants import LIVE_AT_TERM, NO_COMPLICATIONS
from .models import BirthOutcomes, Delivery, PregnancyNotification

fake = Faker()


pregnancynotification = Recipe(
    PregnancyNotification,
    # site=None,
    action_identifier=None,
    subject_identifier=None,
    report_datetime=get_utcnow(),
    bhcg_confirmed=POS,
    unconfirmed_details=None,
    edd=get_utcnow() + relativedelta(months=6),
)

delivery = Recipe(
    Delivery,
    # site=None,
    action_identifier=None,
    subject_identifier=None,
    report_datetime=get_utcnow(),
    informant_is_patient=YES,
    informant_contact=None,
    informant_relation=NOT_APPLICABLE,
    informant_relation_other=None,
    delivery_datetime=get_utcnow(),
    delivery_time_estimated=NO,
    delivery_location=HOSPITAL_CLINIC,
    delivery_location_other=None,
    delivery_location_name="Big hospital",
    delivery_ga=40,
    gm_treated=NO,
    maternal_outcome=NO_COMPLICATIONS,
)

birthoutcomes = Recipe(
    BirthOutcomes,
    delivery=None,
    action_identifier=None,
    maternal_identifier=None,
    report_datetime=get_utcnow(),
    birth_order=1,
    birth_outcome=LIVE_AT_TERM,
    birth_weight=320,
)

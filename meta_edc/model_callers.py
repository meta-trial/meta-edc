from datetime import datetime
from typing import Any

from dateutil.relativedelta import MO, relativedelta
from edc_appointment.constants import NEW_APPT
from edc_call_manager.decorators import register
from edc_call_manager.model_caller import ModelCaller
from edc_utils import get_utcnow


@register("edc_appointment.appointment", "meta_subject.subjectvisit")
class ApppointmentReminderModelCaller(ModelCaller):
    verbose_name = "Appointment reminders"
    label = "AppointmentModelCaller"
    app_label = "edc_call_manager"
    consent_model = "meta_consent.subjectconsent"
    locator_model = "edc_locator.subjectlocator"
    subject_model = "edc_registration.registeredsubject"

    @property
    def start_model_options(self) -> dict:
        """Filter for appts due next week"""
        morning = get_utcnow().replace(second=0, hour=0, minute=0)
        monday = morning + relativedelta(weekday=MO(-1))
        return {
            "appt_status": NEW_APPT,
            **{
                "appt_datetime__gte": monday + relativedelta(weeks=1),
                "appt_datetime__lt": monday + relativedelta(weeks=2),
            },
        }

    def call_datetime(self, start_model_obj: Any) -> datetime:
        """Schedule all calls for next week monday"""
        return start_model_obj.appt_datetime - relativedelta(weekday=MO)

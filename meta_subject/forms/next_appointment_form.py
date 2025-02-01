from datetime import datetime
from zoneinfo import ZoneInfo

from django import forms
from django.db import transaction
from edc_appointment.exceptions import AppointmentWindowError
from edc_appointment.utils import (
    get_allow_skipped_appt_using,
    validate_date_is_on_clinic_day,
)
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import NextAppointment

__all__ = ["NextAppointmentForm"]


class NextAppointmentForm(CrfModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        if (
            cleaned_data.get("health_facility")
            and cleaned_data.get("health_facility").site != self.related_visit.site
        ):
            raise forms.ValidationError({"health_facility": "Invalid for this site"})

        # is next appt
        next_appt = self.related_visit.appointment.next

        if (
            not get_allow_skipped_appt_using()
            and cleaned_data.get("visitschedule")
            and cleaned_data.get("visitschedule").visit_code != next_appt.visit_code
        ):
            raise forms.ValidationError(
                {"visitschedule": f"Invalid. Next visit is {next_appt.visit_code}"}
            )

        appt_date = cleaned_data.get("appt_date")
        appt_datetime = cleaned_data.get("appt_datetime")
        if appt_date:
            appt_datetime = datetime(
                appt_date.year,
                appt_date.month,
                appt_date.day,
                7,
                30,
                0,
                tzinfo=ZoneInfo("UTC"),
            )
        else:
            appt_date = appt_datetime.date()
        if appt_date <= self.related_visit.appointment.appt_datetime.date():
            raise forms.ValidationError(
                "Next date cannot be before current appointment date. "
            )
        if appt_datetime <= self.related_visit.appointment.appt_datetime:
            raise forms.ValidationError(
                "Next date/time cannot be before current appointment date. "
            )

        if cleaned_data.get("health_facility"):
            validate_date_is_on_clinic_day(
                cleaned_data,
                clinic_days=cleaned_data.get("health_facility").clinic_days,
            )

        next_appt.appt_datetime = appt_datetime

        try:
            with transaction.atomic():
                next_appt.save()
                raise TypeError()
        except TypeError:
            pass
        except AppointmentWindowError:
            raise forms.ValidationError(
                {"appt_date": "Invalid. Date falls outside of the window period"}
            )
        return cleaned_data

    class Meta:
        model = NextAppointment
        fields = "__all__"

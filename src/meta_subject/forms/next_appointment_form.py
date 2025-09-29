from __future__ import annotations

from django import forms
from edc_appointment.form_validator_mixins import NextAppointmentCrfFormValidatorMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import NextAppointment

__all__ = ["NextAppointmentForm"]


class NextAppointmentCrfFormValidator(
    NextAppointmentCrfFormValidatorMixin,
    CrfFormValidator,
):
    pass


class NextAppointmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = NextAppointmentCrfFormValidator

    class Meta:
        model = NextAppointment
        fields = "__all__"
        labels = {  # noqa: RUF012
            "appt_date": "Next scheduled appointment date",
            "visitschedule": "Next scheduled appointment",
        }
        help_texts = {  # noqa: RUF012
            "appt_date": (
                "Default recommended. If changed, should be within "
                "the window period of the next appointment"
            ),
            "visitschedule": "Default recommended. Can only be the next visit",
        }

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.forms import forms
from edc_consent.constants import CONSENT_WITHDRAWAL
from edc_constants.constants import DEAD, LOST_TO_FOLLOWUP, OTHER
from edc_form_validators import FormValidator

from ..constants import OTHER_RX_DISCONTINUATION
from .validate_death_report_mixin import ValidateDeathReportMixin


class LossToFollowupFormValidatorMixin:

    loss_to_followup_model = "meta_prn.losstofollowup"

    @property
    def loss_to_followup_model_cls(self):
        return django_apps.get_model(self.loss_to_followup_model)

    def validate_ltfu(self):

        subject_identifier = (
            self.cleaned_data.get("subject_identifier")
            or self.instance.subject_identifier
        )

        try:
            self.loss_to_followup_model_cls.objects.get(
                subject_identifier=subject_identifier
            )
        except ObjectDoesNotExist:
            if self.cleaned_data.get("offschedule_reason") == LOST_TO_FOLLOWUP:
                raise forms.ValidationError(
                    {
                        "offschedule_reason": "Patient was lost to followup, please complete "
                        f"'{self.loss_to_followup_model_cls._meta.verbose_name}' form first."
                    }
                )


class EndOfStudyFormValidator(
    ValidateDeathReportMixin, LossToFollowupFormValidatorMixin, FormValidator
):
    def clean(self):

        self.validate_death_report_if_deceased()
        self.validate_ltfu()

        if self.cleaned_data.get("offschedule_reason"):
            if self.cleaned_data.get("offschedule_reason").name != OTHER:
                self.validate_other_specify(
                    field="offschedule_reason",
                    other_specify_field="other_offschedule_reason",
                    other_stored_value=OTHER_RX_DISCONTINUATION,
                )

            if (
                self.cleaned_data.get("offschedule_reason").name
                != OTHER_RX_DISCONTINUATION
            ):
                self.validate_other_specify(
                    field="offschedule_reason",
                    other_specify_field="other_offschedule_reason",
                    other_stored_value=OTHER,
                )

        self.required_if(DEAD, field="offschedule_reason", field_required="death_date")

        self.required_if(
            LOST_TO_FOLLOWUP, field="offschedule_reason", field_required="ltfu_date",
        )

        self.required_if(
            CONSENT_WITHDRAWAL,
            field="offschedule_reason",
            field_required="consent_withdrawal_reason",
        )

        self.required_if(
            "included_in_error",
            field="offschedule_reason",
            field_required="included_in_error",
        )

        self.required_if(
            "included_in_error",
            field="offschedule_reason",
            field_required="included_in_error_date",
        )

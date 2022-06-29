from django import forms
from django.apps import apps as django_apps
from edc_adverse_event.form_validator_mixins import (
    RequiresDeathReportFormValidatorMixin,
)
from edc_consent.constants import CONSENT_WITHDRAWAL
from edc_constants.constants import DEAD, OTHER
from edc_form_validators import FormValidator
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_ltfu.modelform_mixins import RequiresLtfuFormValidatorMixin
from edc_visit_schedule.models import SubjectScheduleHistory

from ..constants import OTHER_RX_DISCONTINUATION


class EndOfStudyFormValidator(
    RequiresDeathReportFormValidatorMixin,
    RequiresLtfuFormValidatorMixin,
    FormValidator,
):
    death_report_model = "meta_ae.deathreport"
    ltfu_model = None

    def clean(self):

        # is the participant still on a schedule?
        for obj in (
            SubjectScheduleHistory.objects.filter(
                subject_identifier=self.cleaned_data.get("subject_identifier"),
                offschedule_datetime__isnull=True,
            )
            .order_by("onschedule_datetime")
            .first()
        ):
            model_cls = django_apps.get_model(obj.onschedule_model)
            self.raise_validation_error(
                "Participant is still on a study schedule. Got "
                f"{model_cls._meta.verbose_name}. Please take the patient of this "
                "schedule before completing this form"
            )

        if self.cleaned_data.get("offschedule_datetime") and self.cleaned_data.get(
            "last_seen_date"
        ):
            if (
                self.cleaned_data.get("last_seen_date")
                > self.cleaned_data.get("offschedule_datetime").date()
            ):
                raise forms.ValidationError(
                    {"last_seen_date": "Invalid. May not be after termination date"}
                )

        self.validate_death_report_if_deceased()
        self.validate_ltfu()

        if self.cleaned_data.get("offschedule_reason"):
            if self.cleaned_data.get("offschedule_reason").name != OTHER:
                self.validate_other_specify(
                    field="offschedule_reason",
                    other_specify_field="other_offschedule_reason",
                    other_stored_value=OTHER_RX_DISCONTINUATION,
                )

            if self.cleaned_data.get("offschedule_reason").name != OTHER_RX_DISCONTINUATION:
                self.validate_other_specify(
                    field="offschedule_reason",
                    other_specify_field="other_offschedule_reason",
                    other_stored_value=OTHER,
                )

        self.required_if(DEAD, field="offschedule_reason", field_required="death_date")

        self.required_if(
            LOST_TO_FOLLOWUP,
            field="offschedule_reason",
            field_required="ltfu_date",
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

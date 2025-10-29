from decimal import Decimal

from clinicedc_constants import MILLIMOLES_PER_LITER, NO, PENDING, YES
from clinicedc_utils import convert_units
from edc_crf.crf_form_validator import CrfFormValidator
from edc_form_validators import INVALID_ERROR
from edc_glucose.utils import validate_glucose_as_millimoles_per_liter

from meta_reports.models import GlucoseSummary

from .mixins import EndpointValidatorMixin, RepeatFbgDateValidatorMixin


class GlucoseFbgFormValidator(
    EndpointValidatorMixin, RepeatFbgDateValidatorMixin, CrfFormValidator
):
    def clean(self):
        self.required_if(YES, field="fasting", field_required="fasting_duration_str")
        self.required_if(NO, field="fbg_performed", field_required="fbg_not_performed_reason")
        self.required_if(YES, field="fbg_performed", field_required="fbg_datetime")
        if self.cleaned_data.get("fbg_datetime") and self.cleaned_data.get(
            "fbg_datetime"
        ) < self.cleaned_data.get("report_datetime"):
            self.raise_validation_error(
                {"fbg_datetime": "Invalid. Must be on or after report date above"},
                INVALID_ERROR,
            )
        self.required_if(YES, field="fbg_performed", field_required="fbg_value")

        self.applicable_if(YES, field="fbg_performed", field_applicable="fbg_units")

        # endpoint
        self.applicable_if(YES, field="fbg_performed", field_applicable="endpoint_today")
        self.validate_endpoint_fields()

        # repeat_fbg_date
        self.required_if(PENDING, field="endpoint_today", field_required="repeat_fbg_date")
        self.validate_repeat_fbg_date()

    @property
    def converted_fbg_value(self):
        if self.cleaned_data.get("fbg_value") is not None:
            return validate_glucose_as_millimoles_per_liter("fbg", self.cleaned_data)
        return None

    def is_endpoint(self):
        value = NO
        if self.converted_fbg_value and self.converted_fbg_value >= Decimal("7.0"):
            # is there a previous FBG>=7.0 in sequence or do you need to repeat?
            previous_obj = (
                GlucoseSummary.objects.filter(
                    subject_identifier=self.subject_identifier,
                    fbg_datetime__lt=self.cleaned_data.get("fbg_datetime"),
                )
                .order_by("fbg_datetime")
                .last()
            )
            previous_fbg_value = convert_units(
                label="fbg",
                value=float(previous_obj.fbg_value),
                units_from=previous_obj.fbg_units,
                units_to=MILLIMOLES_PER_LITER,
            )
            previous_ogtt_value = convert_units(
                label="ogtt",
                value=float(previous_obj.ogtt_value),
                units_from=previous_obj.ogtt_units,
                units_to=MILLIMOLES_PER_LITER,
            )

            if previous_obj and previous_fbg_value >= 7.0 and previous_ogtt_value <= 11.1:
                value = YES
            else:
                # you need to schedule a repeat
                value = PENDING
        return value

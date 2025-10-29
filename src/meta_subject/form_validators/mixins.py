from decimal import Decimal

from clinicedc_constants import NO, PENDING, YES
from edc_form_validators import INVALID_ERROR

from meta_reports.models import GlucoseSummary


class EndpointValidatorMixin:
    def validate_endpoint_fields(self):
        is_endpoint = self.is_endpoint()
        if is_endpoint == YES and self.cleaned_data.get("endpoint_today") != YES:
            self.raise_validation_error(
                {
                    "endpoint_today": (
                        "Participant has reached a study endpoint today. Expected YES"
                    )
                },
                INVALID_ERROR,
            )
        elif is_endpoint == PENDING and self.cleaned_data.get("endpoint_today") != PENDING:
            self.raise_validation_error(
                {
                    "endpoint_today": (
                        "Participant has not reached a study endpoint today. "
                        "Expected to repeat FBG"
                    )
                },
                INVALID_ERROR,
            )

        elif is_endpoint == NO and self.cleaned_data.get("endpoint_today") != NO:
            self.raise_validation_error(
                {"endpoint_today": "Participant has not reached a study endpoint today"},
                INVALID_ERROR,
            )

    def is_endpoint(self):
        value = NO
        if (
            self.cleaned_data.get("fbg_value")
            and self.cleaned_data.get("ogtt_value")
            and self.cleaned_data.get("fbg_value") >= Decimal("7.0")
            and self.cleaned_data.get("ogtt_value") >= Decimal("11.1")
        ) or (
            self.cleaned_data.get("fbg_value")
            and self.cleaned_data.get("ogtt_value")
            and self.cleaned_data.get("fbg_value") < Decimal("7.0")
            and self.cleaned_data.get("ogtt_value") >= Decimal("11.1")
        ):
            value = YES
        elif (
            self.cleaned_data.get("fbg_value")
            and self.cleaned_data.get("ogtt_value")
            and self.cleaned_data.get("fbg_value") >= Decimal("7.0")
            and self.cleaned_data.get("ogtt_value") < Decimal("11.1")
        ):
            # is there a previous FBG>=7.0 in sequence or do you need to repeat?
            previous_obj = (
                GlucoseSummary.objects.filter(
                    subject_identifier=self.subject_identifier,
                    fbg_datetime__lt=self.cleaned_data.get("fbg_datetime"),
                )
                .order_by("fbg_datetime")
                .last()
            )
            if previous_obj and previous_obj.fbg_value >= Decimal("7.0"):
                value = YES
            else:
                # you need to schedule a repeat
                value = PENDING
        return value


class RepeatFbgDateValidatorMixin:
    def validate_repeat_fbg_date(self):
        if self.cleaned_data.get("repeat_fbg_date"):
            delta = (
                self.cleaned_data.get("repeat_fbg_date")
                - self.cleaned_data.get("fbg_datetime").date()
            )
            if delta.days < 7:
                self.raise_validation_error(
                    {"repeat_fbg_date": "Must be at least 7 days from the FBG date above"},
                    INVALID_ERROR,
                )
            if delta.days > 10:
                self.raise_validation_error(
                    {
                        "repeat_fbg_date": (
                            "Must be no more than 10 days from the FBG date above"
                        )
                    },
                    INVALID_ERROR,
                )

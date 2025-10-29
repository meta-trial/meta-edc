from __future__ import annotations

from datetime import datetime

from clinicedc_constants import NO, YES
from django import forms
from edc_form_validators import INVALID_ERROR, FormValidator
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_utils import formatted_datetime, get_utcnow, to_utc
from edc_utils.date import to_local
from edc_utils.round_up import round_half_away_from_zero

from ..eligibility import EligibilityPartTwo


class ScreeningPartTwoFormValidator(PrnFormValidatorMixin, FormValidator):
    report_datetime_field_attr = "part_two_report_datetime"

    def clean(self):
        self.validate_report_datetimes()

        if (
            self.cleaned_data.get("agree_to_p3") == YES
            and self.cleaned_data.get("advised_to_fast") == NO
        ):
            self.raise_validation_error(
                {"advised_to_fast": "Expected YES. Patient has agreed to return"},
                INVALID_ERROR,
            )
        self.applicable_if_true(self.eligible_part_two, field_applicable="already_fasted")

        self.applicable_if(YES, NO, field="already_fasted", field_applicable="agree_to_p3")

        self.applicable_if(YES, field="agree_to_p3", field_applicable="advised_to_fast")

        self.required_if(YES, field="advised_to_fast", field_required="appt_datetime")

        self.raise_if_not_future_appt_datetime()

        if not self.part_three_report_datetime:
            self.applicable_if_true(
                self.cleaned_data.get("appt_datetime")
                and to_utc(self.cleaned_data.get("appt_datetime")) <= get_utcnow(),
                field_applicable="p3_ltfu",
                applicable_msg="Appointment date has past",
                not_applicable_msg="This field is not applicable. See appointment date above",
            )
        else:
            self.not_applicable_if_true(
                self.part_three_report_datetime is not None,
                field_applicable="p3_ltfu",
                not_applicable_msg=(
                    "The second stage of screening (P3) has already been started."
                ),
            )

        self.required_if(YES, field="p3_ltfu", field_required="p3_ltfu_date")

    @property
    def part_one_report_datetime(self) -> datetime:
        return self.instance.report_datetime

    @property
    def part_three_report_datetime(self) -> datetime | None:
        return self.instance.part_three_report_datetime

    @property
    def eligible_part_two(self) -> bool:
        """Returns False if any of the required fields is YES."""
        eligibility = EligibilityPartTwo(cleaned_data=self.cleaned_data)
        return eligibility.is_eligible

    def validate_report_datetimes(self):
        if (
            self.report_datetime
            and to_utc(self.report_datetime) < self.part_one_report_datetime
        ):
            dte = formatted_datetime(to_local(self.part_one_report_datetime))
            self.raise_validation_error(
                {
                    self.report_datetime_field_attr: (
                        "Cannot be before `Part One` report datetime. "
                        f"Expected date after {dte}. Got {self.report_datetime}"
                    )
                },
                INVALID_ERROR,
            )

        if (
            self.report_datetime
            and self.part_three_report_datetime
            and to_utc(self.report_datetime) > self.part_three_report_datetime
        ):
            dte = formatted_datetime(to_local(self.part_three_report_datetime))
            self.raise_validation_error(
                {
                    self.report_datetime_field_attr: (
                        "Cannot be after `Part Three` report datetime. "
                        f"Expected date before {dte}."
                    )
                },
                INVALID_ERROR,
            )

    def raise_if_not_future_appt_datetime(self):
        """Raises if appt_datetime is not future relative to
        part_two_report_datetime.
        """
        appt_datetime = self.cleaned_data.get("appt_datetime")
        if appt_datetime and self.report_datetime:
            tdelta = appt_datetime - to_local(self.report_datetime)

            hours = tdelta.seconds / 3600

            if (tdelta.days == 0 and hours < 10) or tdelta.days < 0:
                raise forms.ValidationError(
                    {
                        "appt_datetime": (
                            f"Invalid date. Must be at least 10hrs "
                            f"from report date/time. Got {tdelta.days} "
                            f"days {round_half_away_from_zero(hours, 1)} hrs."
                        )
                    }
                )

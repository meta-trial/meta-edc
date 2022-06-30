from zoneinfo import ZoneInfo

from django import forms
from edc_constants.constants import NO, YES
from edc_form_validators import INVALID_ERROR, FormValidator
from edc_utils import get_utcnow

from ..eligibility import EligibilityPartTwo


class ScreeningPartTwoFormValidator(FormValidator):
    def clean(self):

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

        if self.cleaned_data.get("appt_datetime"):
            self.raise_if_not_future_appt_datetime()

        if not self.instance.part_three_report_datetime:
            self.applicable_if_true(
                self.cleaned_data.get("appt_datetime")
                and self.cleaned_data.get("appt_datetime").astimezone(ZoneInfo("UTC"))
                <= get_utcnow(),
                field_applicable="p3_ltfu",
                applicable_msg="Appointment date has past",
                not_applicable_msg="This field is not applicable. See appointment date above",
            )
        else:
            self.not_applicable_if_true(
                self.instance.part_three_report_datetime,
                field_applicable="p3_ltfu",
                not_applicable_msg=(
                    "The second stage of screening (P3) has already been started."
                ),
            )

        self.required_if(YES, field="p3_ltfu", field_required="p3_ltfu_date")

    @property
    def eligible_part_two(self) -> bool:
        """Returns False if any of the required fields is YES."""
        eligibility = EligibilityPartTwo(cleaned_data=self.cleaned_data)
        return eligibility.is_eligible

    def raise_if_not_future_appt_datetime(self):
        """Raises if appt_datetime is not future relative to
        part_two_report_datetime.
        """
        appt_datetime = self.cleaned_data.get("appt_datetime")
        report_datetime = self.cleaned_data.get("part_two_report_datetime")
        if appt_datetime and report_datetime:
            tdelta = appt_datetime - report_datetime

            hours = tdelta.seconds / 3600

            if (tdelta.days == 0 and hours < 10) or tdelta.days < 0:
                raise forms.ValidationError(
                    {
                        "appt_datetime": (
                            f"Invalid date. Must be at least 10hrs "
                            f"from report date/time. Got {tdelta.days} "
                            f"days {round(hours,1)} hrs."
                        )
                    }
                )

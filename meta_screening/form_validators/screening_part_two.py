from django import forms
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator

from ..eligibility import EligibilityPartTwo


class ScreeningPartTwoFormValidator(FormValidator):
    def clean(self):

        self.applicable_if_true(
            self.eligible_part_two, field_applicable="already_fasted"
        )

        self.applicable_if(
            NO, field="already_fasted", field_applicable="advised_to_fast"
        )

        self.required_if_true(self.eligible_part_two, field_required="appt_datetime")

        if self.cleaned_data.get("already_fasted") == NO:
            self.raise_if_not_future_appt_datetime()

        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )

    @property
    def eligible_part_two(self):
        """Returns False if any of the required fields is YES."""
        for fld in EligibilityPartTwo.get_required_fields():
            if not self.cleaned_data.get(fld) or self.cleaned_data.get(fld) == YES:
                return False
        return True

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

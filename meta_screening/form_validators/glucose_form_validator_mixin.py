from django import forms
from edc_constants.constants import NO, YES


class GlucoseFormValidatorMixin:
    """
    Declare with ``FormValidator``.

        class MyFormValidator(GlucoseFormValidatorMixin, FormValidator):
            def clean(self):
                self.validate_ifg()
                self.validate_ogtt()
                self.validate_ogtt_dates()
                self.validate_glucose_dates()
    """

    def validate_ifg(self):
        self.required_if(YES, field="fasted", field_required="fasted_duration_str")

        self.required_if(YES, field="fasted", field_required="fasting_glucose_datetime")

        self.required_if(YES, field="fasted", field_required="fasting_glucose")

        self.required_if_true(
            self.cleaned_data.get("fasting_glucose_datetime"),
            field_required="fasting_glucose",
        )

        self.required_if_true(
            self.cleaned_data.get("fasting_glucose"),
            field_required="fasting_glucose_units",
        )

        self.required_if_true(
            self.cleaned_data.get("fasting_glucose"),
            field_required="fasting_glucose_datetime",
        )

    def validate_ogtt(self):
        self.required_if_true(
            self.cleaned_data.get("ogtt_two_hr_datetime"),
            field_required="ogtt_two_hr",
            inverse=False,
        )

        self.required_if_true(
            self.cleaned_data.get("ogtt_two_hr"),
            field_required="ogtt_two_hr_datetime",
            inverse=False,
        )

        self.required_if_true(
            self.cleaned_data.get("ogtt_two_hr"), field_required="ogtt_two_hr_units"
        )

        self.not_required_if(
            NO, field="fasted", field_not_required="ogtt_base_datetime", inverse=False
        )
        self.not_required_if(
            NO, field="fasted", field_not_required="ogtt_two_hr_datetime", inverse=False
        )
        self.not_required_if(
            NO, field="fasted", field_not_required="ogtt_two_hr", inverse=False
        )
        self.not_required_if(
            NO, field="fasted", field_not_required="ogtt_two_hr_units", inverse=False
        )

    def validate_ogtt_dates(self):
        if self.cleaned_data.get("ogtt_base_datetime") and self.cleaned_data.get(
            "ogtt_two_hr_datetime"
        ):
            dt1 = self.cleaned_data.get("ogtt_base_datetime").date()
            dt2 = self.cleaned_data.get("ogtt_two_hr_datetime").date()
            if dt1.year != dt2.year or dt1.month != dt2.month or dt1.day != dt2.day:
                raise forms.ValidationError(
                    {
                        "ogtt_two_hr_datetime": (
                            f"Invalid date. Expected same day as OGTT initial date."
                        )
                    }
                )
            tdelta = self.cleaned_data.get(
                "ogtt_two_hr_datetime"
            ) - self.cleaned_data.get("ogtt_base_datetime")
            if tdelta.total_seconds() < 3600:
                raise forms.ValidationError(
                    {
                        "ogtt_two_hr_datetime": (
                            "Invalid. Expected more time between OGTT initial and 2hr."
                        )
                    }
                )
            if tdelta.seconds > (3600 * 5):
                raise forms.ValidationError(
                    {
                        "ogtt_two_hr_datetime": (
                            "Invalid. Expected less time between OGTT initial and 2hr."
                        )
                    }
                )

    def validate_glucose_dates(self):
        fasting_glucose_dte = self.cleaned_data.get("fasting_glucose_datetime")
        ogtt_performed_dte = self.cleaned_data.get("ogtt_base_datetime")
        ogtt_two_hr_dte = self.cleaned_data.get("ogtt_two_hr_datetime")
        if fasting_glucose_dte and ogtt_performed_dte and ogtt_two_hr_dte:
            total_seconds = (ogtt_performed_dte - fasting_glucose_dte).total_seconds()
            if total_seconds <= 1:
                raise forms.ValidationError(
                    {
                        "ogtt_base_datetime": (
                            "Invalid date. Expected to be after time "
                            "fasting glucose level was measured"
                        )
                    }
                )
            diff = (ogtt_two_hr_dte - ogtt_performed_dte).total_seconds() / 60.0
            if diff <= 1.0:
                raise forms.ValidationError(
                    {
                        "ogtt_two_hr_datetime": (
                            "Invalid date. Expected to be after time oral glucose "
                            f"tolerance test was performed. ({diff})"
                        )
                    }
                )

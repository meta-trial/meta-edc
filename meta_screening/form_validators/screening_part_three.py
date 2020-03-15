from django import forms
from edc_constants.constants import YES, NO, POS, NEG
from edc_form_validators import FormValidator
from edc_reportable import ConversionNotHandled, CalculatorError, BMI, eGFR


class ScreeningPartThreeFormValidator(FormValidator):
    def clean(self):

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

        self.validate_creatinine()

        self.required_if(YES, field="hba1c_performed", field_required="hba1c")

        self.validate_vitals()

        self.validate_pregnancy()

        self.validate_ogtt_dates()

        self.validate_bmi()

        self.validate_egfr()

        self.validate_glucose_dates()

        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )

        self.applicable_if(
            YES, field="unsuitable_for_study", field_applicable="unsuitable_agreed"
        )

        if self.cleaned_data.get("unsuitable_agreed") == NO:
            raise forms.ValidationError(
                {
                    "unsuitable_agreed": "The study coordinator MUST agree with your assessment. "
                    "Please discuss before continuing."
                }
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

    def validate_bmi(self):
        if self.cleaned_data.get("height") and self.cleaned_data.get("weight"):
            try:
                BMI(
                    height_cm=self.cleaned_data.get("height"),
                    weight_kg=self.cleaned_data.get("weight"),
                ).value
            except CalculatorError as e:
                raise forms.ValidationError(e)

    def validate_egfr(self):
        if (
            self.cleaned_data.get("gender")
            and self.cleaned_data.get("age_in_years")
            and self.cleaned_data.get("ethnicity")
            and self.cleaned_data.get("creatinine")
            and self.cleaned_data.get("creatinine_units")
        ):
            opts = dict(
                gender=self.cleaned_data.get("gender"),
                age=self.cleaned_data.get("age_in_years"),
                ethnicity=self.cleaned_data.get("ethnicity"),
                creatinine=self.cleaned_data.get("creatinine"),
                creatinine_units=self.cleaned_data.get("creatinine_units"),
            )
            try:
                eGFR(**opts).value
            except (CalculatorError, ConversionNotHandled) as e:
                raise forms.ValidationError(e)

    def validate_creatinine(self):
        self.required_if(YES, field="creatinine_performed", field_required="creatinine")
        self.required_if_true(
            self.cleaned_data.get("creatinine"), field_required="creatinine_units"
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

    def validate_pregnancy(self):
        self.applicable_if(
            YES,
            NO,
            field="pregnant",
            field_applicable="urine_bhcg_performed",
            is_instance_field=True,
            msg="See response in part one.",
        )
        self.applicable_if(
            YES, field="urine_bhcg_performed", field_applicable="urine_bhcg"
        )
        self.required_if(
            YES, field="urine_bhcg_performed", field_required="urine_bhcg_date"
        )

        if self.instance.pregnant == YES and self.cleaned_data.get("urine_bhcg") == NEG:
            raise forms.ValidationError(
                {"urine_bhcg": "Invalid, part one says subject is pregnant"}
            )
        elif (
            self.instance.pregnant == NO and self.cleaned_data.get("urine_bhcg") == POS
        ):
            raise forms.ValidationError(
                {"urine_bhcg": "Invalid, part one says subject is not pregnant"}
            )

    def validate_vitals(self):
        fields = [
            "height",
            "weight",
            "waist_circumference",
            "sys_blood_pressure",
            "dia_blood_pressure",
        ]
        if (
            self.cleaned_data.get("height")
            or self.cleaned_data.get("weight")
            or self.cleaned_data.get("waist_circumference")
            or self.cleaned_data.get("sys_blood_pressure")
            or self.cleaned_data.get("dia_blood_pressure")
        ):
            for field in fields:
                if not self.cleaned_data.get(field):
                    raise forms.ValidationError({field: "This field is required"})

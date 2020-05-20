from django import forms
from edc_constants.constants import YES, NO, POS, NEG
from edc_form_validators import FormValidator
from edc_reportable import ConversionNotHandled, CalculatorError, BMI, eGFR

from .glucose_form_validator_mixin import GlucoseFormValidatorMixin


class ScreeningPartThreeFormValidator(GlucoseFormValidatorMixin, FormValidator):
    def clean(self):

        self.validate_ifg()

        self.validate_ogtt()

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
                    "unsuitable_agreed": "The study coordinator MUST agree "
                    "with your assessment. Please discuss before continuing."
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

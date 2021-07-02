from django import forms
from edc_constants.constants import NEG, NO, POS, YES
from edc_form_validators import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin
from edc_glucose.utils import validate_glucose_as_millimoles_per_liter
from edc_reportable import BmiFormValidatorMixin, EgfrFormValidatorMixin


class ScreeningPartThreeFormValidator(
    GlucoseFormValidatorMixin,
    BmiFormValidatorMixin,
    EgfrFormValidatorMixin,
    FormValidator,
):
    def clean(self):

        self.validate_ifg_required_fields()

        validate_glucose_as_millimoles_per_liter("ifg", self.cleaned_data)

        self.validate_ogtt_required_fields()

        validate_glucose_as_millimoles_per_liter("ogtt", self.cleaned_data)

        self.validate_creatinine_required_fields()

        self.required_if(YES, field="hba1c_performed", field_required="hba1c_value")

        self.validate_vitals_fields_required()

        self.validate_pregnancy()

        self.validate_ogtt_dates()

        self.validate_bmi()

        self.validate_egfr()

        self.validate_ifg_before_ogtt()

        self.validate_ogtt_time_interval()

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

    def validate_creatinine_required_fields(self):
        self.required_if(
            YES, field="creatinine_performed", field_required="creatinine_value"
        )
        self.required_if_true(
            self.cleaned_data.get("creatinine_value"), field_required="creatinine_units"
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
            YES, field="urine_bhcg_performed", field_applicable="urine_bhcg_value"
        )
        self.required_if(
            YES, field="urine_bhcg_performed", field_required="urine_bhcg_date"
        )

        if (
            self.instance.pregnant == YES
            and self.cleaned_data.get("urine_bhcg_value") == NEG
        ):
            raise forms.ValidationError(
                {"urine_bhcg_value": "Invalid, part one says subject is pregnant"}
            )
        elif (
            self.instance.pregnant == NO
            and self.cleaned_data.get("urine_bhcg_value") == POS
        ):
            raise forms.ValidationError(
                {"urine_bhcg_value": "Invalid, part one says subject is not pregnant"}
            )

    def validate_vitals_fields_required(self):
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

from django import forms
from edc_form_validators import FormValidatorMixin
from edc_reportable import convert_units, MILLIMOLES_PER_LITER
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin

from ..form_validators import ScreeningPartThreeFormValidator
from ..models import ScreeningPartThree
from .field_lists import part_three_fields


def validate_glucose_as_millimoles_per_liter(
    cleaned_data=None, min_val=None, max_val=None
):
    min_val = min_val or 1.0
    max_val = max_val or 19.0
    for fld in ["fasting_glucose", "ogtt_two_hr"]:
        value = cleaned_data.get(fld)
        units = cleaned_data.get(f"{fld}_units")
        if value and units:
            converted_value = convert_units(
                value, units_from=units, units_to=MILLIMOLES_PER_LITER
            )
            if not (min_val <= converted_value <= max_val):
                raise forms.ValidationError(
                    {
                        fld: (
                            f"This value is out-of-range. "
                            f"Got {converted_value} mmol/L"
                        )
                    }
                )


class ScreeningPartThreeForm(
    AlreadyConsentedFormMixin, FormValidatorMixin, forms.ModelForm
):

    form_validator_cls = ScreeningPartThreeFormValidator

    AUTO_NUMBER_START = 31

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("creatinine"):
            if float(cleaned_data.get("creatinine")) > 9999.0:
                raise forms.ValidationError({"creatinine": "Value is absurd."})

        self.validate_glucose_as_millimoles_per_liter(cleaned_data)

        return cleaned_data

    @staticmethod
    def validate_glucose_as_millimoles_per_liter(cleaned_data=None):
        return validate_glucose_as_millimoles_per_liter(cleaned_data)

    class Meta:
        model = ScreeningPartThree
        fields = part_three_fields

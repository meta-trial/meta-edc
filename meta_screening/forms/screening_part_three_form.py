from django import forms
from edc_form_validators import FormValidatorMixin
from edc_reportable import convert_units, MILLIMOLES_PER_LITER
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin

from ..form_validators import ScreeningPartThreeFormValidator
from ..models import ScreeningPartThree
from .field_lists import part_three_fields


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

        for fld in ["fasting_glucose", "ogtt_two_hr"]:
            value = cleaned_data.get(fld)
            units = cleaned_data.get(f"{fld}_units")
            if value and units:
                converted_value = convert_units(
                    value, units_from=units, units_to=MILLIMOLES_PER_LITER
                )
                if not (1.0 <= converted_value <= 19.0):
                    raise forms.ValidationError(
                        {
                            fld: (
                                f"This value is out-of-range. "
                                f"Got {converted_value} mmol/L"
                            )
                        }
                    )

        return cleaned_data

    class Meta:
        model = ScreeningPartThree
        fields = part_three_fields

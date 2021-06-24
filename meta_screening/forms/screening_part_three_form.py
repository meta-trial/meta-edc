from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from respond_forms.utils import validate_glucose_as_millimoles_per_liter

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

        self.validate_glucose_as_millimoles_per_liter(cleaned_data)

        return cleaned_data

    @staticmethod
    def validate_glucose_as_millimoles_per_liter(cleaned_data=None):
        return validate_glucose_as_millimoles_per_liter(cleaned_data)

    class Meta:
        model = ScreeningPartThree
        fields = part_three_fields

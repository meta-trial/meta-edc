from django import forms
from edc_form_validators import FormValidatorMixin
from edc_glucose.constants import GLUCOSE_HIGH_READING
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin

from ..form_validators import ScreeningPartThreeFormValidator
from ..models import ScreeningPartThree
from .field_lists import part_three_fields

fbg_units_fld = ScreeningPartThree._meta.get_field("fbg_units")


class ScreeningPartThreeForm(AlreadyConsentedFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = ScreeningPartThreeFormValidator

    AUTO_NUMBER_START = 31

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data.get("creatinine_value")
            and float(cleaned_data.get("creatinine_value")) > GLUCOSE_HIGH_READING
        ):
            raise forms.ValidationError({"creatinine_value": "Value is absurd."})
        return cleaned_data

    class Meta:
        model = ScreeningPartThree
        fields = part_three_fields

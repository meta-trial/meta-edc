from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin

from meta_edc.meta_version import PHASE_TWO, get_meta_version

from ..form_validators import ScreeningPartThreeFormValidator
from ..models import ScreeningPartThree
from .field_lists import get_part_three_fields

ifg_units_fld = ScreeningPartThree._meta.get_field("ifg_units")


class ScreeningPartThreeForm(
    AlreadyConsentedFormMixin, FormValidatorMixin, forms.ModelForm
):

    form_validator_cls = ScreeningPartThreeFormValidator

    AUTO_NUMBER_START = 29 if get_meta_version() == PHASE_TWO else 31

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("creatinine_value"):
            if float(cleaned_data.get("creatinine_value")) > 9999.0:
                raise forms.ValidationError({"creatinine_value": "Value is absurd."})
        return cleaned_data

    class Meta:
        model = ScreeningPartThree
        fields = get_part_three_fields()

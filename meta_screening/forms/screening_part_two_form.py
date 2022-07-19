from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin

from ..form_validators import ScreeningPartTwoFormValidator
from ..models import ScreeningPartTwo
from .field_lists import part_two_fields


class ScreeningPartTwoForm(AlreadyConsentedFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ScreeningPartTwoFormValidator

    AUTO_NUMBER_START = 17

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = ScreeningPartTwo
        fields = part_two_fields

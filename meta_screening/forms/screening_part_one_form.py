from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.forms import SiteModelFormMixin
from edc_sites.widgets import SiteField

from ..form_validators import ScreeningPartOneFormValidator
from ..models import ScreeningPartOne
from .field_lists import part_one_fields


class ScreeningPartOneForm(
    AlreadyConsentedFormMixin, SiteModelFormMixin, FormValidatorMixin, forms.ModelForm
):

    form_validator_cls = ScreeningPartOneFormValidator

    site = SiteField()

    class Meta:
        model = ScreeningPartOne
        fields = part_one_fields

from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.forms import SiteModelFormMixin

from ..form_validators import ScreeningPartOneFormValidator
from ..models import ScreeningPartOne
from .field_lists import part_one_fields


class ScreeningPartOneForm(
    AlreadyConsentedFormMixin, SiteModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    form_validator_cls = ScreeningPartOneFormValidator

    class Meta:
        model = ScreeningPartOne
        fields = part_one_fields

        labels = {  # noqa: RUF012
            "site": "Which study site is this?",
        }
        help_texts = {  # noqa: RUF012
            "site": "This question is asked to confirm you are logged in to the correct site.",
        }

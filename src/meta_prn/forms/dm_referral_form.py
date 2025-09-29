from django import forms
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixins import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_offstudy.modelform_mixins import OffstudyNonCrfModelFormMixin
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from ..models import DmReferral


class DmReferralFormValidator(PrnFormValidatorMixin, FormValidator):
    pass


class DmReferralForm(
    SiteModelFormMixin,
    OffstudyNonCrfModelFormMixin,
    ActionItemFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = DmReferralFormValidator

    class Meta:
        model = DmReferral
        fields = "__all__"
        help_text = {"subject_identifier": "(read-only)", "action_identifier": "(read-only)"}  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }

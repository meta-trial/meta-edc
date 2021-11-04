from django import forms
from edc_crf.forms import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import Sf12


class Sf12FormValidator(CrfFormValidatorMixin, FormValidator):
    pass


class Sf12Form(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = Sf12FormValidator

    class Meta:
        model = Sf12
        fields = "__all__"

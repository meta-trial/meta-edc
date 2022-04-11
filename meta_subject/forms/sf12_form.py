from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_qol.forms import Sf12FormValidator as BaseSf12FormValidator

from ..models import Sf12


class Sf12FormValidator(BaseSf12FormValidator):
    pass


class Sf12Form(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = Sf12FormValidator

    class Meta:
        model = Sf12
        fields = "__all__"

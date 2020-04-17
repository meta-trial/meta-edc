from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from sarscov2.forms import CoronaKapFormValidator

from ..models import CoronaKap


class CoronaKapForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = CoronaKapFormValidator

    class Meta:
        model = CoronaKap
        fields = "__all__"

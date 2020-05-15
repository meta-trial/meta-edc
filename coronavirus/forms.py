from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from sarscov2.forms import CoronaKapFormValidator

from .models import CoronaKap


class CoronaKapForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = CoronaKapFormValidator

    class Meta:
        model = CoronaKap
        fields = "__all__"

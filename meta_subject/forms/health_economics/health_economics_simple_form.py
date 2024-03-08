from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from ...form_validators import HealthEconomicsFormValidator
from ...models import HealthEconomicsSimple


class HealthEconomicsSimpleForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsFormValidator

    class Meta:
        model = HealthEconomicsSimple
        fields = "__all__"

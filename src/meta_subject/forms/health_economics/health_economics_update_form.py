from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from ...models import HealthEconomicsUpdate


class HealthEconomicsUpdateForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = None

    class Meta:
        model = HealthEconomicsUpdate
        fields = "__all__"

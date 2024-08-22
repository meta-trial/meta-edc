from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from ...form_validators import DmEndpointFormValidator
from ...models import DmEndpoint


class DmEndpointForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DmEndpointFormValidator

    class Meta:
        model = DmEndpoint
        fields = "__all__"

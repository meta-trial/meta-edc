from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from ...form_validators import DmDiagnosisFormValidator
from ...models import DmDiagnosis


class DmDiagnosisForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DmDiagnosisFormValidator

    class Meta:
        model = DmDiagnosis
        fields = "__all__"

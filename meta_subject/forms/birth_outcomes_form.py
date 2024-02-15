from django import forms
from edc_crf.modelform_mixins import InlineCrfModelFormMixin

from ..form_validators import BirthOutcomesFormValidator
from ..models import BirthOutcomes


class BirthOutcomesForm(InlineCrfModelFormMixin, forms.ModelForm):
    form_validator_cls = BirthOutcomesFormValidator

    class Meta:
        model = BirthOutcomes
        fields = "__all__"

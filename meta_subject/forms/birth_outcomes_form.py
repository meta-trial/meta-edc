from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import InlineCrfModelFormMixin

from ..constants import LIVE_AT_TERM, LIVE_PRETERM
from ..models import BirthOutcomes


class BirthOutcomesFormValidator(CrfFormValidator):
    def clean(self):
        self.required_if(
            LIVE_AT_TERM,
            LIVE_PRETERM,
            field="birth_outcome",
            field_required="birth_weight",
        )


class BirthOutcomesForm(InlineCrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BirthOutcomesFormValidator

    class Meta:
        model = BirthOutcomes
        fields = "__all__"

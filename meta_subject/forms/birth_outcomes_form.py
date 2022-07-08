from django import forms
from edc_crf.modelform_mixins import InlineCrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..constants import LIVE_AT_TERM, LIVE_PRETERM
from ..models import BirthOutcomes


class BirthOutcomesFormValidator(FormValidator):
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

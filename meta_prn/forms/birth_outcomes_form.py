from django import forms
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

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


class BirthOutcomesForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = BirthOutcomesFormValidator

    maternal_identifier = forms.CharField(
        label="Maternal Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = BirthOutcomes
        fields = "__all__"

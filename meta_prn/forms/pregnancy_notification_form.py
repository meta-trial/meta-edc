from django import forms
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_constants.constants import NO
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from ..models import PregnancyNotification


class PregnancyNotificationFormValidator(FormValidator):
    def clean(self):
        self.required_if(
            NO, field="bhcg_confirmed", field_required="unconfirmed_details"
        )


class PregnancyNotificationForm(
    SiteModelFormMixin, FormValidatorMixin, ActionItemFormMixin, forms.ModelForm
):

    form_validator_cls = PregnancyNotificationFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = PregnancyNotification
        fields = "__all__"

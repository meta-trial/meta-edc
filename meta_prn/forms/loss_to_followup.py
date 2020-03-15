from django import forms
from edc_sites.forms import SiteModelFormMixin
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_form_validators.form_validator import FormValidator

from ..models import LossToFollowup


class LossToFollowupFormValidator(FormValidator):
    pass


class LossToFollowupForm(
    SiteModelFormMixin, FormValidatorMixin, ActionItemFormMixin, forms.ModelForm
):

    form_validator_cls = LossToFollowupFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = LossToFollowup
        fields = "__all__"

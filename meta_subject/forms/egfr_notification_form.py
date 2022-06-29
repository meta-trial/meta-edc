from django import forms
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_constants.constants import CLOSED, NEW, OPEN
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import INVALID_ERROR
from edc_form_validators.form_validator import FormValidator

from ..models import EgfrNotification


class EgfrNotificationFormValidator(FormValidator):
    def clean(self):
        self.required_if(OPEN, CLOSED, field="report_status", field_required="narrative")
        if self.cleaned_data.get("report_status") == NEW:
            self.raise_validation_error(
                {"report_status": "Cannot be NEW, set to OPEN or CLOSED"}, INVALID_ERROR
            )


class EgfrNotificationForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):

    form_validator_cls = EgfrNotificationFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = EgfrNotification
        fields = "__all__"

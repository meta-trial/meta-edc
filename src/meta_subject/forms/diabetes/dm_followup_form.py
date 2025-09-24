from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_model_fields.widgets import SliderWidget

from ...form_validators import DmFollowupFormValidator
from ...models import DmFollowup


class DmFollowupForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):
    form_validator_cls = DmFollowupFormValidator

    visual_score_slider = forms.CharField(
        label="Visual Score", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = DmFollowup
        fields = "__all__"
        help_text = {"action_identifier": "(read-only)"}  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "action_identifier": forms.TextInput(
                attrs={"required": False, "readonly": "readonly"}
            ),
        }

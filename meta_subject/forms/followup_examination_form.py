from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..form_validators import FollowupExaminationFormValidator
from ..models import FollowupExamination


class FollowupExaminationForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):
    form_validator_cls = FollowupExaminationFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = FollowupExamination
        fields = "__all__"

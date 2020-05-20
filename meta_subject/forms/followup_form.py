from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import Followup


class FollowupFormValidator(FormValidator):
    pass


class FollowupForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = FollowupFormValidator

    class Meta:
        model = Followup
        fields = "__all__"

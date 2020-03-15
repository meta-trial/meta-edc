from edc_crf.modelform_mixins import CrfModelFormMixin
from django import forms
from edc_form_validators import FormValidator

from ..models import FollowupVitals


class FollowupFormValidator(FormValidator):
    pass


class FollowupVitalsForm(CrfModelFormMixin, forms.ModelForm):

    # form_validator_cls = FollowupFormValidator

    class Meta:
        model = FollowupVitals
        fields = "__all__"

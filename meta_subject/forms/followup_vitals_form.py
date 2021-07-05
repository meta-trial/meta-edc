from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import FollowupVitals


class FollowupVitalsFormValidator(FormValidator):
    pass


class FollowupVitalsForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = FollowupVitalsFormValidator

    class Meta:
        model = FollowupVitals
        fields = "__all__"

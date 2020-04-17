from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import Followup


class FollowupForm(CrfModelFormMixin, forms.ModelForm):

    # form_validator_cls = FollowupFormValidator

    class Meta:
        model = Followup
        fields = "__all__"

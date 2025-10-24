from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..form_validators import HivExitReviewFormValidator
from ..models import HivExitReview


class HivExitReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HivExitReviewFormValidator

    class Meta:
        model = HivExitReview
        fields = "__all__"

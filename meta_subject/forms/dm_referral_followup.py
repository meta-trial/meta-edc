from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_model_fields.widgets import SliderWidget

from ..form_validators import DmReferralFollowupFormValidator
from ..models import DmReferralFollowup


class DmReferralFollowupForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DmReferralFollowupFormValidator

    visual_score_slider = forms.CharField(
        label="Visual Score", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = DmReferralFollowup
        fields = "__all__"

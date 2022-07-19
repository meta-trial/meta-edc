from django import forms
from edc_adverse_event.forms import AeFollowupModelFormMixin

from ..models import AeFollowup


class AeFollowupForm(AeFollowupModelFormMixin, forms.ModelForm):
    class Meta(AeFollowupModelFormMixin.Meta):
        model = AeFollowup
        fields = "__all__"

from django import forms
from edc_adverse_event.forms import AeSusarModelFormMixin

from ..models import AeSusar


class AeSusarForm(AeSusarModelFormMixin, forms.ModelForm):
    class Meta(AeSusarModelFormMixin.Meta):
        model = AeSusar
        fields = "__all__"

from django import forms
from edc_adverse_event.modelform_mixins import AeSusarModelFormMixin

from ..models import AeSusar


class AeSusarForm(AeSusarModelFormMixin, forms.ModelForm):
    class Meta:
        model = AeSusar
        fields = "__all__"

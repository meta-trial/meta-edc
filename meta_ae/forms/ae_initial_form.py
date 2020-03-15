from django import forms
from edc_adverse_event.modelform_mixins import AeInitialModelFormMixin

from ..models import AeInitial


class AeInitialForm(AeInitialModelFormMixin, forms.ModelForm):
    class Meta:
        model = AeInitial
        fields = "__all__"

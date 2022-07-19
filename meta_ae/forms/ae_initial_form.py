from django import forms
from edc_adverse_event.forms import AeInitialModelFormMixin

from ..models import AeInitial


class AeInitialForm(AeInitialModelFormMixin, forms.ModelForm):
    class Meta(AeInitialModelFormMixin.Meta):
        model = AeInitial
        fields = "__all__"

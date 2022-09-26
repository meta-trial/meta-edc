from django import forms
from edc_adverse_event.modelform_mixins import AeTmgModelFormMixin

from ..models import AeTmg


class AeTmgForm(AeTmgModelFormMixin, forms.ModelForm):
    class Meta(AeTmgModelFormMixin.Meta):
        model = AeTmg
        fields = "__all__"

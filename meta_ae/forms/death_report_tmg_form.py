from django import forms
from edc_adverse_event.modelform_mixins import DeathReportTmgModelFormMixin

from ..models import DeathReportTmg


class DeathReportTmgForm(DeathReportTmgModelFormMixin, forms.ModelForm):
    class Meta:
        model = DeathReportTmg
        fields = "__all__"

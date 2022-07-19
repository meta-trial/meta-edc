from django import forms
from edc_adverse_event.forms import DeathReportTmgModelFormMixin

from ..models import DeathReportTmg


class DeathReportTmgForm(DeathReportTmgModelFormMixin, forms.ModelForm):
    class Meta(DeathReportTmgModelFormMixin.Meta):
        model = DeathReportTmg
        fields = "__all__"

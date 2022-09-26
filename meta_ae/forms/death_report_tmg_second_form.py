from django import forms
from edc_adverse_event.modelform_mixins import DeathReportTmgModelFormMixin

from ..models import DeathReportTmgSecond


class DeathReportTmgSecondForm(DeathReportTmgModelFormMixin, forms.ModelForm):
    class Meta(DeathReportTmgModelFormMixin.Meta):
        model = DeathReportTmgSecond
        fields = "__all__"

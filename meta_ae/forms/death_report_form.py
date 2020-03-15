from django import forms
from edc_adverse_event.modelform_mixins import DeathReportModelFormMixin

from ..models import DeathReport


class DeathReportForm(DeathReportModelFormMixin, forms.ModelForm):
    class Meta:
        model = DeathReport
        fields = "__all__"

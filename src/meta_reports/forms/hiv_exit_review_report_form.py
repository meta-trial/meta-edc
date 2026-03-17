from django import forms

from ..models import HivExitReviewReport


class HivExitReviewReportForm(forms.ModelForm):
    class Meta:
        model = HivExitReviewReport
        fields = ("appt_status",)

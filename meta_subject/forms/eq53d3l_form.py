from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_model.widgets import SliderWidget
from edc_qol.forms import Eq5d3lFormValidator

from ..models import Eq5d3l


class Eq5d3lForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = Eq5d3lFormValidator

    health_today_score_slider = forms.CharField(
        label="Health TODAY scale", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = Eq5d3l
        fields = "__all__"

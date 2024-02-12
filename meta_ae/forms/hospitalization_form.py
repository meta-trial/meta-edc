from django import forms
from django.forms import ALL_FIELDS
from edc_adverse_event.modelform_mixins import HospitalizationModelFormMixin

from ..models import Hospitalization


class HospitalizationForm(HospitalizationModelFormMixin, forms.ModelForm):
    class Meta(HospitalizationModelFormMixin.Meta):
        model = Hospitalization
        fields = ALL_FIELDS

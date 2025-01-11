from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from ..models import SubjectConsentV1Ext


class SubjectConsentV1ExtForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    widgets = {
        "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
    }

    class Meta:
        model = SubjectConsentV1Ext
        fields = "__all__"

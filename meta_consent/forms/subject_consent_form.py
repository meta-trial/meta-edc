from django import forms
from django.utils.translation import gettext_lazy as _
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from ..form_validators import SubjectConsentFormValidator
from ..models import SubjectConsent

help_texts = {
    "identity": (
        _(
            "Use Country ID Number, Passport number, driver's license "
            "number or Country ID receipt number"
        )
    ),
    "witness_name": (
        _(
            "Required only if participant is illiterate. "
            "Format is 'LASTNAME, FIRSTNAME'. "
            "All uppercase separated by a comma."
        )
    ),
    "screening_identifier": _("(read-only)"),
}


widgets = {
    "screening_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
}


class SubjectConsentForm(
    SiteModelFormMixin, ConsentModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    form_validator_cls = SubjectConsentFormValidator

    def validate_gender_of_consent(self):
        return None

    def validate_guardian_and_dob(self):
        return None

    class Meta:
        model = SubjectConsent
        fields = "__all__"
        help_texts = help_texts
        widgets = widgets

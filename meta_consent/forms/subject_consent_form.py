from django import forms
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from meta_form_validators import SubjectConsentFormValidator

from ..models import SubjectConsent


class SubjectConsentForm(
    SiteModelFormMixin, FormValidatorMixin, ConsentModelFormMixin, forms.ModelForm
):

    form_validator_cls = SubjectConsentFormValidator

    screening_identifier = forms.CharField(
        label="Screening identifier",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    def clean_gender_of_consent(self):
        return None

    def clean_guardian_and_dob(self):
        return None

    def clean_identity_with_unique_fields(self):
        return None

    class Meta:
        model = SubjectConsent
        fields = "__all__"
        help_texts = {
            "identity": (
                "Use Country ID Number, Passport number, driver's license "
                "number or Country ID receipt number"
            ),
            "witness_name": (
                "Required only if participant is illiterate. "
                "Format is 'LASTNAME, FIRSTNAME'. "
                "All uppercase separated by a comma."
            ),
        }

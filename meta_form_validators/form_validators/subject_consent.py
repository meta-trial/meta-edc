from django import forms
from django.conf import settings
from edc_consent.form_validators import SubjectConsentFormValidatorMixin
from edc_form_validators import FormValidator


class SubjectConsentFormValidator(SubjectConsentFormValidatorMixin, FormValidator):
    def validate_identity(self):
        """Validate that the identity is a hospital number and
        matches that on the screening form.
        """
        if self.cleaned_data.get("identity_type") != "hospital_no":
            raise forms.ValidationError(
                {"identity_type": "Expected 'hospital number'."}
            )

        if self.subject_screening.hospital_identifier != self.cleaned_data.get(
            "identity"
        ):
            raise forms.ValidationError(
                {
                    "identity": (
                        "The hospital identifier does not match that "
                        "reported at screening."
                    )
                }
            )

    def validate_consent_datetime(self):
        if getattr(settings, "EDC_CONSENT_BYPASS_CONSENT_DATETIME_VALIDATION", False):
            return None
        return super().validate_consent_datetime()

from django import forms
from edc_form_validators import FormValidator


class SubjectScreeningFormValidator(FormValidator):
    def clean(self):
        raise forms.ValidationError(
            "This form may only be completed one part at a time. "
            "See the EDC's `Screening` section."
        )

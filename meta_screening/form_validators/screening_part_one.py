from edc_constants.constants import MALE
from edc_constants.constants import YES
from edc_form_validators import FormValidator
from django import forms


class ScreeningPartOneFormValidator(FormValidator):
    def clean(self):

        if (
            not self.cleaned_data.get("screening_consent")
            or self.cleaned_data.get("screening_consent") != YES
        ):
            raise forms.ValidationError(
                {
                    "screening_consent": (
                        "You may NOT screen this subject without their verbal consent."
                    )
                }
            )

        self.applicable_if(YES, field="hiv_pos", field_applicable="art_six_months")

        self.applicable_if(YES, field="hiv_pos", field_applicable="on_rx_stable")

        self.not_applicable_if(
            MALE, field="gender", field_applicable="pregnant", inverse=False
        )

        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )

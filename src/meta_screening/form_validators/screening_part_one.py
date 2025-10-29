from clinicedc_constants import MALE, YES
from django import forms
from edc_form_validators import FormValidator
from edc_prn.modelform_mixins import PrnFormValidatorMixin


class ScreeningPartOneFormValidator(PrnFormValidatorMixin, FormValidator):
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

        self.applicable_if(YES, field="hiv_pos", field_applicable="vl_undetectable")

        # TODO: what if FEMALE and not applicable??

        self.not_applicable_if(
            MALE, field="gender", field_applicable="pregnant", inverse=False
        )

        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )

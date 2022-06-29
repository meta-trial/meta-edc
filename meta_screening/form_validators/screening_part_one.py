from django import forms
from edc_consent.form_validators import ConsentFormValidatorMixin
from edc_constants.constants import MALE, YES
from edc_form_validators import FormValidator


class ScreeningPartOneFormValidator(ConsentFormValidatorMixin, FormValidator):
    def clean(self):

        self.get_consent_for_period_or_raise(self.cleaned_data.get("report_datetime"))

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

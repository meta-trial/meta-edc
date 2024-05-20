from edc_constants.constants import NO, YES
from edc_crf.crf_form_validator import CrfFormValidator
from edc_form_validators import INVALID_ERROR


class DmDiagnosisFormValidator(CrfFormValidator):
    def clean(self):
        # dx_date must be on or before report datetime
        if (
            self.cleaned_data.get("report_datetime")
            and self.cleaned_data.get("dx_date")
            and self.cleaned_data.get("dx_date")
            > self.cleaned_data.get("report_datetime").date()
        ):
            self.raise_validation_error(
                {"dx_date": "Invalid. Expected a date on or before the report date above. "},
                INVALID_ERROR,
            )

        self.required_if(YES, field="dx_tmg", field_required="dx_tmg_date")

        if (
            self.cleaned_data.get("dx_tmg_date")
            and self.cleaned_data.get("dx_date")
            and self.cleaned_data.get("dx_tmg_date") > self.cleaned_data.get("dx_date")
        ):
            self.raise_validation_error(
                {
                    "dx_tmg_date": (
                        "Invalid. Expected a date on or before the diagnosis date above. "
                    )
                },
                INVALID_ERROR,
            )

        self.required_if(NO, field="dx_tmg", field_required="dx_no_tmg_reason")

        # TODO: do we check for lab results listed in the inline?

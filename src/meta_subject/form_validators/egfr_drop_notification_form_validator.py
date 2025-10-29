from clinicedc_constants import CLOSED, NEW, OPEN
from edc_crf.crf_form_validator import CrfFormValidator
from edc_form_validators import INVALID_ERROR


class EgfrDropNotificationFormValidator(CrfFormValidator):
    def clean(self):
        self.required_if(OPEN, CLOSED, field="report_status", field_required="narrative")
        if self.cleaned_data.get("report_status") == NEW:
            self.raise_validation_error(
                {"report_status": "Cannot be NEW, set to OPEN or CLOSED"}, INVALID_ERROR
            )

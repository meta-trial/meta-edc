from edc_constants.constants import OTHER
from edc_form_validators import FormValidator


class SubjectRefusalFormValidator(FormValidator):
    def clean(self):
        self.required_if(OTHER, field="reason", field_required="other_reason")

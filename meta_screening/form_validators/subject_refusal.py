from edc_form_validators import FormValidator
from edc_constants.constants import OTHER


class SubjectRefusalFormValidator(FormValidator):
    def clean(self):
        self.required_if(OTHER, field="reason", field_required="other_reason")

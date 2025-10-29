from clinicedc_constants import OTHER
from edc_form_validators import FormValidator
from edc_prn.modelform_mixins import PrnFormValidatorMixin


class SubjectRefusalFormValidator(PrnFormValidatorMixin, FormValidator):
    def clean(self):
        self.required_if(OTHER, field="reason", field_required="other_reason")

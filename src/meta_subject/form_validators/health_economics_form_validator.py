from edc_crf.crf_form_validator import CrfFormValidator
from edc_he.form_validators import SimpleFormValidatorMixin


class HealthEconomicsFormValidator(SimpleFormValidatorMixin, CrfFormValidator):
    def clean(self):
        self.clean_education()

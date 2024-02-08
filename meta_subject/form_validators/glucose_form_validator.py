from edc_crf.crf_form_validator import CrfFormValidator
from edc_glucose.form_validators import FbgOgttFormValidatorMixin


class GlucoseFormValidator(FbgOgttFormValidatorMixin, CrfFormValidator):
    def clean(self):
        self.validate_glucose_testing_matrix()

from edc_crf.crf_form_validator import CrfFormValidator

from ..constants import LIVE_AT_TERM, LIVE_PRETERM


class BirthOutcomesFormValidator(CrfFormValidator):
    def clean(self):
        self.required_if(
            LIVE_AT_TERM,
            LIVE_PRETERM,
            field="birth_outcome",
            field_required="birth_weight",
        )

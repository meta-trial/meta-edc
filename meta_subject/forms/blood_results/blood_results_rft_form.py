from django import forms
from django.utils.safestring import mark_safe
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_panel.panels import rft_panel
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin
from edc_reportable import BmiFormValidatorMixin

from ...models import BloodResultsRft


class BloodResultsRftFormValidator(
    BloodResultsFormValidatorMixin, BmiFormValidatorMixin, CrfFormValidator
):
    panel = rft_panel

    def clean(self):
        super().clean()
        self.validate_bmi()


class BloodResultsRftForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = BloodResultsRftFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = BloodResultsRft
        fields = "__all__"
        help_texts = {
            "action_identifier": "(read-only)",
            "egfr_value": mark_safe(  # nosec B308
                "Calculated using 2009 CKD-EPI Creatinine. "
                "See https://nephron.com/epi_equation"
            ),
            "egfr_drop_value": mark_safe(  # nosec B308
                "Calculated using 2009 CKD-EPI Creatinine. "
                "See https://nephron.com/epi_equation"
            ),
        }

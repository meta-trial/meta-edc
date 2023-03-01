from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import InlineCrfModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import OtherArvRegimensDetail


class OtherArvRegimensDetailFormValidator(CrfFormValidator):
    def clean(self):
        if not self.cleaned_data.get("DELETE"):
            self.validate_other_specify(
                field="arv_regimen", other_specify_field="other_arv_regimen"
            )
            self.required_if_true(
                self.cleaned_data.get("arv_regimen"),
                field_required="arv_regimen_start_date",
            )

    def validate_crf_report_datetime(self):
        pass


class OtherArvRegimensDetailForm(InlineCrfModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = OtherArvRegimensDetailFormValidator

    class Meta:
        model = OtherArvRegimensDetail
        fields = "__all__"

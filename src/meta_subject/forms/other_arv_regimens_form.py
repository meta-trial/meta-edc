from clinicedc_constants import YES
from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_model_form.mixins import InlineModelFormMixin

from ..models import OtherArvRegimens


class OtherArvRegimensFormValidator(CrfFormValidator):
    def clean(self):
        self.required_if(
            YES,
            field="has_other_regimens",
            field_required="arv_regimen",
            field_required_inline_set="otherarvregimensdetail_set",
            required_msg="Based on your response, additional ARV Regimen(s) are required.",
            not_required_msg=(
                "Based on your response, additional ARV Regimen(s) are NOT required."
            ),
        )


class OtherArvRegimensForm(InlineModelFormMixin, CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = OtherArvRegimensFormValidator

    def clean(self):
        cleaned_data = super().clean()
        self.unique_inline_values_or_raise(
            field="arv_regimen",
            inline_model="meta_subject.otherarvregimensdetail",
            field_label="ARV Regimens",
        )
        self.unique_inline_values_or_raise(
            field="arv_regimen_start_date",
            inline_model="meta_subject.otherarvregimensdetail",
            field_label="ARV Start Dates",
        )
        self.dates_not_after_report_datetime(
            field="arv_regimen_start_date",
            inline_model="meta_subject.otherarvregimensdetail",
            field_label="ARV Start Dates",
        )
        return cleaned_data

    class Meta:
        model = OtherArvRegimens
        fields = "__all__"

from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_constants.constants import NO, YES
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import INVALID_ERROR

from ..models import UrinePregnancy


class UrinePregnancyFormValidator(CrfFormValidator):
    def clean(self):
        self.required_if(NO, field="performed", field_required="not_performed_reason")
        self.required_if(YES, field="performed", field_required="assay_date")
        if (
            self.cleaned_data.get("report_datetime")
            and self.cleaned_data.get("assay_date")
            and self.cleaned_data.get("assay_date")
            > self.cleaned_data.get("report_datetime").date()
        ):
            self.raise_validation_error(
                {"assay_date": "Cannot be after report datetime"}, INVALID_ERROR
            )
        self.applicable_if(YES, field="performed", field_applicable="bhcg_value")


class UrinePregnancyForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):
    form_validator_cls = UrinePregnancyFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = UrinePregnancy
        fields = "__all__"

from django import forms
from edc_constants.constants import YES
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import PhysicalExam


class PhysicalExamFormValidator(CrfFormValidator):
    def clean(self):
        self.required_if(
            YES,
            field="irregular_heartbeat",
            field_required="irregular_heartbeat_description",
        )

        self.required_if(
            YES,
            field="abdominal_tenderness",
            field_required="abdominal_tenderness_description",
        )


class PhysicalExamForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = PhysicalExamFormValidator

    class Meta:
        model = PhysicalExam
        fields = "__all__"

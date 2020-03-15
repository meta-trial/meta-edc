from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab.form_validators import RequisitionFormValidator
from edc_lab.forms import RequisitionFormMixin
from edc_metadata.constants import NOT_REQUIRED

from ..models import SubjectRequisition


class SubjectRequisitionForm(RequisitionFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = RequisitionFormValidator

    requisition_identifier = forms.CharField(
        label="Requisition identifier",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("reason_not_drawn") == NOT_REQUIRED:
            raise forms.ValidationError(
                {"reason_not_drawn": "Invalid choice. Not expected " "for this panel"}
            )
        return cleaned_data

    class Meta:
        model = SubjectRequisition
        fields = "__all__"

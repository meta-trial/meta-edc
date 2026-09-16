from clinicedc_constants import OTHER, YES
from django import forms
from edc_form_validators import FormValidator, FormValidatorMixin

from ..models import AeFinalClassification


class AeFinalClassificationFormValidator(FormValidator):
    def clean(self) -> None:
        self.required_if(
            OTHER,
            field="final_ae_classification",
            field_required="final_ae_classification_other",
        )
        self.required_if(
            YES,
            field="conflict_resolved",
            field_required="final_ae_classification",
        )


class AeFinalClassificationForm(FormValidatorMixin, forms.ModelForm):
    """Form for reconciling the final AE classification post-closure."""

    form_validator_cls = AeFinalClassificationFormValidator

    class Meta:
        model = AeFinalClassification
        fields = "__all__"

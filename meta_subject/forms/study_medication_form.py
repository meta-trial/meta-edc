from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_pharmacy.form_validators import (
    StudyMedicationFormValidator as BaseStudyMedicationFormValidator,
)
from edc_visit_schedule.constants import DAY1

from ..models import StudyMedication


class StudyMedicationFormValidator(BaseStudyMedicationFormValidator):
    def clean(self):
        self.validate_half_dose_at_baseline()
        super().clean()

    def validate_half_dose_at_baseline(self):
        """Require 1000mg dose at baseline"""
        if (
            self.cleaned_data.get("subject_visit").visit_code == DAY1
            and self.cleaned_data.get("subject_visit").visit_code_sequence == 0
        ):
            if (
                self.cleaned_data.get("dosage_guideline")
                and self.cleaned_data.get("dosage_guideline").dose != 1000
            ):
                raise forms.ValidationError(
                    {"dosage_guideline": "Invalid. Expected 1000mg/day at baseline"}
                )


class StudyMedicationForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = StudyMedicationFormValidator

    class Meta:
        model = StudyMedication
        fields = "__all__"

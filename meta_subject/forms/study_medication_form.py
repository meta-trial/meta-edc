from django import forms
from edc_constants.constants import NO, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import INVALID_ERROR, FormValidator
from edc_pharmacy.models import DosageGuideline, Medication, Rx, RxRefill
from edc_visit_schedule.constants import DAY1

from meta_pharmacy.constants import METFORMIN

from ..models import StudyMedication


class StudyMedicationFormValidator(FormValidator):
    def clean(self):
        self.validate_half_dose_at_baseline()

        self.required_if(
            YES, field="order_next", field_required="next_dosage_guideline"
        )
        if self.cleaned_data.get("order_next") == NO and self.next_refill:
            if self.next_refill.active:
                self.raise_validation_error(
                    "Invalid. Next refill is already active", INVALID_ERROR
                )
        if (
            self.cleaned_data.get("order_next") == NO
            and not self.cleaned_data.get("subject_visit").appointment.next
        ):
            self.raise_validation_error(
                "Invalid. This is the last scheduled visit", INVALID_ERROR
            )

        self.required_if(YES, field="order_next", field_required="next_formulation")

    def validate_half_dose_at_baseline(self):
        if (
            self.cleaned_data.get("subject_visit").visit_code == DAY1
            and self.cleaned_data.get("subject_visit").visit_code_sequence == 0
        ):
            if self.cleaned_data.get("dosage_guideline").dose != 1000:
                raise forms.ValidationError(
                    {"dosage_guideline": f"Invalid. Expected 1000mg/day at baseline"}
                )

    @property
    def next_refill(self):
        for obj in RxRefill.objects.filter(
            rx=self.rx,
            refill_date__gt=self.cleaned_data.get("refill_date"),
        ).order_by("refill_date"):
            return obj
        return None

    @property
    def rx(self):
        return Rx.objects.get(
            subject_identifier=self.cleaned_data.get(
                "subject_visit"
            ).subject_identifier,
            medication=self.cleaned_data.get("formulation").medication,
        )


class StudyMedicationForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = StudyMedicationFormValidator

    class Meta:
        model = StudyMedication
        fields = "__all__"

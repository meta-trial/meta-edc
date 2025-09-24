import re

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import INVALID_ERROR
from edc_pharmacy.form_validators import (
    StudyMedicationFormValidator as BaseStudyMedicationFormValidator,
)
from edc_pharmacy.models import Stock
from edc_visit_schedule.constants import DAY1

from ..models import StudyMedication


class StudyMedicationFormValidator(BaseStudyMedicationFormValidator):
    def clean(self):
        super().clean()
        self.validate_half_dose_at_baseline()
        self.validate_stock_codes_are_dispensed()

    def validate_half_dose_at_baseline(self):
        """Require 1000mg dose at baseline"""
        try:
            subject_visit = (
                self.cleaned_data.get("subject_visit") or self.instance.related_visit
            )
        except AttributeError:
            self.raise_validation_error("Subject visit is required", INVALID_ERROR)
        else:
            if (
                subject_visit.visit_code == DAY1
                and subject_visit.visit_code_sequence == 0
                and (
                    self.cleaned_data.get("dosage_guideline")
                    and self.cleaned_data.get("dosage_guideline").dose != 1000
                )
            ):
                raise forms.ValidationError(
                    {"dosage_guideline": "Invalid. Expected 1000mg/day at baseline"}
                )

    def validate_stock_codes_are_dispensed(self):
        if self.cleaned_data.get("stock_codes"):
            # pattern = re.compile("^([A-Z0-9]{6})(,[A-Z0-9]{6})*$")
            pattern = re.compile("^([A-Z0-9]{6})(\r\n[A-Z0-9]{6})*$")
            if not pattern.match(self.cleaned_data.get("stock_codes")):
                raise forms.ValidationError(
                    {
                        "stock_codes": (
                            "Invalid format. Enter one or more valid codes. "
                            "One code per line only. No commas, spaces, etc"
                        )
                    }
                )
            for stock_code in self.cleaned_data.get("stock_codes").split("\r\n"):
                try:
                    Stock.objects.get(
                        code=stock_code,
                        dispenseitem__isnull=False,
                        allocation__registered_subject__subject_identifier=(
                            self.subject_identifier
                        ),
                    )
                except ObjectDoesNotExist as e:
                    raise forms.ValidationError(
                        {
                            "stock_codes": (
                                f"Invalid. Got {stock_code}. "
                                "Either not allocated to this subject or not dispensed. "
                                "Please check the bottle or check with your pharmacist."
                            )
                        }
                    ) from e


class StudyMedicationForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = StudyMedicationFormValidator

    class Meta:
        model = StudyMedication
        fields = "__all__"

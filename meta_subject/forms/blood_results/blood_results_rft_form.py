from django import forms
from django.utils.safestring import mark_safe
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_egfr.form_validator_mixins import EgfrCkdEpiFormValidatorMixin
from edc_lab_panel.panels import rft_panel
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin
from edc_registration.models import RegisteredSubject
from edc_utils import age
from edc_visit_schedule.utils import is_baseline
from edc_vitals.form_validators import BmiFormValidatorMixin

from meta_visit_schedule.constants import DAY1

from ...models import BloodResultsRft, FollowupVitals, PhysicalExam, SubjectVisit


class BloodResultsRftFormValidator(
    BloodResultsFormValidatorMixin,
    EgfrCkdEpiFormValidatorMixin,
    BmiFormValidatorMixin,
    CrfFormValidator,
):
    panel = rft_panel

    def clean(self):
        super().clean()
        self.validate_bmi()
        if self.cleaned_data.get("creatinine_value") and self.cleaned_data.get(
            "creatinine_units"
        ):

            if is_baseline(self.related_visit):
                baseline_egfr_value = None
            else:
                baseline_visit = SubjectVisit.objects.get(
                    subject_identifier=self.related_visit.subject_identifier,
                    visit_code=DAY1,
                    visit_code_sequence=0,
                )
                baseline_egfr_value = BloodResultsRft.objects.get(
                    subject_visit=baseline_visit
                ).egfr_value
            rs = RegisteredSubject.objects.get(
                subject_identifier=self.related_visit.subject_identifier
            )
            age_in_years = age(rs.dob, self.report_datetime).years

            self.validate_egfr(
                gender=rs.gender,
                age_in_years=age_in_years,
                ethnicity=rs.ethnicity,
                weight_in_kgs=self.get_weight_in_kgs(),
                baseline_egfr_value=baseline_egfr_value,
            )

    def get_weight_in_kgs(self) -> float | None:
        if is_baseline(self.related_visit):
            obj = (
                PhysicalExam.objects.filter(
                    subject_visit=self.related_visit, weight__isnull=False
                )
                .order_by("report_datetime")
                .last()
            )
        else:
            obj = (
                FollowupVitals.objects.filter(
                    subject_visit=self.related_visit, weight__isnull=False
                )
                .order_by("report_datetime")
                .last()
            )
        if obj:
            return obj.weight
        return None


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

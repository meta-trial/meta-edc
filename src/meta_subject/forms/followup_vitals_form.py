from clinicedc_constants import NO, YES
from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_visit_schedule.constants import MONTH36, MONTH48

from ..models import FollowupVitals


class FollowupVitalsFormValidator(CrfFormValidator):
    def clean(self):
        self.required_if(
            YES, field="waist_circumference_measured", field_required="waist_circumference"
        )

        visit_code = (
            f"{self.related_visit.visit_code}.{self.related_visit.visit_code_sequence}"
        )
        require_waist_circumference_comment = bool(
            visit_code in [f"{MONTH36}.0", f"{MONTH48}.0"]
            or self.cleaned_data.get("waist_circumference_measured") == YES
        )

        if (
            self.cleaned_data.get("waist_circumference_measured")
            and self.cleaned_data.get("waist_circumference_measured") == NO
        ):
            self.required_if_true(
                require_waist_circumference_comment,
                field_required="waist_circumference_comment",
            )


class FollowupVitalsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = FollowupVitalsFormValidator

    class Meta:
        model = FollowupVitals
        fields = "__all__"

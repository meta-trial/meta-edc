from django import forms
from edc_form_validators import FormValidator, FormValidatorMixin
from edc_visit_tracking.modelform_mixins import get_subject_visit

from ..models import OtherArvRegimensDetail


class OtherArvRegimensDetailFormValidator(FormValidator):
    def clean(self):
        if not self.cleaned_data.get("DELETE"):
            self.validate_other_specify(
                field="arv_regimen", other_specify_field="other_arv_regimen"
            )
            self.required_if_true(
                self.cleaned_data.get("arv_regimen"),
                field_required="arv_regimen_start_date",
            )


class InlineCrfModelFormMixin(FormValidatorMixin, forms.ModelForm):
    @property
    def subject_visit(self):
        return get_subject_visit(self, visit_model_attr=self.subject_visit_attr)

    @property
    def subject_visit_attr(self):
        return self._meta.model.visit_model_attr()


class OtherArvRegimensDetailForm(InlineCrfModelFormMixin, forms.ModelForm):

    form_validator_cls = OtherArvRegimensDetailFormValidator

    class Meta:
        model = OtherArvRegimensDetail
        fields = "__all__"

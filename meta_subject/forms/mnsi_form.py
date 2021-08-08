from django import forms
from edc_constants.constants import NO, OTHER, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import Mnsi


class MnsiFormValidator(FormValidator):
    def clean(self):
        self.required_if(
            NO,
            field="mnsi_performed",
            field_required="mnsi_not_performed_reason",
        )
        if self.cleaned_data.get("mnsi_performed") == YES:
            self.clean_physical_assessments()

    def clean_physical_assessments(self):
        for foot_choice in ["right", "left"]:
            self.applicable_if(
                YES,
                field=f"examined_{foot_choice}_foot",
                field_applicable=f"normal_appearance_{foot_choice}_foot",
            )

            self.applicable_if(
                YES,
                field=f"examined_{foot_choice}_foot",
                field_applicable=f"ulceration_{foot_choice}_foot",
            )

            self.applicable_if(
                YES,
                field=f"examined_{foot_choice}_foot",
                field_applicable=f"ankle_reflexes_{foot_choice}_foot",
            )
            self.applicable_if(
                YES,
                field=f"examined_{foot_choice}_foot",
                field_applicable=f"vibration_perception_{foot_choice}_toe",
            )
            self.applicable_if(
                YES,
                field=f"examined_{foot_choice}_foot",
                field_applicable=f"monofilament_{foot_choice}_foot",
            )

            self.m2m_required_if(
                response=NO,
                field=f"normal_appearance_{foot_choice}_foot",
                m2m_field=f"abnormal_obs_{foot_choice}_foot",
            )

            self.m2m_other_specify(
                OTHER,
                m2m_field=f"abnormal_obs_{foot_choice}_foot",
                field_other=f"abnormal_obs_{foot_choice}_foot_other",
            )


class MnsiForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = MnsiFormValidator

    class Meta:
        model = Mnsi
        fields = "__all__"

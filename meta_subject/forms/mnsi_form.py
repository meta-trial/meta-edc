from django import forms
from edc_constants.constants import NO, OTHER
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import Mnsi


class MnsiFormValidator(FormValidator):
    def clean(self):
        self.m2m_required_if(
            response=NO,
            field="normal_appearance_right_foot",
            m2m_field="abnormal_appearance_observations_right_foot",
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field="abnormal_appearance_observations_right_foot",
            field_other="abnormal_appearance_observations_right_foot_other",
        )

        self.m2m_required_if(
            response=NO,
            field="normal_appearance_left_foot",
            m2m_field="abnormal_appearance_observations_left_foot",
        )
        self.m2m_other_specify(
            OTHER,
            m2m_field="abnormal_appearance_observations_left_foot",
            field_other="abnormal_appearance_observations_left_foot_other",
        )


class MnsiForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = MnsiFormValidator

    class Meta:
        model = Mnsi
        fields = "__all__"

from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_constants.constants import NONE, OTHER, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import FollowupExamination


class FollowupExaminationFormValidator(FormValidator):
    def clean(self):

        self.validate_all_symptoms()

        self.validate_other_problems()

        self.validate_hospitalizations()

        self.validate_hiv_medications()

        self.required_if(YES, field="referral", field_required="referral_reason")

    def validate_all_symptoms(self):

        self.m2m_single_selection_if(NONE, m2m_field="symptoms")
        self.m2m_other_not_specify(NONE, m2m_field="symptoms", field_other="symptoms_detail")
        self.m2m_single_selection_if(NONE, m2m_field="symptoms_g3")
        self.m2m_single_selection_if(NONE, m2m_field="symptoms_g4")

        # G3 and G4 selections, if specified, should come from the original symptoms list
        symptoms = []
        if self.cleaned_data.get("symptoms"):
            symptoms = [
                obj.name for obj in self.cleaned_data.get("symptoms") if obj.name != NONE
            ]
        symptoms_g3 = []
        if self.cleaned_data.get("symptoms_g3"):
            symptoms_g3 = [obj.name for obj in self.cleaned_data.get("symptoms_g3")]
        symptoms_g4 = []
        if self.cleaned_data.get("symptoms_g4"):
            symptoms_g4 = [obj.name for obj in self.cleaned_data.get("symptoms_g4")]
        if symptoms_g3 != [NONE] and [x for x in symptoms_g3 if x not in symptoms]:
            raise forms.ValidationError(
                {"symptoms_g3": "Invalid selection. Must be from above list of symptoms"}
            )
        if symptoms_g4 != [NONE] and [x for x in symptoms_g4 if x not in symptoms]:
            raise forms.ValidationError(
                {"symptoms_g4": "Invalid selection. Must be from above list of symptoms"}
            )

        # provide detail always
        self.m2m_other_not_specify(
            NONE, m2m_field="symptoms_g3", field_other="symptoms_g3_detail"
        )
        # there should not be overlap between the G3 and G4 lists
        if (
            symptoms_g4 != [NONE]
            and OTHER not in symptoms_g4
            and [x for x in symptoms_g4 if x in symptoms_g3]
        ):
            raise forms.ValidationError(
                {"symptoms_g4": "Invalid selection. G3 and G4 events must be unique"}
            )
        self.m2m_other_not_specify(
            NONE, m2m_field="symptoms_g4", field_other="symptoms_g4_detail"
        )
        if (
            symptoms_g3 != [NONE]
            and OTHER not in symptoms_g3
            and [x for x in symptoms_g3 if x in symptoms_g4]
        ):
            raise forms.ValidationError(
                {"symptoms_g3": "Invalid selection. G3 and G4 events must be unique"}
            )

    def validate_other_problems(self):
        self.required_if(
            YES, field="any_other_problems", field_required="any_other_problems_detail"
        )
        self.applicable_if(
            YES,
            field="any_other_problems",
            field_applicable="any_other_problems_sae",
        )
        self.applicable_if(
            YES,
            field="any_other_problems_sae",
            field_applicable="any_other_problems_sae_grade",
        )

    def validate_hospitalizations(self):
        self.required_if(YES, field="attend_clinic", field_required="admitted_hospital")
        self.required_if(YES, field="attend_clinic", field_required="attend_clinic_details")
        self.required_if(YES, field="attend_clinic", field_required="attend_clinic_sae")
        self.required_if(YES, field="attend_clinic", field_required="prescribed_medication")
        self.required_if(
            YES,
            field="prescribed_medication",
            field_required="prescribed_medication_detail",
        )

    def validate_hiv_medications(self):
        self.required_if(YES, field="art_change", field_required="art_change_reason")
        self.required_if(YES, field="art_change", field_required="art_new_regimen")
        self.validate_other_specify(
            field="art_new_regimen", other_specify_field="art_new_regimen_other"
        )


class FollowupExaminationForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):

    form_validator_cls = FollowupExaminationFormValidator

    class Meta:
        model = FollowupExamination
        fields = "__all__"

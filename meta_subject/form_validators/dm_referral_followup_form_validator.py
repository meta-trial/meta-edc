from django import forms
from edc_constants.constants import NO, OTHER, YES
from edc_crf.crf_form_validator import CrfFormValidator


class DmReferralFollowupFormValidator(CrfFormValidator):
    def clean(self):
        # Diabetes clinic attendance
        self.required_if(
            NO,
            field="attended",
            field_required="not_attended_reason",
        )
        self.required_if(
            YES,
            field="attended",
            field_required="facility_attended",
        )
        self.required_if(
            YES,
            field="attended",
            field_required="attended_date",
        )
        self.m2m_required_if(
            YES,
            field="attended",
            m2m_field="healthcare_workers",
        )
        self.m2m_other_specify(
            OTHER,
            m2m_field="healthcare_workers",
            field_other="other_healthcare_workers",
        )

        # investigations
        self.m2m_required_if(
            NO,
            field="investigations_performed",
            m2m_field="investigations",
        )
        self.m2m_other_specify(
            OTHER,
            m2m_field="investigations_performed",
            field_other="other_investigations",
        )
        self.m2m_required_if(
            NO,
            field="complications_checks_performed",
            m2m_field="complications_checks",
        )
        self.m2m_other_specify(
            OTHER,
            m2m_field="complications_checks",
            field_other="other_complications_checks",
        )

        # dm treatment
        self.applicable_if(
            YES,
            field="attended",
            field_applicable="treatment_prescribed",
        )
        self.m2m_required_if(
            YES,
            field="treatment_prescribed",
            m2m_field="dm_treatments",
        )
        self.applicable_if(
            YES,
            field="treatment_prescribed",
            field_applicable="on_dm_medications",
        )
        self.required_if(
            YES,
            field="on_dm_medications",
            field_required="on_dm_medications_init_date",
        )
        self.m2m_required_if(
            YES,
            field="on_dm_medications",
            m2m_field="dm_medications",
        )
        self.m2m_other_specify(
            OTHER,
            m2m_field="dm_medications",
            field_other="other_dm_medications",
        )

        # Diabetes Medication Adherence
        self.applicable_if(
            YES,
            field="on_dm_medications",
            field_applicable="medications_adherent",
        )
        self.required_if(
            YES,
            field="on_dm_medications",
            field_required="last_pill_missed",
        )

        self.confirm_visual_scores_match()

    def confirm_visual_scores_match(self) -> None:
        self.required_if(
            YES,
            field="on_dm_medications",
            field_required="visual_score_slider",
        )
        self.required_if(
            YES,
            field="on_dm_medications",
            field_required="visual_score_confirmed",
        )
        if (
            self.cleaned_data.get("on_dm_medications")
            and self.cleaned_data.get("on_dm_medications") == YES
        ):
            confirmed = self.cleaned_data.get("visual_score_confirmed")
            if confirmed is not None:
                if int(self.cleaned_data.get("visual_score_slider", "0")) != confirmed:
                    raise forms.ValidationError(
                        {"visual_score_confirmed": "Does not match visual score above."}
                    )

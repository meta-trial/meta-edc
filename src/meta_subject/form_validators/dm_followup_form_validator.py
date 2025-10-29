from clinicedc_constants import NO, OTHER, YES
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_crf.crf_form_validator import CrfFormValidator
from edc_form_validators import INVALID_ERROR
from edc_utils import formatted_date
from edc_utils.date import to_local

from meta_prn.models import DmReferral


class DmFollowupFormValidator(CrfFormValidator):
    def clean(self):
        # referral_date must be before report datetime
        if (
            self.report_datetime
            and self.cleaned_data.get("referral_date")
            and self.cleaned_data.get("referral_date") >= to_local(self.report_datetime).date()
        ):
            self.raise_validation_error(
                {"referral_date": "Invalid. Expected a date prior to the report date above."},
                INVALID_ERROR,
            )

        # try to match referral date to the referal form
        try:
            dm_referral = DmReferral.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            self.raise_validation_error(
                {"__all__": "Original Referral form not found."}, INVALID_ERROR
            )
        else:
            if dm_referral.referral_date != self.cleaned_data.get("referral_date"):
                referral_dt = formatted_date(dm_referral.referral_date)
                report_dt = formatted_date(to_local(dm_referral.report_datetime).date())
                self.raise_validation_error(
                    {
                        "referral_date": (
                            f"Invalid. Expected `{referral_dt}` "
                            f"based on the referral form submitted on {report_dt}."
                        )
                    },
                    INVALID_ERROR,
                )

        # Diabetes clinic attendance
        self.m2m_required_if(
            NO,
            field="attended",
            m2m_field="missed_referral_reasons",
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field="missed_referral_reasons",
            field_other="other_missed_referral_reason",
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

        # attended_date cannot be future relative to report datetime
        if (
            self.report_datetime
            and self.cleaned_data.get("attended_date")
            and self.cleaned_data.get("attended_date") > to_local(self.report_datetime).date()
        ):
            self.raise_validation_error(
                {"attended_date": "Invalid. Cannot be after report date above"}, INVALID_ERROR
            )

        # referral_date must be before report datetime
        if (
            self.cleaned_data.get("attended_date")
            and self.cleaned_data.get("referral_date")
            and self.cleaned_data.get("attended_date") < self.cleaned_data.get("referral_date")
        ):
            self.raise_validation_error(
                {"attended_date": "Invalid. Cannot be before the referral date"},
                INVALID_ERROR,
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

        self.applicable_if(
            YES,
            field="attended",
            field_applicable="investigations_performed",
        )

        # investigations
        self.m2m_required_if(
            YES,
            field="investigations_performed",
            m2m_field="investigations",
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field="investigations",
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
            field_required="dm_medications_init_date",
        )

        # dm_medications_init_date must be before report_datetime
        if (
            self.report_datetime
            and self.cleaned_data.get("dm_medications_init_date")
            and self.cleaned_data.get("dm_medications_init_date")
            > to_local(self.report_datetime).date()
        ):
            self.raise_validation_error(
                {"dm_medications_init_date": "Invalid. Cannot be after the report date"},
                INVALID_ERROR,
            )

        # dm_medications_init_date must be after referral_date
        if self.cleaned_data.get("dm_medications_init_date") and self.cleaned_data.get(
            "dm_medications_init_date"
        ) < self.cleaned_data.get("referral_date"):
            self.raise_validation_error(
                {"dm_medications_init_date": "Invalid. Cannot be before the referral date"},
                INVALID_ERROR,
            )

        # dm_medications_init_date must be on or after attended_date
        if self.cleaned_data.get("dm_medications_init_date") and self.cleaned_data.get(
            "dm_medications_init_date"
        ) < self.cleaned_data.get("attended_date"):
            self.raise_validation_error(
                {
                    "dm_medications_init_date": (
                        "Invalid. Expected a date on or after date patient "
                        "attended the health facility."
                    )
                },
                INVALID_ERROR,
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
            field_required="last_missed_pill",
        )

        self.confirm_visual_scores_match()

    def confirm_visual_scores_match(self) -> None:
        self.required_if(
            YES,
            field="on_dm_medications",
            field_required="visual_score_slider",
            inverse=False,
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
            if (
                confirmed is not None
                and int(self.cleaned_data.get("visual_score_slider", "0")) != confirmed
            ):
                raise forms.ValidationError(
                    {"visual_score_confirmed": "Does not match visual score above."}
                )

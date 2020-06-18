from edc_adverse_event.constants import AE_INITIAL_ACTION
from edc_action_item import Action, site_action_items
from edc_constants.constants import NONE, YES, HIGH_PRIORITY
from edc_reportable import GRADE3, GRADE4
from meta_visit_schedule.constants import DAY1

from .constants import (
    BLOOD_RESULTS_FBC_ACTION,
    BLOOD_RESULTS_GLU_ACTION,
    BLOOD_RESULTS_LIPID_ACTION,
    BLOOD_RESULTS_LFT_ACTION,
    BLOOD_RESULTS_RFT_ACTION,
    BLOOD_RESULTS_HBA1C_ACTION,
    BLOOD_RESULTS_EGFR_ACTION,
    FOLLOWUP_EXAMINATION_ACTION,
)


def is_baseline(action):
    return action.reference_obj.subject_visit.appointment.visit_code == DAY1


class FollowupExaminationAction(Action):
    name = FOLLOWUP_EXAMINATION_ACTION
    priority = HIGH_PRIORITY
    display_name = "Followup Exam: AE"
    reference_model = "meta_subject.followupexamination"
    show_on_dashboard = True
    create_by_user = False

    def get_next_actions(self):
        next_actions = []
        if (
            self.reference_obj.symptoms_g3.exclude(name=NONE).count() > 0
            or self.reference_obj.symptoms_g4.exclude(name=NONE).count() > 0
            or self.reference_obj.any_other_problems_sae_grade in [GRADE3, GRADE4]
        ) and not is_baseline(self):
            next_actions.append(AE_INITIAL_ACTION)
        return next_actions


class BaseBloodResultsAction(Action):
    name = None
    display_name = None
    reference_model = None

    priority = HIGH_PRIORITY
    show_on_dashboard = True
    create_by_user = False

    def reopen_action_item_on_change(self):
        return False

    def get_next_actions(self):
        next_actions = []
        if (
            self.reference_obj.results_abnormal == YES
            and self.reference_obj.results_reportable == YES
            and not is_baseline(self)
        ):
            # AE for reportable result, though not on DAY1.0
            next_actions = [AE_INITIAL_ACTION]
        return next_actions


class BloodResultsLftAction(BaseBloodResultsAction):
    name = BLOOD_RESULTS_LFT_ACTION
    display_name = "Reportable result: LFT"
    reference_model = "meta_subject.bloodresultslft"


class BloodResultsRftAction(BaseBloodResultsAction):
    name = BLOOD_RESULTS_RFT_ACTION
    display_name = "Reportable result: RFT"
    reference_model = "meta_subject.bloodresultsrft"


class BloodResultsFbcAction(BaseBloodResultsAction):
    name = BLOOD_RESULTS_FBC_ACTION
    display_name = "Reportable result: FBC"
    reference_model = "meta_subject.bloodresultsfbc"


class BloodResultsLipidAction(BaseBloodResultsAction):
    name = BLOOD_RESULTS_LIPID_ACTION
    display_name = "Reportable result: LIPIDS"
    reference_model = "meta_subject.bloodresultslipid"


class BloodResultsEgfrAction(BaseBloodResultsAction):
    name = BLOOD_RESULTS_EGFR_ACTION
    display_name = "Reportable eGFR"
    reference_model = "meta_subject.bloodresultsfbc"


class BloodResultsGluAction(BaseBloodResultsAction):
    name = BLOOD_RESULTS_GLU_ACTION
    display_name = "Reportable Blood Glucose"
    reference_model = "meta_subject.bloodresultsglu"


class BloodResultsHba1cAction(BaseBloodResultsAction):
    name = BLOOD_RESULTS_HBA1C_ACTION
    display_name = "Reportable HbA1c"
    reference_model = "meta_subject.bloodresultshba1c"


site_action_items.register(BloodResultsFbcAction)
site_action_items.register(BloodResultsEgfrAction)
site_action_items.register(BloodResultsLipidAction)
site_action_items.register(BloodResultsLftAction)
site_action_items.register(BloodResultsRftAction)
site_action_items.register(BloodResultsGluAction)
site_action_items.register(BloodResultsHba1cAction)
site_action_items.register(FollowupExaminationAction)

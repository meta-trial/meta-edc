from edc_action_item import Action, site_action_items
from edc_adverse_event.constants import AE_INITIAL_ACTION
from edc_blood_results.action_items import (
    BloodResultsEgfrAction,
    BloodResultsFbcAction,
    BloodResultsGluAction,
    BloodResultsHba1cAction,
    BloodResultsLftAction,
    BloodResultsLipidAction,
    BloodResultsRftAction,
)
from edc_constants.constants import HIGH_PRIORITY, NONE
from edc_reportable import GRADE3, GRADE4
from edc_visit_schedule.utils import is_baseline

from .constants import FOLLOWUP_EXAMINATION_ACTION


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
        ) and not is_baseline(self.reference_obj.subject_visit):
            next_actions.append(AE_INITIAL_ACTION)
        return next_actions


site_action_items.register(BloodResultsFbcAction)
site_action_items.register(BloodResultsEgfrAction)
site_action_items.register(BloodResultsLipidAction)
site_action_items.register(BloodResultsLftAction)
site_action_items.register(BloodResultsRftAction)
site_action_items.register(BloodResultsGluAction)
site_action_items.register(BloodResultsHba1cAction)
site_action_items.register(FollowupExaminationAction)

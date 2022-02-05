from edc_action_item import Action, site_action_items
from edc_action_item.site_action_items import AlreadyRegistered
from edc_adverse_event.constants import AE_INITIAL_ACTION
from edc_blood_results.action_items import (
    BloodResultsFbcAction,
    BloodResultsGluAction,
    BloodResultsHba1cAction,
    BloodResultsLftAction,
    BloodResultsLipidAction,
)
from edc_blood_results.action_items import (
    BloodResultsRftAction as BaseBloodResultsRftAction,
)
from edc_constants.constants import HIGH_PRIORITY, NONE, YES
from edc_ltfu.constants import LTFU_ACTION
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_reportable import GRADE3, GRADE4
from edc_visit_schedule.utils import is_baseline

from .constants import FOLLOWUP_EXAMINATION_ACTION, MISSED_VISIT_ACTION


class MissedVisitAction(Action):
    name = MISSED_VISIT_ACTION
    priority = HIGH_PRIORITY
    display_name = "Missed Visits: LTFU"
    reference_model = "meta_subject.subjectvisitmissed"
    show_on_dashboard = True
    create_by_user = False

    def get_next_actions(self):
        # TODO: define LTFU, 6 months off study medication
        ltfu = None
        if ltfu:
            next_actions = [LTFU_ACTION]
        return next_actions

    # def ltfu(self):
    #     if self.reference_model_cls().objects.all().count() == 3:
    #         return True
    #     return None


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
            or self.reference_obj.lactic_acidosis == YES
            or self.reference_obj.hepatomegaly == YES
        ) and not is_baseline(self.reference_obj.subject_visit):
            next_actions.append(AE_INITIAL_ACTION)
        return next_actions


class BloodResultsRftAction(BaseBloodResultsRftAction):
    def get_next_actions(self):
        next_actions = super().get_next_actions()
        if (
            self.reference_obj.egfr_value is not None
            and self.reference_obj.egfr_value < 45.0
        ):
            next_actions = [END_OF_STUDY_ACTION]
        return next_actions


def register_actions():
    for action_item_cls in [
        BloodResultsFbcAction,
        BloodResultsLipidAction,
        BloodResultsLftAction,
        BloodResultsRftAction,
        BloodResultsGluAction,
        BloodResultsHba1cAction,
        FollowupExaminationAction,
        MissedVisitAction,
    ]:
        try:
            site_action_items.register(action_item_cls)
        except AlreadyRegistered:
            pass


register_actions()

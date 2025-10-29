from clinicedc_constants import GRADE3, GRADE4, HIGH_PRIORITY, NEW, NONE, POS, YES
from django.apps import apps as django_apps
from edc_action_item.action import Action
from edc_action_item.action_with_notification import ActionWithNotification
from edc_action_item.site_action_items import AlreadyRegistered, site_action_items
from edc_adverse_event.constants import AE_INITIAL_ACTION
from edc_egfr.constants import EGFR_DROP_NOTIFICATION_ACTION
from edc_lab_results.action_items import (
    BloodResultsFbcAction,
    BloodResultsHba1cAction,
    BloodResultsLftAction,
    BloodResultsLipidsAction,
)
from edc_lab_results.action_items import (
    BloodResultsGluAction as BaseBloodResultsGluAction,
)
from edc_lab_results.action_items import (
    BloodResultsRftAction as BaseBloodResultsRftAction,
)
from edc_ltfu.constants import LTFU_ACTION
from edc_visit_schedule.constants import OFFSCHEDULE_ACTION
from edc_visit_schedule.utils import is_baseline
from edc_visit_tracking.constants import MISSED_VISIT

from meta_prn.constants import (
    DM_REFFERAL_ACTION,
    OFFSCHEDULE_DM_REFERRAL_ACTION,
    OFFSCHEDULE_PREGNANCY_ACTION,
    PREGNANCY_NOTIFICATION_ACTION,
)

from .constants import (
    DELIVERY_ACTION,
    DM_FOLLOWUP_ACTION,
    FOLLOWUP_EXAMINATION_ACTION,
    MISSED_VISIT_ACTION,
    URINE_PREGNANCY_ACTION,
)


class MissedVisitAction(Action):
    name = MISSED_VISIT_ACTION
    priority = HIGH_PRIORITY
    display_name = "Missed Visits: LTFU"
    reference_model = "meta_subject.subjectvisitmissed"
    show_on_dashboard = True
    create_by_user = False

    def get_next_actions(self):
        """LTFU, 6 months off study medication using
        diff of report_datetime and refill_end_datetime.
        """
        next_actions = []
        subject_visit_model_cls = django_apps.get_model("meta_subject.subjectvisit")
        study_medication_model_cls = django_apps.get_model("meta_subject.studymedication")
        last_visit = (
            subject_visit_model_cls.objects.filter(subject_identifier=self.subject_identifier)
            .exclude(reason=MISSED_VISIT)
            .order_by("report_datetime")
            .last()
        )
        last_study_medication = (
            study_medication_model_cls.objects.filter(
                subject_visit__subject_identifier=self.subject_identifier
            )
            .order_by("refill_end_datetime")
            .last()
        )
        if (
            last_visit
            and last_study_medication
            and last_study_medication.refill_end_datetime
            and (last_study_medication.refill_end_datetime - last_visit.report_datetime).days
            >= 182
        ):
            next_actions = [LTFU_ACTION]
        return next_actions


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
            or YES in (self.reference_obj.lactic_acidosis, self.reference_obj.hepatomegaly)
        ) and not is_baseline(instance=self.reference_obj.subject_visit):
            next_actions.append(AE_INITIAL_ACTION)
        return next_actions


class UrinePregnancyAction(Action):
    name = URINE_PREGNANCY_ACTION
    priority = HIGH_PRIORITY
    display_name = "Urine Pregnancy Test"
    reference_model = "meta_subject.urinepregnancy"
    show_on_dashboard = True
    create_by_user = False

    def get_next_actions(self):
        next_actions = []
        if (self.reference_obj.bhcg_value == POS) and not is_baseline(
            instance=self.reference_obj.subject_visit
        ):
            next_actions.append(PREGNANCY_NOTIFICATION_ACTION)
        return next_actions


class BloodResultsRftAction(BaseBloodResultsRftAction):
    reference_model = "meta_subject.bloodresultsrft"

    def get_next_actions(self):
        next_actions = super().get_next_actions()
        if self.reference_obj.egfr_value is not None and self.reference_obj.egfr_value < 45.0:
            next_actions.append(OFFSCHEDULE_ACTION)
        return next_actions


class BloodResultsGluAction(BaseBloodResultsGluAction):
    reference_model = "meta_subject.bloodresultsgludummy"


class DeliveryAction(ActionWithNotification):
    name = DELIVERY_ACTION
    display_name = "Submit Delivery Form"
    notification_display_name = "Delivery Form"
    parent_action_names = (PREGNANCY_NOTIFICATION_ACTION,)
    reference_model = "meta_subject.delivery"
    show_link_to_changelist = True
    show_link_to_add = False
    admin_site_name = "meta_subject_admin"
    priority = HIGH_PRIORITY

    def get_next_actions(self):
        return [OFFSCHEDULE_PREGNANCY_ACTION]


class EgfrDropNotificationAction(ActionWithNotification):
    name = EGFR_DROP_NOTIFICATION_ACTION
    display_name = "eGFR drop warning"
    notification_display_name = "eGFR drop warning"
    parent_action_names = ()
    reference_model = "meta_subject.egfrdropnotification"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "meta_subject_admin"
    priority = HIGH_PRIORITY

    def close_action_item_on_save(self) -> bool:
        return self.reference_obj.report_status != NEW


class DmFollowAction(ActionWithNotification):
    name = DM_FOLLOWUP_ACTION
    display_name = "Diabetes Followup"
    notification_display_name = "Diabetes Followup"
    parent_action_names = (DM_REFFERAL_ACTION,)
    reference_model = "meta_subject.dmfollowup"
    show_link_to_changelist = True
    show_link_to_add = False
    show_on_dashboard = False
    create_by_user = False
    create_by_action = True
    admin_site_name = "meta_subject_admin"
    priority = HIGH_PRIORITY

    def get_next_actions(self):
        return [OFFSCHEDULE_DM_REFERRAL_ACTION]


def register_actions():
    for action_item_cls in [
        BloodResultsFbcAction,
        BloodResultsLipidsAction,
        BloodResultsLftAction,
        BloodResultsRftAction,
        BloodResultsHba1cAction,
        FollowupExaminationAction,
        MissedVisitAction,
        UrinePregnancyAction,
        DeliveryAction,
        EgfrDropNotificationAction,
        DmFollowAction,
    ]:
        try:
            site_action_items.register(action_item_cls)
        except AlreadyRegistered:
            del site_action_items.registry[action_item_cls.name]
            site_action_items.register(action_item_cls)


register_actions()

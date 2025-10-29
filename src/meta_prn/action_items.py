from clinicedc_constants import HIGH_PRIORITY, NOT_SURE, TBD, YES
from django.apps import apps as django_apps
from django.utils.safestring import mark_safe
from edc_action_item.action_with_notification import ActionWithNotification
from edc_action_item.site_action_items import site_action_items
from edc_adverse_event.constants import DEATH_REPORT_ACTION
from edc_lab_results import BLOOD_RESULTS_RFT_ACTION
from edc_ltfu.constants import LTFU_ACTION
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_protocol_incident.action_items import (
    ProtocolIncidentAction as BaseProtocolIncidentAction,
)
from edc_transfer.action_items import SubjectTransferAction as BaseSubjectTransferAction
from edc_transfer.constants import SUBJECT_TRANSFER_ACTION
from edc_visit_schedule.constants import OFFSCHEDULE_ACTION

from meta_subject.constants import (
    DELIVERY_ACTION,
    DM_FOLLOWUP_ACTION,
    MISSED_VISIT_ACTION,
    URINE_PREGNANCY_ACTION,
)

from .constants import (
    DM_REFFERAL_ACTION,
    OFFSCHEDULE_DM_REFERRAL_ACTION,
    OFFSCHEDULE_PREGNANCY_ACTION,
    OFFSTUDY_MEDICATION_ACTION,
    PREGNANCY_NOTIFICATION_ACTION,
    REFERRAL,
    UNBLINDING_REQUEST_ACTION,
    UNBLINDING_REVIEW_ACTION,
)
from .pregnancy_action_item_mixin import PregnancyActionItemMixin


class OffscheduleAction(ActionWithNotification):
    name = OFFSCHEDULE_ACTION
    display_name = "Submit Off-Schedule"
    notification_display_name = "Off-Schedule"
    parent_action_names = (
        UNBLINDING_REVIEW_ACTION,
        DEATH_REPORT_ACTION,
        LTFU_ACTION,
        BLOOD_RESULTS_RFT_ACTION,
        SUBJECT_TRANSFER_ACTION,
    )
    reference_model = "meta_prn.offschedule"
    show_link_to_changelist = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        pregnancy_notification = (
            django_apps.get_model("meta_prn.pregnancynotification")
            .objects.filter(subject_identifier=self.subject_identifier)
            .last()
        )

        if pregnancy_notification and pregnancy_notification.may_contact in [YES, NOT_SURE]:
            next_actions = [OFFSTUDY_MEDICATION_ACTION]
        else:
            next_actions = [OFFSTUDY_MEDICATION_ACTION]
        return next_actions


class OffschedulePregnancyAction(ActionWithNotification):
    name = OFFSCHEDULE_PREGNANCY_ACTION
    display_name = "Submit Off-Schedule (Pregnancy)"
    notification_display_name = "Off-Schedule (Pregnancy)"
    parent_action_names = (
        UNBLINDING_REVIEW_ACTION,
        DEATH_REPORT_ACTION,
        LTFU_ACTION,
        SUBJECT_TRANSFER_ACTION,
        DELIVERY_ACTION,
    )
    reference_model = "meta_prn.offschedulepregnancy"
    show_link_to_changelist = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        return [END_OF_STUDY_ACTION]


class OffscheduleDmReferralAction(ActionWithNotification):
    name = OFFSCHEDULE_DM_REFERRAL_ACTION
    display_name = "Submit Off-Schedule (Diabetes Referral)"
    notification_display_name = "Off-Schedule (Diabetes Referral)"
    parent_action_names = (
        DM_FOLLOWUP_ACTION,
        DEATH_REPORT_ACTION,
        LTFU_ACTION,
        SUBJECT_TRANSFER_ACTION,
    )
    reference_model = "meta_prn.offscheduledmreferral"
    show_link_to_changelist = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        return [END_OF_STUDY_ACTION]


class EndOfStudyAction(ActionWithNotification):
    name = END_OF_STUDY_ACTION
    display_name = "Submit End of Study Report"
    notification_display_name = "End of Study Report"
    parent_action_names = (
        OFFSCHEDULE_ACTION,
        OFFSTUDY_MEDICATION_ACTION,
        OFFSCHEDULE_PREGNANCY_ACTION,
        OFFSCHEDULE_DM_REFERRAL_ACTION,
    )
    reference_model = "meta_prn.endofstudy"
    show_link_to_changelist = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True


class LossToFollowupAction(PregnancyActionItemMixin, ActionWithNotification):
    name = LTFU_ACTION
    display_name = "Submit Loss to Follow Up Report"
    notification_display_name = " Loss to Follow Up Report"
    parent_action_names = (MISSED_VISIT_ACTION,)
    reference_model = "meta_prn.losstofollowup"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        return [self.get_next_offschedule_action(), OFFSTUDY_MEDICATION_ACTION]


class PregnancyNotificationAction(ActionWithNotification):
    name = PREGNANCY_NOTIFICATION_ACTION
    display_name = "Submit Pregnancy Notification"
    notification_display_name = "Pregnancy Notification"
    parent_action_names = (URINE_PREGNANCY_ACTION,)
    reference_model = "meta_prn.pregnancynotification"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY


class DmReferralAction(ActionWithNotification):
    """Action to put subject on dm_referral schedule"""

    name = DM_REFFERAL_ACTION
    display_name = "Diabetes referral"
    notification_display_name = "Diabetes referral"
    parent_action_names = (OFFSTUDY_MEDICATION_ACTION,)
    reference_model = "meta_prn.dmreferral"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        return [DM_FOLLOWUP_ACTION]


class OffStudyMedicationAction(ActionWithNotification):
    name = OFFSTUDY_MEDICATION_ACTION
    display_name = "Withdrawal Study Medication"
    notification_display_name = "Withdrawal Study Medication"
    parent_action_names = (
        OFFSCHEDULE_ACTION,
        LTFU_ACTION,
        SUBJECT_TRANSFER_ACTION,
        DEATH_REPORT_ACTION,
    )
    reference_model = "meta_prn.offstudymedication"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        if self.reference_obj.reason == REFERRAL:
            next_actions = [DM_REFFERAL_ACTION]
        else:
            next_actions = [END_OF_STUDY_ACTION]
        return next_actions


class UnblindingRequestAction(ActionWithNotification):
    name = UNBLINDING_REQUEST_ACTION
    display_name = "Unblinding request"
    notification_display_name = " Unblinding request"
    parent_action_names = ()
    reference_model = "edc_unblinding.unblindingrequest"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "edc_unblinding_admin"
    priority = HIGH_PRIORITY

    def get_next_actions(self):
        return self.append_to_next_if_required(
            next_actions=[],
            action_name=UNBLINDING_REVIEW_ACTION,
            required=self.reference_obj.approved == TBD,
        )


class UnblindingReviewAction(PregnancyActionItemMixin, ActionWithNotification):
    name = UNBLINDING_REVIEW_ACTION
    display_name = "Unblinding review pending"
    notification_display_name = " Unblinding review needed"
    parent_action_names = (UNBLINDING_REQUEST_ACTION,)
    reference_model = "edc_unblinding.unblindingreview"
    show_link_to_changelist = True
    admin_site_name = "edc_unblinding_admin"
    priority = HIGH_PRIORITY
    color_style = "info"
    create_by_user = False
    instructions = mark_safe(  # nosec B308
        "This report is to be completed by the UNBLINDING REVIEWERS only."
    )

    def get_next_actions(self):
        return self.append_to_next_if_required(
            next_actions=[],
            action_name=self.get_next_offschedule_action(),
            required=self.reference_obj.approved == YES,
        )


class SubjectTransferAction(PregnancyActionItemMixin, BaseSubjectTransferAction):
    reference_model = "meta_prn.subjecttransfer"
    admin_site_name = "meta_prn_admin"

    def get_next_actions(self):
        return [self.get_next_offschedule_action(), OFFSTUDY_MEDICATION_ACTION]


class ProtocolIncidentAction(BaseProtocolIncidentAction):
    reference_model = "meta_prn.protocolincident"
    admin_site_name = "meta_prn_admin"


site_action_items.register(EndOfStudyAction)
site_action_items.register(LossToFollowupAction)
site_action_items.register(OffscheduleAction)
site_action_items.register(OffschedulePregnancyAction)
site_action_items.register(PregnancyNotificationAction)
site_action_items.register(ProtocolIncidentAction)
site_action_items.register(SubjectTransferAction)
site_action_items.register(UnblindingRequestAction)
site_action_items.register(UnblindingReviewAction)
site_action_items.register(OffStudyMedicationAction)
site_action_items.register(DmReferralAction)
site_action_items.register(OffscheduleDmReferralAction)

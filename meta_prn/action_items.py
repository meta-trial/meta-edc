from django.utils.safestring import mark_safe
from edc_action_item.action_with_notification import ActionWithNotification
from edc_action_item.site_action_items import site_action_items
from edc_adverse_event.constants import DEATH_REPORT_ACTION
from edc_constants.constants import HIGH_PRIORITY, TBD, YES
from edc_ltfu.constants import LTFU_ACTION
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_prn.action_items import (
    ProtocolDeviationViolationAction as BaseProtocolDeviationViolationAction,
)

from .constants import UNBLINDING_REQUEST_ACTION, UNBLINDING_REVIEW_ACTION


class EndOfStudyAction(ActionWithNotification):
    name = END_OF_STUDY_ACTION
    display_name = "Submit End of Study Report"
    notification_display_name = "End of Study Report"
    parent_action_names = [
        UNBLINDING_REVIEW_ACTION,
        DEATH_REPORT_ACTION,
        LTFU_ACTION,
    ]
    reference_model = "meta_prn.endofstudy"
    show_link_to_changelist = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY


class LossToFollowupAction(ActionWithNotification):
    name = LTFU_ACTION
    display_name = "Submit Loss to Follow Up Report"
    notification_display_name = " Loss to Follow Up Report"
    parent_action_names = []
    reference_model = "meta_prn.losstofollowup"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY

    def get_next_actions(self):
        next_actions = [END_OF_STUDY_ACTION]
        return next_actions


class UnblindingRequestAction(ActionWithNotification):
    name = UNBLINDING_REQUEST_ACTION
    display_name = "Unblinding request"
    notification_display_name = " Unblinding request"
    parent_action_names = []
    reference_model = "meta_prn.unblindingrequest"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY

    def get_next_actions(self):
        next_actions = []
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=UNBLINDING_REVIEW_ACTION,
            required=self.reference_obj.approved == TBD,
        )
        return next_actions


class UnblindingReviewAction(ActionWithNotification):
    name = UNBLINDING_REVIEW_ACTION
    display_name = "Unblinding review pending"
    notification_display_name = " Unblinding review needed"
    parent_action_names = [UNBLINDING_REQUEST_ACTION]
    reference_model = "meta_prn.unblindingreview"
    show_link_to_changelist = True
    admin_site_name = "meta_prn_admin"
    priority = HIGH_PRIORITY
    color_style = "info"
    create_by_user = False
    instructions = mark_safe(
        "This report is to be completed by the UNBLINDING REVIEWERS only."
    )

    def get_next_actions(self):
        next_actions = []
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=END_OF_STUDY_ACTION,
            required=self.reference_obj.approved == YES,
        )
        return next_actions


class ProtocolDeviationViolationAction(BaseProtocolDeviationViolationAction):
    reference_model = "meta_prn.protocoldeviationviolation"
    admin_site_name = "meta_prn_admin"


site_action_items.register(ProtocolDeviationViolationAction)
site_action_items.register(EndOfStudyAction)
site_action_items.register(LossToFollowupAction)
site_action_items.register(UnblindingRequestAction)
site_action_items.register(UnblindingReviewAction)

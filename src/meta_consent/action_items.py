from clinicedc_constants import HIGH_PRIORITY
from edc_action_item.action import Action
from edc_action_item.site_action_items import site_action_items

from .constants import CONSENT_V1_EXTENSION_ACTION, RECONSENT_ACTION


class ReconsentAction(Action):
    name = RECONSENT_ACTION
    display_name = "Re-consent participant"
    reference_model = "meta_consent.subjectreconsent"
    priority = HIGH_PRIORITY
    show_on_dashboard = True
    show_link_to_changelist = True
    admin_site_name = "meta_consent_admin"
    create_by_user = False
    singleton = True
    instructions = (
        "Participant must be re-consented as soon as able. "
        "Participant's ICF was initially completed by next-of-kin."
    )

    def reopen_action_item_on_change(self):
        return False


class ConsentV1ExtensionAction(Action):
    name = CONSENT_V1_EXTENSION_ACTION
    display_name = "Ask to extend followup (required)"
    reference_model = "meta_consent.subjectconsentv1ext"
    priority = HIGH_PRIORITY
    show_on_dashboard = True
    show_link_to_changelist = True
    admin_site_name = "meta_consent_admin"
    show_link_to_add = True
    create_by_user = True
    singleton = True
    instructions = "Participant must complete as soon as able. "

    def reopen_action_item_on_change(self):
        return False


site_action_items.register(ReconsentAction)
site_action_items.register(ConsentV1ExtensionAction)

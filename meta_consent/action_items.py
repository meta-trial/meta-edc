from edc_action_item import Action, site_action_items
from edc_constants.constants import HIGH_PRIORITY

from .constants import RECONSENT_ACTION


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


site_action_items.register(ReconsentAction)

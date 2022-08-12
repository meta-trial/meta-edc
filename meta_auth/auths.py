from edc_action_item.auth_objects import (
    ACTION_ITEM,
    ACTION_ITEM_EXPORT,
    ACTION_ITEM_VIEW_ONLY,
)
from edc_adverse_event.auth_objects import AE, AE_REVIEW, AE_SUPER, TMG_REVIEW, TMG_ROLE
from edc_appointment.auth_objects import (
    APPOINTMENT,
    APPOINTMENT_EXPORT,
    APPOINTMENT_VIEW,
)
from edc_auth.auth_objects import (
    AUDITOR,
    AUDITOR_ROLE,
    CLINIC,
    CLINIC_SUPER,
    CLINICIAN_ROLE,
    CLINICIAN_SUPER_ROLE,
    NURSE_ROLE,
    PII,
)
from edc_auth.site_auths import site_auths
from edc_data_manager.auth_objects import DATA_MANAGER_EXPORT
from edc_export.auth_objects import DATA_EXPORTER_ROLE
from edc_mnsi.auth_objects import MNSI, MNSI_SUPER, MNSI_VIEW
from edc_pharmacy.auth_objects import (
    PHARMACIST_ROLE,
    PRESCRIBER_ROLE,
    SITE_PHARMACIST_ROLE,
)
from edc_qol.auth_objects import QOL, QOL_SUPER, QOL_VIEW
from edc_randomization.auth_objects import RANDO_BLINDED, RANDO_UNBLINDED
from edc_unblinding.auth_objects import UNBLINDING_REQUESTORS

from .auth_objects import clinic_codenames

site_auths.update_group(*clinic_codenames, name=AUDITOR, view_only=True)
site_auths.update_group(*clinic_codenames, name=CLINIC, no_delete=True)
site_auths.update_group(*clinic_codenames, name=CLINIC_SUPER)

# update edc roles
site_auths.update_role(
    ACTION_ITEM,
    AE,
    APPOINTMENT,
    CLINIC,
    UNBLINDING_REQUESTORS,
    MNSI,
    QOL,
    PRESCRIBER_ROLE,
    name=CLINICIAN_ROLE,
)

site_auths.update_role(
    ACTION_ITEM,
    AE_SUPER,
    APPOINTMENT,
    CLINIC_SUPER,
    MNSI_SUPER,
    QOL_SUPER,
    UNBLINDING_REQUESTORS,
    PRESCRIBER_ROLE,
    name=CLINICIAN_SUPER_ROLE,
)

site_auths.update_role(
    ACTION_ITEM,
    AE,
    APPOINTMENT,
    CLINIC,
    MNSI,
    QOL,
    name=NURSE_ROLE,
)


site_auths.update_role(ACTION_ITEM, UNBLINDING_REQUESTORS, name=TMG_ROLE)

site_auths.update_role(
    ACTION_ITEM_VIEW_ONLY,
    AE_REVIEW,
    APPOINTMENT_VIEW,
    AUDITOR,
    MNSI_VIEW,
    QOL_VIEW,
    TMG_REVIEW,
    name=AUDITOR_ROLE,
)


# data export
site_auths.update_role(
    ACTION_ITEM_EXPORT,
    APPOINTMENT_EXPORT,
    DATA_MANAGER_EXPORT,
    name=DATA_EXPORTER_ROLE,
)

site_auths.update_role(RANDO_UNBLINDED, PII, name=PHARMACIST_ROLE)
site_auths.update_role(RANDO_BLINDED, PII, name=SITE_PHARMACIST_ROLE)

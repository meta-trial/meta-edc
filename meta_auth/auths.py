from edc_action_item.auth_objects import (
    ACTION_ITEM,
    ACTION_ITEM_EXPORT,
    ACTION_ITEM_VIEW_ONLY,
)
from edc_adverse_event.auth_objects import (
    AE,
    AE_EXPORT,
    AE_REVIEW,
    AE_SUPER,
    TMG,
    TMG_REVIEW,
    TMG_ROLE,
)
from edc_appointment.auth_objects import (
    APPOINTMENT,
    APPOINTMENT_EXPORT,
    APPOINTMENT_VIEW,
)
from edc_auth.auth_objects import (
    AUDITOR,
    AUDITOR_ROLE,
    CLINIC,
    CLINICIAN_ROLE,
    CLINICIAN_SUPER_ROLE,
    NURSE_ROLE,
    PHARMACIST_ROLE,
    SITE_PHARMACIST_ROLE,
)
from edc_auth.site_auths import site_auths
from edc_data_manager.auth_objects import (
    DATA_MANAGER_EXPORT,
    DATA_MANAGER_ROLE,
    DATA_QUERY,
    SITE_DATA_MANAGER_ROLE,
)
from edc_export.auth_objects import DATA_EXPORTER_ROLE
from edc_randomization.auth_objects import RANDO
from edc_screening.auth_objects import SCREENING, SCREENING_SUPER, SCREENING_VIEW
from edc_unblinding.auth_objects import UNBLINDING_REQUESTORS
from sarscov2.auth import SARSCOV2, sarscov2_codenames

from meta_edc.meta_version import get_meta_version

from .auth_objects import (
    META_AUDITOR,
    META_CLINIC,
    META_CLINIC_SUPER,
    clinic_codenames,
    clinic_super_codenames,
)

# meta groups
site_auths.add_group(*clinic_codenames, name=META_AUDITOR, view_only=True)
site_auths.add_group(*clinic_codenames, name=META_CLINIC, no_delete=True)
site_auths.add_group(*clinic_super_codenames, name=META_CLINIC_SUPER)
# site_auths.add_group(*clinic_codenames, name=META_EXPORT, convert_to_export=True)


# meta roles

# update edc roles
site_auths.update_role(
    ACTION_ITEM,
    AE,
    APPOINTMENT,
    DATA_QUERY,
    META_CLINIC,
    SCREENING,
    UNBLINDING_REQUESTORS,
    name=CLINICIAN_ROLE,
)

site_auths.update_role(
    ACTION_ITEM,
    AE_SUPER,
    APPOINTMENT,
    DATA_QUERY,
    META_CLINIC_SUPER,
    SCREENING_SUPER,
    UNBLINDING_REQUESTORS,
    name=CLINICIAN_SUPER_ROLE,
)

site_auths.update_role(
    ACTION_ITEM,
    AE,
    APPOINTMENT,
    DATA_QUERY,
    META_CLINIC,
    SCREENING,
    name=NURSE_ROLE,
)

site_auths.update_role(
    ACTION_ITEM,
    AE,
    APPOINTMENT,
    CLINIC,
    META_CLINIC,
    TMG,
    name=DATA_MANAGER_ROLE,
)

site_auths.update_role(ACTION_ITEM, UNBLINDING_REQUESTORS, name=TMG_ROLE)

site_auths.update_role(
    ACTION_ITEM_VIEW_ONLY,
    AE_REVIEW,
    APPOINTMENT_VIEW,
    META_AUDITOR,
    SCREENING_VIEW,
    TMG_REVIEW,
    name=AUDITOR_ROLE,
)

site_auths.update_role(
    AUDITOR,
    ACTION_ITEM,
    AE_REVIEW,
    DATA_QUERY,
    META_AUDITOR,
    SCREENING_VIEW,
    TMG_REVIEW,
    name=SITE_DATA_MANAGER_ROLE,
)

site_auths.update_role(RANDO, name=PHARMACIST_ROLE)

site_auths.update_role(RANDO, name=SITE_PHARMACIST_ROLE)

# data export
site_auths.update_role(
    ACTION_ITEM_EXPORT,
    AE_EXPORT,
    APPOINTMENT_EXPORT,
    DATA_MANAGER_EXPORT,
    name=DATA_EXPORTER_ROLE,
)


if get_meta_version() == 2:
    site_auths.add_group(*sarscov2_codenames, name=SARSCOV2)

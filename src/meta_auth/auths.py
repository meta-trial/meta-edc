from edc_action_item.auth_objects import ACTION_ITEM, ACTION_ITEM_EXPORT
from edc_appointment.auth_objects import APPOINTMENT_EXPORT
from edc_auth.constants import (
    AUDITOR,
    AUDITOR_ROLE,
    CLINIC,
    CLINIC_SUPER,
    CLINICIAN_ROLE,
    CLINICIAN_SUPER_ROLE,
    NURSE_ROLE,
    PII,
    TMG_ROLE,
)
from edc_auth.site_auths import site_auths
from edc_data_manager.auth_objects import DATA_MANAGER_EXPORT, DATA_MANAGER_ROLE
from edc_export.constants import DATA_EXPORTER_ROLE
from edc_mnsi.auth_objects import MNSI, MNSI_SUPER, MNSI_VIEW
from edc_pharmacy.auth_objects import (
    PHARMACIST_ROLE,
    PHARMACY_PRESCRIBER,
    SITE_PHARMACIST_ROLE,
)
from edc_qareports.auth_objects import QA_REPORTS_AUDIT_ROLE, QA_REPORTS_ROLE
from edc_qol.auth_objects import QOL, QOL_SUPER, QOL_VIEW
from edc_randomization.auth_objects import RANDO_BLINDED, RANDO_UNBLINDED
from edc_screening.auth_objects import SCREENING, SCREENING_SUPER, SCREENING_VIEW
from edc_subject_dashboard.auths import SUBJECT_VIEW
from edc_unblinding.auth_objects import UNBLINDING_REQUESTORS

from .auth_objects import (
    META_PHARMACIST,
    META_REPORTS,
    META_REPORTS_AUDIT,
    clinic_codenames,
    meta_pharmacy_codenames,
    reports_codenames,
    screening_codenames,
)

site_auths.add_group(*reports_codenames, name=META_REPORTS)
site_auths.add_group(*reports_codenames, name=META_REPORTS_AUDIT, view_only=True)
site_auths.add_group(*meta_pharmacy_codenames, name=META_PHARMACIST)

# update edc_auth default groups
site_auths.update_group(*clinic_codenames, name=AUDITOR, view_only=True)
site_auths.update_group(*clinic_codenames, name=CLINIC, no_delete=True)
site_auths.update_group(*clinic_codenames, name=CLINIC_SUPER)
site_auths.update_group(*screening_codenames, name=SCREENING, no_delete=True)
site_auths.update_group(*screening_codenames, name=SCREENING_SUPER)
site_auths.update_group(*screening_codenames, name=SCREENING_VIEW, view_only=True)

# update edc_auth default roles
site_auths.update_role(
    UNBLINDING_REQUESTORS,
    MNSI,
    QOL,
    PHARMACY_PRESCRIBER,
    name=CLINICIAN_ROLE,
)
site_auths.update_role(
    MNSI_SUPER,
    QOL_SUPER,
    UNBLINDING_REQUESTORS,
    PHARMACY_PRESCRIBER,
    name=CLINICIAN_SUPER_ROLE,
)
site_auths.update_role(MNSI, QOL, name=NURSE_ROLE)
site_auths.update_role(MNSI_VIEW, QOL_VIEW, name=AUDITOR_ROLE)
site_auths.update_role(
    ACTION_ITEM_EXPORT,
    APPOINTMENT_EXPORT,
    DATA_MANAGER_EXPORT,
    name=DATA_EXPORTER_ROLE,
)
site_auths.update_role(RANDO_UNBLINDED, PII, META_PHARMACIST, name=PHARMACIST_ROLE)
site_auths.update_role(RANDO_BLINDED, PII, META_PHARMACIST, name=SITE_PHARMACIST_ROLE)
site_auths.update_role(SUBJECT_VIEW, SCREENING_VIEW, name=DATA_MANAGER_ROLE)
site_auths.update_role(
    SUBJECT_VIEW, SCREENING_VIEW, ACTION_ITEM, UNBLINDING_REQUESTORS, name=TMG_ROLE
)
site_auths.update_role(META_REPORTS, name=QA_REPORTS_ROLE)
site_auths.update_role(META_REPORTS_AUDIT, name=QA_REPORTS_AUDIT_ROLE)

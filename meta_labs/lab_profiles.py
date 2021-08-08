from django.conf import settings
from edc_lab import LabProfile, RequisitionPanelGroup
from edc_lab_panel.panels import (
    blood_glucose_panel,
    blood_glucose_poc_panel,
    fbc_panel,
    hba1c_panel,
    hba1c_poc_panel,
    insulin_panel,
    lft_panel,
    lipids_panel,
    rft_panel,
)

from meta_edc.meta_version import PHASE_THREE, get_meta_version

chemistry_panel = RequisitionPanelGroup(
    lft_panel,
    rft_panel,
    lipids_panel,
    name="chemistry",
    verbose_name="Chemistry: LFT, RFT, Lipids",
    reference_range_collection_name="meta",
)

subject_lab_profile = LabProfile(
    name="subject_lab_profile",
    requisition_model=settings.SUBJECT_REQUISITION_MODEL,
    reference_range_collection_name="meta",
)

if get_meta_version() == PHASE_THREE:
    subject_lab_profile.add_panel(blood_glucose_panel)
    subject_lab_profile.add_panel(fbc_panel)
    subject_lab_profile.add_panel(hba1c_panel)
    subject_lab_profile.add_panel(insulin_panel)
    subject_lab_profile.add_panel(lft_panel)
    subject_lab_profile.add_panel(lipids_panel)
    subject_lab_profile.add_panel(rft_panel)
else:
    subject_lab_profile.add_panel(fbc_panel)
    subject_lab_profile.add_panel(blood_glucose_panel)
    subject_lab_profile.add_panel(blood_glucose_poc_panel)
    subject_lab_profile.add_panel(hba1c_panel)
    subject_lab_profile.add_panel(hba1c_poc_panel)
    # subject_lab_profile.add_panel(lipids_panel)
    # subject_lab_profile.add_panel(lft_panel)
    # subject_lab_profile.add_panel(rft_panel)
    subject_lab_profile.add_panel_group(chemistry_panel)

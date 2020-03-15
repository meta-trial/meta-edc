from edc_lab import RequisitionPanel

from .processing_profiles import (
    fbc_processing,
    hba1c_processing,
    chemistry_processing,
    blood_glucose_processing,
    poc_processing,
)


hba1c_panel = RequisitionPanel(
    name="hba1c",
    verbose_name="HbA1c (Venous)",
    processing_profile=hba1c_processing,
    abbreviation="HBA1C",
)


hba1c_poc_panel = RequisitionPanel(
    name="hba1c_poc",
    verbose_name="HbA1c (POC)",
    abbreviation="HBA1C_POC",
    processing_profile=poc_processing,
)


fbc_panel = RequisitionPanel(
    name="fbc", verbose_name="Full Blood Count", processing_profile=fbc_processing
)

blood_glucose_panel = RequisitionPanel(
    name="blood_glucose",
    verbose_name="Blood Glucose (Venous)",
    abbreviation="BGL",
    processing_profile=blood_glucose_processing,
)

blood_glucose_poc_panel = RequisitionPanel(
    name="blood_glucose_poc",
    verbose_name="Blood Glucose (POC)",
    abbreviation="BGL-POC",
    processing_profile=poc_processing,
)

chemistry_panel = RequisitionPanel(
    name="chemistry",
    verbose_name="Chemistry: Creat, Urea, Elec, ALT, etc",
    abbreviation="CHEM",
    processing_profile=chemistry_processing,
)

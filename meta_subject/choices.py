from edc_constants.constants import (
    ABSENT,
    MICROSCOPY,
    NO,
    NO_EXAM,
    NOT_APPLICABLE,
    OTHER,
    PRESENT,
    PRESENT_WITH_REINFORCEMENT,
    RAPID_TEST,
    YES,
)
from edc_reportable.constants import GRADE3, GRADE4
from edc_visit_tracking.constants import MISSED_VISIT, SCHEDULED, UNSCHEDULED

from .constants import APPT, APPT_OTHER

ACTIVITY_CHOICES = (
    ("working", "Working"),
    ("studying", "Studying"),
    ("caring_for_children", "Caring for children"),
    (OTHER, "Other, please specify"),
)


CHILDCARE_CHOICES = (
    (NOT_APPLICABLE, "Not applicable"),
    ("working", "Working"),
    ("studying", "Studying"),
    ("caring_for_children", "Caring for children"),
    ("house_maintenance", "House maintenance"),
    ("nothing", "Nothing"),
    (OTHER, "Other, specify"),
)

DYSLIPIDAEMIA_RX_CHOICES = (
    ("atorvastatin", "Atorvastatin"),
    ("rosuvastatin", "Rosuvastatin"),
    (OTHER, "Other, specify below ..."),
    (NOT_APPLICABLE, "Not applicable"),
)

FOLLOWUP_REASONS = (
    (APPT, "Study appointment"),
    (APPT_OTHER, "Other routine appointment"),
    (UNSCHEDULED, "Unschedule visit"),
    (OTHER, "Other reason, specify below ..."),
)

GRADE34_CHOICES = (
    (GRADE3, "Grade 3"),
    (GRADE4, "Grade 4"),
    (NOT_APPLICABLE, "Not applicable"),
)

INFO_SOURCE = (
    ("hospital_notes", "Hospital notes"),
    ("outpatient_cards", "Outpatient cards"),
    ("patient", "Patient"),
    ("collateral_history", "Collateral History from relative/guardian"),
    (NOT_APPLICABLE, "Not applicable (if missed)"),
    (OTHER, "Other"),
)

FUNDOSCOPY_CHOICES = (
    ("no_retinopathy", "No retinopathy"),
    ("background_retinopathy", "Background retinopathy"),
    ("pre_proliferative_retinopathy", "Pre-proliferative retinopathy"),
    ("proliferative_retinopathy", "Proliferative retinopathy"),
    ("maculopathy", "Maculopathy"),
    (NO_EXAM, "Exam not performed"),
)

MALARIA_TEST_CHOICES = (
    (RAPID_TEST, "Rapid test"),
    (MICROSCOPY, "Microscopy"),
    (NOT_APPLICABLE, "Not applicable"),
)

PAYEE_CHOICES = (
    ("own_cash", "Own cash"),
    ("insurance", "Insurance"),
    ("relative", "Relative of others paying"),
    ("free", "Free drugs from the pharmacy"),
    (NOT_APPLICABLE, "Not applicable"),
)

PRESENT_ABSENT_NOEXAM = (
    (PRESENT, "Present"),
    (ABSENT, "Absent"),
    (NO_EXAM, "Exam not performed"),
)

PRESENT_ABSENT_NOEXAM_NDS = (
    (PRESENT, "Present"),
    (PRESENT_WITH_REINFORCEMENT, "Present with reinforcement"),
    (ABSENT, "Absent"),
    (NO_EXAM, "Exam not performed"),
)
# 0 = Present   1 = Present with reinforcement   2 = Absent

TRANSPORT_CHOICES = (
    ("bus", "Bus"),
    ("train", "Train"),
    ("ambulance", "Ambulance"),
    ("private_taxi", "Private taxi"),
    ("own_bicycle", "Own bicycle"),
    ("hired_motorbike", "Hired motorbike"),
    ("own_car", "Own car"),
    ("own_motorbike", "Own motorbike"),
    ("hired_bicycle", "Hired bicycle"),
    ("foot", "Foot"),
    (OTHER, "Other, specify"),
)


VISIT_UNSCHEDULED_REASON = (
    ("patient_unwell_outpatient", "Patient unwell (outpatient)"),
    ("patient_hospitalised", "Patient hospitalised"),
    ("routine_non_study", "Routine appointment (non-study)"),
    ("recurrence_symptoms", "Recurrence of symptoms"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

VISIT_REASON = (
    (SCHEDULED, "Scheduled visit"),
    (UNSCHEDULED, "Unscheduled visit"),
    (MISSED_VISIT, "Missed visit"),
)

WEIGHT_DETERMINATION = (("estimated", "Estimated"), ("measured", "Measured"))

YES_NO_NO_EXAM = (
    (YES, YES),
    (NO, NO),
    (NO_EXAM, "Exam not performed"),
)

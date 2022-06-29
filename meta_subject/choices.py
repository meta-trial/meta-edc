from edc_constants.constants import (
    ABSENT,
    CLOSED,
    DEAD,
    MICROSCOPY,
    NEW,
    NO,
    NO_EXAM,
    NOT_APPLICABLE,
    OPEN,
    OTHER,
    PATIENT,
    PRESENT,
    PRESENT_WITH_REINFORCEMENT,
    RAPID_TEST,
    YES,
)
from edc_reportable.constants import GRADE3, GRADE4
from edc_visit_tracking.constants import MISSED_VISIT, SCHEDULED, UNSCHEDULED

from meta_ae.choices import INFORMANT_RELATIONSHIP
from meta_ae.constants import HOSPITAL_CLINIC

from .constants import (
    ALL_OF_THE_TIME,
    APPT,
    APPT_OTHER,
    GOOD_BIT_OF_THE_TIME,
    LITTLE_OF_THE_TIME,
    LIVE_AT_TERM,
    LIVE_PRETERM,
    MOST_OF_THE_TIME,
    NO_COMPLICATIONS,
    NONE_OF_THE_TIME,
    SOME_OF_THE_TIME,
)

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

DELIVERY_INFO_SOURCE = (
    (PATIENT, "Study participant"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

DELIVERY_LOCATIONS = (
    ("home", "At home"),
    (HOSPITAL_CLINIC, "Hospital / Clinic"),
    (OTHER, "Other location, specify"),
    (NOT_APPLICABLE, "Not applicable"),
)

DESCRIBE_HEALTH_CHOICES = (
    ("excellent", "Excellent"),
    ("very_good", "Very good"),
    ("good", "Good"),
    ("fair", "Fair"),
    ("poor", "Poor"),
)

DYSLIPIDAEMIA_RX_CHOICES = (
    ("atorvastatin", "Atorvastatin"),
    ("rosuvastatin", "Rosuvastatin"),
    (OTHER, "Other, specify below ..."),
    (NOT_APPLICABLE, "Not applicable"),
)

FEELING_DURATION_CHOICES = (
    (ALL_OF_THE_TIME, "All of the time"),
    (MOST_OF_THE_TIME, "Most of the time"),
    (GOOD_BIT_OF_THE_TIME, " A good bit of the time"),
    (SOME_OF_THE_TIME, "Some of the time"),
    (LITTLE_OF_THE_TIME, "A little of the time"),
    (NONE_OF_THE_TIME, "None of the time"),
)


FETAL_OUTCOMES = (
    (LIVE_AT_TERM, "Live birth at term"),
    (LIVE_PRETERM, "Live birth preterm"),
    ("stillbirth", "Stillbirth"),
    ("miscarriage", "Miscarriage"),
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

HEALTH_LIMITED_CHOICES = (
    ("limited_a_lot", "YES, limited a lot"),
    ("limited_a_little", "YES, limited a little"),
    ("not_limited_at_all", "NO, not at all limited"),
)

INFO_SOURCE = (
    ("hospital_notes", "Hospital notes"),
    ("outpatient_cards", "Outpatient cards"),
    ("patient", "Patient"),
    ("collateral_history", "Collateral History from relative/guardian"),
    (NOT_APPLICABLE, "Not applicable (if missed)"),
    (OTHER, "Other"),
)

DELIVERY_INFORMANT_RELATIONSHIP = list(INFORMANT_RELATIONSHIP)
DELIVERY_INFORMANT_RELATIONSHIP.extend(
    [
        (HOSPITAL_CLINIC, "Hospital / Clinic records"),
        (NOT_APPLICABLE, "Not applicable"),
    ]
)
DELIVERY_INFORMANT_RELATIONSHIP = tuple(DELIVERY_INFORMANT_RELATIONSHIP)

INTERFERENCE_DURATION_CHOICES = (
    (ALL_OF_THE_TIME, "All of the time"),
    (MOST_OF_THE_TIME, "Most of the time"),
    (SOME_OF_THE_TIME, "Some of the time"),
    (LITTLE_OF_THE_TIME, "A little of the time"),
    (NONE_OF_THE_TIME, "None of the time"),
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

MATERNAL_OUTCOMES = (
    (NO_COMPLICATIONS, "No complications"),
    ("complications_full_recovery", "Complications with full recovery"),
    ("complications_ongoing_recovery", "Complications with ongoing recovery"),
    (DEAD, "Maternal mortality"),
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

REPORT_STATUS = (
    (NEW, "New"),
    (OPEN, "Open. Some information is still pending."),
    (CLOSED, "Closed. This report is complete"),
)


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

WORK_PAIN_INTERFERENCE_CHOICES = (
    ("not_at_all", "Not at all"),
    ("a_little_bit", "A little bit"),
    ("moderately", "Moderately"),
    ("quite_a-bit", "Quite a bit"),
    ("extremely", "Extremely"),
)

YES_NO_NO_EXAM = (
    (YES, YES),
    (NO, NO),
    (NO_EXAM, "Exam not performed"),
)

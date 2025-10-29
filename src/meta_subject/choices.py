from clinicedc_constants import (
    ABSENT,
    CLOSED,
    DEAD,
    GRADE3,
    GRADE4,
    NEW,
    NO,
    NO_EXAM,
    NOT_APPLICABLE,
    OPEN,
    OTHER,
    PATIENT,
    PENDING,
    PRESENT,
    PRESENT_WITH_REINFORCEMENT,
    YES,
)
from django.utils.translation import gettext_lazy as _
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
    ("working", _("Working")),
    ("studying", _("Studying")),
    ("caring_for_children", _("Caring for children")),
    (OTHER, _("Other, please specify")),
)


CHILDCARE_CHOICES = (
    (NOT_APPLICABLE, _("Not applicable")),
    ("working", _("Working")),
    ("studying", _("Studying")),
    ("caring_for_children", _("Caring for children")),
    ("house_maintenance", _("House maintenance")),
    ("nothing", _("Nothing")),
    (OTHER, _("Other, specify")),
)

DELIVERY_INFO_SOURCE = (
    (PATIENT, _("Study participant")),
    (OTHER, _("Other")),
    (NOT_APPLICABLE, _("Not applicable")),
)

DELIVERY_LOCATIONS = (
    ("home", _("At home")),
    (HOSPITAL_CLINIC, _("Hospital / Clinic")),
    (OTHER, _("Other location, specify")),
    (NOT_APPLICABLE, _("Not applicable")),
)

DESCRIBE_HEALTH_CHOICES = (
    ("excellent", _("Excellent")),
    ("very_good", _("Very good")),
    ("good", _("Good")),
    ("fair", _("Fair")),
    ("poor", _("Poor")),
)

DYSLIPIDAEMIA_RX_CHOICES = (
    ("atorvastatin", "Atorvastatin"),
    ("rosuvastatin", "Rosuvastatin"),
    (OTHER, _("Other, specify below ...")),
    (NOT_APPLICABLE, _("Not applicable")),
)

ENDPOINT_CHOICES = (
    (YES, _(YES)),
    (PENDING, _("No. A repeat FBG will be scheduled")),
    (NO, _(NO)),
    (NOT_APPLICABLE, _("Not applicable")),
)

FEELING_DURATION_CHOICES = (
    (ALL_OF_THE_TIME, _("All of the time")),
    (MOST_OF_THE_TIME, _("Most of the time")),
    (GOOD_BIT_OF_THE_TIME, _("A good bit of the time")),
    (SOME_OF_THE_TIME, _("Some of the time")),
    (LITTLE_OF_THE_TIME, _("A little of the time")),
    (NONE_OF_THE_TIME, _("None of the time")),
)


FETAL_OUTCOMES = (
    (LIVE_AT_TERM, _("Live birth at term")),
    (LIVE_PRETERM, _("Live birth preterm")),
    ("stillbirth", _("Stillbirth")),
    ("miscarriage", _("Miscarriage")),
)

FOLLOWUP_REASONS = (
    (APPT, _("Study appointment")),
    (APPT_OTHER, _("Other routine appointment")),
    (UNSCHEDULED, _("Unschedule visit")),
    (OTHER, _("Other reason, specify below ...")),
)

GRADE34_CHOICES = (
    (GRADE3, _("Grade %(num)s") % {"num": 3}),
    (GRADE4, _("Grade %(num)s") % {"num": 4}),
    (NOT_APPLICABLE, _("Not applicable")),
)

HEALTH_LIMITED_CHOICES = (
    ("limited_a_lot", _("YES, limited a lot")),
    ("limited_a_little", _("YES, limited a little")),
    ("not_limited_at_all", _("NO, not at all limited")),
)

INFO_SOURCE = (
    ("hospital_notes", _("Hospital notes")),
    ("outpatient_cards", _("Outpatient cards")),
    ("patient", _("Patient")),
    ("collateral_history", _("Collateral History from relative/guardian")),
    (NOT_APPLICABLE, _("Not applicable (if missed)")),
    (OTHER, _("Other")),
)

DELIVERY_INFORMANT_RELATIONSHIP = list(INFORMANT_RELATIONSHIP)
DELIVERY_INFORMANT_RELATIONSHIP.extend(
    [
        (HOSPITAL_CLINIC, _("Hospital / Clinic records")),
        (NOT_APPLICABLE, _("Not applicable")),
    ]
)
DELIVERY_INFORMANT_RELATIONSHIP = tuple(DELIVERY_INFORMANT_RELATIONSHIP)

INTERFERENCE_DURATION_CHOICES = (
    (ALL_OF_THE_TIME, _("All of the time")),
    (MOST_OF_THE_TIME, _("Most of the time")),
    (SOME_OF_THE_TIME, _("Some of the time")),
    (LITTLE_OF_THE_TIME, _("A little of the time")),
    (NONE_OF_THE_TIME, _("None of the time")),
)

FUNDOSCOPY_CHOICES = (
    ("no_retinopathy", _("No retinopathy")),
    ("background_retinopathy", _("Background retinopathy")),
    ("pre_proliferative_retinopathy", _("Pre-proliferative retinopathy")),
    ("proliferative_retinopathy", _("Proliferative retinopathy")),
    ("maculopathy", _("Maculopathy")),
    (NO_EXAM, _("Exam not performed")),
)

MATERNAL_OUTCOMES = (
    (NO_COMPLICATIONS, _("No complications")),
    ("complications_full_recovery", _("Complications with full recovery")),
    ("complications_ongoing_recovery", _("Complications with ongoing recovery")),
    (DEAD, _("Maternal mortality")),
    (NOT_APPLICABLE, _("Not applicable")),
)

PAYEE_CHOICES = (
    ("own_cash", _("Own cash")),
    ("insurance", _("Insurance")),
    ("relative", _("Relative of others paying")),
    ("free", _("Free drugs from the pharmacy")),
    (NOT_APPLICABLE, _("Not applicable")),
)

PRESENT_ABSENT_NOEXAM = (
    (PRESENT, _("Present")),
    (ABSENT, _("Absent")),
    (NO_EXAM, _("Exam not performed")),
)

PRESENT_ABSENT_NOEXAM_NDS = (
    (PRESENT, _("Present")),
    (PRESENT_WITH_REINFORCEMENT, _("Present with reinforcement")),
    (ABSENT, _("Absent")),
    (NO_EXAM, _("Exam not performed")),
)
# 0 = Present   1 = Present with reinforcement   2 = Absent

REPORT_STATUS = (
    (NEW, _("New")),
    (OPEN, _("Open. Some information is still pending.")),
    (CLOSED, _("Closed. This report is complete")),
)


TRANSPORT_CHOICES = (
    ("bus", _("Bus")),
    ("train", _("Train")),
    ("ambulance", _("Ambulance")),
    ("private_taxi", _("Private taxi")),
    ("own_bicycle", _("Own bicycle")),
    ("hired_motorbike", _("Hired motorbike")),
    ("own_car", _("Own car")),
    ("own_motorbike", _("Own motorbike")),
    ("hired_bicycle", _("Hired bicycle")),
    ("foot", _("Foot")),
    (OTHER, _("Other, specify")),
)


VISIT_UNSCHEDULED_REASON = (
    ("patient_unwell_outpatient", _("Patient unwell (outpatient)")),
    ("patient_hospitalised", _("Patient hospitalised")),
    ("routine_non_study", _("Routine appointment (non-study)")),
    ("recurrence_symptoms", _("Recurrence of symptoms")),
    (OTHER, _("Other")),
    (NOT_APPLICABLE, _("Not applicable")),
)

VISIT_REASON = (
    (SCHEDULED, _("Scheduled visit")),
    (UNSCHEDULED, _("Unscheduled visit")),
    (MISSED_VISIT, _("Missed visit")),
)

WEIGHT_DETERMINATION = (("estimated", _("Estimated")), ("measured", _("Measured")))

WORK_PAIN_INTERFERENCE_CHOICES = (
    ("not_at_all", _("Not at all")),
    ("a_little_bit", _("A little bit")),
    ("moderately", _("Moderately")),
    ("quite_a-bit", _("Quite a bit")),
    ("extremely", _("Extremely")),
)

YES_NO_NO_EXAM = (
    (YES, _(YES)),
    (NO, _(NO)),
    (NO_EXAM, _("Exam not performed")),
)

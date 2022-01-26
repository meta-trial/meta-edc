from edc_constants.constants import NOT_APPLICABLE, OTHER

# PHASE_THREE ONLY
CLINICAL_WITHDRAWAL_REASONS = (
    ("pregnancy", "Pregnancy"),
    ("kidney_disease", "Development of chronic kidney disease"),
    ("liver_disease", "Development of chronic liver disease"),
    ("intercurrent_illness", "Intercurrent illness which prevents further treatment"),
    ("investigator_decision", "Investigator decision"),
    (
        OTHER,
        (
            "Other condition that justifies the discontinuation of "
            "treatment in the clinician’s opinion (specify below)"
        ),
    ),
)

# PHASE_THREE ONLY
TOXICITY_WITHDRAWAL_REASONS = (
    ("lactic_acidosis", "Development of lactic acidosis or hyperlactatemia"),
    ("hepatomegaly", "Development of hepatomegaly with steatosis"),
    (OTHER, "Other (specify below)"),
)

LOSS_CHOICES = (
    ("unknown_address", "Changed to an unknown address"),
    ("never_returned", "Did not return despite reminders"),
    ("bad_contact_details", "Inaccurate contact details"),
    (OTHER, "Other"),
)

PROTOCOL_VIOLATION = (
    ("failure_to_obtain_informed_consent", "Failure to obtain informed " "consent"),
    ("enrollment_of_ineligible_patient", "Enrollment of ineligible patient"),
    (
        "screening_procedure not done",
        "Screening procedure required by " "protocol not done",
    ),
    (
        "screening_or_on-study_procedure",
        "Screening or on-study procedure/lab " "work required not done",
    ),
    (
        "incorrect_research_treatment",
        "Incorrect research treatment given to " "patient",
    ),
    (
        "procedure_not_completed",
        "On-study procedure required by protocol not " "completed",
    ),
    ("visit_non-compliance", "Visit non-compliance"),
    ("medication_stopped_early", "Medication stopped early"),
    ("medication_noncompliance", "Medication_noncompliance"),
    (
        "national_regulations_not_met",
        "Standard WPD, ICH-GCP, local/national " "regulations not met",
    ),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

ACTION_REQUIRED = (
    ("remain_on_study", "Participant to remain on trial"),
    ("to_be_withdrawn", "Participant to be withdrawn from trial"),
    (
        "remain_on_study_modified",
        "Patient remains on study but data analysis will be modified",
    ),
)


REASON_STUDY_TERMINATED = ()

from edc_constants.constants import DEAD, NOT_APPLICABLE, OTHER, UNKNOWN

list_data = {
    "edc_adverse_event.aeclassification": [
        ("lactic_acidosis", "Lactic acidosis"),
        ("hepatomegaly_steatosis", "Hepatomegaly with steatosis"),
        ("gastrointestinal_metformin", "Gastrointestinal effects of metformin"),
        # ("anaemia", "Anaemia"),
        # ("diarrhoea", "Diarrhoea"),
        # ("renal_impairment", "Renal impairment"),
        (OTHER, "Other"),
    ],
    "edc_adverse_event.saereason": [
        (NOT_APPLICABLE, "Not applicable"),
        (DEAD, "Death"),
        ("life_threatening", "Life-threatening"),
        ("significant_disability", "Significant disability"),
        (
            "in-patient_hospitalization",
            (
                "In-patient hospitalization or prolongation "
                "(17 or more days from study inclusion)"
            ),
        ),
        (
            "medically_important_event",
            "Medically important event (e.g. Severe thrombophlebitis, Bacteraemia, "
            "recurrence of symptoms not requiring admission, Hospital acquired "
            "pneumonia)",
        ),
    ],
    "edc_adverse_event.causeofdeath": [
        ("art_toxicity", "ART toxicity"),
        ("diarrhea_wasting", "Diarrhea/wasting"),
        (UNKNOWN, "Unknown"),
        (OTHER, "Other"),
    ],
}

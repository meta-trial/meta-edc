from edc_constants.constants import OTHER, NOT_APPLICABLE, DEAD, UNKNOWN
from edc_list_data import PreloadData


list_data = {
    "edc_adverse_event.aeclassification": [
        ("anaemia", "Anaemia"),
        ("diarrhoea", "Diarrhoea"),
        ("renal_impairment", "Renal impairment"),
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

preload_data = PreloadData(list_data=list_data, model_data={}, unique_field_data=None)

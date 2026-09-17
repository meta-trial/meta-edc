from clinicedc_constants import DEAD, NOT_APPLICABLE, OTHER, UNKNOWN

list_data: dict[str, list[tuple[str, str]]] = {
    "edc_adverse_event.aeclassification": [
        ("anaemia", "Anaemia"),
        ("death", "Death"),
        ("dyslipidaemia", "Dyslipidaemia"),
        ("gastrointestinal_metformin", "Gastrointestinal effects of metformin"),
        ("hepatomegaly_steatosis", "Hepatomegaly with steatosis"),
        ("hepatotoxicity", "Hepatotoxicity"),
        ("hypercholesterolaemia", "Hypercholesterolaemia"),
        ("hyperlipidaemia", "Hyperlipidaemia"),
        ("hyperamylasaemia", "Hyperamylasaemia"),
        ("hyperuricaemia", "Hyperuricaemia"),
        ("hypertriglyceridaemia", "Hypertriglyceridaemia"),
        ("hypoalbuminaemia", "Hypoalbuminaemia"),
        ("hypertension", "Hypertension"),
        ("lactic_acidosis", "Lactic acidosis"),
        ("leukopenia", "Leukopenia"),
        ("liver_insufficiency", "Liver insufficiency"),
        ("pancytopenia", "Pancytopenia"),
        ("renal_insufficiency", "Renal insufficiency"),
        ("thrombocytopenia", "Thrombocytopenia"),
        (OTHER, "Other"),
        (NOT_APPLICABLE, "Not applicable"),
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

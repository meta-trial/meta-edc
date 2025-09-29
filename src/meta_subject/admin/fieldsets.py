def get_htn_fieldset(part=None):
    fields = (
        "htn_diagnosis",
        "on_htn_treatment",
        "htn_treatment",
        "other_htn_treatment",
        "dyslipidaemia_diagnosis",
        "on_dyslipidaemia_treatment",
        "dyslipidaemia_rx",
        "concomitant_conditions",
        "concomitant_medications",
    )

    return (
        f"Part {part}: Hypertension",
        {"fields": fields},
    )


def get_hiv_fieldset(part=None):
    title = "HIV, ARVs and other prophylaxis"
    if part:
        title = f"Part {part}: {title}"
    # TODO: previous_arv_regimen_start_date is PHASE 3 only
    fields = (
        "hiv_diagnosis_date",
        "arv_initiation_date",
        "viral_load",
        "viral_load_date",
        "cd4",
        "cd4_date",
        "current_arv_regimen",
        "other_current_arv_regimen",
        "current_arv_regimen_start_date",
        "has_previous_arv_regimen",
        "previous_arv_regimen",
        "other_previous_arv_regimen",
        "previous_arv_regimen_start_date",
        "on_oi_prophylaxis",
        "oi_prophylaxis",
        "other_oi_prophylaxis",
    )
    return (
        title,
        {"fields": fields},
    )


def get_other_history_fieldset(part=None):
    return (
        f"Part {part}: Other history",
        {
            "fields": (
                "current_smoker",
                "former_smoker",
                "dm_symptoms",
                "other_dm_symptoms",
                "dm_in_family",
            )
        },
    )

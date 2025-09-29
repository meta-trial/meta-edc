def get_blood_pressure_fields() -> tuple[str, ...]:
    return (
        "sys_blood_pressure_one",
        "dia_blood_pressure_one",
        "sys_blood_pressure_two",
        "dia_blood_pressure_two",
        "severe_htn",
    )


def get_respiratory_o2_fields() -> tuple[str, ...]:
    return ("respiratory_rate",)

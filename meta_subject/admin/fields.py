from meta_edc.meta_version import PHASE_THREE, get_meta_version


def get_blood_pressure_fields():
    if get_meta_version() == PHASE_THREE:
        return [
            "sys_blood_pressure_one",
            "dia_blood_pressure_one",
            "sys_blood_pressure_two",
            "dia_blood_pressure_two",
            "severe_htn",
        ]
    else:
        return [
            "sys_blood_pressure",
            "dia_blood_pressure",
        ]

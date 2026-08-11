from .ae_final_classification_admin import AeFinalClassificationAdmin
from .ae_followup_admin import AeFollowupAdmin
from .ae_initial_admin import AeInitialAdmin
from .ae_susar_admin import AeSusarAdmin
from .ae_tmg_admin import AeTmgAdmin
from .death_report_admin import DeathReportAdmin
from .death_report_tmg_admin import DeathReportTmgAdmin
from .death_report_tmg_second_admin import DeathReportTmgSecondAdmin
from .hospitalization_admin import HospitalizationAdmin

__all__ = [
    "AeFinalClassificationAdmin",
    "AeFollowupAdmin",
    "AeInitialAdmin",
    "AeSusarAdmin",
    "AeTmgAdmin",
    "DeathReportAdmin",
    "DeathReportTmgAdmin",
    "DeathReportTmgSecondAdmin",
    "HospitalizationAdmin",
]
